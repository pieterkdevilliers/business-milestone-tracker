<template>
  <div class="overflow-hidden rounded-lg border border-slate-200">
    <table class="w-full text-sm">
      <thead>
        <tr class="text-xs font-semibold uppercase tracking-wide text-slate-500 border-b border-slate-200">
          <th class="text-left px-4 py-2 w-1/2">Metric</th>
          <th class="text-left px-4 py-2 w-1/4">Target</th>
          <th class="text-left px-4 py-2 w-1/4">Actual</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(metric, i) in metrics"
          :key="metric.id"
          class="border-b border-slate-100 last:border-0"
          :class="i % 2 === 0 ? 'bg-white' : 'bg-slate-50'"
        >
          <td class="px-4 py-2 text-slate-700 font-medium">{{ metric.label }}</td>
          <td class="px-4 py-2 text-slate-500">{{ metric.target }}</td>
          <td class="px-4 py-2">
            <input
              v-if="editingId === metric.id"
              ref="inputRef"
              v-model="editValue"
              type="text"
              class="w-full border border-slate-300 rounded px-2 py-0.5 text-sm focus:outline-none focus:ring-1 focus:ring-blue-400"
              @blur="save(metric)"
              @keydown.enter="save(metric)"
              @keydown.escape="cancel"
            />
            <button
              v-else
              class="w-full text-left min-h-[1.5rem] px-2 py-0.5 rounded hover:bg-slate-100 transition-colors text-slate-700"
              :class="metric.actual ? '' : 'text-slate-300 italic'"
              @click="startEdit(metric)"
            >
              {{ metric.actual ?? "—" }}
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import type { MonthMetric, QuarterMetric } from "~/types/tracker"

const props = defineProps<{
  metrics: MonthMetric[] | QuarterMetric[]
}>()

const emit = defineEmits<{
  (e: "update", id: number, actual: string | null): void
}>()

const editingId = ref<number | null>(null)
const editValue = ref("")
const inputRef = ref<HTMLInputElement | null>(null)

function startEdit(metric: MonthMetric | QuarterMetric) {
  editingId.value = metric.id
  editValue.value = metric.actual ?? ""
  nextTick(() => inputRef.value?.focus())
}

function save(metric: MonthMetric | QuarterMetric) {
  const val = editValue.value.trim() || null
  if (val !== metric.actual) {
    emit("update", metric.id, val)
  }
  editingId.value = null
}

function cancel() {
  editingId.value = null
}
</script>
