<template>
  <Transition name="fade">
    <div
      v-if="isOpen"
      class="fixed inset-0 z-50 flex items-center justify-center p-2 sm:p-6 bg-black/60 backdrop-blur-sm"
      @click.self="closeModal"
    >
      <div
        class="bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 rounded-xl shadow-2xl w-full max-w-5xl max-h-[92vh] flex flex-col overflow-hidden"
      >
        <!-- Modal Header -->
        <div
          class="flex items-center justify-between px-4 py-3 border-b border-gray-200 dark:border-slate-800 bg-gray-50 dark:bg-slate-800/60"
        >
          <div class="flex items-center space-x-2">
            <span class="text-xl">📜</span>
            <h3 class="font-bold text-base text-gray-900 dark:text-slate-100">
              {{ $t('champion-modal-title') }}
            </h3>
            <span
              class="px-2 py-0.5 text-xs font-semibold rounded-full bg-indigo-100 dark:bg-indigo-900/80 text-indigo-800 dark:text-indigo-200"
            >
              {{ $t('champion-modal-count', { filtered: String(filteredChampions.length), total: String(state.api_data.champions.length) }) }}
            </span>
          </div>

          <button
            @click="closeModal"
            class="p-1 rounded-lg text-gray-400 hover:text-gray-600 dark:hover:text-slate-200 hover:bg-gray-200 dark:hover:bg-slate-700 transition-colors"
            :title="$t('none')"
          >
            <svg
              class="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              ></path>
            </svg>
          </button>
        </div>

        <!-- Champion Detail View -->
        <div v-if="selectedChampion" class="flex-1 overflow-y-auto p-4 space-y-4">
          <div class="flex items-center justify-between">
            <button
              @click="selectedChampion = null"
              class="flex items-center space-x-1 px-3 py-1.5 text-xs font-medium text-indigo-600 dark:text-indigo-400 bg-indigo-50 dark:bg-indigo-950/60 border border-indigo-200 dark:border-indigo-800 rounded-md hover:bg-indigo-100 dark:hover:bg-indigo-900 transition-colors"
            >
              <span>{{ $t('champion-modal-back-button') }}</span>
            </button>
            <span class="text-xs text-gray-500 dark:text-slate-400">
              {{ $t('champion-modal-viewing-details') }}
            </span>
          </div>

          <ChampionInfo :champion="selectedChampion" />
        </div>

        <!-- Champion Grid View -->
        <template v-else>
          <!-- Search & Filter Controls -->
          <div class="p-3 border-b border-gray-100 dark:border-slate-800 bg-white dark:bg-slate-900 space-y-2.5">
            <!-- Row 1: Search & Toggle Filter -->
            <div class="flex flex-wrap gap-2 items-center justify-between">
              <!-- Search Input -->
              <div class="relative flex-1 min-w-[200px]">
                <input
                  v-model="searchQuery"
                  type="text"
                  :placeholder="$t('champion-modal-search-placeholder')"
                  class="w-full pl-8 pr-3 py-1.5 text-xs bg-gray-100 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 text-gray-900 dark:text-slate-100"
                />
                <span class="absolute left-2.5 top-2 text-gray-400 text-xs">🔍</span>
              </div>

              <!-- Filter Toggle Button -->
              <button
                @click="showFilters = !showFilters"
                :class="[
                  'px-3 py-1.5 text-xs font-medium rounded-lg border transition-colors flex items-center space-x-1',
                  showFilters || activeFilterCount > 0
                    ? 'bg-indigo-50 dark:bg-indigo-950/80 border-indigo-300 dark:border-indigo-700 text-indigo-600 dark:text-indigo-300'
                    : 'bg-gray-100 dark:bg-slate-800 border-gray-200 dark:border-slate-700 text-gray-700 dark:text-slate-300 hover:bg-gray-200 dark:hover:bg-slate-700'
                ]"
              >
                <span>{{ $t('champion-modal-filter-title') }}</span>
                <span
                  v-if="activeFilterCount > 0"
                  class="ml-1 px-1.5 py-0.2 text-[10px] font-bold bg-indigo-600 text-white rounded-full"
                >
                  {{ activeFilterCount }}
                </span>
              </button>

              <!-- Reset Filters Button -->
              <button
                v-if="activeFilterCount > 0 || searchQuery || isFilterActive"
                @click="resetAllFilters"
                class="px-2.5 py-1.5 text-xs font-medium text-red-600 dark:text-red-400 bg-red-50 dark:bg-red-950/40 border border-red-200 dark:border-red-900/60 rounded-lg hover:bg-red-100 dark:hover:bg-red-900/60 transition-colors"
              >
                {{ $t('champion-modal-filter-reset') }}
              </button>
            </div>

            <!-- Row 2: Category Dropdown Filters (Collapsible) -->
            <Transition name="expand">
              <div
                v-if="showFilters"
                class="grid grid-cols-2 xs:grid-cols-3 sm:grid-cols-6 gap-2 pt-2 border-t border-gray-100 dark:border-slate-800"
              >
                <!-- 1. 소속 (Region) -->
                <div>
                  <label class="block text-[10px] font-semibold text-gray-500 dark:text-slate-400 mb-0.5">{{ $t('champion-modal-filter-region') }}</label>
                  <select
                    v-model="filterRegion"
                    class="w-full text-xs py-1 px-1.5 rounded bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-gray-800 dark:text-slate-200 focus:ring-1 focus:ring-indigo-500"
                  >
                    <option :value="ALL_KEY">{{ $t('champion-modal-filter-all-regions') }}</option>
                    <option v-for="r in availableRegions" :key="r" :value="r">
                      {{ translateRegion(r) }}
                    </option>
                  </select>
                </div>

                <!-- 2. 역할군 (Role) -->
                <div>
                  <label class="block text-[10px] font-semibold text-gray-500 dark:text-slate-400 mb-0.5">{{ $t('champion-modal-filter-role') }}</label>
                  <select
                    v-model="filterRole"
                    class="w-full text-xs py-1 px-1.5 rounded bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-gray-800 dark:text-slate-200 focus:ring-1 focus:ring-indigo-500"
                  >
                    <option :value="ALL_KEY">{{ $t('champion-modal-filter-all-roles') }}</option>
                    <option v-for="role in availableRoles" :key="role" :value="role">
                      {{ translateRole(role) }}
                    </option>
                  </select>
                </div>

                <!-- 3. 공격 방식 (Attack Type) -->
                <div>
                  <label class="block text-[10px] font-semibold text-gray-500 dark:text-slate-400 mb-0.5">{{ $t('champion-modal-filter-attack-type') }}</label>
                  <select
                    v-model="filterAttackType"
                    class="w-full text-xs py-1 px-1.5 rounded bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-gray-800 dark:text-slate-200 focus:ring-1 focus:ring-indigo-500"
                  >
                    <option :value="ALL_KEY">{{ $t('champion-modal-filter-all-attack-types') }}</option>
                    <option value="melee">{{ state.locale === 'ko' ? '근거리 (Melee)' : 'Melee' }}</option>
                    <option value="ranged">{{ state.locale === 'ko' ? '원거리 (Ranged)' : 'Ranged' }}</option>
                  </select>
                </div>

                <!-- 4. 자원 (Resource) -->
                <div>
                  <label class="block text-[10px] font-semibold text-gray-500 dark:text-slate-400 mb-0.5">{{ $t('champion-modal-filter-resource') }}</label>
                  <select
                    v-model="filterResource"
                    class="w-full text-xs py-1 px-1.5 rounded bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-gray-800 dark:text-slate-200 focus:ring-1 focus:ring-indigo-500"
                  >
                    <option :value="ALL_KEY">{{ $t('champion-modal-filter-all-resources') }}</option>
                    <option v-for="res in availableResources" :key="res" :value="res">
                      {{ translateResource(res) }}
                    </option>
                  </select>
                </div>

                <!-- 5. 성별 (Gender) -->
                <div>
                  <label class="block text-[10px] font-semibold text-gray-500 dark:text-slate-400 mb-0.5">{{ $t('champion-modal-filter-gender') }}</label>
                  <select
                    v-model="filterGender"
                    class="w-full text-xs py-1 px-1.5 rounded bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-gray-800 dark:text-slate-200 focus:ring-1 focus:ring-indigo-500"
                  >
                    <option :value="ALL_KEY">{{ $t('champion-modal-filter-all-genders') }}</option>
                    <option value="Male">{{ state.locale === 'ko' ? '남성 (Male)' : 'Male' }}</option>
                    <option value="Female">{{ state.locale === 'ko' ? '여성 (Female)' : 'Female' }}</option>
                    <option value="Other">{{ state.locale === 'ko' ? '기타 (Other)' : 'Other' }}</option>
                  </select>
                </div>

                <!-- 6. 종족 (Species) -->
                <div>
                  <label class="block text-[10px] font-semibold text-gray-500 dark:text-slate-400 mb-0.5">{{ $t('champion-modal-filter-species') }}</label>
                  <select
                    v-model="filterSpecies"
                    class="w-full text-xs py-1 px-1.5 rounded bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-gray-800 dark:text-slate-200 focus:ring-1 focus:ring-indigo-500"
                  >
                    <option :value="ALL_KEY">{{ $t('champion-modal-filter-all-species') }}</option>
                    <option v-for="spec in availableSpecies" :key="spec" :value="spec">
                      {{ translateSpecies(spec) }}
                    </option>
                  </select>
                </div>
              </div>
            </Transition>

            <!-- Row 3: Choseong Quick Filters -->
            <div class="flex flex-wrap gap-1 items-center justify-center pt-1">
              <button
                v-for="ch in choseongFilters"
                :key="ch"
                @click="selectedChoseong = ch"
                :class="[
                  'px-2 py-0.5 text-xs rounded transition-colors font-medium',
                  selectedChoseong === ch
                    ? 'bg-indigo-600 text-white dark:bg-indigo-500'
                    : 'bg-gray-100 dark:bg-slate-800 text-gray-600 dark:text-slate-300 hover:bg-gray-200 dark:hover:bg-slate-700'
                ]"
              >
                {{ ch === '전체' || ch === 'All' ? $t('champion-modal-choseong-all') : ch }}
              </button>
            </div>
          </div>

          <!-- Champion Grid Container -->
          <div class="flex-1 overflow-y-auto p-4">
            <div
              v-if="filteredChampions.length > 0"
              class="grid grid-cols-4 xs:grid-cols-5 sm:grid-cols-6 md:grid-cols-8 lg:grid-cols-10 gap-3"
            >
              <div
                v-for="champ in filteredChampions"
                :key="champ.champion_id"
                @click="selectedChampion = champ"
                class="group flex flex-col items-center cursor-pointer"
              >
                <div
                  class="w-full aspect-square rounded-lg overflow-hidden border border-gray-200 dark:border-slate-700 bg-slate-100 dark:bg-slate-800 group-hover:border-indigo-500 dark:group-hover:border-indigo-400 group-hover:ring-2 group-hover:ring-indigo-500/50 group-hover:scale-105 transition-all shadow-sm flex items-center justify-center relative"
                >
                  <img
                    :src="getChampImgUrl(champ.image_path)"
                    :alt="getDisplayName(champ)"
                    class="w-full h-full object-cover"
                    @error="onImgError"
                  />
                </div>
                <span
                  class="mt-1 text-[11px] font-medium text-center truncate w-full text-gray-800 dark:text-slate-200 group-hover:text-indigo-600 dark:group-hover:text-indigo-400"
                >
                  {{ getDisplayName(champ) }}
                </span>
              </div>
            </div>

            <!-- Empty State -->
            <div
              v-else
              class="py-12 text-center text-gray-500 dark:text-slate-400 space-y-2"
            >
              <p class="text-2xl">🔍</p>
              <p class="text-sm font-medium">{{ $t('champion-modal-no-results') }}</p>
              <button
                @click="resetAllFilters"
                class="px-3 py-1 text-xs font-semibold text-indigo-600 dark:text-indigo-400 border border-indigo-200 dark:border-indigo-800 rounded-md hover:bg-indigo-50 dark:hover:bg-indigo-950 transition-colors"
              >
                {{ $t('champion-modal-filter-reset') }}
              </button>
            </div>
          </div>
        </template>

        <!-- Modal Footer -->
        <div
          class="px-4 py-2.5 border-t border-gray-200 dark:border-slate-800 bg-gray-50 dark:bg-slate-800/60 flex justify-between items-center text-xs text-gray-500 dark:text-slate-400"
        >
          <span>💡 {{ state.locale === 'ko' ? '챔피언을 클릭하면 상세 스탯과 정보가 표시됩니다.' : 'Click on a champion to view details and stats.' }}</span>
          <button
            @click="closeModal"
            class="px-4 py-1.5 text-xs font-semibold text-gray-700 dark:text-slate-200 bg-gray-200 dark:bg-slate-700 hover:bg-gray-300 dark:hover:bg-slate-600 rounded-lg transition-colors"
          >
            {{ state.locale === 'ko' ? '닫기' : 'Close' }}
          </button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup lang="ts">
const props = defineProps<{
  isOpen: boolean
}>()

const emit = defineEmits(['close'])

const state = useStore()
const ALL_KEY = computed(() => state.locale === 'ko' ? '전체' : 'All')

const searchQuery = ref('')
const selectedChoseong = ref('전체')
const selectedChampion = ref<any>(null)
const showFilters = ref(false)

// Selected Filter States
const filterRegion = ref('전체')
const filterRole = ref('전체')
const filterAttackType = ref('전체')
const filterResource = ref('전체')
const filterGender = ref('전체')
const filterSpecies = ref('전체')

const choseongFilters = computed(() => {
  if (state.locale === 'ko') {
    return ['전체', 'ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
  } else {
    return ['All', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
  }
})

const isFilterActive = computed(() => {
  return selectedChoseong.value !== '전체' && selectedChoseong.value !== 'All'
})

const CHOSEONG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
const CHOSEONG_MAP: Record<string, string> = {
  'ㄲ': 'ㄱ',
  'ㄸ': 'ㄷ',
  'ㅃ': 'ㅂ',
  'ㅆ': 'ㅅ',
  'ㅉ': 'ㅈ',
}

// Translations Maps
const REGION_MAP: Record<string, string> = {
  'Bandle City': '밴들 시티',
  'Bilgewater': '빌지워터',
  'Camavor': '카마보르',
  'Demacia': '데마시아',
  'Freljord': '프렐요드',
  'Icathia': '이카시아',
  'Ionia': '아이오니아',
  'Ixtal': '이스타할',
  'Noxus': '녹서스',
  'Piltover': '필트오버',
  'Runeterra': '룬테라',
  'Shadow Isles': '그림자 제도',
  'Shurima': '슈리마',
  'Targon': '타곤',
  'The Void': '공허',
  'Zaun': '자운',
}

const ROLE_MAP: Record<string, string> = {
  'Fighter': '전사',
  'Tank': '탱커',
  'Mage': '마법사',
  'Assassin': '암살자',
  'Support': '서포터',
  'Marksman': '원거리 딜러',
}

const RESOURCE_MAP: Record<string, string> = {
  'Mana': '마나',
  'Energy': '기력',
  'None': '자원 없음',
  'Blood Well': '피의 샘',
  'Rage': '분노',
  'Courage': '용기',
  'Shield': '기류/보호막',
  'Fury': '분노',
  'Ferocity': '야성',
  'Heat': '열기',
  'Grit': '투지',
  'Crimson Rush': '진홍빛 저주',
  'Flow': '기류',
}

const SPECIES_MAP: Record<string, string> = {
  'Human': '인간',
  'Yordle': '요들',
  'Vastaya': '바스타야',
  'Darkin': '다르킨',
  'Demon': '악마',
  'Dragon': '용',
  'Spirit': '영혼/정령',
  'Undead': '언데드',
  'VoidBorn': '공허생물',
  'Celestial': '천상인',
  'Minotaur': '미노타우로스',
  'Troll': '트롤',
  'Ascended': '초월체',
  'Cat': '고양이',
  'Plant': '식물',
  'Rat': '쥐',
  'Cyborg': '사이보그',
  'Robot': '로봇',
  'Golem': '골렘',
  'Construct': '피조물',
  'Elemental': '원소',
  'God-Warrior': '신전사',
  'Brackern': '브라키온',
  'Doll': '인형',
  'Mutant': '변종/변이',
  'Ooze': '생물체',
  'Serpent': '뱀',
  'Spider': '거미',
  'Tree': '나무',
  'Mech': '메카',
}

function translateRegion(r: string): string {
  if (state.locale !== 'ko') return r
  return REGION_MAP[r] ? `${REGION_MAP[r]} (${r})` : r
}

function translateRole(role: string): string {
  if (state.locale !== 'ko') return role
  return ROLE_MAP[role] ? `${ROLE_MAP[role]} (${role})` : role
}

function translateResource(res: string): string {
  if (state.locale !== 'ko') return res
  return RESOURCE_MAP[res] ? `${RESOURCE_MAP[res]} (${res})` : res
}

function translateSpecies(spec: string): string {
  if (state.locale !== 'ko') return spec
  return SPECIES_MAP[spec] ? `${SPECIES_MAP[spec]} (${spec})` : spec
}

// Atomic Available options derived from dataset by splitting '/'
const availableRegions = computed(() => {
  const set = new Set<string>()
  state.api_data.champions.forEach((c) => {
    if (c.region) {
      c.region.split('/').forEach((r: string) => {
        const trimmed = r.trim()
        if (trimmed) set.add(trimmed)
      })
    }
  })
  return Array.from(set).sort()
})

const availableRoles = computed(() => {
  const set = new Set<string>()
  state.api_data.champions.forEach((c) => {
    if (c.tag_1) set.add(c.tag_1)
    if (c.tag_2) set.add(c.tag_2)
  })
  return Array.from(set).sort()
})

const availableResources = computed(() => {
  const set = new Set<string>()
  state.api_data.champions.forEach((c) => {
    if (c.partype) {
      c.partype.split('/').forEach((r: string) => {
        const trimmed = r.trim()
        if (trimmed) set.add(trimmed)
      })
    }
  })
  return Array.from(set).sort()
})

const availableSpecies = computed(() => {
  const set = new Set<string>()
  state.api_data.champions.forEach((c) => {
    if (c.species) {
      c.species.split('/').forEach((s: string) => {
        const trimmed = s.trim()
        if (trimmed) set.add(trimmed)
      })
    }
  })
  return Array.from(set).sort()
})

const activeFilterCount = computed(() => {
  let count = 0
  if (filterRegion.value !== '전체' && filterRegion.value !== 'All') count++
  if (filterRole.value !== '전체' && filterRole.value !== 'All') count++
  if (filterAttackType.value !== '전체' && filterAttackType.value !== 'All') count++
  if (filterResource.value !== '전체' && filterResource.value !== 'All') count++
  if (filterGender.value !== '전체' && filterGender.value !== 'All') count++
  if (filterSpecies.value !== '전체' && filterSpecies.value !== 'All') count++
  return count
})

function getChoseong(str: string): string {
  if (!str) return ''
  const firstChar = str.trim().charAt(0)
  const code = firstChar.charCodeAt(0) - 0xAC00
  if (code >= 0 && code <= 11171) {
    const idx = Math.floor(code / 588)
    const ch = CHOSEONG_LIST[idx] || ''
    return CHOSEONG_MAP[ch] || ch
  }
  return firstChar.toUpperCase()
}

function getDisplayName(champ: any): string {
  if (state.locale === 'ko') {
    return champ.name_ko || state.translateChampionName(champ.name_en, false) || champ.name_en
  }
  return champ.name_en || champ.name
}

const filteredChampions = computed(() => {
  const list = [...(state.api_data.champions || [])]

  // Alphabetical sort based on current locale
  list.sort((a, b) => {
    const nameA = getDisplayName(a)
    const nameB = getDisplayName(b)
    return nameA.localeCompare(nameB, state.locale || 'ko')
  })

  return list.filter((champ) => {
    const displayName = getDisplayName(champ)
    const engName = champ.name_en || ''

    // 1. Text Search Filter
    const matchesQuery =
      searchQuery.value === '' ||
      displayName.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      engName.toLowerCase().includes(searchQuery.value.toLowerCase())

    if (!matchesQuery) return false

    // 2. Choseong / Initial Letter Filter
    if (selectedChoseong.value !== '전체' && selectedChoseong.value !== 'All') {
      const ch = getChoseong(displayName)
      if (ch !== selectedChoseong.value) return false
    }

    // 3. Category Select Filters with Atomic Split Logic
    if (filterRegion.value !== '전체' && filterRegion.value !== 'All') {
      const rList = (champ.region || '').split('/').map((s: string) => s.trim().toLowerCase())
      if (!rList.includes(filterRegion.value.toLowerCase())) return false
    }

    if (filterRole.value !== '전체' && filterRole.value !== 'All') {
      if (champ.tag_1 !== filterRole.value && champ.tag_2 !== filterRole.value) return false
    }

    if (filterAttackType.value !== '전체' && filterAttackType.value !== 'All') {
      if (champ.attack_type?.toLowerCase() !== filterAttackType.value.toLowerCase()) return false
    }

    if (filterResource.value !== '전체' && filterResource.value !== 'All') {
      const resList = (champ.partype || '').split('/').map((s: string) => s.trim().toLowerCase())
      if (!resList.includes(filterResource.value.toLowerCase())) return false
    }

    if (filterGender.value !== '전체' && filterGender.value !== 'All') {
      if (champ.gender !== filterGender.value) return false
    }

    if (filterSpecies.value !== '전체' && filterSpecies.value !== 'All') {
      const sList = (champ.species || '').split('/').map((s: string) => s.trim().toLowerCase())
      if (!sList.includes(filterSpecies.value.toLowerCase())) return false
    }

    return true
  })
})

function resetAllFilters() {
  searchQuery.value = ''
  selectedChoseong.value = ALL_KEY.value
  filterRegion.value = ALL_KEY.value
  filterRole.value = ALL_KEY.value
  filterAttackType.value = ALL_KEY.value
  filterResource.value = ALL_KEY.value
  filterGender.value = ALL_KEY.value
  filterSpecies.value = ALL_KEY.value
}

function getChampImgUrl(path?: string): string {
  if (!path) return missingChampionImageUrl()
  return sprite_base.value + '/' + path
}

function onImgError(e: Event) {
  const target = e.target as HTMLImageElement
  if (target) {
    target.src = missingChampionImageUrl()
  }
}

function closeModal() {
  selectedChampion.value = null
  emit('close')
}

watch(() => props.isOpen, (newVal) => {
  if (!newVal) {
    selectedChampion.value = null
  }
})
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.expand-enter-active,
.expand-leave-active {
  transition: all 0.2s ease;
  max-height: 200px;
  opacity: 1;
  overflow: hidden;
}
.expand-enter-from,
.expand-leave-to {
  max-height: 0;
  opacity: 0;
  overflow: hidden;
}
</style>
