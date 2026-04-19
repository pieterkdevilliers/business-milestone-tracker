<template>
  <div class="space-y-1">
    <div
      v-for="ms in milestones"
      :key="ms.id"
      class="flex items-start gap-2 group rounded-lg px-1 py-0.5 hover:bg-slate-50"
    >
      <!-- Checkbox -->
      <input
        type="checkbox"
        :checked="ms.completed"
        class="mt-1 h-4 w-4 rounded border-slate-300 cursor-pointer flex-shrink-0"
        :class="accentClass"
        @change="toggle(ms)"
      />

      <!-- Inline text editor -->
      <div class="flex-1 min-w-0">
        <input
          v-if="editingId === ms.id"
          ref="editInput"
          v-model="editText"
          class="w-full text-sm text-slate-700 bg-white border border-slate-300 rounded px-2 py-0.5 focus:outline-none focus:ring-1 focus:ring-blue-400"
          @keydown.enter="saveEdit(ms)"
          @keydown.escape="cancelEdit"
          @blur="saveEdit(ms)"
        />
        <span
          v-else
          class="text-sm leading-snug"
          :class="ms.completed ? 'line-through text-slate-400' : 'text-slate-700'"
        >
          {{ ms.text }}
        </span>
      </div>

      <!-- Action buttons (visible on hover) -->
      <div class="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity flex-shrink-0 mt-0.5">
        <button
          v-if="editingId !== ms.id"
          class="text-slate-400 hover:text-slate-600 p-0.5 rounded"
          title="Edit"
          @click="startEdit(ms)"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" viewBox="0 0 20 20" fill="currentColor">
            <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
          </svg>
        </button>
        <button
          class="text-slate-400 hover:text-red-500 p-0.5 rounded"
          title="Delete"
          @click="remove(ms)"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Add milestone row -->
    <div class="pt-1">
      <div v-if="adding" class="flex items-center gap-2 px-1">
        <div class="w-4 flex-shrink-0" />
        <input
          ref="addInput"
          v-model="addText"
          placeholder="New milestone…"
          class="flex-1 text-sm text-slate-700 bg-white border border-slate-300 rounded px-2 py-1 focus:outline-none focus:ring-1 focus:ring-blue-400"
          @keydown.enter="confirmAdd"
          @keydown.escape="cancelAdd"
          @blur="confirmAdd"
        />
        <button
          class="text-slate-400 hover:text-red-500 p-0.5"
          @mousedown.prevent="cancelAdd"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>
      <button
        v-else
        class="flex items-center gap-1.5 text-xs text-slate-400 hover:text-slate-600 px-1 py-1 transition-colors"
        @click="startAdd"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
        </svg>
        Add milestone
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { MilestoneItem } from "~/types/tracker"

const props = defineProps<{
  milestones: MilestoneItem[]
  colour?: string
  monthId: number
}>()

const emit = defineEmits<{
  (e: "toggle", milestone: MilestoneItem, completed: boolean): void
  (e: "edit-saved"): void
  (e: "deleted"): void
  (e: "added"): void
}>()

const store = useTrackerStore()

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

function toggle(ms: MilestoneItem) {
  emit("toggle", ms, !ms.completed)
}

// --- Edit ---
const editingId = ref<number | null>(null)
const editText = ref("")
const editInput = ref<HTMLInputElement | null>(null)

function startEdit(ms: MilestoneItem) {
  editingId.value = ms.id
  editText.value = ms.text
  nextTick(() => editInput.value?.focus())
}

async function saveEdit(ms: MilestoneItem) {
  if (editingId.value !== ms.id) return
  const text = editText.value.trim()
  if (text && text !== ms.text) {
    await store.updateMilestoneText(ms.id, text)
    emit("edit-saved")
  }
  editingId.value = null
}

function cancelEdit() {
  editingId.value = null
}

// --- Delete ---
async function remove(ms: MilestoneItem) {
  await store.deleteMilestone(ms.id)
  emit("deleted")
}

// --- Add ---
const adding = ref(false)
const addText = ref("")
const addInput = ref<HTMLInputElement | null>(null)

function startAdd() {
  adding.value = true
  addText.value = ""
  nextTick(() => addInput.value?.focus())
}

async function confirmAdd() {
  const text = addText.value.trim()
  if (text) {
    await store.addMilestone(props.monthId, text)
    emit("added")
  }
  adding.value = false
  addText.value = ""
}

function cancelAdd() {
  adding.value = false
  addText.value = ""
}
</script>
