import streamlit as st
from img2table.ocr import PaddleOCR, AzureOCR
from img2table.document import Image
import cv2
from PIL import Image as PILImage
import pandas as pd

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
        subscription_key = "gMYpHRCnHqA8r2MxdtL203rBZ3WLTg4qFlH9wkxU40441ZLI302qJQQJ99AKACGhslBXJ3w3AAAFACOG50Ds"
        endpoint = "https://image-extration.cognitiveservices.azure.com/"
        ocr = AzureOCR(subscription_key=subscription_key, endpoint=endpoint)

    # Convert image to suitable format for table extraction
    cv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)  # Convert to BGR for OpenCV

    # Extract tables from the image
    extracted_tables = img.extract_tables(ocr=ocr, implicit_rows=True, borderless_tables=False, min_confidence=50)

    if extracted_tables:
        # Display extracted tables and highlight the cells on the image
        for table in extracted_tables:
            for row in table.content.values():
                for cell in row:
                    # Draw bounding boxes around table cells
                    cv2.rectangle(cv_img, (cell.bbox.x1, cell.bbox.y1), (cell.bbox.x2, cell.bbox.y2), (255, 0, 0), 2)

        # Convert image with highlighted cells back to PIL format and display
        img_with_boxes = PILImage.fromarray(cv_img)
        st.image(img_with_boxes, caption="Highlighted Image", use_column_width=True)

        # Convert the extracted table to a DataFrame and display it
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
