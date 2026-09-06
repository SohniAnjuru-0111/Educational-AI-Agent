import io
import fitz
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
class PDFReader:

    def extract_text(self, uploaded_file):

        try:

            pdf_bytes = uploaded_file.getvalue()

            if not pdf_bytes:
                return ""

            document = fitz.open(
                stream=pdf_bytes,
                filetype="pdf"
            )

            extracted_text = []

            for page in document:

                text = page.get_text("text")

                if text and text.strip():

                    extracted_text.append(text)

                else:

                    pix = page.get_pixmap(
                        matrix=fitz.Matrix(2, 2)
                    )

                    image_bytes = pix.tobytes(
                        "png"
                    )

                    image = Image.open(
                        io.BytesIO(image_bytes)
                    )

                    ocr_text = pytesseract.image_to_string(
                        image
                    )

                    if ocr_text and ocr_text.strip():

                        extracted_text.append(
                            ocr_text
                        )

            document.close()

            return "\n\n".join(
                extracted_text
            ).strip()

        except Exception as e:

            raise ValueError(
                f"Unable to process PDF: {e}"
            )