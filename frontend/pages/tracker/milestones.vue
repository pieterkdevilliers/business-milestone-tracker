<template>
  <div class="p-6">
    <div v-if="store.isLoading" class="py-24 text-center text-slate-400">Loading…</div>

    <template v-else>
      <!-- Header -->
      <div class="mb-6">
        <h1 class="text-2xl font-bold text-slate-900">Master Milestones</h1>
        <p class="text-sm text-slate-500 mt-1">
          The 24 most important moments — {{ completedCount }} of
          {{ store.masterMilestones.length }} complete
        </p>
        <div class="mt-3 max-w-sm">
          <ProgressBar
            :completed="completedCount"
            :total="store.masterMilestones.length"
            colour="q1"
          />
        </div>
      </div>

      <!-- Table -->
      <div class="overflow-x-auto rounded-xl border border-slate-200">
        <table class="w-full text-sm">
          <thead>
            <tr class="bg-slate-50 border-b border-slate-200 text-xs font-semibold uppercase tracking-wide text-slate-500">
              <th class="text-left px-4 py-3 w-8"></th>
              <th class="text-left px-4 py-3 w-28">Target Date</th>
              <th class="text-left px-4 py-3">Milestone</th>
              <th class="text-left px-4 py-3 w-32">Actual Date</th>
              <th class="text-left px-4 py-3 w-48">Notes</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="ms in store.masterMilestones"
              :key="ms.id"
              class="border-b border-slate-100 last:border-0 hover:bg-slate-50 transition-colors"
            >
              <!-- Checkbox -->
              <td class="px-4 py-3 text-center">
                <input
                  type="checkbox"
                  :checked="ms.completed"
                  class="h-4 w-4 rounded cursor-pointer"
                  :class="accentClass(ms.colour_group)"
                  @change="toggleMs(ms)"
                />
              </td>

              <!-- Target date -->
              <td class="px-4 py-3">
                <span
                  class="text-xs font-semibold px-2 py-0.5 rounded-full"
                  :class="badgeClass(ms.colour_group)"
                >
                  {{ ms.target_date }}
                </span>
              </td>

              <!-- Text -->
              <td class="px-4 py-3">
                <span
                  class="text-slate-800 leading-snug"
                  :class="ms.completed ? 'line-through text-slate-400' : ''"
                >
                  {{ ms.text }}
                </span>
              </td>

              <!-- Actual date (inline editable) -->
              <td class="px-4 py-3">
                <input
                  type="text"
                  :value="ms.actual_date ?? ''"
                  placeholder="—"
                  class="w-full border-0 border-b border-transparent hover:border-slate-300 focus:border-blue-400 bg-transparent text-slate-700 text-sm focus:outline-none py-0.5 transition-colors"
                  @blur="saveActualDate(ms, ($event.target as HTMLInputElement).value)"
                  @keydown.enter="($event.target as HTMLInputElement).blur()"
                />
              </td>

              <!-- Notes (inline editable) -->
              <td class="px-4 py-3">
                <input
                  type="text"
                  :value="ms.notes ?? ''"
                  placeholder="—"
                  class="w-full border-0 border-b border-transparent hover:border-slate-300 focus:border-blue-400 bg-transparent text-slate-700 text-sm focus:outline-none py-0.5 transition-colors"
                  @blur="saveNotes(ms, ($event.target as HTMLInputElement).value)"
                  @keydown.enter="($event.target as HTMLInputElement).blur()"
                />
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>

    <SaveToast ref="toast" />
  </div>
</template>

<script setup lang="ts">
import type { MasterMilestone } from "~/types/tracker"

definePageMeta({ layout: "tracker" })

const store = useTrackerStore()
const toast = ref()

await store.fetchAll()

const completedCount = computed(() =>
  store.masterMilestones.filter((ms) => ms.completed).length
)

function accentClass(group: string): string {
  const map: Record<string, string> = {
    q1: "accent-blue-500",
    q2: "accent-green-600",
    q3: "accent-amber-600",
    q4: "accent-slate-700",
    q5: "accent-blue-500",
    q6: "accent-green-600",
    q7: "accent-amber-600",
    q8: "accent-slate-700",
  }
  return map[group] ?? "accent-blue-500"
}

function badgeClass(group: string): string {
  const map: Record<string, string> = {
    q1: "bg-blue-100 text-blue-700",
    q2: "bg-green-100 text-green-700",
    q3: "bg-amber-100 text-amber-700",
    q4: "bg-slate-100 text-slate-600",
    q5: "bg-blue-100 text-blue-700",
    q6: "bg-green-100 text-green-700",
    q7: "bg-amber-100 text-amber-700",
    q8: "bg-slate-100 text-slate-600",
  }
  return map[group] ?? "bg-slate-100 text-slate-600"
}

async function toggleMs(ms: MasterMilestone) {
  try {
    await store.updateMasterMilestone(ms.id, { completed: !ms.completed })
    toast.value?.show()
  } catch {
    toast.value?.show("Error — could not save")
  }
}

async function saveActualDate(ms: MasterMilestone, val: string) {
  const trimmed = val.trim() || null
  if (trimmed === ms.actual_date) return
  try {
    await store.updateMasterMilestone(ms.id, { actual_date: trimmed ?? "" })
    toast.value?.show()
  } catch {
    toast.value?.show("Error — could not save")
  }
}

async function saveNotes(ms: MasterMilestone, val: string) {
  const trimmed = val.trim() || null
  if (trimmed === ms.notes) return
  try {
    await store.updateMasterMilestone(ms.id, { notes: trimmed ?? "" })
    toast.value?.show()
  } catch {
    toast.value?.show("Error — could not save")
  }
}
</script>
