import json
from pathlib import Path

import streamlit as st

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Haftalık diyet planı",
    page_icon="🥗",
    layout="wide",
)

st.image('chonk3.png')

# ── Data definitions ───────────────────────────────────────────────────────────

data_path = Path(__file__).parent / "meal_data.json"


def load_meal_data(path: Path):
    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        st.error(f"Missing data file: {path}")
        st.stop()
    except json.JSONDecodeError as exc:
        st.error(f"Invalid JSON in {path}: {exc}")
        st.stop()


meal_data = load_meal_data(data_path)

FIXED_MEALS = meal_data["FIXED_MEALS"]
LUNCH_FIXED = meal_data["LUNCH_FIXED"]
LUNCH_DAIRY_OPTIONS = meal_data["LUNCH_DAIRY_OPTIONS"]
DINNER_PROTEIN_OPTIONS = meal_data["DINNER_PROTEIN_OPTIONS"]
DINNER_VEG_OPTIONS = meal_data["DINNER_VEG_OPTIONS"]
DINNER_CARB_OPTIONS = meal_data["DINNER_CARB_OPTIONS"]


def empty_day():
    return {
        "lunch_dairy":    LUNCH_DAIRY_OPTIONS[0],
        "dinner_protein": DINNER_PROTEIN_OPTIONS[0],
        "dinner_veg":     DINNER_VEG_OPTIONS[0],
        "dinner_carb":    DINNER_CARB_OPTIONS[0],
    }

# ── Helpers ────────────────────────────────────────────────────────────────────
def show_fixed(items):
    for item in items:
        st.write(f"• {item}")


# ── App title ──────────────────────────────────────────────────────────────────
st.title("🥗 Haftalık diyet planı")
st.caption("Zayıflayacağız falan böyle...")

# ── Day tabs ───────────────────────────────────────────────────────────────────
st.header("📅 Bu hafta")
col1, col2 = st.columns(2)
with col1:
    st.subheader("🌅 Kahvaltı")
    show_fixed(FIXED_MEALS["Breakfast"])
    st.divider()
    st.subheader("🍎 Kahvaltıdan Sonra")
    show_fixed(FIXED_MEALS["After Breakfast"])
    st.divider()
    st.subheader("🥗 Öğle Yemeği")
    show_fixed(LUNCH_FIXED)
    selected_dairy = st.selectbox(
        "Dairy option",
        LUNCH_DAIRY_OPTIONS)
    st.divider()
    st.subheader("🥜 Ara öğün")
    show_fixed(FIXED_MEALS["After Lunch"])

with col2:
    st.subheader("🍽️ Aksam yemegi")
    selected_protein = st.selectbox(
        "Protein",
        DINNER_PROTEIN_OPTIONS)
    selected_veg = st.selectbox(
        "Vegetable",
        DINNER_VEG_OPTIONS)
    selected_carb = st.selectbox(
        "Carbohydrate",
        DINNER_CARB_OPTIONS)
    st.divider()
    st.subheader("🌙 After Dinner")
    show_fixed(FIXED_MEALS["After Dinner"])