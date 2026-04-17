<template>
  <div class="space-y-2">
    <label
      v-for="ms in milestones"
      :key="ms.id"
      class="flex items-start gap-3 cursor-pointer group"
    >
      <input
        type="checkbox"
        :checked="ms.completed"
        class="mt-0.5 h-4 w-4 rounded border-slate-300 cursor-pointer flex-shrink-0"
        :class="accentClass"
        :disabled="saving.has(ms.id)"
        @change="toggle(ms)"
      />
      <span
        class="text-sm leading-snug transition-colors"
        :class="ms.completed ? 'line-through text-slate-400' : 'text-slate-700'"
      >
        {{ ms.text }}
      </span>
    </label>
  </div>
</template>

<script setup lang="ts">
import type { MilestoneItem } from "~/types/tracker"

const props = defineProps<{
  milestones: MilestoneItem[]
  colour?: string
}>()

const emit = defineEmits<{
  (e: "toggle", milestone: MilestoneItem, completed: boolean): void
}>()

const saving = ref<Set<number>>(new Set())

const accentClass = computed(() => {
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
  return map[props.colour ?? "q1"] ?? "accent-blue-500"
})

async function toggle(ms: MilestoneItem) {
  saving.value.add(ms.id)
  emit("toggle", ms, !ms.completed)
  saving.value.delete(ms.id)
}
</script>
