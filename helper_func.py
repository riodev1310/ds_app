import seaborn as sns
import streamlit as st
import google.generativeai as genai
import PIL.Image
from dotenv import load_dotenv
import os


load_dotenv()

def plot_chart(chart_type, data, x_col, y_col):
    if chart_type == "Line Chart":
        chart = sns.lineplot(data=data, x=x_col, y=y_col, markers='o')
        chart_fig = chart.get_figure()
        chart_fig.savefig("chart.png")
        st.pyplot()
    elif chart_type == "Bar Chart":
        chart = sns.barplot(data=data, x=x_col, y=y_col)
        chart_fig = chart.get_figure()
        chart_fig.savefig("chart.png")
        st.pyplot()
    elif chart_type == "Scatter Plot":
        chart = sns.scatterplot(data=data, x=x_col, y=y_col)
        chart_fig = chart.get_figure()
        chart_fig.savefig("chart.png")
        st.pyplot()
    elif chart_type == "Pie Chart":
        pie_data = data.groupby(x_col)[y_col].sum()
        chart = pie_data.plot.pie(autopct='%1.1f%%', startangle=90)
        chart_fig = chart.get_figure()
        chart_fig.savefig("chart.png")
        st.pyplot()
    
    return chart

def generate_report_from_chart(chart_buffer):
    genai.configure(api_key=os.getenv("API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")
    organ = PIL.Image.open("chart.png")
    
    response = model.generate_content(["According to the chart, what insight could be taken from it", organ])
    return response.text