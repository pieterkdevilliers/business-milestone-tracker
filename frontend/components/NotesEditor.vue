<template>
  <div>
    <textarea
      v-model="localContent"
      :placeholder="placeholder"
      rows="4"
      class="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm text-slate-700 resize-y focus:outline-none focus:ring-1 focus:ring-blue-400 bg-white"
      @blur="flush"
      @input="onInput"
    />
    <div class="flex items-center gap-2 mt-1 h-4">
      <span v-if="lastSaved" class="text-xs text-slate-400">
        Saved {{ formatTime(lastSaved) }}
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  content: string
  placeholder?: string
  updatedAt?: string | null
}>()

const emit = defineEmits<{
  (e: "save", content: string): void
}>()

const localContent = ref(props.content)
const lastSaved = ref<Date | null>(props.updatedAt ? new Date(props.updatedAt) : null)
let debounceTimer: ReturnType<typeof setTimeout> | null = null

watch(
  () => props.content,
  (val) => {
    if (val !== localContent.value) localContent.value = val
  }
)

watch(
  () => props.updatedAt,
  (val) => {
    if (val) lastSaved.value = new Date(val)
  }
)

function onInput() {
  if (debounceTimer) clearTimeout(debounceTimer)
  debounceTimer = setTimeout(flush, 500)
}

function flush() {
  if (debounceTimer) clearTimeout(debounceTimer)
  if (localContent.value !== props.content) {
    emit("save", localContent.value)
    lastSaved.value = new Date()
  }
}

function formatTime(d: Date): string {
  return d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
}
</script>
