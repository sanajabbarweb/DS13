import streamlit as st
import pandas as pd
import altair as alt

# Load the CSV file
@st.cache_data
def load_data():
    data = pd.read_csv("FE1Dataset.csv")  # Replace with the actual path of your dataset
    return data

data = load_data()

# Streamlit App Title
st.title("Crime Index Dashboard")

# Sidebar Filters
st.sidebar.header("Filter Data")
countries = data["Country"].unique()
selected_country = st.sidebar.selectbox("Select Country", countries)

cities = data[data["Country"] == selected_country]["City"].unique()
selected_city = st.sidebar.selectbox("Select City", cities)

years = sorted(data["Year"].unique())
year_range = st.sidebar.slider("Select Year Range", min_value=int(years[0]), max_value=int(years[-1]), value=(int(years[0]), int(years[-1])))

# Filter Data
filtered_data = data[
    (data["Country"] == selected_country) &
    (data["City"] == selected_city) &
    (data["Year"] >= year_range[0]) &
    (data["Year"] <= year_range[1])
]

# Separate actual and predicted data
actual_data = filtered_data[filtered_data["Year"] <= 2024]
predicted_data = filtered_data[filtered_data["Year"] > 2023]

# Main Content
st.subheader(f"Crime Index in {selected_city}, {selected_country} ({year_range[0]}-{year_range[1]})")

if not filtered_data.empty:
    # Combine actual and predicted data for visualization
    actual_data["Type"] = "Actual"
    predicted_data["Type"] = "Predicted"
    combined_data = pd.concat([actual_data, predicted_data])

    # Create an Altair chart for Crime Index
    line_chart = alt.Chart(combined_data).mark_line().encode(
        x=alt.X("Year:O", title="Year"),
        y=alt.Y("City_Crime_Index:Q", title="Crime Index"),  # Changed column to 'City_Crime_Index'
        color=alt.Color("Type", scale=alt.Scale(domain=["Actual", "Predicted"], range=["darkblue", "lightblue"])),
        tooltip=[
            "Year", 
            "City_Crime_Index", 
            "Type", 
            "Rank", 
            "City_Safety_Index", 
            "Rating", 
            "Crime_to_Safety_Ratio",
            "Crime_Activity",
            "Crime_Review", 
            "Safety_Review"
        ]  # Updated tooltip to include other columns
    ).properties(
        width=700,
        height=400
    )

    # Show the Altair chart
    st.altair_chart(line_chart, use_container_width=True)

    # Show the additional features as a table below the chart
    st.subheader("Additional Information")
    additional_info = combined_data[[
        "Year", 
        "City_Crime_Index", 
        "Rank", 
        "City_Safety_Index", 
        "Rating", 
        "Crime_to_Safety_Ratio", 
        "Crime_Activity", 
        "Crime_Review", 
        "Safety_Review"
    ]]
    st.write(additional_info)

else:
    st.write("No data available for the selected filters.")