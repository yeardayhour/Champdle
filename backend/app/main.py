"""
Champdle 메인 FastAPI 웹 애플리케이션 모듈
"""

from typing import List
import os
from random import Random
from datetime import datetime
import json
import re

from fastapi import FastAPI, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import numpy as np

from .models import ErrorMessage, GuessResult, Champion, LocalName, PlayRecord
from .similarity import calculate_ranks

# 환경 변수 기본값 설정
if "LOLMANTLE_CHAMPIONS" not in os.environ:
    os.environ["LOLMANTLE_CHAMPIONS"] = "/data/champions.csv"

if "LOLMANTLE_NAME_MAP" not in os.environ:
    os.environ["LOLMANTLE_NAME_MAP"] = "/data/name_map.csv"

RANDOM = Random(os.environ.get("LOLMANTLE_RANDOM_SEED", 20260725))

# 챔피언 데이터 파일 경로 산출
champions_path = os.environ.get("LOLMANTLE_CHAMPIONS", "../data/champions.csv")
name_map_path = os.environ.get("LOLMANTLE_NAME_MAP", "../data/name_map.csv")

if not os.path.exists(champions_path):
    champions_path = os.path.join(os.path.dirname(__file__), '../../data/champions.csv')
if not os.path.exists(name_map_path):
    name_map_path = os.path.join(os.path.dirname(__file__), '../../data/name_map.csv')

# CSV 데이터로드
CHAMPIONS = pd.read_csv(champions_path).replace({np.nan: None})
CHAMPION_NAME_MAP = pd.read_csv(name_map_path)

CHAMPION_SIZE = len(CHAMPIONS.index)
SECRET_INDEXES = RANDOM.sample(range(CHAMPION_SIZE), k=CHAMPION_SIZE)

app = FastAPI(
    title="Champdle API",
    description="League of Legends Champion Wordle-like Game API",
    docs_url=None if os.environ.get("LOLMANTLE_PRODUCTION", False) else "/docs",
    redoc_url=None,
)

# CORS 미들웨어 구성
if not os.environ.get("LOLMANTLE_PRODUCTION", False):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            os.environ.get("LOLMANTLE_CORS_ORIGIN", "http://localhost:3000")
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def secret_index(puzzle_number: int) -> int:
    """
    퍼즐 번호에 대응하는 오늘의 정답 챔피언 인덱스 산출
    :param puzzle_number: 퍼즐 번호 (0~9999 일수 또는 YYMMDD 날짜)
    :return: 시크릿 정답 인덱스 (0 ~ CHAMPION_SIZE-1)
    """
    if puzzle_number <= 9999:
        days_since = puzzle_number
    else:
        s = str(puzzle_number)
        yy = int(s[0:2]) + 2000
        mm = int(s[2:4])
        dd = int(s[4:6])
        target_date = datetime(yy, mm, dd)
        origin_date = datetime(2022, 4, 28)
        days_since = (target_date - origin_date).days
    return SECRET_INDEXES[days_since % CHAMPION_SIZE]


def normalize_champion_name(s) -> str:
    """
    챔피언 명칭의 특수문자 및 공백 제거, 소문자 정규화
    :param s: 원본 챔피언 문자열
    :return: 정규화된 텍스트
    """
    if s is None or pd.isna(s):
        return ""
    return re.sub(r"[^a-zA-Z0-9가-힣]", "", str(s)).lower()


@app.get(
    "/languages",
    response_model=List[str],
    responses={
        200: {
            "content": {"application/json": {"example": ["english_name", "local_name"]}},
        },
    },
)
async def languages():
    """지원 언어 명칭 컬럼 리스트 반환"""
    return [name for name in CHAMPION_NAME_MAP.columns]


@app.get(
    "/champions",
    response_model=List[Champion],
)
async def champions():
    """전체 챔피언 메타데이터 리스트 반환"""
    return [CHAMPIONS.loc[i].to_dict() for i in CHAMPIONS.index]


@app.get(
    "/champion_name_map/{language}",
    response_model=List[LocalName],
)
async def champion_name_map(
    language: str = Path(..., description="조회 언어 코드 (ko, en)", example="ko"),
):
    """지정 언어 기준 챔피언 명칭 매핑 리스트 반환"""
    col = "local_name" if language == "ko" else "english_name"
    items = [CHAMPION_NAME_MAP.loc[i] for i in CHAMPION_NAME_MAP.index]
    return [
        LocalName(
            english_name=item["english_name"],
            local_name=item[col],
        )
        for item in items
    ]


@app.get(
    "/rank/{puzzle_number}",
    response_model=List[GuessResult],
)
async def rank(
    puzzle_number: int = Path(..., description="퍼즐 일자 번호", example=260810),
):
    """오늘의 정답 대비 전체 173개 챔피언의 유사도 순위 리스트 계산 및 반환"""
    index = secret_index(puzzle_number)
    ranks = calculate_ranks(
        champion_index=index,
        champions=CHAMPIONS,
    )
    return ranks


@app.get(
    "/guess/{puzzle_number}",
    response_model=GuessResult,
    responses={
        404: {
            "model": ErrorMessage,
            "description": "Champion not found.",
            "content": {
                "application/json": {
                    "example": {
                        "code": ErrorMessage.CodeConstant.CODE_CHAMPION_NOT_FOUND,
                        "message": "Champion not found.",
                    }
                }
            },
        }
    },
)
async def guess(
    puzzle_number: int = Path(..., description="퍼즐 일자 번호", example=260810),
    name: str = Query(..., description="추측한 챔피언 이름/별칭", example="애니"),
):
    """입력한 챔피언 매칭 및 정답과의 유사도/순위 산출 결과 반환"""
    index = secret_index(puzzle_number)
    ranks = calculate_ranks(
        champion_index=index,
        champions=CHAMPIONS,
    )

    clean_target = normalize_champion_name(name)
    if not clean_target:
        return JSONResponse(
            status_code=404,
            content=ErrorMessage(
                code=ErrorMessage.CodeConstant.CODE_CHAMPION_NOT_FOUND,
                message="Champion not found.",
            ).dict(),
        )

    # 1. 계산된 결과 이름 직접 매칭
    for guess_result in ranks:
        if normalize_champion_name(guess_result.name) == clean_target:
            return guess_result

    # 2. CHAMPIONS 메타데이터 컬럼 매칭 (영문, 국문, 별칭)
    matched_index = None
    for idx, row in CHAMPIONS.iterrows():
        n_en = normalize_champion_name(row.get('name_en'))
        n_ko = normalize_champion_name(row.get('name_ko'))
        n_alias = normalize_champion_name(row.get('alias'))
        if clean_target in (n_en, n_ko, n_alias) or n_en.startswith(clean_target) or n_alias.startswith(clean_target):
            matched_index = idx
            break

    # 3. NAME_MAP 언어 맵 컬럼 매칭
    if matched_index is None:
        for _, row in CHAMPION_NAME_MAP.iterrows():
            n_eng = normalize_champion_name(row.get('english_name'))
            n_loc = normalize_champion_name(row.get('local_name'))
            if clean_target in (n_eng, n_loc):
                for idx, c_row in CHAMPIONS.iterrows():
                    if normalize_champion_name(c_row.get('name_en')) == n_eng or normalize_champion_name(c_row.get('alias')) == n_eng:
                        matched_index = idx
                        break
                break

    if matched_index is not None:
        target_name_en = CHAMPIONS.loc[matched_index].get('name_en') or CHAMPIONS.loc[matched_index].get('alias')
        for guess_result in ranks:
            if normalize_champion_name(guess_result.name) == normalize_champion_name(target_name_en):
                return guess_result

    return JSONResponse(
        status_code=404,
        content=ErrorMessage(
            code=ErrorMessage.CodeConstant.CODE_CHAMPION_NOT_FOUND,
            message="Champion not found.",
        ).dict(),
    )


records_path = os.environ.get("LOLMANTLE_RECORDS", "/data/champdle_records.json")


@app.post("/record")
async def save_record(rec: PlayRecord):
    """플레이어 퍼즐 클리어 성적 저장 API"""
    records = []
    if os.path.exists(records_path):
        try:
            with open(records_path, "r", encoding="utf-8") as f:
                records = json.load(f)
        except Exception:
            records = []

    data = rec.dict()
    if not data.get("nickname") or not data["nickname"].strip():
        data["nickname"] = "익명"
    if not data.get("created_at"):
        data["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    records.append(data)

    target_dir = os.path.dirname(os.path.abspath(records_path))
    os.makedirs(target_dir, exist_ok=True)
    with open(records_path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    return {"status": "ok", "message": "기록이 저장되었습니다.", "record": data}


@app.get("/records/{puzzle_number}")
async def get_records(puzzle_number: int):
    """지정 퍼즐 일자의 리더보드 플레이 기록 목록 반환"""
    if not os.path.exists(records_path):
        return []
    try:
        with open(records_path, "r", encoding="utf-8") as f:
            records = json.load(f)
        return [r for r in records if r.get("puzzle_number") == puzzle_number]
    except Exception:
        return []
