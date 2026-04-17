<template>
  <div>
    <div class="flex justify-between text-xs text-slate-500 mb-1">
      <span>{{ completed }} of {{ total }} milestones complete</span>
      <span>{{ pct }}%</span>
    </div>
    <div class="h-2 bg-slate-200 rounded-full overflow-hidden">
      <div
        class="h-full rounded-full transition-all duration-300"
        :class="barColour"
        :style="{ width: pct + '%' }"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  completed: number
  total: number
  colour?: string
}>()

const pct = computed(() =>
  props.total === 0 ? 0 : Math.round((props.completed / props.total) * 100)
)

const barColour = computed(() => {
  const map: Record<string, string> = {
    q1: "bg-blue-500",
    q2: "bg-green-600",
    q3: "bg-amber-600",
    q4: "bg-slate-700",
    q5: "bg-blue-500",
    q6: "bg-green-600",
    q7: "bg-amber-600",
    q8: "bg-slate-700",
  }
  return map[props.colour ?? "q1"] ?? "bg-blue-500"
})
</script>
