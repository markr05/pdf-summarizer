import time
from tika import parser
from summarizer import section_maker, summarize_large_pdf
from transformers import pipeline

def main():
  pdf = "dog_pdf.pdf"
  device = -1
  model = "t5-small"

  summarizer = pipeline("summarization", model=model, device=device)

  raw = parser.from_file(pdf)

  start_marker = None
  end_marker = None
  section = section_maker(raw['content'], starting_phrase=start_marker, ending_phrase=end_marker)
  if not section:
    print("Section not found")
    return
  if len(section) < 25:
    print("Section too short")
    return
  
  start_time = time.time()
  summarized_text = summarize_large_pdf(section, summarizer)
  print(summarized_text)
  end_time = time.time()
  print(f"Time taken: {end_time - start_time} seconds")

if __name__ == "__main__":
  main()