"""
Champdle 유사도 알고리즘 모듈 (카테고리 80점 + 스탯 20점 만점 하이브리드 알고리즘)
"""

from typing import List, Dict, Any
import pandas as pd
import math
from .models import GuessResult

# 18개 스탯 항목별 DiffMax 정규화 임계값 사전 정의
STAT_DIFF_MAX: Dict[str, float] = {
    'hp_base': 286.0,
    'hp_max': 1069.0,
    'mp_base': 530.0,
    'mp_max': 1879.0,
    'movespeed': 40.0,
    'armor_base': 25.0,
    'armor_max': 93.65,
    'spellblock_base': 15.0,
    'spellblock_max': 31.65,
    'attackrange': 525.0,
    'hpregen_base': 10.0,
    'hpregen_max': 27.0,
    'mpregen_base': 50.0,
    'mpregen_max': 50.0,
    'attackdamage_base': 25.0,
    'attackdamage_max': 25.0,
    'attackspeed_base': 0.375,
    'attackspeed_max': 0.6375,
}


def calculate_similarity_detail(champ1: Any, champ2: Any) -> Dict[str, Any]:
    """
    두 챔피언 간의 하이브리드 가중치 기반 유사도 상세 계산
    
    [점수 산출 기준]
    - 카테고리 요소 (총 80점 만점):
        1. 소속 지역 (Region): 28점
        2. 역할군 (Role 1 & 2): 15점 (완전일치 15점, 주역할 12점, 교차 10.5점, 부역할 7.5점)
        3. 종족 (Species): 14점 (완전일치 14점, 교차/부분일치 7점)
        4. 자원 유형 (Resource Partype): 11점
        5. 공격 방식 (Attack Type): 4점 (근거리/원거리)
        6. 성별 (Gender): 4점
        7. 출시 순서 (Release Order): 4점 (비율 감쇄)
    - 스탯 요소 (총 20점 만점):
        - 이동 속도 (4.0점), 사거리 (4.0점) 버프 가중치 적용
        - 나머지 16개 스탯: 각 0.75점 (총 12.0점)
    
    :param champ1: 비교 대상 1 챔피언 Series/Dict
    :param champ2: 비교 대상 2 챔피언 Series/Dict
    :return: 유사도 비율, 카테고리 점수, 스탯 점수 및 상세 텍스트 포함 딕셔너리
    """
    category_score = 0.0

    # 1. Region (소속 지역 - 28점)
    if champ1.get('region') and champ2.get('region') and champ1['region'] == champ2['region']:
        category_score += 28.0

    # 2. Species (종족 - 14점)
    sp1_raw = champ1.get('species') if pd.notna(champ1.get('species')) else None
    sp2_raw = champ2.get('species') if pd.notna(champ2.get('species')) else None

    if sp1_raw and sp2_raw:
        if sp1_raw == sp2_raw:
            category_score += 14.0
        else:
            set1 = {s.strip().lower() for s in str(sp1_raw).split('/') if s.strip()}
            set2 = {s.strip().lower() for s in str(sp2_raw).split('/') if s.strip()}
            if set1.intersection(set2):
                category_score += 7.0

    # 3. Role / Tags (주/부 역할군 고려 - 15점)
    t1_1 = champ1.get('tag_1') if pd.notna(champ1.get('tag_1')) else None
    t1_2 = champ1.get('tag_2') if pd.notna(champ1.get('tag_2')) else None
    t2_1 = champ2.get('tag_1') if pd.notna(champ2.get('tag_1')) else None
    t2_2 = champ2.get('tag_2') if pd.notna(champ2.get('tag_2')) else None

    if t1_1 and t2_1:
        if t1_1 == t2_1 and t1_2 == t2_2:
            category_score += 15.0 * 1.0  # 15점
        elif t1_1 == t2_1:
            category_score += 15.0 * 0.8  # 12점
        elif t1_1 == t2_2 and t1_2 == t2_1:
            category_score += 15.0 * 0.7  # 10.5점
        elif (t1_1 == t2_2 or t1_2 == t2_1 or (t1_2 and t2_2 and t1_2 == t2_2)):
            category_score += 15.0 * 0.5  # 7.5점

    # 4. Resource Type (partype: 자원 유형 - 11점)
    if champ1.get('partype') and champ2.get('partype') and champ1['partype'] == champ2['partype']:
        category_score += 11.0

    # 5. Attack Type (근/원거리 - 4점)
    if champ1.get('attack_type') and champ2.get('attack_type') and champ1['attack_type'] == champ2['attack_type']:
        category_score += 4.0

    # 6. Gender (성별 - 4점)
    if champ1.get('gender') and champ2.get('gender') and champ1['gender'] == champ2['gender']:
        category_score += 4.0

    # 7. Release Order (출시 순서 차이 비율 감쇄 - 4점)
    try:
        id1 = float(champ1.get('champion_id', 0))
        id2 = float(champ2.get('champion_id', 0))
        if id1 > 0 and id2 > 0:
            diff = abs(id1 - id2)
            max_id_diff = 172.0
            ratio = max(0.0, 1.0 - (diff / max_id_diff))
            category_score += 4.0 * ratio
    except (ValueError, TypeError):
        pass

    # Stat Score (총 20점 만점 Min-Max 정규화)
    STAT_WEIGHTS = {
        'movespeed': 4.0,       # 이동 속도 4.0점
        'attackrange': 4.0,     # 사거리 4.0점
        'hp_base': 0.75,
        'hp_max': 0.75,
        'mp_base': 0.75,
        'mp_max': 0.75,
        'armor_base': 0.75,
        'armor_max': 0.75,
        'spellblock_base': 0.75,
        'spellblock_max': 0.75,
        'hpregen_base': 0.75,
        'hpregen_max': 0.75,
        'mpregen_base': 0.75,
        'mpregen_max': 0.75,
        'attackdamage_base': 0.75,
        'attackdamage_max': 0.75,
        'attackspeed_base': 0.75,
        'attackspeed_max': 0.75,
    }

    stat_score = 0.0
    for stat_col, diff_max in STAT_DIFF_MAX.items():
        try:
            val1 = float(champ1[stat_col])
            val2 = float(champ2[stat_col])
            diff = abs(val1 - val2)
            ratio = max(0.0, 1.0 - (diff / diff_max)) if diff_max > 0 else 1.0
            weight = STAT_WEIGHTS.get(stat_col, 0.75)
            stat_score += weight * ratio
        except (ValueError, TypeError, KeyError):
            continue

    total_score = (category_score + stat_score) / 100.0
    sim = round(min(1.0, max(0.0, total_score)), 6)
    cat_round = round(category_score, 1)
    stat_round = round(stat_score, 1)

    return {
        'similarity': sim,
        'category_score': cat_round,
        'stat_score': stat_round,
        'formula_detail': f"카테고리 {cat_round}점 + 스탯 {stat_round}점"
    }


def calculate_similarity(champ1: Any, champ2: Any) -> float:
    """단순 유사도 비율(0.0 ~ 1.0) 반환 헬퍼 함수"""
    return calculate_similarity_detail(champ1, champ2)['similarity']


def calculate_ranks(champion_index: int, champions: pd.DataFrame) -> List[GuessResult]:
    """
    지정 정답 챔피언에 대해 전체 173개 챔피언과의 유사도 내림차순 정렬 순위 리스트 산출
    :param champion_index: 정답 챔피언 인덱스
    :param champions: 챔피언 데이터프레임
    :return: GuessResult Pydantic 객체 배열 (1위부터 173위)
    """
    target_champ = champions.loc[champion_index]
    ranks = []

    for i in champions.index:
        champ = champions.loc[i]
        detail = calculate_similarity_detail(target_champ, champ)
        sim = detail['similarity']
        if i == champion_index:
            sim = 1.0
            detail['category_score'] = 80.0
            detail['stat_score'] = 20.0
            detail['formula_detail'] = "카테고리 80.0점 + 스탯 20.0점"

        champ_name = champ.get('name_en') if 'name_en' in champ and pd.notna(champ['name_en']) else champ.get('name', champ.get('alias'))
        ranks.append({
            'name': champ_name,
            'similarity': sim,
            'category_score': detail['category_score'],
            'stat_score': detail['stat_score'],
            'formula_detail': detail['formula_detail'],
            'index': i
        })

    ranks.sort(key=lambda x: x['similarity'], reverse=True)

    results = []
    for rank_idx, item in enumerate(ranks, start=1):
        results.append(GuessResult(
            rank=rank_idx,
            name=str(item['name']),
            similarity=float(item['similarity']),
            category_score=float(item['category_score']),
            stat_score=float(item['stat_score']),
            formula_detail=str(item['formula_detail'])
        ))
    return results
