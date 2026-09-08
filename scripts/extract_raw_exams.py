import subprocess, os, re, json

EXAMS = [
    {
        "id": "ifsp-2025-1-a",
        "title": "Prova IFSP 2025.1 - Prova A",
        "slug": "prova-ifsp-20251-a",
        "pdf": "IFSP_prova_2025_1_a.pdf",
        "q_range": (16, 30),
        "type": "new"
    },
    {
        "id": "ifsp-2025-1-b",
        "title": "Prova IFSP 2025.1 - Prova B",
        "slug": "prova-ifsp-20251-b",
        "pdf": "IFSP_prova_2025_1_b.pdf",
        "q_range": (16, 30),
        "type": "new"
    },
    {
        "id": "ifsp-2024-1-a",
        "title": "Prova IFSP 2024.1 - Prova A",
        "slug": "prova-ifsp-20241-a",
        "pdf": "IFSP_prova_2024_1_a.pdf",
        "q_range": (16, 30),
        "type": "new"
    },
    {
        "id": "ifsp-2024-1-b",
        "title": "Prova IFSP 2024.1 - Prova B",
        "slug": "prova-ifsp-20241-b",
        "pdf": "IFSP_prova_2024_1_b.pdf",
        "q_range": (16, 30),
        "type": "new"
    },
    {
        "id": "ifsp-2023-1-a",
        "title": "Prova IFSP 2023.1 - Prova A",
        "slug": "prova-ifsp-20231-a",
        "pdf": "IFSP_prova_2023_1_a.pdf",
        "q_range": (16, 30),
        "type": "new"
    },
    {
        "id": "ifsp-2023-1-b",
        "title": "Prova IFSP 2023.1 - Prova B",
        "slug": "prova-ifsp-20231-b",
        "pdf": "IFSP_prova_2023_1_b.pdf",
        "q_range": (16, 30),
        "type": "new"
    },
    {
        "id": "ifsp-2022-1-manha",
        "title": "Prova IFSP 2022.1 - Manhã",
        "slug": "prova-ifsp-20221-manha",
        "pdf": "IFSP_prova_2022_1_manha.pdf",
        "q_range": (16, 30),
        "type": "old_30"
    },
    {
        "id": "ifsp-2022-1-tarde",
        "title": "Prova IFSP 2022.1 - Tarde",
        "slug": "prova-ifsp-20221-tarde",
        "pdf": "IFSP_prova_2022_1_tarde.pdf",
        "q_range": (16, 30),
        "type": "old_30"
    },
    {
        "id": "ifsp-2017-2",
        "title": "Prova IFSP 2017.2",
        "slug": "prova-ifsp-20172",
        "pdf": "IFSP_prova_2017_2.pdf",
        "q_range": (21, 40),
        "type": "old_40"
    },
    {
        "id": "ifsp-2017-1",
        "title": "Prova IFSP 2017.1",
        "slug": "prova-ifsp-20171",
        "pdf": "IFSP_prova_2017_1.pdf",
        "q_range": (26, 50),
        "type": "old_50"
    },
    {
        "id": "ifsp-2016-2",
        "title": "Prova IFSP 2016.2",
        "slug": "prova-ifsp-20162",
        "pdf": "IFSP_prova_2016_2.pdf",
        "q_range": (21, 40),
        "type": "old_40"
    },
    {
        "id": "ifsp-2016-1",
        "title": "Prova IFSP 2016.1",
        "slug": "prova-ifsp-20161",
        "pdf": "IFSP_prova_2016_1.pdf",
        "q_range": (26, 50),
        "type": "old_50"
    }
]

raw_output = {}

for ex in EXAMS:
    pdf_path = os.path.join("provas/ifsp", ex["pdf"])
    txt = subprocess.run(['pdftotext', pdf_path, '-'], capture_output=True, text=True, errors='ignore').stdout
    raw_output[ex["id"]] = {
        "meta": ex,
        "full_text": txt
    }
    print(f"Loaded {ex['id']}: {len(txt)} chars")

with open("scripts/raw_ifsp_texts.json", "w", encoding="utf-8") as f:
    json.dump(raw_output, f, ensure_ascii=False, indent=2)

print("Saved raw texts to scripts/raw_ifsp_texts.json")
