export interface MilestoneItem {
  id: number
  month_id: number
  text: string
  completed: boolean
  sort_order: number
}

export interface MonthMetric {
  id: number
  month_id: number
  label: string
  target: string
  actual: string | null
  sort_order: number
}

export interface MonthNote {
  id: number
  month_id: number
  content: string
  updated_at: string
}

export interface MonthDetail {
  id: number
  quarter_id: number
  month_name: string
  year: number
  theme: string
  sort_order: number
  milestones: MilestoneItem[]
  metrics: MonthMetric[]
  note: MonthNote | null
}

export interface QuarterMetric {
  id: number
  quarter_id: number
  label: string
  target: string
  actual: string | null
  sort_order: number
}

export interface QuarterNote {
  id: number
  quarter_id: number
  content: string
  updated_at: string
}

export interface QuarterDetail {
  id: number
  quarter_number: number
  label: string
  theme: string
  year: number
  months: MonthDetail[]
  metrics: QuarterMetric[]
  note: QuarterNote | null
}

export interface MasterMilestone {
  id: number
  target_date: string
  text: string
  completed: boolean
  actual_date: string | null
  notes: string | null
  sort_order: number
  colour_group: string
}
