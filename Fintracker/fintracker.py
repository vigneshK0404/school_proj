from PyPDF2 import PdfReader

reader = PdfReader("statement.pdf")
page = reader.pages[2]
print(page.extract_text())
