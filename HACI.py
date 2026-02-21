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

# Optional company image or logo (if you have one)
st.image(
    "https://www.halal.org.pk/wp-content/uploads/2022/08/cropped-HACI_logo.png",
    width=300,
    caption="Halal Assessment & Certification Institute (HACI)"
)

# -----------------------------
# Introduction Section
# -----------------------------
intro_text = """
**Halal Assessment & Certification Institute (HACI)** is dedicated to ensuring the availability  
of safe, high‑quality Halal and Tayyib products for Muslim consumers through rigorous assessment,  
training, and certification programs. Our approach combines standards, quality assurance, and  
consumer trust to support halal‑compliant businesses across industries.:contentReference[oaicite:1]{index=1}

In this dashboard, you can navigate the left sidebar to explore detailed insights in the  
following areas:
- **Executive Summary** – High‑level performance indicators  
- **Financials** – Revenue, cost, profitability analysis
- **Sales & Clients** – Market, growth, and customer insights
- **Operational Metrics** – Internal performance and process KPIs

Use the navigation sidebar to explore each section in detail.
"""

st.write(intro_text)

# -----------------------------
# Call to Action / Navigation
# -----------------------------
st.markdown(
    """
    <div style="background-color:#8ecae6; border-radius:8px; padding:20px; margin-top:20px;">
        <h4 style="text-align:center; color:#023047;">
            🧭 Use the left sidebar to navigate between dashboards and explore insights
        </h4>
    </div>
    """,
    unsafe_allow_html=True,
)

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
