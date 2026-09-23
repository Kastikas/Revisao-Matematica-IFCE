#!/usr/bin/env python3
"""
scripts/manage_mathdata.py - Ferramenta Unificada de Gestão, Validação e Ingestão do mathData.json

Funcionalidades:
  1. import: Ingestão de novos exames/tópicos a partir de um JSON estruturado.
  2. validate: Auditoria rigorosa de schema, acessibilidade de imagens e sintaxe KaTeX.
  3. sanitize: Higienização automática (vírgulas decimais brasileiras e escape de moedas).
  4. export: Exportação de tópicos ou blocos para JSON isolado.
  5. template: Geração de template JSON para novas provas.
  6. crop-image: Extração precisa e otimizada de figuras de PDFs via PyMuPDF/PIL/optipng.
  7. parse-pdf: Extração automatizada de questões, gabaritos e figuras a partir de PDFs.
  8. drive-test: Validação de conexão e permissões da Google Drive API via Service Account.
  9. drive-upload: Upload de figura avulsa para o Google Drive com geração de link público.
  10. drive-sync: Sincronização em lote de assets/img/questoes/ com o Google Drive e mathData.json.

Uso:
  python3 scripts/manage_mathdata.py import -f prova.json -b 8 --build
  python3 scripts/manage_mathdata.py validate
  python3 scripts/manage_mathdata.py sanitize --apply
  python3 scripts/manage_mathdata.py crop-image -p prova.pdf --page 5 --rect 100 200 450 500 -o assets/img/questoes/ifmg/fig.png
  python3 scripts/manage_mathdata.py parse-pdf -p prova.pdf --q-start 16 --q-end 30 -o prova.json
  python3 scripts/manage_mathdata.py drive-test
  python3 scripts/manage_mathdata.py drive-upload -f assets/img/questoes/ifmg/ifmg-2025-1-q17.png
  python3 scripts/manage_mathdata.py drive-sync --dry-run
"""

import os
import sys
import json
import re
import shutil
import argparse
import subprocess
import unicodedata
from datetime import datetime

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MATH_DATA_PATH = os.path.join(ROOT_DIR, "mathData.json")


# ==============================================================================
# 1. HIGIENIZADOR E FORMATADOR DE TEXTO (TextSanitizer)
# ==============================================================================
class TextSanitizer:
    @staticmethod
    def fix_decimal_commas_in_math(text: str) -> str:
        """Converte vírgulas decimais em blocos KaTeX para {,} conforme regra 5 do GEMINI.md."""
        if not text or not isinstance(text, str):
            return text

        # Corrige notações vazias 3{}14 -> 3{,}14
        text = re.sub(r"(\d+)\{\}(\d+)", r"\1{,}\2", text)

        def fix_math_content(content):
            def repl_decimal(m):
                p1, p2 = m.group(1), m.group(2)
                start = m.start()
                before = content[:start].rstrip()
                after = content[m.end():].lstrip()

                # Preserva conjuntos \{ 1, 2 \}
                if "\\{" in before and "\\}" in after:
                    return m.group(0)
                # Preserva funções MMC, MDC
                if re.search(r"(MMC|MDC|mmc|mdc)\s*\([^)]*$", before, re.IGNORECASE):
                    return m.group(0)
                # Preserva coordenadas cartesianas (2, 3)
                if before.endswith("(") and (after.startswith(")") or after.startswith(",")):
                    return m.group(0)
                # Preserva listas de itens
                if before.endswith(",") or after.startswith(","):
                    return m.group(0)

                return f"{p1}{{,}}{p2}"

            return re.sub(r"(\d+),(\d+)", repl_decimal, content)

        # Trata $$...$$
        text = re.sub(r"\$\$([\s\S]*?)\$\$", lambda m: f"$${fix_math_content(m.group(1))}$$", text)

        # Trata $...$ inline (sem casar com \$)
        def repl_inline(m):
            raw = m.group(0)
            if raw.startswith(r"\$"):
                return raw
            return f"${fix_math_content(m.group(1))}$"

        text = re.sub(r"(?<!\\)\$([^\$]+?)(?<!\\)\$", repl_inline, text)
        return text

    @staticmethod
    def fix_currency_delimiters(text: str) -> str:
        """
        Padroniza valores monetários como $\text{R\$} ...$ e previne colisões com o
        delimitador inline do KaTeX ($).
        Exemplos:
          - R$ 100,00 -> $\text{R\$} 100{,}00$
          - US$ 5,00 -> $\text{US\$} 5{,}00$
          - \R$ -> \text{R\$}
        """
        if not text or not isinstance(text, str):
            return text

        # Corrige macros quebradas como \R$
        text = text.replace(r"\R$", r"\text{R\$}")
        text = text.replace(r"\text{R$}", r"\text{R\$}")
        text = text.replace(r"\text{R\$\;}", r"\text{R\$}")
        text = re.sub(r"\\R\$(?![a-zA-Z])\s*", r"\\text{R\\$} ", text)

        def format_comma(val):
            return re.sub(r"(\d+),(\d+)", r"\1{,}\2", val)

        def sanitize_inline_and_text(s):
            if not s:
                return s
            # Menções contextuais a moedas sem valor numérico: (R$), (US$), sobre R$, em R$, etc.
            s = re.sub(r"\((R|US)\$\)", r"(\1\\$)", s)
            s = re.sub(r"\b(em|de|sobre|para|valores em)\s+(R|US)\$", r"\1 \2\\$", s)

            # Converte valores com R$ em texto para $\text{R\$} X{,}XX$
            # Garantindo que não seja precedido por $, \ ou parte de outra palavra (ex: $R$ ou 4R$ que são variáveis)
            s = re.sub(r"(?<![\$\\])\bR\$\s*([0-9]+(?:\.[0-9]{3})*(?:,[0-9]+)?)", lambda m: "$\\text{R\\$} " + format_comma(m.group(1).strip()) + "$", s)
            s = re.sub(r"(?<![\$\\])\bUS\$\s*([0-9]+(?:\.[0-9]{3})*(?:,[0-9]+)?)", lambda m: "$\\text{US\\$} " + format_comma(m.group(1).strip()) + "$", s)

            # Vírgulas decimais dentro de blocos inline $...$
            def fix_inline(m):
                inner = m.group(1)
                return "$" + format_comma(inner) + "$"
            s = re.sub(r"(?<!\\)\$([^\$]+?)(?<!\\)\$", fix_inline, s)
            return s

        # Tokenização por blocos display math ($$...$$)
        display_parts = []
        last_d = 0
        for dm in re.finditer(r"\$\$([\s\S]*?)\$\$", text):
            non_disp = text[last_d:dm.start()]
            display_parts.append(sanitize_inline_and_text(non_disp))

            inner_math = dm.group(1)
            inner_math = re.sub(r"(?<!\\text\{)R\$\s*", r"\\text{R\\$} ", inner_math)
            inner_math = re.sub(r"(?<!\\text\{)US\$\s*", r"\\text{US\\$} ", inner_math)
            inner_math = re.sub(r"(\d+),(\d+)", lambda d: format_comma(d.group(0)), inner_math)
            display_parts.append(f"$${inner_math}$$")
            last_d = dm.end()

        non_disp = text[last_d:]
        display_parts.append(sanitize_inline_and_text(non_disp))
        return "".join(display_parts)

    @staticmethod
    def fix_html_in_math(text: str) -> str:
        """Remove tags HTML indevidamente envolvidas por delimitadores de fórmula ($$)."""
        if not text or not isinstance(text, str):
            return text

        # Trata duplicações de delimitadores display: $$$$ -> $$\n$$
        text = re.sub(r"\$\$\s*\$\$", "$$\n$$", text)

        # Trata tags como $$<br>...$$ -> quebra em blocos válidos
        def clean_display_html(m):
            inner = m.group(1)
            if re.search(r"<[^>]+>", inner):
                parts = re.split(r"(<br\s*/?>)", inner, flags=re.IGNORECASE)
                res = []
                for p in parts:
                    if re.match(r"^<br\s*/?>$", p, re.IGNORECASE):
                        res.append(p)
                    elif p.strip():
                        sub_parts = re.split(r"(<[^>]+>)", p)
                        for sp in sub_parts:
                            if sp.startswith("<"):
                                res.append(sp)
                            elif sp.strip():
                                res.append(f"$${sp.strip()}$$")
                    else:
                        res.append(p)
                return "".join(res)
            return m.group(0)

        text = re.sub(r"\$\$([\s\S]*?)\$\$", clean_display_html, text)
        return text

    @staticmethod
    def fix_text_mode_math_commands(text: str) -> str:
        """Extrai comandos de modo matemático indevidamente colocados dentro de \\text{...}."""
        if not text or not isinstance(text, str):
            return text
        def repl_text_cdot(m):
            inner = m.group(1)
            parts = inner.split(r"\cdot")
            return " \\cdot ".join([f"\\text{{{p}}}" for p in parts if p.strip()])
        text = re.sub(r"\\text\{([^}]*?\\cdot[^}]*?)\}", repl_text_cdot, text)
        return text

    @staticmethod
    def fix_pdf_ligatures(text: str) -> str:
        """Corrige quebras de ligaturas comuns em PDFs de processos seletivos (ti, fi, fl)."""
        if not text or not isinstance(text, str):
            return text
        broken_fixes = [
            (r"\bgráfi\s+co\b", "gráfico"), (r"\bgráfi\s+cos\b", "gráficos"),
            (r"\bafi\s*rmati\s*va\b", "afirmativa"), (r"\bafi\s*rmati\s*vas\b", "afirmativas"),
            (r"\bfi\s+gura\b", "figura"), (r"\bfi\s+guras\b", "figuras"),
            (r"\bsuperfí\s+cie\b", "superfície"), (r"\bsuperfí\s+cies\b", "superfícies"),
            (r"\buti\s+lizado\b", "utilizado"), (r"\buti\s+lizada\b", "utilizada"),
            (r"\buti\s+lizados\b", "utilizados"), (r"\buti\s+lizadas\b", "utilizadas"),
            (r"\buti\s+lizando\b", "utilizando"), (r"\bdisti\s+nta\b", "distinta"),
            (r"\bdisti\s+ntas\b", "distintas"), (r"\bobti\s+do\b", "obtido"),
            (r"\bobti\s+da\b", "obtida"), (r"\bobti\s+dos\b", "obtidos"),
            (r"\bobti\s+das\b", "obtidas"), (r"\bquanti\s+dade\b", "quantidade"),
            (r"\bquanti\s+dades\b", "quantidades"), (r"\balternati\s+va\b", "alternativa"),
            (r"\balternati\s+vas\b", "alternativas"), (r"\bidenti\s+fi\s+car\b", "identificar"),
            (r"\bsigni\s+fi\s+ca\b", "significa")
        ]
        for pat, rep in broken_fixes:
            text = re.sub(pat, rep, text, flags=re.IGNORECASE)
        return text

    @classmethod
    def sanitize_all(cls, text: str) -> str:
        """Executa a suíte completa de higienização de texto."""
        if not text or not isinstance(text, str):
            return text
        text = cls.fix_pdf_ligatures(text)
        text = cls.fix_text_mode_math_commands(text)
        text = cls.fix_html_in_math(text)
        text = cls.fix_currency_delimiters(text)
        text = cls.fix_decimal_commas_in_math(text)
        return text


# ==============================================================================
# 2. VALIDADOR DE KATEX (KaTeXValidator)
# ==============================================================================
class KaTeXValidator:
    @staticmethod
    def extract_math_blocks(text: str, location: str) -> list:
        """Extrai todos os blocos display ($$...$$) e inline ($...$) de um texto com sua localização."""
        blocks = []
        if not text or not isinstance(text, str):
            return blocks
        for m in re.finditer(r"\$\$([\s\S]*?)\$\$", text):
            blocks.append({"math": m.group(1).strip(), "isDisplay": True, "location": f"{location} [display]"})
        clean = re.sub(r"\$\$[\s\S]*?\$\$", " ", text)
        clean = re.sub(r"\\\$", " ", clean)
        for m in re.finditer(r"\$([^\$]+)\$", clean):
            blocks.append({"math": m.group(1).strip(), "isDisplay": False, "location": f"{location} [inline]"})
        return blocks

    @staticmethod
    def validate_with_katex_engine(math_items: list) -> list:
        """
        Executa validação no motor KaTeX real via Node.js usando scripts/katex.min.js.
        math_items: lista de dicts com {"math": ..., "isDisplay": bool, "location": ...}
        """
        katex_js_path = os.path.join(os.path.dirname(__file__), "katex.min.js")
        if not os.path.exists(katex_js_path) or not shutil.which("node") or not math_items:
            return []

        node_script = """
const katex = require(process.argv[1]);
const readline = require("readline");

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  terminal: false
});

rl.on("line", (line) => {
  if (!line.trim()) return;
  const item = JSON.parse(line);
  try {
    katex.renderToString(item.math, { displayMode: item.isDisplay, throwOnError: true });
  } catch (err) {
    console.log(JSON.stringify({ location: item.location, math: item.math, error: err.message }));
  }
});
"""
        proc = subprocess.Popen(
            ["node", "-e", node_script, katex_js_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        for item in math_items:
            proc.stdin.write(json.dumps(item) + "\n")
        stdout, _ = proc.communicate()

        issues = []
        for line in stdout.strip().splitlines():
            if line.strip():
                try:
                    data = json.loads(line)
                    issues.append({
                        "location": data["location"],
                        "type": "KATEX_ENGINE_ERROR",
                        "message": data["error"],
                        "snippet": data["math"]
                    })
                except Exception:
                    pass
        return issues

    @staticmethod
    def validate_text(text: str, location: str) -> list:
        """Valida a sintaxe KaTeX de um campo de texto."""
        issues = []
        if not text or not isinstance(text, str):
            return issues

        # 1. Checa delimitadores $ não escapados
        clean = re.sub(r"\$\$[\s\S]*?\$\$", "", text)
        clean = re.sub(r"\\\$", "", clean)
        if clean.count("$") % 2 != 0:
            issues.append({
                "location": location,
                "type": "UNPAIRED_DELIMITER",
                "message": "Número ímpar de delimitadores de fórmula inline ($). Pode indicar falta de escape em moeda ou fórmula truncada.",
                "snippet": clean[:100]
            })

        # 2. Extrai expressões $$...$$ e $...$
        math_blocks = []
        for m in re.finditer(r"\$\$([\s\S]*?)\$\$", text):
            math_blocks.append((m.group(1), True, m.start()))
        
        text_without_disp = re.sub(r"\$\$[\s\S]*?\$\$", " ", text)
        # Tokeniza inline ignorando \$
        i = 0
        while i < len(text_without_disp):
            if text_without_disp[i] == '$' and (i == 0 or text_without_disp[i-1] != '\\'):
                start = i + 1
                end = -1
                for j in range(start, len(text_without_disp)):
                    if text_without_disp[j] == '$' and text_without_disp[j-1] != '\\':
                        end = j
                        break
                if end != -1:
                    math_blocks.append((text_without_disp[start:end], False, start))
                    i = end + 1
                    continue
            i += 1

        # 3. Análise léxica e estrutural de cada expressão
        for tex, is_disp, pos in math_blocks:
            # Chaves desbalanceadas
            if tex.count("{") != tex.count("}"):
                issues.append({
                    "location": location,
                    "type": "UNBALANCED_BRACES",
                    "message": f"Chaves desbalanceadas: {tex.count('{')} abertas vs {tex.count('}')} fechadas.",
                    "snippet": tex[:120]
                })

            # Ambientes \begin e \end
            begins = re.findall(r"\\begin\{([^}]+)\}", tex)
            ends = re.findall(r"\\end\{([^}]+)\}", tex)
            if begins != ends:
                issues.append({
                    "location": location,
                    "type": "MISMATCHED_ENV",
                    "message": f"Ambientes incompatíveis: begin={begins} vs end={ends}.",
                    "snippet": tex[:120]
                })

            # Alinhamento @ no ambiente array (não suportado pelo KaTeX)
            if re.search(r"\\begin\{array\}\{[^}]*@[^}]*\}", tex):
                issues.append({
                    "location": location,
                    "type": "KATEX_UNSUPPORTED_ARRAY_ALIGN",
                    "message": "Especificador '@' em \\begin{array} não é suportado pelo KaTeX.",
                    "snippet": tex[:120]
                })

            # Comando \cdot dentro de \text{}
            if re.search(r"\\text\{[^}]*\\cdot[^}]*\}", tex):
                issues.append({
                    "location": location,
                    "type": "CDOT_IN_TEXT_MODE",
                    "message": "\\cdot dentro de \\text{...} não é reconhecido em modo de texto.",
                    "snippet": tex[:120]
                })

            # Uso incorreto de \R$
            if r"\R$" in tex or r"\R " in tex:
                issues.append({
                    "location": location,
                    "type": "INVALID_COMMAND_R_DOLLAR",
                    "message": "Comando inválido \\R$ em modo matemático. Use \\text{R\\$} ou similar.",
                    "snippet": tex[:120]
                })

            # Tags HTML dentro de fórmulas
            if re.search(r"<(?:br|strong|p|div|b|i|span)[^>]*>", tex, re.IGNORECASE):
                issues.append({
                    "location": location,
                    "type": "HTML_INSIDE_LATEX",
                    "message": "Tags HTML encontradas dentro do bloco KaTeX.",
                    "snippet": tex[:120]
                })

        return issues


# ==============================================================================
# 3. VALIDADOR DE SCHEMA E ACESSIBILIDADE (SchemaValidator)
# ==============================================================================
class SchemaValidator:
    REQUIRED_QUESTION_FIELDS = ["q", "options", "correct", "explanation", "bncc"]

    @staticmethod
    def validate_question(q: dict, location: str) -> list:
        issues = []

        # Campos obrigatórios
        for req in SchemaValidator.REQUIRED_QUESTION_FIELDS:
            if req not in q or q[req] is None:
                issues.append({
                    "location": location,
                    "type": "MISSING_FIELD",
                    "message": f"Campo obrigatório '{req}' ausente ou nulo."
                })

        # Validação de alternativas
        options = q.get("options")
        if not isinstance(options, list) or len(options) not in (4, 5):
            issues.append({
                "location": location,
                "type": "INVALID_OPTIONS",
                "message": f"O campo 'options' deve ser uma lista com 4 ou 5 alternativas (encontrado: {len(options) if isinstance(options, list) else type(options)})."
            })

        # Validação de gabarito
        correct = q.get("correct")
        if not isinstance(correct, int) or (isinstance(options, list) and (correct < 0 or correct >= len(options))):
            issues.append({
                "location": location,
                "type": "INVALID_CORRECT_INDEX",
                "message": f"O campo 'correct' deve ser um inteiro válido entre 0 e {len(options)-1 if isinstance(options, list) else 'N'} (encontrado: {correct})."
            })

        # Validação de imagem (Regras 2 e 3 do GEMINI.md)
        image = q.get("image")
        if image is not None:
            if not isinstance(image, dict):
                issues.append({
                    "location": location,
                    "type": "IMAGE_NOT_OBJECT",
                    "message": "O campo 'image' deve ser um objeto no formato {'src', 'alt', 'caption'}, nunca uma string direta."
                })
            else:
                src = image.get("src")
                alt = image.get("alt")
                if not src:
                    issues.append({
                        "location": location,
                        "type": "IMAGE_MISSING_SRC",
                        "message": "Objeto 'image' não possui 'src' definido."
                    })
                if not alt or not alt.strip():
                    issues.append({
                        "location": location,
                        "type": "IMAGE_MISSING_ALT",
                        "message": "Objeto 'image' não possui 'alt' (descrição de acessibilidade obrigatória)."
                    })
                else:
                    # Checagem de Spoilers/Resoluções no alt/caption (Regra 2)
                    spoilers = ["resolução", "gabarito", "resposta correta", "triângulo auxiliar", "traçado auxiliar"]
                    for sp in spoilers:
                        if sp in alt.lower():
                            issues.append({
                                "location": location,
                                "type": "IMAGE_ALT_SPOILER",
                                "message": f"O alt da imagem contém possíveis traçados/spoilers de resolução proibidos pela Regra 2: '{sp}'."
                            })

                # Se o arquivo for local, valida existência
                if src and src.startswith("assets/img/questoes/"):
                    local_path = os.path.join(ROOT_DIR, src)
                    if not os.path.exists(local_path):
                        issues.append({
                            "location": location,
                            "type": "LOCAL_IMAGE_NOT_FOUND",
                            "message": f"Imagem local não encontrada no disco: {src}"
                        })

        return issues


# ==============================================================================
# 4. EXTRATOR E OTIMIZADOR DE IMAGENS (ImageExtractor)
# ==============================================================================
class ImageExtractor:
    @staticmethod
    def crop_region(pdf_path: str, page_num: int, rect_coords: tuple, output_path: str, dpi: int = 200, pad: int = 8, optimize: bool = True):
        """
        Recorta com alta precisão uma região do PDF, elimina margens brancas e otimiza via pngquant/optipng.
        """
        try:
            import pymupdf
        except ImportError:
            raise ImportError("PyMuPDF não está instalado. Execute: pip install pymupdf")

        try:
            from PIL import Image, ImageChops
        except ImportError:
            raise ImportError("Pillow (PIL) não está instalado. Execute: pip install pillow")

        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF não encontrado: {pdf_path}")

        doc = pymupdf.open(pdf_path)
        if page_num < 1 or page_num > len(doc):
            raise ValueError(f"Página inválida {page_num}. O PDF possui {len(doc)} páginas.")

        page = doc[page_num - 1]
        rect = pymupdf.Rect(*rect_coords)
        pix = page.get_pixmap(clip=rect, dpi=dpi)

        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Aparar margens brancas automaticamente
        bg = Image.new(img.mode, img.size, (255, 255, 255))
        diff = ImageChops.difference(img, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        if bbox:
            w, h = img.size
            crop_box = (
                max(0, bbox[0] - pad),
                max(0, bbox[1] - pad),
                min(w, bbox[2] + pad),
                min(h, bbox[3] + pad)
            )
            img = img.crop(crop_box)

        abs_output = os.path.join(ROOT_DIR, output_path) if not os.path.isabs(output_path) else output_path
        os.makedirs(os.path.dirname(abs_output), exist_ok=True)
        img.save(abs_output, "PNG")

        if optimize:
            ImageExtractor.optimize_png(abs_output)

        print(f"✅ Imagem extraída com sucesso ({img.width}x{img.height} px): {abs_output}")
        return abs_output

    @staticmethod
    def optimize_png(img_path: str):
        """Otimiza imagem PNG usando pngquant e optipng se disponíveis."""
        if shutil.which("pngquant"):
            subprocess.run(["pngquant", "--force", "--ext", ".png", "--quality=80-95", "--speed", "1", img_path], capture_output=True)
        if shutil.which("optipng"):
            subprocess.run(["optipng", "-quiet", "-o2", img_path], capture_output=True)


# ==============================================================================
# 5. PARSER AUTOMATIZADO DE PDFS (PDFParser)
# ==============================================================================
class PDFParser:
    """
    Extrai, estrutura e higieniza questões a partir de cadernos de prova oficiais em PDF.
    Identifica enunciados, alternativas A-E, gabaritos e elementos visuais (figuras/desenhos).
    """

    @staticmethod
    def slugify(text: str) -> str:
        """Gera um slug canônico para o ID da prova (ex: 'ifmg-2025-1')."""
        base = os.path.splitext(os.path.basename(text))[0]
        norm = unicodedata.normalize("NFKD", base).encode("ASCII", "ignore").decode("ASCII").lower()
        norm = re.sub(r"(?:prova|caderno|exame|processo|seletivo|gabarito)", "", norm)
        norm = re.sub(r"[^a-z0-9]+", "-", norm).strip("-")
        return re.sub(r"-+", "-", norm)

    @staticmethod
    def derive_title(slug: str) -> str:
        """Infere um título formatado a partir do slug (ex: 'ifmg-2025-1' -> 'IFMG 2025.1')."""
        m = re.search(r"([a-z]+)[-_](\d{4})(?:[-_](\d+))?", slug)
        if m:
            inst = m.group(1).upper()
            ano = m.group(2)
            sem = f".{m.group(3)}" if m.group(3) else ""
            return f"{inst} {ano}{sem}"
        return slug.replace("-", " ").title()

    @staticmethod
    def clean_text(text: str) -> str:
        """Higieniza ligaduras do PDF, junta quebras de linha e remove excesso de espaços."""
        text = TextSanitizer.fix_pdf_ligatures(text)
        # Corrige hifens no fim da linha
        text = re.sub(r"(\w+)-\s*\n\s*(\w+)", r"\1\2", text)
        lines = [l.strip() for l in text.splitlines()]
        joined = []
        for l in lines:
            if not l:
                if joined and joined[-1] != "":
                    joined.append("")
                continue
            if joined and joined[-1] != "":
                prev = joined[-1]
                # Se a linha anterior não terminou com pontuação forte, junta com espaço
                if not prev.endswith((".", ":", "?", "!", ";", ")", "]")):
                    joined[-1] = prev + " " + l
                else:
                    joined.append(l)
            else:
                joined.append(l)
        res = "\n\n".join([j for j in joined if j])
        return re.sub(r"[ \t]+", " ", res)

    @staticmethod
    def split_enunciado_and_options(raw_text: str) -> tuple:
        """
        Separa o enunciado das alternativas (A-E). Suporta múltiplos formatos:
        a), A), (A), a., A., a -
        """
        lines = raw_text.splitlines()
        opt_starts = []
        expected = ["A", "B", "C", "D", "E"]
        exp_idx = 0

        for idx, l in enumerate(lines):
            m = re.match(r"^\s*(?:\(([a-eA-E])\)|([a-eA-E])[\)\.\-])(?:\s+(.*))?$", l)
            if m:
                letter = (m.group(1) or m.group(2)).upper()
                if exp_idx < len(expected) and letter == expected[exp_idx]:
                    content = m.group(3) or ""
                    opt_starts.append((idx, letter, content))
                    exp_idx += 1

        if len(opt_starts) in (4, 5):
            q_lines = lines[:opt_starts[0][0]]
            q_text = PDFParser.clean_text("\n".join(q_lines))
            options = []
            for i in range(len(opt_starts)):
                start_line = opt_starts[i][0]
                end_line = opt_starts[i+1][0] if i+1 < len(opt_starts) else len(lines)
                first_line_content = opt_starts[i][2]
                remaining_lines = lines[start_line+1:end_line]

                # Remove eventuais cabeçalhos de disciplinas subsequentes da última opção
                filtered_remaining = []
                for rem in remaining_lines:
                    rem_upper = rem.upper()
                    if any(h in rem_upper for h in ["CIENCIAS DA NATUREZA", "LINGUAGENS", "CIENCIAS HUMANAS", "PROVA DE"]):
                        break
                    filtered_remaining.append(rem)

                opt_text = (first_line_content + " " + " ".join([l.strip() for l in filtered_remaining if l.strip()])).strip()
                opt_text = PDFParser.clean_text(opt_text)
                if not opt_text:
                    opt_text = "[Alternativa visual - ver figura]"
                options.append(opt_text)
            return q_text, options

        return PDFParser.clean_text(raw_text), ["[Alternativa A]", "[Alternativa B]", "[Alternativa C]", "[Alternativa D]"]

    @staticmethod
    def find_matching_gabarito(pdf_path: str) -> str:
        """Procura gabarito oficial correspondente na mesma pasta ou subpastas de gabaritos."""
        dirname = os.path.dirname(os.path.abspath(pdf_path))
        basename = os.path.basename(pdf_path)

        m = re.search(r"(\d{4})[_\.\-](\d)", basename)
        if not m:
            return None
        year, sem = m.group(1), m.group(2)

        candidate_dirs = [dirname]
        for d in os.listdir(dirname):
            sub = os.path.join(dirname, d)
            if os.path.isdir(sub) and "gabarito" in d.lower():
                candidate_dirs.append(sub)

        for cdir in candidate_dirs:
            for f in os.listdir(cdir):
                f_lower = f.lower()
                if "gabarito" in f_lower and year in f_lower and (f".{sem}" in f_lower or f"_{sem}" in f_lower or f"-{sem}" in f_lower):
                    return os.path.join(cdir, f)
        return None

    @staticmethod
    def parse_gabarito(source: str, q_start: int = 1) -> dict:
        """Extrai mapeamento de respostas de um gabarito em PDF, arquivo TXT ou string direta."""
        answers = {}
        if not source:
            return answers

        if os.path.exists(source):
            text = ""
            if source.lower().endswith(".pdf"):
                try:
                    import pymupdf
                    doc = pymupdf.open(source)
                    for page in doc:
                        text += page.get_text() + "\n"
                except Exception as e:
                    print(f"⚠️ Erro ao ler gabarito PDF: {e}")
                    return answers
            else:
                with open(source, "r", encoding="utf-8") as f:
                    text = f.read()

            for m in re.finditer(r"\b(\d{1,2})\s*[\-:\.\t\|\s]+\s*(anulada|cancelada|[A-Ea-e])\b", text, re.IGNORECASE):
                q_num = int(m.group(1))
                val = m.group(2).upper()
                answers[q_num] = "ANULADA" if ("ANUL" in val or "CANC" in val) else val

            if len(answers) < 5:
                lines = [l.strip() for l in text.splitlines() if l.strip()]
                for i, line in enumerate(lines):
                    if line.isdigit() and 1 <= int(line) <= 60:
                        q_num = int(line)
                        if i + 1 < len(lines):
                            next_l = lines[i+1].upper()
                            if next_l in ["A", "B", "C", "D", "E"]:
                                answers[q_num] = next_l
                            elif "ANUL" in next_l or "CANC" in next_l:
                                answers[q_num] = "ANULADA"
        else:
            if ":" in source or "=" in source:
                pairs = re.findall(r"(\d{1,2})\s*[:=]\s*(anulada|cancelada|[A-Ea-e])", source, re.IGNORECASE)
                for q_num_str, ans in pairs:
                    q_num = int(q_num_str)
                    answers[q_num] = "ANULADA" if "anul" in ans.lower() else ans.upper()
            else:
                letters = [x.strip().upper() for x in re.split(r"[,\s]+", source) if x.strip()]
                cur_q = q_start
                for letter in letters:
                    if letter in ["A", "B", "C", "D", "E"] or "ANUL" in letter:
                        answers[cur_q] = "ANULADA" if "ANUL" in letter else letter
                        cur_q += 1

        return answers

    @classmethod
    def parse_pdf(
        cls,
        pdf_path: str,
        q_start: int = None,
        q_end: int = None,
        pages: list = None,
        exam_id: str = None,
        exam_title: str = None,
        gabarito_src: str = None,
        header_regex: str = None,
        auto_crop: bool = False,
        upload_drive: bool = False,
        folder_id: str = None,
        dpi: int = 200,
        pad: int = 8
    ) -> tuple:
        """
        Executa o pipeline completo de extração, estruturação e corte de figuras.
        Retorna (topic_dict, stats_dict).
        """
        try:
            import pymupdf
        except ImportError:
            raise ImportError("PyMuPDF não está instalado. Execute: pip install pymupdf")

        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"Caderno PDF não encontrado: {pdf_path}")

        exam_id = exam_id or cls.slugify(pdf_path)
        exam_title = exam_title or cls.derive_title(exam_id)

        doc = pymupdf.open(pdf_path)
        total_pages = len(doc)

        # Gabarito
        gab_path = gabarito_src or cls.find_matching_gabarito(pdf_path)
        gabarito = cls.parse_gabarito(gab_path, q_start=q_start or 1)
        if gab_path:
            print(f"📋 Gabarito oficial vinculado: {gab_path} ({len(gabarito)} respostas identificadas)")

        # Páginas a varrer
        if pages:
            scan_page_indices = [p - 1 for p in pages if 1 <= p <= total_pages]
        else:
            scan_page_indices = list(range(total_pages))

        # 1. Agrupamento de blocos de texto por questão
        questions_raw = {}
        current_q = None

        # Padrão padrão de cabeçalho
        pattern_header = header_regex or r"^QUESTAO\s+(\d+)\b"

        for p_idx in scan_page_indices:
            page = doc[p_idx]
            page_num = p_idx + 1
            blocks = page.get_text("blocks")
            for b in blocks:
                if b[6] == 0:  # Bloco de texto
                    norm = unicodedata.normalize("NFKD", b[4]).encode("ASCII", "ignore").decode("ASCII").upper().strip()
                    m = re.search(pattern_header, norm)
                    if m:
                        current_q = int(m.group(1))
                        if current_q not in questions_raw:
                            questions_raw[current_q] = {"blocks": [], "pages": set(), "visuals": []}

                    if current_q is not None:
                        # Ignora números de página isolados e cabeçalhos genéricos
                        if not (norm.isdigit() and len(norm) <= 2) and "MATEMATICA" not in norm:
                            questions_raw[current_q]["blocks"].append((page_num, b))
                            questions_raw[current_q]["pages"].add(page_num)

        # Se o padrão padrão encontrou menos de 2 questões, tenta fallback (ex: IFCE com '16. ')
        if len(questions_raw) < 2 and not header_regex:
            print("ℹ️ Cabeçalhos 'QUESTÃO XX' não detectados; testando padrão numérico 'XX.'...")
            questions_raw.clear()
            current_q = None
            for p_idx in scan_page_indices:
                page = doc[p_idx]
                page_num = p_idx + 1
                blocks = page.get_text("blocks")
                for b in blocks:
                    if b[6] == 0:
                        lines = [l.strip() for l in b[4].splitlines() if l.strip()]
                        if lines:
                            m = re.match(r"^(\d{1,2})\.(?:\s+|$)", lines[0])
                            if m and 1 <= int(m.group(1)) <= 60:
                                current_q = int(m.group(1))
                                if current_q not in questions_raw:
                                    questions_raw[current_q] = {"blocks": [], "pages": set(), "visuals": []}
                        if current_q is not None:
                            questions_raw[current_q]["blocks"].append((page_num, b))
                            questions_raw[current_q]["pages"].add(page_num)

        # 2. Detecção e vinculação espacial de imagens e desenhos
        for p_idx in scan_page_indices:
            page = doc[p_idx]
            page_num = p_idx + 1

            # Imagens raster
            page_visuals = []
            for im in page.get_image_info():
                page_visuals.append({
                    "page": page_num,
                    "bbox": [round(x, 1) for x in im["bbox"]],
                    "type": "raster"
                })

            # Desenhos vetoriais significativos (se não houver raster ou complementares)
            drawings = page.get_drawings()
            sig_drawings = [d for d in drawings if d["rect"].width > 40 and d["rect"].height > 40]
            if sig_drawings and not page_visuals:
                r0 = min(d["rect"].x0 for d in sig_drawings)
                y0 = min(d["rect"].y0 for d in sig_drawings)
                r1 = max(d["rect"].x1 for d in sig_drawings)
                y1 = max(d["rect"].y1 for d in sig_drawings)
                page_visuals.append({
                    "page": page_num,
                    "bbox": [round(r0, 1), round(y0, 1), round(r1, 1), round(y1, 1)],
                    "type": "vector"
                })

            if not page_visuals:
                continue

            page_qs = [qn for qn, qdata in questions_raw.items() if page_num in qdata["pages"]]
            if len(page_qs) == 1:
                target_q = page_qs[0]
                for vis in page_visuals:
                    questions_raw[target_q]["visuals"].append(vis)
            elif len(page_qs) > 1:
                for vis in page_visuals:
                    v_box = vis["bbox"]
                    v_center = ((v_box[0] + v_box[2]) / 2, (v_box[1] + v_box[3]) / 2)
                    best_q = None
                    min_dist = float("inf")
                    for qn in page_qs:
                        q_blocks = [b for p, b in questions_raw[qn]["blocks"] if p == page_num]
                        for b in q_blocks:
                            b_center = ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2)
                            dist = ((v_center[0] - b_center[0])**2 + (v_center[1] - b_center[1])**2)**0.5
                            if dist < min_dist:
                                min_dist = dist
                                best_q = qn
                    if best_q is not None:
                        questions_raw[best_q]["visuals"].append(vis)

        # 3. Montagem da estrutura de questões
        output_questions = []
        crop_commands = []
        images_cropped_count = 0

        sorted_q_nums = sorted(questions_raw.keys())
        for q_num in sorted_q_nums:
            if q_start is not None and q_num < q_start:
                continue
            if q_end is not None and q_num > q_end:
                continue

            qdata = questions_raw[q_num]
            full_text = "".join([b[4] + "\n" for p, b in qdata["blocks"]])

            # Remove o cabeçalho
            clean_raw = re.sub(r"^\s*(?:QUEST[ÃA]O|Quest[ãa]o|QuesT[ãa]o)?\s*\d+[\.\s\-]*", "", full_text, flags=re.IGNORECASE)
            q_enunciado, options = cls.split_enunciado_and_options(clean_raw)
            q_enunciado = TextSanitizer.sanitize_all(q_enunciado)
            options = [TextSanitizer.sanitize_all(opt) for opt in options]

            # Gabarito
            ans_letter = gabarito.get(q_num)
            correct_idx = 0
            explanation_note = ""
            if ans_letter:
                if ans_letter in ["A", "B", "C", "D", "E"]:
                    correct_idx = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4}[ans_letter]
                elif "ANUL" in ans_letter:
                    correct_idx = 0
                    explanation_note = " (Questão anulada no gabarito oficial)."

            # Imagens
            has_visuals = len(qdata["visuals"]) > 0
            image_obj = None

            if has_visuals:
                main_vis = qdata["visuals"][0]
                vis_page = main_vis["page"]
                vis_box = main_vis["bbox"]
                inst_dir = exam_id.split("-")[0].lower() if "-" in exam_id else "geral"
                img_rel_path = f"assets/img/questoes/{inst_dir}/{exam_id}-q{q_num:02d}.png"
                img_abs_path = os.path.join(ROOT_DIR, img_rel_path)

                image_obj = {
                    "src": img_rel_path,
                    "alt": f"[Acessibilidade Obrigatória] Descrição do conteúdo visual da figura da Questão {q_num:02d}",
                    "caption": f"Figura da Questão {q_num:02d}"
                }

                # Comando sugerido de recorte
                crop_cmd = f"python3 scripts/manage_mathdata.py crop-image -p {pdf_path} --page {vis_page} --rect {vis_box[0]} {vis_box[1]} {vis_box[2]} {vis_box[3]} -o {img_rel_path}"
                crop_commands.append((q_num, crop_cmd, vis_page, vis_box))

                if auto_crop:
                    try:
                        ImageExtractor.crop_region(
                            pdf_path=pdf_path,
                            page_num=vis_page,
                            rect_coords=tuple(vis_box),
                            output_path=img_abs_path,
                            dpi=dpi,
                            pad=pad,
                            optimize=True
                        )
                        images_cropped_count += 1

                        if upload_drive:
                            try:
                                print(f"   ☁️ Enviando figura da Questão {q_num:02d} para o Google Drive...")
                                drive_res = GoogleDriveManager.upload_image(img_abs_path, parent_folder_id=folder_id)
                                image_obj["src"] = drive_res["url"]
                                print(f"      Link gerado: {drive_res['url']}")
                            except Exception as de:
                                print(f"   ⚠️ Falha no upload para o Google Drive da Questão {q_num:02d} (mantendo local): {de}")

                    except Exception as e:
                        print(f"⚠️ Falha no auto-crop da Questão {q_num}: {e}")

            question_entry = {
                "q": f"({exam_title} - Q{q_num:02d}) {q_enunciado}",
                "image": image_obj,
                "options": options,
                "correct": correct_idx,
                "explanation": f"Resolução comentada da Questão {q_num:02d} passo a passo.{explanation_note}",
                "bncc": "EF09MA01",
                "bnccDesc": "Habilidade da BNCC associada à questão.",
                "unidadeTematica": "Números",
                "anoEscolar": "9º ano",
                "topicoId": exam_id
            }
            output_questions.append(question_entry)

        topic_dict = {
            "id": exam_id,
            "title": exam_title,
            "overview": f"Caderno de questões de Matemática do {exam_title}.",
            "questions": output_questions
        }

        stats = {
            "exam_id": exam_id,
            "exam_title": exam_title,
            "total_questions": len(output_questions),
            "questions_with_images": len(crop_commands),
            "images_cropped": images_cropped_count,
            "gabarito_answers": len([q for q in output_questions if gabarito.get(int(re.search(r"Q(\d+)", q['q']).group(1)))]),
            "crop_commands": crop_commands
        }

        return topic_dict, stats


# ==============================================================================
# 6. GESTOR PRINCIPAL DE DADOS (MathDataManager)
# ==============================================================================
class MathDataManager:
    def __init__(self, data_path: str = MATH_DATA_PATH):
        self.data_path = data_path
        self.data = self._load()

    def _load(self) -> dict:
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Arquivo de dados {self.data_path} não encontrado.")
        with open(self.data_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def backup(self) -> str:
        """Cria um backup timestamped e um .bak fixo de segurança."""
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        bak_file = f"{self.data_path}.bak"
        history_bak = f"{self.data_path}.{ts}.bak"
        shutil.copy2(self.data_path, bak_file)
        shutil.copy2(self.data_path, history_bak)
        return history_bak

    def save(self, create_backup: bool = True):
        """Salva mathData.json com formatação canônica e validação atômica."""
        if create_backup:
            self.backup()

        temp_path = f"{self.data_path}.tmp"
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

        os.replace(temp_path, self.data_path)

    def validate(self, target_data: dict = None, use_katex_engine: bool = True) -> list:
        """Realiza validação completa de schema, KaTeX léxico e KaTeX motor Node.js."""
        dataset = target_data if target_data is not None else self.data
        all_issues = []
        math_items = []

        def inspect_q(q, loc):
            all_issues.extend(SchemaValidator.validate_question(q, loc))
            all_issues.extend(KaTeXValidator.validate_text(q.get("q", ""), f"{loc} (q)"))
            all_issues.extend(KaTeXValidator.validate_text(q.get("explanation", ""), f"{loc} (exp)"))
            math_items.extend(KaTeXValidator.extract_math_blocks(q.get("q", ""), f"{loc} (q)"))
            math_items.extend(KaTeXValidator.extract_math_blocks(q.get("explanation", ""), f"{loc} (exp)"))
            for o_idx, opt in enumerate(q.get("options", [])):
                all_issues.extend(KaTeXValidator.validate_text(opt, f"{loc} (opt {o_idx})"))
                math_items.extend(KaTeXValidator.extract_math_blocks(opt, f"{loc} (opt {o_idx})"))

        if isinstance(dataset, dict):
            for block_id, block in dataset.items():
                topics = block.get("topics", [])
                for topic in topics:
                    t_id = topic.get("id", "sem-id")
                    for idx, q in enumerate(topic.get("questions", [])):
                        loc = f"Bloco {block_id} -> {t_id} -> Q{idx+1}"
                        inspect_q(q, loc)

        elif isinstance(dataset, list):
            for topic in dataset:
                t_id = topic.get("id", "sem-id")
                for idx, q in enumerate(topic.get("questions", [])):
                    loc = f"{t_id} -> Q{idx+1}"
                    inspect_q(q, loc)

        # Validação KaTeX com motor Node.js
        if use_katex_engine and math_items:
            engine_issues = KaTeXValidator.validate_with_katex_engine(math_items)
            all_issues.extend(engine_issues)

        return all_issues

    def sanitize_inplace(self, target_data: dict = None) -> int:
        """Aplica sanitização de texto (vírgulas e moedas) em todo o banco ou em um conjunto de dados."""
        dataset = target_data if target_data is not None else self.data
        count = 0

        def sanitize_question(q):
            nonlocal count
            fields = ["q", "explanation"]
            for f in fields:
                if f in q and isinstance(q[f], str):
                    orig = q[f]
                    clean = TextSanitizer.sanitize_all(orig)
                    if clean != orig:
                        q[f] = clean
                        count += 1
            if "options" in q and isinstance(q["options"], list):
                for i in range(len(q["options"])):
                    orig = q["options"][i]
                    if isinstance(orig, str):
                        clean = TextSanitizer.sanitize_all(orig)
                        if clean != orig:
                            q["options"][i] = clean
                            count += 1

        if isinstance(dataset, dict):
            for b in dataset.values():
                for t in b.get("topics", []):
                    for q in t.get("questions", []):
                        sanitize_question(q)
        elif isinstance(dataset, list):
            for t in dataset:
                for q in t.get("questions", []):
                    sanitize_question(q)

        return count

    def import_topics(self, input_path: str, block_id: str, sanitize: bool = True, dry_run: bool = False) -> tuple:
        """
        Importa tópicos a partir de um arquivo JSON estruturado para o bloco desejado.
        Suporta:
          - Um único tópico como objeto dict
          - Uma lista de tópicos
          - Um objeto com chave 'topics'
        """
        with open(input_path, "r", encoding="utf-8") as f:
            raw_input = json.load(f)

        if isinstance(raw_input, dict):
            if "topics" in raw_input and isinstance(raw_input["topics"], list):
                incoming_topics = raw_input["topics"]
            elif "questions" in raw_input:
                incoming_topics = [raw_input]
            elif block_id in raw_input and "topics" in raw_input[block_id]:
                incoming_topics = raw_input[block_id]["topics"]
            else:
                raise ValueError("Estrutura do JSON de entrada não reconhecida (deve ser um tópico ou lista de tópicos).")
        elif isinstance(raw_input, list):
            incoming_topics = raw_input
        else:
            raise ValueError("O arquivo de entrada deve conter um objeto ou uma lista.")

        if sanitize:
            print(f"🧹 Aplicando sanitização automática de KaTeX, moedas e vírgulas decimais...")
            self.sanitize_inplace(incoming_topics)

        # Validação prévia
        print(f"🔍 Validando {len(incoming_topics)} tópicos candidatos antes da inserção...")
        issues = self.validate(incoming_topics)
        critical_issues = [i for i in issues if i["type"] in ("UNBALANCED_BRACES", "KATEX_UNSUPPORTED_ARRAY_ALIGN", "INVALID_OPTIONS", "INVALID_CORRECT_INDEX", "MISSING_FIELD")]

        if critical_issues:
            print(f"❌ {len(critical_issues)} erros críticos encontrados no arquivo de entrada:")
            for ci in critical_issues[:10]:
                print(f"   • [{ci['type']}] {ci['location']}: {ci['message']}")
            raise ValueError("Importação cancelada devido a erros críticos no JSON de entrada. Corrija-os antes de prosseguir.")

        if issues:
            print(f"⚠️ {len(issues)} avisos não-críticos detectados:")
            for w in issues[:5]:
                print(f"   • [{w['type']}] {w['location']}: {w['message']}")

        # Merge no mathData.json
        if block_id not in self.data:
            print(f"➕ Criando novo Bloco '{block_id}' no mathData.json...")
            self.data[block_id] = {
                "id": block_id,
                "title": f"Bloco {block_id}",
                "topics": []
            }

        existing_topics = self.data[block_id].get("topics", [])
        existing_indices = {t["id"]: i for i, t in enumerate(existing_topics) if "id" in t}

        inserted_count = 0
        updated_count = 0

        for new_topic in incoming_topics:
            tid = new_topic.get("id")
            if not tid:
                raise ValueError("Tópico de entrada não possui campo obrigatório 'id'.")

            # Injeta referências de infraestrutura
            new_topic["blockId"] = block_id
            if "folder" not in new_topic:
                # Dedução automática de pasta padrão
                folder_map = {
                    "5": "bloco-5-provas-ifsc",
                    "6": "bloco-6-provas-ifce",
                    "7": "bloco-7-provas-ifsp",
                    "8": "bloco-8-provas-ifmg"
                }
                new_topic["folder"] = folder_map.get(block_id, f"bloco-{block_id}")

            if tid in existing_indices:
                idx = existing_indices[tid]
                existing_topics[idx] = new_topic
                updated_count += 1
            else:
                existing_topics.append(new_topic)
                inserted_count += 1

        self.data[block_id]["topics"] = existing_topics

        if not dry_run:
            self.save(create_backup=True)
            print(f"✅ Ingestão concluída com sucesso no mathData.json:")
            print(f"   • {updated_count} tópicos atualizados")
            print(f"   • {inserted_count} novos tópicos inseridos")
        else:
            print(f"🔎 [DRY-RUN] Nenhuma alteração gravada em disco ({updated_count} updates, {inserted_count} inserts previstos).")

        return updated_count, inserted_count


# ==============================================================================
# 7. GERENCIADOR DO GOOGLE DRIVE (GoogleDriveManager)
# ==============================================================================
class GoogleDriveManager:
    SCOPES = ["https://www.googleapis.com/auth/drive.file"]
    CACHE_FILE = os.path.join(ROOT_DIR, "assets", "img", "drive_sync_cache.json")
    TOKEN_FILE = os.path.join(ROOT_DIR, "token.json")
    CLIENT_SECRET_FILE = os.path.join(ROOT_DIR, "client_secret.json")

    @staticmethod
    def load_env(env_path=None):
        """Carrega variáveis do arquivo .env sem exigir pacotes externos."""
        path = env_path or os.path.join(ROOT_DIR, ".env")
        if not os.path.exists(path):
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    if k and k not in os.environ:
                        os.environ[k] = v
        except Exception:
            pass

    @classmethod
    def resolve_credentials_path(cls, creds_path=None):
        """Localiza o arquivo de credenciais da Service Account ou OAuth."""
        cls.load_env()
        if creds_path and os.path.exists(creds_path):
            return os.path.abspath(creds_path)

        env_cred = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        if env_cred and os.path.exists(env_cred):
            return os.path.abspath(env_cred)

        for candidate in ["client_secret.json", "service_account.json", "credentials.json", "service-account.json"]:
            cand_path = os.path.join(ROOT_DIR, candidate)
            if os.path.exists(cand_path):
                return cand_path

        return None

    @classmethod
    def resolve_folder_id(cls, folder_id=None):
        """Obtém o ID da pasta do Google Drive."""
        cls.load_env()
        if folder_id:
            return folder_id.strip()
        env_f = os.environ.get("GOOGLE_DRIVE_FOLDER_ID")
        return env_f.strip() if env_f else None

    @classmethod
    def get_service(cls, creds_path=None):
        """
        Inicializa e retorna o cliente Google Drive API v3.
        Suporta automaticamente tanto OAuth 2.0 (token.json / client_secret.json)
        quanto Service Account (service_account.json).
        """
        try:
            from googleapiclient.discovery import build
        except ImportError:
            raise ImportError(
                "Bibliotecas da Google API não estão instaladas.\n"
                "Execute: pip install google-api-python-client google-auth google-auth-httplib2 google-auth-oauthlib"
            )

        # 1. Tenta carregar token OAuth já autenticado
        if os.path.exists(cls.TOKEN_FILE):
            try:
                from google.oauth2.credentials import Credentials
                from google.auth.transport.requests import Request

                creds = Credentials.from_authorized_user_file(cls.TOKEN_FILE, cls.SCOPES)
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                    with open(cls.TOKEN_FILE, "w", encoding="utf-8") as f:
                        f.write(creds.to_json())
                if creds and creds.valid:
                    service = build("drive", "v3", credentials=creds, cache_discovery=False)
                    return service, "OAuth 2.0 (token.json)"
            except Exception as e:
                print(f"⚠️ Token existente inválido ou expirado ({e}), tentando novo fluxo...")

        # 2. Se client_secret.json existir, executa o fluxo OAuth 2.0
        client_secret = cls.CLIENT_SECRET_FILE if os.path.exists(cls.CLIENT_SECRET_FILE) else None
        if client_secret:
            try:
                from google_auth_oauthlib.flow import InstalledAppFlow

                flow = InstalledAppFlow.from_client_secrets_file(client_secret, cls.SCOPES)
                auth_url, _ = flow.authorization_url(prompt="consent")
                print("\n" + "=" * 70)
                print("🔑 AUTORIZAÇÃO GOOGLE OAUTH 2.0 (ESCOPO SEGURO drive.file)")
                print("=" * 70)
                print("Acesse o link abaixo no seu navegador para autorizar:")
                print(f"\n👉 {auth_url}\n")
                print("=" * 70)
                print("Aguardando autorização via localhost:8080...")
                creds = flow.run_local_server(port=8080, prompt="consent", open_browser=True)
                with open(cls.TOKEN_FILE, "w", encoding="utf-8") as f:
                    f.write(creds.to_json())
                print(f"💾 Token de autorização salvo em: {cls.TOKEN_FILE}")
                service = build("drive", "v3", credentials=creds, cache_discovery=False)
                return service, "OAuth 2.0 (client_secret.json)"
            except Exception as e:
                print(f"⚠️ Falha no fluxo OAuth 2.0: {e}")
                if "redirect_uri" in str(e).lower():
                    print("💡 Dica: Se o cliente foi criado como 'Aplicativo da Web', adicione 'http://localhost:8080/' nos URIs de redirecionamento autorizados no Google Cloud Console (ou crie um cliente do tipo 'Aplicativo para computador').")

        # 3. Fallback para Service Account
        resolved_creds = cls.resolve_credentials_path(creds_path)
        if not resolved_creds:
            raise FileNotFoundError(
                "Nenhuma credencial configurada!\n"
                "Para configurar:\n"
                "  • OAuth 2.0 (Gmail pessoal): salve 'client_secret.json' na raiz do projeto.\n"
                "  • Service Account (Shared Drives): salve 'service_account.json' na raiz do projeto."
            )

        try:
            from google.oauth2 import service_account

            credentials = service_account.Credentials.from_service_account_file(
                resolved_creds, scopes=cls.SCOPES
            )
            service = build("drive", "v3", credentials=credentials, cache_discovery=False)
            return service, resolved_creds
        except Exception as e:
            raise RuntimeError(f"Falha ao autenticar com as credenciais '{resolved_creds}': {e}")

    @classmethod
    def test_connection(cls, creds_path=None, folder_id=None):
        """Testa conectividade, autenticação e permissão de acesso à pasta."""
        print("🔌 Testando autenticação com a Google Drive API...")
        try:
            service, resolved_creds = cls.get_service(creds_path)
        except Exception as e:
            print(f"❌ {e}")
            return False

        print(f"✅ Credenciais carregadas com sucesso de: {resolved_creds}")

        client_email = None
        if os.path.exists(str(resolved_creds)):
            try:
                with open(resolved_creds, "r", encoding="utf-8") as f:
                    sa_data = json.load(f)
                    client_email = sa_data.get("client_email")
                    project_id = sa_data.get("project_id")
                if client_email:
                    print(f"👤 Service Account: {client_email}")
                if project_id:
                    print(f"📦 Projeto Google Cloud: {project_id}")
            except Exception:
                pass

        try:
            about = service.about().get(fields="user, storageQuota").execute()
            user_info = about.get("user", {})
            user_display = user_info.get("displayName") or "Autenticado"
            user_email = user_info.get("emailAddress", "")
            print(f"🌐 Conexão com Google Drive API estabelecida:")
            print(f"   • Conta: {user_display} ({user_email})")
            quota = about.get("storageQuota", {})
            if quota and quota.get("limit"):
                limit_gb = round(int(quota.get("limit", 0)) / (1024**3), 1)
                usage_gb = round(int(quota.get("usage", 0)) / (1024**3), 2)
                print(f"   • Armazenamento no Drive: {usage_gb} GB usados de {limit_gb} GB")
        except Exception as e:
            print(f"❌ Falha ao consultar endpoint about(): {e}")
            return False

        target_folder = cls.resolve_folder_id(folder_id)
        if not target_folder:
            print("\n⚠️ Nenhuma pasta raiz configurada (GOOGLE_DRIVE_FOLDER_ID não definido).")
            print("💡 Para que a Service Account salve imagens na sua conta pessoal do Drive:")
            print(f"   1. Crie uma pasta no seu Google Drive (ex: 'PartiuIF_Imagens').")
            if client_email:
                print(f"   2. Compartilhe a pasta com o e-mail: {client_email} (Permissão: Editor).")
            print(f"   3. Defina GOOGLE_DRIVE_FOLDER_ID no arquivo .env ou passe via --folder-id.")
            return True

        print(f"\n📁 Verificando acesso à pasta remota (ID: {target_folder})...")
        try:
            folder_info = service.files().get(fileId=target_folder, fields="id, name, mimeType, capabilities, trashed").execute()
            if folder_info.get("trashed"):
                print(f"❌ A pasta {target_folder} está na lixeira!")
                return False
            if folder_info.get("mimeType") != "application/vnd.google-apps.folder":
                print(f"❌ O ID especificado ({target_folder}) não é uma pasta (Mime: {folder_info.get('mimeType')}).")
                return False

            caps = folder_info.get("capabilities", {})
            can_add = caps.get("canAddChildren", False)
            folder_name = folder_info.get("name", "Sem Nome")

            if can_add:
                print(f"🎉 Acesso concedido com permissão de escrita!")
                print(f"   • Nome da pasta: {folder_name}")
                print(f"   • ID da pasta: {target_folder}")
                return True
            else:
                print(f"⚠️ A Service Account tem acesso à pasta '{folder_name}', mas NÃO possui permissão de escrita (canAddChildren=False).")
                if client_email:
                    print(f"   Certifique-se de compartilhar a pasta com {client_email} como 'Editor' (não apenas Leitor).")
                return False
        except Exception as e:
            print(f"❌ Erro ao acessar pasta {target_folder}: {e}")
            if client_email:
                print(f"💡 Dica: Compartilhe a pasta com a Service Account ({client_email}) como 'Editor'.")
            return False

    @classmethod
    def get_or_create_subfolder(cls, service, parent_id, folder_name):
        """Busca ou cria uma subpasta (ex: ifce, ifmg) dentro de parent_id."""
        query = f"'{parent_id}' in parents and name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
        res = service.files().list(q=query, spaces="drive", fields="files(id, name)").execute()
        files = res.get("files", [])
        if files:
            return files[0]["id"]

        folder_metadata = {
            "name": folder_name,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [parent_id]
        }
        folder = service.files().create(body=folder_metadata, fields="id").execute()
        return folder["id"]

    @classmethod
    def load_cache(cls):
        if os.path.exists(cls.CACHE_FILE):
            try:
                with open(cls.CACHE_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    @classmethod
    def save_cache(cls, cache):
        os.makedirs(os.path.dirname(cls.CACHE_FILE), exist_ok=True)
        with open(cls.CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, indent=2, ensure_ascii=False)

    @classmethod
    def upload_image(cls, local_path, parent_folder_id=None, creds_path=None, make_public=True):
        """
        Envia uma imagem para o Google Drive na subpasta correspondente,
        aplica permissão pública de leitura e retorna {'id', 'url', 'name', 'subfolder'}.
        """
        from googleapiclient.http import MediaFileUpload

        service, _ = cls.get_service(creds_path)
        folder_id = cls.resolve_folder_id(parent_folder_id)
        if not folder_id:
            raise ValueError("ID da pasta raiz do Google Drive não configurado (use GOOGLE_DRIVE_FOLDER_ID ou --folder-id).")

        abs_path = os.path.abspath(local_path)
        if not os.path.exists(abs_path):
            raise FileNotFoundError(f"Imagem local não encontrada: {local_path}")

        filename = os.path.basename(abs_path)
        inst_dir = filename.split("-")[0].lower() if "-" in filename else "geral"

        # Garante subpasta por IF
        target_folder_id = cls.get_or_create_subfolder(service, folder_id, inst_dir)

        # Checa se o arquivo já existe na pasta de destino para evitar duplicatas
        query = f"'{target_folder_id}' in parents and name = '{filename}' and trashed = false"
        res = service.files().list(q=query, spaces="drive", fields="files(id, name)").execute()
        existing = res.get("files", [])

        ext = os.path.splitext(filename)[1].lower()
        mimetype = "image/jpeg" if ext in [".jpg", ".jpeg"] else "image/png"

        if existing:
            file_id = existing[0]["id"]
            media = MediaFileUpload(abs_path, mimetype=mimetype, resumable=True)
            service.files().update(fileId=file_id, media_body=media).execute()
        else:
            file_metadata = {
                "name": filename,
                "parents": [target_folder_id]
            }
            media = MediaFileUpload(abs_path, mimetype=mimetype, resumable=True)
            new_file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
            file_id = new_file.get("id")

        if make_public:
            try:
                service.permissions().create(
                    fileId=file_id,
                    body={"role": "reader", "type": "anyone"}
                ).execute()
            except Exception:
                pass

        public_url = f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"
        return {
            "id": file_id,
            "url": public_url,
            "name": filename,
            "subfolder": inst_dir
        }

    @classmethod
    def sync_local_images(cls, base_dir="assets/img/questoes", folder_id=None, creds_path=None, dry_run=False, update_mathdata=False, build_site=False):
        """
        Varre todos os diretórios locais de imagens por IF, envia as pendentes para o Drive,
        mantém um cache local de IDs já sincronizados e opcionalmente atualiza mathData.json.
        """
        folder_id = cls.resolve_folder_id(folder_id)
        if not dry_run and not folder_id:
            raise ValueError("ID da pasta raiz do Google Drive não configurado (use GOOGLE_DRIVE_FOLDER_ID ou --folder-id).")

        abs_base = os.path.join(ROOT_DIR, base_dir) if not os.path.isabs(base_dir) else base_dir
        if not os.path.exists(abs_base):
            raise FileNotFoundError(f"Diretório de imagens não encontrado: {abs_base}")

        # Localiza todas as imagens
        files_to_sync = []
        for root, _, files in os.walk(abs_base):
            for f in sorted(files):
                if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".svg")):
                    full_path = os.path.join(root, f)
                    rel_to_root = os.path.relpath(full_path, ROOT_DIR)
                    parts = rel_to_root.split(os.sep)
                    inst = parts[-2] if len(parts) >= 2 and parts[-2] != "questoes" else "geral"
                    files_to_sync.append((full_path, rel_to_root, f, inst))

        print(f"📸 Total de imagens encontradas no acervo local: {len(files_to_sync)}")

        cache = cls.load_cache()
        pending = [item for item in files_to_sync if item[1] not in cache]
        already_synced = len(files_to_sync) - len(pending)

        print(f"   • Já sincronizadas no cache: {already_synced}")
        print(f"   • Pendentes de envio: {len(pending)}")

        if dry_run:
            print("\n🔎 [DRY-RUN] Simulação de sincronização com o Google Drive:")
            by_inst = {}
            for _, rel_path, fname, inst in files_to_sync:
                by_inst.setdefault(inst, []).append((fname, rel_path in cache))

            for inst, items in sorted(by_inst.items()):
                print(f"\n📂 Subpasta remota sugerida: [{inst}/] ({len(items)} imagens)")
                for fname, in_cache in items[:5]:
                    status = "✅ Já no cache" if in_cache else "📤 Pendente"
                    print(f"   • {status}: {fname}")
                if len(items) > 5:
                    print(f"   ... e mais {len(items) - 5} arquivos.")
            print("\n💡 Para executar o upload real, remova a flag --dry-run.")
            return

        service, _ = cls.get_service(creds_path)
        synced_count = 0
        path_to_url_map = {}

        for rel_p, info in cache.items():
            path_to_url_map[rel_p] = info["url"]

        for i, (full_p, rel_p, fname, inst) in enumerate(pending, 1):
            print(f"[{i}/{len(pending)}] Enviando {fname} para subpasta [{inst}/]...")
            target_folder_id = cls.get_or_create_subfolder(service, folder_id, inst)
            res = cls.upload_image(full_p, parent_folder_id=target_folder_id, creds_path=creds_path, make_public=True)
            cache[rel_p] = {
                "id": res["id"],
                "url": res["url"],
                "synced_at": datetime.now().isoformat()
            }
            path_to_url_map[rel_p] = res["url"]
            synced_count += 1
            cls.save_cache(cache)

        print(f"\n🎉 Sincronização de imagens concluída com sucesso! ({synced_count} novos uploads)")

        if update_mathdata:
            print("\n📝 Atualizando referências em mathData.json com os links do Google Drive...")
            manager = MathDataManager()
            data = manager.data
            updated_questions = 0

            for block_id, block in data.items():
                if isinstance(block, dict):
                    for topic in block.get("topics", []):
                        for q in topic.get("questions", []):
                            img = q.get("image")
                            if img and isinstance(img, dict) and "src" in img:
                                src = img["src"]
                                if src in path_to_url_map:
                                    img["src"] = path_to_url_map[src]
                                    updated_questions += 1

            if updated_questions > 0:
                manager.save(create_backup=True)
                print(f"💾 mathData.json atualizado: {updated_questions} questões agora apontam para links do Drive.")
                if build_site:
                    print("\n🚀 Recompilando o site estático...")
                    subprocess.run([sys.executable, "build_full_site.py"], cwd=ROOT_DIR)
            else:
                print("Nenhuma referência precisava ser atualizada em mathData.json.")


# ==============================================================================
# 8. CLI E COMANDOS
# ==============================================================================
def main():
    parser = argparse.ArgumentParser(description="Gestão, Validação e Ingestão do mathData.json (PartiuIF)")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcomando: import
    import_parser = subparsers.add_parser("import", help="Importa uma prova ou lista de tópicos a partir de um JSON")
    import_parser.add_argument("-f", "--file", required=True, help="Caminho do arquivo JSON a ser importado")
    import_parser.add_argument("-b", "--block", required=True, help="ID do Bloco de destino (ex: 8 para IFMG)")
    import_parser.add_argument("--no-sanitize", action="store_true", help="Desativa sanitização automática de vírgulas e moedas")
    import_parser.add_argument("--dry-run", action="store_true", help="Simula a operação sem gravar em disco")
    import_parser.add_argument("--build", action="store_true", help="Executa automaticamente python3 build_full_site.py após a importação")

    # Subcomando: validate
    val_parser = subparsers.add_parser("validate", help="Valida schema, KaTeX e imagens de mathData.json")
    val_parser.add_argument("-f", "--file", help="Arquivo JSON específico a validar (padrão: mathData.json)")
    val_parser.add_argument("--no-engine", action="store_true", help="Desativa validação profunda via motor KaTeX Node.js")

    # Subcomando: sanitize
    san_parser = subparsers.add_parser("sanitize", help="Higieniza vírgulas decimais e escape de moedas no mathData.json")
    san_parser.add_argument("--apply", action="store_true", help="Grava as alterações sanitizadas em disco (com backup)")
    san_parser.add_argument("--build", action="store_true", help="Recompila o site após sanitizar")

    # Subcomando: template
    tpl_parser = subparsers.add_parser("template", help="Gera um modelo de prova JSON para preenchimento")
    tpl_parser.add_argument("-o", "--output", required=True, help="Caminho de saída para o template JSON")
    tpl_parser.add_argument("-q", "--num-questions", type=int, default=10, help="Quantidade de questões modelo")
    tpl_parser.add_argument("--id", default="exame-ano-semestre", help="ID do tópico modelo")
    tpl_parser.add_argument("--title", default="Prova IFXX 2025.1", help="Título do exame modelo")

    # Subcomando: crop-image
    crop_parser = subparsers.add_parser("crop-image", help="Recorta e otimiza uma figura do PDF com alta resolução")
    crop_parser.add_argument("-p", "--pdf", required=True, help="Caminho do caderno oficial em PDF")
    crop_parser.add_argument("--page", type=int, required=True, help="Número da página no PDF (1-indexed)")
    crop_parser.add_argument("--rect", nargs=4, type=float, required=True, metavar=("X0", "Y0", "X1", "Y1"), help="Coordenadas (x0 y0 x1 y1) do PDF em pontos")
    crop_parser.add_argument("-o", "--output", required=True, help="Caminho do arquivo PNG de saída")
    crop_parser.add_argument("--dpi", type=int, default=200, help="Resolução de renderização em DPI (padrão: 200)")
    crop_parser.add_argument("--pad", type=int, default=8, help="Margem de espaçamento branco em pixels após o corte (padrão: 8)")
    crop_parser.add_argument("--no-optimize", action="store_true", help="Desativa a otimização com optipng/pngquant")
    crop_parser.add_argument("--upload-drive", action="store_true", help="Envia automaticamente a imagem recortada para o Google Drive")
    crop_parser.add_argument("--folder-id", help="ID da pasta remota no Google Drive para o upload")

    # Subcomando: parse-pdf
    pdf_parser_cmd = subparsers.add_parser("parse-pdf", help="Extrai e estrutura questões a partir de um PDF de prova oficial")
    pdf_parser_cmd.add_argument("-p", "--pdf", required=True, help="Caminho do caderno oficial em PDF")
    pdf_parser_cmd.add_argument("-o", "--output", help="Caminho do arquivo JSON de saída (padrão: <exam_id>.json)")
    pdf_parser_cmd.add_argument("--q-start", type=int, help="Número inicial da questão (ex: 16)")
    pdf_parser_cmd.add_argument("--q-end", type=int, help="Número final da questão (ex: 30)")
    pdf_parser_cmd.add_argument("--pages", help="Intervalo ou lista de páginas a processar (ex: '13-21' ou '13,14,15')")
    pdf_parser_cmd.add_argument("--exam-id", help="ID personalizado para a prova (ex: 'ifmg-2025-1')")
    pdf_parser_cmd.add_argument("--exam-title", help="Título da prova (ex: 'IFMG 2025.1')")
    pdf_parser_cmd.add_argument("--gabarito", help="Caminho do gabarito em PDF/TXT ou string de respostas (ex: '16:C,17:C')")
    pdf_parser_cmd.add_argument("--header-regex", help="Regex customizada para cabeçalho de questão")
    pdf_parser_cmd.add_argument("--auto-crop", action="store_true", help="Recorta e salva automaticamente as figuras detectadas")
    pdf_parser_cmd.add_argument("--upload-drive", action="store_true", help="Envia figuras recortadas automaticamente para o Google Drive")
    pdf_parser_cmd.add_argument("--folder-id", help="ID da pasta remota no Google Drive")
    pdf_parser_cmd.add_argument("--dpi", type=int, default=200, help="DPI para corte de imagens (padrão: 200)")
    pdf_parser_cmd.add_argument("--pad", type=int, default=8, help="Padding em pixels para corte de imagens (padrão: 8)")
    pdf_parser_cmd.add_argument("-b", "--import-to-block", help="Importa o JSON gerado diretamente para o Bloco especificado do mathData.json")
    pdf_parser_cmd.add_argument("--build", action="store_true", help="Executa build_full_site.py após importar para o bloco")

    # Subcomando: drive-test
    dtest_parser = subparsers.add_parser("drive-test", help="Testa conexão e permissões da Google Drive API via Service Account")
    dtest_parser.add_argument("-c", "--credentials", help="Caminho da chave JSON da Service Account")
    dtest_parser.add_argument("--folder-id", help="ID da pasta remota no Google Drive para testar permissão de escrita")

    # Subcomando: drive-upload
    dupload_parser = subparsers.add_parser("drive-upload", help="Envia uma imagem local para o Google Drive e gera link público")
    dupload_parser.add_argument("-f", "--file", required=True, help="Caminho da imagem local a ser enviada")
    dupload_parser.add_argument("--folder-id", help="ID da pasta raiz no Google Drive (padrão: GOOGLE_DRIVE_FOLDER_ID do .env)")
    dupload_parser.add_argument("-c", "--credentials", help="Caminho da chave JSON da Service Account")
    dupload_parser.add_argument("--no-public", action="store_true", help="Não aplica permissão pública de leitura")

    # Subcomando: drive-sync
    dsync_parser = subparsers.add_parser("drive-sync", help="Sincroniza em lote o acervo local de imagens com o Google Drive")
    dsync_parser.add_argument("--dir", default="assets/img/questoes", help="Diretório base de imagens (padrão: assets/img/questoes)")
    dsync_parser.add_argument("--folder-id", help="ID da pasta raiz no Google Drive (padrão: GOOGLE_DRIVE_FOLDER_ID do .env)")
    dsync_parser.add_argument("-c", "--credentials", help="Caminho da chave JSON da Service Account")
    dsync_parser.add_argument("--dry-run", action="store_true", help="Simula a sincronização sem fazer uploads reais")
    dsync_parser.add_argument("--update-mathdata", action="store_true", help="Atualiza mathData.json com os links do Drive")
    dsync_parser.add_argument("--build", action="store_true", help="Executa build_full_site.py após atualizar mathData.json")

    args = parser.parse_args()
    manager = MathDataManager()

    if args.command == "import":
        try:
            manager.import_topics(
                input_path=args.file,
                block_id=args.block,
                sanitize=not args.no_sanitize,
                dry_run=args.dry_run
            )
            if args.build and not args.dry_run:
                print("\n🚀 Executando build_full_site.py para sincronizar o site estático...")
                res = subprocess.run([sys.executable, "build_full_site.py"], cwd=ROOT_DIR)
                if res.returncode == 0:
                    print("🎉 Site estático sincronizado e compilado com sucesso!")
                else:
                    print(f"❌ Falha na compilação do site (código {res.returncode}).")
        except Exception as e:
            print(f"❌ Erro na importação: {e}")
            sys.exit(1)

    elif args.command == "validate":
        target = None
        if args.file:
            with open(args.file, "r", encoding="utf-8") as f:
                target = json.load(f)
            print(f"🔍 Validando arquivo customizado: {args.file}...")
        else:
            print(f"🔍 Validando mathData.json oficial...")

        issues = manager.validate(target, use_katex_engine=not args.no_engine)
        if not issues:
            print("✨ Nenhum problema encontrado! Todos os schemas e sintaxes KaTeX estão conformes.")
        else:
            print(f"\n⚠️ Total de ocorrências encontradas: {len(issues)}")
            by_type = {}
            for iss in issues:
                by_type.setdefault(iss["type"], []).append(iss)
            for itype, ilist in by_type.items():
                print(f"\n📌 Categoria [{itype}] ({len(ilist)} ocorrências):")
                for item in ilist[:5]:
                    print(f"   • {item['location']}: {item['message']}")
                    if "snippet" in item:
                        print(f"     Trecho: {repr(item['snippet'])}")
                if len(ilist) > 5:
                    print(f"     ... e mais {len(ilist) - 5} ocorrências.")

    elif args.command == "sanitize":
        print("🧹 Analisando mathData.json para sanitização de KaTeX, moedas e vírgulas...")
        changes = manager.sanitize_inplace()
        print(f"📝 Total de campos higienizados: {changes}")
        if args.apply:
            if changes > 0:
                manager.save(create_backup=True)
                print("💾 Alterações salvas com sucesso em mathData.json (backup criado).")
                if args.build:
                    print("\n🚀 Recompilando o site estático...")
                    subprocess.run([sys.executable, "build_full_site.py"], cwd=ROOT_DIR)
            else:
                print("Nenhuma alteração pendente para salvar.")
        else:
            print("💡 Use a flag --apply para gravar as alterações em disco.")

    elif args.command == "template":
        questions = []
        for i in range(1, args.num_questions + 1):
            questions.append({
                "q": f"(Exame - Q{i:02d}) Enunciado oficial completo da questão.",
                "image": None,
                "options": [
                    "Alternativa A",
                    "Alternativa B",
                    "Alternativa C",
                    "Alternativa D"
                ],
                "correct": 0,
                "explanation": "Resolução comentada passo a passo com KaTeX: $$x = 10$$.",
                "bncc": "EF09MA01",
                "bnccDesc": "Habilidade da BNCC associada à questão.",
                "unidadeTematica": "Números",
                "anoEscolar": "9º ano",
                "topicoId": "b1-t1"
            })

        topic_template = {
            "id": args.id,
            "title": args.title,
            "overview": f"Caderno de questões de Matemática do {args.title}.",
            "questions": questions
        }

        with open(args.output, "w", encoding="utf-8") as f:
            json.dump([topic_template], f, ensure_ascii=False, indent=2)

        print(f"✅ Template gerado com sucesso em: {args.output}")

    elif args.command == "crop-image":
        try:
            ImageExtractor.crop_region(
                pdf_path=args.pdf,
                page_num=args.page,
                rect_coords=tuple(args.rect),
                output_path=args.output,
                dpi=args.dpi,
                pad=args.pad,
                optimize=not args.no_optimize
            )
            if args.upload_drive:
                print(f"☁️ Enviando imagem recortada para o Google Drive...")
                res = GoogleDriveManager.upload_image(args.output, parent_folder_id=args.folder_id)
                print(f"🎉 Imagem hospedada no Google Drive com sucesso!")
                print(f"   • Link público: {res['url']}")
                print(f"   • ID do arquivo: {res['id']}")
        except Exception as e:
            print(f"❌ Erro no recorte da imagem: {e}")
            sys.exit(1)

    elif args.command == "parse-pdf":
        try:
            pages_list = None
            if args.pages:
                pages_list = []
                for part in args.pages.split(","):
                    part = part.strip()
                    if "-" in part:
                        p1, p2 = part.split("-")
                        pages_list.extend(range(int(p1), int(p2) + 1))
                    elif part.isdigit():
                        pages_list.append(int(part))

            topic_dict, stats = PDFParser.parse_pdf(
                pdf_path=args.pdf,
                q_start=args.q_start,
                q_end=args.q_end,
                pages=pages_list,
                exam_id=args.exam_id,
                exam_title=args.exam_title,
                gabarito_src=args.gabarito,
                header_regex=args.header_regex,
                auto_crop=args.auto_crop,
                upload_drive=args.upload_drive,
                folder_id=args.folder_id,
                dpi=args.dpi,
                pad=args.pad
            )

            # Define saída JSON
            output_file = args.output
            if not output_file:
                out_dir = os.path.dirname(os.path.abspath(args.pdf))
                output_file = os.path.join(out_dir, f"{topic_dict['id']}.json")

            os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump([topic_dict], f, ensure_ascii=False, indent=2)

            print(f"\n🎉 Extração concluída com sucesso!")
            print(f"📄 Arquivo JSON estruturado salvo em: {output_file}")
            print(f"   • Questões extraídas: {stats['total_questions']}")
            print(f"   • Respostas associadas pelo gabarito: {stats['gabarito_answers']}/{stats['total_questions']}")
            print(f"   • Questões com figuras detectadas: {stats['questions_with_images']}")
            if args.auto_crop:
                print(f"   • Imagens recortadas e salvas em disco: {stats['images_cropped']}")

            if stats["crop_commands"] and not args.auto_crop:
                print(f"\n🖼️ Comandos sugeridos para recorte de figuras ({len(stats['crop_commands'])} detectadas):")
                for q_num, cmd, p_num, rect in stats["crop_commands"]:
                    print(f"   • Q{q_num:02d} (pág {p_num}): {cmd}")
                print(f"\n💡 Dica: execute novamente com a flag --auto-crop para recortar e salvar todas as figuras automaticamente.")

            # Se solicitado import direto para um bloco
            if args.import_to_block:
                print(f"\n📥 Ingerindo diretamente no Bloco {args.import_to_block} do mathData.json...")
                manager.import_topics(input_path=output_file, block_id=args.import_to_block, sanitize=True)
                if args.build:
                    print("\n🚀 Executando build_full_site.py...")
                    res = subprocess.run([sys.executable, "build_full_site.py"], cwd=ROOT_DIR)
                    if res.returncode == 0:
                        print("🎉 Site estático sincronizado e compilado com sucesso!")
                    else:
                        print(f"❌ Falha na compilação do site (código {res.returncode}).")

        except Exception as e:
            print(f"❌ Erro na extração do PDF: {e}")
            sys.exit(1)

    elif args.command == "drive-test":
        success = GoogleDriveManager.test_connection(creds_path=args.credentials, folder_id=args.folder_id)
        if not success:
            sys.exit(1)

    elif args.command == "drive-upload":
        try:
            print(f"☁️ Enviando imagem {args.file} para o Google Drive...")
            res = GoogleDriveManager.upload_image(
                local_path=args.file,
                parent_folder_id=args.folder_id,
                creds_path=args.credentials,
                make_public=not args.no_public
            )
            print(f"🎉 Upload realizado com sucesso!")
            print(f"   • Nome: {res['name']}")
            print(f"   • Subpasta remota: [{res['subfolder']}/]")
            print(f"   • ID no Drive: {res['id']}")
            print(f"   • Link público: {res['url']}")
        except Exception as e:
            print(f"❌ Erro no upload: {e}")
            sys.exit(1)

    elif args.command == "drive-sync":
        try:
            GoogleDriveManager.sync_local_images(
                base_dir=args.dir,
                folder_id=args.folder_id,
                creds_path=args.credentials,
                dry_run=args.dry_run,
                update_mathdata=args.update_mathdata,
                build_site=args.build
            )
        except Exception as e:
            print(f"❌ Erro na sincronização: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
