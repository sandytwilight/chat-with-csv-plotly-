





 
import pandas as pd
import os
import streamlit as st
import plotly.graph_objs as go
from pandasai.llm import OpenAI
from pandasai import SmartDataframe, SmartDatalake
import plotly.express as px
 
# Function to load data from uploaded files (individual or folder path)
def load_data(upload_method, files=None, folder_path=None):
    dataframes = []
    if upload_method == "Folder Path":
        if folder_path:
            for f in os.listdir(folder_path):
                file_path = os.path.join(folder_path, f)
                if os.path.isfile(file_path):
                    if file_path.endswith(".csv"):
                        df = pd.read_csv(file_path)
                        print(f"Loaded CSV file: {f}")
                        dataframes.append(df)
                    elif file_path.endswith((".xlsx", ".xls")):
                        xls = pd.ExcelFile(file_path)
                        for sheet_name in xls.sheet_names:
                            df = pd.read_excel(xls, sheet_name=sheet_name)
                            dataframes.append(df)
                            print(f"Loaded Excel sheet '{sheet_name}' from file: {f}")
    else:
        if files:
            for file in files:
                if file is not None:
                    if file.type in ('application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'):
                        xls = pd.ExcelFile(file)
                        for sheet_name in xls.sheet_names:
                            df = pd.read_excel(xls, sheet_name=sheet_name)
                            dataframes.append(df)
                            print(f"Loaded Excel sheet '{sheet_name}' from file: {file.name}")
                    elif file.type == 'text/csv':
                        df = pd.read_csv(file)
                        dataframes.append(df)
                        print(f"Loaded CSV file: {file.name}")
    return pd.concat(dataframes, ignore_index=True) if dataframes else None
 
 
# Function to generate interactive plot
def generate_plot(data, x_column, y_column):
    if x_column == y_column:
        return "Please select different columns for the x-axis and y-axis."
    else:
        fig = px.bar(data, x=x_column, y=y_column)
        fig.update_layout(title=f"{y_column} vs {x_column}", xaxis_title=x_column, yaxis_title=y_column)
        return fig
 
# Main function to display UI and perform actions
def main():
    st.set_page_config(page_title="Employee Data Analysis", page_icon=":bar_chart:", layout="wide")
   
    # Create Streamlit app
    styled_text = """
        <h1 style="font-family: 'Peace Sans', sans-serif;">
            <span style="color: #006DB5;">CHAT</span>
            <span style="color: #006DB5;"> </span>
            <span style="color: #006DB5;">WITH</span>
            <span style="color: #006DB5;"> </span>
            <span style="color: #006DB5;">CSV</span>
            <span style="color: #006DB5;"> </span>
            <span style="color: #006DB5;">AND</span>
            <span style="color: #0XFF0D47A1;"> </span>
            <span style="background: linear-gradient(to right, #006DB5, #00FF00); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">EXCEL</span>
            <span style="color: #00FF00;"> </span>
            <span style="color: #00FF00;"></span>
            <span style="color: #00FF00;"> </span>
            <span style="color: #00FF00;"> </span>
            <span style="color: #00FF00;"> </span>
            <span style="color: #00FF00;"></span>
        </h1>
        """
       
    # Create a container for the sidebar
    sidebar = st.sidebar
    # Display the styled text
    st.write(styled_text, unsafe_allow_html=True)
 
    # Company logo and description in the sidebar
    with sidebar:
        # Assuming you have a company logo image file named 'company_logo.png'
        st.image('image.png', width=200)
        # Replace with your company details
        text_3 = '<font color="teal" font-family: caveat>"Pozent - Pioneering AI Solutions . Deep Dive In AI Excellence"</font>'
        st.sidebar.write(text_3, unsafe_allow_html=True)
       
        # Assuming you have a company logo image file named 'company_logo.png'
        st.image('my.png', width=200)
        # Replace with your company details
        text_3 = '<font color="teal" font-family: caveat>"CHAT WITH CSV AND EXCEL - Chat with CSV and Excel. This project uses natural language processing (NLP) to interact with data in a conversational way, likely through CSV and Excel files"</font>'
        st.sidebar.write(text_3, unsafe_allow_html=True)
 
    st.header("Upload Data")
 
    # Upload options: folder path or individual files
    upload_option = st.radio("Upload Option", ("Folder Path", "Individual Files"))
 
    if upload_option == "Folder Path":
        folder_path = st.text_input("Enter Folder Path:")
        # Disable file upload option when folder path is selected
        uploaded_files = st.file_uploader("Upload Data Files (CSV or Excel)", type=['csv', 'xlsx', 'xls'], accept_multiple_files=True, disabled=True)
    else:
        folder_path = None
        uploaded_files = st.file_uploader("Upload Data Files (CSV or Excel)", type=['csv', 'xlsx', 'xls'], accept_multiple_files=True)
 
    # Loading data based on upload method
    dataframe = load_data(upload_option, uploaded_files, folder_path)
 
    if dataframe is not None:
        # Creating SmartDataframe
        llm = OpenAI(api_token='')
        smart_df = SmartDataframe(dataframe, config={"llm": llm})
 
        # Asking a question
        question = st.text_input("Ask a question:")
        if st.button("Ask"):
            answer = smart_df.chat(question)
            if isinstance(answer, str) and answer.startswith(("http", "https", "C:/Users", "D:/Users")):
                st.image(answer, use_column_width=True)
                # Display image without pop-up
                # st.image(answer, use_column_width=True)
            else:
                st.markdown("## Answer:")
                st.write(answer)  # Displaying answer as it is
 
    if dataframe is not None:
        # Choose columns for x-axis and y-axis
        st.header("Select X-Axis and Y-Axis Columns")
        x_column = st.selectbox("X-Axis Column:", options=dataframe.columns)
        y_column = st.selectbox("Y-Axis Column:", options=dataframe.columns)
 
        # Generate interactive plot
        st.header("Interactive Plot")
        plot_result = generate_plot(dataframe, x_column, y_column)
        if isinstance(plot_result, str):
            st.warning(plot_result)
        else:
            st.plotly_chart(plot_result)
 
    else:
        if upload_option == "Folder Path" and folder_path:
            st.warning(f"No valid CSV or Excel files found in folder: {folder_path}")
        else:
            st.warning("No valid files uploaded. Please upload CSV or Excel files or provide a valid folder path.")
 
if __name__ == "__main__":
    main()
 