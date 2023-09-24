import PyPDF2
import re

# Replace 'your_pdf_file.pdf' with the actual path to your PDF file
pdf_file_path = '/home/arjun/Documents/GitHub/Research-Paper-Assistant/paper_downloads/1706.03762.pdf'

# Initialize variables to store the sections
abstract_text = ""
introduction_text = ""
conclusion_text = ""
references_text = ""

# Open the PDF file in read-binary mode
with open(pdf_file_path, 'rb') as pdf_file:
    # Create a PdfFileReader object
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Get the number of pages in the PDF
    num_pages = len(pdf_reader.pages)

    # Initialize a variable to track the current section
    current_section = None

    # Loop through each page and extract the text
    for page_num in range(num_pages):
        # Get a specific page from the PDF
        page = pdf_reader.pages[page_num]

        # Extract text from the page
        page_text = page.extract_text()

        # Search for patterns to identify sections
        if re.search(r'\bAbstract\b', page_text, re.IGNORECASE):
            current_section = "abstract"
        elif re.search(r'\bIntroduction\b', page_text, re.IGNORECASE):
            current_section = "introduction"
        elif re.search(r'\bReferences\b', page_text, re.IGNORECASE):
            current_section = "references"

        # Append text to the appropriate section
        if current_section == "abstract":
            abstract_text += page_text
        elif current_section == "introduction":
            introduction_text += page_text
        elif current_section == "conclusion":
            conclusion_text += page_text
        elif current_section == "references":
            references_text += page_text

# Print the extracted sections
print("Abstract:-----------------------------------------------------\n", abstract_text)
print("\nIntroduction:-----------------------------------------------------\n", introduction_text)
print("\nConclusion:-------------------------------------------------------\n", conclusion_text)
print("\nReferences:---------------------------------------------\n", references_text)
