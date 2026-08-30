import csv
import re
import os

input_file = 'toeic_vocabulary.csv'
output_file = 'toeic_vocabulary_modified.csv'

# Pattern: English phrase (letters, spaces, hyphens) followed by parentheses
# The English phrase might have leading/trailing spaces, which we will strip
pattern = re.compile(r"([a-zA-Z][a-zA-Z\s\-]*[a-zA-Z]|[a-zA-Z])\s*[\(（]([^)）]+)[\)）]")

def process_description(desc):
    lines = desc.split('\n')
    new_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        if line.strip() == "【考試重點/搭配詞】":
            collocations = []
            i += 1
            # Collect all lines until the next section or end
            while i < len(lines) and not lines[i].startswith("【"):
                tip_text = lines[i].replace("'", "").replace('"', "")
                matches = pattern.findall(tip_text)
                for eng, chi in matches:
                    eng = eng.strip()
                    chi = chi.strip()
                    # Filter out single words if they are just the word itself, but the prompt says 
                    # "搭配詞簡化...直接翻譯". Usually they are fine.
                    colloc_str = f"{eng} {chi}"
                    if colloc_str not in collocations:
                        collocations.append(colloc_str)
                i += 1
                
            if collocations:
                new_lines.append("【搭配詞】")
                for c in collocations[:2]:
                    new_lines.append(c)
                new_lines.append("")
            continue # Already incremented i to the next section
            
        elif line.strip() == "【例句】":
            new_lines.append("【例句】")
            i += 1
            if i < len(lines) and not lines[i].startswith("【"):
                new_lines.append(lines[i]) # Keep only the first example
                i += 1
            # Skip any remaining examples
            while i < len(lines) and not lines[i].startswith("【"):
                i += 1
            new_lines.append("")
            continue
            
        else:
            new_lines.append(line)
            i += 1
            
    # Clean up trailing empty lines
    while new_lines and new_lines[-1] == "":
        new_lines.pop()
        
    return "\n".join(new_lines)


count_processed = 0
count_removed = 0

with open(input_file, 'r', encoding='utf-8') as fin, open(output_file, 'w', encoding='utf-8', newline='') as fout:
    reader = csv.reader(fin)
    writer = csv.writer(fout, quoting=csv.QUOTE_MINIMAL)
    
    for row in reader:
        if not row:
            continue
            
        word = row[0].strip()
        
        # Rule 1: Remove rows where word has space (more than one word)
        if ' ' in word:
            count_removed += 1
            continue
            
        desc = row[1] if len(row) > 1 else ""
        
        # Rule 2, 3, 4 processed here
        new_desc = process_description(desc)
        
        # Rule 2: Ensure [衍生字] is 【詞性變化】
        # (It's already 【詞性變化】 in the current CSV, but just in case we replace it)
        new_desc = new_desc.replace("[衍生字]", "【詞性變化】")
        
        writer.writerow([word, new_desc])
        count_processed += 1

print(f"Processed {count_processed} words. Removed {count_removed} multi-word phrases.")
os.replace(output_file, input_file)
