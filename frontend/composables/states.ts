/**
 * @file states.ts
 * @description Pinia 기반 전역 상태 관리 및 localStorage 영속화 모듈
 */

import { defineStore } from "pinia"
import type { ApiData, GuessData, GuessResult, State, Statistics } from "./models"

/** API 서버 내부 통신 전역 릴레이션 참조 */
export const api_server_base = ref<string>("")
/** API 클라이언트 전역 엔드포인트 참조 */
export const api_client_base = ref<string>("")
/** 스프라이트 이미지 서버 엔드포인트 참조 */
export const sprite_base = ref<string>("")

/**
 * Champdle 앱 전역 상태 스토어 (Pinia)
 */
export const useStore = defineStore("state", {
  state: (): State => {
    return {
      puzzle_number: 0,
      guess_data_list: [],
      last_guess_data: undefined,
      locale: undefined,
      api_data: {
        champions: [],
        champion_local_name_map: {},
        champion_english_name_map: {},
      },
      statistics: {
        last_puzzle_number: NaN,
        clear_count: 0,
        last_guess_count: 0,
        total_guess_count: 0,
        streak: 0,
        best_streak: 0,
        last_correct_guess: undefined,
        last_best_guess: undefined,
      },
    }
  },
  actions: {
    /**
     * 새로운 챔피언 추측 결과를 스토어에 추가 및 저장
     * @param {GuessResult} guess_result - 추측 결과 데이터
     * @returns {GuessData} 인덱스가 부여된 추측 데이터 객체
     */
    addGuessResult(guess_result: GuessResult): GuessData {
      const old_guess_data: GuessData | undefined = this.guess_data_list.find(
        (x: GuessData) => x.name === guess_result.name
      )
      if (old_guess_data !== undefined) {
        return old_guess_data
      }
      const guess_data: GuessData = Object.assign(
        { index: this.guess_data_list.length },
        guess_result
      )
      this.guess_data_list.push(guess_data)
      savePuzzleNumber(this.puzzle_number)
      saveGuessDataList(this.guess_data_list)
      return guess_data
    },

    /**
     * 앱 언어 변경 및 챔피언 명칭 맵 동기화
     * @param {string} locale - 언어 코드 (예: 'ko', 'en')
     */
    changeLocale(locale: string): void {
      if (isValidFluentLocale(locale)) {
        if (process.client) {
          localStorage.setItem("champdle_locale", locale)
        }
        changeFluentLocale(locale)
        apiChampionNameMap(locale).then((data) => {
          this.api_data.champion_local_name_map = {}
          this.api_data.champion_english_name_map = {}
          for (const item of data) {
            this.api_data.champion_local_name_map[
              item.local_name.toLowerCase()
            ] = item.english_name
            this.api_data.champion_english_name_map[
              item.english_name.toLowerCase()
            ] = item.local_name
          }
          saveApiData(this.api_data)
        })
      }
    },

    /**
     * 챔피언 이름을 한국어<->영어 수직 변환
     * @param {string} [name] - 변환 대상 이름
     * @param {boolean} to_eng - true일 경우 영어로, false일 경우 현지어로 변환
     * @returns {string | undefined} 변환된 이름
     */
    translateChampionName(name: string | undefined, to_eng: boolean): string | undefined {
      if (!name) return name
      const key = name.toLowerCase()
      if (to_eng) {
        return this.api_data.champion_local_name_map?.[key] || name
      } else {
        return this.api_data.champion_english_name_map?.[key] || name
      }
    },
  },
})

/**
 * 데이터를 브라우저 localStorage에 JSON 문자열로 저장
 * @param {string} key - 스토리지 키
 * @param {any} data - 저장할 데이터
 */
export const saveToLocalStorage = (key: string, data: any): void => {
  if (process.client) {
    localStorage.setItem(key, JSON.stringify(data))
  }
}

/**
 * 브라우저 localStorage에서 JSON 객체를 불러옴
 * @param {string} key - 스토리지 키
 * @returns {any | null} 역직렬화된 객체 또는 null
 */
export const loadFromLocalStorage = (key: string): any | null => {
  if (process.client) {
    const localdata = localStorage.getItem(key)
    if (typeof localdata === "string") {
      return JSON.parse(localdata)
    }
  }
  return null
}

/** 추측 리스트 헬퍼 함수들 */
export const saveGuessDataList = (guess_data_list: GuessData[]): void =>
  saveToLocalStorage("guess_data_list", guess_data_list)
export const savePuzzleNumber = (puzzle_number: number): void =>
  saveToLocalStorage("puzzle_number", puzzle_number)
export const saveStatistics = (statistics: Statistics): void =>
  saveToLocalStorage("statistics", statistics)
export const saveApiData = (api_data: ApiData): void =>
  saveToLocalStorage("api_data", api_data)

export const loadGuessDataList = (): GuessData[] | null =>
  loadFromLocalStorage("guess_data_list")
export const loadPuzzleNumber = (): number | null =>
  loadFromLocalStorage("puzzle_number")
export const loadStatistics = (): Statistics | null =>
  loadFromLocalStorage("statistics")
export const loadApiData = (): ApiData | null =>
  loadFromLocalStorage("api_data")
