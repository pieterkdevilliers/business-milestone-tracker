<template>
  <Transition name="fade">
    <div
      v-if="visible"
      class="fixed bottom-4 right-4 bg-slate-800 text-white text-sm px-4 py-2 rounded-lg shadow-lg z-50"
    >
      {{ message }}
    </div>
  </Transition>
</template>

<script setup lang="ts">
const props = withDefaults(defineProps<{ message?: string }>(), {
  message: "Saved",
})

const visible = ref(false)
let timer: ReturnType<typeof setTimeout> | null = null

function show() {
  visible.value = true
  if (timer) clearTimeout(timer)
  timer = setTimeout(() => {
    visible.value = false
  }, 2000)
}

defineExpose({ show })
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
