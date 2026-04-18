<template>
  <div class="p-6 max-w-4xl">
    <div v-if="store.isLoading" class="py-24 text-center text-slate-400">Loading…</div>

    <div v-else-if="!quarter" class="py-24 text-center text-slate-400">
      Quarter not found.
    </div>

    <template v-else>
      <!-- Quarter header -->
      <div class="rounded-xl px-6 py-5 mb-6 text-white" :class="headerBg">
        <div class="text-xs font-semibold uppercase tracking-widest opacity-70 mb-1">
          Year {{ quarter.year }}
        </div>
        <h1 class="text-2xl font-bold">{{ quarter.label }}</h1>
        <p class="text-sm opacity-80 mt-1">{{ quarter.theme }}</p>
        <div class="mt-3 max-w-sm">
          <ProgressBar :completed="qCompleted" :total="qTotal" :colour="colour" />
        </div>
      </div>

      <!-- Month cards -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
        <NuxtLink
          v-for="month in quarter.months"
          :key="month.id"
          :to="`/tracker?month=${month.sort_order}`"
          class="bg-white rounded-xl border p-5 hover:shadow-md transition-all group"
          :class="isCurrentMonth(month) ? 'border-blue-300 ring-2 ring-blue-100' : 'border-slate-200 hover:border-slate-300'"
        >
          <!-- Month name + "current" badge -->
          <div class="flex items-start justify-between mb-1">
            <div class="font-bold text-slate-800 group-hover:text-slate-900">
              {{ month.month_name }} {{ month.year }}
            </div>
            <span
              v-if="isCurrentMonth(month)"
              class="text-xs font-semibold px-2 py-0.5 rounded-full ml-2 flex-shrink-0"
              :class="badgeClass"
            >
              Now
            </span>
          </div>

          <p class="text-xs text-slate-500 leading-snug mb-3">{{ month.theme }}</p>

          <!-- Milestone progress -->
          <ProgressBar
            :completed="monthCompleted(month)"
            :total="month.milestones.length"
            :colour="colour"
          />

          <!-- Milestone mini-list (first 3 items) -->
          <ul class="mt-3 space-y-1">
            <li
              v-for="ms in month.milestones.slice(0, 3)"
              :key="ms.id"
              class="flex items-start gap-1.5 text-xs"
              :class="ms.completed ? 'text-slate-400 line-through' : 'text-slate-600'"
            >
              <span class="mt-px flex-shrink-0">{{ ms.completed ? '✓' : '·' }}</span>
              <span class="truncate">{{ ms.text }}</span>
            </li>
            <li
              v-if="month.milestones.length > 3"
              class="text-xs text-slate-400 pl-3"
            >
              +{{ month.milestones.length - 3 }} more →
            </li>
          </ul>
        </NuxtLink>
      </div>

      <!-- Quarter review metrics -->
      <section class="bg-white rounded-xl border border-slate-200 p-5 mb-4">
        <h2 class="text-xs font-semibold uppercase tracking-widest text-slate-400 mb-4">
          Quarter Review — Target vs Actual
        </h2>
        <MetricsTable :metrics="quarter.metrics" @update="handleMetricUpdate" />
      </section>

      <!-- Quarter notes -->
      <section class="bg-white rounded-xl border border-slate-200 p-5">
        <h2 class="text-xs font-semibold uppercase tracking-widest text-slate-400 mb-3">
          Quarter Notes
        </h2>
        <NotesEditor
          :content="quarter.note?.content ?? ''"
          :updated-at="quarter.note?.updated_at ?? null"
          placeholder="Quarter reflections — what changed, what you'd do differently."
          @save="handleNoteSave"
        />
      </section>
    </template>

    <SaveToast ref="toast" />
  </div>
</template>

<script setup lang="ts">
import type { MonthDetail } from "~/types/tracker"

definePageMeta({ layout: "tracker" })

const store = useTrackerStore()
const route = useRoute()
const toast = ref()

await store.fetchAll()

const quarterNumber = computed(() => Number(route.params.id))

const quarter = computed(() =>
  store.quarters.find((q) => q.quarter_number === quarterNumber.value) ?? null
)

const colour = computed(() =>
  quarter.value ? store.getQuarterColour(quarter.value.quarter_number) : "q1"
)

const headerBg = computed(() => {
  const map: Record<string, string> = {
    q1: "bg-blue-500", q2: "bg-green-700", q3: "bg-amber-700", q4: "bg-slate-800",
    q5: "bg-blue-500", q6: "bg-green-700", q7: "bg-amber-700", q8: "bg-slate-800",
  }
  return map[colour.value] ?? "bg-blue-500"
})

const badgeClass = computed(() => {
  const map: Record<string, string> = {
    q1: "bg-blue-100 text-blue-700", q2: "bg-green-100 text-green-700",
    q3: "bg-amber-100 text-amber-700", q4: "bg-slate-200 text-slate-700",
    q5: "bg-blue-100 text-blue-700", q6: "bg-green-100 text-green-700",
    q7: "bg-amber-100 text-amber-700", q8: "bg-slate-200 text-slate-700",
  }
  return map[colour.value] ?? "bg-blue-100 text-blue-700"
})

const qTotal = computed(() =>
  quarter.value ? quarter.value.months.reduce((s, m) => s + m.milestones.length, 0) : 0
)

const qCompleted = computed(() =>
  quarter.value
    ? quarter.value.months.reduce((s, m) => s + monthCompleted(m), 0)
    : 0
)

function monthCompleted(month: MonthDetail): number {
  return month.milestones.filter((ms) => ms.completed).length
}

function isCurrentMonth(month: MonthDetail): boolean {
  const now = new Date()
  const names = ["January","February","March","April","May","June",
    "July","August","September","October","November","December"]
  return month.year === now.getFullYear() && names.indexOf(month.month_name) + 1 === now.getMonth() + 1
}

async function handleMetricUpdate(id: number, actual: string | null) {
  try {
    await store.updateQuarterMetric(id, actual)
    toast.value?.show()
  } catch {
    toast.value?.show("Error — could not save")
  }
}

async function handleNoteSave(content: string) {
  if (!quarter.value) return
  try {
    await store.updateQuarterNote(quarter.value.id, content)
  } catch {
    toast.value?.show("Error — could not save note")
  }
}
</script>
