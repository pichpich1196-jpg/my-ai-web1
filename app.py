import os
import tempfile
import docx
from google import genai
from pptx import Presentation
import streamlit as st

# កំណត់ទម្រង់ទំព័រ
st.set_page_config(
    page_title="KhemaraAI WorkSuite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==================== KHEMARAAI DARK SAAS CSS ====================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Kantumruy+Pro:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"], .stApp {
        font-family: 'Kantumruy Pro', sans-serif !important;
        background-color: #0b0e17 !important;
        color: #e2e8f0 !important;
    }

    /* Navbar Header */
    .top-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 5px 0 20px 0;
        border-bottom: 1px solid #1e2436;
        margin-bottom: 25px;
    }
    .brand-box {
        display: flex;
        align-items: center;
        gap: 14px;
    }
    .brand-logo {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        width: 44px;
        height: 44px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        box-shadow: 0 4px 15px rgba(168, 85, 247, 0.4);
    }
    .brand-title {
        font-size: 22px;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: 0.5px;
    }
    .brand-subtitle {
        font-size: 13px;
        color: #94a3b8;
    }
    .status-badge {
        background-color: rgba(16, 185, 129, 0.12);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #131722;
        padding: 6px;
        border-radius: 14px;
        border: 1px solid #1e2433;
        margin-bottom: 25px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 42px;
        border-radius: 10px;
        font-weight: 500;
        font-size: 14px;
        color: #94a3b8;
        padding: 0 18px;
        border: none !important;
        background-color: transparent;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.35);
    }

    /* Container Cards */
    .card-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }
    .card-header-title {
        font-size: 18px;
        font-weight: 700;
        color: #f8fafc;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .tag-badge {
        background: rgba(99, 102, 241, 0.15);
        color: #818cf8;
        border: 1px solid rgba(99, 102, 241, 0.3);
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }

    /* Primary Action Button */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #7c3aed 0%, #6366f1 100%) !important;
        color: #ffffff !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        border: none !important;
        width: 100% !important;
        transition: all 0.25s ease !important;
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.35) !important;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(124, 58, 237, 0.5) !important;
    }

    /* Upload Box Styling */
    [data-testid="stFileUploader"] {
        background-color: #0f121d;
        border: 1.5px dashed #2d3748;
        border-radius: 14px;
        padding: 12px;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #6366f1;
    }
