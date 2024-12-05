import streamlit as st 
import pandas as pd
from helper_func import plot_chart, generate_report_from_chart, display_report, generate_report_pdf, refresh_session, remove_chart
import os
from PIL import Image
from streamlit_js_eval import streamlit_js_eval
from datetime import datetime, timezone

# Title of the app
st.title("Data Visualization and Forecasting App with Streamlit")

# File Uploader
uploaded_file = st.file_uploader("Upload your data", type=["csv"])

charts_folder = "charts"

element_num = 0

if st.button("Refresh Session"):
    refresh_session(charts_folder)
    streamlit_js_eval(js_expressions="parent.window.location.reload()")

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
        
        if st.button("Plot Graph"):
            chart = plot_chart(chart_type, aggregated_data, category_col, numeric_col)
        
        for filename in os.listdir(charts_folder):
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                file_path = os.path.join(charts_folder, filename)
                
                image = Image.open(file_path)
                st.image(image, caption=filename, use_column_width=True)
                element_num += 1
                if st.button("Remove chart", key=element_num):
                    remove_chart(file_path)
                    # streamlit_js_eval(js_expressions="parent.window.location.refresh()")
        
        if st.button("Generate Report"):
            reports = generate_report_from_chart(charts_folder)
            st.subheader("Generated report")
            display_report(reports)
            # generate_report_pdf(reports, f"report_{datetime.now(timezone.utc)}")