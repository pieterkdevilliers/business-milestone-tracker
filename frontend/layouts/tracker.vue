<template>
  <div class="flex h-screen bg-slate-50 overflow-hidden">
    <!-- Sidebar -->
    <aside class="w-64 flex-shrink-0 bg-slate-900 text-slate-100 flex flex-col overflow-hidden">
      <!-- Header -->
      <div class="px-5 py-4 border-b border-slate-700">
        <div class="text-xs font-semibold uppercase tracking-widest text-slate-400 mb-1">
          Blindspot Works
        </div>
        <div class="text-base font-bold text-white leading-tight">
          Two-Year Milestone Tracker
        </div>
        <div class="text-xs text-slate-400 mt-0.5">Apr 2026 — Mar 2028</div>
      </div>

      <!-- Overall progress -->
      <div class="px-5 py-3 border-b border-slate-700">
        <div class="flex justify-between text-xs text-slate-400 mb-1">
          <span>Overall progress</span>
          <span>{{ store.completedMilestones }}/{{ store.totalMilestones }}</span>
        </div>
        <div class="h-1.5 bg-slate-700 rounded-full overflow-hidden">
          <div
            class="h-full bg-blue-500 rounded-full transition-all"
            :style="{ width: overallPct + '%' }"
          />
        </div>
      </div>

      <!-- Master milestones link -->
      <div class="px-3 py-2 border-b border-slate-700">
        <NuxtLink
          to="/tracker/milestones"
          class="flex items-center gap-2 px-3 py-2 rounded-lg text-sm text-slate-300 hover:bg-slate-700 hover:text-white transition-colors"
          :class="{ 'bg-slate-700 text-white': route.path === '/tracker/milestones' }"
        >
          <span class="text-base">★</span>
          <span>Master Milestones</span>
        </NuxtLink>
      </div>

      <!-- Quarter / month tree -->
      <nav class="flex-1 overflow-y-auto py-2 px-3 space-y-1">
        <div v-for="quarter in store.quarters" :key="quarter.id">
          <!-- Quarter row -->
          <button
            class="w-full flex items-center gap-2 px-3 py-2 rounded-lg text-xs font-semibold uppercase tracking-wide hover:bg-slate-700 transition-colors text-left"
            :class="[
              quarterTextClass(quarter.quarter_number),
              isQuarterOpen(quarter.quarter_number) ? 'bg-slate-800' : '',
            ]"
            @click="toggleQuarter(quarter.quarter_number)"
          >
            <span class="flex-1">{{ quarterShortLabel(quarter) }}</span>
            <NuxtLink
              :to="`/tracker/quarter/${quarter.quarter_number}`"
              class="ml-auto text-slate-400 hover:text-white text-xs px-1"
              title="Quarter review"
              @click.stop
            >
              ↗
            </NuxtLink>
            <span class="text-slate-500 text-xs">{{ isQuarterOpen(quarter.quarter_number) ? '▾' : '▸' }}</span>
          </button>

          <!-- Month links -->
          <div v-if="isQuarterOpen(quarter.quarter_number)" class="ml-2 space-y-0.5">
            <NuxtLink
              v-for="month in quarter.months"
              :key="month.id"
              :to="`/tracker?month=${month.sort_order}`"
              class="flex items-center justify-between px-3 py-1.5 rounded-md text-sm text-slate-400 hover:bg-slate-700 hover:text-white transition-colors"
              :class="{
                'bg-slate-700 text-white': isCurrentNav(month.sort_order),
                'font-medium': isCurrentMonth(month),
              }"
            >
              <span>{{ month.month_name }} {{ month.year }}</span>
              <span class="text-xs text-slate-500">
                {{ completedCount(month) }}/{{ month.milestones.length }}
              </span>
            </NuxtLink>
          </div>
        </div>
      </nav>
    </aside>

    <!-- Main content -->
    <main class="flex-1 overflow-y-auto">
      <NuxtPage />
    </main>
  </div>
</template>

<script setup lang="ts">
import type { QuarterDetail, MonthDetail } from "~/types/tracker"

const store = useTrackerStore()
const route = useRoute()

await store.fetchAll()

const openQuarters = ref<Set<number>>(new Set())

const currentMonthSortOrder = computed(() => {
  const q = Number(route.query.month)
  return isNaN(q) ? defaultMonthSortOrder() : q
})

function defaultMonthSortOrder(): number {
  const now = new Date()
  const y = now.getFullYear()
  const m = now.getMonth() + 1 // 1-based
  const month = store.months.find((mo) => mo.year === y && monthIndex(mo.month_name) === m)
  if (month) return month.sort_order
  if (y < 2026 || (y === 2026 && m < 4)) return 1
  return store.months.length > 0 ? store.months[store.months.length - 1].sort_order : 1
}

function monthIndex(name: string): number {
  return [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December",
  ].indexOf(name) + 1
}

function isCurrentNav(sortOrder: number): boolean {
  return sortOrder === currentMonthSortOrder.value
}

function isCurrentMonth(month: MonthDetail): boolean {
  const now = new Date()
  return month.year === now.getFullYear() && monthIndex(month.month_name) === now.getMonth() + 1
}

function toggleQuarter(qNum: number) {
  if (openQuarters.value.has(qNum)) {
    openQuarters.value.delete(qNum)
  } else {
    openQuarters.value.add(qNum)
  }
}

function isQuarterOpen(qNum: number): boolean {
  return openQuarters.value.has(qNum)
}

function quarterShortLabel(q: QuarterDetail): string {
  return `Q${q.quarter_number} · Y${q.year}`
}

function quarterTextClass(qNum: number): string {
  const map: Record<number, string> = {
    1: "text-blue-400",
    2: "text-green-400",
    3: "text-amber-500",
    4: "text-slate-300",
    5: "text-blue-400",
    6: "text-green-400",
    7: "text-amber-500",
    8: "text-slate-300",
  }
  return map[qNum] ?? "text-slate-300"
}

function completedCount(month: MonthDetail): number {
  return month.milestones.filter((ms) => ms.completed).length
}

const overallPct = computed(() => {
  if (store.totalMilestones === 0) return 0
  return Math.round((store.completedMilestones / store.totalMilestones) * 100)
})

// Auto-open the quarter that contains the active month
watch(
  () => store.quarters,
  (qs) => {
    for (const q of qs) {
      const hasActive = q.months.some((m) => m.sort_order === currentMonthSortOrder.value)
      if (hasActive) openQuarters.value.add(q.quarter_number)
    }
  },
  { immediate: true }
)

watch(currentMonthSortOrder, (sortOrder) => {
  for (const q of store.quarters) {
    if (q.months.some((m) => m.sort_order === sortOrder)) {
      openQuarters.value.add(q.quarter_number)
    }
  }
})
</script>
