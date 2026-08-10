/**
 * @file utils.ts
 * @description 날짜 계산, 문자열 인코딩, 포맷 변환 및 기본 유틸리티 함수 모듈
 */

// @ts-ignore
import parser from "accept-language-parser"
import { Buffer } from "buffer"

/** 서비스 퍼즐 기준 기점 날짜 (2026-08-11) */
export const puzzleOriginDate = new Date("2026-08-11T00:00:00")

/**
 * YYYY-MM-DD 날짜 문자열을 퍼즐 번호(YYMMDD 포맷 정수)로 변환
 * @param {string} dateStr - 변환할 날짜 문자열
 * @returns {number} YYMMDD 정수 퍼즐 번호
 */
export const dateToPuzzleNumber = (dateStr: string): number => {
  const target = new Date(dateStr)
  if (isNaN(target.getTime())) return todayPuzzleNumber()
  const yy = String(target.getFullYear()).slice(-2)
  const mm = String(target.getMonth() + 1).padStart(2, "0")
  const dd = String(target.getDate()).padStart(2, "0")
  return parseInt(`${yy}${mm}${dd}`)
}

/**
 * 퍼즐 번호(YYMMDD 정수 또는 일수)를 YYYY-MM-DD 날짜 문자열로 변환
 * @param {number} puzzleNum - 퍼즐 번호
 * @returns {string} YYYY-MM-DD 날짜 문자열
 */
export const puzzleNumberToDateString = (puzzleNum: number): string => {
  const str = String(puzzleNum)
  if (str.length <= 4) {
    const date = new Date(puzzleOriginDate.getTime() + puzzleNum * 86400000)
    return date.toISOString().split("T")[0]
  }
  const yy = str.slice(0, 2)
  const mm = str.slice(2, 4)
  const dd = str.slice(4, 6)
  return `20${yy}-${mm}-${dd}`
}

/**
 * 지정된 퍼즐 번호의 전날(어제) 퍼즐 번호 산출
 * @param {number} puzzleNum - 기준 퍼즐 번호
 * @returns {number} 어제 날짜 퍼즐 번호
 */
export const getYesterdayPuzzleNumber = (puzzleNum: number): number => {
  const dateStr = puzzleNumberToDateString(puzzleNum)
  const date = new Date(dateStr)
  date.setDate(date.getDate() - 1)
  const yy = String(date.getFullYear()).slice(-2)
  const mm = String(date.getMonth() + 1).padStart(2, "0")
  const dd = String(date.getDate()).padStart(2, "0")
  return parseInt(`${yy}${mm}${dd}`)
}

/**
 * 오늘 일자의 퍼즐 번호 산출 (URL 쿼리스트링 파라미터 감지 지원)
 * @returns {number} 오늘 날짜 퍼즐 번호
 */
export const todayPuzzleNumber = (): number => {
  if (process.client) {
    const urlParams = new URLSearchParams(window.location.search)
    const puzzleParam = urlParams.get("puzzle")
    if (puzzleParam && !isNaN(parseInt(puzzleParam))) {
      return parseInt(puzzleParam)
    }
    const dateParam = urlParams.get("date")
    if (dateParam) {
      return dateToPuzzleNumber(dateParam)
    }
  }
  const today = new Date()
  const yy = String(today.getFullYear()).slice(-2)
  const mm = String(today.getMonth() + 1).padStart(2, "0")
  const dd = String(today.getDate()).padStart(2, "0")
  return parseInt(`${yy}${mm}${dd}`)
}

/**
 * 사용자 설정 및 브라우저/헤더 기반 자동 언어 감지 반환
 * @returns {string} 언어 코드 ('ko', 'en')
 */
export const getLocale = (): string => {
  if (process.client) {
    const saved = localStorage.getItem("champdle_locale")
    if (saved && isValidFluentLocale(saved)) {
      return saved
    }
  }

  let lang: string = "en"
  if (process.client) {
    if (window.navigator.languages && window.navigator.languages.length) {
      lang = window.navigator.languages[0].split("-")[0]
    } else {
      lang = (
        (window.navigator as any).userLanguage ||
        window.navigator.language ||
        (window.navigator as any).browserLanguage ||
        "en"
      ).split("-")[0]
    }
  } else {
    const accept_language: string | undefined = useRequestHeaders([
      "accept-language",
    ])["accept-language"]
    if (accept_language !== undefined) {
      lang =
        parser.pick(Object.keys(fluentBundles), accept_language, {
          loose: true,
        }) || "en"
    } else {
      lang = "en"
    }
  }

  const cleanLang = lang.split("-")[0]
  return isValidFluentLocale(cleanLang) ? cleanLang : "en"
}

/**
 * UTF-8 문자열을 Base64 엔코딩 문자열로 변환
 * @param {string} str - 원본 문자열
 * @returns {string} Base64 문자열
 */
export const utf8ToB64 = (str: string): string => {
  return Buffer.from(str, "utf8").toString("base64")
}

/**
 * Base64 디코딩하여 원본 UTF-8 문자열 반환
 * @param {string} str - Base64 인코딩 문자열
 * @returns {string} 원본 디코딩 문자열
 */
export const b64ToUtf8 = (str: string): string => {
  return Buffer.from(str, "base64").toString("utf8")
}

/**
 * SSR / CSR 환경에 따른 API 기본 URL 베이스 반환
 * @returns {string} API 베이스 URL
 */
export const apiBase = (): string => {
  return process.client ? api_client_base.value : api_server_base.value
}

/**
 * 이미지를 찾지 못했을 때 사용할 대체 SVG Data URL 생성
 * @returns {string} 대체 SVG Data URL
 */
export const missingChampionImageUrl = (): string => {
  return "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='120' height='120' viewBox='0 0 120 120'><rect width='100%' height='100%' fill='%23334155'/><text x='50%' y='50%' dominant-baseline='middle' text-anchor='middle' font-size='40' fill='%2394a3b8'>?</text></svg>"
}

/**
 * 이미지 로드 에러 발생 시 Fallback 대체 이미지 반환
 * @param {string} [imagePath] - 이미지 경로
 * @returns {string} 대체 이미지 URL
 */
export const fallbackChampionImageUrl = (imagePath?: string): string => {
  return missingChampionImageUrl()
}

export const missingPokemonImageUrl = missingChampionImageUrl
export const fallbackPokemonImageUrl = fallbackChampionImageUrl
