from PyPDF2 import PdfReader

def extract(text, start_page, end_page):
  try:
    reader = PdfReader(text)
    text = ""
    if start_page is None and end_page is None:
      for page in reader.pages:
          text += page.extract_text()
    elif end_page is None:
      for page_num in range(int(start_page) - 1, len(reader.pages) - 1):
        text += reader.pages[page_num].extract_text()
    elif start_page is None:
      for page_num in range(0, int(end_page)):
        text += reader.pages[page_num].extract_text()
    else:
      for page_num in range(int(start_page) - 1, int(end_page)):
        text += reader.pages[page_num].extract_text()
    return text
  except FileNotFoundError:
    print(f"File ({text}) not found.")
    return None
  
def section_maker(content, starting_phrase=None, ending_phrase=None):
  section = None
  if starting_phrase is None and ending_phrase is None:
    section = content
  elif starting_phrase is None:
    end_index = content.find(ending_phrase)
    section = content[:end_index]
  elif ending_phrase is None:
    start_index = content.find(starting_phrase)
    section = content[start_index:]
  else:
    start_index = content.find(starting_phrase)
    end_index = content.find(ending_phrase)
    section = content[start_index:end_index]

  if section:
    section = " ".join(section.split())

  return section

def output(text, output_file=None):
  print(text)
  if output_file:
    with open(output_file, "w") as f:
      f.write(text)