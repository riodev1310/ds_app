import seaborn as sns
import streamlit as st
import google.generativeai as genai
import PIL.Image
from dotenv import load_dotenv
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


load_dotenv()

def plot_chart(chart_type, data, x_col, y_col):
    if chart_type == "Line Chart":
        chart = sns.lineplot(data=data, x=x_col, y=y_col, markers='o')
        chart_fig = chart.get_figure()
        chart_fig.savefig(f"./charts/{chart_type}_{x_col}_by_{y_col}.png")
        # st.pyplot()
    elif chart_type == "Bar Chart":
        chart = sns.barplot(data=data, x=x_col, y=y_col)
        chart_fig = chart.get_figure()
        chart_fig.savefig(f"./charts/{chart_type}_{x_col}_by_{y_col}.png")
        # st.pyplot()
    elif chart_type == "Scatter Plot":
        chart = sns.scatterplot(data=data, x=x_col, y=y_col)
        chart_fig = chart.get_figure()
        chart_fig.savefig(f"./charts/{chart_type}_{x_col}_by_{y_col}.png")
        # st.pyplot()
    elif chart_type == "Pie Chart":
        pie_data = data.groupby(x_col)[y_col].sum()
        chart = pie_data.plot.pie(autopct='%1.1f%%', startangle=90)
        chart_fig = chart.get_figure()
        chart_fig.savefig(f"./charts/{chart_type}_{x_col}_by_{y_col}.png")
        # st.pyplot()
    
    return chart

def generate_report_from_chart(folder):
    genai.configure(api_key=os.getenv("API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")
    reports = []
    for index, filename in enumerate(os.listdir(folder)):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            file_path = os.path.join(folder, filename)
            organ = PIL.Image.open(file_path)
                
            response = model.generate_content(["According to the chart, what insight could be taken from it", organ])
            report = {}
            report["chart"] = file_path
            report["text"] = response.text
            reports.append(report)
    return reports


def refresh_session(folder_path):
    # if "refresh_triggered" not in st.session_state:
    #     st.session_state.refresh_triggered = False
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    else:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            
            if os.path.isfile(file_path):
                os.remove(file_path)
                
                
def display_report(reports):
    for obj in reports:
        image = PIL.Image.open(obj["chart"])
        st.image(image, use_column_width=True)
        st.write(obj["text"])
    
    
def generate_report_pdf(reports, report_name):
    c = canvas.Canvas(f"{report_name}.pdf", pagesize=letter)
    width, height = letter
    
    y_position = height - 100
    
    for obj in reports:
        c.drawImage(obj["chart"], 50, y_position, width=400, height=200)
        y_position -= 220
        
        c.setFont("Helvetica", 12)
        c.drawString(100, y_position, obj["text"])
        y_position -= 20
        
        if y_position < 200:
            c.showPage()
            y_position = height - 100
    
    c.save()


def remove_chart(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)
    # st.session_state.refresh_triggered = True