"""
Ming Qimen 明奇门 - History v6.0
View past readings and track outcomes
"""

import streamlit as st
from datetime import datetime, timezone, timedelta
import json

st.set_page_config(page_title="History | Ming Qimen", page_icon="📜", layout="wide")

# CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&display=swap');
    
    .page-header {
        font-family: 'Cinzel', serif;
        color: #FFD700;
        font-size: 2rem;
        letter-spacing: 2px;
    }
    
    .history-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #12121e 100%);
        border: 1px solid #333;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.2s ease;
    }
    
    .history-card:hover {
        border-color: #FFD700;
    }
    
    .history-date {
        font-family: 'Cinzel', serif;
        color: #FFD700;
        font-size: 1.1rem;
    }
    
    .history-details {
        color: #888;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    .verdict-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
    }
    
    .verdict-highly-auspicious { background: #27ae60; color: white; }
    .verdict-auspicious { background: #2ecc71; color: white; }
    .verdict-neutral { background: #f39c12; color: black; }
    .verdict-inauspicious { background: #e67e22; color: white; }
    .verdict-highly-inauspicious { background: #c0392b; color: white; }
    
    .outcome-badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.75rem;
        margin-left: 0.5rem;
    }
    
    .outcome-pending { background: #95a5a6; color: white; }
    .outcome-success { background: #27ae60; color: white; }
    .outcome-partial { background: #f39c12; color: black; }
    .outcome-failure { background: #e74c3c; color: white; }
    
    .empty-state {
        text-align: center;
        padding: 3rem;
        color: #888;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #12121e 100%);
        border: 1px solid #333;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }
    
    .stat-number {
        font-family: 'Cinzel', serif;
        color: #FFD700;
        font-size: 2rem;
        font-weight: 700;
    }
    
    .stat-label {
        color: #888;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="page-header">📜 HISTORY</h1>', unsafe_allow_html=True)
st.markdown("*Past readings and outcome tracking*")

st.divider()

# Initialize history in session state
if "reading_history" not in st.session_state:
    st.session_state.reading_history = []

history = st.session_state.reading_history

# Stats row
if history:
    col1, col2, col3, col4 = st.columns(4)
    
    total = len(history)
    pending = len([h for h in history if h.get("outcome") == "PENDING"])
    success = len([h for h in history if h.get("outcome") == "SUCCESS"])
    
    success_rate = (success / (total - pending) * 100) if (total - pending) > 0 else 0
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{total}</div>
            <div class="stat-label">Total Readings</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{pending}</div>
            <div class="stat-label">Pending Outcome</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{success}</div>
            <div class="stat-label">Successful</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{success_rate:.0f}%</div>
            <div class="stat-label">Success Rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()

# Display history
if history:
    st.subheader("📋 Reading History")
    
    for idx, reading in enumerate(reversed(history)):
        verdict = reading.get("verdict", "NEUTRAL")
        verdict_class = f"verdict-{verdict.lower().replace(' ', '-')}"
        outcome = reading.get("outcome", "PENDING")
        outcome_class = f"outcome-{outcome.lower()}"
        
        st.markdown(f"""
        <div class="history-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span class="history-date">{reading.get('date', 'Unknown')} {reading.get('time', '')}</span>
                    <span class="verdict-badge {verdict_class}">{verdict}</span>
                    <span class="outcome-badge {outcome_class}">{outcome}</span>
                </div>
                <div style="color: #FFD700;">
                    Palace {reading.get('palace', '?')} • Ju {reading.get('ju', '?')}
                </div>
            </div>
            <div class="history-details">
                <strong>Lead:</strong> P{reading.get('lead_palace', '?')} | 
                <strong>Star:</strong> {reading.get('star', '?')} | 
                <strong>Door:</strong> {reading.get('door', '?')} |
                <strong>Score:</strong> {reading.get('score', '?')}/10
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander(f"Details & Outcome Tracking"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Reading Details:**")
                st.json(reading)
            
            with col2:
                st.markdown("**Update Outcome:**")
                new_outcome = st.selectbox(
                    "Outcome",
                    ["PENDING", "SUCCESS", "PARTIAL", "FAILURE", "NOT_APPLICABLE"],
                    index=["PENDING", "SUCCESS", "PARTIAL", "FAILURE", "NOT_APPLICABLE"].index(outcome),
                    key=f"outcome_{idx}"
                )
                
                notes = st.text_area("Notes", reading.get("notes", ""), key=f"notes_{idx}")
                
                if st.button("💾 Save", key=f"save_{idx}"):
                    # Update in reversed order
                    actual_idx = len(history) - 1 - idx
                    st.session_state.reading_history[actual_idx]["outcome"] = new_outcome
                    st.session_state.reading_history[actual_idx]["notes"] = notes
                    st.success("Saved!")
                    st.rerun()
    
    st.divider()
    
    # Export history
    st.subheader("📤 Export History")
    
    col1, col2 = st.columns(2)
    
    with col1:
        json_str = json.dumps(history, indent=2, ensure_ascii=False)
        st.download_button(
            "⬇️ Download as JSON",
            json_str,
            file_name=f"ming_qimen_history_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col2:
        # CSV format
        csv_lines = ["Date,Time,Palace,Ju,Star,Door,Score,Verdict,Outcome,Notes"]
        for h in history:
            csv_lines.append(f"{h.get('date','')},{h.get('time','')},{h.get('palace','')},{h.get('ju','')},{h.get('star','')},{h.get('door','')},{h.get('score','')},{h.get('verdict','')},{h.get('outcome','')},{h.get('notes','').replace(',',';')}")
        
        csv_str = "\n".join(csv_lines)
        st.download_button(
            "⬇️ Download as CSV",
            csv_str,
            file_name=f"ming_qimen_history_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    # Clear history
    st.divider()
    if st.button("🗑️ Clear All History", type="secondary"):
        if st.checkbox("I understand this cannot be undone"):
            st.session_state.reading_history = []
            st.success("History cleared!")
            st.rerun()

else:
    # Empty state
    st.markdown("""
    <div class="empty-state">
        <div style="font-size: 4rem; margin-bottom: 1rem;">📜</div>
        <h2>No Readings Yet</h2>
        <p>Generate your first QMDJ chart to start tracking your readings and outcomes.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("📊 Generate First Chart", type="primary", use_container_width=True):
        st.switch_page("pages/1_Chart.py")

# Sidebar
with st.sidebar:
    st.markdown("### 📜 History")
    
    if history:
        st.markdown(f"**Total:** {len(history)} readings")
        
        # Quick stats
        verdicts = [h.get("verdict", "NEUTRAL") for h in history]
        for v in set(verdicts):
            count = verdicts.count(v)
            st.markdown(f"- {v}: {count}")
    else:
        st.info("No history yet")
    
    st.markdown("---")
    st.markdown("### 💡 Tips")
    st.markdown("""
    - Track outcomes to improve predictions
    - Export data for ML analysis
    - Review patterns over time
    """)

st.markdown("---")
st.caption("🌟 Ming Qimen 明奇门 | History v6.0")
