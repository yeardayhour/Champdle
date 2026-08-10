<template>
  <nav class="flex flex-wrap items-center justify-between py-4 mx-auto gap-2">
    <div class="flex items-center space-x-2">
      <NuxtLink to="/" class="font-bold text-xl dark:text-slate-200">{{
        title
      }}</NuxtLink>
      <span
        v-if="subtitle"
        class="font-bold text-md text-gray-700 dark:text-slate-300"
        >{{ subtitle }}</span
      >
    </div>
    <div class="inline-flex items-center space-x-1.5 flex-wrap gap-y-1">
      <!-- Compact Date Picker Input for Custom Champion Date -->
      <div class="flex items-center space-x-1 bg-gray-100 dark:bg-slate-800 p-0.5 px-1 rounded-md border border-gray-200 dark:border-slate-700 text-xs">
        <span class="text-[11px] text-gray-500 dark:text-slate-400 pl-0.5">📅</span>
        <input
          type="date"
          v-model="selectedDate"
          @change="onDateChange"
          :title="$t('menu-date-tooltip')"
          class="rounded py-0.5 px-1 text-[11px] border border-gray-300 dark:border-slate-600 dark:bg-slate-700 dark:text-slate-200 shadow-sm cursor-pointer w-28"
        />
      </div>

      <!-- Champion List Button -->
      <button
        @click="showChampionList = true"
        class="flex items-center space-x-1 py-1 px-2 text-xs font-semibold text-indigo-700 dark:text-indigo-300 bg-indigo-50 dark:bg-indigo-950/60 border border-indigo-200 dark:border-indigo-800 rounded-md hover:bg-indigo-100 dark:hover:bg-indigo-900 transition-colors shadow-sm cursor-pointer"
        :title="$t('menu-champion-list-tooltip')"
      >
        <span>{{ $t('menu-champion-list-button') }}</span>
      </button>

      <button
        v-if="$colorMode.value === 'dark'"
        class="p-1.5"
        @click="$colorMode.preference = 'light'"
        title="Light Mode"
      >
        <SunIcon></SunIcon>
      </button>
      <button
        v-if="$colorMode.value === 'light'"
        class="p-1.5"
        @click="$colorMode.preference = 'dark'"
        title="Dark Mode"
      >
        <MoonIcon></MoonIcon>
      </button>
      <select
        v-model="state.locale"
        class="rounded py-0.5 pl-1.5 pr-1 border border-gray-200 dark:border-slate-600 dark:bg-slate-700 dark:text-slate-200 shadow-sm text-xs cursor-pointer"
      >
        <option v-for="(_, locale) in fluentBundles" :value="locale">
          {{ $t("language-locale-" + locale) }}
        </option>
      </select>

      <!-- Champion List Modal -->
      <ChampionListModal :is-open="showChampionList" @close="showChampionList = false" />
    </div>
  </nav>
</template>

<script setup lang="ts">
import { fluentBundles } from "#imports"

const state = useStore()
const selectedDate = ref("")
const showChampionList = ref(false)

onMounted(() => {
  selectedDate.value = puzzleNumberToDateString(state.puzzle_number)
})

watch(() => state.puzzle_number, (newVal) => {
  selectedDate.value = puzzleNumberToDateString(newVal)
})

const onDateChange = () => {
  if (selectedDate.value) {
    const targetPuzzle = dateToPuzzleNumber(selectedDate.value)
    const baseURL = useRuntimeConfig().app.baseURL || "/"
    const separator = baseURL.endsWith("/") ? "" : "/"
    window.location.href = `${baseURL}${separator}?puzzle=${targetPuzzle}`
  }
}

const props = defineProps({
  title: {
    type: String,
    default: fluent.format("champdle"),
  },
  subtitle: {
    type: String,
  },
})
</script>
