import streamlit as st
import pandas as pd
import time
import pickle
import jwt
from streamlit_option_menu import option_menu
from streamlit.components.v1 import html
from sqlalchemy import text
from streamlit_oauth import OAuth2Component

# --- Google OAuth Configuration ---
GOOGLE_CLIENT_ID = st.secrets.get("google_oauth", {}).get("client_id", "")
GOOGLE_CLIENT_SECRET = st.secrets.get("google_oauth", {}).get("client_secret", "")
REDIRECT_URI = st.secrets.get("google_oauth", {}).get("redirect_uri", "http://localhost:8501")
AUTHORIZE_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"

# --- Streamlit Page Config ---
st.set_page_config(
    page_title="Milkqu - Predict Milk Quality",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="auto",
)


def main():
    """Login screen with modern milk-themed design."""
    
    # Welcome Header with Gradient
    st.markdown(
        """
        <div style="text-align: center; padding: 40px 20px; animation: fadeInUp 0.6s ease-out;">
            <div style="font-size: 4rem; margin-bottom: 10px;">🥛</div>
            <h1 style="
                font-size: 3.5rem; 
                font-weight: 800; 
                background: linear-gradient(135deg, #4AAED9 0%, #7DD3FC 50%, #FFF8E7 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin: 0;
                text-shadow: none;
            ">Welcome to MilkQu</h1>
            <p style="
                color: #B8C5D3 !important; 
                font-size: 1.2rem; 
                margin-top: 12px;
                font-weight: 400;
            ">Predict your milk quality easily with AI-powered analysis</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # Hero Image with Glassmorphism Container
    st.markdown(
        """
        <div style="
            display: flex; 
            justify-content: center; 
            margin: 40px auto;
            padding: 20px;
        ">
            <div style="
                background: rgba(26, 35, 50, 0.6);
                backdrop-filter: blur(20px);
                -webkit-backdrop-filter: blur(20px);
                border: 1px solid rgba(74, 174, 217, 0.2);
                border-radius: 24px;
                padding: 16px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
                max-width: 550px;
                transition: all 0.4s ease;
            "
            onmouseover="this.style.transform='translateY(-8px)'; this.style.boxShadow='0 30px 80px rgba(74, 174, 217, 0.2)';"
            onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 20px 60px rgba(0, 0, 0, 0.4)';"
            >
                <img src="https://raw.githubusercontent.com/jidan24/asset/refs/heads/master/milk-%230e1117.jpg" 
                    alt="MilkQu - AI Milk Quality Prediction"
                    style="
                        width: 100%;
                        border-radius: 16px;
                        display: block;
                    "
                >
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Features Section
    st.markdown(
        """
        <div style="
            display: flex;
            justify-content: center;
            gap: 20px;
            flex-wrap: wrap;
            margin: 40px auto;
            max-width: 700px;
        ">
            <div style="
                background: rgba(26, 35, 50, 0.5);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(74, 174, 217, 0.15);
                border-radius: 12px;
                padding: 16px 24px;
                text-align: center;
                flex: 1;
                min-width: 150px;
            ">
                <div style="font-size: 1.5rem; margin-bottom: 8px;">🔬</div>
                <div style="color: #F5F5F5 !important; font-weight: 600; font-size: 0.9rem;">AI Analysis</div>
            </div>
            <div style="
                background: rgba(26, 35, 50, 0.5);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(74, 174, 217, 0.15);
                border-radius: 12px;
                padding: 16px 24px;
                text-align: center;
                flex: 1;
                min-width: 150px;
            ">
                <div style="font-size: 1.5rem; margin-bottom: 8px;">⚡</div>
                <div style="color: #F5F5F5 !important; font-weight: 600; font-size: 0.9rem;">Fast Results</div>
            </div>
            <div style="
                background: rgba(26, 35, 50, 0.5);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(74, 174, 217, 0.15);
                border-radius: 12px;
                padding: 16px 24px;
                text-align: center;
                flex: 1;
                min-width: 150px;
            ">
                <div style="font-size: 1.5rem; margin-bottom: 8px;">📊</div>
                <div style="color: #F5F5F5 !important; font-weight: 600; font-size: 0.9rem;">Track History</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Login Section
    st.markdown(
        """
        <div style="
            text-align: center;
            margin: 30px auto;
            padding: 30px;
            max-width: 400px;
            background: rgba(26, 35, 50, 0.6);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(74, 174, 217, 0.2);
            border-radius: 20px;
        ">
            <p style="color: #B8C5D3 !important; margin-bottom: 20px; font-size: 1rem;">
                Sign in to access milk quality predictions
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Render OAuth button
    render_oauth_button()
    
    # Footer
    st.markdown(
        """
        <div style="text-align: center; margin-top: 60px; padding: 20px;">
            <p style="color: #5A6A7A !important; font-size: 0.85rem;">
                © 2025 MilkQu • Powered by Machine Learning
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# --- Apply style & script configurations ---
style_configurations = """
<style>
    /* ═══════════════════════════════════════════════════════════════════
       🥛 MILKQU DESIGN SYSTEM - Milk-Themed Modern Dark UI
       ═══════════════════════════════════════════════════════════════════ */
    
    /* CSS Variables for easy theming */
    :root {
        --milk-primary: #4AAED9;
        --milk-primary-light: #7DD3FC;
        --milk-cream: #FFF8E7;
        --milk-white: #FEFEFE;
        --milk-success: #22C55E;
        --milk-warning: #FBBF24;
        --milk-danger: #EF4444;
        --milk-bg: #0C1222;
        --milk-surface: #1A2332;
        --milk-surface-light: #243447;
        --milk-text: #F5F5F5;
        --milk-text-secondary: #B8C5D3;
        --milk-border: #3D4F5F;
    }
    
    /* ─── GLOBAL STYLES ─────────────────────────────────────────────── */
    .stApp {
        background: linear-gradient(135deg, #0C1222 0%, #1A2332 50%, #0C1222 100%);
        background-attachment: fixed;
    }
    
    .main .block-container {
        background: transparent;
        padding: 2rem;
        max-width: 1200px;
    }
    
    /* ─── TYPOGRAPHY ────────────────────────────────────────────────── */
    h1, h2, h3, h4, h5 {
        color: var(--milk-text) !important;
        font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
        font-weight: 600;
    }
    
    h1 {
        background: linear-gradient(135deg, var(--milk-primary) 0%, var(--milk-primary-light) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    p, li, span, label, div {
        color: var(--milk-text-secondary) !important;
        font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
    }
    
    /* ─── GLASSMORPHISM CARDS ───────────────────────────────────────── */
    .glass-card {
        background: rgba(26, 35, 50, 0.7);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(74, 174, 217, 0.2);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(74, 174, 217, 0.15);
        border-color: rgba(74, 174, 217, 0.4);
    }
    
    /* ─── BUTTONS ───────────────────────────────────────────────────── */
    .stButton > button {
        background: linear-gradient(135deg, var(--milk-primary) 0%, var(--milk-primary-light) 100%);
        color: #0C1222 !important;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(74, 174, 217, 0.4);
        transition: all 0.3s ease;
        width: auto;
        min-width: 180px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(74, 174, 217, 0.5);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }

    .stButton {
        display: flex;
        justify-content: center;
        margin-top: 1rem;
    }
    
    /* ─── FORM INPUTS ───────────────────────────────────────────────── */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background-color: var(--milk-surface) !important;
        color: var(--milk-text) !important;
        border: 1px solid var(--milk-border) !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: var(--milk-primary) !important;
        box-shadow: 0 0 0 3px rgba(74, 174, 217, 0.2) !important;
    }
    
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        background-color: var(--milk-surface) !important;
        border-color: var(--milk-border) !important;
        border-radius: 10px !important;
    }
    
    /* ─── DATAFRAMES ────────────────────────────────────────────────── */
    .stDataFrame {
        background-color: var(--milk-surface);
        border-radius: 12px;
        overflow: hidden;
    }
    
    .stDataFrame > div > div > div {
        background-color: var(--milk-surface) !important;
    }
    
    /* ─── PROGRESS BAR ──────────────────────────────────────────────── */
    .stProgress > div > div {
        background: linear-gradient(90deg, var(--milk-primary) 0%, var(--milk-primary-light) 100%) !important;
        border-radius: 10px;
    }
    
    .stProgress > div {
        background-color: var(--milk-surface-light) !important;
        border-radius: 10px;
    }
    
    /* ─── ALERTS ────────────────────────────────────────────────────── */
    .stAlert {
        background: rgba(74, 174, 217, 0.1) !important;
        color: var(--milk-text) !important;
        border: 1px solid rgba(74, 174, 217, 0.3) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px);
    }
    
    /* ─── EXPANDER ──────────────────────────────────────────────────── */
    .streamlit-expanderHeader {
        background: var(--milk-surface-light) !important;
        color: var(--milk-text) !important;
        border-radius: 12px !important;
        border: 1px solid var(--milk-border) !important;
        padding: 16px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: var(--milk-surface) !important;
        border-color: var(--milk-primary) !important;
    }
    
    .streamlit-expanderContent {
        background: var(--milk-surface) !important;
        border: 1px solid var(--milk-border) !important;
        border-top: none !important;
        border-radius: 0 0 12px 12px !important;
        padding: 20px !important;
    }
    
    /* ─── SIDEBAR ───────────────────────────────────────────────────── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0C1222 0%, #1A2332 100%) !important;
        border-right: 1px solid var(--milk-border);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: transparent !important;
    }
    
    /* ─── CODE BLOCKS ───────────────────────────────────────────────── */
    code {
        background-color: var(--milk-surface-light) !important;
        color: var(--milk-primary-light) !important;
        padding: 3px 8px;
        border-radius: 6px;
        font-family: 'JetBrains Mono', 'Fira Code', monospace;
    }
    
    pre {
        background-color: var(--milk-surface) !important;
        border-radius: 12px;
        padding: 16px;
        border: 1px solid var(--milk-border);
    }
    
    /* ─── CUSTOM DIVIDER ────────────────────────────────────────────── */
    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent 0%, var(--milk-border) 50%, transparent 100%) !important;
        margin: 24px 0 !important;
    }
    
    /* ─── FORM SUBMIT BUTTON ────────────────────────────────────────── */
    div[data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(135deg, var(--milk-primary) 0%, var(--milk-primary-light) 100%);
        color: #0C1222 !important;
        border: none;
        font-weight: 600;
        padding: 0.75rem 2rem;
        border-radius: 12px;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    div[data-testid="stFormSubmitButton"] > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(74, 174, 217, 0.4);
    }
    
    /* ─── DOWNLOAD BUTTON ───────────────────────────────────────────── */
    div[data-testid="stDownloadButton"] > button {
        background: linear-gradient(135deg, var(--milk-success) 0%, #34D399 100%);
        color: #0C1222 !important;
        border: none;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        transition: all 0.3s ease;
    }
    
    div[data-testid="stDownloadButton"] > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(34, 197, 94, 0.4);
    }
    
    /* ─── METRIC CARDS ──────────────────────────────────────────────── */
    .metric-card {
        background: rgba(26, 35, 50, 0.8);
        backdrop-filter: blur(20px);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(74, 174, 217, 0.1);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
    }
    
    .metric-value {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 4px;
    }
    
    .metric-label {
        font-size: 14px;
        color: var(--milk-text-secondary);
        opacity: 0.8;
    }
    
    /* ─── ANIMATIONS ────────────────────────────────────────────────── */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    
    .animate-fadeIn {
        animation: fadeInUp 0.5s ease-out;
    }
    
    /* ─── SCROLLBAR ─────────────────────────────────────────────────── */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--milk-bg);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--milk-border);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--milk-primary);
    }
    
    /* ─── MOBILE RESPONSIVE ─────────────────────────────────────────── */
    @media (max-width: 768px) {
        h1 {
            font-size: 2rem !important;
        }
        
        h2 {
            font-size: 1.5rem !important;
        }
        
        .main .block-container {
            padding: 1rem !important;
        }
        
        /* Make inputs touch-friendly */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input {
            min-height: 44px !important;
            font-size: 16px !important;
        }
        
        .stButton > button {
            min-height: 48px !important;
            font-size: 1rem !important;
            padding: 0.75rem 1rem !important;
        }
        
        /* Stack columns on mobile */
        [data-testid="stHorizontalBlock"] {
            flex-wrap: wrap;
        }
        
        [data-testid="stHorizontalBlock"] > div {
            flex: 1 1 100% !important;
            min-width: 100% !important;
        }
        
        /* Metric cards responsive */
        .metric-card {
            padding: 16px !important;
        }
        
        .metric-value {
            font-size: 24px !important;
        }
        
        /* Sidebar adjustments */
        [data-testid="stSidebar"] {
            min-width: 250px !important;
        }
        
        /* Form container */
        .stForm {
            padding: 12px !important;
        }
        
        /* Glassmorphism cards */
        .glass-card {
            padding: 16px !important;
            border-radius: 12px !important;
        }
    }
    
    @media (max-width: 480px) {
        h1 {
            font-size: 1.75rem !important;
        }
        
        .main .block-container {
            padding: 0.5rem !important;
        }
        
        /* Extra small screen adjustments */
        .stButton > button {
            width: 100% !important;
        }
    }
</style>
"""
script_configurations = """
<script>
    console.log("Welcome To Milkqu Version 0.0.1");
</script>
"""

st.markdown(style_configurations, unsafe_allow_html=True)
html(script_configurations)


# --- Declare global function ---
@st.cache_data
def load_default_milk_data():
    return pd.DataFrame(
        {
            "pH": ["6.6"],
            "Temprature": ["35"],
            "Taste": ["1"],
            "Odor": ["0"],
            "Fat ": ["1"],
            "Turbidity": ["0"],
            "Colour": ["254"],
        },
        index=[0],
    )


@st.cache_data
def load_milk_data(ph, temprature, taste, odor, fat, turbidity, colour):
    return pd.DataFrame(
        {
            "pH": [ph],
            "Temprature": [temprature],
            "Taste": [taste],
            "Odor": [odor],
            "Fat ": [fat],
            "Turbidity": [turbidity],
            "Colour": [colour],
        },
        index=[0],
    )


@st.cache_data
def load_encoded_milk_data(ph, temprature, taste, odor, fat, turbidity, colour, _list_column):
    return pd.DataFrame(
        {
            "pH": ph,
            "Temprature": temprature,
            "Taste": taste,
            "Odor": odor,
            "Fat ": fat,
            "Turbidity": turbidity,
            "Colour": colour,
        },
        index=[0],
        columns=_list_column,
    )


@st.cache_resource
def init_model():
    return pickle.load(open("milk_model.pickle", "rb"))


# Function for parsing with type safety
def safe_get_float(source: dict, key: str, default: float = 0.0) -> float:
    """Safely get float value from source dict, returns non-negative only."""
    try:
        value = float(source.get(key, [default])[0])
        return max(0.0, value)  # Ensure non-negative
    except (ValueError, TypeError, IndexError):
        return max(0.0, default)


def safe_get_int(source: dict, key: str, default: int = 0) -> int:
    """Safely get int value from source dict, returns non-negative only."""
    try:
        value = int(source.get(key, [default])[0])
        return max(0, value)  # Ensure non-negative
    except (ValueError, TypeError, IndexError):
        return max(0, default)


# --- Declare global variables ---
current_url = st.query_params.to_dict()
direct_menu = int(current_url["redirect"][0]) if "redirect" in current_url else 0

tilt_effect = """
<div class="contaienr">
    <img src="https://raw.githubusercontent.com/jidan24/asset/refs/heads/master/milk-%230e1117.jpg" alt="Milkqu Header" style="width: 100%;"/>
</div>
<br/>
"""

# --- Google OAuth Login Functions ---
def init_session_state():
    """Initialize session state for OAuth."""
    if "user_info" not in st.session_state:
        st.session_state.user_info = None

def logout():
    """Clear session and logout user."""
    st.session_state.user_info = None
    # Note: st.rerun() tidak dipanggil di sini karena akan otomatis rerun setelah callback

def is_user_logged_in():
    """Check if user is logged in via OAuth."""
    init_session_state()
    return st.session_state.user_info is not None

def get_user_name():
    """Get logged in user's name."""
    if st.session_state.user_info:
        return st.session_state.user_info.get("name", st.session_state.user_info.get("email", "User"))
    return "User"

def render_oauth_button():
    """Render Google OAuth login button and handle authentication."""
    if GOOGLE_CLIENT_ID == "" or GOOGLE_CLIENT_SECRET == "":
        st.error("⚠️ Google OAuth belum dikonfigurasi. Silakan tambahkan `client_id` dan `client_secret` di `.streamlit/secrets.toml`")
        st.code("""
[google_oauth]
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
redirect_uri = "http://localhost:8501"
        """, language="toml")
        return False
    
    oauth2 = OAuth2Component(
        GOOGLE_CLIENT_ID,
        GOOGLE_CLIENT_SECRET,
        AUTHORIZE_ENDPOINT,
        TOKEN_ENDPOINT,
        TOKEN_ENDPOINT,
    )
    
    result = oauth2.authorize_button(
        "🔐 Log in with Google",
        redirect_uri=REDIRECT_URI,
        scope="openid email profile",
    )
    
    if result and "token" in result:
        try:
            id_token = result["token"]["id_token"]
            user_info = jwt.decode(id_token, options={"verify_signature": False})
            st.session_state.user_info = user_info
            st.rerun()
        except Exception as e:
            st.error(f"Login failed: {str(e)}")
    
    return False

# Initialize session state
init_session_state()

# CORE
if not is_user_logged_in():
    main()
else:

    # --- Sidebar ---
    with st.sidebar:
        # Sidebar Header with Logo
        st.markdown(
            """
            <div style="
                text-align: center;
                padding: 20px 10px;
                margin-bottom: 10px;
            ">
                <div style="font-size: 2.5rem; margin-bottom: 8px;">🥛</div>
                <h2 style="
                    font-size: 1.5rem;
                    font-weight: 700;
                    background: linear-gradient(135deg, #4AAED9 0%, #7DD3FC 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    margin: 0;
                ">MilkQu</h2>
                <p style="color: #5A6A7A !important; font-size: 0.75rem; margin-top: 4px;">v1.0.0</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        st.markdown("---")

        # --- Menu ---
        menu = option_menu(
            None,
            ["Documentations", "Milkqu Prediction", "Prediction History"],
            icons=["book", "droplet-half", "clock-history"],
            default_index=int(direct_menu),
            styles={
                "container": {
                    "background-color": "transparent",
                    "padding": "8px 0",
                },
                "icon": {
                    "color": "#4AAED9",
                    "font-size": "18px",
                },
                "nav-link": {
                    "color": "#B8C5D3",
                    "font-size": "15px",
                    "text-align": "left",
                    "margin": "4px 0",
                    "padding": "12px 16px",
                    "border-radius": "10px",
                    "transition": "all 0.3s ease",
                },
                "nav-link-selected": {
                    "background": "linear-gradient(135deg, rgba(74, 174, 217, 0.2) 0%, rgba(125, 211, 252, 0.1) 100%)",
                    "color": "#F5F5F5",
                    "font-weight": "600",
                    "border": "1px solid rgba(74, 174, 217, 0.3)",
                },
            }
        )

        st.markdown("---")

        # External Links
        st.markdown(
            """
            <style>
            .modern-link {
                display: flex;
                align-items: center;
                gap: 12px;
                background: rgba(26, 35, 50, 0.5);
                border: 1px solid rgba(74, 174, 217, 0.15);
                border-radius: 10px;
                padding: 12px 16px;
                margin-bottom: 8px;
                color: #B8C5D3 !important;
                text-decoration: none;
                font-size: 14px;
                font-weight: 500;
                transition: all 0.3s ease;
            }
            .modern-link:hover {
                background: rgba(74, 174, 217, 0.15);
                border-color: rgba(74, 174, 217, 0.4);
                color: #F5F5F5 !important;
                transform: translateX(4px);
            }
            .link-icon {
                width: 20px;
                height: 20px;
                opacity: 0.8;
            }
            </style>
            
            <a href="https://github.com/bimbingan-skripsi-jidan/prediction-milkqu" target="_blank" class="modern-link">
                <svg class="link-icon" viewBox="0 0 24 24" fill="#B8C5D3">
                    <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405 1.02 0 2.04.135 3 .405 2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z"/>
                </svg>
                GitHub Repository
            </a>
            <a href="https://www.kaggle.com/datasets/jidanhaviarsaviola/milk-quality" target="_blank" class="modern-link">
                <svg class="link-icon" viewBox="0 0 24 24" fill="#B8C5D3">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/>
                </svg>
                Explore Dataset
            </a>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")
        
        # User Info Card
        st.markdown(
            f"""
            <div style="
                background: rgba(26, 35, 50, 0.6);
                border: 1px solid rgba(74, 174, 217, 0.2);
                border-radius: 12px;
                padding: 16px;
                margin-bottom: 16px;
            ">
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
                    <div style="
                        width: 40px;
                        height: 40px;
                        background: linear-gradient(135deg, #4AAED9 0%, #7DD3FC 100%);
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 1.2rem;
                    ">👤</div>
                    <div>
                        <div style="color: #F5F5F5 !important; font-weight: 600; font-size: 0.95rem;">{get_user_name()}</div>
                        <div style="color: #5A6A7A !important; font-size: 0.75rem;">Logged in</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        st.button("🚪 Log out", on_click=logout)

    if menu == "Documentations":

        # ─── PAGE HEADER ────────────────────────────────────────────────────────────────
        st.markdown(
            """
            <div style="
                text-align: center;
                padding: 40px 20px;
                background: linear-gradient(135deg, rgba(74, 174, 217, 0.1) 0%, rgba(125, 211, 252, 0.05) 100%);
                border-radius: 20px;
                border: 1px solid rgba(74, 174, 217, 0.2);
                margin-bottom: 30px;
            ">
                <div style="font-size: 3rem; margin-bottom: 16px;">📖</div>
                <h1 style="
                    font-size: 2.5rem;
                    font-weight: 700;
                    background: linear-gradient(135deg, #4AAED9 0%, #7DD3FC 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    margin: 0;
                ">MilkQu Documentation</h1>
                <p style="color: #B8C5D3 !important; font-size: 1.1rem; margin-top: 12px;">
                    Learn how to use our AI-powered milk quality prediction system
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ─── WHAT IS MILKQU? ───────────────────────────────────────────────────────────
        st.markdown(
            """
            <div style="
                background: rgba(26, 35, 50, 0.6);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(74, 174, 217, 0.2);
                border-radius: 16px;
                padding: 24px;
                margin-bottom: 20px;
            ">
                <h2 style="color: #F5F5F5 !important; margin-top: 0; display: flex; align-items: center; gap: 12px;">
                    <span style="font-size: 1.5rem;">🥛</span> What is MilkQu?
                </h2>
                <p style="color: #B8C5D3 !important; line-height: 1.8; margin: 0;">
                    <strong style="color: #4AAED9 !important;">MilkQu (Milk Quality)</strong> adalah web app berbasis machine learning untuk mengklasifikasikan kualitas susu berdasarkan parameter: keasaman, suhu, kejernihan, bau, kandungan lemak, tingkat keruh, dan warna.
                    <br><br>
                    Dataset diambil dari Kaggle untuk memahami karakteristik fisika & kimia susu. Melalui antarmuka yang intuitif, Anda dapat mengunduh laporan prediksi history dengan format CSV untuk analisis lebih dalam.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ─── FEATURES ────────────────────────────────────────────────────────────
        st.markdown(
            """
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 20px;">
                <div style="
                    background: rgba(26, 35, 50, 0.5);
                    border: 1px solid rgba(34, 197, 94, 0.2);
                    border-radius: 12px;
                    padding: 20px;
                    text-align: center;
                ">
                    <div style="font-size: 2rem; margin-bottom: 12px;">🔬</div>
                    <div style="color: #22C55E !important; font-weight: 600;">AI Analysis</div>
                    <p style="color: #B8C5D3 !important; font-size: 0.85rem; margin-top: 8px;">Machine learning-powered predictions</p>
                </div>
                <div style="
                    background: rgba(26, 35, 50, 0.5);
                    border: 1px solid rgba(251, 191, 36, 0.2);
                    border-radius: 12px;
                    padding: 20px;
                    text-align: center;
                ">
                    <div style="font-size: 2rem; margin-bottom: 12px;">📊</div>
                    <div style="color: #FBBF24 !important; font-weight: 600;">Rich Dataset</div>
                    <p style="color: #B8C5D3 !important; font-size: 0.85rem; margin-top: 8px;">1000+ samples from Kaggle</p>
                </div>
                <div style="
                    background: rgba(26, 35, 50, 0.5);
                    border: 1px solid rgba(74, 174, 217, 0.2);
                    border-radius: 12px;
                    padding: 20px;
                    text-align: center;
                ">
                    <div style="font-size: 2rem; margin-bottom: 12px;">📥</div>
                    <div style="color: #4AAED9 !important; font-weight: 600;">Export CSV</div>
                    <p style="color: #B8C5D3 !important; font-size: 0.85rem; margin-top: 8px;">Download prediction history</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ─── ABOUT DATASETS ────────────────────────────────────────────────────────────
        with st.expander("📊 About the Dataset"):
            st.markdown("""
**Milk Quality Dataset from Kaggle**

| Feature | Description |
|---------|-------------|
| **pH** | Acidity level (6.0 - 7.0) |
| **Temperature** | Milk temperature in °C |
| **Taste** | Normal (1) or Abnormal (0) |
| **Odor** | Fresh (1) or Spoiled (0) |
| **Fat** | Fat content level |
| **Turbidity** | Cloudiness level |
| **Colour** | Color index |
| **Grade** | Quality output (High/Medium/Low) |
            """)

        # ─── HOW IT WORKS ──────────────────────────────────────────────────────────
        st.markdown(
            """
            <div style="
                background: rgba(26, 35, 50, 0.6);
                border: 1px solid rgba(74, 174, 217, 0.2);
                border-radius: 16px;
                padding: 24px;
                margin: 20px 0;
            ">
                <h2 style="color: #F5F5F5 !important; margin-top: 0; display: flex; align-items: center; gap: 12px;">
                    <span style="font-size: 1.5rem;">⚙️</span> How It Works
                </h2>
                <div style="display: flex; flex-direction: column; gap: 16px;">
                    <div style="display: flex; align-items: center; gap: 16px;">
                        <div style="
                            min-width: 40px;
                            height: 40px;
                            background: linear-gradient(135deg, #4AAED9 0%, #7DD3FC 100%);
                            border-radius: 50%;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            font-weight: 700;
                            color: #0C1222;
                        ">1</div>
                        <p style="color: #B8C5D3 !important; margin: 0;">Input milk parameters (pH, temperature, etc.)</p>
                    </div>
                    <div style="display: flex; align-items: center; gap: 16px;">
                        <div style="
                            min-width: 40px;
                            height: 40px;
                            background: linear-gradient(135deg, #4AAED9 0%, #7DD3FC 100%);
                            border-radius: 50%;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            font-weight: 700;
                            color: #0C1222;
                        ">2</div>
                        <p style="color: #B8C5D3 !important; margin: 0;">ML model analyzes your data</p>
                    </div>
                    <div style="display: flex; align-items: center; gap: 16px;">
                        <div style="
                            min-width: 40px;
                            height: 40px;
                            background: linear-gradient(135deg, #4AAED9 0%, #7DD3FC 100%);
                            border-radius: 50%;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            font-weight: 700;
                            color: #0C1222;
                        ">3</div>
                        <p style="color: #B8C5D3 !important; margin: 0;">Get quality result: <span style="color: #22C55E;">High</span>, <span style="color: #FBBF24;">Medium</span>, or <span style="color: #EF4444;">Low</span></p>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ─── FOOTER ───────────────────────────────────────────────────────────────────
        st.markdown("---")
        st.markdown(
            """
            <p style="text-align: center; color: #5A6A7A !important; font-size: 0.85rem;">
                © 2025 MilkQu • Built with Streamlit & ❤️
            </p>
            """,
            unsafe_allow_html=True,
        )

    elif menu == "Milkqu Prediction":
        # declare variable
        identity_value = current_url.get("identity", [""])[0]
        ph_value = safe_get_float(current_url, "pH")
        temprature_value = safe_get_int(current_url, "Temprature")
        taste_value = safe_get_int(current_url, "Taste")
        odor_value = safe_get_int(current_url, "Odor")
        fat = safe_get_int(current_url, "Fat ")
        turbidity = safe_get_int(current_url, "Turbidity")
        colour_value = safe_get_int(current_url, "Colour")

        prediction_result = ""
        default_milkqu_df = load_default_milk_data()
        clusters = init_model()

        # ─── PAGE HEADER ────────────────────────────────────────────────────────────────
        st.markdown(
            """
            <div style="
                text-align: center;
                padding: 40px 20px;
                background: linear-gradient(135deg, rgba(74, 174, 217, 0.1) 0%, rgba(125, 211, 252, 0.05) 100%);
                border-radius: 20px;
                border: 1px solid rgba(74, 174, 217, 0.2);
                margin-bottom: 30px;
            ">
                <div style="font-size: 3rem; margin-bottom: 16px;">🧪</div>
                <h1 style="
                    font-size: 2.5rem;
                    font-weight: 700;
                    background: linear-gradient(135deg, #4AAED9 0%, #7DD3FC 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    margin: 0;
                ">Milk Quality Prediction</h1>
                <p style="color: #B8C5D3 !important; font-size: 1.1rem; margin-top: 12px;">
                    Enter milk parameters to predict quality grade
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ─── PARAMETER REFERENCE ────────────────────────────────────────────────────────
        with st.expander("📋 Parameter Reference"):
            st.dataframe(default_milkqu_df, use_container_width=True)
            st.markdown(
                """
                <div style="
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 12px;
                    margin-top: 16px;
                ">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="color: #4AAED9;">•</span>
                        <span style="color: #B8C5D3; font-size: 0.9rem;"><strong>pH</strong> — Acidity level (6.0-7.0)</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="color: #4AAED9;">•</span>
                        <span style="color: #B8C5D3; font-size: 0.9rem;"><strong>Temperature</strong> — Milk temp in °C</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="color: #4AAED9;">•</span>
                        <span style="color: #B8C5D3; font-size: 0.9rem;"><strong>Taste</strong> — 1=Normal, 0=Abnormal</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="color: #4AAED9;">•</span>
                        <span style="color: #B8C5D3; font-size: 0.9rem;"><strong>Odor</strong> — 1=Fresh, 0=Spoiled</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="color: #4AAED9;">•</span>
                        <span style="color: #B8C5D3; font-size: 0.9rem;"><strong>Fat</strong> — Fat content level</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="color: #4AAED9;">•</span>
                        <span style="color: #B8C5D3; font-size: 0.9rem;"><strong>Turbidity</strong> — Cloudiness level</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="color: #4AAED9;">•</span>
                        <span style="color: #B8C5D3; font-size: 0.9rem;"><strong>Colour</strong> — Color index (240-260)</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # ─── PREDICTION FORM ────────────────────────────────────────────────────────────
        st.markdown(
            """
            <h2 style="
                color: #F5F5F5 !important;
                display: flex;
                align-items: center;
                gap: 12px;
                margin: 30px 0 20px 0;
            ">
                <span style="font-size: 1.5rem;">🔬</span> Enter Milk Parameters
            </h2>
            """,
            unsafe_allow_html=True,
        )

        # Form styling
        st.markdown(
            """
            <style>
            .stForm {
                background-color: #21262d;
                padding: 20px;
                border-radius: 10px;
                border: 1px solid #2c3854;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            .stForm > div {
                background-color: #21262d;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        with st.form(key="prediction_form"):

            identity = st.text_input("Your Name", value=identity_value, max_chars=100)
            ph = st.number_input("pH", value=ph_value, min_value=0.0, max_value=14.0, step=0.1, help="Acidity level (0-14, typical milk: 6.0-7.0)")
            temprature = st.number_input("Temperature (°C)", value=temprature_value, min_value=0, max_value=100, step=1, help="Milk temperature in Celsius")
            c1, c2 = st.columns(2)
            c3, c4 = st.columns(2)
            colour = st.number_input("Colour", value=colour_value, min_value=0, max_value=300, step=1, help="Color index (typical: 240-260)")

            with c1:
                taste = st.number_input("Taste", value=taste_value, min_value=0, max_value=1, step=1, help="1=Normal, 0=Abnormal")
            with c2:
                odor = st.number_input("Odor", value=odor_value, min_value=0, max_value=1, step=1, help="1=Fresh, 0=Spoiled")
            with c3:
                fat = st.number_input("Fat", value=fat, min_value=0, max_value=1, step=1, help="1=High, 0=Low")
            with c4:
                turbidity = st.number_input("Turbidity", value=turbidity, min_value=0, max_value=1, step=1, help="1=High, 0=Low")

            progress_text = "STATUS : IDLE"
            progress_bar = st.progress(0, text=progress_text)

            st.markdown(
                """
                <style>
                div[data-testid="stFormSubmitButton"] > button {
                    background-color: #2f80ed;
                    color: white;
                    border: none;
                    font-weight: bold;
                    padding: 0.6rem 1.5rem;
                    border-radius: 8px;
                    transition: all 0.3s ease;
                    width: 100%;
                }
                div[data-testid="stFormSubmitButton"] > button:hover {
                    background-color: #1c6fd1;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                }
                </style>
                """,
                unsafe_allow_html=True
            )
            
            delivered_results = st.form_submit_button("Predict Milk Quality", use_container_width=True)

            if delivered_results:
                # Validate inputs before processing
                validation_errors = []
                
                # Check name is not empty
                if not identity or identity.strip() == "":
                    validation_errors.append("Name is required")
                
                # Type-safe validation for numeric fields
                try:
                    if not isinstance(ph, (int, float)) or ph < 0:
                        validation_errors.append("pH must be a non-negative number")
                    if not isinstance(temprature, (int, float)) or temprature < 0:
                        validation_errors.append("Temperature must be a non-negative number")
                    if not isinstance(colour, (int, float)) or colour < 0:
                        validation_errors.append("Colour must be a non-negative number")
                    if taste not in [0, 1]:
                        validation_errors.append("Taste must be 0 or 1")
                    if odor not in [0, 1]:
                        validation_errors.append("Odor must be 0 or 1")
                    if fat not in [0, 1]:
                        validation_errors.append("Fat must be 0 or 1")
                    if turbidity not in [0, 1]:
                        validation_errors.append("Turbidity must be 0 or 1")
                except TypeError:
                    validation_errors.append("All fields must be valid numbers")
                
                if validation_errors:
                    for error in validation_errors:
                        st.error(f"❌ {error}")
                else:
                    st.session_state["milkqu_answer_state"] = identity.strip()

        # save result as state
        if "milkqu_answer_state" not in st.session_state:
            st.markdown(
                """
                <div style="
                    background: rgba(74, 174, 217, 0.1);
                    border-left: 4px solid #4AAED9;
                    color: #B8C5D3;
                    padding: 16px;
                    border-radius: 8px;
                    margin: 20px 0;
                ">
                    <p style="margin: 0; display: flex; align-items: center; gap: 8px;">
                        <span style="font-size: 1.2rem;">ℹ️</span>
                        Please fill all parameters above and click <strong>Predict Milk Quality</strong> to see the result!
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.markdown("---")
            st.markdown("<p style='text-align: center; color: #5A6A7A; font-size: 0.85rem;'>© 2025 MilkQu • Built with Streamlit</p>", unsafe_allow_html=True)

        # execute
        else:

            # handle error
            try:

                if delivered_results:
                    for percent_complete in range(100):
                        df_predict = load_milk_data(ph, temprature, taste, odor, fat, turbidity, colour)
                        encoded_df = load_encoded_milk_data(
                            ph,
                            temprature,
                            taste,
                            odor,
                            fat,
                            turbidity,
                            colour,
                            df_predict.columns,
                        )
                        predictions = clusters.predict(encoded_df)
                        if df_predict is not None and percent_complete == 20:
                            progress_bar.progress(percent_complete + 1, text="STATUS : GATHERING DATASET")
                            time.sleep(2)
                            st.dataframe(df_predict, use_container_width=True)
                        if encoded_df is not None and percent_complete == 40:
                            progress_bar.progress(percent_complete + 1, text="STATUS : PREPROCESSING DATA")
                            time.sleep(2)
                            st.dataframe(encoded_df, use_container_width=True)
                        if predictions is not None and percent_complete == 80:
                            progress_bar.progress(percent_complete + 1, text="STATUS : PREDICTING DATA")
                            time.sleep(2)
                            st.dataframe(predictions, use_container_width=True)
                    progress_bar.progress(percent_complete + 1, text="STATUS : PREDICTION COMPLETE")

                    prediction_label = {0: "High", 1: "Low", 2: "Medium"}
                    # history_prediction_label = {"High": "rocket", "Low": "walking", "Medium": "bicyclist"}

                    # conn.query("INSERT INTO histories VALUES ('Belly', 'rocket');")
                    # Perform query.

                    conn = st.connection("postgresql", type="sql")

                    with conn.session as session:
                        session.execute(
                            text("INSERT INTO histories (name, quality) VALUES (:name, :quality)"),
                            {
                                "name": identity,
                                "quality": prediction_label[int(predictions)],
                            },
                        )
                        session.commit()

                    # Enhanced success message
                    quality_colors = {"High": "#4CAF50", "Low": "#F44336", "Medium": "#FF9800"}
                    quality = prediction_label[int(predictions)]
                    st.markdown(
                        f"""
                        <div style="
                            background-color: #2c3854;
                            border-left: 4px solid {quality_colors[quality]};
                            padding: 15px;
                            border-radius: 5px;
                            margin: 20px 0;
                            animation: fadeIn 0.5s ease-in-out;
                        ">
                            <div style="font-size: 1.2rem; font-weight: bold; color: #d1ebfb;">
                                {identity}'s Milk Grade Is <span style="color: {quality_colors[quality]};">{quality}</span>
                            </div>
                        </div>
                        <style>
                            @keyframes fadeIn {{
                                from {{ opacity: 0; transform: translateY(10px); }}
                                to {{ opacity: 1; transform: translateY(0); }}
                            }}
                        </style>
                        """,
                        unsafe_allow_html=True
                    )

            except:
                print(st.error)
                st.error("Invalid parameters, please [follow](#milkqu-default-template) default template above !")

    elif menu == "Prediction History":

        # ─── PAGE HEADER ────────────────────────────────────────────────────────────────
        st.markdown(
            """
            <div style="
                text-align: center;
                padding: 40px 20px;
                background: linear-gradient(135deg, rgba(74, 174, 217, 0.1) 0%, rgba(125, 211, 252, 0.05) 100%);
                border-radius: 20px;
                border: 1px solid rgba(74, 174, 217, 0.2);
                margin-bottom: 30px;
            ">
                <div style="font-size: 3rem; margin-bottom: 16px;">📈</div>
                <h1 style="
                    font-size: 2.5rem;
                    font-weight: 700;
                    background: linear-gradient(135deg, #4AAED9 0%, #7DD3FC 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    margin: 0;
                ">Prediction History</h1>
                <p style="color: #B8C5D3 !important; font-size: 1.1rem; margin-top: 12px;">
                    View and analyze your milk quality predictions
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Color theme matching milk design
        PRIMARY_COLOR = "#4AAED9"
        SUCCESS_COLOR = "#22C55E"
        WARNING_COLOR = "#FBBF24"
        DANGER_COLOR = "#EF4444"

        # ─── DATABASE & DATAFRAME ────────────────────────────────────────────────────
        conn = st.connection("postgresql", type="sql")
        df = conn.query("SELECT name, quality AS grade FROM histories;", ttl=0)

        # ubah label jadi pakai ikon
        label_map = {"High": "🚀 High", "Medium": "🚴 Medium", "Low": "🚶 Low"}
        df["grade"] = df["grade"].map(label_map)

        # ─── SUMMARY METRICS ──────────────────────────────────────────────────────────
        total_pred = len(df)
        high_count = df["grade"].str.contains("High").sum()
        medium_count = df["grade"].str.contains("Medium").sum()
        low_count = df["grade"].str.contains("Low").sum()

        st.markdown("<div style='display: flex; gap: 15px;'>", unsafe_allow_html=True)

        metrics = [
            {
                "label": "Total Predictions",
                "value": total_pred,
                "color": PRIMARY_COLOR,
                "percentage": "",
            },
            {
                "label": "High 🚀",
                "value": high_count,
                "color": SUCCESS_COLOR,
                "percentage": f"{high_count/total_pred:.0%}" if total_pred > 0 else "0%",
            },
            {
                "label": "Medium 🚴",
                "value": medium_count,
                "color": WARNING_COLOR,
                "percentage": f"{medium_count/total_pred:.0%}" if total_pred > 0 else "0%",
            },
            {
                "label": "Low 🚶",
                "value": low_count,
                "color": DANGER_COLOR,
                "percentage": f"{low_count/total_pred:.0%}" if total_pred > 0 else "0%",
            },
        ]

        col1, col2, col3, col4 = st.columns(4)
        cols = [col1, col2, col3, col4]

        for i, (col, metric) in enumerate(zip(cols, metrics)):
            with col:
                st.markdown(
                    f"""
                    <div class="metric-card" style="border-left: 5px solid {metric['color']}">
                        <div class="metric-value" style="color: {metric['color']}">{metric['value']}</div>
                        <div class="metric-label">{metric['label']}</div>
                        <div style="color: {metric['color']}; font-size: 12px; font-weight: bold; margin-top: 5px;">{metric['percentage']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        # ─── DISTRIBUTION CHART ───────────────────────────────────────────────────────
        st.markdown("""
            <h3 style="color: #d1ebfb; margin-top: 30px; font-family: 'Segoe UI', sans-serif;">
                📊 Grade Distribution
            </h3>
            """, 
            unsafe_allow_html=True
        )
        
        # Apply custom chart theme for dark mode
        st.markdown("""
            <style>
                div[data-testid="stVegaLiteChart"] > div > div > div > svg {
                    background-color: #21262d !important;
                }
                div[data-testid="stVegaLiteChart"] .vega-embed .marks .role-axis-title text {
                    fill: #94c2e8 !important;
                }
                div[data-testid="stVegaLiteChart"] .vega-embed .marks .role-axis-label text {
                    fill: #d1ebfb !important;
                }
                div[data-testid="stVegaLiteChart"] .vega-embed .marks .role-axis-domain path {
                    stroke: #4a6284 !important;
                }
                div[data-testid="stVegaLiteChart"] .vega-embed .marks .role-axis-tick line {
                    stroke: #4a6284 !important;
                }
            </style>
        """, unsafe_allow_html=True)
        
        dist = df["grade"].value_counts()
        st.bar_chart(dist)

        # ─── FILTER PANEL ─────────────────────────────────────────────────────────────
        st.markdown("""
            <style>
                .streamlit-expanderHeader {
                    background-color: #2c3854 !important;
                    color: #d1ebfb !important;
                    border-radius: 8px !important;
                    padding: 10px !important;
                    font-weight: 500 !important;
                }
                .streamlit-expanderContent {
                    background-color: #21262d !important;
                    border: 1px solid #2c3854 !important;
                    border-top: none !important;
                    border-radius: 0 0 8px 8px !important;
                    padding: 15px !important;
                }
            </style>
        """, unsafe_allow_html=True)
        
        with st.expander("🔍 Filter & Search", expanded=True):
            with st.form("filter_form"):
                selected_grades = st.multiselect(
                    "Pilih Grade",
                    options=df["grade"].unique(),
                    default=df["grade"].unique(),
                )
                name_query = st.text_input("Cari berdasarkan Nama")
                
                # Style the search button
                st.markdown("""
                    <style>
                    div[data-testid="stFormSubmitButton"] > button {
                        background-color: #2f80ed;
                        color: white;
                        border: none;
                        font-weight: 500;
                        padding: 0.5rem 1rem;
                        border-radius: 8px;
                        transition: all 0.3s ease;
                    }
                    div[data-testid="stFormSubmitButton"] > button:hover {
                        background-color: #1c6fd1;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )
                
                cari = st.form_submit_button("🔍 Cari")

            if cari:
                mask = df["grade"].isin(selected_grades)
                if name_query:
                    mask &= df["name"].str.contains(name_query, case=False)
                df_filtered = df[mask]
            else:
                df_filtered = df.copy()

        # ─── FILTERED RESULTS ─────────────────────────────────────────────────────────
        st.markdown("""
            <h3 style="color: #d1ebfb; margin-top: 30px; font-family: 'Segoe UI', sans-serif;">
                📋 Hasil Filter
            </h3>
            """, 
            unsafe_allow_html=True
        )
        
        # Style for empty results
        if len(df_filtered) == 0:
            st.markdown("""
                <div style="
                    background-color: #2c3854;
                    border-left: 4px solid #5d9df5;
                    color: #d1ebfb;
                    padding: 15px;
                    border-radius: 5px;
                    margin: 20px 0;
                    text-align: center;
                ">
                    <i>Tidak ada data yang sesuai dengan filter yang dipilih</i>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.dataframe(
                df_filtered,
                use_container_width=True,
            )

        # ─── DOWNLOAD BUTTON ──────────────────────────────────────────────────────────
        csv = df_filtered.to_csv(index=False).encode("utf-8")
        
        st.download_button(
            label="⬇️ Download CSV",
            data=csv,
            file_name="milkqu_prediction_history.csv",
            mime="text/csv",
        )
        
        st.markdown("<hr style='border: 1px solid #2c3854; margin-top: 30px;'>", unsafe_allow_html=True)
        st.caption("© 2025 MilkQu • built with Streamlit")
