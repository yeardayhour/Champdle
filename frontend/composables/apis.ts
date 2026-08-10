/**
 * @file apis.ts
 * @description 백엔드 REST API 호스팅 엔드포인트 통신 모듈
 */

import type { Champion, GuessResult, LocalName } from "./models"

/**
 * 지원하는 언어 목록 조회 API
 * @returns {Promise<Array<string>>} 지원 언어 식별자 배열
 */
export const apiLanguages = (): Promise<Array<string>> =>
  $fetch<Array<string>>(`${apiBase()}/languages`)

/**
 * 전체 챔피언 메타데이터 목록 조회 API
 * @returns {Promise<Array<Champion>>} 챔피언 객체 배열
 */
export const apiChampions = (): Promise<Array<Champion>> =>
  $fetch<Array<Champion>>(`${apiBase()}/champions`)

/**
 * 특정 언어 기준 챔피언 이름 맵 매핑 데이터 조회 API
 * @param {string} language - 언어 코드 (예: 'ko', 'en')
 * @returns {Promise<Array<LocalName>>} 챔피언 언어별 명칭 객체 배열
 */
export const apiChampionNameMap = (language: string): Promise<Array<LocalName>> =>
  $fetch<Array<LocalName>>(`${apiBase()}/champion_name_map/${language}`)

/**
 * 지정된 퍼즐 번호의 전체 챔피언 순위 리스트 조회 API
 * @param {number} puzzle_number - 퍼즐 일자 번호 (YYMMDD 또는 0~9999 일수)
 * @returns {Promise<Array<GuessResult>>} 전체 순위 결과 배열
 */
export const apiRank = (puzzle_number: number): Promise<Array<GuessResult>> =>
  $fetch<Array<GuessResult>>(`${apiBase()}/rank/${puzzle_number}`)

/**
 * 챔피언 추측 실행 및 유사도 계산 결과 요청 API
 * @param {number} puzzle_number - 퍼즐 일자 번호
 * @param {string} name - 입력한 챔피언 이름 (한국어/영어/별칭)
 * @returns {Promise<GuessResult>} 유사도 및 순위 결과 객체
 */
export const apiGuess = (puzzle_number: number, name: string): Promise<GuessResult> =>
  $fetch<GuessResult>(`${apiBase()}/guess/${puzzle_number}?name=${encodeURIComponent(name)}`)

/**
 * 플레이어 퍼즐 클리어 기록 저장 API
 * @param {Object} payload - 플레이 기록 정보
 * @param {string} [payload.nickname] - 플레이어 닉네임 (기본: 익명)
 * @param {number} payload.puzzle_number - 퍼즐 번호
 * @param {number} payload.guess_count - 시도 횟수
 * @param {number} payload.best_rank - 최고 유사 순위
 * @param {number} payload.worst_rank - 최저 유사 순위
 * @returns {Promise<{ status: string; message: string; record: any }>} 저장 응답 객체
 */
export const apiSaveRecord = (payload: {
  nickname?: string
  puzzle_number: number
  guess_count: number
  best_rank: number
  worst_rank: number
}): Promise<{ status: string; message: string; record: any }> =>
  $fetch<{ status: string; message: string; record: any }>(`${apiBase()}/record`, {
    method: "POST",
    body: payload,
  })

/**
 * 특정 퍼즐 일자의 리더보드 플레이 기록 목록 조회 API
 * @param {number} puzzle_number - 퍼즐 일자 번호
 * @returns {Promise<Array<any>>} 등록된 플레이 기록 리스트
 */
export const apiGetRecords = (puzzle_number: number): Promise<Array<any>> =>
  $fetch<Array<any>>(`${apiBase()}/records/${puzzle_number}`)
