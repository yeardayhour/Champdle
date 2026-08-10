"""
Champdle FastAPI Pydantic 모델 정의 모듈
"""

from typing import Optional
from pydantic import BaseModel, Field


class Champion(BaseModel):
    """챔피언 전체 세부 메타데이터 모델"""
    champion_id: int = Field(..., example=1, description="챔피언 출시 순서 고유 ID")
    riot_id: int = Field(..., example=1, description="라이엇 공식 챔피언 ID")
    alias: str = Field(..., example="Annie", description="영문 식별 별칭")
    name_en: str = Field(..., example="Annie", description="영문 이름")
    name_ko: str = Field(..., example="애니", description="국문 이름")
    title_en: str = Field(..., example="the Dark Child", description="영문 칭호")
    title_ko: str = Field(..., example="어둠의 아이", description="국문 칭호")
    gender: str = Field(..., example="Female", description="성별 (Male, Female, Other)")
    species: str = Field(..., example="Human", description="종족")
    region: str = Field(..., example="Noxus", description="소속 지역")
    attack_type: str = Field(..., example="ranged", description="공격 방식 (melee, ranged)")
    tag_1: str = Field(..., example="Mage", description="주 역할군")
    tag_2: Optional[str] = Field(None, example="Support", description="부 역할군")
    partype: Optional[str] = Field(None, example="Mana", description="자원 유형")
    hp_base: float = Field(..., example=560, description="기본 체력")
    hp_max: float = Field(..., example=2192, description="최대 체력")
    mp_base: float = Field(..., example=418, description="기본 마나")
    mp_max: float = Field(..., example=843, description="최대 마나")
    movespeed: float = Field(..., example=335, description="이동 속도")
    armor_base: float = Field(..., example=23, description="기본 방어력")
    armor_max: float = Field(..., example=91, description="최대 방어력")
    spellblock_base: float = Field(..., example=30, description="기본 마법 저항력")
    spellblock_max: float = Field(..., example=52.1, description="최대 마법 저항력")
    attackrange: float = Field(..., example=625, description="공격 사거리")
    hpregen_base: float = Field(..., example=5.5, description="기본 체력 재생")
    hpregen_max: float = Field(..., example=14.85, description="최대 체력 재생")
    mpregen_base: float = Field(..., example=8.0, description="기본 마나 재생")
    mpregen_max: float = Field(..., example=21.6, description="최대 마나 재생")
    crit_base: float = Field(..., example=0.0, description="기본 치명타 확률")
    crit_max: float = Field(..., example=0.0, description="최대 치명타 확률")
    attackdamage_base: float = Field(..., example=50, description="기본 공격력")
    attackdamage_max: float = Field(..., example=50, description="최대 공격력")
    attackspeed_base: float = Field(..., example=0.61, description="기본 공격 속도")
    attackspeed_max: float = Field(..., example=0.751, description="최대 공격 속도")
    image_path: str = Field(..., example='1.png', description="이미지 경로")


class LocalName(BaseModel):
    """영문-현지어 명칭 매핑 모델"""
    english_name: str = Field(..., example="Annie", description="영어 이름")
    local_name: str = Field(..., example="애니", description="현지어 이름")


class ErrorMessage(BaseModel):
    """오류 응답 모델"""
    code: int = Field(..., example=11, description="에러 코드 번호")
    message: str = Field(..., example="Champion not found.", description="에러 메시지")

    class CodeConstant:
        CODE_CHAMPION_NOT_FOUND = 11


class GuessResult(BaseModel):
    """챔피언 추측 계산 결과 모델"""
    name: str = Field(..., example="Annie", description="추측한 챔피언 이름")
    rank: int = Field(..., example=1, description="유사도 순위 (1~173위)")
    similarity: float = Field(..., example=1.0, description="유사도 비율 (0.0~1.0)")
    category_score: Optional[float] = Field(None, example=72.5, description="카테고리 80점 만점 수치")
    stat_score: Optional[float] = Field(None, example=18.2, description="스탯 20점 만점 수치")
    formula_detail: Optional[str] = Field(None, example="카테고리 72.5점 + 스탯 18.2점", description="세부 점수 내역")


class PlayRecord(BaseModel):
    """플레이 기록 저장 요청/응답 모델"""
    nickname: Optional[str] = Field("익명", example="플레이어", description="플레이어 닉네임")
    puzzle_number: int = Field(..., example=260724, description="퍼즐 일자 번호")
    guess_count: int = Field(..., example=5, description="총 시도 횟수")
    best_rank: int = Field(..., example=1, description="최고 유사 순위")
    worst_rank: int = Field(..., example=140, description="최저 유사 순위")
    created_at: Optional[str] = Field(None, description="기록 생성 일시")
