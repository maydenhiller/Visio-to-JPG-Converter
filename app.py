import streamlit as st
import os
import zipfile
import tempfile
import convertapi

convertapi.api_secret = 'your_api_secret_here'  # Get from https://www.convertapi.com/a/demo

st.set_page_config(page_title="Visio to JPG Converter", layout="centered")
st.title("📐 Visio to JPG Converter")
st.markdown("Upload `.vsdx` or `.vsdm` files and download a ZIP of high-quality `.jpg` sketches.")

uploaded_files = st.file_uploader("Upload Visio files", type=["vsdx", "vsdm"], accept_multiple_files=True)

if uploaded_files:
    with tempfile.TemporaryDirectory() as temp_dir:
        output_dir = os.path.join(temp_dir, "sketches")
        os.makedirs(output_dir, exist_ok=True)

        for file in uploaded_files:
            file_path = os.path.join(temp_dir, file.name)
            with open(file_path, "wb") as f:
                f.write(file.getbuffer())

            result = convertapi.convert('jpg', {'File': file_path})
            for i, file_info in enumerate(result.files):
                file_info.save_file(os.path.join(output_dir, f"{os.path.splitext(file.name)[0]}_page{i+1}.jpg"))

        zip_path = os.path.join(temp_dir, "sketches.zip")
        with zipfile.ZipFile(zip_path, "w") as zipf:
            for root, _, files in os.walk(output_dir):
                for file in files:
                    zipf.write(os.path.join(root, file), arcname=file)

        with open(zip_path, "rb") as f:
            st.download_button("📦 Download sketches.zip", f, file_name="sketches.zip", mime="application/zip")
