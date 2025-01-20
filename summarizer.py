from tika import parser
from transformers import pipeline
from concurrent.futures import ThreadPoolExecutor

def section_maker(content, starting_phrase=None, ending_phrase=None):
  if starting_phrase is None and ending_phrase is None:
    return content
  if starting_phrase is None:
    end_index = content.find(ending_phrase)
    return content[:end_index]
  if ending_phrase is None:
    start_index = content.find(starting_phrase)
    return content[start_index:]
  
  start_index = content.find(starting_phrase)
  end_index = content.find(ending_phrase)
  return content[start_index:end_index]

def remove_extra_spaces(content):
  return " ".join(content.split())

def summarize_large_pdf(pdf_content, summarizer, max_length=60, min_length=1, num_threads=6):
  pdf_content = remove_extra_spaces(pdf_content)
  part_length = 512
  parts = [pdf_content[i:i+part_length] for i in range(0, len(pdf_content), part_length)]

  with ThreadPoolExecutor(max_workers=num_threads) as executor:
    summaries = list(executor.map(lambda part: summarizer(part, max_length=max_length, min_length=min_length, do_sample=False)[0]["summary_text"], parts))

  return " ".join(summaries)
