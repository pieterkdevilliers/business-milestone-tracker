from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tracker import (
    MasterMilestone,
    Milestone,
    Month,
    MonthMetric,
    Quarter,
    QuarterMetric,
)

QUARTERS = [
    {
        "quarter_number": 1,
        "label": "Q1 — April, May, June 2026",
        "theme": "Launch and first proof points",
        "year": 1,
        "metrics": [
            {"label": "Coaching clients (end Q1)", "target": "2", "sort_order": 1},
            {"label": "WRP workshops (Q1 total)", "target": "1", "sort_order": 2},
            {"label": "Audit calls (Q1 total)", "target": "5–7", "sort_order": 3},
            {"label": "Q1 revenue total", "target": "~£5,000–6,000", "sort_order": 4},
            {"label": "Outreach messages (Q1 total)", "target": "360–480", "sort_order": 5},
        ],
    },
    {
        "quarter_number": 2,
        "label": "Q2 — July, August, September 2026",
        "theme": "Scaling and NEC",
        "year": 1,
        "metrics": [
            {"label": "Coaching clients (end Q2)", "target": "5", "sort_order": 1},
            {"label": "WRP workshops (Q2 total)", "target": "2", "sort_order": 2},
            {"label": "Audit calls (Q2 total)", "target": "24–27", "sort_order": 3},
            {"label": "Q2 revenue total", "target": "~£10,500–12,500", "sort_order": 4},
            {"label": "NEC opt-ins captured", "target": "150–300", "sort_order": 5},
            {"label": "Case studies documented", "target": "2", "sort_order": 6},
        ],
    },
    {
        "quarter_number": 3,
        "label": "Q3 — October, November, December 2026",
        "theme": "NEC pipeline and year-end",
        "year": 1,
        "metrics": [
            {"label": "Coaching clients (end Q3)", "target": "8", "sort_order": 1},
            {"label": "WRP workshops (Q3 total)", "target": "5", "sort_order": 2},
            {"label": "Audit calls (Q3 total)", "target": "33–40", "sort_order": 3},
            {"label": "Q3 revenue total", "target": "~£17,500–20,500", "sort_order": 4},
            {"label": "NEC Audit calls booked", "target": "15–20", "sort_order": 5},
            {"label": "Case studies published", "target": "2–3", "sort_order": 6},
        ],
    },
    {
        "quarter_number": 4,
        "label": "Q4 — January, February, March 2027",
        "theme": "Year-one close",
        "year": 1,
        "metrics": [
            {"label": "Coaching clients (end Y1)", "target": "10–12", "sort_order": 1},
            {"label": "WRP workshops (year total)", "target": "12+", "sort_order": 2},
            {"label": "Audit calls (year total)", "target": "~100", "sort_order": 3},
            {"label": "Year-one revenue", "target": "~£80,000–103,000", "sort_order": 4},
            {"label": "Case studies", "target": "5+", "sort_order": 5},
            {"label": "EC certification", "target": "Complete", "sort_order": 6},
        ],
    },
    {
        "quarter_number": 5,
        "label": "Q5 — April, May, June 2027",
        "theme": "Price transition",
        "year": 2,
        "metrics": [
            {"label": "Coaching clients (end Q5)", "target": "12 at £850", "sort_order": 1},
            {"label": "WRP workshops (Q5 total)", "target": "9", "sort_order": 2},
            {"label": "Audit calls (Q5 total)", "target": "36–39", "sort_order": 3},
            {"label": "Q5 revenue total", "target": "~£56,000–65,000", "sort_order": 4},
            {"label": "Monthly revenue run rate", "target": "£20,000–23,000", "sort_order": 5},
            {"label": "Referral % of new clients", "target": "30–40%", "sort_order": 6},
        ],
    },
    {
        "quarter_number": 6,
        "label": "Q6 — July, August, September 2027",
        "theme": "Full model optimising",
        "year": 2,
        "metrics": [
            {"label": "Coaching clients (end Q6)", "target": "12 at £850+", "sort_order": 1},
            {"label": "WRP workshops (Q6 total)", "target": "9", "sort_order": 2},
            {"label": "Audit calls (Q6 total)", "target": "36–39", "sort_order": 3},
            {"label": "Q6 revenue total", "target": "~£66,000–75,000", "sort_order": 4},
            {"label": "Annual run rate", "target": "£270,000–300,000", "sort_order": 5},
            {"label": "Referral % of new clients", "target": "40–50%", "sort_order": 6},
        ],
    },
    {
        "quarter_number": 7,
        "label": "Q7 — October, November, December 2027",
        "theme": "Approaching the ceiling",
        "year": 2,
        "metrics": [
            {"label": "Coaching clients (end Q7)", "target": "12 at £850–950", "sort_order": 1},
            {"label": "WRP workshops (Q7 total)", "target": "9", "sort_order": 2},
            {"label": "Audit calls (Q7 total)", "target": "36–39", "sort_order": 3},
            {"label": "Q7 revenue total", "target": "~£69,000–78,000", "sort_order": 4},
            {"label": "Annual revenue to date", "target": "~£260,000–280,000", "sort_order": 5},
            {"label": "Year 3 direction", "target": "Set", "sort_order": 6},
        ],
    },
    {
        "quarter_number": 8,
        "label": "Q8 — January, February, March 2028",
        "theme": "Year-two close",
        "year": 2,
        "metrics": [
            {"label": "Coaching clients (end Y2)", "target": "12 at £850–950", "sort_order": 1},
            {"label": "WRP workshops (year total)", "target": "36", "sort_order": 2},
            {"label": "Audit calls (year total)", "target": "~156", "sort_order": 3},
            {"label": "Year-two revenue", "target": "~£295,000–310,000", "sort_order": 4},
            {"label": "Referral % of new clients", "target": "50%+", "sort_order": 5},
            {"label": "Year-three direction", "target": "Confirmed and active", "sort_order": 6},
        ],
    },
]

MONTHS = [
    # ── Q1 ──────────────────────────────────────────────────────────────────
    {
        "quarter_number": 1,
        "month_name": "April",
        "year": 2026,
        "theme": "Foundation month — get the engine running",
        "sort_order": 1,
        "milestones": [
            {"text": "First LinkedIn outreach batch sent (30–40 messages)", "sort_order": 1},
            {"text": "VA onboarded and running outreach workflow", "sort_order": 2},
            {"text": "EC coaching certification — first conversation", "sort_order": 3},
            {"text": "First inbound from content or outreach (even just a reply)", "sort_order": 4},
            {"text": "CRM and email sequences confirmed working end-to-end", "sort_order": 5},
            {"text": "Scorecard and report tools stress-tested", "sort_order": 6},
        ],
        "metrics": [
            {"label": "Coaching clients", "target": "0", "sort_order": 1},
            {"label": "WRP workshops", "target": "0", "sort_order": 2},
            {"label": "Audit calls", "target": "0–1", "sort_order": 3},
            {"label": "Monthly revenue", "target": "£0–249", "sort_order": 4},
            {"label": "Outreach sent", "target": "120–160", "sort_order": 5},
            {"label": "Reports generated", "target": "5–10", "sort_order": 6},
        ],
    },
    {
        "quarter_number": 1,
        "month_name": "May",
        "year": 2026,
        "theme": "First revenue — prove the funnel works",
        "sort_order": 2,
        "milestones": [
            {"text": "First Audit Call booked from cold outreach", "sort_order": 1},
            {"text": "First Audit Call completed and report delivered", "sort_order": 2},
            {"text": "First coaching client signed (any price)", "sort_order": 3},
            {"text": "LinkedIn content cadence established — 3 posts/week", "sort_order": 4},
            {"text": "First Blindspot Report sent to warm prospect", "sort_order": 5},
            {"text": "VA running outreach independently — Pieter reviewing weekly", "sort_order": 6},
        ],
        "metrics": [
            {"label": "Coaching clients", "target": "1", "sort_order": 1},
            {"label": "WRP workshops", "target": "0", "sort_order": 2},
            {"label": "Audit calls", "target": "2–3", "sort_order": 3},
            {"label": "Monthly revenue", "target": "£750–1,200", "sort_order": 4},
            {"label": "Outreach sent", "target": "120–160", "sort_order": 5},
            {"label": "Reports generated", "target": "8–12", "sort_order": 6},
        ],
    },
    {
        "quarter_number": 1,
        "month_name": "June",
        "year": 2026,
        "theme": "Momentum — first workshop, second client",
        "sort_order": 3,
        "milestones": [
            {"text": "Second coaching client signed", "sort_order": 1},
            {"text": "First WRP workshop delivered", "sort_order": 2},
            {"text": "First case study notes documented", "sort_order": 3},
            {"text": "EC certification — formal application submitted", "sort_order": 4},
            {"text": "Quarterly review completed (Q1 actual vs target)", "sort_order": 5},
            {"text": "NEC exhibition — initial research and consideration", "sort_order": 6},
        ],
        "metrics": [
            {"label": "Coaching clients", "target": "2", "sort_order": 1},
            {"label": "WRP workshops", "target": "1", "sort_order": 2},
            {"label": "Audit calls", "target": "2–3", "sort_order": 3},
            {"label": "Monthly revenue", "target": "£2,000–2,800", "sort_order": 4},
            {"label": "Outreach sent", "target": "120–160", "sort_order": 5},
            {"label": "Reports generated", "target": "8–12", "sort_order": 6},
        ],
    },
    # ── Q2 ──────────────────────────────────────────────────────────────────
    {
        "quarter_number": 2,
        "month_name": "July",
        "year": 2026,
        "theme": "Decision month — commit to NEC or defer",
        "sort_order": 4,
        "milestones": [
            {"text": "NEC exhibition decision made (requires 2+ case studies)", "sort_order": 1},
            {"text": "If committing: stand booked, build plan confirmed", "sort_order": 2},
            {"text": "Third coaching client signed", "sort_order": 3},
            {"text": "Outreach data review — 90-day analysis of what's converting", "sort_order": 4},
            {"text": "Sales Navigator search refined based on Q1 data", "sort_order": 5},
            {"text": "Audit calls averaging 2/week", "sort_order": 6},
        ],
        "metrics": [
            {"label": "Coaching clients", "target": "3", "sort_order": 1},
            {"label": "WRP workshops", "target": "2 (cumulative)", "sort_order": 2},
            {"label": "Audit calls", "target": "8–9", "sort_order": 3},
            {"label": "Monthly revenue", "target": "£3,000–3,500", "sort_order": 4},
            {"label": "Outreach sent", "target": "120–160", "sort_order": 5},
            {"label": "Reports generated", "target": "10–15", "sort_order": 6},
        ],
    },
    {
        "quarter_number": 2,
        "month_name": "August",
        "year": 2026,
        "theme": "Pre-exhibition build — everything ready before September",
        "sort_order": 5,
        "milestones": [
            {"text": "Entry page built, tested, and live", "sort_order": 1},
            {"text": "QR code tested on multiple devices from 1m and 2m", "sort_order": 2},
            {"text": "Flyers designed, printed (500 minimum), delivered", "sort_order": 3},
            {"text": "Stand graphics ordered", "sort_order": 4},
            {"text": "All NEC email sequences built and tested end-to-end", "sort_order": 5},
            {"text": "Fourth coaching client signed", "sort_order": 6},
            {"text": "Paper entry card process documented for VA", "sort_order": 7},
        ],
        "metrics": [
            {"label": "Coaching clients", "target": "4", "sort_order": 1},
            {"label": "WRP workshops", "target": "2 (cumulative)", "sort_order": 2},
            {"label": "Audit calls", "target": "8–9", "sort_order": 3},
            {"label": "Monthly revenue", "target": "£3,500–4,000", "sort_order": 4},
            {"label": "Outreach sent", "target": "120–160", "sort_order": 5},
            {"label": "NEC prep", "target": "100% complete", "sort_order": 6},
        ],
    },
    {
        "quarter_number": 2,
        "month_name": "September",
        "year": 2026,
        "theme": "NEC exhibition — 7–8 September",
        "sort_order": 6,
        "milestones": [
            {"text": "NEC stand delivered — day one and day two", "sort_order": 1},
            {"text": "Day-one reports delivered before day two begins", "sort_order": 2},
            {"text": "Winner announced within 3 days of event", "sort_order": 3},
            {"text": "NEC follow-up sequence active for all opt-ins", "sort_order": 4},
            {"text": "Fifth coaching client signed", "sort_order": 5},
            {"text": "50% voucher deadline set — 90 days from 8 September", "sort_order": 6},
        ],
        "metrics": [
            {"label": "Coaching clients", "target": "5", "sort_order": 1},
            {"label": "WRP workshops", "target": "3 (cumulative)", "sort_order": 2},
            {"label": "NEC opt-ins", "target": "150–300 target", "sort_order": 3},
            {"label": "Monthly revenue", "target": "£4,000–5,000", "sort_order": 4},
            {"label": "Audit calls", "target": "8–9", "sort_order": 5},
            {"label": "Reports generated", "target": "150–300 (NEC)", "sort_order": 6},
        ],
    },
    # ── Q3 ──────────────────────────────────────────────────────────────────
    {
        "quarter_number": 3,
        "month_name": "October",
        "year": 2026,
        "theme": "NEC follow-up — convert the list",
        "sort_order": 7,
        "milestones": [
            {"text": "NEC 50% vouchers push — deadline awareness campaign", "sort_order": 1},
            {"text": "Target 10–15 Audit Calls from NEC list this month", "sort_order": 2},
            {"text": "Sixth coaching client signed", "sort_order": 3},
            {
                "text": "First coaching client approaching 6-month mark — renewal conversation",
                "sort_order": 4,
            },
            {"text": "EC certification — progress checkpoint", "sort_order": 5},
            {"text": "First proper case study written and published", "sort_order": 6},
        ],
        "metrics": [
            {"label": "Coaching clients", "target": "6", "sort_order": 1},
            {"label": "WRP workshops", "target": "4–5 (cumulative)", "sort_order": 2},
            {"label": "Audit calls (inc NEC)", "target": "15–18", "sort_order": 3},
            {"label": "Monthly revenue", "target": "£5,500–6,500", "sort_order": 4},
            {"label": "NEC Audit calls booked", "target": "10–15", "sort_order": 5},
            {"label": "Outreach sent", "target": "120–160", "sort_order": 6},
        ],
    },
    {
        "quarter_number": 3,
        "month_name": "November",
        "year": 2026,
        "theme": "Building toward year-end",
        "sort_order": 8,
        "milestones": [
            {"text": "Seventh or eighth coaching client signed", "sort_order": 1},
            {"text": "Two WRP workshops delivered this month", "sort_order": 2},
            {"text": "First client hitting measurable, documentable results", "sort_order": 3},
            {"text": "NEC list — secondary follow-up to unconverted leads", "sort_order": 4},
            {"text": "Pricing review — are current prices holding without resistance?", "sort_order": 5},
            {"text": "Begin planning January content push", "sort_order": 6},
        ],
        "metrics": [
            {"label": "Coaching clients", "target": "7–8", "sort_order": 1},
            {"label": "WRP workshops", "target": "6–7 (cumulative)", "sort_order": 2},
            {"label": "Audit calls", "target": "10–12", "sort_order": 3},
            {"label": "Monthly revenue", "target": "£6,000–7,000", "sort_order": 4},
            {"label": "Outreach sent", "target": "120–160", "sort_order": 5},
            {"label": "Reports generated", "target": "10–15", "sort_order": 6},
        ],
    },
    {
        "quarter_number": 3,
        "month_name": "December",
        "year": 2026,
        "theme": "Consolidation and year-end review",
        "sort_order": 9,
        "milestones": [
            {"text": "Eight coaching clients active going into January", "sort_order": 1},
            {"text": "Year-end review with each coaching client completed", "sort_order": 2},
            {"text": "Annual financial review — actual vs target", "sort_order": 3},
            {"text": "Personal review — what worked, what to change", "sort_order": 4},
            {"text": "Year-two plan drafted — pricing, client cap, working pattern", "sort_order": 5},
            {"text": "January pipeline confirmed — calls booked ahead", "sort_order": 6},
        ],
        "metrics": [
            {"label": "Coaching clients", "target": "8", "sort_order": 1},
            {"label": "WRP workshops", "target": "8 (cumulative)", "sort_order": 2},
            {"label": "Audit calls", "target": "8–10", "sort_order": 3},
            {"label": "Monthly revenue", "target": "£6,000–7,000", "sort_order": 4},
            {"label": "Outreach sent", "target": "80–100 (shorter month)", "sort_order": 5},
            {"label": "Annual revenue to date", "target": "£35,000–40,000", "sort_order": 6},
        ],
    },
    # ── Q4 ──────────────────────────────────────────────────────────────────
    {
        "quarter_number": 4,
        "month_name": "January",
        "year": 2027,
        "theme": "New year momentum — strong month",
        "sort_order": 10,
        "milestones": [
            {"text": "3 Audit Calls per week through January", "sort_order": 1},
            {"text": "Ninth coaching client signed", "sort_order": 2},
            {"text": "Audit Call price raised to £350 for all new clients", "sort_order": 3},
            {"text": "EC certification — target completion this quarter", "sort_order": 4},
            {"text": "Year-two pricing strategy confirmed", "sort_order": 5},
            {"text": "January content push — problem-first angles for new year", "sort_order": 6},
        ],
        "metrics": [
            {"label": "Coaching clients", "target": "9", "sort_order": 1},
            {"label": "WRP workshops", "target": "2 this month", "sort_order": 2},
            {"label": "Audit calls", "target": "12–13", "sort_order": 3},
            {"label": "Monthly revenue", "target": "£7,500–8,500", "sort_order": 4},
            {"label": "Outreach sent", "target": "120–160", "sort_order": 5},
            {"label": "Audit call price", "target": "£350 (new)", "sort_order": 6},
        ],
    },
    {
        "quarter_number": 4,
        "month_name": "February",
        "year": 2027,
        "theme": "Refining — test higher prices",
        "sort_order": 11,
        "milestones": [
            {"text": "Tenth coaching client signed", "sort_order": 1},
            {"text": "Three WRP workshops delivered", "sort_order": 2},
            {"text": "First WRP at £3,000 (testing toward £3,500)", "sort_order": 3},
            {"text": "Best-converting outreach sector identified — double down", "sort_order": 4},
            {"text": "First proper case study with named results published", "sort_order": 5},
            {"text": "EC certification — completed or final stage", "sort_order": 6},
        ],
        "metrics": [
            {"label": "Coaching clients", "target": "10", "sort_order": 1},
            {"label": "WRP workshops", "target": "3 this month", "sort_order": 2},
            {"label": "Audit calls", "target": "12–13", "sort_order": 3},
            {"label": "Monthly revenue", "target": "£8,500–9,500", "sort_order": 4},
            {"label": "WRP price tested", "target": "£3,000", "sort_order": 5},
            {"label": "Outreach sent", "target": "100–130", "sort_order": 6},
        ],
    },
    {
        "quarter_number": 4,
        "month_name": "March",
        "year": 2027,
        "theme": "Year-one close — confirm year-two plan",
        "sort_order": 12,
        "milestones": [
            {"text": "10–12 coaching clients active", "sort_order": 1},
            {"text": "WRP workshops at 2–3/month consistently", "sort_order": 2},
            {"text": "Full year-one financial review completed", "sort_order": 3},
            {
                "text": "Year-two pricing confirmed (coaching £850, WRP £3,500, Audit £350)",
                "sort_order": 4,
            },
            {"text": "Year-two client cap confirmed (12 coaching clients)", "sort_order": 5},
            {"text": "5+ case studies documented with results", "sort_order": 6},
        ],
        "metrics": [
            {"label": "Coaching clients", "target": "10–12", "sort_order": 1},
            {"label": "WRP workshops", "target": "2–3 this month", "sort_order": 2},
            {"label": "Audit calls", "target": "12–13", "sort_order": 3},
            {"label": "Monthly revenue", "target": "£9,000–11,000", "sort_order": 4},
            {"label": "Year-one total", "target": "~£80,000–103,000", "sort_order": 5},
            {"label": "Case studies", "target": "5+", "sort_order": 6},
        ],
    },
    # ── Q5 ──────────────────────────────────────────────────────────────────
    {
        "quarter_number": 5,
        "month_name": "April",
        "year": 2027,
        "theme": "New pricing live — year two begins",
        "sort_order": 13,
        "milestones": [
            {
                "text": "All new pricing active: coaching £850, WRP £3,500, Audit £350",
                "sort_order": 1,
            },
            {"text": "Existing clients — phased price increase conversations", "sort_order": 2},
            {"text": "12 coaching clients target (mix of old and new pricing)", "sort_order": 3},
            {"text": "First coaching client at 12-month renewal", "sort_order": 4},
            {"text": "NEC 2026 list — 6-month reactivation campaign launched", "sort_order": 5},
            {"text": "Year-two working pattern bedded in", "sort_order": 6},
        ],
        "metrics": [
            {"label": "Coaching clients", "target": "11–12", "sort_order": 1},
            {"label": "WRP workshops", "target": "3", "sort_order": 2},
            {"label": "Audit calls", "target": "12–13", "sort_order": 3},
            {"label": "Monthly revenue", "target": "£17,000–20,000", "sort_order": 4},
            {"label": "New clients at £850", "target": "2–3", "sort_order": 5},
            {"label": "Outreach sent", "target": "120–160", "sort_order": 6},
        ],
    },
    {
        "quarter_number": 5,
        "month_name": "May",
        "year": 2027,
        "theme": "Full year-two model running",
        "sort_order": 14,
        "milestones": [
            {"text": "12 coaching clients all at new pricing", "sort_order": 1},
            {"text": "Three WRP workshops at £3,500", "sort_order": 2},
            {"text": "First month at full year-two revenue run rate", "sort_order": 3},
            {"text": "Review: are clients accepting new prices without pushback?", "sort_order": 4},
            {"text": "NEC 2026 reactivation — Audit Calls being booked", "sort_order": 5},
            {"text": "Consider NEC 2027 exhibition", "sort_order": 6},
        ],
        "metrics": [
            {"label": "Coaching clients", "target": "12 at £850", "sort_order": 1},
            {"label": "WRP workshops", "target": "3 at £3,500", "sort_order": 2},
            {"label": "Audit calls", "target": "12–13 at £350", "sort_order": 3},
            {"label": "Monthly revenue", "target": "£19,000–22,000", "sort_order": 4},
            {"label": "Outreach sent", "target": "120–160", "sort_order": 5},
            {"label": "Referrals as % of new", "target": "20–30%", "sort_order": 6},
        ],
    },
    {
        "quarter_number": 5,
        "month_name": "June",
        "year": 2027,
        "theme": "Quarterly review — is the model sustainable?",
        "sort_order": 15,
        "milestones": [
            {"text": "Quarterly review: workload sustainable and enjoyable?", "sort_order": 1},
            {"text": "Are the right clients in the programme?", "sort_order": 2},
            {
                "text": "WRP pipeline: is 3/month filling consistently from Audit Calls?",
                "sort_order": 3,
            },
            {"text": "One-week-UK / three-weeks-remote — working practically?", "sort_order": 4},
            {"text": "Content review: what has performed best over 14 months?", "sort_order": 5},
            {"text": "Year-three thinking: stay here, scale, or evolve?", "sort_order": 6},
        ],
        "metrics": [
            {"label": "Coaching clients", "target": "12 at £850", "sort_order": 1},
            {"label": "WRP workshops", "target": "3 at £3,500", "sort_order": 2},
            {"label": "Audit calls", "target": "12–13", "sort_order": 3},
            {"label": "Monthly revenue", "target": "£20,000–23,000", "sort_order": 4},
            {"label": "Outreach sent", "target": "80–120", "sort_order": 5},
            {"label": "Referrals as % of new", "target": "30–40%", "sort_order": 6},
        ],
    },
    # ── Q6 ──────────────────────────────────────────────────────────────────
    {
        "quarter_number": 6,
        "month_name": "July",
        "year": 2027,
        "theme": "Annual run rate tracking toward £280,000+",
        "sort_order": 16,
        "milestones": [
            {"text": "Annual revenue run rate confirmed at £280,000+", "sort_order": 1},
            {
                "text": "Client quality review — all 12 coaching clients getting full value?",
                "sort_order": 2,
            },
            {
                "text": "Waiting list emerging? If so, consider raising coaching to £950",
                "sort_order": 3,
            },
            {
                "text": "NEC 2027 decision — exhibit again with stronger case studies?",
                "sort_order": 4,
            },
            {"text": "Consider second coach under Blindspot Works brand", "sort_order": 5},
            {"text": "Outreach review — is referral now primary source?", "sort_order": 6},
        ],
        "metrics": [
            {"label": "Coaching clients", "target": "12 at £850", "sort_order": 1},
            {"label": "WRP workshops", "target": "3", "sort_order": 2},
            {"label": "Audit calls", "target": "12–13", "sort_order": 3},
            {"label": "Monthly revenue", "target": "£22,000–25,000", "sort_order": 4},
            {"label": "Waiting list", "target": "0–2", "sort_order": 5},
            {"label": "Referrals as % of new", "target": "40%+", "sort_order": 6},
        ],
    },
    {
        "quarter_number": 6,
        "month_name": "August",
        "year": 2027,
        "theme": "Mid-year review — every client, every metric",
        "sort_order": 17,
        "milestones": [
            {"text": "Mid-year review with every coaching client", "sort_order": 1},
            {"text": "Progress, results, renewal likelihood assessed for all 12", "sort_order": 2},
            {"text": "VA review — is outreach still needed at this volume?", "sort_order": 3},
            {"text": "Content review — best performing topics over 16 months", "sort_order": 4},
            {"text": "Best sector identified — consider a niche specialisation", "sort_order": 5},
            {"text": "Begin thinking about Barefoot Business 2.0 or new book", "sort_order": 6},
        ],
        "metrics": [
            {"label": "Coaching clients", "target": "12 at £850", "sort_order": 1},
            {"label": "WRP workshops", "target": "3", "sort_order": 2},
            {"label": "Audit calls", "target": "12–13", "sort_order": 3},
            {"label": "Monthly revenue", "target": "£22,000–25,000", "sort_order": 4},
            {"label": "Renewals confirmed", "target": "8+ of 12", "sort_order": 5},
            {"label": "Outreach sent", "target": "60–100", "sort_order": 6},
        ],
    },
    {
        "quarter_number": 6,
        "month_name": "September",
        "year": 2027,
        "theme": "One year since NEC — review the full pipeline value",
        "sort_order": 18,
        "milestones": [
            {
                "text": "NEC 2026 one-year anniversary — total pipeline value calculated",
                "sort_order": 1,
            },
            {
                "text": "All 12 coaching clients renewing or actively being replaced",
                "sort_order": 2,
            },
            {"text": "Second coach — first serious conversation or decision", "sort_order": 3},
            {
                "text": "Methodology documentation begun — for licensing or training",
                "sort_order": 4,
            },
            {
                "text": "EC community — referral relationships generating consistent pipeline?",
                "sort_order": 5,
            },
            {"text": "Consider NEC 2027 if not already committed", "sort_order": 6},
        ],
        "metrics": [
            {"label": "Coaching clients", "target": "12 at £850", "sort_order": 1},
            {"label": "WRP workshops", "target": "3", "sort_order": 2},
            {"label": "Audit calls", "target": "12–13", "sort_order": 3},
            {"label": "Monthly revenue", "target": "£22,000–25,000", "sort_order": 4},
            {"label": "NEC 2026 total value", "target": "Calculate and document", "sort_order": 5},
            {"label": "Referrals as % of new", "target": "40–50%", "sort_order": 6},
        ],
    },
    # ── Q7 ──────────────────────────────────────────────────────────────────
    {
        "quarter_number": 7,
        "month_name": "October",
        "year": 2027,
        "theme": "Decisions about what comes next",
        "sort_order": 19,
        "milestones": [
            {"text": "Annual revenue on track for £275,000+", "sort_order": 1},
            {
                "text": "Raise prices further or license the methodology — decision",
                "sort_order": 2,
            },
            {"text": "Second WRP facilitator — serious conversation", "sort_order": 3},
            {
                "text": "EC community referral relationships — formally measured",
                "sort_order": 4,
            },
            {"text": "Coaching price test: offer one new slot at £950", "sort_order": 5},
            {"text": "Methodology documentation — first draft of framework", "sort_order": 6},
        ],
        "metrics": [
            {"label": "Coaching clients", "target": "12 at £850–950", "sort_order": 1},
            {"label": "WRP workshops", "target": "3", "sort_order": 2},
            {"label": "Audit calls", "target": "12–13", "sort_order": 3},
            {"label": "Monthly revenue", "target": "£23,000–26,000", "sort_order": 4},
            {"label": "WRP price tested", "target": "£3,500 (or £4,000 test)", "sort_order": 5},
            {"label": "Methodology doc", "target": "In progress", "sort_order": 6},
        ],
    },
    {
        "quarter_number": 7,
        "month_name": "November",
        "year": 2027,
        "theme": "Price testing and ceiling planning",
        "sort_order": 20,
        "milestones": [
            {"text": "WRP price test at £4,000 — does it hold?", "sort_order": 1},
            {
                "text": "Coaching: if waiting list exists, raise to £950–1,000",
                "sort_order": 2,
            },
            {
                "text": "Barefoot Business 2.0 or new Blindspot Works book — plan confirmed",
                "sort_order": 3,
            },
            {"text": "Second coach — decision made (yes/no/not yet)", "sort_order": 4},
            {"text": "Year-three plan first draft", "sort_order": 5},
            {"text": "NEC 2028 — early consideration", "sort_order": 6},
        ],
        "metrics": [
            {"label": "Coaching clients", "target": "12 at £850–950", "sort_order": 1},
            {"label": "WRP workshops", "target": "3", "sort_order": 2},
            {"label": "Audit calls", "target": "12–13", "sort_order": 3},
            {"label": "Monthly revenue", "target": "£23,000–26,000", "sort_order": 4},
            {"label": "WRP price", "target": "£4,000 test", "sort_order": 5},
            {"label": "Year 3 direction", "target": "Drafted", "sort_order": 6},
        ],
    },
    {
        "quarter_number": 7,
        "month_name": "December",
        "year": 2027,
        "theme": "Year-two financial review and personal review",
        "sort_order": 21,
        "milestones": [
            {"text": "Year-two financial review — actual vs £300k target", "sort_order": 1},
            {"text": "Full client review — who would refer, who wouldn't", "sort_order": 2},
            {
                "text": "Personal review — is the working pattern enjoyable and sustainable?",
                "sort_order": 3,
            },
            {"text": "Year-three direction set and written down", "sort_order": 4},
            {"text": "January pipeline confirmed ahead of time", "sort_order": 5},
            {"text": "Celebrate the year — this is a significant achievement", "sort_order": 6},
        ],
        "metrics": [
            {"label": "Coaching clients", "target": "12 at £850–950", "sort_order": 1},
            {"label": "WRP workshops", "target": "3", "sort_order": 2},
            {"label": "Audit calls", "target": "12–13", "sort_order": 3},
            {"label": "Monthly revenue", "target": "£23,000–26,000", "sort_order": 4},
            {"label": "Annual revenue to date", "target": "~£260,000–280,000", "sort_order": 5},
            {"label": "Year 3 direction", "target": "Confirmed", "sort_order": 6},
        ],
    },
    # ── Q8 ──────────────────────────────────────────────────────────────────
    {
        "quarter_number": 8,
        "month_name": "January",
        "year": 2028,
        "theme": "Strong month — lean into it",
        "sort_order": 22,
        "milestones": [
            {"text": "3 WRP workshops confirmed for January", "sort_order": 1},
            {"text": "Coaching stable at 12 clients — no disruption to January", "sort_order": 2},
            {"text": "No new discounting — prices are what they are", "sort_order": 3},
            {"text": "Year-three plan reviewed and refined", "sort_order": 4},
            {
                "text": "January content push — biggest ideas, most provocative angles",
                "sort_order": 5,
            },
            {"text": "NEC 2028 — commit or defer decision", "sort_order": 6},
        ],
        "metrics": [
            {"label": "Coaching clients", "target": "12 at £850–950", "sort_order": 1},
            {"label": "WRP workshops", "target": "3", "sort_order": 2},
            {"label": "Audit calls", "target": "12–13", "sort_order": 3},
            {"label": "Monthly revenue", "target": "£24,000–27,000", "sort_order": 4},
            {"label": "Outreach sent", "target": "120–160", "sort_order": 5},
            {"label": "Referrals as % of new", "target": "50%+", "sort_order": 6},
        ],
    },
    {
        "quarter_number": 8,
        "month_name": "February",
        "year": 2028,
        "theme": "Year-three vision — what does the business become?",
        "sort_order": 23,
        "milestones": [
            {
                "text": "Year-three model decided: stay, grow via second coach, or productise",
                "sort_order": 1,
            },
            {
                "text": "Book project — Barefoot Business 2.0 or new title — first chapter",
                "sort_order": 2,
            },
            {"text": "Methodology — ready to license or train others?", "sort_order": 3},
            {
                "text": "All coaching clients at £850+ — no legacy pricing remaining",
                "sort_order": 4,
            },
            {
                "text": "Review: net promoter — who are the strongest advocates?",
                "sort_order": 5,
            },
            {"text": "Identify the 3 best case studies for public use", "sort_order": 6},
        ],
        "metrics": [
            {"label": "Coaching clients", "target": "12 at £850+", "sort_order": 1},
            {"label": "WRP workshops", "target": "3", "sort_order": 2},
            {"label": "Audit calls", "target": "12–13", "sort_order": 3},
            {"label": "Monthly revenue", "target": "£24,000–27,000", "sort_order": 4},
            {"label": "Book project", "target": "Started", "sort_order": 5},
            {"label": "Year 3 model", "target": "Confirmed", "sort_order": 6},
        ],
    },
    {
        "quarter_number": 8,
        "month_name": "March",
        "year": 2028,
        "theme": "Year-two close — two years from start to here",
        "sort_order": 24,
        "milestones": [
            {"text": "Full year-two financial review completed", "sort_order": 1},
            {"text": "Actual vs £300k target reviewed honestly", "sort_order": 2},
            {"text": "Document what the business looks like vs two years ago", "sort_order": 3},
            {
                "text": "Personal review — energy levels, enjoyment, what to protect",
                "sort_order": 4,
            },
            {"text": "Year-three plan confirmed and written down", "sort_order": 5},
            {"text": "Acknowledge the achievement — this is the goal reached", "sort_order": 6},
        ],
        "metrics": [
            {"label": "Coaching clients", "target": "12 at £850–950", "sort_order": 1},
            {"label": "WRP workshops", "target": "3", "sort_order": 2},
            {"label": "Audit calls", "target": "12–13", "sort_order": 3},
            {"label": "Monthly revenue", "target": "£24,000–27,000", "sort_order": 4},
            {"label": "Year-two total", "target": "~£295,000–310,000", "sort_order": 5},
            {"label": "Year 3 plan", "target": "Live", "sort_order": 6},
        ],
    },
]

MASTER_MILESTONES = [
    # Q1 — blue
    {
        "target_date": "May 2026",
        "text": "First Audit Call from cold outreach",
        "colour_group": "q1",
        "sort_order": 1,
    },
    {
        "target_date": "May 2026",
        "text": "First coaching client signed",
        "colour_group": "q1",
        "sort_order": 2,
    },
    {
        "target_date": "June 2026",
        "text": "First WRP workshop delivered",
        "colour_group": "q1",
        "sort_order": 3,
    },
    {
        "target_date": "June 2026",
        "text": "VA running outreach independently",
        "colour_group": "q1",
        "sort_order": 4,
    },
    {
        "target_date": "June 2026",
        "text": "EC coaching certification begun",
        "colour_group": "q1",
        "sort_order": 5,
    },
    # Q2 — green
    {
        "target_date": "July 2026",
        "text": "NEC exhibition committed (if proceeding)",
        "colour_group": "q2",
        "sort_order": 6,
    },
    {
        "target_date": "September 2026",
        "text": "NEC exhibition delivered — 150–300 opt-ins",
        "colour_group": "q2",
        "sort_order": 7,
    },
    {
        "target_date": "September 2026",
        "text": "5 coaching clients active",
        "colour_group": "q2",
        "sort_order": 8,
    },
    # Q3 — amber
    {
        "target_date": "October 2026",
        "text": "First documented case study published",
        "colour_group": "q3",
        "sort_order": 9,
    },
    {
        "target_date": "October 2026",
        "text": "10–15 NEC Audit Calls booked",
        "colour_group": "q3",
        "sort_order": 10,
    },
    {
        "target_date": "December 2026",
        "text": "8 coaching clients active",
        "colour_group": "q3",
        "sort_order": 11,
    },
    # Q4 — dark
    {
        "target_date": "January 2027",
        "text": "Audit Call price raised to £350",
        "colour_group": "q4",
        "sort_order": 12,
    },
    {
        "target_date": "January 2027",
        "text": "EC certification complete",
        "colour_group": "q4",
        "sort_order": 13,
    },
    {
        "target_date": "February 2027",
        "text": "First WRP at £3,000 tested",
        "colour_group": "q4",
        "sort_order": 14,
    },
    {
        "target_date": "March 2027",
        "text": "Year-one revenue ~£100k",
        "colour_group": "q4",
        "sort_order": 15,
    },
    # Q5 — blue
    {
        "target_date": "April 2027",
        "text": "Year-two pricing live (coaching £850, WRP £3,500)",
        "colour_group": "q5",
        "sort_order": 16,
    },
    {
        "target_date": "May 2027",
        "text": "12 coaching clients at new pricing",
        "colour_group": "q5",
        "sort_order": 17,
    },
    {
        "target_date": "May 2027",
        "text": "WRP consistently 3/month at £3,500",
        "colour_group": "q5",
        "sort_order": 18,
    },
    {
        "target_date": "June 2027",
        "text": "Monthly revenue £20,000+",
        "colour_group": "q5",
        "sort_order": 19,
    },
    # Q6 — green
    {
        "target_date": "September 2027",
        "text": "Referrals = 40%+ of new clients",
        "colour_group": "q6",
        "sort_order": 20,
    },
    # Q7 — amber
    {
        "target_date": "October 2027",
        "text": "Coaching price test at £950",
        "colour_group": "q7",
        "sort_order": 21,
    },
    {
        "target_date": "December 2027",
        "text": "Annual revenue £280,000+",
        "colour_group": "q7",
        "sort_order": 22,
    },
    # Q8 — dark
    {
        "target_date": "February 2028",
        "text": "Year-three model confirmed",
        "colour_group": "q8",
        "sort_order": 23,
    },
    {
        "target_date": "March 2028",
        "text": "Year-two revenue ~£300k",
        "colour_group": "q8",
        "sort_order": 24,
    },
]


async def seed_if_empty(db: AsyncSession) -> None:
    result = await db.execute(select(Quarter).limit(1))
    if result.scalar_one_or_none() is not None:
        return

    quarter_map: dict[int, int] = {}

    for q_data in QUARTERS:
        quarter = Quarter(
            quarter_number=q_data["quarter_number"],
            label=q_data["label"],
            theme=q_data["theme"],
            year=q_data["year"],
        )
        db.add(quarter)
        await db.flush()
        quarter_map[q_data["quarter_number"]] = quarter.id

        for m_data in q_data["metrics"]:
            db.add(
                QuarterMetric(
                    quarter_id=quarter.id,
                    label=m_data["label"],
                    target=m_data["target"],
                    sort_order=m_data["sort_order"],
                )
            )

    for m_data in MONTHS:
        quarter_id = quarter_map[m_data["quarter_number"]]
        month = Month(
            quarter_id=quarter_id,
            month_name=m_data["month_name"],
            year=m_data["year"],
            theme=m_data["theme"],
            sort_order=m_data["sort_order"],
        )
        db.add(month)
        await db.flush()

        for ms_data in m_data["milestones"]:
            db.add(
                Milestone(
                    month_id=month.id,
                    text=ms_data["text"],
                    sort_order=ms_data["sort_order"],
                )
            )

        for metric_data in m_data["metrics"]:
            db.add(
                MonthMetric(
                    month_id=month.id,
                    label=metric_data["label"],
                    target=metric_data["target"],
                    sort_order=metric_data["sort_order"],
                )
            )

    for ms_data in MASTER_MILESTONES:
        db.add(
            MasterMilestone(
                target_date=ms_data["target_date"],
                text=ms_data["text"],
                colour_group=ms_data["colour_group"],
                sort_order=ms_data["sort_order"],
            )
        )

    await db.commit()
