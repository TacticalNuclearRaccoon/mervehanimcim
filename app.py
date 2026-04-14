import streamlit as st

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Weekly Diet Planner",
    page_icon="🥗",
    layout="wide",
)

st.image('chonk.png', width=200)


# ── Data definitions ───────────────────────────────────────────────────────────
DAYS = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7"]

FIXED_MEALS = {
    "Breakfast": [
        "1 cup of tea", "1 egg", "1 piece of cheese",
        "2 slices of whole flavour bread", "5 olives", "2 nuts", "greens"
    ],
    "After Breakfast": ["1 piece of fruit", "1 glass of milk", "1 biscuit"],
    "After Lunch":     ["1 piece of fruit", "5 pieces of almonds"],
    "After Dinner":    ["1 piece of fruit", "1 glass of kefir"],
}

LUNCH_FIXED          = ["4 tbs vegetables", "2 pieces of breast"]
LUNCH_DAIRY_OPTIONS  = ["Yoghurt", "Ayran", "Tzatziki"]

DINNER_PROTEIN_OPTIONS = [
    "60g meat (2 meatballs)", "Chicken", "Fish",
    "Vegetable protein (5 tbs)", "Cheese (1 matchbox)", "1 egg"
]
DINNER_VEG_OPTIONS  = ["Cooked vegetables (4 tbs)", "Salad"]
DINNER_CARB_OPTIONS = ["Rice (2 tbs)", "Pasta (2 tbs)", "1 cup of soup"]


def empty_day():
    return {
        "lunch_dairy":    LUNCH_DAIRY_OPTIONS[0],
        "dinner_protein": DINNER_PROTEIN_OPTIONS[0],
        "dinner_veg":     DINNER_VEG_OPTIONS[0],
        "dinner_carb":    DINNER_CARB_OPTIONS[0],
    }


# ── Session state ──────────────────────────────────────────────────────────────
if "menu" not in st.session_state:
    st.session_state.menu = {day: empty_day() for day in DAYS}


# ── Helpers ────────────────────────────────────────────────────────────────────
def show_fixed(items):
    for item in items:
        st.write(f"• {item}")


def build_shopping_list():
    """
    Aggregate all ingredients needed for the week.
    Returns a dict: { category: { item: count } }
    Fixed items are counted across all 7 days; variable items counted per selection.
    """
    from collections import defaultdict
    shop = defaultdict(lambda: defaultdict(int))

    for day in DAYS:
        d = st.session_state.menu[day]

        # ── Breakfast (fixed, every day) ──────────────────────────────────────
        shop["☕ Breakfast"]["Tea bags"]            += 1
        shop["☕ Breakfast"]["Eggs"]                += 1   # breakfast egg
        shop["☕ Breakfast"]["Cheese (slices)"]     += 1
        shop["☕ Breakfast"]["Whole flavour bread (slices)"] += 2
        shop["☕ Breakfast"]["Olives"]              += 5
        shop["☕ Breakfast"]["Walnuts / nuts"]       += 2
        shop["☕ Breakfast"]["Greens (handful)"]    += 1

        # ── After Breakfast (fixed) ───────────────────────────────────────────
        shop["🍎 Fruits"]["Fruit (any)"]            += 3   # after bfast + after lunch + after dinner
        shop["🥛 Dairy & Drinks"]["Milk (glasses)"] += 1
        shop["🍪 Snacks"]["Biscuits"]               += 1

        # ── Lunch fixed ───────────────────────────────────────────────────────
        shop["🥦 Vegetables"]["Vegetables (4 tbs)"] += 1
        shop["🍗 Meat & Protein"]["Chicken breast (pieces)"] += 2

        # ── Lunch dairy (variable) ────────────────────────────────────────────
        dairy = d["lunch_dairy"]
        shop["🥛 Dairy & Drinks"][dairy]            += 1

        # ── After Lunch (fixed) ───────────────────────────────────────────────
        shop["🥜 Nuts & Seeds"]["Almonds"]          += 5

        # ── Dinner protein (variable) ─────────────────────────────────────────
        protein = d["dinner_protein"]
        shop["🍗 Meat & Protein"][protein]          += 1

        # ── Dinner vegetable (variable) ───────────────────────────────────────
        veg = d["dinner_veg"]
        shop["🥦 Vegetables"][veg]                  += 1

        # ── Dinner carb (variable) ────────────────────────────────────────────
        carb = d["dinner_carb"]
        shop["🌾 Carbs"][carb]                      += 1

        # ── After Dinner (fixed) ──────────────────────────────────────────────
        shop["🥛 Dairy & Drinks"]["Kefir (glasses)"] += 1

    return shop


def build_shopping_text(shop):
    lines = ["WEEKLY SHOPPING LIST", "=" * 50,
             "Assuming an empty fridge — covers all 7 days.", ""]
    for category, items in shop.items():
        lines.append(category)
        lines.append("-" * len(category))
        for item, qty in items.items():
            lines.append(f"  {item}: {qty}x")
        lines.append("")
    return "\n".join(lines)


def build_summary_text():
    lines = ["WEEKLY DIET MENU", "=" * 50, ""]
    for day in DAYS:
        d = st.session_state.menu[day]
        lines.append(f"── {day.upper()} ──")
        lines.append("BREAKFAST:       " + " | ".join(FIXED_MEALS["Breakfast"]))
        lines.append("AFTER BREAKFAST: " + " | ".join(FIXED_MEALS["After Breakfast"]))
        lines.append("LUNCH:           " + " | ".join(LUNCH_FIXED) + " | " + d["lunch_dairy"])
        lines.append("AFTER LUNCH:     " + " | ".join(FIXED_MEALS["After Lunch"]))
        lines.append(f"DINNER:          {d['dinner_protein']} | {d['dinner_veg']} | {d['dinner_carb']}")
        lines.append("AFTER DINNER:    " + " | ".join(FIXED_MEALS["After Dinner"]))
        lines.append("")
    return "\n".join(lines)


# ── App title ──────────────────────────────────────────────────────────────────
st.title("🥗 Weekly Diet Planner")
st.caption("Compose your meals for the week — select your options for each day.")

tab_labels = DAYS + ["📋 Weekly Summary", "🛒 Shopping List"]
tabs = st.tabs(tab_labels)

# ── Day tabs ───────────────────────────────────────────────────────────────────
for i, day in enumerate(DAYS):
    with tabs[i]:
        st.header(day)
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🌅 Breakfast")
            show_fixed(FIXED_MEALS["Breakfast"])

            st.divider()
            st.subheader("🍎 After Breakfast")
            show_fixed(FIXED_MEALS["After Breakfast"])

            st.divider()
            st.subheader("🥗 Lunch")
            show_fixed(LUNCH_FIXED)
            selected_dairy = st.selectbox(
                "Dairy option",
                LUNCH_DAIRY_OPTIONS,
                index=LUNCH_DAIRY_OPTIONS.index(st.session_state.menu[day]["lunch_dairy"]),
                key=f"lunch_dairy_{day}"
            )
            st.session_state.menu[day]["lunch_dairy"] = selected_dairy

            st.divider()
            st.subheader("🥜 After Lunch")
            show_fixed(FIXED_MEALS["After Lunch"])

        with col2:
            st.subheader("🍽️ Dinner")
            selected_protein = st.selectbox(
                "Protein",
                DINNER_PROTEIN_OPTIONS,
                index=DINNER_PROTEIN_OPTIONS.index(st.session_state.menu[day]["dinner_protein"]),
                key=f"dinner_protein_{day}"
            )
            st.session_state.menu[day]["dinner_protein"] = selected_protein

            selected_veg = st.selectbox(
                "Vegetable",
                DINNER_VEG_OPTIONS,
                index=DINNER_VEG_OPTIONS.index(st.session_state.menu[day]["dinner_veg"]),
                key=f"dinner_veg_{day}"
            )
            st.session_state.menu[day]["dinner_veg"] = selected_veg

            selected_carb = st.selectbox(
                "Carbohydrate",
                DINNER_CARB_OPTIONS,
                index=DINNER_CARB_OPTIONS.index(st.session_state.menu[day]["dinner_carb"]),
                key=f"dinner_carb_{day}"
            )
            st.session_state.menu[day]["dinner_carb"] = selected_carb

            st.divider()
            st.subheader("🌙 After Dinner")
            show_fixed(FIXED_MEALS["After Dinner"])

# ── Summary tab ────────────────────────────────────────────────────────────────
with tabs[-2]:
    st.header("📋 Weekly Summary")

    rows = []
    for day in DAYS:
        d = st.session_state.menu[day]
        rows.append({
            "Day":             day,
            "🌅 Breakfast":    ", ".join(FIXED_MEALS["Breakfast"]),
            "🍎 After Bfast":  ", ".join(FIXED_MEALS["After Breakfast"]),
            "🥗 Lunch":        ", ".join(LUNCH_FIXED) + f", {d['lunch_dairy']}",
            "🥜 After Lunch":  ", ".join(FIXED_MEALS["After Lunch"]),
            "🍽️ Dinner":      f"{d['dinner_protein']}, {d['dinner_veg']}, {d['dinner_carb']}",
            "🌙 After Dinner": ", ".join(FIXED_MEALS["After Dinner"]),
        })

    st.dataframe(rows, use_container_width=True, hide_index=True)

    st.divider()
    col_dl, col_reset, _ = st.columns([1, 1, 4])
    with col_dl:
        st.download_button(
            label="⬇️ Download as .txt",
            data=build_summary_text(),
            file_name="weekly_diet_menu.txt",
            mime="text/plain"
        )
    with col_reset:
        if st.button("🔄 Reset All"):
            st.session_state.menu = {day: empty_day() for day in DAYS}
            st.rerun()

# ── Shopping list tab ──────────────────────────────────────────────────────────
with tabs[-1]:
    st.header("🛒 Weekly Shopping List")
    st.caption("All ingredients needed for the week — assuming an empty fridge.")

    shop = build_shopping_list()

    # Display category by category in columns
    categories = list(shop.keys())
    col_a, col_b = st.columns(2)
    for idx, category in enumerate(categories):
        col = col_a if idx % 2 == 0 else col_b
        with col:
            st.subheader(category)
            rows = [{"Item": item, "Quantity": f"{qty}x"}
                    for item, qty in shop[category].items()]
            st.dataframe(rows, use_container_width=True, hide_index=True)

    st.divider()
    st.download_button(
        label="⬇️ Download Shopping List as .txt",
        data=build_shopping_text(shop),
        file_name="weekly_shopping_list.txt",
        mime="text/plain"
    )
