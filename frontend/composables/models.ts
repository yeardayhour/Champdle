/**
 * @file models.ts
 * @description 애플리케이션 핵심 도메인 인터페이스 및 타입 정의
 */

/** 챔피언 메타데이터 인터페이스 */
export interface Champion {
  /** 챔피언 고유 ID (출시 순서) */
  champion_id: number
  /** 라이엇 내부 ID */
  riot_id: number
  /** 챔피언 식별 별칭 */
  alias: string
  /** 영어 이름 */
  name_en: string
  /** 한국어 이름 */
  name_ko: string
  /** 영어 칭호 */
  title_en: string
  /** 한국어 칭호 */
  title_ko: string
  /** 성별 (Male, Female, Other) */
  gender: string
  /** 종족 (Human, Vastaya 등) */
  species: string
  /** 소속 지역 (Demacia, Noxus 등) */
  region: string
  /** 공격 타입 (Melee, Ranged) */
  attack_type: string
  /** 주 역할군 (Fighter, Tank, Mage 등) */
  tag_1: string
  /** 부 역할군 (선택적) */
  tag_2?: string
  /** 자원 유형 (Mana, Energy, None 등) */
  partype: string
  /** 기본 체력 */
  hp_base: number
  /** 만렙 체력 */
  hp_max: number
  /** 기본 마나/자원 */
  mp_base: number
  /** 만렙 마나/자원 */
  mp_max: number
  /** 이동 속도 */
  movespeed: number
  /** 기본 방어력 */
  armor_base: number
  /** 만렙 방어력 */
  armor_max: number
  /** 기본 마법 저항력 */
  spellblock_base: number
  /** 만렙 마법 저항력 */
  spellblock_max: number
  /** 공격 사거리 */
  attackrange: number
  /** 기본 체력 재생 */
  hpregen_base: number
  /** 만렙 체력 재생 */
  hpregen_max: number
  /** 기본 마나/자원 재생 */
  mpregen_base: number
  /** 만렙 마나/자원 재생 */
  mpregen_max: number
  /** 기본 치명타 확률 */
  crit_base: number
  /** 만렙 치명타 확률 */
  crit_max: number
  /** 기본 공격력 */
  attackdamage_base: number
  /** 만렙 공격력 */
  attackdamage_max: number
  /** 기본 공격 속도 */
  attackspeed_base: number
  /** 만렙 공격 속도 */
  attackspeed_max: number
  /** 초상화 이미지 파일 경로 */
  image_path?: string
}

/** 언어별 챔피언 명칭 매핑 객체 */
export interface LocalName {
  english_name: string
  local_name: string
}

/** 백엔드 추측 응답 데이터 */
export interface GuessResult {
  name: string
  rank: number
  similarity: number
  category_score?: number
  stat_score?: number
  formula_detail?: string
}

/** 클라이언트 추측 기록 데이터 (인덱스 포함) */
export interface GuessData {
  index: number
  name: string
  rank: number
  similarity: number
  category_score?: number
  stat_score?: number
  formula_detail?: string
}

/** Pinia 전역 상태 인터페이스 */
export interface State {
  puzzle_number: number
  guess_data_list: GuessData[]
  last_guess_data: GuessData | undefined
  locale: string | undefined
  api_data: ApiData
  statistics: Statistics
}

/** 캐싱된 API 메타데이터 */
export interface ApiData {
  champions: Champion[]
  champion_local_name_map: Record<string, string>
  champion_english_name_map: Record<string, string>
}

/** 플레이 통계 정보 데이터 */
export interface Statistics {
  last_puzzle_number: number
  clear_count: number
  last_guess_count: number
  total_guess_count: number
  streak: number
  best_streak: number
  last_correct_guess: undefined | GuessData
  last_best_guess: undefined | GuessData
}
