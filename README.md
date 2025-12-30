# Ming QiMenDunJia 明奇门遁甲 v6.0

## "Clarity for the People" - 奇门遁甲分析系统

A comprehensive Qi Men Dun Jia (QMDJ) analysis system with full BaZi integration.

![Version](https://img.shields.io/badge/version-6.0-gold)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red)

## ✨ Features

### v6.0 Complete Edition

**Core QMDJ Indicators:**
- ✅ QMDJ Four Pillars (Chart time, not BaZi)
- ✅ Death & Emptiness (空亡)
- ✅ Lead Stem Palace (值符宫)
- ✅ Lead Star & Lead Door (直符/直使)
- ✅ Horse Star (驿马)
- ✅ Nobleman Star (贵人)
- ✅ Ju Number (局数)
- ✅ Yang/Yin Structure display

**BaZi Integration:**
- ✅ Four Pillars calculator
- ✅ Day Master strength analysis
- ✅ Useful Gods determination
- ✅ Ten God profile
- ✅ Special structures detection
- ✅ Cross-reference with QMDJ palaces

**Export & Integration:**
- ✅ Universal Schema v3.0 JSON
- ✅ Analysis prompt for Claude (Project 1)
- ✅ ML database row tracking
- ✅ History with outcome tracking

## 📂 File Structure

```
ming-qimendunjia/
├── .streamlit/
│   └── config.toml          # Dark theme config
├── core/
│   ├── __init__.py          # Module exports
│   └── qmdj_engine.py       # QMDJ calculation engine
├── pages/
│   ├── 1_Chart.py           # Chart Generator
│   ├── 2_Export.py          # Export Center
│   ├── 3_History.py         # Reading History
│   ├── 4_Settings.py        # Settings
│   ├── 5_Help.py            # Help & Guide
│   └── 6_BaZi.py            # BaZi Calculator
├── app.py                    # Main dashboard
├── requirements.txt
├── README.md
└── PROJECT_STATE.md         # Development tracking
```

## 🚀 Quick Start

### Local Development

```bash
# Clone repository
git clone https://github.com/Espivc/ming-qimendunjia.git
cd ming-qimendunjia

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py
```

### Deploy to Streamlit Cloud

1. Push to GitHub
2. Connect to Streamlit Cloud
3. Deploy from `app.py`

## 📖 Usage

### 1. Set Up BaZi Profile
- Go to **BaZi Calculator**
- Enter your birth date and time
- Click "Calculate My BaZi"
- Click "Save to Profile"

### 2. Generate QMDJ Chart
- Go to **Chart Generator**
- Select date and time
- Click "Generate Chart"
- Review palaces and indicators

### 3. Analyze a Palace
- Click any palace in the grid
- Review Star, Door, Deity
- Check special indicators
- See BaZi alignment

### 4. Export for AI Analysis
- Go to **Export Center**
- Copy JSON or Analysis Prompt
- Paste into Claude (Project 1)
- Receive detailed interpretation

## 🔗 Two-Project Architecture

```
PROJECT 2 (Ming QiMenDunJia)          PROJECT 1 (Claude)
┌──────────────────────┐        ┌──────────────────────┐
│ • Generate QMDJ      │        │ • Formation ID       │
│ • Calculate BaZi     │ ──────▶│ • Strategic synthesis│
│ • Export JSON        │        │ • Deep analysis      │
│ • Track outcomes     │        │ • Bilingual reports  │
└──────────────────────┘        └──────────────────────┘
```

## 📊 Universal Schema v3.0

The export format includes:
- Metadata (datetime, method, purpose)
- QMDJ data (pillars, indicators, components)
- BaZi data (Day Master, useful gods, profile)
- Synthesis (scores, verdict, recommendations)
- Tracking (DB row, outcome status)

## 🎨 Design

- **Theme:** Dark luxury (navy + gold)
- **Fonts:** Cinzel (headers), Noto Sans SC (Chinese)
- **Colors:** 
  - Gold: #FFD700
  - Purple: #9B59B6
  - Navy: #0a0a12

## 📝 License

Open source - "Helping People First"

## 👤 Author

Ben - Geng Metal Day Master, Pioneer (Indirect Wealth)

---

*Ming QiMenDunJia 明奇门 - Clarity for the People*
