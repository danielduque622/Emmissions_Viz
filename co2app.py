import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import squarify
import numpy as np

# Load the data
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
# Clean and prepare data
    df = df.rename(columns=lambda x: x.strip())
    df = df.rename(columns=lambda x: x.replace("_", " "))
    return df

file_path = 'data/owid-co2-data.csv'
df = load_data(file_path)

emission_columns = ["co2", "co2 per capita", "coal co2", "coal co2 per capita", 
                    "consumption co2", "consumption co2 per capita", "flaring co2", 
                    "flaring co2 per capita", "gas co2", "gas co2 per capita", 
                    "methane", "methane per capita", "nitrous oxide", 
                    "nitrous oxide per capita", "oil co2", "oil co2 per capita", 
                    "other industry co2"]

emission_columns_2 = ["co2", "coal co2", "consumption co2", "flaring co2", 
                      "gas co2", "methane", "nitrous oxide", "oil co2", "other industry co2"]

temp_columns = ["temperature change from ghg","temperature change from ch4","temperature change from co2",
"temperature change from n2o"]

#columns for correlations
corr_columns = ["gdp","population","co2 growth abs","co2", "co2 per capita", "coal co2", "coal co2 per capita", 
                    "consumption co2", "consumption co2 per capita", "flaring co2", 
                    "flaring co2 per capita", "gas co2", "gas co2 per capita", 
                    "methane", "methane per capita", "nitrous oxide", 
                    "nitrous oxide per capita", "oil co2", "oil co2 per capita", 
                    "other industry co2"]
    

if "Select Countries" not in st.session_state:
    st.session_state.countries = ["World"]
if "Select Emission Type" not in st.session_state:
    st.session_state.emission_type = emission_columns[0]
if "Select Year Range" not in st.session_state:
    st.session_state.years = (2000, 2020)
if "Select Columns to Analyze" not in st.session_state:
    st.session_state.corr_coumns = corr_columns[:3]

# App Title
st.markdown(
    """
    <style>
    .title-with-border {
        font-size: 36px;
        color: white;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7); /* Shadow effect */
        border: 1.5px solid white; /* White border */
        padding: 10px; /* Padding inside the border */
        display: inline-block; /* Ensures the border wraps neatly around the text */
        border-radius: 8px; /* Rounded corners for the border */
    }
    </style>
    <div class="title-with-border">Global CO₂ and Greenhouse Gas Emissions Exploration</div>
    """,
    unsafe_allow_html=True
)

st.markdown("Analyze emissions trends by country, year, and type of emissions")

st.markdown("Choose the type of analysis you would like to conduct using the drop down on the left pane")

# Page Navigation
page = st.sidebar.selectbox("Choose Analysis Type", ["Emmission Analysis", "Temperature Analysis", "Correlation Analysis","Data Dictionary and Sources"])

#emmission analysis page
if page == "Emmission Analysis":
    st.markdown("Filters")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        countries = st.multiselect(
            "Select Countries", 
            df["country"].unique()
            , default=st.session_state.get("countries", ["World"]))
    with col2:
        emission_type = st.selectbox("Select Emission Type", options=emission_columns, index=0)
    with col3:
        years = st.slider("Select Year Range", int(df["year"].min()), int(df["year"].max()), (2000, 2020))


    # Filtered Data
    @st.cache_data
    def filter_data(df, countries, years):
        return df[(df["country"].isin(countries)) & (df["year"].between(*years))]

    filtered_df = filter_data(df, st.session_state.countries, st.session_state.years)

    # Line Chart
    st.subheader("Emissions Over Time")
    fig, ax = plt.subplots(facecolor='none')
    for country in  st.session_state.countries:
        country_data = filtered_df[filtered_df["country"] == country]
        ax.plot(country_data["year"], country_data[st.session_state.emission_type], label=country)
    ax.set_title(f"{st.session_state.emission_type} Trends ({st.session_state.years[0]}-{st.session_state.years[1]})")
    ax.set_xlabel("Year")
    ax.set_ylabel("Emissions")
    ax.legend()
    ax.set_title("Time Series Chart", color='white')  
    ax.set_xlabel("Time", color='white')  
    ax.set_ylabel("Million Tonnes", color='white')  
    ax.tick_params(axis='x', colors='white')  
    ax.tick_params(axis='y', colors='white') 
    fig.patch.set_alpha(0)  # Transparent figure background
    ax.set_facecolor('none')  # Transparent plot background
    st.pyplot(fig)

    # White space line
    st.markdown(
        """
        <hr style="border: 1.5px solid white; margin: 20px 0;">
        """,
        unsafe_allow_html=True
    )

    # Bar Chart
    st.subheader("Country Comparison")
    avg_emissions = filtered_df.groupby("country")[st.session_state.emission_type].mean().sort_values()
    if avg_emissions.empty:
        st.warning("No data available for the selected filters.")
    else:
        fig, ax = plt.subplots(facecolor='none')
    ax.set_title("Category Values", color='white')  
    ax.set_xlabel("Categories", color='white')  
    ax.set_ylabel("Million Tonnes", color='white')  
    ax.tick_params(axis='x', colors='white', rotation=0)  
    ax.tick_params(axis='y', colors='white')  
    fig.patch.set_alpha(0)  # Transparent figure background
    ax.set_facecolor('none')  # Transparent plot background
    avg_emissions.plot(kind="bar", ax=ax)
    ax.set_title(f"Average {st.session_state.emission_type} Emissions ({st.session_state.years[0]}-{st.session_state.years[1]})")
    ax.set_xlabel("Emissions")
    st.pyplot(fig)

    # White space line
    st.markdown(
        """
        <hr style="border: 1.5px solid white; margin: 20px 0;">
        """,
        unsafe_allow_html=True
    )
    
    # Tree Chart
    st.subheader("Emission Type Distribution")
    # Summing the emissions
    total_emissions = filtered_df[emission_columns_2].sum()

    # Prepare data for the treemap
    sizes = total_emissions.values  # Values for each emission type
    sizes = sizes[sizes > 0]  # Remove zero or negative values
    labels = [f"{col}\n{val:.1f}%" for col, val in zip(emission_columns_2, (sizes / sizes.sum()) * 100)]  # Labels with percentages

    # Normalize sizes
    normed_sizes = (sizes / sizes.sum()) * 100

    # Generate at least 10 distinct colors using 'tab10'
    color_count = len(sizes)
    base_colors = plt.cm.tab10(np.linspace(0, 1, color_count))  # Get base colors
    colors = [(*color[:3], 0.8) for color in base_colors]  # Add transparency (alpha = 0.8)

    # Create the treemap    
    fig, ax = plt.subplots(figsize=(8, 6), facecolor='none')
    squarify.plot(
    sizes=sizes,
    label=labels,
    color=colors,
    alpha=0.5,
    ax=ax,
    text_kwargs={'color': 'white', 'fontsize': 10}  # Make labels white
    )

    ax.axis('off')  # Turn off axes
    st.pyplot(fig)

    # White space line
    st.markdown(
        """
        <hr style="border: 1.5px solid white; margin: 20px 0;">
        """,
        unsafe_allow_html=True
    )

    # Data Table
    st.subheader("Filtered Data")
    st.dataframe(filtered_df)

    # Download Filtered Data
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Filtered Data",
        data=csv,
        file_name="filtered_co2_data.csv",
        mime="text/csv"
    )

# Temp analysis Page
if page == "Temperature Analysis":
    st.markdown("Filters")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        countries = st.multiselect("Select Countries", df["country"].unique(), default=["World"])
    with col2:
        years = st.slider("Select Year Range", int(df["year"].min()), int(df["year"].max()), (2000, 2020))

    emission_type = st.selectbox("Select Emission Type", options=temp_columns, index=0)

    # Filtered Data
    @st.cache_data
    def filter_data(df, countries, years):
        return df[(df["country"].isin(countries)) & (df["year"].between(*years))]

    filtered_df = filter_data(df, st.session_state.countries, st.session_state.years)

    # Line Chart
    st.subheader("Temperature Change Over Time")
    fig, ax = plt.subplots(facecolor='none')
    for country in st.session_state.countries:
        country_data = filtered_df[filtered_df["country"] == country]
        ax.plot(country_data["year"], country_data[emission_type], label=country)
    ax.set_title(f"{emission_type} Trends ({st.session_state.years[0]}-{st.session_state.years[1]})")
    ax.set_xlabel("Year")
    ax.set_ylabel("Emissions")
    ax.legend()
    ax.set_title("Time Series Chart", color='white')  
    ax.set_xlabel("Time", color='white')  
    ax.set_ylabel("°C", color='white')  
    ax.tick_params(axis='x', colors='white')  
    ax.tick_params(axis='y', colors='white')  
    fig.patch.set_alpha(0)  # Transparent figure background
    ax.set_facecolor('none')  # Transparent plot background
    st.pyplot(fig)

    # White space line
    st.markdown(
        """
        <hr style="border: 1.5px solid white; margin: 20px 0;">
        """,
        unsafe_allow_html=True
    )

    # Bar Chart
    st.subheader("Country Comparison")
    avg_emissions = filtered_df.groupby("country")[emission_type].mean().sort_values()
    if avg_emissions.empty:
        st.warning("No data available for the selected filters.")
    else:
        fig, ax = plt.subplots(facecolor='none')
    ax.set_title("Category Values", color='white')  
    ax.set_xlabel("Categories", color='white')  
    ax.set_ylabel("°C", color='white')  
    ax.tick_params(axis='x', colors='white', rotation=0)  
    ax.tick_params(axis='y', colors='white')  
    fig.patch.set_alpha(0)  
    ax.set_facecolor('none')  
    avg_emissions.plot(kind="bar", ax=ax)
    ax.set_title(f"Average {emission_type} Emissions ({st.session_state.years[0]}-{st.session_state.years[1]})")
    ax.set_xlabel("Emissions")
    st.pyplot(fig)

        # White space line
    st.markdown(
        """
        <hr style="border: 1.5px solid white; margin: 20px 0;">
        """,
        unsafe_allow_html=True
    )
    
    # Tree Chart
    st.subheader("Emission Type Distribution")
    # Summing the emissions
    total_emissions = filtered_df[temp_columns].sum()

    # Prepare data for the treemap
    sizes = total_emissions.values  # Values for each emission type
    sizes = sizes[sizes > 0]  # Remove zero or negative values
    labels = [f"{col}\n{val:.1f}%" for col, val in zip(temp_columns, (sizes / sizes.sum()) * 100)]  # Labels with percentages

    # Normalize sizes
    normed_sizes = (sizes / sizes.sum()) * 100

    # Generate at least 10 distinct colors using 'tab10'
    color_count = len(sizes)
    base_colors = plt.cm.tab10(np.linspace(0, 1, color_count))  # Get base colors
    colors = [(*color[:3], 0.8) for color in base_colors]  # Add transparency (alpha = 0.8)

    # Create the treemap    
    fig, ax = plt.subplots(figsize=(8, 6), facecolor='none')
    squarify.plot(
    sizes=sizes,
    label=labels,
    color=colors,
    alpha=0.5,
    ax=ax,
    text_kwargs={'color': 'white', 'fontsize': 10}  # Make labels white
    )

    ax.axis('off')  # Turn off axes
    st.pyplot(fig)

        # White space line
    st.markdown(
        """
        <hr style="border: 1.5px solid white; margin: 20px 0;">
        """,
        unsafe_allow_html=True
    )

    # Data Table
    st.subheader("Filtered Data")
    st.dataframe(filtered_df)

    # Download Filtered Data
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Filtered Data",
        data=csv,
        file_name="filtered_co2_data.csv",
        mime="text/csv"
    )

if page == "Data Dictionary and Sources":
    DD = pd.read_csv("data/owid-co2-codebook.csv")
    st.dataframe(DD)

# Corr Analysis Page 
elif page == "Correlation Analysis":
    st.markdown("### Correlation Analysis")


    # Filters for Correlation Analysis
    st.session_state.countries = st.multiselect("Select Countries", df["country"].unique(), default=["World"], key="corr_countries")
    st.session_state.years = st.slider("Select Year Range", int(df["year"].min()), int(df["year"].max()), (2000, 2020), key="corr_years")
    st.session_state.corr_coumns = st.multiselect("Select Columns to Analyze", corr_columns, default=corr_columns[:3])

    # Filtered Data for Correlation
    filtered_corr_df = df[(df["country"].isin(st.session_state.countries)) & (df["year"].between(* st.session_state.years))]

    # Correlation Matrix
    if len(st.session_state.corr_coumns) > 1:
        correlation_matrix = filtered_corr_df[st.session_state.corr_coumns].corr()
        st.write(correlation_matrix)
        fig, ax = plt.subplots()
        cax = ax.matshow(correlation_matrix, cmap="coolwarm")
        # Add a colorbar with white labels
        cbar = plt.colorbar(cax)
        cbar.ax.yaxis.set_tick_params(color='white')
        plt.setp(plt.getp(cbar.ax, 'yticklabels'), color='white')
        ax.set_xticks(np.arange(len(st.session_state.corr_coumns)))
        ax.set_yticks(np.arange(len(st.session_state.corr_coumns)))
        ax.set_xticklabels(st.session_state.corr_coumns, rotation=90, color='white')
        ax.set_yticklabels(st.session_state.corr_coumns,color='white')
        # Set transparent background for figure and axes
        fig.patch.set_alpha(0)  # Transparent figure background
        ax.set_facecolor('none')  # Transparent axes background
        # Customize ticks and grid
        ax.tick_params(colors='white')  # White ticks
        ax.grid(False)  # Remove grid lines
        st.pyplot(fig)
    else:
        st.warning("Please select at least two columns for correlation analysis.")
