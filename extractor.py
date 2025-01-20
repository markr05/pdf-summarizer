from tika import parser
from summarizer import section_maker

file_path = "dog_pdf.pdf"

parsed_pdf = parser.from_file(file_path)

pdf_content = parsed_pdf.get("content", "")

result = "\n".join([line for line in pdf_content.split("\n") if line.strip() != ""])



print(f"Content: \n{result}")