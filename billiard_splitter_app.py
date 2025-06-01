import streamlit as st
import pandas as pd

st.set_page_config(page_title="Billiard Bill Splitter", layout="centered")
st.title("🎱 Billiard Bill Splitter")

st.markdown("""
This tool helps you split billiard table + food + service charges + tax fairly between people.
""")

# --- Input: Rate Declaration ---
st.header("📋 Set Table Rates")
table_types = ["Reg", "VIP"]
shifts = ["Day", "Night"]
custom_rates = {}

for t_type in table_types:
    for shift in shifts:
        key = f"{t_type}_{shift}"
        rate = st.number_input(f"Rate for {t_type} - {shift} (Rp/min):", min_value=0, key=f"rate_{key}")
        custom_rates[key] = rate

# --- Input: Participants ---
st.header("👥 People & Food")
num_people = st.number_input("Number of People:", min_value=1, step=1, key="num_people")

people = {}

for i in range(num_people):
    with st.expander(f"Person {i+1} Details"):
        name = st.text_input(f"Name of Person {i+1}", key=f"name_{i}")
        food_items = []
        total_food = 0

        food_count = st.number_input(f"How many food/drink items for {name}?", min_value=0, step=1, key=f"food_count_{i}")
        for j in range(food_count):
            col1, col2 = st.columns([2, 1])
            with col1:
                item_name = st.text_input(f"  Item {j+1} Name", key=f"item_{i}_{j}")
            with col2:
                item_price = st.number_input(f"  Price", min_value=0.0, key=f"price_{i}_{j}")
            total_food += item_price
            food_items.append({"name": item_name, "price": item_price})

        people[name] = {
            "food_items": food_items,
            "food_total": total_food,
            "sessions": [],
            "table_total": 0
        }

# --- Input: Shared Sessions ---
st.header("🕒 Table Sessions")
session_count = st.number_input("Number of Shared Table Sessions:", min_value=0, step=1)

sessions = []

for s in range(session_count):
    with st.expander(f"Session {s+1}"):
        minutes = st.number_input("Minutes Played:", min_value=1, key=f"mins_{s}")
        table_type = st.selectbox("Table Type:", table_types, key=f"type_{s}")
        shift = st.selectbox("Shift:", shifts, key=f"shift_{s}")
        participants = st.multiselect("Participants:", options=list(people.keys()), key=f"participants_{s}")

        rate_key = f"{table_type}_{shift}"
        rate = custom_rates.get(rate_key, 0)
        total_cost = minutes * rate
        cost_per_person = total_cost / len(participants) if participants else 0

        sessions.append({
            "minutes": minutes,
            "table_type": table_type,
            "shift": shift,
            "rate": rate,
            "participants": participants,
            "total_cost": total_cost,
            "split_cost": cost_per_person
        })

# --- Input: Service Fee ---
st.header("💰 Other Charges")
service_cost = st.number_input("Total Service Cost:", min_value=0.0)
service_per_person = service_cost / num_people if num_people > 0 else 0

tax_rate = 0.10

# --- Calculate Bills ---
if st.button("💸 Calculate Bill"):
    # Assign table costs
    for session in sessions:
        for name in session["participants"]:
            if name in people:
                people[name]["sessions"].append(session)
                people[name]["table_total"] += session["split_cost"]

    # Show Results
    st.header("🧾 Final Bill")
    for name, data in people.items():
        st.subheader(f"{name}")
        table_total = data["table_total"]
        food_total = data["food_total"]
        subtotal = table_total + food_total
        subtotal_with_service = subtotal + service_per_person
        total = subtotal_with_service * (1 + tax_rate)

        with st.expander("🔍 Breakdown"):
            st.write("**Table Sessions:**")
            for session in data["sessions"]:
                st.write(f"{session['minutes']} min @ Rp{session['rate']} ({session['table_type']}, {session['shift']})")
                st.write(f"  → Shared with: {', '.join(session['participants'])}")
                st.write(f"  → Share: Rp{session['split_cost']:.0f}")
            st.write("**Food & Drinks:**")
            for item in data["food_items"]:
                st.write(f"- {item['name']}: Rp{item['price']:.0f}")
            st.write(f"**Service Cost Share:** Rp{service_per_person:.0f}")
            st.write(f"**Tax (10%) applied to subtotal+service.**")

        st.success(f"**Total: Rp{total:,.0f}**")
