import streamlit as st
from paddleocr import PaddleOCR
from img2table.ocr import AzureOCR
from img2table.document import Image
import cv2
from PIL import Image as PILImage

subscription_key = "gMYpHRCnHqA8r2MxdtL203rBZ3WLTg4qFlH9wkxU40441ZLI302qJQQJ99AKACGhslBXJ3w3AAAFACOG50Ds"
endpoint = "https://image-extration.cognitiveservices.azure.com/"

# Streamlit UI
st.title("OCR-based Table Extraction")

# Choose OCR Model
ocr_option = st.selectbox("Select OCR Model", ("Azure OCR", "PaddleOCR"))

# Upload Image
uploaded_file = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])
if uploaded_file is not None:
    # Save uploaded file temporarily
    with open("temp_image.png", "wb") as f:
        f.write(uploaded_file.read())

    # Display the uploaded image
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    # Initialize OCR model
    if ocr_option == "Azure OCR":
        azure_ocr = AzureOCR(subscription_key=subscription_key, endpoint=endpoint)
        ocr_model = azure_ocr
    else:
        paddle_ocr = PaddleOCR(use_angle_cls=True, lang="en")
        ocr_model = paddle_ocr

    # Load image for processing
    img = Image(src="temp_image.png")
    cv_img = cv2.imread("temp_image.png")

    # Extract tables
    with st.spinner("Extracting tables..."):
        extracted_tables = img.extract_tables(
            ocr=ocr_model,
            implicit_rows=True,
            borderless_tables=False,
            min_confidence=50,
        )

    # Display extracted tables
    if extracted_tables:
        st.success("Tables extracted successfully!")
        for table in extracted_tables:
            st.write(table.html_repr(title="Extracted Table"), unsafe_allow_html=True)

        # Save to Excel option
        if st.button("Download as Excel"):
            img.to_xlsx(
                "extracted_tables.xlsx",
                ocr=ocr_model,
                implicit_rows=True,
                borderless_tables=False,
                min_confidence=50,
            )
            st.download_button(
                label="Download Excel",
                data=open("extracted_tables.xlsx", "rb"),
                file_name="extracted_tables.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
    else:
        st.error("No tables found in the image.")
