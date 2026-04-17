import { defineStore } from "pinia"
import type {
  MasterMilestone,
  MilestoneItem,
  MonthDetail,
  MonthMetric,
  MonthNote,
  QuarterDetail,
  QuarterMetric,
  QuarterNote,
} from "~/types/tracker"

export const useTrackerStore = defineStore("tracker", () => {
  const quarters = ref<QuarterDetail[]>([])
  const masterMilestones = ref<MasterMilestone[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const months = computed<MonthDetail[]>(() =>
    quarters.value.flatMap((q) => q.months)
  )

  const totalMilestones = computed(() =>
    months.value.reduce((sum, m) => sum + m.milestones.length, 0)
  )

  const completedMilestones = computed(() =>
    months.value.reduce(
      (sum, m) => sum + m.milestones.filter((ms) => ms.completed).length,
      0
    )
  )

  function getQuarterColour(quarterNumber: number): string {
    const map: Record<number, string> = {
      1: "q1",
      2: "q2",
      3: "q3",
      4: "q4",
      5: "q5",
      6: "q6",
      7: "q7",
      8: "q8",
    }
    return map[quarterNumber] ?? "q1"
  }

  async function fetchAll() {
    if (quarters.value.length > 0) return
    isLoading.value = true
    error.value = null
    try {
      const api = useApi()
      const [quartersData, milestonesData] = await Promise.all([
        api.get<QuarterDetail[]>("/tracker/quarters"),
        api.get<MasterMilestone[]>("/tracker/master-milestones"),
      ])
      quarters.value = quartersData
      masterMilestones.value = milestonesData
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : "Failed to load data"
    } finally {
      isLoading.value = false
    }
  }

  async function toggleMilestone(milestoneId: number, completed: boolean) {
    const api = useApi()
    const updated = await api.patch<MilestoneItem>(
      `/tracker/milestones/${milestoneId}`,
      { completed }
    )
    for (const q of quarters.value) {
      for (const m of q.months) {
        const idx = m.milestones.findIndex((ms) => ms.id === milestoneId)
        if (idx >= 0) {
          m.milestones[idx] = updated
          return
        }
      }
    }
  }

  async function updateMonthMetric(metricId: number, actual: string | null) {
    const api = useApi()
    const updated = await api.patch<MonthMetric>(
      `/tracker/month-metrics/${metricId}`,
      { actual }
    )
    for (const q of quarters.value) {
      for (const m of q.months) {
        const idx = m.metrics.findIndex((mt) => mt.id === metricId)
        if (idx >= 0) {
          m.metrics[idx] = updated
          return
        }
      }
    }
  }

  async function updateMonthNote(monthId: number, content: string) {
    const api = useApi()
    const updated = await api.patch<MonthNote>(
      `/tracker/month-notes/${monthId}`,
      { content }
    )
    for (const q of quarters.value) {
      const m = q.months.find((m) => m.id === monthId)
      if (m) {
        m.note = updated
        return
      }
    }
  }

  async function updateQuarterMetric(metricId: number, actual: string | null) {
    const api = useApi()
    const updated = await api.patch<QuarterMetric>(
      `/tracker/quarter-metrics/${metricId}`,
      { actual }
    )
    for (const q of quarters.value) {
      const idx = q.metrics.findIndex((mt) => mt.id === metricId)
      if (idx >= 0) {
        q.metrics[idx] = updated
        return
      }
    }
  }

  async function updateQuarterNote(quarterId: number, content: string) {
    const api = useApi()
    const updated = await api.patch<QuarterNote>(
      `/tracker/quarter-notes/${quarterId}`,
      { content }
    )
    const q = quarters.value.find((q) => q.id === quarterId)
    if (q) q.note = updated
  }

  async function updateMasterMilestone(
    milestoneId: number,
    payload: { completed?: boolean; actual_date?: string; notes?: string }
  ) {
    const api = useApi()
    const updated = await api.patch<MasterMilestone>(
      `/tracker/master-milestones/${milestoneId}`,
      payload
    )
    const idx = masterMilestones.value.findIndex((m) => m.id === milestoneId)
    if (idx >= 0) masterMilestones.value[idx] = updated
  }

  return {
    quarters,
    masterMilestones,
    months,
    isLoading,
    error,
    totalMilestones,
    completedMilestones,
    getQuarterColour,
    fetchAll,
    toggleMilestone,
    updateMonthMetric,
    updateMonthNote,
    updateQuarterMetric,
    updateQuarterNote,
    updateMasterMilestone,
  }
})
