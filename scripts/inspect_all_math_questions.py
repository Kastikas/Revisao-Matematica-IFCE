import subprocess, re, json

with open("scripts/raw_ifsp_texts.json") as f:
    raw = json.load(f)

for eid, item in raw.items():
    meta = item["meta"]
    txt = item["full_text"]
    q_min, q_max = meta["q_range"]
    
    print(f"\n=======================================================")
    print(f"Exam: {meta['title']} ({meta['pdf']}) - Q{q_min} to Q{q_max}")
    print(f"=======================================================")
    
    for q in range(q_min, q_max + 1):
        # find question start
        patterns = [
            rf'(?:^|\n)\s*(?:QUESTÃO\s+)?{q}\b[.\s]',
            rf'(?:^|\n)\s*Questão\s+{q}\b',
            rf'(?:^|\n)\s*{q}\s+[A-Z\u00C0-\u00DCa-z]'
        ]
        found = False
        for p in patterns:
            m = re.search(p, txt)
            if m:
                snippet = txt[m.start():m.start()+140].replace('\n', ' ')
                print(f"  Q{q}: {snippet[:90]}...")
                found = True
                break
        if not found:
            print(f"  Q{q}: NOT FOUND DIRECTLY with simple regex")

