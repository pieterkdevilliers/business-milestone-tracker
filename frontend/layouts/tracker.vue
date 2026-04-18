<template>
  <div class="flex h-screen bg-slate-50 overflow-hidden">
    <!-- Slim sidebar -->
    <aside class="w-52 flex-shrink-0 bg-slate-900 text-slate-100 flex flex-col overflow-hidden">
      <!-- Brand -->
      <div class="px-5 py-4 border-b border-slate-700">
        <div class="text-xs font-semibold uppercase tracking-widest text-slate-400 mb-1">
          Blindspot Works
        </div>
        <div class="text-sm font-bold text-white leading-tight">
          Milestone Tracker
        </div>
        <div class="text-xs text-slate-400 mt-0.5">Apr 2026 — Mar 2028</div>
      </div>

      <!-- Overall progress -->
      <div class="px-5 py-3 border-b border-slate-700">
        <div class="flex justify-between text-xs text-slate-400 mb-1.5">
          <span>Overall</span>
          <span>{{ store.completedMilestones }}/{{ store.totalMilestones }}</span>
        </div>
        <div class="h-1.5 bg-slate-700 rounded-full overflow-hidden">
          <div
            class="h-full bg-blue-500 rounded-full transition-all duration-300"
            :style="{ width: overallPct + '%' }"
          />
        </div>
        <div class="text-xs text-slate-500 mt-1">{{ overallPct }}% complete</div>
      </div>

      <!-- Navigation links -->
      <nav class="p-3 space-y-1">
        <NuxtLink
          to="/tracker"
          class="flex items-center gap-2 px-3 py-2 rounded-lg text-sm transition-colors"
          :class="
            route.path === '/tracker'
              ? 'bg-slate-700 text-white'
              : 'text-slate-400 hover:bg-slate-700 hover:text-white'
          "
        >
          <span>📅</span>
          <span>Current Month</span>
        </NuxtLink>

        <NuxtLink
          to="/tracker/milestones"
          class="flex items-center gap-2 px-3 py-2 rounded-lg text-sm transition-colors"
          :class="
            route.path === '/tracker/milestones'
              ? 'bg-slate-700 text-white'
              : 'text-slate-400 hover:bg-slate-700 hover:text-white'
          "
        >
          <span>★</span>
          <span>24 Key Milestones</span>
        </NuxtLink>
      </nav>

      <!-- Quarter quick links -->
      <div class="px-3 mt-2">
        <div class="text-xs font-semibold uppercase tracking-widest text-slate-500 px-3 mb-2">
          Quarters
        </div>
        <div class="space-y-0.5">
          <NuxtLink
            v-for="q in store.quarters"
            :key="q.id"
            :to="`/tracker/quarter/${q.quarter_number}`"
            class="flex items-center justify-between px-3 py-1.5 rounded-lg text-xs transition-colors"
            :class="
              isActiveQuarter(q.quarter_number)
                ? 'bg-slate-700 text-white font-semibold'
                : 'text-slate-400 hover:bg-slate-700 hover:text-slate-200'
            "
          >
            <span :class="quarterTextClass(q.quarter_number)">Q{{ q.quarter_number }}</span>
            <span class="text-slate-500 ml-1 flex-1 truncate pl-1">{{ q.theme.split('—')[0].trim() }}</span>
            <span class="text-slate-600 ml-1">
              {{ quarterCompletedCount(q) }}/{{ quarterTotalCount(q) }}
            </span>
          </NuxtLink>
        </div>
      </div>
    </aside>

    <!-- Main content -->
    <div class="flex-1 flex flex-col overflow-hidden">

      <!-- Quarter tab bar -->
      <div class="bg-white border-b border-slate-200 flex-shrink-0 px-4">
        <div class="flex overflow-x-auto gap-0.5 -mb-px">
          <NuxtLink
            v-for="q in store.quarters"
            :key="q.id"
            :to="`/tracker/quarter/${q.quarter_number}`"
            class="flex-shrink-0 flex flex-col items-center px-4 py-3 border-b-2 text-sm font-medium transition-colors whitespace-nowrap"
            :class="
              isActiveQuarter(q.quarter_number)
                ? [activeTabBorder(q.quarter_number), activeTabText(q.quarter_number), 'border-b-2']
                : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300'
            "
          >
            <span class="font-bold">Q{{ q.quarter_number }}</span>
            <span class="text-xs opacity-60">Y{{ q.year }}</span>
            <div class="flex gap-0.5 mt-1">
              <span
                v-for="m in q.months"
                :key="m.id"
                class="h-1 w-3 rounded-full"
                :class="monthDotClass(m, q.quarter_number)"
                :title="`${m.month_name}: ${monthCompleted(m)}/${m.milestones.length}`"
              />
            </div>
          </NuxtLink>
        </div>
      </div>

      <!-- Page -->
      <main class="flex-1 overflow-y-auto">
        <NuxtPage />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { QuarterDetail, MonthDetail } from "~/types/tracker"

const store = useTrackerStore()
const route = useRoute()

await store.fetchAll()

const overallPct = computed(() => {
  if (store.totalMilestones === 0) return 0
  return Math.round((store.completedMilestones / store.totalMilestones) * 100)
})

function activeQuarterNumber(): number | null {
  if (route.path.startsWith("/tracker/quarter/")) {
    return Number(route.params.id) || null
  }
  if (route.path === "/tracker") {
    const s = Number(route.query.month)
    const sortOrder = isNaN(s) ? currentMonthSortOrder() : s
    const month = store.months.find((m) => m.sort_order === sortOrder)
    if (month) {
      const q = store.quarters.find((q) => q.id === month.quarter_id)
      return q?.quarter_number ?? null
    }
  }
  return null
}

function currentMonthSortOrder(): number {
  const now = new Date()
  const names = ["January","February","March","April","May","June",
    "July","August","September","October","November","December"]
  const m = store.months.find(
    (mo) => mo.year === now.getFullYear() && names.indexOf(mo.month_name) + 1 === now.getMonth() + 1
  )
  return m?.sort_order ?? 1
}

function isActiveQuarter(qNum: number): boolean {
  return activeQuarterNumber() === qNum
}

function quarterTextClass(qNum: number): string {
  const map: Record<number, string> = {
    1: "text-blue-400", 2: "text-green-400", 3: "text-amber-400", 4: "text-slate-300",
    5: "text-blue-400", 6: "text-green-400", 7: "text-amber-400", 8: "text-slate-300",
  }
  return map[qNum] ?? "text-slate-300"
}

function activeTabBorder(qNum: number): string {
  const map: Record<number, string> = {
    1: "border-blue-500", 2: "border-green-600", 3: "border-amber-600", 4: "border-slate-700",
    5: "border-blue-500", 6: "border-green-600", 7: "border-amber-600", 8: "border-slate-700",
  }
  return map[qNum] ?? "border-blue-500"
}

function activeTabText(qNum: number): string {
  const map: Record<number, string> = {
    1: "text-blue-600", 2: "text-green-700", 3: "text-amber-700", 4: "text-slate-800",
    5: "text-blue-600", 6: "text-green-700", 7: "text-amber-700", 8: "text-slate-800",
  }
  return map[qNum] ?? "text-blue-600"
}

function monthDotClass(month: MonthDetail, qNum: number): string {
  const done = monthCompleted(month)
  const total = month.milestones.length
  if (done === total && total > 0) {
    const colours: Record<number, string> = {
      1: "bg-blue-500", 2: "bg-green-600", 3: "bg-amber-600", 4: "bg-slate-600",
      5: "bg-blue-500", 6: "bg-green-600", 7: "bg-amber-600", 8: "bg-slate-600",
    }
    return colours[qNum] ?? "bg-blue-500"
  }
  if (done > 0) return "bg-slate-300"
  return "bg-slate-200"
}

function monthCompleted(month: MonthDetail): number {
  return month.milestones.filter((ms) => ms.completed).length
}

function quarterCompletedCount(q: QuarterDetail): number {
  return q.months.reduce((s, m) => s + monthCompleted(m), 0)
}

function quarterTotalCount(q: QuarterDetail): number {
  return q.months.reduce((s, m) => s + m.milestones.length, 0)
}
</script>
