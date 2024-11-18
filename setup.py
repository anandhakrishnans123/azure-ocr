from setuptools import setup, find_packages

setup(
    name="streamlit-ocr-extractor",
    version="1.0.0",
    description="A Streamlit app for table extraction using OCR (Azure OCR and PaddleOCR)",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "streamlit",
        "paddleocr",
        "img2table[paddle]",
        "img2table[azure]",
        "opencv-python-headless",
        "pillow",
    ],
    entry_points={
        "console_scripts": [
            "streamlit-ocr-extractor=app:main",  # Replace 'app' if your app.py file has a different name
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
