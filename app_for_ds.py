import streamlit as st 
import pandas as pd
from helper_func import plot_chart, generate_report_from_chart
import io

# Title of the app
st.title("Data Visualization and Forecasting App with Streamlit")

# File Uploader
uploaded_file = st.file_uploader("Upload your data", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    
    st.subheader("Uploaded Data")
    st.dataframe(data)
    
    st.subheader("Aggregation Options")
    categorical_columns = data.select_dtypes(include=['object']).columns.tolist()
    numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns.tolist()
    
    if len(categorical_columns) > 0 and len(numeric_columns) > 0:
        # User selects the categorical column
        category_col = st.selectbox("Choose a categorical column for grouping:", categorical_columns)
        
        numeric_col = st.selectbox("Choose a numeric column for aggregation:", numeric_columns)
        
        aggregation_function = st.selectbox(
            "Aggregation function: ",
            ["Sum", "Mean", "Count", "Min", "Max"]
        )
        
        if aggregation_function == "Sum":
            aggregated_data = data.groupby(category_col)[numeric_col].sum().reset_index()
        elif aggregation_function == "Mean":
            aggregated_data = data.groupby(category_col)[numeric_col].mean().reset_index()
        elif aggregation_function == "Count":
            aggregated_data = data.groupby(category_col)[numeric_col].count().reset_index()
        elif aggregation_function == "Min":
            aggregated_data = data.groupby(category_col)[numeric_col].min().reset_index()
        elif aggregation_function == "Max":
            aggregated_data = data.groupby(category_col)[numeric_col].max().reset_index()
            
        st.subheader(f"Aggregated Data: {aggregation_function} of {numeric_col} by {category_col}")
        st.dataframe(aggregated_data)
        
        st.subheader("Visualize your data")
        
        chart_type = st.selectbox(
            "Choose chart type",
            ["Line Chart", "Bar Chart", "Scatter Plot", "Pie Chart"]
        )
        
        chart = plot_chart(chart_type, aggregated_data, category_col, numeric_col)
        
        if st.button("Generated Report"):
            report = generate_report_from_chart("chart.png")
            st.subheader("Generated report")
            st.write(report)