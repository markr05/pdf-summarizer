from transformers import pipeline
from concurrent.futures import ThreadPoolExecutor
from pdf_text_parser import extract, section_maker, output
import torch

def summarize_large_pdf(pdf_content, summarizer, batch_size, max_length=60, min_length=1):
    # Split text into chunks of 512 tokens
    inputs = [pdf_content[i:i+512] for i in range(0, len(pdf_content), 512)]
    
    # Summarize in batches
    results = summarizer(
        inputs,
        max_length=max_length,
        min_length=min_length,
        do_sample=False,
        batch_size=int(batch_size),  # Experiment with batch size
        truncation=True,
    )
    
    return " ".join([res["summary_text"] for res in results])

def summarize(args):
  print(f"Beginning summarization. Give up to 90 seconds depending on the model selected and section size.\n")

  summarizer = pipeline("summarization", 
                        model=args.model, 
                        # device=args.device,
                        torch_dtype=torch.float16,
                        device=0 if args.device == "mps" else -1)

  torch.mps.empty_cache()
  text = extract(args.file, args.starting_page, args.ending_page)

  section = section_maker(text, starting_phrase=args.start, ending_phrase=args.end)
  if not section:
    print("Section not found")
    return
  if len(section) < 25:
    print("Section too short")
    return
  summarized_text = summarize_large_pdf(section, summarizer, args.batch_size)
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
