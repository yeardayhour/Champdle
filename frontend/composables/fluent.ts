/**
 * @file fluent.ts
 * @description Mozilla Fluent i18n 번들 초기화 및 언어 스위칭 모듈
 */

import { FluentBundle, FluentResource } from "@fluent/bundle"
import { createFluentVue } from "fluent-vue"

// @ts-ignore
import enMessages from "~/i18n/en.ftl?raw"
// @ts-ignore
import koMessages from "~/i18n/ko.ftl?raw"

/** 영어 (en) Fluent 번들 객체 생성 및 리소스 로드 */
const enBundle = new FluentBundle("en")
enBundle.addResource(new FluentResource(enMessages))

/** 한국어 (ko) Fluent 번들 객체 생성 및 리소스 로드 */
const koBundle = new FluentBundle("ko")
koBundle.addResource(new FluentResource(koMessages))

/** 지원 언어별 FluentBundle 맵 객체 */
export const fluentBundles: Record<string, FluentBundle> = {
  en: enBundle,
  ko: koBundle,
}

/** Vue i18n 플러그인 인스턴스 */
export const fluent = createFluentVue({
  bundles: [enBundle],
})

/**
 * 주어진 언어 식별자가 유효한 Fluent 번들 목록에 포함되는지 검증
 * @param {string} locale - 검증할 언어 코드
 * @returns {boolean} 유효 여부
 */
export const isValidFluentLocale = (locale: string): boolean => locale in fluentBundles

/**
 * 런타임 다국어 번들 1순위 우대 언어 교체 (Fallback: 영어 번들)
 * @param {string} locale - 적용할 언어 코드
 */
export const changeFluentLocale = (locale: string): void => {
  if (isValidFluentLocale(locale)) {
    fluent.bundles = [fluentBundles[locale], enBundle]
  } else {
    fluent.bundles = [enBundle]
  }
}
