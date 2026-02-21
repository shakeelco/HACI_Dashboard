import streamlit as st

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="HACI Business Intelligence",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Header Section
# -----------------------------
st.markdown(
    """
    <div style="background-color: #023047; padding: 30px; border-radius: 10px;">
        <h1 style="color: white; text-align: center;">
            HACI Business Intelligence Dashboard
        </h1>
        <p style="color: white; text-align: center; font-size:18px;">
            Empowering data‑driven decision making for Halal compliance and business performance
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Optional company image or logo
st.image(
    "https://www.halal.org.pk/wp-content/uploads/2022/08/cropped-HACI_logo.png",
    width=300,
    caption="Halal Assessment & Certification Institute (HACI)"
)

# -----------------------------
# Introduction Section
# -----------------------------
intro_text = """
**Halal Assessment & Certification Institute (HACI)** ensures safe, high‑quality Halal products  
through certification, training, and quality assurance.  

In this dashboard, use the left sidebar or the buttons below to navigate:
- **Executive Summary** – High-level performance indicators  
- **Financials** – Revenue, cost, profitability analysis  
- **Sales & Clients** – Market, growth, and customer insights  
- **Operational Metrics** – Internal performance and process KPIs
"""
st.write(intro_text)

# -----------------------------
# Navigation Cards / Buttons
# -----------------------------
st.subheader("Explore Dashboards")
cols = st.columns(4)
sections = [
    ("Executive Summary", "🧾"),
    ("Financials", "💰"),
    ("Sales & Clients", "📊"),
    ("Operational Metrics", "⚙️")
]

for col, (title, emoji) in zip(cols, sections):
    if col.button(f"{emoji} {title}"):
        st.session_state["page"] = title  # optional: track selection
        st.experimental_rerun()  # navigate (if multi-page setup implemented)

# -----------------------------
# Footer / Contact Info
# -----------------------------
st.markdown(
    """
    <hr>
    <p style="text-align:center; font-size:14px;">
        📍 HACI – Halal Assessment & Certification Institute Pvt. Ltd., Pakistan  
        | 📧 halal@halal.org.pk | 📞 +92‑33‑379702035
    </p>
    """,
    unsafe_allow_html=True,
)
