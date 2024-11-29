import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

# Helper function to convert dates to numeric
def convert_dates_to_numeric(data, date_column):
    """Converts a date column to numeric values (days since the start date)."""
    # Convert to datetime with dayfirst=True to handle DD/MM/YYYY format
    data[date_column] = pd.to_datetime(data[date_column], errors='coerce', dayfirst=True)
    start_date = data[date_column].min()  # Reference start date
    data['NumericDate'] = (data[date_column] - start_date).dt.days
    return data, 'NumericDate', start_date

# Title of the app
st.title("Data Visualization and Forecasting App with Streamlit")

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the uploaded CSV
    data = pd.read_csv(uploaded_file)

    # Display the data as a table
    st.subheader("Uploaded Data")
    st.dataframe(data)

    # Allow the user to select a column for aggregation and visualization
    st.subheader("Aggregation Options")
    categorical_columns = data.select_dtypes(include=['object']).columns.tolist()
    numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns.tolist()

    if len(categorical_columns) > 0 and len(numeric_columns) > 0:
        # User selects the categorical column
        category_col = st.selectbox("Choose a categorical column for grouping:", categorical_columns)

        # Check if the selected column is a date and convert it if necessary
        if pd.to_datetime(data[category_col], errors='coerce', dayfirst=True).notnull().all():
            st.info(f"The column '{category_col}' is detected as a date. Converting to numeric.")
            data, category_col, start_date = convert_dates_to_numeric(data, category_col)

        # User selects the numeric column
        numeric_col = st.selectbox("Choose a numeric column for aggregation:", numeric_columns)

        # User selects the aggregation function
        aggregation_function = st.selectbox(
            "Choose an aggregation function:",
            ["Sum", "Mean", "Count", "Min", "Max"]
        )

        # Perform the aggregation based on user selection
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

        # Show aggregated data
        st.subheader(f"Aggregated Data ({aggregation_function})")
        st.dataframe(aggregated_data)

        # Dropdown to select chart type
        chart_type = st.selectbox(
            "Choose Chart Type:",
            ["Line Chart", "Bar Chart", "Scatter Plot", "Pie Chart", "Forecasting"]
        )

        # Input for custom chart title
        chart_title = st.text_input("Enter Chart Title:", f"{chart_type} of {numeric_col} by {category_col}")

        # Handle chart types
        if chart_type in ["Line Chart", "Bar Chart", "Scatter Plot", "Pie Chart"]:
            fig, ax = plt.subplots(figsize=(10, 5))

            if chart_type == "Line Chart":
                ax.plot(aggregated_data[category_col], aggregated_data[numeric_col], marker="o", color="blue")
            elif chart_type == "Bar Chart":
                ax.bar(aggregated_data[category_col], aggregated_data[numeric_col], color="skyblue")
            elif chart_type == "Scatter Plot":
                ax.scatter(aggregated_data[category_col], aggregated_data[numeric_col], color="green")
            elif chart_type == "Pie Chart":
                ax.pie(
                    aggregated_data[numeric_col],
                    labels=aggregated_data[category_col],
                    autopct='%1.1f%%',
                    startangle=90
                )
                ax.axis("equal")

            ax.set_title(chart_title)
            ax.set_xlabel(category_col)
            ax.set_ylabel(numeric_col)
            st.pyplot(fig)

        elif chart_type == "Forecasting":
            # Prepare data for regression using numeric date values
            X = data[['NumericDate']].values
            y = data[numeric_col].values

            # Train a Linear Regression model
            model = LinearRegression()
            model.fit(X, y)

            # Input for forecasting
            future_date = st.date_input(
                f"Select a future date for {category_col}:",
                min_value=start_date
            )

            # Convert the selected date to numeric for prediction
            if future_date:
                future_date_ts = pd.Timestamp(future_date)
                future_numeric = (future_date_ts - start_date).days
                
                # Predict the future value
                future_prediction = model.predict([[future_numeric]])[0]
                st.write(f"Predicted {numeric_col} of {future_date}: **{future_prediction:.2f}**")
                
                # Visualization
                st.subheader("Forecasting Visualization")
                fig, ax = plt.subplots(figsize=(10, 6))

                # Scatter plot of the actual data
                ax.scatter(X, y, color="blue", label="Actual Data")
                
                # Regression line
                ax.plot(X, model.predict(X), color="red", label="Regression Line")

                # Mark the predicted point
                ax.scatter(future_numeric, future_prediction, color="green", s=100, label=f"Forecasted Point: {future_prediction:.2f}")

                ax.set_title(f"Forecasting {numeric_col} based on {category_col}")
                ax.set_xlabel(category_col)
                ax.set_ylabel(numeric_col)
                ax.legend()
                st.pyplot(fig)

    else:
        st.warning("Ensure you have both categorical and numeric columns for aggregation.")
else:
    st.info("Please upload a CSV file to start.")
