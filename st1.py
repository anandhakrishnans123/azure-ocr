import streamlit as st
from img2table.ocr import PaddleOCR, AzureOCR
from img2table.document import Image
import pandas as pd
from PIL import Image as PILImage
import numpy as np

# Set up page title and description
st.title("Table Extraction from Image")
st.write("Upload an image with a table, and choose the OCR method to extract and display the data.")

# Input for choosing OCR method (PaddleOCR or Azure OCR)
ocr_method = st.selectbox("Select OCR Method", ["PaddleOCR", "AzureOCR"])

# Upload an image file
uploaded_file = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Load the uploaded image
    img = PILImage.open(uploaded_file)
    st.image(img, caption="Uploaded Image", use_column_width=True)

    # Initialize OCR based on user's choice
    if ocr_method == "PaddleOCR":
        ocr = PaddleOCR(lang="en", kw={"use_dilation": True})
    else:
        # Azure OCR credentials (replace with your own credentials)
        subscription_key = "your_azure_subscription_key"
        endpoint = "your_azure_endpoint"
        ocr = AzureOCR(subscription_key=subscription_key, endpoint=endpoint)

    # Convert image to numpy array (for img2table)
    img_array = np.array(img)

    # Extract tables from the image
    extracted_tables = img.extract_tables(ocr=ocr, implicit_rows=True, borderless_tables=False, min_confidence=50)

    if extracted_tables:
        # Convert extracted table data into a DataFrame
        extracted_table = extracted_tables[0]  # Assuming extracting one table
        table_data = []

        for row in extracted_table.content.values():
            row_data = [cell.content for cell in row]
            table_data.append(row_data)

        # Create DataFrame from table data
        df = pd.DataFrame(table_data)

        st.write("Extracted Table:")
        st.write(df)

        # Provide an option to download the table as a CSV file
        csv_file = df.to_csv(index=False)
        st.download_button("Download CSV", csv_file, file_name="extracted_table.csv", mime="text/csv")
    else:
        st.warning("No tables detected in the image.")
