import PyPDF2

# Replace 'your_pdf_file.pdf' with the actual path to your PDF file
pdf_file_path = '/home/arjun/Documents/GitHub/Research-Paper-Assistant/paper_downloads/1706.03762.pdf'

# Open the PDF file in read-binary mode
with open(pdf_file_path, 'rb') as pdf_file:
    # Create a PdfFileReader object
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Get the number of pages in the PDF
    num_pages = len(pdf_reader.pages)

    # Loop through each page and extract the text
    for page_num in range(num_pages):
        # Get a specific page from the PDF
        page = pdf_reader.pages[page_num]

        # Extract text from the page
        page_text = page.extract_text()

        # Print the text from the page
        # print(f"Page {page_num + 1}:\n")
        print(page_text)
        # print("\n--------------------------------------------\n")
