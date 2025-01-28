import streamlit as st
import pandas as pd
import openai
from dotenv import load_dotenv
import os

# Load the API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Streamlit Web App
st.set_page_config(page_title="Excel Data Visualization", layout="wide")

# Header
st.markdown("<h1 style='text-align: center;'>Excel Data Visualization App</h1>", unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"])

if uploaded_file:
    try:
        # Load the uploaded file into a DataFrame
        df = pd.read_excel(uploaded_file)
        st.write("### Uploaded Dataset")
        st.dataframe(df)

        # Column selection for visualization
        st.write("### Select Columns for Visualization")
        columns = df.columns.tolist()
        x_axis = st.selectbox("Choose X-axis column", columns)
        y_axis = st.selectbox("Choose Y-axis column", columns)

        # Visualization
        if x_axis and y_axis:
            st.write("### Visualization")
            st.line_chart(df[[x_axis, y_axis]])

        # Generating a summary using OpenAI (optional)
        if st.button("Generate AI Summary"):
            prompt = f"Provide a summary of this dataset:\n\n{df.head(5).to_string()}"
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",  # Updated model
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt}
                    ]
                )
                st.write("### AI Summary")
                st.success(response['choices'][0]['message']['content'].strip())
            except Exception as e:
                st.error("Error generating summary: " + str(e))
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")

else:
    st.write("<h3 style='text-align: center;'>Please upload an Excel file to get started.</h3>", unsafe_allow_html=True)
