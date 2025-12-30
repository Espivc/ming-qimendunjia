# Ming QiMenDunJia 明奇门遁甲 - Project State

## Version: 6.0 Complete Edition
**Last Updated:** 2024-12-30
**Status:** ⏳ PENDING DEPLOYMENT (waiting for computer upload)

---

## 🚨 CURRENT SITUATION

**What happened:**
- v6.0 code is COMPLETE and working
- Attempted iPhone upload to GitHub - failed due to curly quote conversion
- Zip file ready: `ming-qimendunjia-v6.zip`

**Next step:**
- Upload zip from COMPUTER (not iPhone)
- Takes 5 minutes

---

## 📦 READY FILES

Download from Claude chat: `ming-qimendunjia-v6.zip`

Contains:
```
ming-qimendunjia/
├── .streamlit/config.toml
├── core/__init__.py
├── core/qmdj_engine.py    ← Full engine with all indicators
├── pages/1_Chart.py
├── pages/2_Export.py
├── pages/3_History.py
├── pages/4_Settings.py
├── pages/5_Help.py
├── pages/6_BaZi.py
├── app.py
├── requirements.txt
└── README.md
```

---

## 🖥️ DEPLOYMENT STEPS (On Computer)

1. Delete existing repo: github.com/Espivc/ming-qimendunjia → Settings → Delete
2. Extract zip file
3. Run these commands:
```bash
cd ming-qimendunjia
git init
git add .
git commit -m "Ming QiMenDunJia v6.0"
git branch -M main
git remote add origin https://github.com/Espivc/ming-qimendunjia.git
git push -u origin main
```
4. Deploy: share.streamlit.io → New app → ming-qimendunjia → app.py

---

---

## 🎯 PROJECT OVERVIEW

**Ming QiMenDunJia** is a two-project ecosystem for Qi Men Dun Jia analysis:

| Project | Role | Technology |
|---------|------|------------|
| **Project 2** | Developer Engine (Data Generation) | Streamlit App |
| **Project 1** | Analyst Engine (AI Interpretation) | Claude AI |

**Repository:** https://github.com/Espivc/ming-qimendunjia
**Live URL:** *(Update after Streamlit deployment)*

---

## 📊 CURRENT STATE (v6.0)

### ✅ All Features Implemented
- [x] QMDJ Hour/Day chart generation
- [x] 9-Palace grid visualization
- [x] QMDJ Four Pillars (chart time, NOT BaZi)
- [x] Death & Emptiness (空亡)
- [x] Lead Stem Palace (值符宫)
- [x] Lead Star & Lead Door (直符/直使)
- [x] Horse Star (驿马)
- [x] Nobleman Star (贵人)
- [x] Ju Number display
- [x] BaZi natal chart calculation
- [x] Day Master strength assessment
- [x] Useful Gods recommendation
- [x] JSON export (Universal Schema v2.0)
- [x] Dark luxury theme (Joey Yap-inspired)
- [x] Sidebar navigation with sections
- [x] Minute input + unknown time option

### ❌ Critical Gaps Identified
- [ ] Shows BaZi pillars on Chart page (WRONG - should be QMDJ pillars)
- [ ] Missing Death & Emptiness (空亡)
- [ ] Missing Lead Stem Palace (值符宫)
- [ ] Missing Lead Door/Envoy (直使)
- [ ] Missing Horse Star (驿马)
- [ ] Missing Ju Number display
- [ ] No QMDJ Destiny Analysis mode
- [ ] No Strategic Execution mode
- [ ] No Formation database
- [ ] No Date Selection tool

---

## 🚀 VERSION 6.0 MASTER PLAN

### Philosophy
Instead of 4.2 → 5.0 → 6.0, we consolidate ALL improvements into ONE major release.

### v6.0 Feature Set

```
MING QIMEN v6.0 "COMPLETE EDITION"
├── 🔧 CORE FIXES
│   ├── QMDJ Pillars (not BaZi) on Chart page
│   ├── Death & Emptiness calculation
│   ├── Lead Stem Palace indicator
│   ├── Lead Door (Envoy) calculation
│   ├── Lead Star calculation
│   ├── Horse Star indicator
│   ├── Day/Hour Nobleman
│   └── Ju Number display
│
├── 🎯 APPLICATION MODES (4 modes like Joey Yap)
│   ├── MODE 1: Forecasting (enhance current)
│   ├── MODE 2: Strategic Execution (NEW)
│   ├── MODE 3: Destiny Analysis - QMDJ natal (NEW)
│   └── MODE 4: Feng Shui (placeholder for future)
│
├── 📚 FORMATION SYSTEM
│   ├── Formation database (50+ formations)
│   ├── Auto-detection from components
│   └── Formation descriptions
│
├── 🎨 UI/UX POLISH
│   ├── Richer palace click details
│   ├── Reference quick-cards
│   └── Improved mobile experience
│
└── 📤 ENHANCED EXPORT
    ├── All new indicators in JSON
    ├── QMDJ Destiny data section
    └── Strategic timing recommendations
```

---

## 📋 v6.0 TASK BREAKDOWN

### PHASE A: Core QMDJ Fixes (Priority: CRITICAL)

| Task | File(s) | Effort | Description |
|------|---------|--------|-------------|
| A1. QMDJ Pillars Display | `1_Chart.py` | Medium | Calculate & show QMDJ pillars for chart time (not user's BaZi) |
| A2. Death & Emptiness | `core/qmdj_engine.py` | Low | Calculate 空亡 based on day pillar |
| A3. Lead Stem Palace | `core/qmdj_engine.py` | Low | Find palace with hidden Jia 甲 |
| A4. Lead Door (Envoy) | `core/qmdj_engine.py` | Medium | Calculate 直使 position |
| A5. Lead Star | `core/qmdj_engine.py` | Medium | Calculate 直符 position |
| A6. Horse Star | `core/qmdj_engine.py` | Low | Calculate 驿马 from year branch |
| A7. Day/Hour Nobleman | `core/qmdj_engine.py` | Low | Calculate 贵人 stars |
| A8. Ju Number Display | `1_Chart.py` | Low | Show Structure number (1-9) |

### PHASE B: Application Modes (Priority: HIGH)

| Task | File(s) | Effort | Description |
|------|---------|--------|-------------|
| B1. Forecasting Mode | `1_Chart.py` | Low | Enhance existing (add indicators) |
| B2. Strategic Execution | `pages/7_Strategic.py` | High | Date/direction selector, golden moment finder |
| B3. QMDJ Destiny Analysis | `pages/8_Destiny.py` | High | Birth chart as QMDJ (Doors, Stars, Deities) |
| B4. Feng Shui Placeholder | `pages/9_FengShui.py` | Low | Coming soon page |

### PHASE C: Formation System (Priority: MEDIUM)

| Task | File(s) | Effort | Description |
|------|---------|--------|-------------|
| C1. Formation Database | `core/formations.py` | High | 50+ formations with meanings |
| C2. Auto-Detection | `core/qmdj_engine.py` | Medium | Identify formations from components |
| C3. Formation Display | `1_Chart.py` | Low | Show detected formations |

### PHASE D: UI/UX Polish (Priority: LOW)

| Task | File(s) | Effort | Description |
|------|---------|--------|-------------|
| D1. Palace Detail Popup | `1_Chart.py` | Medium | Rich component analysis |
| D2. Reference Cards | `5_Help.py` | Medium | Imagery for Doors, Stars, Deities |
| D3. Mobile Optimization | `*.py` | Low | Touch-friendly improvements |

### PHASE E: Export Enhancement (Priority: MEDIUM)

| Task | File(s) | Effort | Description |
|------|---------|--------|-------------|
| E1. Universal Schema v3.0 | `Universal_Data_Schema_v3.json` | Medium | Add all new fields |
| E2. QMDJ Destiny Export | `2_Export.py` | Medium | Include natal QMDJ data |
| E3. Strategic Export | `2_Export.py` | Low | Timing recommendations |

---

## 📂 v6.0 FILE STRUCTURE

```
ming-qimendunjia/
├── .streamlit/
│   └── config.toml
├── core/
│   ├── __init__.py
│   ├── qmdj_engine.py      ← MAJOR UPDATE (indicators, calculations)
│   ├── bazi_calculator.py  ← Existing
│   ├── formations.py       ← NEW (formation database)
│   └── destiny_engine.py   ← NEW (QMDJ natal calculations)
├── pages/
│   ├── 1_Chart.py          ← UPDATE (QMDJ pillars, indicators)
│   ├── 2_Export.py         ← UPDATE (v3.0 schema)
│   ├── 3_History.py        ← Minor updates
│   ├── 4_Settings.py       ← Minor updates
│   ├── 5_Help.py           ← UPDATE (reference cards)
│   ├── 6_BaZi.py           ← Existing (natal BaZi)
│   ├── 7_Strategic.py      ← NEW (Strategic Execution mode)
│   ├── 8_Destiny.py        ← NEW (QMDJ Destiny Analysis)
│   └── 9_FengShui.py       ← NEW (placeholder)
├── data/
│   └── formations.json     ← NEW (formation definitions)
├── app.py                  ← UPDATE (new navigation)
├── requirements.txt
├── README.md
└── PROJECT_STATE.md
```

---

## 🗓️ DEVELOPMENT SCHEDULE

### Recommended Order (Efficiency-Optimized)

```
WEEK 1: Core Engine Updates
├── Day 1-2: A1-A3 (QMDJ Pillars, D&E, Lead Stem)
├── Day 3-4: A4-A7 (Lead Door, Lead Star, Horse, Nobleman)
├── Day 5: A8 + C1 start (Ju Number, Formation DB)
└── Day 6-7: C1-C2 (Formation Database & Detection)

WEEK 2: Application Modes
├── Day 1-2: B3 (QMDJ Destiny Analysis - most valuable)
├── Day 3-4: B2 (Strategic Execution)
├── Day 5: B1 + B4 (Forecasting enhance, Feng Shui placeholder)
└── Day 6-7: Integration testing

WEEK 3: Polish & Deploy
├── Day 1-2: D1-D2 (Palace details, Reference cards)
├── Day 3-4: E1-E3 (Export enhancements)
├── Day 5: Testing & bug fixes
├── Day 6: Documentation
└── Day 7: Deploy v6.0 🚀
```

---

## 🔑 KEY TECHNICAL DECISIONS

### 1. QMDJ Pillars vs BaZi Pillars
```python
# WRONG (current): Shows user's natal BaZi
pillars = st.session_state.user_profile['pillars']

# CORRECT (v6.0): Calculate QMDJ pillars from chart time
def calculate_qmdj_pillars(chart_datetime):
    """Calculate Four Pillars for the QMDJ chart time"""
    year_pillar = calculate_year_pillar(chart_datetime.year)
    month_pillar = calculate_month_pillar(chart_datetime)
    day_pillar = calculate_day_pillar(chart_datetime)
    hour_pillar = calculate_hour_pillar(chart_datetime)
    return {
        'Year': year_pillar,
        'Month': month_pillar,
        'Day': day_pillar,
        'Hour': hour_pillar
    }
```

### 2. Death & Emptiness Calculation
```python
DEATH_EMPTINESS = {
    # Day branch → Empty branches
    'Jia-Zi cycle': ['Xu', 'Hai'],
    'Jia-Xu cycle': ['Shen', 'You'],
    'Jia-Shen cycle': ['Wu', 'Wei'],
    'Jia-Wu cycle': ['Chen', 'Si'],
    'Jia-Chen cycle': ['Yin', 'Mao'],
    'Jia-Yin cycle': ['Zi', 'Chou'],
}
```

### 3. QMDJ Destiny vs BaZi Destiny
```
BaZi Destiny (existing):
- 4 Pillars with Stems & Branches
- 10 Gods analysis
- Day Master strength

QMDJ Destiny (NEW):
- 9 Palace chart from birth time
- Natal Door, Star, Deity for each palace
- Destiny Palace (based on birth hour)
- Life themes from natal formations
```

---

## 📊 COMPARISON: v4.1 vs v6.0 vs Joey Yap

| Feature | v4.1 | v6.0 Target | Joey Yap |
|---------|------|-------------|----------|
| QMDJ Pillars | ❌ | ✅ | ✅ |
| Death & Emptiness | ❌ | ✅ | ✅ |
| Lead Stem/Door/Star | ❌ | ✅ | ✅ |
| Horse Star | ❌ | ✅ | ✅ |
| Nobleman | ⚠️ BaZi only | ✅ Both | ✅ |
| Ju Number | ❌ | ✅ | ✅ |
| Forecasting Mode | ⚠️ Basic | ✅ Full | ✅ |
| Strategic Execution | ❌ | ✅ | ✅ |
| QMDJ Destiny | ❌ | ✅ | ✅ |
| Feng Shui Mode | ❌ | ⚠️ Placeholder | ✅ |
| Formation Database | ❌ | ✅ 50+ | ✅ 200+ |
| 7 Star Path | ❌ | ❌ | ✅ |
| 64 Hexagrams | ❌ | ❌ | ✅ |
| AI Analysis | ✅ Project 1 | ✅ Project 1 | ❌ |
| ML Learning | ✅ | ✅ | ❌ |

**v6.0 Target Coverage: ~80% of Joey Yap features + AI advantages**

---

## 🧭 CONTINUITY INSTRUCTIONS

### Starting New Chat:
```
Continue Ming QiMenDunJia (明奇门) development.
Repository: https://github.com/Espivc/ming-qimendunjia
Current: v4.1 → Building v6.0 directly
Check PROJECT_STATE.md for full task list.

Key context:
- Skipping v4.2, v5.0 - going straight to v6.0
- Need: QMDJ pillars, Death & Emptiness, Lead indicators
- Need: Strategic Execution mode, QMDJ Destiny mode
- Need: Formation database (50+)
- User: Ben (Geng Metal, Weak, Pioneer, Wealth Vault)

I want to work on [specific task from PROJECT_STATE.md]
```

### Progress Tracking:
Update this file after completing each task:
```
### PHASE A: Core QMDJ Fixes
- [x] A1. QMDJ Pillars Display ← Mark when done
- [ ] A2. Death & Emptiness
...
```

---

## 👤 USER PROFILE (Ben)

```
Day Master: Geng 庚 (Yang Metal)
Strength: Weak (4/10)
Profile: Pioneer (Indirect Wealth)
Useful Gods: Earth, Metal
Unfavorable: Fire
Special: Wealth Vault present
Birth: 1978-06-27 (27 Jun 1978)
```

---

## 🏷️ VERSION HISTORY

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-12 | Initial QMDJ chart generator |
| 2.0 | 2024-12 | Added export, history, settings |
| 3.0 | 2024-12-30 | Full BaZi integration, rebrand to Ming QiMenDunJia |
| 3.5 | 2024-12-30 | Session state fixes |
| 4.0 | 2024-12-30 | UX streamlined, minute input |
| 4.1 | 2024-12-30 | Joey Yap-inspired redesign |
| **6.0** | **TBD** | **Complete Edition - all modes, all indicators** |

---

## 📚 REFERENCE DOCUMENTS

- `ming-qimendunjia-comparison.md` - Feature comparison with Joey Yap
- `ming-qimendunjia-full-comparison.md` - Full ecosystem (P1+P2) analysis
- `Universal_Data_Schema_v2.json` - Current export format
- Joey Yap Qimen Explorer documentation (external reference)

---

*Ming QiMenDunJia 明奇门 - "Clarity for the People"*
*Target: v6.0 Complete Edition*
