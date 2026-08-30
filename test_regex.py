from datasets import load_dataset
import re

ds = load_dataset('kknono668/toeic-vocab-tw', split='train')

pattern_quoted = re.compile(r"['\"]([a-zA-Z\s\-]+)['\"]\s*[\(（]([^)）]+)[\)）]")
pattern_unquoted = re.compile(r"([a-zA-Z\s\-]+)\s*[\(（]([^)）a-zA-Z]+)[\)）]")

count_quoted = 0
count_unquoted = 0

for row in ds:
    tips = row.get('exam_tips', [])
    for tip in tips:
        m1 = pattern_quoted.findall(tip)
        if m1: count_quoted += 1
        
        # Test unquoted (just any english words followed by chinese in parens)
        # We need to limit the english words to not include the whole sentence.
        # Maybe split by space and take last 2-3 words?
        pass

print(f"Total quoted matches found in rows: {count_quoted}")
