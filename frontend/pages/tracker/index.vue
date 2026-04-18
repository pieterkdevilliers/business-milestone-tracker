<template>
  <div class="p-6 max-w-3xl">
    <!-- Loading -->
    <div v-if="store.isLoading" class="flex items-center justify-center py-24 text-slate-400">
      Loading…
    </div>

    <!-- No data -->
    <div v-else-if="!month" class="py-24 text-center text-slate-400">
      Month not found.
    </div>

    <template v-else>
      <!-- Breadcrumb -->
      <div class="mb-4">
        <NuxtLink
          v-if="quarter"
          :to="`/tracker/quarter/${quarter.quarter_number}`"
          class="text-sm text-slate-400 hover:text-slate-600 transition-colors"
        >
          ← {{ quarter.label }}
        </NuxtLink>
      </div>

      <!-- Month header -->
      <div
        class="rounded-xl px-6 py-5 mb-6 text-white"
        :class="headerBg"
      >
        <div class="text-xs font-semibold uppercase tracking-widest opacity-75 mb-1">
          {{ quarterLabel }}
        </div>
        <h1 class="text-2xl font-bold">{{ month.month_name }} {{ month.year }}</h1>
        <p class="text-sm opacity-80 mt-1">{{ month.theme }}</p>
        <div class="mt-3">
          <ProgressBar
            :completed="completedCount"
            :total="month.milestones.length"
            :colour="colour"
          />
        </div>
      </div>

      <!-- Milestones -->
      <section class="bg-white rounded-xl border border-slate-200 p-5 mb-4">
        <h2 class="text-xs font-semibold uppercase tracking-widest text-slate-400 mb-4">
          Milestones
        </h2>
        <MilestoneList
          :milestones="month.milestones"
          :colour="colour"
          @toggle="handleToggle"
        />
      </section>

      <!-- Target vs Actual -->
      <section class="bg-white rounded-xl border border-slate-200 p-5 mb-4">
        <h2 class="text-xs font-semibold uppercase tracking-widest text-slate-400 mb-4">
          Target vs Actual
        </h2>
        <MetricsTable
          :metrics="month.metrics"
          @update="handleMetricUpdate"
        />
      </section>

      <!-- Notes -->
      <section class="bg-white rounded-xl border border-slate-200 p-5">
        <h2 class="text-xs font-semibold uppercase tracking-widest text-slate-400 mb-3">
          Notes / Reflections
        </h2>
        <NotesEditor
          :content="month.note?.content ?? ''"
          :updated-at="month.note?.updated_at ?? null"
          placeholder="What happened this month? What surprised you? What would you do differently?"
          @save="handleNoteSave"
        />
      </section>
    </template>

    <SaveToast ref="toast" />
  </div>
</template>

<script setup lang="ts">
import type { MilestoneItem } from "~/types/tracker"

definePageMeta({ layout: "tracker" })

const store = useTrackerStore()
const route = useRoute()
const toast = ref()

await store.fetchAll()

const sortOrder = computed(() => {
  const q = Number(route.query.month)
  if (!isNaN(q) && q >= 1 && q <= 24) return q
  return defaultSortOrder()
})

function defaultSortOrder(): number {
  const now = new Date()
  const names = [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December",
  ]
  const m = store.months.find(
    (mo) => mo.year === now.getFullYear() && names.indexOf(mo.month_name) + 1 === now.getMonth() + 1
  )
  if (m) return m.sort_order
  if (now < new Date(2026, 3, 1)) return 1
  return store.months.length > 0 ? store.months[store.months.length - 1].sort_order : 1
}

const month = computed(() =>
  store.months.find((m) => m.sort_order === sortOrder.value) ?? null
)

const quarter = computed(() =>
  store.quarters.find((q) => q.id === month.value?.quarter_id) ?? null
)

const colour = computed(() =>
  quarter.value ? store.getQuarterColour(quarter.value.quarter_number) : "q1"
)

const headerBg = computed(() => {
  const map: Record<string, string> = {
    q1: "bg-blue-500",
    q2: "bg-green-700",
    q3: "bg-amber-700",
    q4: "bg-slate-800",
    q5: "bg-blue-500",
    q6: "bg-green-700",
    q7: "bg-amber-700",
    q8: "bg-slate-800",
  }
  return map[colour.value] ?? "bg-blue-500"
})

const quarterLabel = computed(() => quarter.value?.label ?? "")

const completedCount = computed(() =>
  month.value ? month.value.milestones.filter((ms) => ms.completed).length : 0
)

async function handleToggle(ms: MilestoneItem, completed: boolean) {
  try {
    await store.toggleMilestone(ms.id, completed)
    toast.value?.show()
  } catch {
    toast.value?.show("Error — could not save")
  }
}

async function handleMetricUpdate(id: number, actual: string | null) {
  try {
    await store.updateMonthMetric(id, actual)
    toast.value?.show()
  } catch {
    toast.value?.show("Error — could not save")
  }
}

async function handleNoteSave(content: string) {
  if (!month.value) return
  try {
    await store.updateMonthNote(month.value.id, content)
  } catch {
    toast.value?.show("Error — could not save note")
  }
}
</script>
