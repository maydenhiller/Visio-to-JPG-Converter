import streamlit as st
import os
import zipfile
import tempfile
import subprocess
from pdf2image import convert_from_path

st.set_page_config(page_title="Visio to JPG Converter", layout="centered")
st.title("📐 Visio to JPG Converter (LibreOffice)")
st.markdown("Upload `.vsdx` or `.vsdm` files. We'll convert them to high-quality `.jpg` images and zip them for download.")

uploaded_files = st.file_uploader("Upload Visio files", type=["vsdx", "vsdm"], accept_multiple_files=True)

if uploaded_files:
    with tempfile.TemporaryDirectory() as temp_dir:
        output_dir = os.path.join(temp_dir, "sketches")
        os.makedirs(output_dir, exist_ok=True)

        for file in uploaded_files:
            visio_path = os.path.join(temp_dir, file.name)
            with open(visio_path, "wb") as f:
                f.write(file.getbuffer())

            # Convert to PDF using LibreOffice
            subprocess.run([
                "soffice", "--headless", "--convert-to", "pdf", "--outdir", temp_dir, visio_path
            ], check=True)

            pdf_name = os.path.splitext(file.name)[0] + ".pdf"
            pdf_path = os.path.join(temp_dir, pdf_name)

            # Convert PDF to JPG
            images = convert_from_path(pdf_path, dpi=300)
            for i, img in enumerate(images):
                img_path = os.path.join(output_dir, f"{os.path.splitext(file.name)[0]}_page{i+1}.jpg")
                img.save(img_path, "JPEG")

        # Zip the output
        zip_path = os.path.join(temp_dir, "sketches.zip")
        with zipfile.ZipFile(zip_path, "w") as zipf:
            for root, _, files in os.walk(output_dir):
                for file in files:
                    zipf.write(os.path.join(root, file), arcname=file)

        with open(zip_path, "rb") as f:
            st.download_button("📦 Download sketches.zip", f, file_name="sketches.zip", mime="application/zip")
