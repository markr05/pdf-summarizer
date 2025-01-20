from tika import parser
from transformers import pipeline
from concurrent.futures import ThreadPoolExecutor

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

def summarize_large_pdf(pdf_content, summarizer, max_length=60, min_length=1, num_threads=6):
  part_length = 512
  parts = [pdf_content[i:i+part_length] for i in range(0, len(pdf_content), part_length)]

  with ThreadPoolExecutor(max_workers=num_threads) as executor:
    summaries = list(executor.map(lambda part: summarizer(part, max_length=max_length, min_length=min_length, do_sample=False)[0]["summary_text"], parts))

  return " ".join(summaries)

def output(text, output_file=None):
  print(text)
  if output_file:
    with open(output_file, "w") as f:
      f.write(text)

def summarize(args):
  print("Beginning summarization. Give up to 90 seconds depending on the model selected and section size.")

  summarizer = pipeline("summarization", model=args.model, device=args.device)

  raw = parser.from_file(args.file)

  section = section_maker(raw['content'], starting_phrase=args.start, ending_phrase=args.end)
  if not section:
    print("Section not found")
    return
  if len(section) < 25:
    print("Section too short")
    return
  summarized_text = summarize_large_pdf(section, summarizer)
  output(summarized_text, args.output)
