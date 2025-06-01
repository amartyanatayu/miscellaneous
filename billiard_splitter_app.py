import streamlit as st

st.set_page_config(page_title="Billiard Bill Splitter", layout="centered")

st.title("🎱 Billiard Bill Splitter")
st.markdown("Split your billiard bill fairly among friends with different sessions and food.")

# --- Setup Rates ---
st.header("1. Set Rates per Minute")

with st.form("rate_form"):
    reg_day = st.number_input("Regular - Day", min_value=0.0, value=670.0)
    reg_night = st.number_input("Regular - Night", min_value=0.0, value=840.0)
    vip_day = st.number_input("VIP - Day", min_value=0.0, value=1000.0)
    vip_night = st.number_input("VIP - Night", min_value=0.0, value=1200.0)
    submitted_rates = st.form_submit_button("Confirm Rates")

if submitted_rates:
    rates = {
        "reg": {"day": reg_day, "night": reg_night},
        "vip": {"day": vip_day, "night": vip_night}
    }
    st.success("Rates saved!")

# --- Input People ---
people_data = []
st.header("2. Add People and Their Sessions")

num_people = st.number_input("How many people?", min_value=1, step=1, value=2)

for i in range(int(num_people)):
    with st.expander(f"Person {i+1} Info"):
        name = st.text_input(f"Name of Person {i+1}", key=f"name_{i}")
        num_sessions = st.number_input(f"Number of Sessions for {name}", min_value=1, step=1, key=f"sess_{i}")
        sessions = []
        for j in range(int(num_sessions)):
            st.markdown(f"**Session {j+1}**")
            table_type = st.selectbox("Table Type", ["reg", "vip"], key=f"type_{i}_{j}")
            shift = st.selectbox("Shift", ["day", "night"], key=f"shift_{i}_{j}")
            minutes = st.number_input("Minutes Played", min_value=1.0, step=1.0, key=f"min_{i}_{j}")
            sessions.append({"table_type": table_type, "shift": shift, "minutes": minutes})

        st.markdown("**Food & Drinks**")
        food_items = []
        num_food = st.number_input(f"Number of items for {name}", min_value=0, step=1, key=f"food_{i}")
        for k in range(int(num_food)):
            item = st.text_input(f"Item {k+1} name", key=f"item_{i}_{k}")
            price = st.number_input(f"Item {k+1} price", min_value=0.0, key=f"price_{i}_{k}")
            food_items.append({"item": item, "price": price})

        people_data.append({
            "name": name,
            "sessions": sessions,
            "food": food_items
        })

# --- Service Charge ---
st.header("3. Service Charge")
service_charge = st.number_input("Total Service Charge (Rp)", min_value=0.0, step=100.0)

# --- Calculate Bills ---
if st.button("💸 Calculate Split"):
    st.header("4. Bill Summary")
    service_per_person = service_charge / len(people_data)

    for person in people_data:
        name = person["name"]
        table_cost = 0
        for session in person["sessions"]:
            rate = rates[session["table_type"]][session["shift"]]
            table_cost += session["minutes"] * rate

        food_total = sum(item["price"] for item in person["food"])
        subtotal = table_cost + food_total + service_per_person
        tax = 0.10 * subtotal
        total = subtotal + tax

        st.subheader(f"{name}")
        st.write(f"🎱 Table Cost: Rp {table_cost:,.0f}")
        st.write(f"🍴 Food & Drinks: Rp {food_total:,.0f}")
        st.write(f"🛎️ Service Share: Rp {service_per_person:,.0f}")
        st.write(f"💰 Subtotal: Rp {subtotal:,.0f}")
        st.write(f"📊 Tax (10%): Rp {tax:,.0f}")
        st.write(f"✅ **Total: Rp {total:,.0f}**")

