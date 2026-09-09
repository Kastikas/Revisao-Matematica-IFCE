import json
import re

def fix_decimals_in_text(text):
    if not isinstance(text, str):
        return text

    # 1. Corrige ocorrências de \d+{}\d+ (vírgula decimal omitida/substituída por {})
    # Ex: 3{}14 -> 3{,}14, 0{}509 -> 0{,}509, 8{}5\% -> 8{,}5\%
    text = re.sub(r"(\d+)\{\}(\d+)", r"\1{,}\2", text)

    # 2. Corrige vírgulas decimais soltas dentro de blocos matemáticos $...$ ou $$...$$
    # Ex: $3,50$ -> $3{,}50$, $\text{R\$} 220,00$ -> $\text{R\$} 220{,}00$
    def fix_math_content(content):
        def repl_decimal(m):
            p1, p2 = m.group(1), m.group(2)
            start = m.start()
            before = content[:start].rstrip()
            after = content[m.end():].lstrip()

            # Preserva conjuntos \{ ... \}
            if "\\{" in before and "\\}" in after:
                return m.group(0)
            # Preserva funções MMC, MDC, etc.
            if re.search(r"(MMC|MDC|mmc|mdc)\s*\([^)]*$", before):
                return m.group(0)
            # Preserva coordenadas cartesianas (x, y) como (-2, 0) ou T(0, 1)
            if before.endswith("(") and (after.startswith(")") or after.startswith(",")):
                return m.group(0)
            # Preserva listas numéricas separadas por vírgula: 1, 2, 3
            if before.endswith(",") or after.startswith(","):
                return m.group(0)

            return f"{p1}{{,}}{p2}"

        return re.sub(r"(\d+),(\d+)", repl_decimal, content)

    # Aplica primeiro em $$...$$
    text = re.sub(r"\$\$([^\$]+)\$\$", lambda m: f"$${fix_math_content(m.group(1))}$$", text)
    # Aplica em $...$ (ignorando \$ escapado)
    def repl_inline(m):
        raw = m.group(0)
        # Se for \$ apenas, pula
        if raw.startswith("\\$"):
            return raw
        return f"${fix_math_content(m.group(1))}$"

    # Regex para capturar $ inline sem casar com \$
    # Substitui preservando blocos
    text = re.sub(r"(?<!\\)\$([^\$]+?)(?<!\\)\$", repl_inline, text)

    return text

def walk_and_fix(obj):
    if isinstance(obj, dict):
        return {k: walk_and_fix(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [walk_and_fix(item) for item in obj]
    elif isinstance(obj, str):
        return fix_decimals_in_text(obj)
    return obj

print("Lendo mathData_augmented.json...")
with open("mathData_augmented.json", "r", encoding="utf-8") as f:
    data = json.load(f)

fixed_data = walk_and_fix(data)

with open("mathData_augmented.json", "w", encoding="utf-8") as f:
    json.dump(fixed_data, f, ensure_ascii=False, indent=2)

print("mathData_augmented.json corrigido com sucesso!")

# Corrige revisao_descritores_validados.json
validados_file = "revisao_descritores_validados.json"
if True:
    with open(validados_file, "r", encoding="utf-8") as f:
        v_data = json.load(f)
    fixed_v_data = walk_and_fix(v_data)
    with open(validados_file, "w", encoding="utf-8") as f:
        json.dump(fixed_v_data, f, ensure_ascii=False, indent=2)
    print("revisao_descritores_validados.json corrigido com sucesso!")

# Corrige revisao_descritores_provas.txt
with open("revisao_descritores_provas.txt", "r", encoding="utf-8") as f:
    txt = f.read()
fixed_txt = fix_decimals_in_text(txt)
with open("revisao_descritores_provas.txt", "w", encoding="utf-8") as f:
    f.write(fixed_txt)
print("revisao_descritores_provas.txt corrigido com sucesso!")

# Corrige mudancas_descritores_bncc.txt
with open("mudancas_descritores_bncc.txt", "r", encoding="utf-8") as f:
    m_txt = f.read()
fixed_m_txt = fix_decimals_in_text(m_txt)
with open("mudancas_descritores_bncc.txt", "w", encoding="utf-8") as f:
    f.write(fixed_m_txt)
print("mudancas_descritores_bncc.txt corrigido com sucesso!")

