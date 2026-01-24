import os, sys
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import yfinance as yf
import pandas as pd
import json
import pdfplumber
from PIL import Image
import pytesseract
from docx import Document

def dump_csv(df, file_name: str):
    return df.to_csv(file_name)

def load_csv(file_name: str, sep: str = ',', delimiter = None, header: str = 'infer'):
    if not os.path.exists(file_name):
        raise RuntimeError(f"{file_name} not exists")
    
    df = pd.read_csv(file_name, sep=sep, delimiter=delimiter, header=header)
    return df

def extract_github_repository(user: str, repo: str):
    url = f"https://api.github.com/repos/{user}/{repo}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    res = requests.get(url, headers=headers)
    return json.loads(res.text)

def extract_img(file_name: str) -> str:
    if not os.path.exists(file_name):
        raise RuntimeError(f"{file_name} not exists")
    
    return pytesseract.image_to_string(file_name)

def extract_pdf(file_name: str) -> str:
    text = ""
    with pdfplumber.open(file_name) as pdf:
        for i, page in enumerate(pdf.pages):
            text += page.extract_text()

    return text

def extract_docx(file_name: str) -> str:
    docx = Document(file_name)
    text = ""
    for paragraph in docx.paragraphs:
        text += paragraph.text
        text += '\n'

    return text

if __name__ == "__main__":
    # Extract CSV file
    print("Extract CSV file..")
    df = yf.Ticker("DX-Y.NYB").history(period="30d")
    df = df[["Open", "High", "Low", "Close"]]
    print(df.shape)
    print(df.tail(5))
    
    csv_file = "../data/retrieve/csv_format.csv"
    df = dump_csv(df, csv_file)
    
    # ASCII Texts like Forum Postings and HTML
    print("Extract ASCII Texts like Forum Postings and HTML..")
    user = "csian98"
    repo = "sian"
    json_py = extract_github_repository(user, repo)
    
    data = json.dumps(json_py, indent=4)
    print(data)
    
    html_file = "../data/retrieve/html_format.csv"
    with open(html_file, 'w') as fp:
        fp.write(data)
    
    # PDF and Word Documents
    print("Extract PDF and Word Documents..")
    pdf_file = "../data/retrieve/resume.pdf"
    img_file = "../data/retrieve/resume.png"
    docx_file = "../data/retrieve/resume.docx"
    output_file = "../data/retrieve/output.txt"

    pdf_text = extract_pdf(pdf_file)
    img_text = extract_img(img_file)
    docx_text = extract_docx(docx_file)

    print("===== Text From PDF ======")
    print(pdf_text)

    print("\n\n\n===== Text From IMG =====")
    print(img_text)

    print("\n\n\n===== Text From DOCX =====")
    print(docx_text)

    with open(output_file, 'w') as fp:
        fp.write(pdf_text)
        fp.write(img_text)
        fp.write(docx_text)
