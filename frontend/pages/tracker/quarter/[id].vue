<template>
  <div class="p-6 max-w-3xl">
    <div v-if="store.isLoading" class="py-24 text-center text-slate-400">Loading…</div>

    <div v-else-if="!quarter" class="py-24 text-center text-slate-400">
      Quarter not found.
    </div>

    <template v-else>
      <!-- Quarter header -->
      <div class="rounded-xl px-6 py-5 mb-6 text-white" :class="headerBg">
        <div class="text-xs font-semibold uppercase tracking-widest opacity-75 mb-1">
          Year {{ quarter.year }}
        </div>
        <h1 class="text-2xl font-bold">{{ quarter.label }}</h1>
        <p class="text-sm opacity-80 mt-1">{{ quarter.theme }}</p>
        <div class="mt-3">
          <ProgressBar
            :completed="qCompleted"
            :total="qTotal"
            :colour="colour"
          />
        </div>
      </div>

      <!-- Month cards -->
      <section class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
        <NuxtLink
          v-for="month in quarter.months"
          :key="month.id"
          :to="`/tracker?month=${month.sort_order}`"
          class="bg-white rounded-xl border border-slate-200 p-4 hover:border-slate-300 hover:shadow-sm transition-all"
        >
          <div class="font-semibold text-slate-800 mb-1">
            {{ month.month_name }} {{ month.year }}
          </div>
          <div class="text-xs text-slate-500 mb-3 leading-snug">{{ month.theme }}</div>
          <ProgressBar
            :completed="monthCompleted(month)"
            :total="month.milestones.length"
            :colour="colour"
          />
        </NuxtLink>
      </section>

      <!-- Quarter review metrics -->
      <section class="bg-white rounded-xl border border-slate-200 p-5 mb-4">
        <h2 class="text-xs font-semibold uppercase tracking-widest text-slate-400 mb-4">
          Quarter Review — Target vs Actual
        </h2>
        <MetricsTable
          :metrics="quarter.metrics"
          @update="handleMetricUpdate"
        />
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

const qTotal = computed(() =>
  quarter.value
    ? quarter.value.months.reduce((s, m) => s + m.milestones.length, 0)
    : 0
)

const qCompleted = computed(() =>
  quarter.value
    ? quarter.value.months.reduce(
        (s, m) => s + m.milestones.filter((ms) => ms.completed).length,
        0
      )
    : 0
)

function monthCompleted(month: MonthDetail): number {
  return month.milestones.filter((ms) => ms.completed).length
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
