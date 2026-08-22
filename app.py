import streamlit as st
from streamlit_option_menu import option_menu
import sqlite3
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from dotenv import load_dotenv
from supabase import create_client
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
import base64
import mimetypes
import re


# ---------------- PAGE SETTING ----------------
if "name" not in st.session_state:
    st.session_state.name = ""
st.set_page_config(
    page_title="SmartHome AI",
    page_icon="🏠",
    layout="wide"
)
st.markdown("""
<style>
/* ===== MODERN SMART HOME UI ===== */
.stApp {
    background:
        radial-gradient(circle at 8% 5%, rgba(56,189,248,.14), transparent 25%),
        radial-gradient(circle at 92% 8%, rgba(139,92,246,.14), transparent 28%),
        linear-gradient(135deg, #04101d 0%, #071b2e 50%, #092640 100%);
    color: #f8fbff;
}

[data-testid="stHeader"] { background: transparent; }
[data-testid="stDecoration"] { display: none; }

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1,h2,h3,h4 {
    color: #fff !important;
    font-weight: 850 !important;
}
p,label,.stMarkdown { color:#dcecff; }
html,body,[class*="css"] { font-size:15px; }

/* ===== SIDEBAR ===== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#03101e,#071b2f 55%,#092846) !important;
    border-right:1px solid rgba(56,189,248,.22);
}
[data-testid="stSidebar"] * { color:#f5f9ff; }

[data-testid="stSidebar"] div[role="radiogroup"] {
    background:transparent !important;
    padding:6px !important;
}

[data-testid="stSidebar"] div[role="radiogroup"] label {
    background:rgba(16,48,76,.55) !important;
    border:1px solid rgba(77,166,255,.13);
    border-radius:13px;
    padding:11px 13px;
    margin-bottom:7px;
    transition:.18s ease;
}

[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background:rgba(28,77,115,.9) !important;
    border-color:#38bdf8;
    transform:translateX(3px);
}

[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
    background:linear-gradient(100deg,#0879d1,#6941d9) !important;
    border:1px solid rgba(125,211,252,.8);
    box-shadow:0 8px 25px rgba(18,100,216,.3);
}

[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p {
    color:white !important;
    font-weight:800;
}

/* ===== CARDS ===== */
.sh-card {
    background:linear-gradient(145deg,rgba(16,54,84,.88),rgba(7,28,48,.94));
    border:1px solid rgba(77,166,255,.20);
    border-radius:20px;
    padding:20px;
    margin:5px 0 15px;
    box-shadow:0 14px 34px rgba(0,0,0,.22);
    transition:.18s ease;
}
.sh-card:hover {
    transform:translateY(-2px);
    border-color:rgba(56,189,248,.5);
    box-shadow:0 18px 40px rgba(0,0,0,.3);
}

.sh-pill {
    display:inline-block;
    padding:5px 10px;
    border-radius:999px;
    background:rgba(56,189,248,.1);
    border:1px solid rgba(56,189,248,.25);
    color:#bfefff;
    font-size:11px;
    font-weight:800;
    letter-spacing:.6px;
}
.sh-muted { color:#9fc5df; font-size:13px; }
.sh-number { font-size:30px; font-weight:850; color:#fff; }

.sh-hero {
    background:
        linear-gradient(120deg,rgba(18,100,216,.30),rgba(113,56,213,.20)),
        rgba(7,25,43,.94);
    border:1px solid rgba(125,211,252,.25);
    border-radius:20px;
    padding:22px 26px;
    margin-bottom:17px;
    box-shadow:0 14px 32px rgba(0,0,0,.22);
}
.sh-hero-title {
    font-size:27px;
    line-height:1.18;
    font-weight:850;
    color:#fff;
    margin:8px 0 4px;
}
.sh-hero-sub {
    color:#b9d8ed;
    font-size:14px;
    max-width:820px;
}
.sh-hero .sh-pill {
    padding:4px 9px;
    font-size:10px;
}
.sh-section { font-size:21px; font-weight:850; margin:18px 0 11px; color:#fff; }
.dash-chart-card {
    min-height:118px;
    padding:17px 19px;
    border-radius:19px;
    background:linear-gradient(135deg,rgba(20,86,135,.90),rgba(8,31,53,.96));
    border:1px solid rgba(83,183,255,.26);
    box-shadow:0 12px 30px rgba(0,0,0,.20);
    margin:4px 0 10px;
}
.dash-chart-title {
    font-size:19px;
    font-weight:850;
    color:#fff;
    margin:8px 0 4px;
}
.dash-chart-sub {
    font-size:12.5px;
    color:#a9cee5;
}
.dash-chart-icon {
    font-size:17px;
    margin-right:6px;
}


/* ===== METRICS ===== */
[data-testid="stMetric"] {
    background:linear-gradient(145deg,rgba(17,57,89,.94),rgba(9,31,52,.92));
    border:1px solid rgba(77,166,255,.23);
    padding:18px 19px;
    border-radius:18px;
    box-shadow:0 14px 35px rgba(0,0,0,.22);
    transition:.18s ease;
}
[data-testid="stMetric"]:hover {
    transform:translateY(-4px);
    border-color:rgba(56,189,248,.7);
}
[data-testid="stMetricLabel"] { color:#bfe5ff !important; }
[data-testid="stMetricValue"] { color:#fff !important; font-weight:850; }

/* ===== INPUTS / BUTTONS ===== */
.stTextInput input,.stNumberInput input,.stDateInput input,.stTextArea textarea {
    background:rgba(10,35,59,.94) !important;
    color:#fff !important;
    border:1px solid rgba(77,166,255,.3) !important;
    border-radius:12px !important;
}
[data-baseweb="select"] > div {
    background:rgba(10,35,59,.94) !important;
    color:#fff !important;
    border-color:rgba(77,166,255,.3) !important;
    border-radius:12px !important;
}
.stButton > button {
    background:linear-gradient(100deg,#0879d1,#6941d9);
    color:white;
    border:1px solid rgba(125,211,252,.22);
    border-radius:12px;
    font-weight:750;
    padding:9px 18px;
    box-shadow:0 8px 20px rgba(18,100,216,.2);
    transition:.18s ease;
}
.stButton > button:hover {
    transform:translateY(-2px);
    border-color:#5bd2ff;
}

/* ===== TABLES / ALERTS / UPLOADS ===== */
[data-testid="stDataFrame"] {
    border:1px solid rgba(77,166,255,.22);
    border-radius:15px;
    overflow:hidden;
    box-shadow:0 12px 28px rgba(0,0,0,.18);
}
[data-testid="stAlert"] { border-radius:14px; }
[data-testid="stFileUploader"] {
    background:rgba(10,35,59,.62);
    border:1px dashed rgba(56,189,248,.45);
    border-radius:16px;
    padding:9px;
}
[data-testid="stExpander"] {
    background:rgba(9,31,52,.55);
    border:1px solid rgba(77,166,255,.18);
    border-radius:15px;
}
hr { border-color:rgba(56,189,248,.18); }

.sh-ai-card {
    background:linear-gradient(145deg,rgba(17,55,88,.96),rgba(12,34,58,.96));
    border:1px solid rgba(77,166,255,.24);
    border-radius:18px;
    padding:18px;
    margin:8px 0 14px;
    min-height:145px;
}
.sh-ai-title { font-size:18px; font-weight:800; color:#fff; }
.sh-ai-help { font-size:14px; color:#b9d8ed; line-height:1.55; }
.sh-ai-badge {
    display:inline-block;
    font-size:11px;
    font-weight:800;
    color:#bfefff;
    background:rgba(56,189,248,.1);
    border:1px solid rgba(56,189,248,.24);
    border-radius:999px;
    padding:4px 8px;
    margin-bottom:8px;
}
.sh-doc-card {
    background:linear-gradient(145deg,rgba(15,45,74,.94),rgba(9,29,50,.94));
    border:1px solid rgba(77,166,255,.22);
    border-radius:16px;
    padding:15px 17px;
    margin:8px 0;
}
.sh-doc-name { font-size:16px; font-weight:800; color:#fff; }
.sh-doc-meta { font-size:13px; color:#9fc5df; margin-top:4px; }

.sh-footer {
    text-align:center;
    color:#7fa7c3;
    font-size:12px;
    margin-top:30px;
    padding-top:16px;
    border-top:1px solid rgba(56,189,248,.12);
}

</style>
""", unsafe_allow_html=True)


# ---------------- SIMPLE FILE UPLOAD ----------------

def get_user_upload_folder():
    # Each logged-in user gets a separate document folder.
    safe_email = re.sub(r"[^a-zA-Z0-9_.-]", "_", st.session_state.email)
    folder = os.path.join("uploads", safe_email)
    os.makedirs(folder, exist_ok=True)
    return folder


def save_file(file):
    folder = get_user_upload_folder()
    path = os.path.join(folder, file.name)

    with open(path, "wb") as f:
        f.write(file.getbuffer())

    return path

# ---------------- DATABASE ----------------

# ---------------- DATABASE PATH ----------------
# Keep the database inside the database folder.
# If an existing SmartHome.db/smarthome.db is present, use it.
os.makedirs("database", exist_ok=True)

if os.path.exists(os.path.join("database", "SmartHome.db")):
    DB_PATH = os.path.join("database", "SmartHome.db")
elif os.path.exists(os.path.join("database", "smarthome.db")):
    DB_PATH = os.path.join("database", "smarthome.db")
else:
    DB_PATH = os.path.join("database", "smarthome.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Users(
    Name TEXT,
    Email TEXT,
    Password TEXT
)
""")
# Grocery Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Grocery(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Item TEXT,
    Quantity INTEGER,
    Price REAL,
    Category TEXT,
    Status TEXT
)
""")
conn.commit()

# Medicine Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Medicines(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Medicine TEXT,
    Quantity INTEGER,
    Expiry_Date TEXT,
    Purpose TEXT,
    Status TEXT
)
""")
conn.commit()

# Document Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Documents(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Document_Name TEXT,
    Document_Number TEXT,
    Expiry_Date TEXT,
    Status TEXT
)
""")
conn.commit()
# Bills Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Bills(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Bill_Type TEXT,
    Amount REAL,
    Due_Date TEXT,
    Status TEXT
)
""")
conn.commit()
# Expense Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Expenses(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Expense_Name TEXT,
    Category TEXT,
    Amount REAL,
    Date TEXT
)
""")
conn.commit()
# ---------------- USER DATA SUPPORT ----------------

tables = ["Grocery", "Medicines", "Documents", "Bills", "Expenses"]

for table in tables:
    try:
        cursor.execute(
            f"ALTER TABLE {table} ADD COLUMN User_Email TEXT"
        )
    except:
        pass

conn.commit()
# ---------------- LOGIN SESSION ----------------
if "monthly_budget" not in st.session_state:
    st.session_state.monthly_budget = 20000

if "login" not in st.session_state:
    st.session_state.login = False
if "email" not in st.session_state:
    st.session_state.email = ""
# ---------------- LOGIN / SIGNUP ----------------

if st.session_state.login == False:

    st.title("🏠 SmartHome AI")
    st.subheader("AI-Powered Intelligent Home Management System")

    choice = st.radio(
        "Select",
        ["Login", "Sign Up"],
        horizontal=True
    )


    # LOGIN

    if choice == "Login":

        st.subheader("🔐 Login")

        email = st.text_input("Enter Email")

        password = st.text_input(
            "Enter Password",
            type="password"
        )

        if st.button("Login"):

            cursor.execute(
                "SELECT * FROM Users WHERE Email=? AND Password=?",
                (email, password)
            )

            user = cursor.fetchone()

            if user:

                st.session_state.login = True
                st.session_state.name = user[0]
                st.session_state.email = user[1]

                st.rerun()
            else:

                st.error("❌ Invalid Email or Password")


    # SIGN UP

    if choice == "Sign Up":

        st.subheader("📝 Create Account")

        name = st.text_input("Enter Full Name")

        email = st.text_input("Enter Email")

        password = st.text_input(
            "Create Password",
            type="password"
        )

        confirm = st.text_input(
            "Confirm Password",
            type="password"
        )

        if st.button("Create Account"):

            if name == "" or email == "" or password == "":

                st.warning("⚠️ Please fill all details")

            elif password != confirm:

                st.error("❌ Passwords do not match")

            else:

                cursor.execute(
                    "INSERT INTO Users VALUES(?,?,?)",
                    (name, email, password)
                )

                conn.commit()

                st.success("✅ Account Created Successfully")

                st.info("Now select Login and login to your account.")


    st.stop()


# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.markdown(
        """
        <div class="sh-card" style="padding:17px;">
            <div class="sh-pill">✦ SMART HOME</div>
            <div style="font-size:25px;font-weight:900;margin-top:8px;">✦ SmartHome AI</div>
            <div class="sh-muted">Intelligent Home Management</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="sh-card" style="padding:14px;">
            <div class="sh-pill">● ONLINE</div>
            <div style="font-size:16px;font-weight:750;margin-top:9px;">
                👤 {st.session_state.name}
            </div>
            <div class="sh-muted">{st.session_state.email}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("""
    <style>
    .nav-link,
    .nav-link span,
    .nav-link p {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)
    menu = option_menu(
    "Main Menu",

    [
        "Dashboard",
        "Grocery",
        "Medicines",
        "Documents",
        "Bills",
        "Expenses",
        "Analytics",
        "AI/ML Center",
        "Reports",
        "About"
    ],

    icons=[
        "house",
        "cart",
        "capsule",
        "file-earmark-text",
        "receipt",
        "wallet2",
        "bar-chart",
        "robot",
        "file-earmark-arrow-down",
        "info-circle"
    ],

    default_index=0,

    styles={
        "container": {
            "padding": "10px",
            "background-color": "#102f50",
            "border-radius": "15px",
            "border": "1px solid #28658c"
        },

        "icon": {
            "color": "#7dd3fc",
            "font-size": "18px"
        },

        "nav-link": {
            "color": "#ffffff",
            "font-size": "16px",
            "text-align": "left",
            "margin": "5px",
            "padding": "10px",
            "border-radius": "9px"
        },

        "nav-link-selected": {
            "background-color": "#1264d8",
            "color": "#ffffff",
            "font-weight": "bold"
        }
    }
)
    st.divider()

    if st.button("🚪 Logout"):

        st.session_state.login = False

        st.rerun()


# ---------------- DASHBOARD ----------------

if menu == "Dashboard":

    grocery_count = cursor.execute(
        "SELECT COUNT(*) FROM Grocery WHERE User_Email=?",
        (st.session_state.email,)
    ).fetchone()[0]

    medicine_count = cursor.execute(
        "SELECT COUNT(*) FROM Medicines WHERE User_Email=?",
        (st.session_state.email,)
    ).fetchone()[0]

    pending_bills = cursor.execute(
        "SELECT COUNT(*) FROM Bills WHERE Status='Pending' AND User_Email=?",
        (st.session_state.email,)
    ).fetchone()[0]

    expense_df = pd.read_sql_query(
        "SELECT * FROM Expenses WHERE User_Email=?",
        conn,
        params=(st.session_state.email,)
    )

    bill_df = pd.read_sql_query(
        "SELECT * FROM Bills WHERE User_Email=?",
        conn,
        params=(st.session_state.email,)
    )

    total_expense = expense_df["Amount"].sum() if len(expense_df) else 0
    total_bills_amount = bill_df["Amount"].sum() if len(bill_df) else 0
    budget = float(st.session_state.monthly_budget)

    used_percent = (total_expense / budget * 100) if budget else 0
    remaining = max(budget - total_expense, 0)

    if used_percent < 60:
        status_text = "Your spending is comfortably controlled."
        status_badge = "● HEALTHY"
    elif used_percent < 85:
        status_text = "Your spending deserves a little attention."
        status_badge = "● WATCH"
    elif used_percent <= 100:
        status_text = "You are close to your personal budget."
        status_badge = "● NEAR LIMIT"
    else:
        status_text = "Your spending has crossed your personal limit."
        status_badge = "● OVER BUDGET"

    # ---------- MODERN DASHBOARD HEADER ----------
    st.markdown(
        f"""
        <div class="sh-hero">
            <div class="sh-pill">🏠 SMART HOME COMMAND CENTER</div>
            <div class="sh-hero-title">Good to see you, {st.session_state.name} 👋</div>
            <div class="sh-hero-sub">
                Your home at a glance — clear, smart and under control.
            </div>
            <div style="margin-top:18px;">
                <span class="sh-pill">🤖 AI ACTIVE</span>
                <span class="sh-pill" style="margin-left:7px;">{status_badge}</span>
                <span style="margin-left:10px;color:#9fc5df;">
                    Personal budget ₹{budget:,.0f}
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------- TOP KPI ROW ----------
    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.metric("💰 Total Spending", f"₹{total_expense:,.0f}")

    with k2:
        st.metric("🎯 Budget Used", f"{used_percent:.0f}%")

    with k3:
        st.metric("🧾 Pending Bills", pending_bills)

    with k4:
        st.metric("💚 Available", f"₹{remaining:,.0f}")

    # ---------- MAIN COMMAND CENTER ----------
    st.markdown(
        '<div class="sh-section">⚡ Live Household Command Center</div>',
        unsafe_allow_html=True
    )

    left, right = st.columns([1.05, .95])

    with left:
        st.markdown(
            f"""
            <div class="sh-card">
                <div class="sh-pill">🎯 PERSONAL BUDGET</div>
                <div style="font-size:38px;font-weight:900;margin-top:10px;">
                    ₹{total_expense:,.0f}
                    <span style="font-size:16px;color:#9fc5df;"> / ₹{budget:,.0f}</span>
                </div>
                <div class="sh-muted" style="margin-top:7px;">{status_text}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.progress(min(used_percent / 100, 1.0))

    with right:
        if len(expense_df):
            category_data = expense_df.groupby("Category")["Amount"].sum()
            highest_category = category_data.idxmax()
            highest_amount = category_data.max()
            insight = (
                f"Your highest spending area is <b>{highest_category}</b> "
                f"with <b>₹{highest_amount:,.0f}</b>."
            )
        else:
            insight = "Add expenses and your dashboard will start building personal insights."

        st.markdown(
            f"""
            <div class="sh-card" style="min-height:153px;">
                <div class="sh-pill">🧠 SMART INSIGHT</div>
                <div style="font-size:21px;font-weight:850;margin-top:12px;">Your Home Intelligence</div>
                <div class="sh-muted" style="font-size:14px;line-height:1.7;margin-top:7px;">
                    {insight}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ---------- HOUSEHOLD PULSE ----------
    st.markdown(
        '<div class="sh-section">🏠 Household Pulse</div>',
        unsafe_allow_html=True
    )

    q1, q2, q3, q4 = st.columns(4)

    q1.markdown(
        f'<div class="sh-card"><div class="sh-muted">🛒 GROCERIES</div>'
        f'<div class="sh-number">{grocery_count}</div>'
        f'<div class="sh-muted">records</div></div>',
        unsafe_allow_html=True
    )

    q2.markdown(
        f'<div class="sh-card"><div class="sh-muted">💊 MEDICINES</div>'
        f'<div class="sh-number">{medicine_count}</div>'
        f'<div class="sh-muted">records</div></div>',
        unsafe_allow_html=True
    )

    q3.markdown(
        f'<div class="sh-card"><div class="sh-muted">🧾 BILL VALUE</div>'
        f'<div class="sh-number">₹{total_bills_amount:,.0f}</div>'
        f'<div class="sh-muted">tracked</div></div>',
        unsafe_allow_html=True
    )

    q4.markdown(
        f'<div class="sh-card"><div class="sh-muted">📊 EXPENSE RECORDS</div>'
        f'<div class="sh-number">{len(expense_df)}</div>'
        f'<div class="sh-muted">data points</div></div>',
        unsafe_allow_html=True
    )

    # ---------- VISUAL ANALYTICS ----------
    st.markdown(
        '<div class="sh-section">📊 Home Insights</div>',
        unsafe_allow_html=True
    )

    if len(expense_df):

        category_data = expense_df.groupby("Category")["Amount"].sum()

        # 1: category spending chart
        st.markdown(
            '<div class="dash-chart-card">'
            '<div class="sh-pill">SPENDING</div>'
            '<div class="dash-chart-title"><span class="dash-chart-icon">📊</span>Where Money Goes</div>'
            '<div class="dash-chart-sub">Category-wise household spending</div>'
            '</div>',
            unsafe_allow_html=True
        )

        fig1, ax1 = plt.subplots(figsize=(12, 4.6))
        fig1.subplots_adjust(left=.08, right=.98, top=.94, bottom=.22)
        fig1.patch.set_alpha(0)
        ax1.set_facecolor("none")
        ax1.bar(category_data.index, category_data.values, color="#38bdf8")
        ax1.tick_params(axis="x", colors="white", rotation=30)
        ax1.tick_params(axis="y", colors="white")
        ax1.set_ylabel("₹", color="white")
        ax1.grid(axis="y", alpha=.12)
        for spine in ax1.spines.values():
            spine.set_color("#28658c")
        plt.tight_layout()
        st.pyplot(fig1, transparent=True)
        plt.close(fig1)

        # 3: expense trend
        st.markdown(
            '<div class="sh-card"><div class="sh-pill">TREND</div>'
            '<div style="font-size:18px;font-weight:850;margin:8px 0;">Expense Flow</div>'
            '<div class="sh-muted">Recorded expenses over time</div></div>',
            unsafe_allow_html=True
        )

        fig3, ax3 = plt.subplots(figsize=(12, 3.5))
        fig3.patch.set_alpha(0)
        ax3.set_facecolor("none")
        ax3.plot(
            range(1, len(expense_df) + 1),
            expense_df["Amount"].values,
            marker="o",
            linewidth=2.5,
            color="#8b5cf6"
        )
        ax3.set_xlabel("Expense Record", color="#b9d8ed")
        ax3.set_ylabel("₹", color="white")
        ax3.tick_params(axis="x", colors="white")
        ax3.tick_params(axis="y", colors="white")
        ax3.grid(alpha=.12)
        for spine in ax3.spines.values():
            spine.set_color("#28658c")
        plt.tight_layout()
        st.pyplot(fig3, transparent=True)
        plt.close(fig3)

        # 4: budget gauge (simple horizontal visual)
        st.markdown(
            '<div class="sh-card"><div class="sh-pill">BUDGET</div>'
            '<div style="font-size:18px;font-weight:850;margin:8px 0;">Budget Health</div>'
            '<div class="sh-muted">Actual spending compared with your personal limit</div></div>',
            unsafe_allow_html=True
        )

        fig4, ax4 = plt.subplots(figsize=(12, 2.5))
        fig4.patch.set_alpha(0)
        ax4.set_facecolor("none")
        max_value=max(budget,total_expense,1)
        ax4.barh(["Budget"], [budget], alpha=.20, height=.45, color="#7dd3fc")
        ax4.barh(["Budget"], [min(total_expense,max_value)], height=.45, color="#38bdf8")
        ax4.set_xlim(0, max_value * 1.15)
        ax4.set_xlabel("₹", color="white")
        ax4.tick_params(axis="x", colors="white")
        ax4.tick_params(axis="y", colors="white")
        ax4.grid(axis="x", alpha=.12)
        for spine in ax4.spines.values():
            spine.set_color("#28658c")
        plt.tight_layout()
        st.pyplot(fig4, transparent=True)
        plt.close(fig4)

        # 5: bill overview, only when bill data exists
        if len(bill_df):
            st.markdown(
                '<div class="sh-card"><div class="sh-pill">BILLS</div>'
                '<div style="font-size:18px;font-weight:850;margin:8px 0;">Bill Overview</div>'
                '<div class="sh-muted">Tracked bill amounts</div></div>',
                unsafe_allow_html=True
            )

            bill_values = bill_df["Amount"].values

            fig5, ax5 = plt.subplots(figsize=(12, 3.2))
            fig5.patch.set_alpha(0)
            ax5.set_facecolor("none")
            ax5.plot(
                range(1, len(bill_values) + 1),
                bill_values,
                marker="o",
                linewidth=2.2,
                color="#22c55e"
            )
            ax5.fill_between(
                range(1, len(bill_values) + 1),
                bill_values,
                alpha=.10,
                color="#22c55e"
            )
            ax5.set_xlabel("Bill Record", color="#b9d8ed")
            ax5.set_ylabel("₹", color="white")
            ax5.tick_params(axis="x", colors="white")
            ax5.tick_params(axis="y", colors="white")
            ax5.grid(alpha=.12)
            for spine in ax5.spines.values():
                spine.set_color("#28658c")
            plt.tight_layout()
            st.pyplot(fig5, transparent=True)
            plt.close(fig5)

    else:
        st.markdown(
            """
            <div class="sh-card">
                <div class="sh-pill">📊 HOME INSIGHTS</div>
                <h3>No spending data yet</h3>
                <div class="sh-muted">
                    Add expenses to unlock the dashboard graphs.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ---------- BUDGET CONTROL ----------
    st.markdown(
        '<div class="sh-section">🎯 Control Your AI</div>',
        unsafe_allow_html=True
    )

    b1, b2 = st.columns([2, 1])

    with b1:
        new_budget = st.number_input(
            "Your usual monthly household budget (₹)",
            min_value=1000.0,
            step=1000.0,
            value=float(st.session_state.monthly_budget),
            key="dashboard_budget_input"
        )

    with b2:
        st.markdown("#### 🤖 AI Budget Mode")
        if st.button("Update Budget", width="stretch"):
            st.session_state.monthly_budget = new_budget
            st.success("Personal AI budget updated!")
            st.rerun()

    st.markdown(
        f"""
        <div class="sh-card">
            <div class="sh-pill">SIGMA MODE</div>
            <div style="font-size:22px;font-weight:900;margin-top:9px;">
                Don't just track your home. Understand it.
            </div>
            <div class="sh-muted" style="margin-top:5px;">
                Current AI reference limit: ₹{st.session_state.monthly_budget:,.0f}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Grocery
elif menu == "Grocery":

    st.title("🛒 Grocery Management")

    st.subheader("➕ Add Grocery Item")

    item = st.text_input("Item Name")

    quantity = st.number_input(
        "Quantity",
        min_value=1,
        value=1
    )

    price = st.number_input(
        "Price ₹",
        min_value=0.0
    )

    category = st.selectbox(
        "Category",
        ["Vegetables", "Fruits", "Dairy",
         "Snacks", "Grains", "Other"]
    )

    if st.button("Add Grocery"):

        cursor.execute(
            "INSERT INTO Grocery(Item, Quantity, Price, Category, Status, User_Email) VALUES(?,?,?,?,?,?)",
            (item, quantity, price, category, "Pending", st.session_state.email)
        )

        conn.commit()

        st.success("✅ Grocery Added Successfully!")

        st.divider()

    st.subheader("📋 Grocery List")

    df = pd.read_sql_query("SELECT * FROM Grocery WHERE User_Email=?", conn, params=(st.session_state.email,))

    if len(df) > 0:
        st.dataframe(df, width="stretch")
    else:
        st.info("No grocery items added yet.")

        st.divider()

    st.subheader("✅ Mark as Purchased")

    if len(df) > 0:

        grocery_id = st.selectbox(
            "Select Grocery ID",
            df["ID"]
        )

        if st.button("Mark Purchased"):

            cursor.execute(
                "UPDATE Grocery SET Status='Purchased' WHERE ID=? AND User_Email=?",
                (grocery_id, st.session_state.email)
            )

            conn.commit()

            st.success("✅ Grocery marked as Purchased!")
            st.divider()

    st.subheader("✏️ Edit Grocery")

    df = pd.read_sql_query("SELECT * FROM Grocery WHERE User_Email=?", conn, params=(st.session_state.email,))

    if len(df) > 0:

        edit_id = st.selectbox(
            "Select ID to Edit",
            df["ID"]
        )

        new_item = st.text_input("New Item Name")

        new_quantity = st.number_input(
            "New Quantity",
            min_value=1,
            value=1
        )

        new_price = st.number_input(
            "New Price ₹",
            min_value=0.0
        )

        if st.button("Update Grocery"):

            cursor.execute(
                """UPDATE Grocery
                SET Item=?, Quantity=?, Price=?
                WHERE ID=? AND User_Email=?""",
                (new_item, new_quantity, new_price, edit_id, st.session_state.email)
            )

            conn.commit()
            
            st.rerun()
            st.divider()

    st.subheader("🗑️ Delete Grocery")

    df = pd.read_sql_query("SELECT * FROM Grocery WHERE User_Email=?", conn, params=(st.session_state.email,))

    if len(df) > 0:

        delete_id = st.selectbox(
            "Select Grocery ID to Delete",
            df["ID"]
        )

        if st.button("Delete Grocery"):

            cursor.execute(
                "DELETE FROM Grocery WHERE ID=? AND User_Email=?",
                (delete_id, st.session_state.email)
            )

            conn.commit()

            st.success("🗑️ Grocery Deleted Successfully!")

            st.rerun()

    else:
        st.info("No grocery items available.")

    st.divider()
    #ML PREDICTIONS
    st.subheader("🤖 AI Grocery Price Prediction")

    df = pd.read_sql_query(
        "SELECT * FROM Grocery WHERE User_Email=?",
        conn,
        params=(st.session_state.email,)
    )

    if len(df) > 0:

        item = st.selectbox(
            "Select Grocery Item",
            df["Item"].unique()
        )

        qty = st.number_input(
            "Enter Quantity",
            min_value=1,
            value=1
        )

        item_data = df[df["Item"] == item]

        avg_price = item_data["Price"].mean()
        avg_qty = item_data["Quantity"].mean()

        price_per_unit = avg_price / avg_qty

        predicted_price = price_per_unit * qty

        if st.button("🤖 Predict Price"):

            st.success(
                "Predicted Grocery Price: ₹" +
                str(round(predicted_price, 2))
            )

    else:
        st.info("Add grocery data first.")
#medicines
elif menu == "Medicines":

    st.title("💊 Medicine Management")

    st.write("Manage medicines, expiry dates and health reminders.")

    st.divider()

    st.subheader("➕ Add Medicine")

    medicine = st.text_input("Medicine Name")

    quantity = st.number_input(
        "Quantity",
        min_value=1,
        value=1
    )

    expiry = st.date_input("Expiry Date")

    purpose = st.text_input("Purpose")

    if st.button("Add Medicine"):

        cursor.execute(
            """INSERT INTO Medicines
            (Medicine, Quantity, Expiry_Date, Purpose, Status, User_Email)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (medicine, quantity, str(expiry), purpose, "Active", st.session_state.email)
        )

        conn.commit()

        st.success("✅ Medicine Added Successfully!")

    st.divider()
    st.subheader("📋 Medicine List")

    medicine_df = pd.read_sql_query(
        "SELECT * FROM Medicines WHERE User_Email=?",
        conn,
        params=(st.session_state.email,)
    )

    if len(medicine_df) > 0:

        st.dataframe(
            medicine_df,
            width="stretch"
        )

    else:
        st.info("No medicines added yet.")

    st.divider()

    st.subheader("⚠️ Smart Expiry Alert")

    medicine_df = pd.read_sql_query(
        "SELECT * FROM Medicines WHERE User_Email=?",
        conn,
        params=(st.session_state.email,)
    )

    if len(medicine_df) > 0:

        today = pd.Timestamp.today()

        for index, row in medicine_df.iterrows():

            expiry_date = pd.to_datetime(row["Expiry_Date"])

            days_left = (expiry_date - today).days

            if days_left < 0:
                st.error(
                    "❌ " + row["Medicine"] +
                    " has expired!"
                )

            elif days_left <= 30:
                st.warning(
                    "⚠️ " + row["Medicine"] +
                    " expires in " + str(days_left) + " days!"
                )

            else:
                st.success(
                    "✅ " + row["Medicine"] +
                    " is safe. " + str(days_left) +
                    " days remaining."
                )

    else:
        st.info("No medicines available for expiry checking.")

    st.divider()

    st.subheader("✏️ Edit Medicine")

    medicine_df = pd.read_sql_query(
        "SELECT * FROM Medicines WHERE User_Email=?",
        conn,
        params=(st.session_state.email,)
    )

    if len(medicine_df) > 0:

        edit_id = st.selectbox(
            "Select Medicine ID to Edit",
            medicine_df["ID"]
        )

        new_medicine = st.text_input("New Medicine Name")

        new_quantity = st.number_input(
            "New Quantity",
            min_value=1,
            value=1
        )

        new_purpose = st.text_input("New Purpose")

        if st.button("Update Medicine"):

            cursor.execute(
                """UPDATE Medicines
                SET Medicine=?, Quantity=?, Purpose=?
                WHERE ID=? AND User_Email=?""",
                (new_medicine, new_quantity, new_purpose, edit_id, st.session_state.email)
            )

            conn.commit()

            st.rerun()

    st.divider()

    st.subheader("🗑️ Delete Medicine")

    medicine_df = pd.read_sql_query(
        "SELECT * FROM Medicines WHERE User_Email=?",
        conn,
        params=(st.session_state.email,)
    )

    if len(medicine_df) > 0:

        delete_id = st.selectbox(
            "Select Medicine ID to Delete",
            medicine_df["ID"],
            key="delete_medicine"
        )

        if st.button("Delete Medicine"):

            cursor.execute(
                "DELETE FROM Medicines WHERE ID=? AND User_Email=?",
                (delete_id, st.session_state.email)
            )

            conn.commit()

            st.rerun()

    else:
        st.info("No medicines available.")


elif menu == "Documents":

    st.markdown(
        """
        <div class="sh-hero">
            <div class="sh-pill">📄 DOCUMENT VAULT</div>
            <div class="sh-hero-title">Your Important Documents</div>
            <div class="sh-hero-sub">
                View, download, upload and manage your documents securely.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # EXISTING FILE DOCUMENTS
    # =====================================================
    st.markdown("### 📂 Existing Documents")

    # IMPORTANT:
    # Each logged-in user gets their own folder.
    # Database is not changed.
    user_upload_folder = get_user_upload_folder()

    existing_files = []

    if os.path.exists(user_upload_folder):
        for name in os.listdir(user_upload_folder):
            file_path = os.path.join(user_upload_folder, name)
            if os.path.isfile(file_path):
                existing_files.append(file_path)

    existing_files = sorted(existing_files)

    if existing_files:

        # Simple document selector makes VIEW reliable after Streamlit reruns.
        file_names = [os.path.basename(x) for x in existing_files]

        selected_name = st.selectbox(
            "📌 Select a document to view",
            file_names,
            key="selected_document_to_view"
        )

        selected_path = existing_files[file_names.index(selected_name)]

        with open(selected_path, "rb") as f:
            selected_bytes = f.read()

        selected_mime = (
            mimetypes.guess_type(selected_name)[0]
            or "application/octet-stream"
        )

        size_kb = os.path.getsize(selected_path) / 1024

        st.markdown(
            f"""
            <div class="sh-doc-card">
                <div class="sh-doc-name">📎 {selected_name}</div>
                <div class="sh-doc-meta">
                    {size_kb:.1f} KB • Your document • Ready to view
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # ---------------- VIEW ----------------
        st.markdown("#### 👁️ Document Preview")

        if selected_mime.startswith("image/"):

            st.image(
                selected_bytes,
                caption=selected_name,
                width="stretch"
            )

        elif selected_mime == "application/pdf":

            # st.pdf gives a proper PDF viewer in supported Streamlit versions.
            # Fallback iframe keeps older versions usable.
            try:
                st.pdf(selected_bytes)
            except Exception:
                encoded = base64.b64encode(selected_bytes).decode()

                st.markdown(
                    f"""
                    <iframe
                        src="data:application/pdf;base64,{encoded}"
                        width="100%"
                        height="700"
                        style="border:1px solid rgba(77,166,255,.3);
                               border-radius:15px;">
                    </iframe>
                    """,
                    unsafe_allow_html=True
                )

        else:
            st.info(
                "Preview is not available for this file type. "
                "Use Download to open it on your device."
            )

        # ---------------- EDIT + ACTIONS ----------------
        st.markdown("#### ✏️ Edit Document")

        # Simple text-based editing: change only the document file name.
        # The actual file remains in the same user folder and the database is untouched.
        edit_col1, edit_col2 = st.columns([2.2, 1])

        with edit_col1:
            edited_name = st.text_input(
                "Document Name",
                value=selected_name,
                key="edited_document_name"
            )

        with edit_col2:
            st.write("")
            st.write("")
            if st.button(
                "💾 Save Changes",
                key="save_document_name",
                width="stretch"
            ):
                edited_name = os.path.basename(edited_name.strip())

                if edited_name == "":
                    st.error("❌ Document name cannot be empty.")
                else:
                    original_ext = os.path.splitext(selected_name)[1]

                    # Keep the original file extension when the user
                    # enters only a new name.
                    if not os.path.splitext(edited_name)[1]:
                        edited_name += original_ext

                    new_path = os.path.join(
                        user_upload_folder,
                        edited_name
                    )

                    if edited_name == selected_name:
                        st.info("ℹ️ No changes were made.")
                    elif os.path.exists(new_path):
                        st.error("❌ A document with this name already exists.")
                    else:
                        try:
                            os.rename(selected_path, new_path)
                            st.success("✅ Document name updated successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error("❌ Unable to rename the document.")

        # ---------------- ACTIONS ----------------
        d1, d2 = st.columns(2)

        with d1:
            st.download_button(
                "⬇️ Download Document",
                data=selected_bytes,
                file_name=selected_name,
                mime=selected_mime,
                key="download_selected_document",
                width="stretch"
            )

        with d2:
            if st.button(
                "🗑️ Delete Document File",
                key="delete_selected_document",
                width="stretch"
            ):
                try:
                    os.remove(selected_path)
                    st.success("🗑️ Document deleted successfully!")
                    st.rerun()
                except Exception:
                    st.error("❌ Unable to delete the document.")

    else:
        st.markdown(
            """
            <div class="sh-card">
                <div class="sh-pill">DOCUMENT VAULT</div>
                <h3>No documents yet</h3>
                <div class="sh-muted">
                    Upload a PDF or image below and it will appear here automatically.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # =====================================================
    # UPLOAD
    # =====================================================
    st.divider()
    st.markdown("### 📤 Upload New Document")

    document_file = st.file_uploader(
        "Choose a PDF or image from your device",
        type=["pdf", "jpg", "jpeg", "png"],
        key="document_upload"
    )

    if document_file:

        save_file(document_file)

        st.success(
            "✅ Document uploaded successfully! "
            "It is now available in Existing Documents."
        )

        st.rerun()

    # =====================================================
    # DATABASE DOCUMENT DETAILS
    # =====================================================
    st.divider()
    st.markdown("### ➕ Add Document Details")

    document_name = st.selectbox(
        "Document Name",
        [
            "Aadhaar Card",
            "PAN Card",
            "Driving Licence",
            "Passport",
            "Insurance",
            "Other"
        ]
    )

    document_number = st.text_input("Document Number")
    expiry_date = st.date_input("Expiry Date")

    if st.button("Add Document", width="stretch"):

        cursor.execute(
            """INSERT INTO Documents
            (Document_Name, Document_Number, Expiry_Date, Status, User_Email)
            VALUES (?, ?, ?, ?, ?)""",
            (
                document_name,
                document_number,
                str(expiry_date),
                "Active",
                st.session_state.email
            )
        )

        conn.commit()

        st.success("✅ Document details added successfully!")

    # =====================================================
    # EXPIRY STATUS
    # =====================================================
    st.divider()
    st.markdown("### ⚠️ Document Expiry Status")

    document_df = pd.read_sql_query(
        "SELECT * FROM Documents WHERE User_Email=?",
        conn,
        params=(st.session_state.email,)
    )

    if len(document_df) > 0:

        today = pd.Timestamp.today()

        for _, row in document_df.iterrows():

            expiry = pd.to_datetime(row["Expiry_Date"])
            days_left = (expiry - today).days

            if days_left < 0:
                st.error(
                    "❌ " + row["Document_Name"] + " has expired!"
                )

            elif days_left <= 30:
                st.warning(
                    "⚠️ " + row["Document_Name"] +
                    " expires in " + str(days_left) + " days!"
                )

            else:
                st.success(
                    "✅ " + row["Document_Name"] + " is valid."
                )

    else:
        st.info("No document records added yet.")

    # =====================================================
    # UPDATE / DELETE DATABASE DOCUMENT RECORD
    # =====================================================
    st.divider()
    st.markdown("### ✏️ Manage Document Details")

    if len(document_df) > 0:

        edit_id = st.selectbox(
            "Select Document ID",
            document_df["ID"],
            key="edit_document"
        )

        current_record = document_df[document_df["ID"] == edit_id].iloc[0]

        new_number = st.text_input(
            "New Document Number",
            value=str(current_record["Document_Number"] or ""),
            key="new_document_number"
        )

        current_expiry = pd.to_datetime(
            current_record["Expiry_Date"]
        ).date()

        new_expiry = st.date_input(
            "New Expiry Date",
            value=current_expiry,
            key="new_document_expiry"
        )

        if st.button("Update Document", width="stretch"):

            cursor.execute(
                """UPDATE Documents
                SET Document_Number=?, Expiry_Date=?
                WHERE ID=? AND User_Email=?""",
                (
                    new_number,
                    str(new_expiry),
                    edit_id,
                    st.session_state.email
                )
            )

            conn.commit()
            st.success("✅ Document details updated!")
            st.rerun()

        delete_id = st.selectbox(
            "Select Document ID to Delete",
            document_df["ID"],
            key="delete_document"
        )

        if st.button("Delete Document Record", width="stretch"):

            cursor.execute(
                "DELETE FROM Documents WHERE ID=? AND User_Email=?",
                (
                    delete_id,
                    st.session_state.email
                )
            )

            conn.commit()
            st.success("🗑️ Document record deleted!")
            st.rerun()

    else:
        st.info("Add a document record to enable editing and deletion.")

elif menu == "Bills":

    st.title("🧾 Bill Management")

    st.write("Manage household bills, payments and due dates.")

    st.subheader("📤 Import Your Bill")

    bill_file = st.file_uploader(
        "Upload bill from your device",
        type=["pdf", "jpg", "jpeg", "png"],
        key="bill_upload"
    )

    if bill_file:
        bill_path = save_file(bill_file)
        st.success("✅ Bill uploaded successfully!")
        st.write("File:", bill_file.name)

        with open(bill_path, "rb") as f:
            st.download_button(
                "⬇️ Download Bill",
                f,
                file_name=bill_file.name,
                key="download_bill"
            )

    st.divider()

    st.subheader("➕ Add Bill")

    bill_type = st.selectbox(
        "Bill Type",
        ["Electricity", "Water", "Gas",
         "Internet", "Mobile", "Other"]
    )

    amount = st.number_input(
        "Bill Amount ₹",
        min_value=0.0
    )

    due_date = st.date_input(
        "Due Date"
    )

    status = st.selectbox(
        "Status",
        ["Pending", "Paid"]
    )

    if st.button("Add Bill"):

        cursor.execute(
            """INSERT INTO Bills
            (Bill_Type, Amount, Due_Date, Status, User_Email)
            VALUES (?, ?, ?, ?, ?)""",
            (bill_type, amount, str(due_date), status, st.session_state.email)
        )

        conn.commit()

        st.success("✅ Bill Added Successfully!")
    st.divider()

    st.subheader("📋 Bill List")

    bill_df = pd.read_sql_query(
        "SELECT * FROM Bills WHERE User_Email=?",
        conn,
        params=(st.session_state.email,)
    )

    if len(bill_df) > 0:

        st.dataframe(
            bill_df,
            width="stretch"
        )

    else:
        st.info("No bills added yet.")
    st.divider()

    st.subheader("⚠️ Bill Due-Date Alert")

    bill_df = pd.read_sql_query(
        "SELECT * FROM Bills WHERE User_Email=?",
        conn,
        params=(st.session_state.email,)
    )

    if len(bill_df) > 0:

        today = pd.Timestamp.today()

        for index, row in bill_df.iterrows():

            due_date = pd.to_datetime(row["Due_Date"])

            days_left = (due_date - today).days

            if row["Status"] == "Paid":

                st.success(
                    "✅ " + row["Bill_Type"] +
                    " bill is already paid."
                )

            elif days_left < 0:

                st.error(
                    "❌ " + row["Bill_Type"] +
                    " bill is overdue!"
                )

            elif days_left <= 7:

                st.warning(
                    "⚠️ " + row["Bill_Type"] +
                    " bill is due in " +
                    str(days_left) + " days!"
                )

            else:

                st.info(
                    "📅 " + row["Bill_Type"] +
                    " bill is due in " +
                    str(days_left) + " days."
                )
    st.divider()

    st.subheader("✅ Mark Bill as Paid")

    bill_df = pd.read_sql_query(
        "SELECT * FROM Bills WHERE User_Email=?",
        conn,
        params=(st.session_state.email,)
    )

    if len(bill_df) > 0:

        bill_id = st.selectbox(
            "Select Bill ID",
            bill_df["ID"]
        )

        if st.button("Mark as Paid"):

            cursor.execute(
                "UPDATE Bills SET Status='Paid' WHERE ID=? AND User_Email=?",
                (bill_id, st.session_state.email)
            )

            conn.commit()

            st.rerun()
    st.divider()

    st.subheader("✏️ Edit Bill")

    bill_df = pd.read_sql_query(
        "SELECT * FROM Bills WHERE User_Email=?",
        conn,
        params=(st.session_state.email,)
    )

    if len(bill_df) > 0:

        edit_id = st.selectbox(
            "Select Bill ID to Edit",
            bill_df["ID"],
            key="edit_bill"
        )

        new_amount = st.number_input(
            "New Bill Amount ₹",
            min_value=0.0
        )

        new_due_date = st.date_input(
            "New Due Date"
        )

        if st.button("Update Bill"):

            cursor.execute(
                """UPDATE Bills
                SET Amount=?, Due_Date=?
                WHERE ID=? AND User_Email=?""",
                (new_amount, str(new_due_date), edit_id, st.session_state.email)
            )

            conn.commit()

            st.rerun()
    st.divider()

    st.subheader("🗑️ Delete Bill")

    bill_df = pd.read_sql_query(
        "SELECT * FROM Bills WHERE User_Email=?",
        conn,
        params=(st.session_state.email,)
    )

    if len(bill_df) > 0:

        delete_id = st.selectbox(
            "Select Bill ID to Delete",
            bill_df["ID"],
            key="delete_bill"
        )

        if st.button("Delete Bill"):

            cursor.execute(
                "DELETE FROM Bills WHERE ID=? AND User_Email=?",
                (delete_id, st.session_state.email)
            )

            conn.commit()

            st.rerun()

    else:
        st.info("No bills available.")
    st.divider()
#ML PREDICTION 2
    st.subheader("🤖 AI Bill Prediction")

    bill_df = pd.read_sql_query(
        "SELECT * FROM Bills WHERE User_Email=?",
        conn,
        params=(st.session_state.email,)
    )

    if len(bill_df) >= 3:

        X = np.arange(len(bill_df)).reshape(-1, 1)

        y = bill_df["Amount"]

        model = LinearRegression()

        model.fit(X, y)

        next_bill = model.predict([[len(bill_df)]])

        st.success(
            "🔮 Predicted Next Bill: ₹" +
            str(round(next_bill[0], 2))
        )
        st.caption("Model used: Linear Regression")

    else:

        st.info(
            "Add at least 3 bills for AI prediction."
        )
elif menu == "Expenses":

    st.title("💰 Expense Management")

    st.write("Track and manage your household expenses.")

    st.divider()

    st.subheader("➕ Add Expense")

    expense_name = st.text_input(
        "Expense Name"
    )

    category = st.selectbox(
        "Expense Category",
        [
            "Grocery",
            "Electricity",
            "Water",
            "Gas",
            "Internet",
            "Maintenance",
            "Shopping",
            "Other"
        ]
    )

    amount = st.number_input(
        "Expense Amount ₹",
        min_value=0.0
    )

    expense_date = st.date_input(
        "Expense Date"
    )

    if st.button("Add Expense"):

        cursor.execute(
            """INSERT INTO Expenses
            (Expense_Name, Category, Amount, Date, User_Email)
            VALUES (?, ?, ?, ?, ?)""",
            (
                expense_name,
                category,
                amount,
                str(expense_date),
                st.session_state.email
            )
        )

        conn.commit()

        st.success("✅ Expense Added Successfully!")
    st.divider()

    st.subheader("📋 Expense List")

    expense_df = pd.read_sql_query(
        "SELECT * FROM Expenses WHERE User_Email=?",
        conn,
        params=(st.session_state.email,)
    )

    if len(expense_df) > 0:

        st.dataframe(
            expense_df,
            width="stretch"
        )

    else:
        st.info("No expenses added yet.")
    st.divider()

    st.subheader("✏️ Edit Expense")

    expense_df = pd.read_sql_query(
        "SELECT * FROM Expenses WHERE User_Email=?",
        conn,
        params=(st.session_state.email,)
    )

    if len(expense_df) > 0:

        edit_id = st.selectbox(
            "Select Expense ID to Edit",
            expense_df["ID"]
        )

        new_name = st.text_input(
            "New Expense Name"
        )

        new_amount = st.number_input(
            "New Amount ₹",
            min_value=0.0
        )

        if st.button("Update Expense"):

            cursor.execute(
                """UPDATE Expenses
                SET Expense_Name=?, Amount=?
                WHERE ID=? AND User_Email=?""",
                (new_name, new_amount, edit_id, st.session_state.email)
            )

            conn.commit()

            st.rerun()
    st.divider()

    st.subheader("🗑️ Delete Expense")

    expense_df = pd.read_sql_query(
        "SELECT * FROM Expenses WHERE User_Email=?",
        conn,
        params=(st.session_state.email,)
    )

    if len(expense_df) > 0:

        delete_id = st.selectbox(
            "Select Expense ID to Delete",
            expense_df["ID"],
            key="delete_expense"
        )

        if st.button("Delete Expense"):

            cursor.execute(
                "DELETE FROM Expenses WHERE ID=? AND User_Email=?",
                (delete_id, st.session_state.email)
            )

            conn.commit()

            st.rerun()

    else:
        st.info("No expenses available.")
    st.divider()

    st.subheader("📊 Expense Analytics")

    expense_df = pd.read_sql_query(
        "SELECT * FROM Expenses WHERE User_Email=?",
        conn,
        params=(st.session_state.email,)
    )

    if len(expense_df) > 0:

        category_data = expense_df.groupby(
            "Category"
        )["Amount"].sum()

        fig, ax = plt.subplots(figsize=(7, 3))

        fig.patch.set_alpha(0)
        ax.set_facecolor("#102f50")

        ax.bar(
            category_data.index,
            category_data.values,
            color="#38bdf8"
        )

        ax.set_ylabel("Amount ₹", color="white")
        ax.tick_params(axis="x", colors="white", rotation=45)
        ax.tick_params(axis="y", colors="white")

        for spine in ax.spines.values():
            spine.set_color("#28658c")

        plt.tight_layout()

        st.pyplot(fig, transparent=True)

        total = expense_df["Amount"].sum()

        st.metric(
            "💰 Total Household Expense",
            "₹" + str(total)
        )

    else:
        st.info(
            "Add some expenses to view analytics."
        )

#ML PREDICTION 3
    st.divider()

    st.subheader("🔮 AI Expense Prediction")

    expense_df = pd.read_sql_query(
        "SELECT * FROM Expenses WHERE User_Email=?",
        conn,
        params=(st.session_state.email,)
    )

    if len(expense_df) >= 2:

        amounts = expense_df["Amount"]

        predicted_expense = amounts.mean()

        st.success(
            "🔮 Predicted Next Expense: ₹" +
            str(round(predicted_expense, 2))
        )

    else:
        st.info("Add at least 2 expenses for prediction.")

    st.divider()
    st.subheader("📈 ML Expense Prediction")

    if len(expense_df) >= 2:

        X = np.arange(len(expense_df)).reshape(-1, 1)
        y = expense_df["Amount"]

        model = LinearRegression()
        model.fit(X, y)

        next_expense = model.predict([[len(expense_df)]])

        st.success(
            "🤖 Predicted Next Expense: ₹" +
            str(round(next_expense[0], 2))
        )

        st.caption("Model used: Linear Regression")
    else:
        st.info("Add at least 2 expenses for ML prediction.")
elif menu == "Analytics":

    st.markdown(
        """
        <div class="sh-hero">
            <div class="sh-pill">📊 SMART ANALYTICS</div>
            <h1>Analytics Command Center</h1>
            <div class="sh-muted">Turn household records into clear decisions.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    expense_df = pd.read_sql_query(
        "SELECT * FROM Expenses WHERE User_Email=?",
        conn,
        params=(st.session_state.email,)
    )

    bill_df = pd.read_sql_query(
        "SELECT * FROM Bills WHERE User_Email=?",
        conn,
        params=(st.session_state.email,)
    )

    grocery_df = pd.read_sql_query(
        "SELECT * FROM Grocery WHERE User_Email=?",
        conn,
        params=(st.session_state.email,)
    )

    total_expense = expense_df["Amount"].sum() if len(expense_df) else 0
    total_bill = bill_df["Amount"].sum() if len(bill_df) else 0
    average = expense_df["Amount"].mean() if len(expense_df) else 0
    highest = expense_df["Amount"].max() if len(expense_df) else 0

    a, b, c, d = st.columns(4)
    a.metric("💰 TOTAL SPEND", f"₹{total_expense:,.0f}")
    b.metric("🧾 BILL VALUE", f"₹{total_bill:,.0f}")
    c.metric("📌 AVERAGE", f"₹{average:,.0f}")
    d.metric("🛒 GROCERY ITEMS", len(grocery_df))

    if len(expense_df):

        category_data = expense_df.groupby("Category")["Amount"].sum().sort_values(ascending=False)

        left, right = st.columns(2)

        with left:
            st.markdown("### 📈 Spending Pattern")

            fig, ax = plt.subplots(figsize=(7, 4))
            ax.set_facecolor("#0f2a46")
            fig.patch.set_facecolor("#0f2a46")

            ax.bar(category_data.index, category_data.values)
            ax.set_xlabel("Category", color="white")
            ax.set_ylabel("Amount (₹)", color="white")
            ax.tick_params(colors="white")
            ax.spines["bottom"].set_color("#5aa9d6")
            ax.spines["left"].set_color("#5aa9d6")
            ax.set_title("Category Spending", color="white")

            plt.xticks(rotation=25)
            st.pyplot(fig)

        with right:
            st.markdown("### 🥧 Money Distribution")

            fig, ax = plt.subplots(figsize=(6, 4))
            fig.patch.set_facecolor("#0f2a46")
            ax.set_facecolor("#0f2a46")

            ax.pie(
                category_data.values,
                labels=category_data.index,
                autopct="%1.0f%%",
                textprops={"color": "white"}
            )
            ax.set_title("Expense Distribution", color="white")

            st.pyplot(fig)

        st.markdown("### 🧠 Decision Signals")

        x, y, z = st.columns(3)

        x.markdown(
            f'<div class="sh-card"><div class="sh-pill">TOP CATEGORY</div>'
            f'<div class="sh-number">{category_data.index[0]}</div>'
            f'<div class="sh-muted">Highest spending area</div></div>',
            unsafe_allow_html=True
        )

        y.markdown(
            f'<div class="sh-card"><div class="sh-pill">TOP VALUE</div>'
            f'<div class="sh-number">₹{category_data.iloc[0]:,.0f}</div>'
            f'<div class="sh-muted">Largest category spend</div></div>',
            unsafe_allow_html=True
        )

        z.markdown(
            f'<div class="sh-card"><div class="sh-pill">DATA DEPTH</div>'
            f'<div class="sh-number">{len(expense_df)}</div>'
            f'<div class="sh-muted">Expense records analysed</div></div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="sh-card"><div class="sh-pill">SIGMA ANALYTICS</div>'
            '<h3>Data never needs an excuse.</h3>'
            '<div class="sh-muted">Read the pattern. Own the decision.</div></div>',
            unsafe_allow_html=True
        )

    else:
        st.info("Add expenses to unlock your analytics intelligence.")


elif menu == "AI/ML Center":

    st.markdown(
        """
        <div class="sh-hero">
            <div class="sh-pill">🤖 SMART AI CENTER • 12 FEATURES</div>
            <div class="sh-hero-title">Smart Intelligence</div>
            <div class="sh-hero-sub">
                Simple AI that learns from household records and turns them into useful decisions.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Read existing user data only. No database structure is changed.
    expense_df = pd.read_sql_query(
        "SELECT * FROM Expenses WHERE User_Email=?",
        conn,
        params=(st.session_state.email,)
    )

    bill_df = pd.read_sql_query(
        "SELECT * FROM Bills WHERE User_Email=?",
        conn,
        params=(st.session_state.email,)
    )

    medicine_df = pd.read_sql_query(
        "SELECT * FROM Medicines WHERE User_Email=?",
        conn,
        params=(st.session_state.email,)
    )

    grocery_df = pd.read_sql_query(
        "SELECT * FROM Grocery WHERE User_Email=?",
        conn,
        params=(st.session_state.email,)
    )

    budget = float(st.session_state.monthly_budget)

    total_expense = (
        float(expense_df["Amount"].sum())
        if len(expense_df) else 0
    )

    used = (total_expense / budget * 100) if budget else 0
    remaining = max(budget - total_expense, 0)

    # Simple reusable values
    pending = 0
    if len(bill_df) and "Status" in bill_df.columns:
        pending = int(
            (bill_df["Status"].astype(str).str.lower() == "pending").sum()
        )

    if len(expense_df):
        category_data = expense_df.groupby("Category")["Amount"].sum()
        top_category = category_data.idxmax()
        top_amount = category_data.max()
    else:
        category_data = pd.Series(dtype=float)
        top_category = "No data"
        top_amount = 0

    if len(expense_df) >= 3:
        average = expense_df["Amount"].mean()
        unusual = int(
            (expense_df["Amount"] > average * 2).sum()
        )
    else:
        average = 0
        unusual = 0

    # =====================================================
    # FEATURE 1 — PERSONAL AI SNAPSHOT
    # =====================================================
    st.markdown("### 01 • 🎯 Personal AI Snapshot")

    a1, a2, a3, a4 = st.columns(4)

    a1.metric("💰 Budget", f"₹{budget:,.0f}")
    a2.metric("💸 Spent", f"₹{total_expense:,.0f}")
    a3.metric("💚 Remaining", f"₹{remaining:,.0f}")
    a4.metric("📊 Used", f"{used:.0f}%")

    if used <= 60:
        st.success("🟢 Excellent — spending is well controlled.")
    elif used <= 85:
        st.info("🔵 Good — keep monitoring your spending.")
    elif used <= 100:
        st.warning("🟡 Near limit — your budget is almost used.")
    else:
        st.error("🔴 Over budget — spending has crossed your limit.")

    # =====================================================
    # FEATURE 2 — SMARTHOME SCORE
    # =====================================================
    st.markdown("### 02 • 🏠 SmartHome Score")

    score = 100

    if used > 100:
        score -= 25
    elif used > 85:
        score -= 10

    score -= min(pending * 5, 15)
    score -= min(unusual * 5, 15)
    score = max(0, score)

    if score >= 80:
        st.success(f"🟢 {score}/100 — Excellent")
    elif score >= 60:
        st.warning(f"🟡 {score}/100 — Good")
    else:
        st.error(f"🔴 {score}/100 — Needs Attention")

    st.progress(score / 100)

    # =====================================================
    # FEATURE 3 + 4 — SIMPLE LINEAR REGRESSION
    # =====================================================
    st.markdown("### 03 • 🔮 AI Predictions")

    p1, p2 = st.columns(2)

    with p1:
        st.markdown(
            '<div class="sh-ai-card"><div class="sh-ai-badge">FEATURE 3</div>'
            '<div class="sh-ai-title">💸 Next Expense</div>'
            '<div class="sh-ai-help">Linear Regression estimates the next expense from previous records.</div></div>',
            unsafe_allow_html=True
        )

        if len(expense_df) >= 2:
            X = np.arange(len(expense_df)).reshape(-1, 1)
            y = expense_df["Amount"].values

            model = LinearRegression()
            model.fit(X, y)

            prediction = max(
                0,
                float(model.predict([[len(expense_df)]])[0])
            )

            st.metric("Estimated Expense", f"₹{prediction:,.0f}")
        else:
            st.info("Add at least 2 expenses.")

    with p2:
        st.markdown(
            '<div class="sh-ai-card"><div class="sh-ai-badge">FEATURE 4</div>'
            '<div class="sh-ai-title">🧾 Next Bill</div>'
            '<div class="sh-ai-help">The same simple model estimates the next bill amount.</div></div>',
            unsafe_allow_html=True
        )

        if len(bill_df) >= 2:
            X = np.arange(len(bill_df)).reshape(-1, 1)
            y = bill_df["Amount"].values

            model = LinearRegression()
            model.fit(X, y)

            prediction = max(
                0,
                float(model.predict([[len(bill_df)]])[0])
            )

            st.metric("Estimated Bill", f"₹{prediction:,.0f}")
        else:
            st.info("Add at least 2 bills.")

    # =====================================================
    # FEATURE 5 — SMART ALERTS
    # =====================================================
    st.markdown("### 05 • 🚨 Smart Alerts")

    alerts = []

    if used > 100:
        alerts.append("🔴 Budget crossed.")
    elif used > 85:
        alerts.append("🟡 Budget is close to the limit.")

    if pending:
        alerts.append(f"🧾 {pending} pending bill(s) need attention.")

    if unusual:
        alerts.append(f"⚠️ {unusual} unusually high expense(s) detected.")

    if not alerts:
        st.success("✅ No major alerts right now.")
    else:
        for alert in alerts:
            st.warning(alert)

    # =====================================================
    # FEATURE 6 — TOP SPENDING AREA
    # =====================================================
    st.markdown("### 06 • 🎯 Top Spending Area")

    if len(expense_df):
        st.markdown(
            f"""
            <div class="sh-card">
                <div class="sh-pill">AI INSIGHT</div>
                <h2 style="margin-top:10px;">{top_category}</h2>
                <div class="sh-muted">
                    Highest recorded spending • ₹{top_amount:,.0f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.info("Add expenses to unlock this insight.")

    # =====================================================
    # FEATURE 7 — SPENDING TREND
    # =====================================================
    st.markdown("### 07 • 📈 Spending Trend")

    if len(expense_df) >= 2:
        first = expense_df["Amount"].iloc[0]
        last = expense_df["Amount"].iloc[-1]

        if last > first:
            st.warning("📈 Spending is increasing.")
        elif last < first:
            st.success("📉 Spending is decreasing.")
        else:
            st.info("➡️ Spending is stable.")
    else:
        st.info("Add at least 2 expenses.")

    # =====================================================
    # FEATURE 8 — SMART ADVICE
    # =====================================================
    st.markdown("### 08 • 🧠 Smart Advice")

    if used > 100:
        advice = "Reduce optional spending because your budget is already crossed."
    elif used > 85:
        advice = "You are close to your budget. Plan your next purchases carefully."
    elif len(expense_df):
        advice = "Your spending is under control. Keep following your budget."
    else:
        advice = "Add household records and AI will start giving personal insights."

    st.info("💡 " + advice)

    # =====================================================
    # FEATURE 9 — SMART SAVINGS SUGGESTION
    # =====================================================
    st.markdown("### 09 • 💰 Smart Savings Suggestion")

    if budget > total_expense:
        possible_saving = (budget - total_expense) * 0.20
        st.success(
            f"💚 You could target around ₹{possible_saving:,.0f} "
            "as an extra saving amount."
        )
    else:
        st.warning(
            "⚠️ First bring spending below your budget, then AI can suggest savings."
        )

    # =====================================================
    # FEATURE 10 — SMART PURCHASE ALERT
    # =====================================================
    st.markdown("### 10 • 🛒 Smart Purchase Alert")

    if used > 85:
        st.warning(
            "🛒 Your budget is getting tight. Consider checking the need "
            "before making optional purchases."
        )
    elif len(expense_df) >= 3 and unusual:
        st.warning(
            "🛒 AI noticed unusually high spending. Review your next purchase."
        )
    else:
        st.success(
            "✅ No purchase warning. Your current spending pattern looks comfortable."
        )

    # =====================================================
    # FEATURE 11 — NEXT MONTH EXPENSE FORECAST
    # =====================================================
    st.markdown("### 11 • 🔮 Next Month Expense Forecast")

    monthly_df = pd.DataFrame()

    if len(expense_df) and "Date" in expense_df.columns:
        monthly_df = expense_df.copy()
        monthly_df["Month"] = pd.to_datetime(
            monthly_df["Date"], errors="coerce"
        ).dt.to_period("M").astype(str)

        monthly_df = (
            monthly_df.dropna(subset=["Month"])
            .groupby("Month", as_index=False)["Amount"]
            .sum()
        )

    if len(monthly_df) >= 2:
        X = np.arange(len(monthly_df)).reshape(-1, 1)
        y = monthly_df["Amount"].values

        forecast_model = LinearRegression()
        forecast_model.fit(X, y)

        next_month_total = max(
            0,
            float(forecast_model.predict([[len(monthly_df)]])[0])
        )

        st.success(
            f"🔮 AI estimates next month's total household expense at "
            f"₹{next_month_total:,.0f}."
        )
    elif len(expense_df) >= 2:
        # Simple fallback when the user has not yet recorded 2 different months.
        next_month_total = max(
            0,
            float(expense_df["Amount"].mean() * len(expense_df))
        )

        st.info(
            f"📌 Early estimate: around ₹{next_month_total:,.0f}. "
            "Add records from more months for a stronger forecast."
        )
    else:
        next_month_total = 0
        st.info("Add at least 2 expenses to unlock the forecast.")

    # =====================================================
    # FEATURE 12 — AI SPENDING RECOMMENDATION
    # =====================================================
    st.markdown("### 12 • 🧠 AI Spending Recommendation")

    if len(expense_df):
        category_data = expense_df.groupby("Category")["Amount"].sum()
        top_category = category_data.idxmax()
        top_amount = float(category_data.max())
        top_share = (top_amount / total_expense * 100) if total_expense else 0

        if top_share >= 60:
            recommendation = (
                f"{top_category} is your biggest spending area at "
                f"{top_share:.0f}% of total spending. "
                "Try reducing optional purchases in this category first."
            )
        elif top_share >= 35:
            recommendation = (
                f"{top_category} leads your spending at "
                f"{top_share:.0f}%. "
                "Set a small category limit to improve your savings."
            )
        else:
            recommendation = (
                "Your spending is spread across categories. "
                "Keep your current budget discipline and review the top "
                "category before large purchases."
            )

        st.info("💡 " + recommendation)
    else:
        st.info("Add expenses to receive a personalized AI recommendation.")

    # =====================================================
    # UNIQUE AI PROGRESS / LINE GRAPH
    # =====================================================
    st.markdown("### 📈 AI Spending Journey")
    st.caption("Actual spending trend with the AI forecast point.")

    if len(expense_df) >= 2:
        graph_df = expense_df.copy()

        if "Date" in graph_df.columns:
            graph_df["Graph Date"] = pd.to_datetime(
                graph_df["Date"], errors="coerce"
            )
            graph_df = graph_df.sort_values("Graph Date")

        amounts = graph_df["Amount"].astype(float).tolist()

        X = np.arange(len(amounts)).reshape(-1, 1)
        y = np.array(amounts)

        journey_model = LinearRegression()
        journey_model.fit(X, y)

        future_value = max(
            0,
            float(journey_model.predict([[len(amounts)]])[0])
        )

        labels = [str(i + 1) for i in range(len(amounts))] + ["AI"]
        values = amounts + [future_value]

        fig_ai, ax_ai = plt.subplots(figsize=(12, 3.8))
        fig_ai.patch.set_alpha(0)
        ax_ai.set_facecolor("none")

        ax_ai.plot(
            labels[:-1],
            amounts,
            marker="o",
            linewidth=2.5,
            label="Actual Spending"
        )
        ax_ai.plot(
            [labels[-2], labels[-1]],
            [amounts[-1], future_value],
            linestyle="--",
            linewidth=2.5,
            label="AI Forecast"
        )

        ax_ai.axhline(
            budget,
            linestyle=":",
            linewidth=1.8,
            label="Personal Budget"
        )

        ax_ai.set_ylabel("₹", color="white")
        ax_ai.tick_params(axis="x", colors="white")
        ax_ai.tick_params(axis="y", colors="white")
        ax_ai.grid(axis="y", alpha=.12)

        for spine in ax_ai.spines.values():
            spine.set_color("#28658c")

        ax_ai.legend(
            facecolor="#092640",
            edgecolor="#28658c",
            labelcolor="white"
        )

        plt.tight_layout()
        st.pyplot(fig_ai, transparent=True)
        plt.close(fig_ai)

        st.caption(
            f"AI forecast point: ₹{future_value:,.0f} • "
            f"Personal budget: ₹{budget:,.0f}"
        )
    else:
        st.info("Add at least 2 expenses to unlock the AI spending journey.")

    # =====================================================
    # SIMPLE HOW AI WORKS
    # =====================================================
    with st.expander("⚙️ How AI Works"):
        st.write(
            "🎯 Budget → AI compares spending with the customer's own budget."
        )
        st.write(
            "🔮 Prediction → Linear Regression learns from previous values."
        )
        st.write(
            "🚨 Alerts → AI checks budget, bills and unusually high expenses."
        )
        st.write(
            "🎯 Top Category → AI finds where the customer spends the most."
        )
        st.write(
            "📈 Trend → AI compares earlier and recent spending."
        )
        st.write(
            "💰 Savings → AI estimates a simple possible saving amount."
        )
        st.write(
            "🛒 Purchase Alert → AI checks whether spending is getting too high."
        )
        st.write(
            "🔮 Forecast → AI uses previous monthly totals to estimate next month's expense."
        )
        st.write(
            "🧠 Recommendation → AI identifies the strongest spending category and suggests a simple action."
        )
        st.write(
            "📈 Spending Journey → The line graph shows actual spending, the AI forecast and the personal budget."
        )

    st.markdown(
        """
        <div class="sh-card">
            <div class="sh-pill">SIGMA MODE</div>
            <h2>Track less. Understand more.</h2>
            <div class="sh-muted">
                Simple AI • Personal budget • Clear decisions
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

elif menu == "Reports":

    st.markdown(
        """
        <div class="sh-hero">
            <div class="sh-pill">📑 EXECUTIVE MODE</div>
            <h1>SmartHome AI Report</h1>
            <div class="sh-muted">Decision-ready household summary.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    grocery_df = pd.read_sql_query(
        "SELECT * FROM Grocery WHERE User_Email=?",
        conn,
        params=(st.session_state.email,)
    )

    medicine_df = pd.read_sql_query(
        "SELECT * FROM Medicines WHERE User_Email=?",
        conn,
        params=(st.session_state.email,)
    )

    bill_df = pd.read_sql_query(
        "SELECT * FROM Bills WHERE User_Email=?",
        conn,
        params=(st.session_state.email,)
    )

    expense_df = pd.read_sql_query(
        "SELECT * FROM Expenses WHERE User_Email=?",
        conn,
        params=(st.session_state.email,)
    )

    a, b, c, d = st.columns(4)

    a.metric("🛒 GROCERIES", len(grocery_df))
    b.metric("💊 MEDICINES", len(medicine_df))
    c.metric("🧾 BILLS", len(bill_df))
    d.metric("💰 EXPENSES", len(expense_df))

    total_expense = expense_df["Amount"].sum() if len(expense_df) else 0
    total_bill = bill_df["Amount"].sum() if len(bill_df) else 0
    pending = len(bill_df[bill_df["Status"] == "Pending"]) if len(bill_df) else 0

    st.markdown("### 💰 Financial Snapshot")

    x, y, z = st.columns(3)

    x.metric("Total Expense", f"₹{total_expense:,.0f}")
    y.metric("Total Bill Value", f"₹{total_bill:,.0f}")
    z.metric("Pending Bills", pending)

    if len(expense_df):

        category_data = expense_df.groupby("Category")["Amount"].sum()
        top_category = category_data.idxmax()

        st.success(
            f"🧠 Executive Insight: **{top_category}** is your highest spending category."
        )

    if pending:
        st.warning(f"⚠️ {pending} bill(s) are still pending.")
    else:
        st.success("✅ No pending bills.")

    st.markdown(
        '<div class="sh-card"><div class="sh-pill">SIGMA REPORT</div>'
        '<h3>Control the numbers. Control the outcome.</h3>'
        '<div class="sh-muted">No unnecessary tables — only the information that matters.</div></div>',
        unsafe_allow_html=True
    )


elif menu == "About":

    st.markdown(
        """
        <div class="sh-hero">
            <div class="sh-pill">🏠 SMART • ANALYTICAL • INTELLIGENT</div>
            <h1>SmartHome AI</h1>
            <div class="sh-muted">Smart Data → Smarter Decisions.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    a, b, c = st.columns(3)

    with a:
        st.markdown(
            '<div class="sh-card"><h3>🗄️ MANAGE</h3>'
            '<div class="sh-muted">Bills, expenses, groceries, medicines and documents.</div></div>',
            unsafe_allow_html=True
        )

    with b:
        st.markdown(
            '<div class="sh-card"><h3>📊 ANALYZE</h3>'
            '<div class="sh-muted">Charts, trends, categories and household insights.</div></div>',
            unsafe_allow_html=True
        )

    with c:
        st.markdown(
            '<div class="sh-card"><h3>🤖 PREDICT</h3>'
            '<div class="sh-muted">Simple machine learning and intelligent alerts.</div></div>',
            unsafe_allow_html=True
        )

    st.markdown(
        '<div class="sh-card" style="margin-bottom:16px;">'
        '<div class="sh-pill">PROJECT DEVELOPER</div>'
        '<div style="font-size:24px;font-weight:850;margin-top:10px;">Soham Patole</div>'
        '<div class="sh-muted">Diploma in Information Technology • SmartHome AI</div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("### 🛠️ Technology Stack")

    st.write(
        "🐍 Python  •  🎨 Streamlit  •  🗄️ SQLite  •  "
        "📊 Pandas  •  🔢 NumPy  •  📈 Matplotlib  •  🤖 Scikit-learn"
    )

    st.markdown(
        '<div class="sh-card" style="text-align:center;">'
        '<div class="sh-pill">SIGMA PRINCIPLE</div>'
        '<h2>Manage. Analyze. Predict.</h2>'
        '<div class="sh-muted">Build quietly. Let the results speak.</div></div>',
        unsafe_allow_html=True
    )


st.markdown(
    """
    <div class="sh-footer">
        🏠 SmartHome AI • Intelligent Home Management • Simple • Private • Smart
    </div>
    """,
    unsafe_allow_html=True
)
