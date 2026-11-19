# 把 toeic_vocabulary.csv 轉成 App 開啟時直接載入的 toeic_vocabulary.json（改過 CSV 後重新執行一次）
import csv, json

rows = []
with open('toeic_vocabulary.csv', encoding='utf-8-sig', newline='') as f:
    for r in csv.reader(f):
        if len(r) >= 2 and r[0].strip():
            rows.append([r[0].strip(), r[1].strip()])

with open('toeic_vocabulary.json', 'w', encoding='utf-8') as f:
    json.dump(rows, f, ensure_ascii=False, separators=(',', ':'))

print(f'{len(rows)} words -> toeic_vocabulary.json')
