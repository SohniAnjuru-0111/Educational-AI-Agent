from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import os
import html


class PDFExporter:

    def export(self, title, content, filename):

        os.makedirs("outputs", exist_ok=True)

        filepath = os.path.join("outputs", filename)

        doc = SimpleDocTemplate(filepath)

        styles = getSampleStyleSheet()

        story = []

        story.append(
            Paragraph(f"<b>{html.escape(title)}</b>", styles["Heading1"])
        )

        # Split content into lines
        lines = content.split("\n")

        for line in lines:

            line = line.strip()

            if line == "":
                continue

            # Escape HTML tags
            safe_line = html.escape(line)

            story.append(
                Paragraph(safe_line, styles["BodyText"])
            )

        doc.build(story)

        return filepath