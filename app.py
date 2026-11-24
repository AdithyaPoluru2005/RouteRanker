
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="RouteRanker | Transit Analytics",
    page_icon="🚌",
    layout="wide"
)

BASE = os.path.dirname(os.path.abspath(__file__))

CITIES = [
    "delhi", "hyderabad", "bengaluru",
    "chennai", "mumbai", "pune"
]

MODEL_PATH = os.path.join(BASE, "data", "model_results")
INFERENCE_PATH = os.path.join(BASE, "data", "inference")
PROCESSED_PATH = os.path.join(BASE, "data", "processed")

# --------------------------------------------------
# 2. CUSTOM DESIGN

st.markdown("""
<style>
.stApp {
    background: #0B1220;
    color: #E6EDF7;
}
[data-testid="stAppViewContainer"] {
    background: #0B1220;
}
[data-testid="stHeader"] {
    background: #0B1220;
}
[data-testid="stSidebar"] {
    background: #111D30;
    border-right: 1px solid #26364A;
}
[data-testid="stSidebar"] * {
    color: #E6EDF7;
}
.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}
h1, h2, h3 {
    color: #F1F5FB !important;
    font-weight: 700;
}
p, label {
    color: #C5D1E2;
}
[data-testid="stMetric"] {
    background: #16243A !important;
    border: 1px solid #2B405C !important;
    border-radius: 15px;
    padding: 22px;
}
[data-testid="stMetricLabel"] {
    color: #9FB2CC !important;
}
[data-testid="stMetricValue"] {
    color: #35C6B4 !important;
}
[data-testid="stDataFrame"] {
    border: 1px solid #2B405C;
    border-radius: 12px;
}
.stSelectbox, .stMultiSelect {
    border-radius: 10px;
}
.stButton > button {
    background: #167D89;
    color: white;
    border: 1px solid #35C6B4;
    border-radius: 9px;
}
hr {
    border-color: #26364A;
}
</style>
""", unsafe_allow_html=True)

px.defaults.template = "plotly_dark"
px.defaults.color_discrete_sequence = [
    "#35C6B4", "#4F8CFF", "#F5B84B",
    "#A78BFA", "#F07F8B", "#63C7E8"
]


def show_chart(fig):
    fig.update_layout(
        template="plotly_dark",
        autosize=True,
        height=430,
        margin=dict(l=45, r=25, t=65, b=90),
        paper_bgcolor="#0B1220",
        plot_bgcolor="#111D30",
        font=dict(color="#E6EDF7", size=12),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.22,
            xanchor="left",
            x=0
        )
    )

    fig.update_xaxes(
        automargin=True,
        gridcolor="#26364A"
    )
    fig.update_yaxes(
        automargin=True,
        gridcolor="#26364A"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"responsive": True, "displayModeBar": False}
    )

# End custom design

# 3. DATA LOADING
# --------------------------------------------------

@st.cache_data
def load_csv(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame()


def city_file(folder, city, filename):
    return os.path.join(folder, city, filename)


def model_file(filename):
    return os.path.join(MODEL_PATH, filename)


def inference_file(filename):
    return os.path.join(INFERENCE_PATH, filename)


def get_route_data(city):
    path = city_file(
        PROCESSED_PATH, city, "route_profile.csv"
    )
    return load_csv(path)


def get_hourly_data(city):
    path = city_file(
        PROCESSED_PATH, city, "hourly_trip_counts.csv"
    )
    return load_csv(path)


def get_cluster_data(city, algorithm):
    if algorithm == "K-Means":
        filename = f"{city}_kmeans_inference.csv"
    else:
        filename = f"{city}_dbscan_inference.csv"

    return load_csv(inference_file(filename))


# --------------------------------------------------
# 4. SIDEBAR NAVIGATION
# --------------------------------------------------

st.sidebar.title("🚌 RouteRanker")
st.sidebar.caption("AI-Powered Public Transit Route Optimization")

page = st.sidebar.radio(
    "Dashboard Navigation",
    [
        "Home",
        "Dataset Overview",
        "Exploratory Data Analysis",
        "Route Analysis",
        "Clustering Results",
        "Model Predictions",
        "Route Optimization",
        "Metrics Comparison",
        "About"
    ]
)

city = st.sidebar.selectbox(
    "Select City",
    CITIES,
    format_func=lambda x: x.title()
)

st.sidebar.divider()
st.sidebar.caption("Data from RouteRanker Modules 1–6")

# Load selected city data
routes = get_route_data(city)
hourly = get_hourly_data(city)

# --------------------------------------------------
# 5. HOME
# --------------------------------------------------

if page == "Home":

    st.title("🚌 RouteRanker")
    st.subheader("AI-Powered Public Transit Route Optimization")

    st.markdown("""
    Welcome to RouteRanker!

    This dashboard brings together public transportation
    data analysis, machine learning results and hypothetical
    route schedule simulations for six Indian cities.

    Explore route information, clustering results,
    model predictions and optimization scenarios.
    """)

    st.divider()

    total_routes = 0
    total_trips = 0

    for c in CITIES:
        df = get_route_data(c)

        if not df.empty:
            total_routes += len(df)

            if "total_trips" in df.columns:
                total_trips += df["total_trips"].fillna(0).sum()

    col1, col2, col3 = st.columns(3)

    col1.metric("Cities Covered", len(CITIES))
    col2.metric("Total Routes", f"{total_routes:,}")
    col3.metric("Scheduled Trips", f"{total_trips:,.0f}")

    st.divider()

    st.subheader("Project Coverage")

    overview = pd.DataFrame({
        "City": [c.title() for c in CITIES],
        "Routes": [
            len(get_route_data(c)) for c in CITIES
        ]
    })

    fig = px.bar(
        overview,
        x="City",
        y="Routes",
        color="City",
        title="Route Distribution Across Six Cities"
    )

    show_chart(fig)

    st.info(
        "This project analyses scheduled public transport "
        "services. Scheduled trips do not represent actual "
        "passenger counts or occupancy."
    )

# --------------------------------------------------
# 6. DATASET OVERVIEW
# --------------------------------------------------

elif page == "Dataset Overview":

    st.title("Dataset Overview")
    st.write(f"Selected City: **{city.title()}**")

    if routes.empty:
        st.warning("Route dataset not found.")
    else:

        col1, col2 = st.columns(2)

        col1.metric("Total Records", f"{len(routes):,}")
        col2.metric("Total Features", len(routes.columns))

        st.subheader("Dataset Preview")
        st.dataframe(routes.head(100), use_container_width=True)

        st.subheader("Column Information")

        info = pd.DataFrame({
            "Column": routes.columns,
            "Data Type": routes.dtypes.astype(str).values,
            "Missing Values": routes.isnull().sum().values
        })

        st.dataframe(info, use_container_width=True)

        st.subheader("Statistical Summary")

        st.dataframe(
            routes.describe(include="all").fillna(""),
            use_container_width=True
        )

        st.subheader("Filter Routes")

        if "route_id" in routes.columns:
            selected_route = st.text_input(
                "Search Route ID"
            )

            filtered = routes.copy()

            if selected_route:
                filtered = filtered[
                    filtered["route_id"].astype(str)
                    .str.contains(selected_route, case=False, na=False)
                ]

            st.dataframe(filtered, use_container_width=True)

# --------------------------------------------------
# 7. EXPLORATORY DATA ANALYSIS
# --------------------------------------------------

elif page == "Exploratory Data Analysis":

    st.title("Exploratory Data Analysis")

    if routes.empty:
        st.warning("Route dataset not available.")
    else:

        st.subheader("Scheduled Trips Distribution")

        fig = px.histogram(
            routes,
            x="total_trips",
            nbins=30,
            title="Distribution of Scheduled Trips per Route"
        )

        show_chart(fig)

        st.subheader("Stops Distribution")

        fig = px.histogram(
            routes,
            x="total_stops",
            nbins=30,
            title="Distribution of Stops per Route"
        )

        show_chart(fig)

        st.subheader("Trips vs Stops")

        fig = px.scatter(
            routes,
            x="total_stops",
            y="total_trips",
            hover_data=["route_id"],
            title="Relationship Between Stops and Scheduled Trips"
        )

        show_chart(fig)

        st.subheader("Scheduled Trips by Service Hour")

        if not hourly.empty:

            hourly_summary = (
                hourly.groupby("departure_service_hour")["trip_count"]
                .sum()
                .reset_index()
                .sort_values("departure_service_hour")
            )

            fig = px.line(
                hourly_summary,
                x="departure_service_hour",
                y="trip_count",
                markers=True,
                title="Scheduled Trips by Service Hour"
            )

            show_chart(fig)

        else:
            st.info("Hourly trip data is unavailable.")

        numeric = routes.select_dtypes(include="number")

        if len(numeric.columns) > 1:

            st.subheader("Feature Correlation")

            fig = px.imshow(
                numeric.corr(),
                text_auto=True,
                aspect="auto",
                title="Correlation Between Numerical Features"
            )

            show_chart(fig)

# --------------------------------------------------
# 8. ROUTE ANALYSIS
# --------------------------------------------------

elif page == "Route Analysis":

    st.title("Route Analysis")

    if routes.empty:
        st.warning("Route data not available.")
    else:

        st.subheader(f"Route Details – {city.title()}")

        min_trips = float(routes["total_trips"].fillna(0).min())
        max_trips = float(routes["total_trips"].fillna(0).max())

        trip_range = st.slider(
            "Filter by Scheduled Trips",
            min_value=min_trips,
            max_value=max_trips,
            value=(min_trips, max_trips)
        )

        filtered = routes[
            routes["total_trips"].fillna(0).between(
                trip_range[0], trip_range[1]
            )
        ]

        st.metric("Matching Routes", len(filtered))

        st.dataframe(filtered, use_container_width=True)

        st.subheader("Top Routes by Scheduled Trips")

        top_routes = routes.nlargest(10, "total_trips")

        fig = px.bar(
            top_routes,
            x="route_id",
            y="total_trips",
            title="Top 10 Routes by Scheduled Trips"
        )

        show_chart(fig)

# --------------------------------------------------
# 9. CLUSTERING RESULTS
# --------------------------------------------------

elif page == "Clustering Results":

    st.title("Route Clustering Results")

    algorithm = st.radio(
        "Select Clustering Algorithm",
        ["K-Means", "DBSCAN"],
        horizontal=True
    )

    cluster_df = get_cluster_data(city, algorithm)

    if cluster_df.empty:
        st.warning("Clustering inference file not found.")
    else:

        cluster_column = (
            "KMeans_Inference_Cluster"
            if algorithm == "K-Means"
            else "DBSCAN_Inference_Cluster"
        )

        cluster_df[cluster_column] = (
            cluster_df[cluster_column].astype(str)
        )

        st.metric("Routes Analysed", len(cluster_df))

        st.subheader(f"{algorithm} Cluster Distribution")

        counts = (
            cluster_df[cluster_column]
            .value_counts()
            .rename_axis("Cluster")
            .reset_index(name="Routes")
        )

        fig = px.bar(
            counts,
            x="Cluster",
            y="Routes",
            color="Cluster",
            title=f"{algorithm} Cluster Distribution"
        )

        show_chart(fig)

        selected_cluster = st.multiselect(
            "Select Clusters",
            sorted(cluster_df[cluster_column].unique()),
            default=sorted(cluster_df[cluster_column].unique())
        )

        filtered = cluster_df[
            cluster_df[cluster_column].isin(selected_cluster)
        ]

        st.subheader("Cluster Visualization")

        fig = px.scatter(
            filtered,
            x="total_trips",
            y="total_stops",
            color=cluster_column,
            hover_data=["route_id"],
            title=f"{algorithm}: Routes by Cluster"
        )

        show_chart(fig)

        st.subheader("Cluster Records")

        st.dataframe(filtered, use_container_width=True)

        if algorithm == "DBSCAN":
            noise_count = (
                cluster_df[cluster_column] == "-1"
            ).sum()

            st.info(
                f"DBSCAN unassigned/noise records: {noise_count}. "
                "These are records for review, not confirmed inefficient routes."
            )

# --------------------------------------------------
# 10. MODEL PREDICTIONS
# --------------------------------------------------

elif page == "Model Predictions":

    st.title("Machine Learning Predictions")

    predictions = load_csv(
        model_file("classification_predictions.csv")
    )

    comparison = load_csv(
        model_file("classification_comparison.csv")
    )

    if predictions.empty:
        st.warning("Classification predictions not found.")
    else:

        selected_predictions = predictions[
            predictions["city"].astype(str).str.lower() == city
        ]

        st.subheader("Classification Results")

        st.caption(
            "These are test-set predictions from models trained "
            "using proxy labels derived from scheduled-trip frequency."
        )

        if selected_predictions.empty:
            st.info("No classification records for this city.")
        else:

            col1, col2 = st.columns(2)

            col1.metric(
                "Records Displayed",
                len(selected_predictions)
            )

            col2.metric(
                "Models Compared",
                "2"
            )

            st.subheader("Random Forest Predictions")

            rf_counts = (
                selected_predictions["RandomForest_Prediction"]
                .value_counts()
                .rename_axis("Category")
                .reset_index(name="Records")
            )

            fig = px.bar(
                rf_counts,
                x="Category",
                y="Records",
                color="Category",
                title="Random Forest Predicted Categories"
            )

            show_chart(fig)

            st.subheader("XGBoost Predictions")

            xgb_counts = (
                selected_predictions["XGBoost_Prediction"]
                .value_counts()
                .rename_axis("Category")
                .reset_index(name="Records")
            )

            fig = px.bar(
                xgb_counts,
                x="Category",
                y="Records",
                color="Category",
                title="XGBoost Predicted Categories"
            )

            show_chart(fig)

            st.subheader("Prediction Comparison")

            st.dataframe(
                selected_predictions,
                use_container_width=True
            )

        if not comparison.empty:
            st.subheader("Model Evaluation Results")
            st.dataframe(comparison, use_container_width=True)

        st.info(
            "Predicted categories are based on proxy labels, "
            "not actual passenger demand or occupancy. "
            "Prediction confidence scores are not displayed."
        )

# --------------------------------------------------
# 11. ROUTE OPTIMIZATION
# --------------------------------------------------

elif page == "Route Optimization":

    st.title("Route Optimization Suggestions")

    suggestions = load_csv(
        inference_file("route_review_suggestions.csv")
    )

    if not suggestions.empty:

        city_suggestions = suggestions[
            suggestions["City"].astype(str).str.lower() == city
        ]

        st.subheader("Routes Flagged for Review")

        st.metric(
            "Routes Requiring Review",
            len(city_suggestions)
        )

        st.dataframe(
            city_suggestions,
            use_container_width=True
        )

        if "Review_Reason" in city_suggestions.columns:

            reason_counts = (
                city_suggestions["Review_Reason"]
                .value_counts()
                .rename_axis("Reason")
                .reset_index(name="Routes")
            )

            fig = px.bar(
                reason_counts,
                x="Reason",
                y="Routes",
                title="Route Review Reasons"
            )

            show_chart(fig)

    else:
        st.warning("Route review suggestions not found.")

    st.divider()

    st.subheader("Simulated Schedule Adjustments")

    simulated = load_csv(
        inference_file(f"{city}_simulated_routes.csv")
    )

    if not simulated.empty:

        st.write(
            "The following values represent hypothetical schedule "
            "adjustments created in Module 6."
        )

        if {"Original_Trips", "Simulated_Trips"}.issubset(
            simulated.columns
        ):

            original = simulated["Original_Trips"].sum()
            proposed = simulated["Simulated_Trips"].sum()

            col1, col2 = st.columns(2)

            col1.metric(
                "Original Scheduled Trips",
                f"{original:,.0f}"
            )

            col2.metric(
                "Simulated Scheduled Trips",
                f"{proposed:,.0f}",
                delta=f"{proposed - original:,.0f}"
            )

            chart_data = pd.DataFrame({
                "Scenario": ["Current", "Simulated"],
                "Scheduled Trips": [original, proposed]
            })

            fig = px.bar(
                chart_data,
                x="Scenario",
                y="Scheduled Trips",
                color="Scenario",
                title="Current vs Simulated Scheduled Trips"
            )

            show_chart(fig)

        st.dataframe(simulated, use_container_width=True)

    else:
        st.warning("Simulated route data not found.")

    st.caption(
        "These are hypothetical scenarios. Merge/split changes "
        "and real-world service improvements have not been validated."
    )

# --------------------------------------------------
# 12. CURRENT VS SIMULATED METRICS
# --------------------------------------------------

elif page == "Metrics Comparison":

    st.title("Current vs Simulated Results")

    comparison = load_csv(
        inference_file("simulation_comparison.csv")
    )

    if comparison.empty:
        st.warning("Simulation comparison file not found.")
    else:

        st.subheader("Six-City Comparison")

        st.dataframe(
            comparison,
            use_container_width=True
        )

        selected = comparison[
            comparison["City"].astype(str).str.lower() == city
        ]

        if not selected.empty:

            row = selected.iloc[0]

            st.subheader(f"{city.title()} Metrics")

            col1, col2 = st.columns(2)

            col1.metric(
                "Original Routes",
                f"{int(row['Original_Routes']):,}"
            )

            col2.metric(
                "Simulated Routes",
                f"{int(row['Simulated_Routes']):,}"
            )

            col3, col4 = st.columns(2)

            col3.metric(
                "Original Scheduled Trips",
                f"{row['Original_Scheduled_Trips']:,.0f}"
            )

            col4.metric(
                "Simulated Scheduled Trips",
                f"{row['Simulated_Scheduled_Trips']:,.0f}",
                delta=(
                    f"{row['Simulated_Scheduled_Trips'] - row['Original_Scheduled_Trips']:,.0f}"
                )
            )

        st.subheader("Scheduled Trips Across Cities")

        chart_df = comparison.melt(
            id_vars="City",
            value_vars=[
                "Original_Scheduled_Trips",
                "Simulated_Scheduled_Trips"
            ],
            var_name="Scenario",
            value_name="Scheduled Trips"
        )

        fig = px.bar(
            chart_df,
            x="City",
            y="Scheduled Trips",
            color="Scenario",
            barmode="group",
            title="Current vs Simulated Scheduled Trips"
        )

        show_chart(fig)

        st.info(
            "A decrease in scheduled trips alone does not prove "
            "that service quality or route efficiency improved."
        )

# --------------------------------------------------
# 13. ABOUT
# --------------------------------------------------

elif page == "About":

    st.title("About RouteRanker")

    st.markdown("""
    ### Project Objective

    RouteRanker is an AI-powered public transit route
    analysis and optimization project.

    ### Technologies Used

    - Python
    - Pandas
    - Scikit-learn
    - K-Means Clustering
    - DBSCAN
    - Random Forest
    - XGBoost
    - Streamlit
    - Plotly

    ### Project Modules

    1. Data Collection
    2. Feature Engineering
    3. Exploratory Data Analysis
    4. Data Preprocessing
    5. Model Development and Evaluation
    6. Model Inference and Route Optimization
    7. Frontend and Interactive Dashboard

    ### Cities Covered

    Delhi, Hyderabad, Bengaluru, Chennai, Mumbai and Pune.

    ### Important Limitations

    - GTFS scheduled trips do not represent passenger counts.
    - Clusters do not automatically indicate efficiency.
    - Classification categories use proxy labels.
    - Schedule adjustments are hypothetical simulations.
    - Route merging and splitting require further geographical
      and operational validation.
    """)

    st.success("RouteRanker Dashboard | Module 7")
