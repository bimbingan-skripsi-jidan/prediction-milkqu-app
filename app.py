import streamlit as st
import pandas as pd
import time
import pickle
from streamlit_option_menu import option_menu
from streamlit.components.v1 import html
from sqlalchemy import text

# --- Streamlit Page Config ---
st.set_page_config(
    page_title="Milkqu - Predict Milk Quality",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="auto",
)


def main():

    # def login_screen():
    st.markdown(
        "<div style='text-align: center; font-size: 3.5rem; font-weight: bold; color: white; text-shadow: -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000, -2px 0 0 #000, 2px 0 0 #000, 0 -2px 0 #000, 0 2px 0 #000;'>👋 Welcome to MilkQu</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align: center; color: #D1EBFB;'>Predict your milk quality easily with AI</p>",
        unsafe_allow_html=True,
    )
    # st.header("This app is private.")

    st.markdown("---")

    # Centered Image
    st.markdown(
        """
        <div style="
            display: flex; 
            justify-content: center; 
            margin: 30px auto;
            position: relative;
            max-width: 550px;
        ">
            <img src="https://raw.githubusercontent.com/jidan24/asset/refs/heads/master/milk-%230e1117.jpg"  alt="logo Milkqu login"
                style="
                    width: 100%;
                    border-radius: 12px;
                    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
                    transition: transform 0.3s ease, box-shadow 0.3s ease;
                "
                onmouseover="this.style.transform='scale(1.02)'; this.style.boxShadow='0 15px 40px rgba(0, 0, 0, 0.3)';"
                onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='0 10px 30px rgba(0, 0, 0, 0.25)';"
            >
        </div>
        
        <style>
            @media (max-width: 768px) {
                img {
                    width: 90% !important;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Styling dan UI login MilkQu
    st.markdown(
        """
    <style>
    /* Body style */
    body {
        background-color: #1a1a1a;
        color: #d1ebfb;
        font-family: 'Segoe UI', Arial, sans-serif;
    }
    
    /* Button style */
    .stButton>button {
        background-color: #2c3854;
        color: #d1ebfb;
        border: 1px solid #4a6284;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-size: 1rem;
        font-weight: 500;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        width: auto;
        min-width: 200px;
    }

    .stButton>button:hover {
        background-color: #3d4e70;
        border-color: #5d7eaf;
        color: #ffffff;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
    }
    
    .stButton>button:active {
        transform: translateY(1px);
        box-shadow: 0 2px 2px rgba(0, 0, 0, 0.3);
    }

    .stButton {
        display: flex;
        justify-content: center;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    /* Streamlit base element styling */
    .css-1d391kg, .css-12oz5g7 {
        background-color: #1e1e1e;
    }
    
    .stTextInput > div > div > input {
        background-color: #2d2d2d;
        color: #d1ebfb;
        border-color: #4a6284;
    }
    
    .stNumberInput > div > div > input {
        background-color: #2d2d2d;
        color: #d1ebfb;
        border-color: #4a6284;
    }
    
    .stSelectbox > div > div > div {
        background-color: #2d2d2d;
        color: #d1ebfb;
    }
    
    .stDataFrame {
        background-color: #2d2d2d;
    }
    
    /* Make sure links are visible in dark mode */
    a {
        color: #5d9df5 !important;
    }
    
    a:hover {
        color: #8ab6f9 !important;
    }
    
    /* Fix for expandable sections in dark mode */
    .streamlit-expanderHeader {
        background-color: #2c3854;
        color: #d1ebfb !important;
        border-radius: 5px;
    }
    
    .streamlit-expanderContent {
        background-color: #1a1a1a;
        border: 1px solid #2c3854;
        border-top: none;
        border-radius: 0 0 5px 5px;
    }
    </style>
""",
        unsafe_allow_html=True,
    )

    st.button("Log in with Google", on_click=st.login)
    st.markdown("<hr style='border: 1px solid #2c3854;'>", unsafe_allow_html=True)


# --- Apply style & script configurations ---
style_configurations = """
<style>
    /* Streamlit dark mode enhancements */
    .stApp {
        background-color: #121212;
    }
    
    .main .block-container {
        background-color: #1a1a1a;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    h1, h2, h3, h4, h5 {
        color: #d1ebfb !important;
    }
    
    p, li, span, label {
        color: #c9d1d9 !important;
    }
    
    code {
        background-color: #2d333b !important;
        color: #d1ebfb !important;
        padding: 2px 5px;
        border-radius: 3px;
    }
    
    pre {
        background-color: #2d333b !important;
        border-radius: 8px;
        padding: 10px;
        border: 1px solid #444c56;
    }
    
    .css-1kyxreq {
        background-color: #21262d !important;
    }
    
    /* Progress bar customization */
    .stProgress > div > div {
        background-color: #5d9df5 !important;
    }
    
    /* Info box styling */
    .stAlert {
        background-color: #2c3854 !important;
        color: #d1ebfb !important;
        border-color: #4a6284 !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg, .css-12oz5g7 {
        background-color: #1e1e1e;
    }
    
    .sidebar .sidebar-content {
        background-color: #1e1e1e;
    }
    
    .sidebar .block-container {
        background-color: #141414;
    }
    
    /* Custom divider */
    hr {
        border-color: #2c3854 !important;
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


# Function for parcing
def safe_get_float(source, key, default=0.0):
    try:
        return float(source.get(key, [default])[0])
    except ValueError:
        return default


def safe_get_int(source, key, default=0):
    try:
        return int(source.get(key, [default])[0])
    except ValueError:
        return default


# --- Declare global variables ---
current_url = st.query_params.to_dict()
direct_menu = int(current_url["redirect"][0]) if "redirect" in current_url else 0

tilt_effect = """
<div class="contaienr">
    <img src="https://raw.githubusercontent.com/jidan24/asset/refs/heads/master/milk-%230e1117.jpg" alt="Milkqu Header" style="width: 100%;"/>
</div>
<br/>
"""

# Helper function to check if user is logged in
def is_user_logged_in():
    """Check if user is logged in, with fallback for different Streamlit versions/environments."""
    try:
        # Try the new attribute first (Streamlit Community Cloud)
        if hasattr(st.experimental_user, 'is_logged_in'):
            return st.experimental_user.is_logged_in
        # Fallback: check if user has an email (indicates logged in)
        if hasattr(st.experimental_user, 'email') and st.experimental_user.email:
            return True
        return False
    except Exception:
        return False

# CORE
if not is_user_logged_in():
    main()
else:

    # --- Sidebar ---
    with st.sidebar:
        # st.success(f"👋 Welcome {st.session_state.user_info['name']}")
        st.markdown("---")
        # st.caption(f"📧 {st.session_state.user_info['email']}")
        st.markdown(tilt_effect, unsafe_allow_html=True)

        # --- Menu ---
        menu = option_menu(
            None,
            ["Documentations", "Milkqu Prediction", "Prediction History"],
            icons=["journal-text", "ui-checks", "receipt", "clock-history"],
            default_index=int(direct_menu),
            styles={
                "container": {"background-color": "#1e1e1e", "padding": "10px", "border-radius": "8px"},
                "icon": {"color": "#8ab6f9", "font-size": "18px"},
                "nav-link": {"color": "#d1ebfb", "font-size": "16px", "text-align": "left", "margin": "0px", "padding": "10px"},
                "nav-link-selected": {"background-color": "#2c3854", "color": "#ffffff", "font-weight": "bold"},
            }
        )

        # github and dataset button
        st.write(
            """
        <style>
        .custom-button {
            background-color: #2c3854;
            color: #d1ebfb;
            border: 1px solid #4a6284;
            width: 100%;
            height: 40px;
            border-radius: 8px;
            font-family: 'Segoe UI', Helvetica, Arial, sans-serif;
            font-size: 14px;
            text-align: left;
            padding-left: 10px;
            cursor: pointer;
            margin-bottom: 10px;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .custom-button:hover {
            background-color: #3d4e70;
            border-color: #5d7eaf;
            color: #ffffff;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        }
        .button-icon {
            width: 18px;
            height: 18px;
            display: inline-block;
        }
        </style>

        <div style='margin-top: 10px; margin-bottom: 25px;'>
        <a href="https://github.com/bimbingan-skripsi-jidan/prediction-milkqu" target="_blank">
            <button class="custom-button">
                <svg class="button-icon" viewBox="0 0 24 24" fill="#d1ebfb">
                    <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405 1.02 0 2.04.135 3 .405 2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z"/>
                </svg>
                GitHub Repository
            </button>
        </a>
        <a href="https://www.kaggle.com/datasets/jidanhaviarsaviola/milk-quality" target="_blank">
            <button class="custom-button">
                <svg class="button-icon" viewBox="0 0 24 24" fill="#d1ebfb">
                    <path d="M17.872 9.01c1.304-1.293 2.835-1.293 3.543-.578c.717.717.777 2.24-.527 3.544l-5.673 5.67c-1.304 1.304-2.835 1.304-3.543.588c-.78-.78-.72-2.24.585-3.544l1.304-1.304c-.15-.4-.277-.806-.335-1.224l-1.996 1.995c-1.756 1.754-1.756 4.2-.02 5.94c1.754 1.753 4.192 1.753 5.95-.02l5.67-5.674c1.756-1.755 1.756-4.192.03-5.94c-1.757-1.758-4.218-1.758-5.982-.01l-.2.208c.478.732.717 1.6.766 2.468l.717-.717zm-11.74 5.95c-1.303 1.303-2.835 1.303-3.552.585c-.717-.717-.777-2.248.526-3.545l5.673-5.67c1.304-1.304 2.835-1.304 3.543-.585c.772.78.712 2.234-.594 3.545l-1.304 1.304c.15.4.278.807.337 1.225l1.994-1.995c1.756-1.756 1.756-4.2.02-5.94c-1.754-1.754-4.192-1.754-5.948.02l-5.673 5.674c-1.754 1.755-1.754 4.192-.02 5.938c1.754 1.753 4.215 1.753 5.95.01l.21-.21c-.478-.72-.716-1.6-.766-2.467l-.697.706z"/>
                </svg>
                Explore Dataset
            </button>
        </a>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.button("Log out", on_click=st.logout)
        st.markdown("<hr style='border: 1px solid #2c3854;'>", unsafe_allow_html=True)
        user_name = getattr(st.experimental_user, 'name', None) or getattr(st.experimental_user, 'email', 'User')
        st.success(f"Welcome to MilkQu App, {user_name}!")

    if menu == "Documentations":

        # declare variable
        st.markdown(
            """
            <style>
                .stApp > header {visibility: hidden;}
                .title {font-family: 'Segoe UI', sans-serif; color: #d1ebfb;}
                .section-title {color: #94c2e8; margin-top: 30px; margin-bottom: 10px;}
                .info-box {background-color: #2c3854; padding: 15px; border-radius: 8px; border-left: 4px solid #5d9df5; color: #d1ebfb;}
                .code-box {background-color: #2d333b; padding: 15px; border-radius: 8px; color: #d1ebfb; font-family: monospace;}
            </style>
            """,
            unsafe_allow_html=True,
        )

        # ─── PAGE TITLE ────────────────────────────────────────────────────────────────
        st.markdown(
            """
            <div style='display: flex; align-items: center; gap: 10px;'>
                <img src='https://raw.githubusercontent.com/jidan24/asset/refs/heads/master/logo-milk.png' alt='MilkQu Logo' width='40'/>
                <h1 style='margin: 0;' class='title'>MilkQu Docs</h1>
            </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown("<hr style='border: 1px solid #2c3854;'>", unsafe_allow_html=True)

        # ─── WHAT IS MILKQU? ───────────────────────────────────────────────────────────
        st.markdown("<h2 class='section-title'>🥛 What is MilkQu?</h2>", unsafe_allow_html=True)
        st.info("""
            MilkQu (Milk Quality) adalah web app berbasis machine learning
            untuk mengklasifikasikan kualitas susu berdasarkan beberapa parameter seperti:
            keasaman, suhu, kejernihan, bau, kandungan lemak, tingkat keruh, dan warna.
            Dataset diambil dari Kaggle untuk memahami karakteristik fisika & kimia susu.Melalui antarmuka yang intuitif dan dapat mengunduh laporan prediksi history dengan format CSV, atau langsung mengekspor dataset ke format CSV untuk analisis lebih dalam. Model kami dilatih menggunakan Milk Quality Dataset dari Kaggle memberikan jaminan bahwa setiap prediksi lahir dari data real beragam kondisi susu.Dengan MilkQu, analisis kualitas susu menjadi lebih efisien, terpercaya, dan mudah diakses di mana saja—cukup buka browser, unggah data, dan biarkan algoritma cerdas kami bekerja untuk Anda!
            """)

        # ─── ABOUT DATASETS ────────────────────────────────────────────────────────────
        st.markdown("<h2 class='section-title'>📊 About Datasets</h2>", unsafe_allow_html=True)
        with st.expander("Detail Dataset (Kaggle: Milk Quality Dataset)"):
            st.markdown("""
                - **Jumlah baris:** 1000+  
                - **Fitur utama:** pH, Temperature, Taste, Odor, Fat, Turbidity, Colour and Grade  
                """)

        # ─── HOW MILKQU WORKS ──────────────────────────────────────────────────────────
        st.markdown("<h2 class='section-title'>⚙️ How MilkQu Works</h2>", unsafe_allow_html=True)
        st.markdown("""
            1. User mengunggah data parameter susu  
            2. Model ML melakukan prediksi kualitas  
            3. Hasil ditampilkan sebagai **High**, **Medium**, atau **Low**
            """)
        code = '''def predict():
        """
        this is code
        for processing
        the machine learning
        """
        print(f"your milk quality is {predict_result}")'''
        st.code(code, language="python")

        # ─── FOOTER ───────────────────────────────────────────────────────────────────
        st.markdown("<hr style='border: 1px solid #2c3854;'>", unsafe_allow_html=True)
        st.caption("© 2025 MilkQu • built with Streamlit")

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

        # sub header and caption
        st.markdown("<h2 style='color: #d1ebfb;'>Milkqu Example Template</h2>", unsafe_allow_html=True)
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

        st.markdown(
            """
            <style>
            .dataframe {
                background-color: #2d333b !important;
                color: #d1ebfb !important;
                border: 1px solid #444c56 !important;
            }
            .dataframe th {
                background-color: #2c3854 !important;
                color: #ffffff !important;
                font-weight: bold !important;
                padding: 8px !important;
            }
            .dataframe td {
                background-color: #21262d !important;
                color: #d1ebfb !important;
                padding: 8px !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        
        st.dataframe(default_milkqu_df, use_container_width=True)

        # Parameter descriptions with improved styling
        st.markdown(
            """
            <style>
            .param-description {
                color: #94c2e8; 
                margin: 3px 0;
                font-size: 0.9rem;
            }
            </style>
            """, 
            unsafe_allow_html=True
        )

        st.markdown("<div class='param-description'>pH = Mengukur tingkat keasaman susu, yang bisa mempengaruhi kesegarannya.</div>", unsafe_allow_html=True)
        st.markdown("<div class='param-description'>Temperature = Suhu susu saat diukur, yang berpengaruh terhadap pertumbuhan bakteri.</div>", unsafe_allow_html=True)
        st.markdown("<div class='param-description'>Taste = Apakah susu terasa normal atau asam.</div>", unsafe_allow_html=True)
        st.markdown("<div class='param-description'>Odor = Bau susu, apakah masih segar atau sudah menunjukkan tanda-tanda pembusukan.</div>", unsafe_allow_html=True)
        st.markdown("<div class='param-description'>Fat = Kandungan lemak dalam susu.</div>", unsafe_allow_html=True)
        st.markdown("<div class='param-description'>Turbidity = Seberapa keruh susu tersebut.</div>", unsafe_allow_html=True)
        st.markdown("<div class='param-description'>Colour = Warna susu yang bisa menunjukkan perubahan kualitas.</div>", unsafe_allow_html=True)
        st.markdown("<div class='param-description'>Grade = Label hasil kualitas susu berdasarkan fitur-fitur di atas (high, medium, low).</div>", unsafe_allow_html=True)

        # category one : predict milkqu answer
        st.markdown("<h2 style='color: #d1ebfb; margin-top: 20px;'>Milk Quality Prediction</h2>", unsafe_allow_html=True)

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

            identity = st.text_input("Your Name", value=identity_value)
            ph = st.number_input("pH", value=ph_value)
            temprature = st.number_input("Temprature", value=temprature_value)
            c1, c2 = st.columns(2)
            c3, c4 = st.columns(2)
            colour = st.number_input("Colour", value=colour_value)

            with c1:
                taste = st.number_input("Taste", value=taste_value)
            with c2:
                odor = st.number_input("Odor", value=odor_value)
            with c3:
                fat = st.number_input("Fat ", value=fat)
            with c4:
                turbidity = st.number_input("Turbidity", value=turbidity)

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
                st.session_state["milkqu_answer_state"] = identity

        # save result as state
        if "milkqu_answer_state" not in st.session_state:
            st.markdown(
                """
                <div style="
                    background-color: #2c3854;
                    border-left: 4px solid #5d9df5;
                    color: #d1ebfb;
                    padding: 15px;
                    border-radius: 5px;
                    margin: 20px 0;
                ">
                    <i>ℹ️ Please fill parameters above and submit predict to see the result!</i>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.caption("© 2025 MilkQu • built with Streamlit")

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

        # Warna tema utama untuk dark mode
        PRIMARY_COLOR = "#2F80ED"
        SUCCESS_COLOR = "#4CAF50"
        WARNING_COLOR = "#FF9800"
        DANGER_COLOR = "#F44336"

        st.markdown(
            f"""
                <style>
            .metric-card {{
                background-color: #2d333b;
                border-radius: 10px;
                padding: 15px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.2);
                margin-bottom: 15px;
                border-left: 5px solid {PRIMARY_COLOR};
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }}
            .metric-card:hover {{
                transform: translateY(-3px);
                box-shadow: 0 6px 10px rgba(0,0,0,0.3);
            }}
            .metric-value {{
                font-size: 28px;
                font-weight: bold;
                color: {PRIMARY_COLOR};
                text-shadow: 0 1px 2px rgba(0,0,0,0.2);
            }}
            .metric-label {{
                font-size: 14px;
                color: #94c2e8;
                margin-top: 5px;
            }}
            
            /* Chart styling */
            div[data-testid="stVegaLiteChart"] {{
                background-color: #21262d;
                border-radius: 10px;
                padding: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}
            
            /* Table styling */
            .stDataFrame > div > div > div {{
                background-color: #21262d !important;
            }}
            
            .stDataFrame th {{
                background-color: #2c3854 !important;
                color: #d1ebfb !important;
            }}
            
            .stDataFrame td {{
                background-color: #1e1e1e !important;
                color: #d1ebfb !important;
            }}
            
            /* Download button styling */
            div[data-testid="stDownloadButton"] > button {{
                background-color: #2f80ed;
                color: white;
                border: none;
                font-weight: bold;
                padding: 0.5rem 1rem;
                border-radius: 8px;
                transition: all 0.3s ease;
            }}
            
            div[data-testid="stDownloadButton"] > button:hover {{
                background-color: #1c6fd1;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div style="text-align: center; padding: 10px 0;">
                <h1 style="margin: 0; font-family: 'Segoe UI', sans-serif; color: #d1ebfb; text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);">
                    📈 Milk Quality History Prediction
                </h1>
                <p style="color: #94c2e8; font-size: 16px; margin-top: 10px;">
                    Ringkasan riwayat prediksi kualitas.
                    Gunakan filter untuk menelusuri data lebih detail!
                </p>
            </div>
            <hr style="border: 1px solid #2c3854; margin: 15px 0;">
            """,
            unsafe_allow_html=True,
        )

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
