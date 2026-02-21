import streamlit as st

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="HACI Business Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Header Section
# -----------------------------
st.markdown("""
<div style="background: linear-gradient(90deg, #023047, #219ebc); padding: 40px; border-radius: 15px; text-align:center;">
    <h1 style="color:white; font-size:48px;">HACI Business Intelligence Dashboard</h1>
    <p style="color:white; font-size:20px;">Empowering Halal businesses with actionable insights and compliance intelligence</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Logo / Image
# -----------------------------
st.image(
    "https://www.halal.org.pk/wp-content/uploads/2022/08/cropped-HACI_logo.png",
    width=250,
    caption="Halal Assessment & Certification Institute (HACI)"
)

# -----------------------------
# Introduction
# -----------------------------
st.markdown("""
**About HACI:**  
HACI ensures safe, high-quality Halal products for consumers through certification, training, and quality assurance programs.  
This dashboard provides insights into financials, sales, client data, and operational performance for better decision-making.
""")

# -----------------------------
# Navigation Cards (Buttons)
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
        st.session_state["page"] = title  # Optional: you can integrate with multi-page navigation
        st.experimental_rerun()  # navigate to selected dashboard

# -----------------------------
# Footer
# -----------------------------
st.markdown("""
<hr>
<p style="text-align:center; font-size:14px;">
📍 HACI – Halal Assessment & Certification Institute Pvt. Ltd., Pakistan |  
📧 halal@halal.org.pk | 📞 +92‑33‑379702035
</p>
""", unsafe_allow_html=True)
