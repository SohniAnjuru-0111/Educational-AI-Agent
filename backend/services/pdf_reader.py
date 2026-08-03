import PyPDF2


class PDFReader:

    def extract_text(self, uploaded_file):

        pdf = PyPDF2.PdfReader(uploaded_file)

        text = ""

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text