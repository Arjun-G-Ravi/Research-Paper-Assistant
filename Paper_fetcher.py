import requests
from bs4 import BeautifulSoup
import re
import glob
import os

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
                        return
                else:
                    print("PDF link not found on the arXiv page.")
                    return
            
            else:
                print(f"The given link is not an arxiv link. Status code: {response.status_code}")
                return
    except:
        print("The given link is invalid")