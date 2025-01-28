import streamlit as st
import pandas as pd
import openai

# Set OpenAI API Key (Replace with your key)
# openai.api_key = "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"
from openai import OpenAI

client = OpenAI(
  api_key="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"
)

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
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=prompt,
                    max_tokens=100,
                )
                st.write("### AI Summary")
                st.success(response.choices[0].text.strip())
            except Exception as e:
                st.error("Error generating summary: " + str(e))
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")

else:
    st.write("<h3 style='text-align: center;'>Please upload an Excel file to get started.</h3>", unsafe_allow_html=True)