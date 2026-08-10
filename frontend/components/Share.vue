<template>
  <div
    class="mb-4 px-4 pt-4 pb-6 bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 dark:text-slate-300 rounded shadow-sm"
  >
    <p class="text-xl font-bold">
      {{ $t("share-title", { puzzle_number: String(state.puzzle_number) }) }}
    </p>
    <p v-if="!is_hide_answer" class="text-md font-bold mt-2">
      {{
        $t("share-champion-name", {
          name: state.translateChampionName(
            state.statistics?.last_correct_guess?.name,
            false
          ),
        })
      }}
    </p>

    <!-- Stats 3-Grid (Guess Count, Best Rank, Worst Rank) -->
    <div class="grid grid-cols-1 zs:grid-cols-2 xs:grid-cols-3 gap-2">
      <div>
        <p class="text-sm font-medium text-gray-500 dark:text-slate-400 mt-3">
          {{ $t("share-guess-count-title") }}
        </p>
        <p class="mt-1">
          <span class="inline-block text-2xl font-medium leading-none">
            {{ $t("share-guess-count-value", { value: String(guessCount) }) }}
          </span>
        </p>
      </div>
      <div>
        <p class="text-sm font-medium text-gray-500 dark:text-slate-400 mt-3">
          {{ $t("share-best-rank-title") }}
        </p>
        <p class="mt-1">
          <span class="inline-block text-2xl font-medium leading-none">
            {{ $t("share-best-rank-value", { value: String(bestRank) }) }}
          </span>
        </p>
      </div>

      <div>
        <p class="text-sm font-medium text-gray-500 dark:text-slate-400 mt-3">
          {{ $t("share-worst-rank-title") }}
        </p>
        <p class="mt-1">
          <span class="inline-block text-2xl font-medium leading-none text-rose-500 dark:text-rose-400">
            {{ $t("share-worst-rank-value", { value: String(worstRank) }) }}
          </span>
        </p>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="flex flex-wrap items-center justify-end gap-2 mt-4">
      <button
        class="py-2 px-3 text-sm font-medium text-indigo-600 dark:text-indigo-200 border border-indigo-600 dark:border-indigo-200 rounded shadow-sm hover:bg-indigo-600 dark:hover:bg-indigo-800 hover:text-white active:bg-indigo-500 focus:outline-none"
        @click="copyToClipboard"
      >
        {{ $t("share-button") }}
      </button>

      <button
        class="py-2 px-3 text-sm font-medium text-indigo-600 dark:text-indigo-200 border border-indigo-600 dark:border-indigo-200 rounded shadow-sm hover:bg-indigo-600 dark:hover:bg-indigo-800 hover:text-white active:bg-indigo-500 focus:outline-none"
        @click="showRankList"
      >
        {{ $t("show-rank-list-button") }}
      </button>

      <!-- 기록하기 버튼 ('오늘'의 퍼즐일 때만 표시) -->
      <button
        v-if="isTodayPuzzle"
        class="py-2 px-3 text-sm font-medium text-white bg-indigo-600 dark:bg-indigo-500 rounded shadow-sm hover:bg-indigo-700 dark:hover:bg-indigo-400 active:bg-indigo-800 focus:outline-none transition-colors"
        @click="toggleRecordForm"
      >
        {{ isRecorded ? $t('share-recorded-button') : $t('share-record-button') }}
      </button>
    </div>

    <div class="inline-flex items-center w-full justify-end mt-3">
      <input
        v-model="is_hide_answer"
        class="appearance-none h-4 w-4 mr-2 rounded-sm bg-white checked:bg-indigo-600 cursor-pointer"
        type="checkbox"
        id="shareHideAnswer"
      />
      <label
        class="inline-block text-xs text-gray-500 dark:text-slate-400"
        for="shareHideAnswer"
      >
        {{ $t("share-hide-answer-checkbox-label") }}
      </label>
    </div>

    <!-- 기록하기 입력 폼 영역 -->
    <div v-if="showForm && isTodayPuzzle" class="mt-4 p-4 bg-slate-50 dark:bg-slate-900 border border-indigo-300 dark:border-indigo-700 rounded-lg">
      <h4 class="font-bold text-sm text-indigo-800 dark:text-indigo-300 flex items-center gap-1.5 mb-2">
        <span>{{ $t('share-record-form-title') }}</span>
      </h4>
      <p class="text-xs text-gray-600 dark:text-slate-400 mb-3">
        {{ $t('share-record-summary', { guessCount: String(guessCount), bestRank: String(bestRank), worstRank: String(worstRank) }) }}
      </p>

      <div class="flex items-center gap-2">
        <input
          v-model="nicknameInput"
          type="text"
          :placeholder="$t('share-nickname-placeholder')"
          class="flex-1 px-3 py-1.5 text-sm bg-white dark:bg-slate-800 border border-gray-300 dark:border-slate-600 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
          :disabled="isSubmitting || isRecorded"
        />
        <button
          @click="submitRecord"
          class="px-4 py-1.5 text-sm font-bold text-white bg-indigo-600 hover:bg-indigo-700 dark:bg-indigo-500 dark:hover:bg-indigo-400 disabled:opacity-50 rounded transition-all"
          :disabled="isSubmitting || isRecorded"
        >
          {{ isSubmitting ? $t('share-saving') : (isRecorded ? $t('share-saved') : $t('share-save-button')) }}
        </button>
      </div>

      <!-- 리더보드 목록 -->
      <div v-if="savedRecords.length > 0" class="mt-4 pt-3 border-t border-gray-200 dark:border-slate-800">
        <p class="text-xs font-bold text-gray-700 dark:text-slate-300 mb-2">
          {{ $t('share-leaderboard-title', { count: String(savedRecords.length) }) }}
        </p>
        <div class="max-h-40 overflow-y-auto divide-y divide-gray-200 dark:divide-slate-800 text-xs">
          <div v-for="(rec, idx) in savedRecords" :key="idx" class="py-1.5 flex justify-between items-center">
            <span class="font-semibold text-indigo-600 dark:text-indigo-400">
              #{{ idx + 1 }} {{ rec.nickname || $t('share-anonymous') }}
            </span>
            <span class="text-gray-500 dark:text-slate-400">
              {{ $t('share-leaderboard-item', { guesses: String(rec.guess_count), best: String(rec.best_rank), worst: String(rec.worst_rank) }) }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const state = useStore()

const is_hide_answer = ref(false)
const showForm = ref(false)
const nicknameInput = ref("")
const isSubmitting = ref(false)
const isRecorded = ref(false)
const savedRecords = ref<any[]>([])

/** 오늘 자 퍼즐 여부 (오늘 일자 퍼즐일 경우에만 리더보드 기록 가능) */
const isTodayPuzzle = computed<boolean>(() => {
  return state.puzzle_number === todayPuzzleNumber()
})

/** 총 시도 횟수 (통계 데이터 기준, 데이터 부재 시 리스트 길이 또는 기본값 1 반환) */
const guessCount = computed<number>(() => {
  return state.statistics?.last_guess_count || state.guess_data_list?.length || 1
})

/**
 * 최고 유사 순위 산출 (정답 1위를 제외한 추측 중 최고 순위, 1회차 정답 시 1위 반환)
 */
const bestRank = computed<number>(() => {
  // 1. 저장된 통계 데이터 내 최고 순위가 존재하는 경우 우선 반환
  if (state.statistics?.last_best_guess?.rank !== undefined) {
    return state.statistics.last_best_guess.rank
  }
  // 2. 정답(rank=1)을 제외한 일반 추측들의 순위 수치 목록 추출
  const nonCorrectRanks = (state.guess_data_list || [])
    .filter((g) => g.rank > 1)
    .map((g) => g.rank)

  // 3. 일반 추측이 있는 경우 최댓값(최고 순위) 산출, 1회차 정답 시 기본값 1 반환
  return nonCorrectRanks.length > 0 ? Math.min(...nonCorrectRanks) : 1
})

/** 최저 유사 순위 산출 (추측 목록 중 가장 낮은 순위 수치) */
const worstRank = computed<number>(() => {
  const ranks = (state.guess_data_list || []).map((g) => g.rank)
  return ranks.length > 0 ? Math.max(...ranks) : 1
})

onMounted(() => {
  if (process.client) {
    nicknameInput.value = localStorage.getItem("champdle_nickname") || "익명"
    const recordedPuzzles = JSON.parse(localStorage.getItem("champdle_recorded_puzzles") || "[]")
    if (recordedPuzzles.includes(state.puzzle_number)) {
      isRecorded.value = true
    }
  }
  loadRecords()
})

async function loadRecords() {
  try {
    const list = await apiGetRecords(state.puzzle_number)
    savedRecords.value = list || []
  } catch (e) {
    console.error("기록 로드 실패", e)
  }
}

function toggleRecordForm() {
  showForm.value = !showForm.value
  if (showForm.value) {
    loadRecords()
  }
}

async function submitRecord() {
  if (isRecorded.value || isSubmitting.value) return

  isSubmitting.value = true
  try {
    const nick = nicknameInput.value.trim() || "익명"
    if (process.client) {
      localStorage.setItem("champdle_nickname", nick)
    }

    await apiSaveRecord({
      nickname: nick,
      puzzle_number: state.puzzle_number,
      guess_count: guessCount.value,
      best_rank: bestRank.value,
      worst_rank: worstRank.value,
    })

    isRecorded.value = true
    if (process.client) {
      const recordedPuzzles = JSON.parse(localStorage.getItem("champdle_recorded_puzzles") || "[]")
      if (!recordedPuzzles.includes(state.puzzle_number)) {
        recordedPuzzles.push(state.puzzle_number)
        localStorage.setItem("champdle_recorded_puzzles", JSON.stringify(recordedPuzzles))
      }
    }

    alert(fluent.format("share-record-success-alert"))
    await loadRecords()
  } catch (err) {
    alert(fluent.format("share-record-error-alert"))
  } finally {
    isSubmitting.value = false
  }
}

function copyToClipboard() {
  const url = process.client
    ? window.location.href
    : useRuntimeConfig().public.frontendBase + useRoute().fullPath

  let textToCopy = ""
  try {
    textToCopy =
      fluent.format("share-clipboard-text", {
        puzzle_number: String(state.puzzle_number),
        guess_count: guessCount.value,
        best_rank: bestRank.value,
        best_similarity: (
          (state.statistics?.last_best_guess?.similarity || 1.0) * 100
        ).toFixed(2),
      }) +
      "\n" +
      url
  } catch (e) {
    textToCopy = `Champdle #${state.puzzle_number} 성공!\n${url}`
  }

  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard
      .writeText(textToCopy)
      .then(() => {
        alert(fluent.format("share-clipboard-text-alert"))
      })
      .catch(() => {
        fallbackCopyTextToClipboard(textToCopy)
      })
  } else {
    fallbackCopyTextToClipboard(textToCopy)
  }
}

function fallbackCopyTextToClipboard(text: string) {
  const textArea = document.createElement("textarea")
  textArea.value = text
  textArea.style.top = "0"
  textArea.style.left = "0"
  textArea.style.position = "fixed"
  textArea.style.opacity = "0"
  document.body.appendChild(textArea)
  textArea.focus()
  textArea.select()
  try {
    const successful = document.execCommand("copy")
    if (successful) {
      alert(fluent.format("share-clipboard-text-alert"))
    } else {
      prompt("결과를 복사해 공유해보세요:", text)
    }
  } catch (err) {
    prompt("결과를 복사해 공유해보세요:", text)
  }
  document.body.removeChild(textArea)
}

function showRankList() {
  const targetName =
    state.statistics?.last_correct_guess?.name ||
    state.statistics?.last_best_guess?.name ||
    ""
  if (targetName) {
    useRouter().push(
      `/rank/${state.puzzle_number}/${utf8ToB64(targetName)}`
    )
  } else {
    useRouter().push(`/rank/${state.puzzle_number}`)
  }
}
</script>
