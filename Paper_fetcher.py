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

def get_text(pdf_file_path):
   with open(pdf_file_path, 'rb') as pdf_file:
    # Create a PdfFileReader object
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Get the number of pages in the PDF
    num_pages = len(pdf_reader.pages)

    # Loop through each page and extract the text
    full_text = ''
    for page_num in range(num_pages):
        # Get a specific page from the PDF
        page = pdf_reader.pages[page_num]

        # Extract text from the page
        page_text = page.extract_text()

        full_text += page_text

    return(''.join(full_text.split('References')[:-1]))

pdf_file_path = '/home/arjun/Documents/GitHub/Research-Paper-Assistant/paper_downloads/1706.03762.pdf'

print(get_text(pdf_file_path))