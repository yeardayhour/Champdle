<template>
  <div v-if="champion" class="space-y-2 text-xs dark:text-slate-300">
    <!-- Image & Hero Banner Card -->
    <div class="flex items-center space-x-3 p-2 rounded-lg bg-gray-100 dark:bg-slate-800 border border-gray-200 dark:border-slate-700">
      <img
        class="w-14 h-14 rounded-full border border-gray-300 dark:border-slate-600 object-cover shadow-sm"
        :alt="state.translateChampionName(champion.name_en, false) || champion.name_en"
        v-lazy="{
          src: championImageUrl,
          error: fallbackChampionImageUrl(champion.image_path),
        }"
      />
      <div>
        <div class="font-bold text-sm text-gray-900 dark:text-slate-100">
          {{ state.translateChampionName(champion.name_en, false) || champion.name_en }}
          <span class="text-xs font-normal text-gray-500 dark:text-slate-400">({{ champion.name_en }})</span>
        </div>
        <div class="italic text-xs text-indigo-600 dark:text-indigo-400 font-medium">
          {{ state.locale === 'ko' ? champion.title_ko : champion.title_en }}
        </div>
        <div v-if="formula_detail" class="mt-1">
          <span class="px-2 py-0.5 text-[11px] font-mono rounded bg-indigo-100 dark:bg-indigo-900/80 text-indigo-800 dark:text-indigo-200">
            📊 계산 구성: {{ formula_detail }}
          </span>
        </div>
      </div>
    </div>

    <!-- Section 1: Official Category Factors (80pts) -->
    <div class="p-2 rounded-lg bg-indigo-50/70 dark:bg-indigo-950/40 border border-indigo-200 dark:border-indigo-900/60">
      <div class="flex items-center justify-between mb-1.5">
        <span class="px-2 py-0.5 text-[11px] font-bold rounded bg-indigo-100 text-indigo-800 dark:bg-indigo-900/80 dark:text-indigo-200">
          📌 공식 카테고리 항목 (80점 만점 요인)
        </span>
      </div>
      <div class="grid grid-cols-1 xs:grid-cols-2 gap-2">
        <ChampionInfoBlock class="bg-white/90 dark:bg-slate-900/90 border-indigo-100 dark:border-indigo-900/40 p-2 space-y-1.5">
          <div class="flex justify-between items-center border-b border-gray-100 dark:border-slate-800 pb-1.5 last:border-0 last:pb-0">
            <span class="text-gray-600 dark:text-slate-400 font-medium">{{ $t('champion-info-release-order') }}</span>
            <span class="font-medium text-gray-800 dark:text-slate-200">{{ champion.champion_id }}번째</span>
          </div>
          <div class="flex justify-between items-center border-b border-gray-100 dark:border-slate-800 pb-1.5 last:border-0 last:pb-0">
            <span class="text-gray-600 dark:text-slate-400 font-medium">{{ $t('champion-info-region') }}</span>
            <span class="font-medium text-gray-800 dark:text-slate-200">{{ trVal(champion.region) }}</span>
          </div>
          <div class="flex justify-between items-center border-b border-gray-100 dark:border-slate-800 pb-1.5 last:border-0 last:pb-0">
            <span class="text-gray-600 dark:text-slate-400 font-medium">{{ $t('champion-info-species') }}</span>
            <span class="font-medium text-gray-800 dark:text-slate-200">{{ trVal(champion.species) }}</span>
          </div>
          <div class="flex justify-between items-center pb-1.5 last:border-0 last:pb-0">
            <span class="text-gray-600 dark:text-slate-400 font-medium">{{ $t('champion-info-gender') }}</span>
            <span class="font-medium text-gray-800 dark:text-slate-200">{{ trVal(champion.gender) }}</span>
          </div>
        </ChampionInfoBlock>

        <ChampionInfoBlock class="bg-white/90 dark:bg-slate-900/90 border-indigo-100 dark:border-indigo-900/40 p-2 space-y-1.5">
          <div class="flex justify-between items-center border-b border-gray-100 dark:border-slate-800 pb-1.5 last:border-0 last:pb-0">
            <span class="text-gray-600 dark:text-slate-400 font-medium">{{ $t('champion-info-attack-type') }}</span>
            <span class="font-medium text-gray-800 dark:text-slate-200">{{ trVal(champion.attack_type) }}</span>
          </div>
          <div class="flex justify-between items-center border-b border-gray-100 dark:border-slate-800 pb-1.5 last:border-0 last:pb-0">
            <span class="text-gray-600 dark:text-slate-400 font-medium">{{ $t('champion-info-resource') }}</span>
            <span class="font-medium text-gray-800 dark:text-slate-200">{{ trVal(champion.partype) }}</span>
          </div>
          <div class="flex justify-between items-center border-b border-gray-100 dark:border-slate-800 pb-1.5 last:border-0 last:pb-0">
            <span class="text-gray-600 dark:text-slate-400 font-medium">{{ $t('champion-info-role-1') }}</span>
            <ChampionInfoTag :class="roleBgClass(champion.tag_1)">{{ trVal(champion.tag_1) }}</ChampionInfoTag>
          </div>
          <div class="flex justify-between items-center pb-1.5 last:border-0 last:pb-0">
            <span class="text-gray-600 dark:text-slate-400 font-medium">{{ $t('champion-info-role-2') }}</span>
            <ChampionInfoTag :class="roleBgClass(champion.tag_2)">{{
              champion.tag_2 !== null && champion.tag_2 !== '' ? trVal(champion.tag_2) : "없음"
            }}</ChampionInfoTag>
          </div>
        </ChampionInfoBlock>
      </div>
    </div>

    <!-- Section 2: Official Stat Factors (20pts) -->
    <div class="p-2 rounded-lg bg-emerald-50/70 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-900/60">
      <div class="flex items-center justify-between mb-1.5">
        <span class="px-2 py-0.5 text-[11px] font-bold rounded bg-emerald-100 text-emerald-800 dark:bg-emerald-900/80 dark:text-emerald-200">
          📊 공식 스탯 Min-Max 항목 (20점 만점 요인)
        </span>
      </div>
      <div class="grid grid-cols-1 xs:grid-cols-2 gap-2">
        <ChampionInfoBlock class="bg-white/90 dark:bg-slate-900/90 border-emerald-100 dark:border-emerald-900/40 p-2.5 space-y-1.5">
          <div class="flex justify-between items-center border-b border-gray-100 dark:border-slate-800 pb-1.5 last:border-0 last:pb-0">
            <span class="text-gray-600 dark:text-slate-400 font-medium">🎯 {{ $t('champion-info-range') }}</span>
            <span class="font-mono text-emerald-700 dark:text-emerald-400">{{ champion.attackrange }}</span>
          </div>
          <div class="flex justify-between items-center border-b border-gray-100 dark:border-slate-800 pb-1.5 last:border-0 last:pb-0">
            <span class="text-gray-600 dark:text-slate-400 font-medium">🏃 {{ $t('champion-info-movespeed') }}</span>
            <span class="font-mono text-emerald-700 dark:text-emerald-400">{{ champion.movespeed }}</span>
          </div>
          <div class="flex justify-between items-center border-b border-gray-100 dark:border-slate-800 pb-1.5 last:border-0 last:pb-0">
            <span class="text-gray-600 dark:text-slate-400 font-medium">❤️ {{ $t('champion-info-hp') }}</span>
            <span class="font-mono text-emerald-700 dark:text-emerald-400">{{ champion.hp_base }} <span class="text-gray-400 dark:text-slate-600 text-[10px]">~</span> {{ champion.hp_max }}</span>
          </div>
          <div class="flex justify-between items-center border-b border-gray-100 dark:border-slate-800 pb-1.5 last:border-0 last:pb-0">
            <span class="text-gray-600 dark:text-slate-400 font-medium">💧 {{ $t('champion-info-mp') }}</span>
            <span class="font-mono text-emerald-700 dark:text-emerald-400">{{ champion.mp_base }} <span class="text-gray-400 dark:text-slate-600 text-[10px]">~</span> {{ champion.mp_max }}</span>
          </div>
          <div class="flex justify-between items-center border-b border-gray-100 dark:border-slate-800 pb-1.5 last:border-0 last:pb-0">
            <span class="text-gray-600 dark:text-slate-400 font-medium">💖 {{ $t('champion-info-hp-regen') }}</span>
            <span class="font-mono text-emerald-700 dark:text-emerald-400">{{ champion.hpregen_base }} <span class="text-gray-400 dark:text-slate-600 text-[10px]">~</span> {{ champion.hpregen_max }}</span>
          </div>
          <div class="flex justify-between items-center pb-1.5 last:border-0 last:pb-0">
            <span class="text-gray-600 dark:text-slate-400 font-medium">💦 {{ $t('champion-info-mp-regen') }}</span>
            <span class="font-mono text-emerald-700 dark:text-emerald-400">{{ champion.mpregen_base }} <span class="text-gray-400 dark:text-slate-600 text-[10px]">~</span> {{ champion.mpregen_max }}</span>
          </div>
        </ChampionInfoBlock>

        <ChampionInfoBlock class="bg-white/90 dark:bg-slate-900/90 border-emerald-100 dark:border-emerald-900/40 p-2.5 space-y-1.5">
          <div class="flex justify-between items-center border-b border-gray-100 dark:border-slate-800 pb-1.5 last:border-0 last:pb-0">
            <span class="text-gray-600 dark:text-slate-400 font-medium">⚔️ {{ $t('champion-info-attack-damage') }}</span>
            <span class="font-mono text-emerald-700 dark:text-emerald-400">{{ champion.attackdamage_base }} <span class="text-gray-400 dark:text-slate-600 text-[10px]">~</span> {{ champion.attackdamage_max }}</span>
          </div>
          <div class="flex justify-between items-center border-b border-gray-100 dark:border-slate-800 pb-1.5 last:border-0 last:pb-0">
            <span class="text-gray-600 dark:text-slate-400 font-medium">🗡️ {{ $t('champion-info-attack-speed') }}</span>
            <span class="font-mono text-emerald-700 dark:text-emerald-400">{{ champion.attackspeed_base }} <span class="text-gray-400 dark:text-slate-600 text-[10px]">~</span> {{ champion.attackspeed_max }}</span>
          </div>
          <div class="flex justify-between items-center border-b border-gray-100 dark:border-slate-800 pb-1.5 last:border-0 last:pb-0">
            <span class="text-gray-600 dark:text-slate-400 font-medium">🛡️ {{ $t('champion-info-armor') }}</span>
            <span class="font-mono text-emerald-700 dark:text-emerald-400">{{ champion.armor_base }} <span class="text-gray-400 dark:text-slate-600 text-[10px]">~</span> {{ champion.armor_max }}</span>
          </div>
          <div class="flex justify-between items-center pb-1.5 last:border-0 last:pb-0">
            <span class="text-gray-600 dark:text-slate-400 font-medium">✨ {{ $t('champion-info-spellblock') }}</span>
            <span class="font-mono text-emerald-700 dark:text-emerald-400">{{ champion.spellblock_base }} <span class="text-gray-400 dark:text-slate-600 text-[10px]">~</span> {{ champion.spellblock_max }}</span>
          </div>
        </ChampionInfoBlock>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const state = useStore()
const props = defineProps<{
  champion: any
  formula_detail?: string
}>()

const championImageUrl = computed(() => {
  if (
    !props.champion ||
    props.champion.image_path === undefined ||
    props.champion.image_path === ""
  ) {
    return missingChampionImageUrl()
  } else {
    return sprite_base.value + "/" + props.champion.image_path
  }
})

function trVal(val: any): string {
  if (val === null || val === undefined || val === '') return '없음'
  if (state.locale !== 'ko') return String(val)
  const map: Record<string, string> = {
    // Roles
    'Fighter': '전사',
    'Tank': '탱커',
    'Mage': '마법사',
    'Assassin': '암살자',
    'Support': '서포터',
    'Marksman': '원거리 딜러',
    // Attack Type
    'Melee': '근접',
    'Ranged': '원거리',
    // Resource
    'Mana': '마나',
    'Energy': '기력',
    'None': '자원 없음',
    'BloodWell': '피의 샘',
    'Rage': '분노',
    'Courage': '용기',
    'Shield': '기류/보호막',
    'Fury': '분노',
    'Ferocity': '야성',
    'Heat': '열기',
    'Grit': '투지',
    'CrimsonRush': '진홍빛 저주',
    'Flow': '기류',
    'Other': '기타',
    // Genders
    'Male': '남성',
    'Female': '여성',
  }
  return map[val] || String(val)
}

function roleBgClass(role?: string): string {
  if (!role) return "bg-none"
  const class_name: Record<string, string> = {
    Fighter: "bg-red-200 dark:bg-red-900",
    Tank: "bg-lime-200 dark:bg-lime-900",
    Mage: "bg-purple-200 dark:bg-purple-900",
    Assassin: "bg-gray-400 dark:bg-gray-700",
    Support: "bg-green-200 dark:bg-green-900",
    Marksman: "bg-orange-200 dark:bg-orange-900",
  }
  return class_name[role] || "bg-none"
}
</script>
