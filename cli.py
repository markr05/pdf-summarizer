import argparse
import pdf_processing
import time

def parse_arguments():
  parser = argparse.ArgumentParser(description="CLI tool for PDF operations")
  parser.add_argument('-t', '--timer', help="Times the function if needed", action="store_true")
  subparsers = parser.add_subparsers(dest="command", help="Available commands")
  subparsers.required = True

  pdf_summarizer = subparsers.add_parser("summarize", help="Takes a pdf and uses ai to summarize")
  pdf_summarizer.add_argument('-f', '--file', help='Path to the pdf file', required=True)
  pdf_summarizer.add_argument('-m', '--model', help='The model used to summarize (\'t5-base\' by default)', default='t5-base', required=False)
  pdf_summarizer.add_argument('-d', '--device', help='\'-1\' for CPU (default) or \'0\' for GPU', default=-1, required=False)
  pdf_summarizer.add_argument('-o', '--output', help='Output file (prints the output by default)', default=None, required=False)
  pdf_summarizer.add_argument('-t', '--threads', help='Number of CPU threads to be used (default=4)', default=4, required=False)
  pdf_summarizer.add_argument('--max_length', help='Maximum length of the summarization section (default=60)', default=60, required=False)
  pdf_summarizer.add_argument('--min_length', help='Minimum length of the summarization section (default=1)', default=1, required=False)
  pdf_summarizer.add_argument('-s', '--start', help='Starting phrase of the summarization', default=None, required=False)
  pdf_summarizer.add_argument('-e', '--end', help='Ending phrase of the summarization', default=None, required=False)
  pdf_summarizer.add_argument('-sp', '--starting_page', help='Starting page of the summarization', default=None, required=False)
  pdf_summarizer.add_argument('-ep', '--ending_page', help='Ending page of the summarization', default=None, required=False)
  pdf_summarizer.add_argument('-b', '--batch_size', help='The batch size of the summarization', default=4, required=False)
  pdf_summarizer.set_defaults(func=pdf_processing.summarize)

  pdf_extractor = subparsers.add_parser("extract", help="Takes a pdf and outputs the text")
  pdf_extractor.add_argument('-f', '--file', help='Path to the pdf file', required=True)
  pdf_extractor.add_argument('-o', '--output', help='Output file (prints the output by default)', default=None, required=False)
  pdf_extractor.add_argument('-s', '--start', help='Starting phrase of the extraction', default=None, required=False)
  pdf_extractor.add_argument('-e', '--end', help='Ending phrase of the extraction', default=None, required=False)
  pdf_extractor.add_argument('-sp', '--starting_page', help='Starting page of the extraction', default=None, required=False)
  pdf_extractor.add_argument('-ep', '--ending_page', help='Ending page of the extraction', default=None, required=False)
  pdf_extractor.set_defaults(func=pdf_processing.extract_pdf_section)

  return parser.parse_args()

def main():
  args = parse_arguments()
  if args.timer:
    start_time = time.time()
    args.func(args)
    print(f"\nThe function took {time.time() - start_time:.2f}second(s) to complete. ")
    return
  args.func(args)

if __name__ == "__main__":
  main()
