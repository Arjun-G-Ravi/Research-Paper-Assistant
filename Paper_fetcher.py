import requests
from bs4 import BeautifulSoup
import re
import glob
import os
import PyPDF2
import re


def fetch_paper(arxiv_url):
    try:
        response = requests.get(arxiv_url)
        pdf_name = arxiv_url.split('/')[-1]+'.pdf'

        pdf_files_in_folder = glob.glob(os.path.join('paper_downloads', '*.pdf'))
        if 'paper_downloads/'+pdf_name in pdf_files_in_folder:
            print('Paper present in paper_downloads')
            return 'paper_downloads/'+pdf_name
        else:
            if response.status_code == 200:
                print("Fetching pdf link...")
                soup = BeautifulSoup(response.text, 'html.parser')
                pdf_link = None
                for link in soup.find_all('a', href=True): # extracting pdf link
                    if re.search(r'pdf$', link['href']):
                        pdf_link = link['href']
                        break

                if pdf_link:
                    print("Downloading paper...")
                    full_pdf_url = 'https://arxiv.org' + pdf_link
                    pdf_response = requests.get(full_pdf_url)

                    if pdf_response.status_code == 200:
                        with open('paper_downloads/' + pdf_name, 'wb') as pdf_file:
                            pdf_file.write(pdf_response.content)
                        print(f"Successfully downloaded '{pdf_name}'.")
                        return 'paper_downloads/' + pdf_name
                    else:
                        print(f"Failed to download PDF. Status code: {pdf_response.status_code}")
                        return # later raise error
                else:
                    print("PDF link not found on the arXiv page.")
                    return
            
            else:
                print(f"The given link is not an arxiv link. Status code: {response.status_code}")
                return
    except:
        print("The given link is invalid")

def get_text(pdf_file_path ):
    abstract_text = ""
    introduction_text = ""
    conclusion_text = ""
    references_text = ""

    with open(pdf_file_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)
        current_section = None

        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()

            if re.search(r'\bAbstract\b', page_text, re.IGNORECASE):
                current_section = "abstract"
            elif re.search(r'\bIntroduction\b', page_text, re.IGNORECASE):
                current_section = "introduction"
            elif re.search(r'\bConclusion\b', page_text, re.IGNORECASE):
                current_section = "conclusion"
            elif re.search(r'\bReferences\b', page_text, re.IGNORECASE):
                current_section = "references"

            if current_section == "abstract":
                abstract_text += page_text
            elif current_section == "introduction":
                introduction_text += page_text
            elif current_section == "conclusion":
                conclusion_text += page_text
            elif current_section == "references":
                references_text += page_text

    # print("Abstract:-----------------------------------------------------\n", abstract_text)
    # print("\nIntroduction:-----------------------------------------------------\n", introduction_text)
    # print("\nConclusion:-------------------------------------------------------\n", conclusion_text)
    # print("\nReferences:---------------------------------------------\n", references_text)
    return abstract_text,introduction_text,conclusion_text
