import PyPDF2
import docx

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfFileReader(file)
    text = ''
    for page_num in range(reader.numPages):
        page = reader.getPage(page_num)
        text += page.extract_text()
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = ''
    for para in doc.paragraphs:
        text += para.text
    return text

def extract_text(file):
    print("hghhv")
    if file.name.endswith('.pdf'):
        return extract_text_from_pdf(file)
    elif file.name.endswith('.docx'):
        return extract_text_from_docx(file)
    else:
        raise ValueError('Unsupported file format')
