import pandas as pd
import streamlit as st


# 1. The same reusable class pattern as your notebook.
class BouquetCost:
    def __init__(self, hourly_rate):
        self.hourly_rate = hourly_rate

    @classmethod
    def from_dict(cls, data):
        return cls(hourly_rate=data["hourly_rate"])

    def cost(self, materials_used, parking, hours, other_costs):
        return materials_used + parking + hours * self.hourly_rate + other_costs


# 2. Dashboard layout.
st.set_page_config(page_title="FloraAI Cost Dashboard", page_icon="🌷", layout="wide")
st.title("🌷 FloraAI Cost Dashboard")
st.caption("cost planning tool")
st.info(
    "Planning estimates, not recorded sales."
)


# 3. Sidebar inputs. Streamlit reruns calculations when these change.
st.sidebar.header("1. Supplier and output")
supplier = st.sidebar.selectbox("Supplier", ["Trader Joe's", "Downtown Flower Market"])
is_tj = supplier == "Trader Joe's"
size_options = ["Medium"] if is_tj else ["Medium", "Large", "Small"]
size = st.sidebar.selectbox("Bouquet size", size_options)
scenario_key = f"{supplier}_{size}"
default_yield = 1 if is_tj else {"Medium": 2, "Large": 1, "Small": 3}[size]
bouquets = st.sidebar.number_input(
    "Bouquets from this batch",
    min_value=1, value=default_yield, step=1, key=f"{scenario_key}_yield",
    help="Expected output, not confirmed production. Update after testing.",
)

st.sidebar.header("2. Materials")
main_bunches = st.sidebar.number_input("Main flower bunches", min_value=0, value=3, step=1)
main_price = st.sidebar.number_input(
    "Price per main bunch ($)", min_value=0.0,
    value=12.99 if is_tj else 13.99, step=0.50, key=f"{supplier}_main_price",
    help="Your Downtown planning range is $10–$20 per bunch.",
)
green_bunches = st.sidebar.number_input("Greenery bunches", min_value=0, value=2, step=1)
green_price = st.sidebar.number_input(
    "Price per greenery bunch ($)", min_value=0.0,
    value=3.99 if is_tj else 6.99, step=0.50, key=f"{supplier}_green_price",
    help="Your Downtown planning range is $5–$15 per bunch.",
)
wrapping = st.sidebar.number_input(
    "Wrapping allocated to this batch ($)", min_value=0.0, value=10.91, step=0.50,
    key=f"{scenario_key}_wrapping",
    help="$10.91 is a starting assumption. Allocate the wrapping used for this batch, not a whole roll if some remains.",
)
unused = st.sidebar.number_input(
    "Unused flowers/greenery value ($)", min_value=0.0, value=0.0, step=0.50,
    key=f"{scenario_key}_unused",
    help="Subtract only unused flowers/greenery here. Wrapping is already entered by allocated use.",
)

st.sidebar.header("3. Batch time and expenses")
hours = st.sidebar.number_input(
    "Total batch hours (including shopping)", min_value=0.0, value=4.0, step=0.25,
    key=f"{scenario_key}_hours",
    help="Four hours is an editable assumption. Two bouquets may take longer than one; measure the entire batch.",
)
hourly_rate = st.sidebar.number_input(
    "Assumed hourly labor rate ($)", min_value=0.0, value=20.0, step=1.0,
)
parking = st.sidebar.number_input(
    "Parking for the batch ($)", min_value=0.0,
    value=0.0 if is_tj else 10.35, step=0.50, key=f"{supplier}_parking",
    help="TJ parking is free per your notes. Downtown's $10.35 default comes from B002; confirm it for future trips.",
)
other = st.sidebar.number_input(
    "Other costs for this batch ($)", min_value=0.0, value=0.0, step=0.50,
    key=f"{scenario_key}_other",
    help="Add allocated delivery, travel, payment, generation or other order costs when relevant.",
)
selling_price = st.sidebar.number_input(
    "Scenario selling price per bouquet ($)", min_value=0.0, value=150.0, step=5.0,
    help="Hypothetical selling price before collected sales tax; not a recorded sale or a pricing recommendation.",
)


# 4. DataFrame and calculations.
plan = pd.DataFrame({
    "Item": ["Main flowers", "Greenery"],
    "Bunches": [main_bunches, green_bunches],
    "Price per bunch ($)": [main_price, green_price],
})
plan["Purchase cost ($)"] = (plan["Bunches"] * plan["Price per bunch ($)"]).round(2)
flower_spending = round(plan["Purchase cost ($)"].sum(), 2)

if unused > flower_spending:
    st.error("Unused flower value cannot exceed this batch's flower and greenery purchases.")
    st.stop()

config = {"labor": {"2026": {"hourly_rate": hourly_rate}}}
model = BouquetCost.from_dict(config["labor"]["2026"])
materials_used = flower_spending - unused + wrapping
labor_cost = hours * model.hourly_rate
batch_cost = model.cost(materials_used, parking, hours, other)
cost_per_bouquet = batch_cost / bouquets
contribution = selling_price - cost_per_bouquet
margin = contribution / selling_price * 100 if selling_price > 0 else None


# 5. Key numbers.
st.subheader(f"{supplier} · {size} · {bouquets} bouquet(s) per batch")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Batch cost", f"${batch_cost:,.2f}")
col2.metric("Cost per bouquet", f"${cost_per_bouquet:,.2f}")
col3.metric("Contribution per bouquet", f"${contribution:,.2f}")
col4.metric("Contribution margin", f"{margin:.1f}%" if margin is not None else "—")
st.caption(
    "Contribution is the amount remaining after the costs entered here, including assumed labor. "
    "It still needs to cover omitted costs, business overhead, and profit. "
)

left, right = st.columns(2)
with left:
    st.subheader("Purchase plan")
    st.dataframe(plan.round(2), hide_index=True)
    st.write(f"**Flower purchases:** ${flower_spending:.2f}")
    st.write(f"**Materials consumed, including wrapping:** ${materials_used:.2f}")

with right:
    st.subheader("Cost per bouquet")
    breakdown = pd.DataFrame({
        "Component": ["Materials used", "Assumed labor", "Parking", "Other costs"],
        "Cost per bouquet ($)": [
            materials_used / bouquets, labor_cost / bouquets,
            parking / bouquets, other / bouquets,
        ],
    }).set_index("Component")
    st.bar_chart(breakdown)


# 6. Price comparison, holding this selected batch's costs constant.
st.subheader("Compare selling prices")
prices = pd.DataFrame({"Selling price ($)": [100, 125, 150, 175, 200]})
prices["Cost per bouquet ($)"] = cost_per_bouquet
prices["Contribution ($)"] = prices["Selling price ($)"] - prices["Cost per bouquet ($)"]
prices["Contribution margin (%)"] = prices["Contribution ($)"] / prices["Selling price ($)"] * 100
st.dataframe(prices.round(2), hide_index=True)
st.caption("These are alternative price scenarios, not actual orders. Do not sum their contributions as revenue.")


# 7. Download all inputs and the selected scenario's results.
record = pd.DataFrame([{
    "status": "Planning scenario", "supplier": supplier, "size": size,
    "bouquets": bouquets, "main_bunches": main_bunches, "main_price": main_price,
    "green_bunches": green_bunches, "green_price": green_price,
    "flower_spending": flower_spending, "unused_flowers": unused,
    "wrapping_used": wrapping, "batch_hours": hours, "hourly_rate": hourly_rate,
    "parking": parking, "other_costs": other, "batch_cost": batch_cost,
    "cost_per_bouquet": cost_per_bouquet, "selling_price": selling_price,
    "contribution": contribution, "contribution_margin_pct": margin,
}]).round(2)
st.download_button(
    "Download this scenario",
    data=record.to_csv(index=False).encode("utf-8-sig"),
    file_name="floraai_cost_scenario.csv", mime="text/csv",
)
st.caption("Edits are planning inputs for this session; use Download to keep a copy. No OpenAI API key is required.")
