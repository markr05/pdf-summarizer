from transformers import pipeline
from concurrent.futures import ThreadPoolExecutor
from pdf_text_parser import extract, section_maker, output

def summarize_large_pdf(pdf_content, summarizer, max_length=60, min_length=1, num_threads=6):
  part_length = 512
  parts = [pdf_content[i:i+part_length] for i in range(0, len(pdf_content), part_length)]

  with ThreadPoolExecutor(max_workers=num_threads) as executor:
    summaries = list(executor.map(lambda part: summarizer(part, max_length=max_length, min_length=min_length, do_sample=False)[0]["summary_text"], parts))

  return "".join(summaries)

def summarize(args):
  print(f"Beginning summarization. Give up to 90 seconds depending on the model selected and section size.\n")

  summarizer = pipeline("summarization", model=args.model, device=args.device)

  text = extract(args.file, args.starting_page, args.ending_page)

  section = section_maker(text, starting_phrase=args.start, ending_phrase=args.end)
  if not section:
    print("Section not found")
    return
  if len(section) < 25:
    print("Section too short")
    return
  summarized_text = summarize_large_pdf(section, summarizer)
  output(summarized_text, args.output)

def extract_pdf_section(args):
  print(f"Beginning extraction. Give up to 30 seconds depending on the text size.\n")

  text = extract(args.file, args.starting_page, args.ending_page)
  section = section_maker(text, starting_phrase=args.start, ending_phrase=args.end)
  if not section:
    print("Section not found")
    return
  if len(section) < 25:
    print("Section too short")
    return
  
  output(section, args.output)
