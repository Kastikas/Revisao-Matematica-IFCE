import json
import os
import re
from datetime import datetime

# ==============================================================================
# 1. CARREGAMENTO E SINCRONIZAÇÃO DE DADOS (Single Source of Truth)
# ==============================================================================
with open("mathData_augmented.json", "r", encoding="utf-8") as f:
    math_data = json.load(f)

# Carregamento e mapeamento dos links do Google Drive para os PDFs oficiais
DRIVE_LINKS_FILE = "drive_links.json"
PENDING_LINKS_FILE = "provas_pendentes_drive.txt"
GOOGLE_DRIVE_PDFS = {}
if os.path.exists(DRIVE_LINKS_FILE):
    with open(DRIVE_LINKS_FILE, "r", encoding="utf-8") as f:
        GOOGLE_DRIVE_PDFS = json.load(f)

# Auto-importa links preenchidos pelo usuário em provas_pendentes_drive.txt
if os.path.exists(PENDING_LINKS_FILE):
    with open(PENDING_LINKS_FILE, "r", encoding="utf-8") as f:
        txt_content = f.read()
    matches = re.findall(r'Arquivo:\s*([A-Za-z0-9_.-]+\.pdf)[\r\n]+Link:\s*(https?://\S+)', txt_content)
    updated_from_txt = False
    for pdf_f, drive_url in matches:
        drive_url = drive_url.strip()
        if drive_url and (pdf_f not in GOOGLE_DRIVE_PDFS or GOOGLE_DRIVE_PDFS[pdf_f] != drive_url):
            GOOGLE_DRIVE_PDFS[pdf_f] = drive_url
            updated_from_txt = True
    if updated_from_txt:
        with open(DRIVE_LINKS_FILE, "w", encoding="utf-8") as f:
            json.dump(GOOGLE_DRIVE_PDFS, f, indent=2, ensure_ascii=False)
        print(f"📥 Novos links do Google Drive importados automaticamente de {PENDING_LINKS_FILE}!")

# Sincroniza em memória a propriedade driveUrl nos tópicos correspondentes
for b_id, block in math_data.items():
    for topic in block.get("topics", []):
        pdf_name = topic.get("pdf")
        if pdf_name and pdf_name in GOOGLE_DRIVE_PDFS:
            topic["driveUrl"] = GOOGLE_DRIVE_PDFS[pdf_name]

# Métricas Globais Calculadas Dinamicamente
total_subtopics = sum(len(b["topics"]) for b in math_data.values())
total_questions = sum(sum(len(t["questions"]) for t in b["topics"]) for b in math_data.values())

def is_exam_block(b_id, block):
    """Verifica se o bloco pertence ao acervo de provas oficiais."""
    title = block.get("title", "").lower()
    return str(b_id) in ["5", "6", "7"] or "provas" in title or "oficiais" in title

theory_blocks_data = {k: v for k, v in math_data.items() if not is_exam_block(k, v)}
exam_blocks_data = {k: v for k, v in math_data.items() if is_exam_block(k, v)}

total_theory_subtopics = sum(len(b["topics"]) for b in theory_blocks_data.values())
total_theory_questions = sum(sum(len(t["questions"]) for t in b["topics"]) for b in theory_blocks_data.values())

total_official_exams = sum(len(b["topics"]) for b in exam_blocks_data.values())
total_exam_questions = sum(sum(len(t["questions"]) for t in b["topics"]) for b in exam_blocks_data.values())

def sync_data_files():
    """Garante que mathData_augmented.json, mathData.json e assets/js/data.js estejam 100% sincronizados."""
    with open("mathData_augmented.json", "w", encoding="utf-8") as f:
        json.dump(math_data, f, ensure_ascii=False, indent=2)

    with open("mathData.json", "w", encoding="utf-8") as f:
        json.dump(math_data, f, ensure_ascii=False, indent=2)

    js_data_content = f"""/**
 * PartiuIF - Banco de Dados de Matemática Oficial
 * Contém os {len(math_data)} blocos, {total_subtopics} subtópicos e {total_questions} exercícios com resoluções KaTeX.
 * Gerado automaticamente por build_full_site.py - Fonte da verdade: mathData_augmented.json
 */
var mathData = window.mathData || {json.dumps(math_data, ensure_ascii=False, indent=2)};

if (typeof module !== "undefined" && module.exports) {{
  module.exports = mathData;
}}
"""
    with open("assets/js/data.js", "w", encoding="utf-8") as f:
        f.write(js_data_content)
    print(f"Data synchronized: mathData.json & assets/js/data.js ({total_subtopics} tópicos, {total_questions} questões)")

# ==============================================================================
# 2. RESOLUÇÃO DINÂMICA DE PASTAS E RECURSOS
# ==============================================================================
def get_block_folder(b_id, block):
    """Determina dinamicamente a pasta do bloco."""
    if "folder" in block:
        return block["folder"]
    topics = block.get("topics", [])
    if topics and "folder" in topics[0]:
        return topics[0]["folder"]
    return f"bloco-{b_id}"

def get_pdf_relative_path(pdf_filename, rel_root=".."):
    """Localiza o PDF oficial em qualquer subdiretório de provas/."""
    if not pdf_filename:
        return None
    provas_dir = "provas"
    if os.path.exists(provas_dir):
        for entry in os.listdir(provas_dir):
            full = os.path.join(provas_dir, entry, pdf_filename)
            if os.path.isfile(full):
                return f"{rel_root}/provas/{entry}/{pdf_filename}"
    return None

def resolve_pdf_link(topic_or_filename, rel_root=".."):
    """
    Localiza o PDF oficial priorizando o link do Google Drive se configurado.
    Retorna um dicionário com os metadados do botão ou None se não houver PDF.
    """
    if not topic_or_filename:
        return None
    
    if isinstance(topic_or_filename, dict):
        pdf_filename = topic_or_filename.get("pdf")
        drive_url = topic_or_filename.get("driveUrl") or GOOGLE_DRIVE_PDFS.get(pdf_filename)
    else:
        pdf_filename = topic_or_filename
        drive_url = GOOGLE_DRIVE_PDFS.get(pdf_filename)
        
    if drive_url:
        return {
            "url": drive_url,
            "is_drive": True,
            "attrs": 'target="_blank" rel="noopener noreferrer"',
            "icon": "external-link",
            "title": "Abrir Caderno Oficial no Google Drive (Visualizar ou Baixar)",
            "filename": pdf_filename
        }
    
    local_path = get_pdf_relative_path(pdf_filename, rel_root=rel_root)
    if local_path:
        return {
            "url": local_path,
            "is_drive": False,
            "attrs": 'download',
            "icon": "download",
            "title": "Baixar Caderno Oficial em PDF",
            "filename": pdf_filename
        }
        
    return None

def get_navbar_label(b_id, block):
    """Gera um rótulo curto e elegante para o menu de navegação."""
    title = block.get("title", f"Bloco {b_id}")
    if "ifsc" in title.lower():
        return "Provas IFSC"
    elif "ifce" in title.lower():
        return "Provas IFCE"
    elif "ifsp" in title.lower():
        return "Provas IFSP"
    elif "provas" in title.lower():
        return f"Provas {title.split()[-1]}"
    return f"Bloco {b_id}"

# ==============================================================================
# 3. TEMPLATES REUTILIZÁVEIS (Head, Navbar, Footer)
# ==============================================================================
def get_head(title, rel_root=".", theme="green"):
    if theme == "dark-blue":
        html_tag = '<html lang="pt-BR" class="dark">'
        body_class = 'class="bg-[#0a0f1d] text-slate-100 font-sans antialiased min-h-screen flex flex-col" data-theme="dark"'
    else:
        html_tag = '<html lang="pt-BR">'
        body_class = 'class="bg-gray-50 text-gray-800 font-sans antialiased min-h-screen flex flex-col"'

    return f"""<!DOCTYPE html>
{html_tag}
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            darkMode: 'class',
            theme: {{
                extend: {{
                    colors: {{
                        brand: {{
                            50: '#f0fdf4',
                            100: '#dcfce7',
                            200: '#bbf7d0',
                            300: '#86efac',
                            400: '#4ade80',
                            500: '#22c55e',
                            600: '#16a34a',
                            700: '#15803d',
                            800: '#166534',
                            900: '#14532d',
                            950: '#052e16',
                        }},
                        navy: {{
                            800: '#0f172a',
                            850: '#0b132b',
                            900: '#0a0f1d',
                            950: '#020617',
                        }}
                    }}
                }}
            }}
        }}
    </script>
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>
    <!-- KaTeX para Renderização de Equações -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
    <script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"></script>
    <!-- Custom CSS -->
    <link rel="stylesheet" href="{rel_root}/assets/css/styles.css">
</head>
<body {body_class}>
"""

def get_navbar(active_key="", rel_root=".", is_exam=False):
    if is_exam:
        # Navbar da Parte 2 (Provas - Full Dark Mode Escuro-Azul)
        ifce_n = len(math_data.get("6", {}).get("topics", []))
        ifsc_n = len(math_data.get("5", {}).get("topics", []))
        ifsp_n = len(math_data.get("7", {}).get("topics", []))
        nav_links = [
            ("provas_hub", f"{rel_root}/provas.html", "Todas as Provas", "layout-grid"),
            ("pesquisa", f"{rel_root}/pesquisa.html", "Pesquisa BNCC", "search"),
            ("6", f"{rel_root}/bloco-6-provas-ifce/index.html", f"Provas IFCE ({ifce_n})", "award"),
            ("5", f"{rel_root}/bloco-5-provas-ifsc/index.html", f"Provas IFSC ({ifsc_n})", "award"),
            ("7", f"{rel_root}/bloco-7-provas-ifsp/index.html", f"Provas IFSP ({ifsp_n})", "award"),
        ]
        
        desktop_items = []
        for key, href, label, icon in nav_links:
            is_active = (key == active_key)
            cls = "bg-blue-600 text-white font-semibold shadow-inner" if is_active else "text-slate-300 hover:bg-slate-800 hover:text-white"
            desktop_items.append(f"""<a href="{href}" class="px-3 py-2 rounded-lg text-sm transition flex items-center gap-1.5 {cls}">
                <i data-lucide="{icon}" class="w-4 h-4"></i> {label}
            </a>""")
            
        mobile_items = []
        for key, href, label, icon in nav_links:
            is_active = (key == active_key)
            cls = "bg-blue-600 font-bold" if is_active else "hover:bg-slate-800"
            mobile_items.append(f"""<a href="{href}" class="block px-3 py-2 rounded-md text-base font-medium text-white flex items-center gap-2 {cls}">
                <i data-lucide="{icon}" class="w-4 h-4"></i> {label}
            </a>""")

        return f"""    <!-- Header / Navbar da Área de Provas (Parte 2 - Escuro-Azul) -->
    <header class="gradient-header-dark text-white shadow-xl sticky top-0 z-50 border-b border-slate-800">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-16">
                <!-- Logo Provas -->
                <a href="{rel_root}/provas.html" class="flex items-center space-x-3 group">
                    <div class="bg-blue-600 p-2 rounded-xl text-white font-bold shadow-md shadow-blue-500/20 flex items-center justify-center group-hover:scale-105 transition">
                        <i data-lucide="file-check" class="w-6 h-6"></i>
                    </div>
                    <div>
                        <span class="font-extrabold text-xl tracking-tight text-white flex items-center gap-1.5">
                            Partiu<span class="text-sky-400">IF</span>
                            <span class="text-[10px] font-bold uppercase tracking-wider bg-blue-500/30 text-sky-200 border border-blue-400/30 px-2 py-0.5 rounded-full">Provas</span>
                        </span>
                        <p class="text-xs text-slate-400 hidden sm:flex items-center gap-1">
                            <i data-lucide="archive" class="w-3 h-3 text-sky-400"></i> Acervo Oficial com PDFs e Gabarito
                        </p>
                    </div>
                </a>

                <!-- Navegação Desktop -->
                <nav class="hidden md:flex space-x-1 items-center">
                    {''.join(desktop_items)}
                </nav>

                <!-- Ações do Usuário -->
                <div class="flex items-center gap-2 sm:gap-3">
                    <a href="{rel_root}/index.html" class="bg-slate-800/90 hover:bg-slate-700 text-slate-200 border border-slate-700 px-3.5 py-1.5 rounded-lg text-xs sm:text-sm font-semibold transition flex items-center gap-1.5 shadow-sm" title="Retornar à Teoria e Eixos Temáticos">
                        <i data-lucide="arrow-left" class="w-4 h-4 text-emerald-400"></i> <span class="hidden sm:inline">Voltar para </span>Teoria
                    </a>
                    <a href="{rel_root}/simulado.html" class="bg-blue-600 hover:bg-blue-500 text-white font-semibold px-3.5 py-1.5 rounded-lg text-xs sm:text-sm transition flex items-center gap-1.5 shadow">
                        <i data-lucide="award" class="w-4 h-4"></i> Simulado
                    </a>
                    <button id="mobile-menu-btn" class="md:hidden p-2 rounded-lg text-slate-300 hover:text-white hover:bg-slate-800" aria-label="Abrir menu">
                        <i data-lucide="menu" class="w-6 h-6"></i>
                    </button>
                </div>
            </div>
        </div>

        <!-- Menu Mobile -->
        <div id="mobile-menu" class="hidden md:hidden bg-slate-950 border-t border-slate-800 px-4 pt-2 pb-4 space-y-1">
            {''.join(mobile_items)}
            <a href="{rel_root}/index.html" class="block px-3 py-2 rounded-md text-base font-semibold text-slate-200 hover:bg-slate-800 flex items-center gap-2 mt-2 border-t border-slate-800 pt-3">
                <i data-lucide="arrow-left" class="w-4 h-4 text-emerald-400"></i> Voltar para Teoria (Parte 1)
            </a>
            <a href="{rel_root}/simulado.html" class="block px-3 py-2 rounded-md text-base font-bold bg-blue-600 text-white flex items-center gap-2 mt-2">
                <i data-lucide="award" class="w-4 h-4"></i> Simulado IF
            </a>
        </div>
    </header>
"""

    # Navbar da Parte 1 (Teoria - Verde Institucional)
    blocks_nav = [("home", f"{rel_root}/index.html", "Início", "home")]
    for b_id, block in theory_blocks_data.items():
        folder = get_block_folder(b_id, block)
        label = get_navbar_label(b_id, block)
        icon = block.get("icon", "book")
        blocks_nav.append((b_id, f"{rel_root}/{folder}/index.html", label, icon))

    desktop_links = []
    for key, href, label, icon in blocks_nav:
        is_active = (key == active_key)
        active_class = "bg-brand-800 text-white font-semibold shadow-inner" if is_active else "text-brand-100 hover:bg-brand-800/70 hover:text-white"
        desktop_links.append(f"""<a href="{href}" class="px-3 py-2 rounded-lg text-sm transition flex items-center gap-1.5 {active_class}">
            <i data-lucide="{icon}" class="w-4 h-4"></i> {label}
        </a>""")

    mobile_links = []
    for key, href, label, icon in blocks_nav:
        is_active = (key == active_key)
        active_class = "bg-brand-800 font-bold" if is_active else "hover:bg-brand-800/60"
        mobile_links.append(f"""<a href="{href}" class="block px-3 py-2 rounded-md text-base font-medium text-white flex items-center gap-2 {active_class}">
            <i data-lucide="{icon}" class="w-4 h-4"></i> {label}
        </a>""")

    return f"""    <!-- Header / Navbar Principal (Parte 1 - Teoria) -->
    <header class="gradient-header text-white shadow-lg sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-16">
                <!-- Logo & Título -->
                <a href="{rel_root}/index.html" class="flex items-center space-x-3 group">
                    <div class="bg-white p-2 rounded-xl text-brand-700 font-bold shadow-md flex items-center justify-center group-hover:scale-105 transition">
                        <i data-lucide="graduation-cap" class="w-6 h-6"></i>
                    </div>
                    <div>
                        <span class="font-extrabold text-xl tracking-tight text-white flex items-center gap-1">
                            Partiu<span class="text-brand-300">IF</span>
                        </span>
                        <p class="text-xs text-brand-100 hidden sm:flex items-center gap-1">
                            <i data-lucide="save" class="w-3 h-3 text-brand-300"></i> Progresso local ativado
                        </p>
                    </div>
                </a>

                <!-- Navegação Desktop -->
                <nav class="hidden md:flex space-x-1">
                    {''.join(desktop_links)}
                </nav>

                <!-- Ações do Usuário: Botão Destacado de Provas, Pesquisa e Simulado -->
                <div class="flex items-center gap-2 sm:gap-2.5">
                    <a href="{rel_root}/pesquisa.html" class="bg-emerald-600 hover:bg-emerald-500 text-white font-bold px-3 py-1.5 rounded-lg text-xs sm:text-sm transition flex items-center gap-1.5 shadow" title="Pesquisar questões por descritor BNCC">
                        <i data-lucide="search" class="w-4 h-4 text-emerald-200"></i> <span class="hidden xl:inline">Pesquisa</span> BNCC
                    </a>
                    <a href="{rel_root}/provas.html" class="bg-gradient-to-r from-blue-700 to-indigo-800 hover:from-blue-600 hover:to-indigo-700 text-white font-bold px-3.5 py-1.5 rounded-lg text-sm transition flex items-center gap-1.5 shadow-md border border-blue-400/40" title="Acessar o Banco de Provas Oficiais (Parte 2)">
                        <i data-lucide="file-check" class="w-4 h-4 text-sky-300"></i> Provas Oficiais <span class="bg-sky-400 text-slate-950 text-[10px] font-extrabold px-1.5 py-0.2 rounded-full ml-0.5">{total_official_exams}</span>
                    </a>
                    <a href="{rel_root}/simulado.html" class="bg-brand-500 hover:bg-brand-400 text-white font-semibold px-3 py-1.5 rounded-lg text-sm transition flex items-center gap-1.5 shadow hover:shadow-md">
                        <i data-lucide="award" class="w-4 h-4"></i> Simulado
                    </a>
                    <button id="mobile-menu-btn" class="md:hidden p-2 rounded-lg text-brand-100 hover:text-white hover:bg-brand-800" aria-label="Abrir menu">
                        <i data-lucide="menu" class="w-6 h-6"></i>
                    </button>
                </div>
            </div>
        </div>

        <!-- Menu Mobile -->
        <div id="mobile-menu" class="hidden md:hidden bg-brand-900 border-t border-brand-800 px-4 pt-2 pb-4 space-y-1">
            {''.join(mobile_links)}
            <a href="{rel_root}/provas.html" class="block px-3 py-2 rounded-md text-base font-bold bg-blue-700 text-white flex items-center justify-between gap-2 mt-2">
                <span class="flex items-center gap-2"><i data-lucide="file-check" class="w-4 h-4 text-sky-300"></i> Provas Oficiais (Parte 2)</span>
                <span class="bg-sky-400 text-slate-950 text-xs font-bold px-2 py-0.5 rounded-full">{total_official_exams} Provas</span>
            </a>
            <a href="{rel_root}/simulado.html" class="block px-3 py-2 rounded-md text-base font-bold bg-brand-600 text-white flex items-center gap-2 mt-1">
                <i data-lucide="award" class="w-4 h-4"></i> Simulado IF Geral
            </a>
        </div>
    </header>
"""

def get_footer(rel_root=".", is_exam=False):
    if is_exam:
        # Footer da Área de Provas (Parte 2 - Escuro-Azul)
        return f"""    <footer class="bg-[#020617] text-slate-300 border-t border-slate-800 mt-16 py-10">
        <div class="max-w-7xl mx-auto px-4 grid grid-cols-1 md:grid-cols-3 gap-8 text-sm">
            <div>
                <div class="flex items-center gap-2 text-lg font-bold text-sky-400 mb-2">
                    <i data-lucide="file-check" class="w-5 h-5 text-blue-500"></i> PartiuIF - Banco de Provas
                </div>
                <p class="text-slate-400 text-xs leading-relaxed">
                    Acervo completo com {total_official_exams} cadernos oficiais do IFCE, IFSC e IFSP. Provas interativas com resoluções KaTeX passo a passo e downloads dos cadernos originais em PDF.
                </p>
                <div class="mt-4 inline-flex items-center gap-2 bg-slate-900 px-3 py-1.5 rounded-lg border border-slate-800 text-xs text-sky-300">
                    <i data-lucide="hard-drive" class="w-3.5 h-3.5"></i> Respostas salvas localmente
                </div>
            </div>
            <div>
                <h4 class="font-semibold text-white mb-3 text-sm flex items-center gap-1.5">
                    <i data-lucide="layers" class="w-4 h-4 text-blue-400"></i> Navegação do Acervo
                </h4>
                <ul class="space-y-2 text-xs text-slate-300">
                    <li><a href="{rel_root}/provas.html" class="hover:text-white transition flex items-center gap-1.5">• Ver Todas as Provas</a></li>
                    <li><a href="{rel_root}/bloco-6-provas-ifce/index.html" class="hover:text-white transition flex items-center gap-1.5">• Provas IFCE ({len(math_data.get("6", {}).get("topics", []))} Cadernos)</a></li>
                    <li><a href="{rel_root}/bloco-5-provas-ifsc/index.html" class="hover:text-white transition flex items-center gap-1.5">• Provas IFSC ({len(math_data.get("5", {}).get("topics", []))} Cadernos)</a></li>
                    <li><a href="{rel_root}/bloco-7-provas-ifsp/index.html" class="hover:text-white transition flex items-center gap-1.5">• Provas IFSP ({len(math_data.get("7", {}).get("topics", []))} Cadernos)</a></li>
                    <li class="pt-2"><a href="{rel_root}/index.html" class="text-emerald-400 hover:text-emerald-300 font-semibold transition flex items-center gap-1.5">← Voltar para Teoria e Eixos Temáticos</a></li>
                </ul>
            </div>
            <div>
                <h4 class="font-semibold text-white mb-2 text-sm flex items-center gap-1.5">
                    <i data-lucide="trending-up" class="w-4 h-4 text-blue-400"></i> Progresso no Acervo
                </h4>
                <div class="w-full bg-slate-800 rounded-full h-3 overflow-hidden border border-slate-700 mb-1.5">
                    <div id="footer-progress" class="bg-blue-500 h-full w-0 transition-all duration-500"></div>
                </div>
                <span id="footer-progress-text" class="text-xs text-slate-400 block mb-4">Carregando progresso...</span>
                
                <button onclick="resetProgress()" class="text-xs text-red-400 hover:text-red-300 underline flex items-center gap-1 transition">
                    <i data-lucide="trash-2" class="w-3.5 h-3.5"></i> Zerar Todo o Meu Progresso
                </button>
            </div>
        </div>
        <div class="max-w-7xl mx-auto px-4 mt-8 pt-4 border-t border-slate-900 text-center text-xs text-slate-500">
            PartiuIF &copy; 2026 - Acervo Oficial de Provas para os Institutos Federais.
        </div>
    </footer>

    <!-- Scripts Globais da Aplicação -->
    <script src="{rel_root}/assets/js/data.js"></script>
    <script src="{rel_root}/assets/js/app.js"></script>
"""

    # Footer da Parte 1 (Teoria - Verde Institucional)
    footer_block_links = []
    for b_id, block in theory_blocks_data.items():
        folder = get_block_folder(b_id, block)
        footer_block_links.append(f'<li><a href="{rel_root}/{folder}/index.html" class="hover:text-white transition flex items-center gap-1">• {block["title"]}</a></li>')

    return f"""    <footer class="bg-brand-950 text-white border-t border-brand-800 mt-16 py-10">
        <div class="max-w-7xl mx-auto px-4 grid grid-cols-1 md:grid-cols-3 gap-8 text-sm">
            <div>
                <div class="flex items-center gap-2 text-lg font-bold text-brand-300 mb-2">
                    <i data-lucide="book-open-check" class="w-5 h-5"></i> PartiuIF - Matemática
                </div>
                <p class="text-brand-200 text-xs leading-relaxed">
                    Plataforma completa de revisão estruturada por subtópicos, teoria detalhada, fórmulas KaTeX e simulados com {total_official_exams} provas oficiais do IFCE, IFSC e IFSP.
                </p>
                <div class="mt-4 inline-flex items-center gap-2 bg-brand-900/80 px-3 py-1.5 rounded-lg border border-brand-800 text-xs text-brand-300">
                    <i data-lucide="hard-drive" class="w-3.5 h-3.5"></i> Progresso salvo no seu navegador
                </div>
            </div>
            <div>
                <h4 class="font-semibold text-white mb-3 text-sm flex items-center gap-1.5">
                    <i data-lucide="layers" class="w-4 h-4 text-brand-400"></i> Eixos Temáticos
                </h4>
                <ul class="space-y-1.5 text-xs text-brand-200">
                    {''.join(footer_block_links)}
                    <li class="pt-2">
                        <a href="{rel_root}/provas.html" class="inline-flex items-center gap-1.5 bg-blue-900/60 hover:bg-blue-800 text-sky-300 font-bold px-3 py-1.5 rounded-lg border border-blue-700/60 transition">
                            <i data-lucide="file-check" class="w-3.5 h-3.5"></i> Acessar Banco de Provas (Parte 2) →
                        </a>
                    </li>
                </ul>
            </div>
            <div>
                <h4 class="font-semibold text-white mb-2 text-sm flex items-center gap-1.5">
                    <i data-lucide="trending-up" class="w-4 h-4 text-brand-400"></i> Status Geral da Preparação
                </h4>
                <div class="w-full bg-brand-900 rounded-full h-3 overflow-hidden border border-brand-700 mb-1.5">
                    <div id="footer-progress" class="bg-brand-400 h-full w-0 transition-all duration-500"></div>
                </div>
                <span id="footer-progress-text" class="text-xs text-brand-300 block mb-4">Carregando progresso...</span>
                
                <button onclick="resetProgress()" class="text-xs text-red-400 hover:text-red-300 underline flex items-center gap-1 transition">
                    <i data-lucide="trash-2" class="w-3.5 h-3.5"></i> Zerar Todo o Meu Progresso
                </button>
            </div>
        </div>
        <div class="max-w-7xl mx-auto px-4 mt-8 pt-4 border-t border-brand-900 text-center text-xs text-brand-400">
            PartiuIF &copy; 2026 - Plataforma Educacional de Revisão para os Institutos Federais.
        </div>
    </footer>

    <!-- Scripts Globais da Aplicação -->
    <script src="{rel_root}/assets/js/data.js"></script>
    <script src="{rel_root}/assets/js/app.js"></script>
"""

# ==============================================================================
# 4. GERAÇÃO DE PÁGINAS DE SUBTÓPICOS / PROVAS INDIVIDUAIS
# ==============================================================================
def build_subtopic_pages():
    print(f"\n--- Generating {total_subtopics} Subtopic & Exam Pages ---")
    
    for b_id, block in math_data.items():
        folder = get_block_folder(b_id, block)
        os.makedirs(folder, exist_ok=True)
        topics = block["topics"]
        is_exam = is_exam_block(b_id, block)
        theme = "dark-blue" if is_exam else "green"
        
        for idx, topic in enumerate(topics):
            t_id = topic["id"]
            title = topic["title"]
            filename = topic["filename"]
            target_path = os.path.join(folder, filename)
            
            prev_topic = topics[idx - 1] if idx > 0 else None
            next_topic = topics[idx + 1] if idx < len(topics) - 1 else None

            # Exemplo Resolvido
            solved_ex = topic.get("solvedExample", {})
            problem_txt = solved_ex.get("problem", "")
            sol_txt = solved_ex.get("solution", "")

            # Botão de Download / Acesso do Caderno Oficial
            pdf_info = resolve_pdf_link(topic, rel_root="..")

            if is_exam:
                # ----------------------- MODO ESCURO-AZUL (PROVAS) -----------------------
                key_points_html = "".join([f"""
                    <li class="flex items-start gap-2 text-xs sm:text-sm text-slate-300">
                        <i data-lucide="check" class="w-4 h-4 text-sky-400 flex-shrink-0 mt-0.5"></i>
                        <span>{point}</span>
                    </li>
                """ for point in topic.get("keyPoints", [])])

                pdf_download_btn = ""
                if pdf_info:
                    btn_label = "Caderno Oficial no Drive" if pdf_info["is_drive"] else "Baixar Caderno em PDF"
                    pdf_download_btn = f"""
                        <a href="{pdf_info['url']}" {pdf_info['attrs']} class="bg-blue-600 hover:bg-blue-500 text-white font-bold px-4 py-2 rounded-xl text-sm transition flex items-center gap-2 shadow-lg shadow-blue-600/25" title="{pdf_info['title']}">
                            <i data-lucide="{pdf_info['icon']}" class="w-4 h-4"></i> {btn_label}
                        </a>
                    """

                questions_html = []
                for q_idx, q in enumerate(topic.get("questions", [])):
                    q_id = f"{t_id}-q{q_idx}"
                    options_buttons = []
                    for opt_idx, opt in enumerate(q.get("options", [])):
                        letter = chr(65 + opt_idx)
                        options_buttons.append(f"""
                            <button onclick="selectOption('{q_id}', {opt_idx})" id="btn-{q_id}-{opt_idx}" class="w-full text-left p-3.5 rounded-xl border border-slate-800 bg-slate-950/60 hover:border-blue-500 hover:bg-slate-800/60 transition text-sm text-slate-200 flex items-center justify-between group">
                                <span class="flex items-center gap-2"><strong class="text-sky-400 font-bold">{letter})</strong> {opt}</span>
                                <i data-lucide="circle" class="w-4 h-4 text-slate-600 opt-icon group-hover:text-blue-400 flex-shrink-0"></i>
                            </button>
                        """)

                    bncc_badge = ""
                    if is_exam and q.get("bncc"):
                        bncc_code = q["bncc"]
                        bncc_desc = q.get("bnccDesc", "")
                        bncc_badge = f"""
                            <a href="../pesquisa.html?bncc={bncc_code}" class="text-[11px] font-mono font-bold text-emerald-300 bg-emerald-950/80 hover:bg-emerald-900/90 px-2.5 py-0.5 rounded-full border border-emerald-800/60 flex items-center gap-1 transition shadow-sm" title="{bncc_desc}">
                                <i data-lucide="bookmark" class="w-3 h-3 text-emerald-400"></i> BNCC: {bncc_code}
                            </a>
                        """

                    questions_html.append(f"""
                        <div class="mb-8 border-b border-slate-800/80 pb-6 last:border-0 last:pb-0" id="q-container-{q_id}">
                            <div class="flex items-center justify-between mb-3 flex-wrap gap-2">
                                <div class="flex items-center gap-2">
                                    <span class="text-xs font-bold uppercase tracking-wider text-sky-300 bg-blue-950/60 px-2.5 py-0.5 rounded-full border border-blue-800/40">Questão {q_idx + 1}</span>
                                    {bncc_badge}
                                </div>
                            </div>
                            <p class="font-medium text-slate-100 mb-4 text-sm sm:text-base leading-relaxed">{q.get('q', '')}</p>
                            <div class="space-y-2 mb-4" id="opts-{q_id}">
                                {''.join(options_buttons)}
                            </div>
                            <div class="flex items-center gap-3">
                                <button id="submit-btn-{q_id}" onclick="submitAnswer('{b_id}', '{t_id}', {q_idx})" class="bg-blue-600 hover:bg-blue-500 text-white px-5 py-2.5 rounded-xl text-sm font-bold transition flex items-center gap-1.5 shadow-lg shadow-blue-600/25">
                                    <i data-lucide="send" class="w-4 h-4"></i> Enviar Resposta
                                </button>
                            </div>
                            <div id="feedback-{q_id}" class="hidden p-4 rounded-xl text-sm mt-4"></div>
                        </div>
                    """)

                sidebar_items = []
                for s_idx, s_topic in enumerate(topics):
                    is_current = (s_topic["id"] == t_id)
                    active_sidebar_class = "bg-blue-950/80 text-sky-200 font-bold border-l-4 border-blue-500 pl-3" if is_current else "text-slate-400 hover:bg-slate-800/60 hover:text-white pl-2"
                    sidebar_items.append(f"""
                        <a href="./{s_topic['filename']}" class="w-full text-left py-2 px-2.5 rounded-lg text-xs transition flex items-center justify-between {active_sidebar_class}">
                            <span class="truncate pr-2">{s_idx + 1}. {s_topic['title']}</span>
                            <i id="status-icon-{s_topic['id']}" data-lucide="circle" class="w-4 h-4 text-slate-600 flex-shrink-0"></i>
                        </a>
                    """)

                nav_buttons = []
                if prev_topic:
                    nav_buttons.append(f"""
                        <a href="./{prev_topic['filename']}" class="bg-slate-900 border border-slate-800 hover:bg-slate-800 text-slate-200 font-semibold px-4 py-2.5 rounded-xl text-sm transition flex items-center gap-2 shadow-sm">
                            <i data-lucide="arrow-left" class="w-4 h-4 text-sky-400"></i> Anterior: {prev_topic['title']}
                        </a>
                    """)
                else:
                    nav_buttons.append(f"""
                        <a href="../provas.html" class="bg-slate-900 border border-slate-800 hover:bg-slate-800 text-slate-200 font-semibold px-4 py-2.5 rounded-xl text-sm transition flex items-center gap-2 shadow-sm">
                            <i data-lucide="arrow-left" class="w-4 h-4 text-sky-400"></i> Acervo de Provas
                        </a>
                    """)

                nav_buttons.append(f"""
                    <a href="./index.html" class="bg-blue-950/60 border border-blue-800/50 text-sky-200 hover:bg-blue-900/60 font-semibold px-4 py-2.5 rounded-xl text-sm transition flex items-center gap-2 shadow-sm">
                        <i data-lucide="grid" class="w-4 h-4"></i> Todas do Bloco
                    </a>
                """)

                if next_topic:
                    nav_buttons.append(f"""
                        <a href="./{next_topic['filename']}" class="bg-blue-600 hover:bg-blue-500 text-white font-bold px-4 py-2.5 rounded-xl text-sm transition flex items-center gap-2 shadow-lg shadow-blue-600/20 ml-auto">
                            Próxima: {next_topic['title']} <i data-lucide="arrow-right" class="w-4 h-4"></i>
                        </a>
                    """)
                else:
                    nav_buttons.append(f"""
                        <a href="../provas.html" class="bg-blue-600 hover:bg-blue-500 text-white font-bold px-4 py-2.5 rounded-xl text-sm transition flex items-center gap-2 shadow-lg shadow-blue-600/20 ml-auto">
                            Todas as Provas <i data-lucide="award" class="w-4 h-4"></i>
                        </a>
                    """)

                page_html = f"""{get_head(f"{title} - {block['title']} | PartiuIF", rel_root="..", theme="dark-blue")}
{get_navbar(active_key=b_id, rel_root="..", is_exam=True)}

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-grow">
        <!-- Breadcrumbs -->
        <nav class="flex text-xs font-medium text-slate-400 mb-6" aria-label="Breadcrumb">
            <ol class="inline-flex items-center space-x-1 sm:space-x-2">
                <li><a href="../index.html" class="hover:text-sky-400 flex items-center gap-1"><i data-lucide="home" class="w-3.5 h-3.5"></i> Início</a></li>
                <li><span class="text-slate-600">/</span></li>
                <li><a href="../provas.html" class="hover:text-sky-400 flex items-center gap-1"><i data-lucide="archive" class="w-3.5 h-3.5"></i> Provas</a></li>
                <li><span class="text-slate-600">/</span></li>
                <li><a href="./index.html" class="hover:text-sky-400">{block['title']}</a></li>
                <li><span class="text-slate-600">/</span></li>
                <li class="text-slate-200 font-semibold truncate max-w-xs sm:max-w-none">{title}</li>
            </ol>
        </nav>

        <div class="grid grid-cols-1 lg:grid-cols-4 gap-8 items-start">
            <!-- Conteúdo Principal (3 Colunas) -->
            <div class="lg:col-span-3 space-y-8">
                
                <!-- Cabeçalho do Exame -->
                <div class="bg-slate-900/90 border border-slate-800 rounded-3xl p-6 sm:p-8 shadow-xl text-slate-100">
                    <div class="flex flex-wrap items-center justify-between gap-3 mb-4">
                        <span class="text-xs font-bold uppercase tracking-wider text-sky-300 bg-blue-950/80 px-3 py-1 rounded-full border border-blue-800/60">
                            BNCC: {topic.get('bncc', 'Exame Oficial')}
                        </span>
                        <div class="flex items-center gap-2">
                            {pdf_download_btn}
                            <button id="btn-toggle-done-{t_id}" onclick="toggleTopicDone('{t_id}')" class="px-4 py-2 rounded-xl text-sm font-semibold border bg-slate-900 text-slate-300 border-slate-700 hover:bg-slate-800 transition flex items-center gap-2 shadow-sm">
                                <i data-lucide="square" class="w-4 h-4 text-slate-500"></i> Marcar como Concluída
                            </button>
                        </div>
                    </div>

                    <h1 class="text-2xl sm:text-4xl font-extrabold text-white tracking-tight mb-3">
                        {title}
                    </h1>
                    <p class="text-slate-300 text-sm sm:text-base leading-relaxed mb-6">
                        {topic.get('summary', '')}
                    </p>

                    <!-- Seção Teórica / Informações do Exame -->
                    <div class="bg-slate-950/70 border border-slate-800/80 rounded-2xl p-5 mb-6">
                        <h2 class="text-sm font-bold text-sky-400 uppercase tracking-wider mb-2 flex items-center gap-2">
                            <i data-lucide="book-open" class="w-4 h-4 text-sky-400"></i> Informações do Exame e Conteúdos Cobrados
                        </h2>
                        <div class="text-xs sm:text-sm text-slate-300 leading-relaxed space-y-2">
                            <p>{topic.get('detailedTheory', '')}</p>
                        </div>
                    </div>

                    <!-- Pontos-Chave -->
                    <div class="mb-6">
                        <h3 class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">Conceitos Mais Cobrados Nesta Edição</h3>
                        <ul class="grid grid-cols-1 sm:grid-cols-2 gap-2">
                            {key_points_html}
                        </ul>
                    </div>

                    <!-- Fórmulas KaTeX -->
                    <div class="bg-slate-950 border border-blue-900/50 text-white rounded-2xl p-5 shadow-inner">
                        <div class="flex items-center justify-between mb-2">
                            <span class="text-xs font-bold text-sky-300 uppercase tracking-wider flex items-center gap-1.5">
                                <i data-lucide="sigma" class="w-4 h-4"></i> Fórmulas-Chave para a Prova
                            </span>
                        </div>
                        <div class="text-sm sm:text-base font-mono overflow-x-auto py-2 text-center text-sky-200">
                            $${topic.get('formula', '')}$$
                        </div>
                    </div>
                </div>

                <!-- Exemplo Resolvido Passo a Passo -->
                <section class="bg-slate-900/90 border border-slate-800 rounded-3xl p-6 sm:p-8 shadow-xl text-slate-100">
                    <h2 class="text-lg font-bold text-sky-300 mb-3 flex items-center gap-2">
                        <i data-lucide="file-check-2" class="w-5 h-5 text-sky-400"></i> Resolução Comentada de Destaque
                    </h2>
                    <div class="bg-slate-950/90 border border-slate-800 rounded-2xl p-5 shadow-inner">
                        <p class="text-sm sm:text-base font-semibold text-slate-100 mb-3">{problem_txt}</p>
                        <div class="text-xs sm:text-sm text-slate-300 leading-relaxed whitespace-pre-line border-t border-slate-800 pt-3">
                            <strong class="text-sky-300 block mb-1">Resolução Detalhada:</strong>
                            {sol_txt}
                        </div>
                    </div>
                </section>

                <!-- Caderno de Questões da Prova -->
                <section class="bg-slate-900/90 border border-slate-800 rounded-3xl p-6 sm:p-8 shadow-xl text-slate-100">
                    <div class="flex items-center justify-between mb-6 pb-4 border-b border-slate-800">
                        <div>
                            <h2 class="text-xl font-bold text-white flex items-center gap-2">
                                <i data-lucide="list-checks" class="w-6 h-6 text-sky-400"></i> Questões Oficiais da Prova
                            </h2>
                            <p class="text-xs text-slate-400 mt-1">Resolva as questões para simular o exame. Suas respostas são salvas automaticamente.</p>
                        </div>
                        <span class="text-xs font-semibold px-2.5 py-1 rounded-full bg-blue-950/60 text-sky-300 border border-blue-800/40">
                            {len(topic.get('questions', []))} Questões
                        </span>
                    </div>

                    {''.join(questions_html)}
                </section>

                <!-- Navegação Inferior -->
                <div class="flex flex-wrap items-center justify-between gap-4 pt-4 border-t border-slate-800">
                    {''.join(nav_buttons)}
                </div>

            </div>

            <!-- Sidebar Lateral (1 Coluna) -->
            <div class="lg:col-span-1 space-y-6">
                <div class="bg-slate-900/95 border border-slate-800 rounded-3xl p-5 shadow-xl sticky top-24 text-slate-200">
                    <div class="flex items-center justify-between mb-4 pb-3 border-b border-slate-800">
                        <div>
                            <span class="text-xs font-bold text-sky-400 uppercase tracking-wider block">Acervo da Instituição</span>
                            <h3 class="text-sm font-extrabold text-white truncate">{block['title']}</h3>
                        </div>
                        <span class="text-xs font-semibold px-2 py-0.5 rounded-full bg-slate-800 text-slate-400 border border-slate-700">
                            {idx + 1}/{len(topics)}
                        </span>
                    </div>

                    <div class="space-y-1 dark-scrollbar max-h-[60vh] overflow-y-auto pr-1">
                        {''.join(sidebar_items)}
                    </div>

                    <div class="mt-5 pt-4 border-t border-slate-800 flex flex-col gap-2">
                        <a href="./index.html" class="w-full bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold py-2 px-3 rounded-xl text-xs transition flex items-center justify-center gap-1.5 border border-slate-700">
                            <i data-lucide="layout-grid" class="w-3.5 h-3.5"></i> Visão Geral do Bloco
                        </a>
                        <a href="../provas.html" class="w-full bg-blue-950/60 hover:bg-blue-900/60 text-sky-300 font-semibold py-2 px-3 rounded-xl text-xs transition flex items-center justify-center gap-1.5 border border-blue-800/40">
                            <i data-lucide="archive" class="w-3.5 h-3.5"></i> Todas as Provas
                        </a>
                    </div>
                </div>
            </div>

        </div>
    </main>

{get_footer(rel_root="..", is_exam=True)}

    <script>
        document.addEventListener('DOMContentLoaded', () => {{
            initQuestionStates('{t_id}', '{b_id}');
            updateTopicDoneButtonUI('{t_id}');
        }});
    </script>
</body>
</html>
"""
            else:
                # ----------------------- MODO VERDE PADRÃO (TEORIA) -----------------------
                key_points_html = "".join([f"""
                    <li class="flex items-start gap-2 text-xs sm:text-sm text-gray-700">
                        <i data-lucide="check" class="w-4 h-4 text-brand-600 flex-shrink-0 mt-0.5"></i>
                        <span>{point}</span>
                    </li>
                """ for point in topic.get("keyPoints", [])])

                pdf_download_btn = ""
                if pdf_info:
                    btn_label = "Caderno Oficial no Drive" if pdf_info["is_drive"] else "Baixar Prova em PDF"
                    pdf_download_btn = f"""
                        <a href="{pdf_info['url']}" {pdf_info['attrs']} class="bg-brand-700 hover:bg-brand-800 text-white font-semibold px-4 py-2 rounded-xl text-sm transition flex items-center gap-2 shadow-sm" title="{pdf_info['title']}">
                            <i data-lucide="{pdf_info['icon']}" class="w-4 h-4"></i> {btn_label}
                        </a>
                    """

                questions_html = []
                for q_idx, q in enumerate(topic.get("questions", [])):
                    q_id = f"{t_id}-q{q_idx}"
                    options_buttons = []
                    for opt_idx, opt in enumerate(q.get("options", [])):
                        letter = chr(65 + opt_idx)
                        options_buttons.append(f"""
                            <button onclick="selectOption('{q_id}', {opt_idx})" id="btn-{q_id}-{opt_idx}" class="w-full text-left p-3.5 rounded-xl border border-gray-200 hover:border-brand-400 hover:bg-brand-50/40 transition text-sm text-gray-700 flex items-center justify-between group">
                                <span class="flex items-center gap-2"><strong class="text-brand-700 font-bold">{letter})</strong> {opt}</span>
                                <i data-lucide="circle" class="w-4 h-4 text-gray-300 opt-icon group-hover:text-brand-400 flex-shrink-0"></i>
                            </button>
                        """)

                    questions_html.append(f"""
                        <div class="mb-8 border-b border-gray-100 pb-6 last:border-0 last:pb-0" id="q-container-{q_id}">
                            <div class="flex items-center justify-between mb-2">
                                <span class="text-xs font-bold uppercase tracking-wider text-brand-700 bg-brand-50 px-2.5 py-0.5 rounded-full border border-brand-100">Questão {q_idx + 1}</span>
                            </div>
                            <p class="font-medium text-gray-800 mb-4 text-sm sm:text-base leading-relaxed">{q.get('q', '')}</p>
                            <div class="space-y-2 mb-4" id="opts-{q_id}">
                                {''.join(options_buttons)}
                            </div>
                            <div class="flex items-center gap-3">
                                <button id="submit-btn-{q_id}" onclick="submitAnswer('{b_id}', '{t_id}', {q_idx})" class="bg-brand-600 hover:bg-brand-700 text-white px-4 py-2 rounded-lg text-sm font-semibold transition flex items-center gap-1.5 shadow-sm">
                                    <i data-lucide="send" class="w-4 h-4"></i> Enviar Resposta
                                </button>
                            </div>
                            <div id="feedback-{q_id}" class="hidden p-4 rounded-xl text-sm mt-4"></div>
                        </div>
                    """)

                sidebar_items = []
                for s_idx, s_topic in enumerate(topics):
                    is_current = (s_topic["id"] == t_id)
                    active_sidebar_class = "bg-brand-100 text-brand-900 font-bold border-l-4 border-brand-600 pl-3" if is_current else "text-gray-600 hover:bg-gray-100 pl-2"
                    sidebar_items.append(f"""
                        <a href="./{s_topic['filename']}" class="w-full text-left py-2 px-2.5 rounded-lg text-xs transition flex items-center justify-between {active_sidebar_class}">
                            <span class="truncate pr-2">{s_idx + 1}. {s_topic['title']}</span>
                            <i id="status-icon-{s_topic['id']}" data-lucide="circle" class="w-4 h-4 text-gray-300 flex-shrink-0"></i>
                        </a>
                    """)

                nav_buttons = []
                if prev_topic:
                    nav_buttons.append(f"""
                        <a href="./{prev_topic['filename']}" class="bg-white border border-gray-200 hover:bg-gray-50 text-gray-700 font-semibold px-4 py-2.5 rounded-xl text-sm transition flex items-center gap-2 shadow-sm">
                            <i data-lucide="arrow-left" class="w-4 h-4"></i> Anterior: {prev_topic['title']}
                        </a>
                    """)
                else:
                    nav_buttons.append(f"""
                        <a href="./index.html" class="bg-white border border-gray-200 hover:bg-gray-50 text-gray-700 font-semibold px-4 py-2.5 rounded-xl text-sm transition flex items-center gap-2 shadow-sm">
                            <i data-lucide="arrow-left" class="w-4 h-4"></i> Visão Geral do Bloco
                        </a>
                    """)

                nav_buttons.append(f"""
                    <a href="./index.html" class="bg-brand-50 border border-brand-200 text-brand-800 hover:bg-brand-100 font-semibold px-4 py-2.5 rounded-xl text-sm transition flex items-center gap-2 shadow-sm">
                        <i data-lucide="grid" class="w-4 h-4"></i> Todos os Tópicos
                    </a>
                """)

                if next_topic:
                    nav_buttons.append(f"""
                        <a href="./{next_topic['filename']}" class="bg-brand-600 hover:bg-brand-700 text-white font-semibold px-4 py-2.5 rounded-xl text-sm transition flex items-center gap-2 shadow-sm ml-auto">
                            Próximo: {next_topic['title']} <i data-lucide="arrow-right" class="w-4 h-4"></i>
                        </a>
                    """)
                else:
                    nav_buttons.append(f"""
                        <a href="../simulado.html" class="bg-brand-600 hover:bg-brand-700 text-white font-semibold px-4 py-2.5 rounded-xl text-sm transition flex items-center gap-2 shadow-sm ml-auto">
                            Simulado Geral <i data-lucide="award" class="w-4 h-4"></i>
                        </a>
                    """)

                page_html = f"""{get_head(f"{title} - {block['title']} | PartiuIF", rel_root="..", theme="green")}
{get_navbar(active_key=b_id, rel_root="..", is_exam=False)}

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-grow">
        <!-- Breadcrumbs -->
        <nav class="flex text-xs font-medium text-gray-500 mb-6" aria-label="Breadcrumb">
            <ol class="inline-flex items-center space-x-1 sm:space-x-2">
                <li><a href="../index.html" class="hover:text-brand-700 flex items-center gap-1"><i data-lucide="home" class="w-3.5 h-3.5"></i> Início</a></li>
                <li><span class="text-gray-400">/</span></li>
                <li><a href="./index.html" class="hover:text-brand-700">{block['title']}</a></li>
                <li><span class="text-gray-400">/</span></li>
                <li class="text-gray-800 font-semibold truncate max-w-xs sm:max-w-none">{title}</li>
            </ol>
        </nav>

        <div class="grid grid-cols-1 lg:grid-cols-4 gap-8 items-start">
            
            <!-- Conteúdo Principal (3 Colunas) -->
            <div class="lg:col-span-3 space-y-8">
                
                <!-- Cabeçalho do Subtópico -->
                <div class="bg-white border border-gray-200 rounded-2xl p-6 sm:p-8 shadow-sm">
                    <div class="flex flex-wrap items-center justify-between gap-3 mb-4">
                        <span class="text-xs font-bold uppercase tracking-wider text-brand-800 bg-brand-100 px-3 py-1 rounded-full border border-brand-200">
                            BNCC: {topic.get('bncc', 'Revisão Geral')}
                        </span>
                        <div class="flex items-center gap-2">
                            {pdf_download_btn}
                            <button id="btn-toggle-done-{t_id}" onclick="toggleTopicDone('{t_id}')" class="px-4 py-2 rounded-xl text-sm font-semibold border border-gray-300 hover:bg-gray-50 transition flex items-center gap-2 shadow-sm text-gray-700">
                                <i data-lucide="square" class="w-4 h-4 text-gray-400"></i> Marcar como Concluído
                            </button>
                        </div>
                    </div>

                    <h1 class="text-2xl sm:text-4xl font-extrabold text-gray-900 tracking-tight mb-3">
                        {title}
                    </h1>
                    <p class="text-gray-600 text-sm sm:text-base leading-relaxed mb-6">
                        {topic.get('summary', '')}
                    </p>

                    <!-- Seção Teórica Detalhada -->
                    <div class="bg-gray-50 border border-gray-200 rounded-xl p-5 mb-6">
                        <h2 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-2 flex items-center gap-2">
                            <i data-lucide="book-open" class="w-4 h-4 text-brand-600"></i> Teoria e Fundamentos Essenciais
                        </h2>
                        <div class="text-xs sm:text-sm text-gray-700 leading-relaxed space-y-2">
                            <p>{topic.get('detailedTheory', '')}</p>
                        </div>
                    </div>

                    <!-- Pontos-Chave -->
                    <div class="mb-6">
                        <h3 class="text-xs font-bold text-gray-500 uppercase tracking-wider mb-3">Conceitos Mais Cobrados</h3>
                        <ul class="grid grid-cols-1 sm:grid-cols-2 gap-2">
                            {key_points_html}
                        </ul>
                    </div>

                    <!-- Fórmulas KaTeX -->
                    <div class="bg-brand-950 text-white rounded-xl p-5 shadow-inner">
                        <div class="flex items-center justify-between mb-2">
                            <span class="text-xs font-bold text-brand-300 uppercase tracking-wider flex items-center gap-1.5">
                                <i data-lucide="sigma" class="w-4 h-4"></i> Fórmulas-Chave para a Prova
                            </span>
                        </div>
                        <div class="text-sm sm:text-base font-mono overflow-x-auto py-2 text-center text-brand-100">
                            $${topic.get('formula', '')}$$
                        </div>
                    </div>
                </div>

                <!-- Exemplo Resolvido Passo a Passo -->
                <section class="bg-emerald-50/60 border border-brand-200 rounded-2xl p-6 sm:p-8 shadow-sm">
                    <h2 class="text-lg font-bold text-brand-900 mb-3 flex items-center gap-2">
                        <i data-lucide="file-check-2" class="w-5 h-5 text-brand-700"></i> Exemplo Resolvido Passo a Passo
                    </h2>
                    <div class="bg-white border border-brand-100 rounded-xl p-5 shadow-inner">
                        <p class="text-sm sm:text-base font-semibold text-gray-800 mb-3">{problem_txt}</p>
                        <div class="text-xs sm:text-sm text-gray-700 leading-relaxed whitespace-pre-line border-t border-gray-100 pt-3">
                            <strong class="text-brand-800 block mb-1">Resolução Detalhada:</strong>
                            {sol_txt}
                        </div>
                    </div>
                </section>

                <!-- Exercícios de Fixação -->
                <section class="bg-white border border-gray-200 rounded-2xl p-6 sm:p-8 shadow-sm">
                    <div class="flex items-center justify-between mb-6 pb-4 border-b border-gray-100">
                        <div>
                            <h2 class="text-xl font-bold text-brand-800 flex items-center gap-2">
                                <i data-lucide="list-checks" class="w-6 h-6 text-brand-600"></i> Questões e Exercícios
                            </h2>
                            <p class="text-xs text-gray-500 mt-1">Resolva as questões para fixar o conteúdo. Suas respostas são salvas automaticamente.</p>
                        </div>
                        <span class="text-xs font-semibold px-2.5 py-1 rounded-full bg-brand-50 text-brand-700 border border-brand-200">
                            {len(topic.get('questions', []))} Questões
                        </span>
                    </div>

                    {''.join(questions_html)}
                </section>

                <!-- Navegação Inferior -->
                <div class="flex flex-wrap items-center justify-between gap-4 pt-4 border-t border-gray-200">
                    {''.join(nav_buttons)}
                </div>

            </div>

            <!-- Sidebar Lateral (1 Coluna) -->
            <div class="lg:col-span-1 space-y-6">
                <div class="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm sticky top-24">
                    <div class="flex items-center justify-between mb-4 pb-3 border-b border-gray-100">
                        <div>
                            <span class="text-xs font-bold text-brand-700 uppercase tracking-wider block">Navegação do Bloco</span>
                            <h3 class="text-sm font-extrabold text-gray-900 truncate">{block['title']}</h3>
                        </div>
                        <span class="text-xs font-semibold px-2 py-0.5 rounded-full bg-gray-100 text-gray-600">
                            {idx + 1}/{len(topics)}
                        </span>
                    </div>

                    <div class="space-y-1 custom-scrollbar max-h-[60vh] overflow-y-auto pr-1">
                        {''.join(sidebar_items)}
                    </div>

                    <div class="mt-5 pt-4 border-t border-gray-100">
                        <a href="./index.html" class="w-full bg-brand-50 hover:bg-brand-100 text-brand-800 font-semibold py-2 px-3 rounded-xl text-xs transition flex items-center justify-center gap-1.5">
                            <i data-lucide="layout-grid" class="w-3.5 h-3.5"></i> Visão Geral do Bloco
                        </a>
                    </div>
                </div>
            </div>

        </div>
    </main>

{get_footer(rel_root="..", is_exam=False)}

    <script>
        document.addEventListener('DOMContentLoaded', () => {{
            initQuestionStates('{t_id}', '{b_id}');
            updateTopicDoneButtonUI('{t_id}');
        }});
    </script>
</body>
</html>
"""
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(page_html)

    print(f"Generated all {total_subtopics} subtopic and exam pages successfully!")

# ==============================================================================
# 5. GERAÇÃO DE PÁGINAS DE VISÃO GERAL DOS BLOCOS
# ==============================================================================
def build_block_overview_pages():
    print(f"\n--- Generating {len(math_data)} Block Overview Pages ---")

    for b_id, block in math_data.items():
        folder = get_block_folder(b_id, block)
        os.makedirs(folder, exist_ok=True)
        topics = block["topics"]
        target_path = os.path.join(folder, "index.html")
        first_topic = topics[0]
        is_exam = is_exam_block(b_id, block)

        if is_exam:
            # ---------------- MODO ESCURO-AZUL PARA BLOCOS DE PROVAS ----------------
            topic_cards = []
            for idx, topic in enumerate(topics):
                t_id = topic["id"]
                title = topic["title"]
                filename = topic["filename"]
                q_count = len(topic.get("questions", []))
                summary = topic.get("summary", "")
                
                pdf_info = resolve_pdf_link(topic, rel_root="..")
                pdf_btn = ""
                if pdf_info:
                    btn_label = "PDF Drive" if pdf_info["is_drive"] else "PDF Oficial"
                    pdf_btn = f"""
                        <a href="{pdf_info['url']}" {pdf_info['attrs']} class="bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold px-3 py-2 rounded-xl text-xs transition flex items-center gap-1.5 border border-slate-700" title="{pdf_info['title']}">
                            <i data-lucide="{pdf_info['icon']}" class="w-3.5 h-3.5 text-sky-400"></i> {btn_label}
                        </a>
                    """

                topic_cards.append(f"""
                    <div class="bg-slate-900/90 border border-slate-800 hover:border-blue-500/50 rounded-3xl p-6 shadow-xl hover-card flex flex-col justify-between text-slate-100 transition" data-topic-id="{t_id}">
                        <div>
                            <div class="flex items-center justify-between mb-3">
                                <span class="text-xs font-bold text-sky-300 bg-blue-950/80 px-2.5 py-1 rounded-lg border border-blue-800/60">
                                    Edição {idx + 1:02d}
                                </span>
                                <span id="status-badge-{t_id}" class="text-xs font-medium px-2 py-0.5 rounded-full bg-slate-800 text-slate-400 border border-slate-700">
                                    Pendente
                                </span>
                            </div>
                            <h3 class="text-lg font-bold text-white mb-2 leading-snug">{title}</h3>
                            <p class="text-slate-400 text-xs sm:text-sm leading-relaxed mb-4 line-clamp-2">{summary}</p>
                        </div>

                        <div class="pt-4 border-t border-slate-800 flex items-center justify-between gap-2">
                            <span class="text-xs text-slate-400 flex items-center gap-1">
                                <i data-lucide="help-circle" class="w-3.5 h-3.5 text-sky-400"></i> {q_count} Questões
                            </span>
                            <div class="flex items-center gap-2">
                                {pdf_btn}
                                <a href="./{filename}" class="bg-blue-600 hover:bg-blue-500 text-white font-bold px-4 py-2 rounded-xl text-xs transition flex items-center gap-1.5 shadow-md shadow-blue-600/20">
                                    Resolver Prova <i data-lucide="arrow-right" class="w-3.5 h-3.5"></i>
                                </a>
                            </div>
                        </div>
                    </div>
                """)

            block_page_html = f"""{get_head(f"{block['title']} | PartiuIF", rel_root="..", theme="dark-blue")}
{get_navbar(active_key=b_id, rel_root="..", is_exam=True)}

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-grow">
        <!-- Breadcrumbs -->
        <nav class="flex text-xs font-medium text-slate-400 mb-6" aria-label="Breadcrumb">
            <ol class="inline-flex items-center space-x-1 sm:space-x-2">
                <li><a href="../index.html" class="hover:text-sky-400 flex items-center gap-1"><i data-lucide="home" class="w-3.5 h-3.5"></i> Início</a></li>
                <li><span class="text-slate-600">/</span></li>
                <li><a href="../provas.html" class="hover:text-sky-400 flex items-center gap-1"><i data-lucide="archive" class="w-3.5 h-3.5"></i> Acervo de Provas</a></li>
                <li><span class="text-slate-600">/</span></li>
                <li class="text-slate-200 font-semibold">{block['title']}</li>
            </ol>
        </nav>

        <!-- Hero do Bloco de Provas -->
        <div class="gradient-hero-dark rounded-3xl p-6 sm:p-10 text-white mb-10 shadow-2xl relative overflow-hidden border border-slate-800">
            <div class="relative z-10 max-w-3xl">
                <div class="inline-flex items-center gap-2 bg-blue-500/20 border border-blue-400/30 px-3 py-1 rounded-full text-xs font-bold text-sky-300 uppercase tracking-wider mb-4">
                    <i data-lucide="award" class="w-3.5 h-3.5 text-sky-400"></i> Acervo de Provas Oficiais
                </div>
                <h1 class="text-3xl sm:text-4xl font-black tracking-tight mb-3">{block['title']}</h1>
                <p class="text-slate-300 text-sm sm:text-base leading-relaxed mb-6">{block.get('description', '')}</p>
                <div class="flex flex-wrap items-center gap-4">
                    <a href="./{first_topic['filename']}" class="bg-blue-600 hover:bg-blue-500 text-white font-extrabold px-6 py-3.5 rounded-xl text-sm transition flex items-center gap-2 shadow-lg shadow-blue-600/30">
                        Começar pela Prova 01 <i data-lucide="arrow-right" class="w-4 h-4"></i>
                    </a>
                    <a href="../provas.html" class="bg-slate-800/90 hover:bg-slate-700 text-slate-200 font-bold px-5 py-3.5 rounded-xl text-sm transition flex items-center gap-2 border border-slate-700">
                        <i data-lucide="archive" class="w-4 h-4 text-sky-400"></i> Ver Todas as Provas
                    </a>
                </div>
            </div>
        </div>

        <!-- Barra de Progresso do Bloco -->
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl mb-8">
            <div class="flex justify-between items-center text-xs font-semibold text-slate-300 mb-2">
                <span>Progresso do Bloco de Provas</span>
                <span id="block-progress-txt-{b_id}" class="text-sky-400 font-bold">0% (0/{len(topics)})</span>
            </div>
            <div class="w-full bg-slate-800 rounded-full h-2.5 overflow-hidden">
                <div id="block-progress-bar-{b_id}" class="bg-blue-600 h-full w-0 transition-all duration-500"></div>
            </div>
        </div>

        <!-- Grade de Provas -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {''.join(topic_cards)}
        </div>
    </main>

{get_footer(rel_root="..", is_exam=True)}

    <script>
        document.addEventListener('DOMContentLoaded', () => {{
            updateGlobalProgress();
        }});
    </script>
</body>
</html>
"""
        else:
            # ---------------- MODO VERDE PADRÃO PARA BLOCOS TEÓRICOS ----------------
            topic_cards = []
            for idx, topic in enumerate(topics):
                t_id = topic["id"]
                title = topic["title"]
                filename = topic["filename"]
                q_count = len(topic.get("questions", []))
                bncc = topic.get("bncc", "Revisão Geral")
                summary = topic.get("summary", "")

                topic_cards.append(f"""
                    <div class="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm hover-card flex flex-col justify-between" data-topic-id="{t_id}">
                        <div>
                            <div class="flex items-center justify-between mb-3">
                                <span class="text-xs font-bold text-brand-700 bg-brand-50 px-2.5 py-1 rounded-lg border border-brand-100">
                                    Tópico {idx + 1:02d}
                                </span>
                                <span id="status-badge-{t_id}" class="text-xs font-medium px-2 py-0.5 rounded-full bg-gray-100 text-gray-600 border border-gray-200">
                                    Pendente
                                </span>
                            </div>
                            <h3 class="text-lg font-bold text-gray-900 mb-1.5">{title}</h3>
                            <div class="mb-3">
                                <span class="text-xs font-semibold text-gray-500 bg-gray-50 px-2 py-0.5 rounded border border-gray-200">
                                    BNCC: {bncc}
                                </span>
                            </div>
                            <p class="text-gray-600 text-xs sm:text-sm leading-relaxed mb-4 line-clamp-2">{summary}</p>
                        </div>

                        <div class="pt-4 border-t border-gray-100 flex items-center justify-between gap-2">
                            <span class="text-xs text-gray-500 flex items-center gap-1">
                                <i data-lucide="help-circle" class="w-3.5 h-3.5 text-brand-600"></i> {q_count} Questões
                            </span>
                            <div class="flex items-center gap-2">
                                <a href="./{filename}" class="bg-brand-600 hover:bg-brand-700 text-white font-semibold px-4 py-2 rounded-xl text-xs transition flex items-center gap-1.5 shadow-sm">
                                    Estudar <i data-lucide="arrow-right" class="w-3.5 h-3.5"></i>
                                </a>
                            </div>
                        </div>
                    </div>
                """)

            block_page_html = f"""{get_head(f"{block['title']} | PartiuIF", rel_root="..", theme="green")}
{get_navbar(active_key=b_id, rel_root="..", is_exam=False)}

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-grow">
        <!-- Breadcrumbs -->
        <nav class="flex text-xs font-medium text-gray-500 mb-6" aria-label="Breadcrumb">
            <ol class="inline-flex items-center space-x-1 sm:space-x-2">
                <li><a href="../index.html" class="hover:text-brand-700 flex items-center gap-1"><i data-lucide="home" class="w-3.5 h-3.5"></i> Início</a></li>
                <li><span class="text-gray-400">/</span></li>
                <li class="text-gray-800 font-semibold">{block['title']}</li>
            </ol>
        </nav>

        <!-- Hero do Bloco Teórico -->
        <div class="bg-gradient-to-r from-brand-800 to-brand-950 rounded-3xl p-6 sm:p-10 text-white mb-10 shadow-xl relative overflow-hidden">
            <div class="relative z-10 max-w-3xl">
                <div class="inline-flex items-center gap-2 bg-brand-700/60 border border-brand-500/40 px-3 py-1 rounded-full text-xs font-bold text-brand-200 uppercase tracking-wider mb-4">
                    <i data-lucide="{block.get('icon', 'book')}" class="w-3.5 h-3.5 text-brand-300"></i> Eixo Temático
                </div>
                <h1 class="text-3xl sm:text-4xl font-extrabold tracking-tight mb-3">{block['title']}</h1>
                <p class="text-brand-100 text-sm sm:text-base leading-relaxed mb-6">{block.get('description', '')}</p>
                <div class="flex flex-wrap items-center gap-4">
                    <a href="./{first_topic['filename']}" class="bg-white hover:bg-brand-50 text-brand-900 font-bold px-6 py-3 rounded-xl text-sm transition flex items-center gap-2 shadow-lg">
                        Começar pelo Tópico 01 <i data-lucide="arrow-right" class="w-4 h-4 text-brand-700"></i>
                    </a>
                    <a href="../simulado.html?block={b_id}" class="bg-brand-700/80 hover:bg-brand-700 text-white font-bold px-5 py-3 rounded-xl text-sm transition flex items-center gap-2 border border-brand-500/30">
                        <i data-lucide="award" class="w-4 h-4"></i> Simulado deste Bloco
                    </a>
                </div>
            </div>
        </div>

        <!-- Barra de Progresso do Bloco -->
        <div class="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm mb-8">
            <div class="flex justify-between items-center text-xs font-semibold text-gray-700 mb-2">
                <span>Progresso do Bloco</span>
                <span id="block-progress-txt-{b_id}" class="text-brand-700 font-bold">0% (0/{len(topics)})</span>
            </div>
            <div class="w-full bg-gray-100 rounded-full h-2.5 overflow-hidden">
                <div id="block-progress-bar-{b_id}" class="bg-brand-600 h-full w-0 transition-all duration-500"></div>
            </div>
        </div>

        <!-- Grade de Subtópicos -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {''.join(topic_cards)}
        </div>
    </main>

{get_footer(rel_root="..", is_exam=False)}

    <script>
        document.addEventListener('DOMContentLoaded', () => {{
            updateGlobalProgress();
        }});
    </script>
</body>
</html>
"""
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(block_page_html)

    print(f"Generated all {len(math_data)} block overview pages successfully!")

# ==============================================================================
# 6. GERAÇÃO DA HOMEPAGE (index.html) - PARTE 1 (TEORIA & EIXOS TEMÁTICOS)
# ==============================================================================
def build_homepage():
    print("\n--- Generating Homepage (index.html) ---")

    home_block_cards = []
    all_topics_directory = []

    for b_id, block in theory_blocks_data.items():
        folder = get_block_folder(b_id, block)
        topics = block["topics"]
        
        # Preview dos 3 primeiros tópicos
        preview_links = []
        for t in topics[:3]:
            preview_links.append(f"""
                <a href="./{folder}/{t['filename']}" class="flex items-center justify-between py-1.5 px-2 rounded-lg text-xs text-gray-700 hover:bg-brand-50 hover:text-brand-900 transition">
                    <span class="truncate pr-2">• {t['title']}</span>
                    <i data-lucide="arrow-right" class="w-3 h-3 text-brand-600 flex-shrink-0"></i>
                </a>
            """)

        home_block_cards.append(f"""
            <div class="bg-white border border-gray-200 rounded-3xl p-6 sm:p-7 shadow-sm hover-card flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between mb-4">
                        <div class="w-12 h-12 bg-brand-100 text-brand-800 rounded-2xl flex items-center justify-center font-bold shadow-inner">
                            <i data-lucide="{block.get('icon', 'book')}" class="w-6 h-6 text-brand-700"></i>
                        </div>
                        <span class="text-xs font-bold px-3 py-1 rounded-full bg-brand-50 text-brand-700 border border-brand-200">
                            {len(topics)} Subtópicos
                        </span>
                    </div>
                    
                    <h3 class="text-xl font-extrabold text-gray-900 mb-2">{block['title']}</h3>
                    <p class="text-gray-600 text-xs sm:text-sm leading-relaxed mb-5">{block.get('description', '')}</p>

                    <div class="mb-5 bg-gray-50 border border-gray-100 p-3 rounded-xl">
                        <div class="flex justify-between text-xs text-gray-500 mb-1.5 font-medium">
                            <span>Progresso do Bloco</span>
                            <span id="block-progress-txt-{b_id}" class="font-bold text-brand-700">0%</span>
                        </div>
                        <div class="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
                            <div id="block-progress-bar-{b_id}" class="bg-brand-600 h-full w-0 transition-all duration-500"></div>
                        </div>
                    </div>

                    <div class="space-y-1 mb-5">
                        <span class="text-[11px] font-bold text-gray-400 uppercase tracking-wider block mb-1">Destaques:</span>
                        {''.join(preview_links)}
                    </div>
                </div>

                <div class="pt-4 border-t border-gray-100">
                    <a href="./{folder}/index.html" class="w-full bg-brand-50 hover:bg-brand-100 text-brand-900 font-bold py-2.5 px-4 rounded-xl text-xs sm:text-sm transition flex items-center justify-center gap-2">
                        Acessar Bloco Completo <i data-lucide="arrow-right" class="w-4 h-4"></i>
                    </a>
                </div>
            </div>
        """)

        # Diretório completo do bloco para home
        block_topic_links = []
        for t_idx, t in enumerate(topics):
            block_topic_links.append(f"""
                <a href="./{folder}/{t['filename']}" class="group p-3 rounded-xl border border-gray-100 hover:border-brand-300 hover:bg-brand-50/50 transition flex items-center justify-between bg-white">
                    <div class="flex items-center gap-2.5 min-w-0">
                        <span class="text-xs font-bold text-gray-400 group-hover:text-brand-700 flex-shrink-0">{t_idx + 1:02d}.</span>
                        <span class="text-xs sm:text-sm font-semibold text-gray-800 group-hover:text-brand-900 truncate">{t['title']}</span>
                    </div>
                    <i data-lucide="chevron-right" class="w-4 h-4 text-gray-300 group-hover:text-brand-600 flex-shrink-0"></i>
                </a>
            """)

        all_topics_directory.append(f"""
            <div class="mb-8 bg-white border border-gray-200 rounded-2xl p-5 sm:p-6 shadow-sm">
                <div class="flex flex-col sm:flex-row justify-between sm:items-center gap-2 mb-4 pb-3 border-b border-gray-100">
                    <div class="flex items-center gap-3">
                        <div class="w-8 h-8 rounded-lg bg-brand-100 text-brand-800 flex items-center justify-center font-bold text-sm">
                            {b_id}
                        </div>
                        <h3 class="text-base sm:text-lg font-extrabold text-gray-900">{block['title']}</h3>
                    </div>
                    <a href="./{folder}/index.html" class="text-xs font-bold text-brand-700 hover:text-brand-800 flex items-center gap-1">
                        Ver detalhes <i data-lucide="arrow-right" class="w-3.5 h-3.5"></i>
                    </a>
                </div>
                <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2.5">
                    {''.join(block_topic_links)}
                </div>
            </div>
        """)

    ifce_n = len(math_data.get("6", {}).get("topics", []))
    ifsc_n = len(math_data.get("5", {}).get("topics", []))
    ifsp_n = len(math_data.get("7", {}).get("topics", []))

    home_page_html = f"""{get_head("PartiuIF - Plataforma de Matemática para Institutos Federais", rel_root=".", theme="green")}
{get_navbar(active_key="home", rel_root=".", is_exam=False)}

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-grow">
        
        <!-- Hero Principal -->
        <div class="gradient-hero rounded-3xl p-6 sm:p-12 text-white mb-10 shadow-2xl relative overflow-hidden">
            <div class="relative z-10 max-w-3xl">
                <span class="bg-brand-500/30 text-brand-200 border border-brand-400/30 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider mb-4 inline-flex items-center gap-1.5">
                    <i data-lucide="sparkles" class="w-3.5 h-3.5 text-brand-300"></i> Parte 1: Teoria & Eixos Temáticos BNCC
                </span>
                
                <h1 class="text-3xl sm:text-5xl font-extrabold tracking-tight mb-4 leading-tight">
                    Matriz de Referência IF: Matemática
                </h1>
                
                <p class="text-brand-100 text-sm sm:text-base mb-8 leading-relaxed">
                    Preparação modular completa para o Exame de Classificação dos Institutos Federais. Cada subtópico possui sua própria página com teoria detalhada, fórmulas KaTeX, exemplos resolvidos e {total_theory_questions} exercícios com auto-salvamento.
                </p>

                <div class="flex flex-wrap items-center gap-4">
                    <a href="./simulado.html" class="bg-white hover:bg-brand-50 text-brand-900 font-extrabold px-6 py-3.5 rounded-2xl text-sm transition flex items-center gap-2.5 shadow-lg hover:scale-102">
                        <i data-lucide="award" class="w-5 h-5 text-brand-700"></i> Iniciar Simulado Geral
                    </a>
                    <a href="./provas.html" class="bg-gradient-to-r from-blue-600 to-indigo-700 hover:from-blue-500 hover:to-indigo-600 text-white font-extrabold px-6 py-3.5 rounded-2xl text-sm transition flex items-center gap-2 border border-blue-400/40 shadow-lg">
                        <i data-lucide="file-check" class="w-5 h-5 text-sky-300"></i> Acessar Banco de Provas ({total_official_exams})
                    </a>
                </div>
            </div>
        </div>

        <!-- Dashboard de Status Rápido (4 Métricas da Teoria) -->
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-10">
            <div class="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm flex items-center gap-4">
                <div class="w-12 h-12 rounded-xl bg-brand-100 flex items-center justify-center text-brand-700 flex-shrink-0">
                    <i data-lucide="check-circle" class="w-6 h-6"></i>
                </div>
                <div>
                    <span class="text-xs text-gray-500 font-medium block">Tópicos Concluídos</span>
                    <strong id="global-completed-count" class="text-xl font-black text-gray-900">0/{total_subtopics}</strong>
                </div>
            </div>

            <div class="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm flex items-center gap-4">
                <div class="w-12 h-12 rounded-xl bg-emerald-100 flex items-center justify-center text-emerald-700 flex-shrink-0">
                    <i data-lucide="trending-up" class="w-6 h-6"></i>
                </div>
                <div>
                    <span class="text-xs text-gray-500 font-medium block">Progresso Geral</span>
                    <strong id="global-percent" class="text-xl font-black text-emerald-800">0%</strong>
                </div>
            </div>

            <div class="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm flex items-center gap-4">
                <div class="w-12 h-12 rounded-xl bg-blue-100 flex items-center justify-center text-blue-700 flex-shrink-0">
                    <i data-lucide="help-circle" class="w-6 h-6"></i>
                </div>
                <div>
                    <span class="text-xs text-gray-500 font-medium block">Questões Salvas</span>
                    <strong id="global-answered-questions" class="text-xl font-black text-blue-900">0/{total_questions}</strong>
                </div>
            </div>

            <div class="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm flex items-center gap-4">
                <div class="w-12 h-12 rounded-xl bg-purple-100 flex items-center justify-center text-purple-700 flex-shrink-0">
                    <i data-lucide="file-text" class="w-6 h-6"></i>
                </div>
                <div>
                    <span class="text-xs text-gray-500 font-medium block">Provas Oficiais</span>
                    <strong id="global-official-exams" class="text-xl font-black text-purple-900">{total_official_exams} Edições</strong>
                </div>
            </div>
        </div>

        <!-- Busca Rápida de Subtópicos -->
        <div class="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm mb-12">
            <div class="flex flex-col sm:flex-row justify-between sm:items-center gap-4 mb-4">
                <div>
                    <h3 class="text-lg font-bold text-gray-900 flex items-center gap-2">
                        <i data-lucide="search" class="w-5 h-5 text-brand-600"></i> Localizador Rápido de Tópicos
                    </h3>
                    <p class="text-xs text-gray-500">Digite um tema (ex: Pitágoras, Frações, Áreas, Probabilidade) para acessar diretamente.</p>
                </div>
            </div>
            
            <div class="relative">
                <input type="text" id="topic-search-input" placeholder="Digite para filtrar subtópicos de teoria..." class="w-full bg-gray-50 border border-gray-300 rounded-xl px-4 py-3 pl-11 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 focus:bg-white transition">
                <i data-lucide="search" class="w-5 h-5 text-gray-400 absolute left-3.5 top-3.5"></i>
            </div>
            
            <div id="search-results-container" class="hidden mt-4 pt-4 border-t border-gray-100 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                <!-- Preenchido dinamicamente pelo módulo app.js -->
            </div>
        </div>

        <!-- Grade dos Blocos de Conteúdo Teórico -->
        <section id="blocos" class="mb-14">
            <div class="flex flex-col sm:flex-row justify-between sm:items-center gap-4 mb-6">
                <div>
                    <h2 class="text-2xl font-extrabold text-gray-900 flex items-center gap-2 border-l-4 border-brand-600 pl-3">
                        Eixos Temáticos de Conteúdo (Parte 1)
                    </h2>
                    <p class="text-xs sm:text-sm text-gray-500 mt-1 pl-3">Os {len(theory_blocks_data)} eixos fundamentais da BNCC com teoria, resoluções passo a passo e simulados.</p>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 xl:grid-cols-4 gap-6">
                {''.join(home_block_cards)}
            </div>
        </section>

        <!-- Diretório Completo de Todos os Subtópicos Teóricos -->
        <section class="mb-14">
            <div class="mb-6">
                <h2 class="text-2xl font-extrabold text-gray-900 flex items-center gap-2 border-l-4 border-brand-600 pl-3">
                    Diretório Completo de Subtópicos ({total_theory_subtopics} Páginas)
                </h2>
                <p class="text-xs sm:text-sm text-gray-500 mt-1 pl-3">Acesse cada página individual para estudar e resolver as questões com auto-salvamento.</p>
            </div>

            {''.join(all_topics_directory)}
        </section>

        <!-- SEÇÃO PARTE 2: ACERVO DE PROVAS OFICIAIS (FIM DA PARTE 1) -->
        <section class="mt-16 mb-10 relative overflow-hidden rounded-3xl bg-gradient-to-br from-slate-950 via-slate-900 to-blue-950 border-2 border-blue-500/30 p-6 sm:p-12 text-white shadow-2xl">
            <div class="absolute -right-16 -bottom-16 w-96 h-96 bg-blue-600/10 rounded-full blur-3xl pointer-events-none"></div>
            <div class="relative z-10">
                <div class="inline-flex items-center gap-2 bg-blue-500/20 text-sky-300 border border-blue-400/30 text-xs font-extrabold px-3.5 py-1.5 rounded-full uppercase tracking-wider mb-5">
                    <i data-lucide="award" class="w-4 h-4 text-sky-400"></i> Parte 2 da Plataforma • Modo Escuro-Azul
                </div>
                <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
                    <div class="lg:col-span-8 space-y-4">
                        <h2 class="text-3xl sm:text-4xl font-black tracking-tight leading-tight">
                            Banco de Provas Oficiais dos <span class="text-transparent bg-clip-text bg-gradient-to-r from-sky-400 to-blue-300">Institutos Federais</span>
                        </h2>
                        <p class="text-slate-300 text-sm sm:text-base leading-relaxed max-w-2xl">
                            Pratique em um ambiente imersivo com mais de <strong>{total_official_exams} cadernos oficiais</strong> do <strong>IFCE</strong>, <strong>IFSC</strong> e <strong>IFSP</strong>. Resolva as questões com gabarito inteligente e resoluções completas KaTeX, ou faça o <strong>download direto dos cadernos originais em PDF</strong> para simular as condições reais do exame.
                        </p>
                        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2 max-w-lg">
                            <div class="bg-slate-900/90 border border-slate-800 p-3 rounded-2xl text-center">
                                <span class="text-xl sm:text-2xl font-black text-sky-400 block">{ifce_n}</span>
                                <span class="text-[11px] text-slate-400 uppercase font-bold">Provas IFCE</span>
                            </div>
                            <div class="bg-slate-900/90 border border-slate-800 p-3 rounded-2xl text-center">
                                <span class="text-xl sm:text-2xl font-black text-indigo-400 block">{ifsc_n}</span>
                                <span class="text-[11px] text-slate-400 uppercase font-bold">Provas IFSC</span>
                            </div>
                            <div class="bg-slate-900/90 border border-slate-800 p-3 rounded-2xl text-center">
                                <span class="text-xl sm:text-2xl font-black text-amber-400 block">{ifsp_n}</span>
                                <span class="text-[11px] text-slate-400 uppercase font-bold">Provas IFSP</span>
                            </div>
                            <div class="bg-slate-900/90 border border-slate-800 p-3 rounded-2xl text-center">
                                <span class="text-xl sm:text-2xl font-black text-emerald-400 block">100%</span>
                                <span class="text-[11px] text-slate-400 uppercase font-bold">Com PDFs</span>
                            </div>
                        </div>
                    </div>
                    <div class="lg:col-span-4 flex flex-col gap-3 justify-center">
                        <a href="./provas.html" class="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-extrabold px-6 py-4 rounded-2xl text-center text-sm sm:text-base shadow-xl hover:shadow-blue-500/25 transition flex items-center justify-center gap-2 group">
                            <span>Acessar Acervo de Provas (Parte 2)</span>
                            <i data-lucide="arrow-right" class="w-5 h-5 group-hover:translate-x-1 transition-transform"></i>
                        </a>
                        <a href="./provas.html#catalogo-provas" class="bg-slate-800/80 hover:bg-slate-800 text-slate-200 border border-slate-700 font-semibold px-5 py-3 rounded-xl text-center text-xs sm:text-sm transition flex items-center justify-center gap-2">
                            <i data-lucide="download" class="w-4 h-4 text-sky-400"></i> Baixar Cadernos Oficiais em PDF
                        </a>
                    </div>
                </div>
            </div>
        </section>

    </main>

{get_footer(rel_root=".", is_exam=False)}

</body>
</html>
"""
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(home_page_html)

    print("Generated homepage index.html successfully!")

# ==============================================================================
# 7. GERAÇÃO DO HUB DE PROVAS (provas.html) - PARTE 2 (FULL DARK MODE ESCURO-AZUL)
# ==============================================================================
def build_provas_hub():
    print("\n--- Generating Provas Hub (provas.html) ---")
    
    all_exam_cards = []
    
    for b_id, block in exam_blocks_data.items():
        folder = get_block_folder(b_id, block)
        b_title = block.get("title", "")
        inst = "IFCE" if "ifce" in b_title.lower() else "IFSC" if "ifsc" in b_title.lower() else "IFSP" if "ifsp" in b_title.lower() else "IF"
        badge_style = "bg-blue-500/20 text-sky-300 border-blue-400/30" if inst == "IFCE" else "bg-indigo-500/20 text-indigo-300 border-indigo-400/30" if inst == "IFSC" else "bg-amber-500/20 text-amber-300 border-amber-400/30"
        
        for idx, topic in enumerate(block["topics"]):
            t_id = topic["id"]
            title = topic["title"]
            filename = topic["filename"]
            summary = topic.get("summary", "")
            q_count = len(topic.get("questions", []))
            pdf_filename = topic.get("pdf")
            pdf_info = resolve_pdf_link(topic, rel_root=".")
            
            pdf_btn = ""
            if pdf_info:
                btn_label = "PDF (Drive)" if pdf_info["is_drive"] else "PDF"
                pdf_btn = f"""
                    <a href="{pdf_info['url']}" {pdf_info['attrs']} class="bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 font-semibold px-3 py-2 rounded-xl text-xs transition flex items-center gap-1.5" title="{pdf_info['title']}">
                        <i data-lucide="{pdf_info['icon']}" class="w-3.5 h-3.5 text-sky-400"></i> {btn_label}
                    </a>
                """

            search_str = f"{title} {inst} {summary} {b_title}".lower()

            all_exam_cards.append(f"""
                <div class="exam-card bg-slate-900/90 border border-slate-800 hover:border-blue-500/60 rounded-3xl p-6 shadow-xl hover-card flex flex-col justify-between transition-all" data-inst="{inst}" data-search="{search_str}" data-topic-id="{t_id}">
                    <div>
                        <div class="flex items-center justify-between mb-3">
                            <span class="text-xs font-extrabold uppercase tracking-wider px-3 py-1 rounded-full border {badge_style}">
                                {inst}
                            </span>
                            <span id="status-badge-{t_id}" class="text-xs font-medium px-2.5 py-0.5 rounded-full bg-slate-800 text-slate-400 border border-slate-700">
                                Pendente
                            </span>
                        </div>
                        <h3 class="text-lg font-bold text-white mb-2 leading-snug">{title}</h3>
                        <p class="text-slate-400 text-xs sm:text-sm leading-relaxed mb-4 line-clamp-2">{summary}</p>
                    </div>

                    <div class="pt-4 border-t border-slate-800 flex items-center justify-between gap-2">
                        <span class="text-xs text-slate-400 flex items-center gap-1">
                            <i data-lucide="help-circle" class="w-3.5 h-3.5 text-sky-400"></i> {q_count} Questões
                        </span>
                        <div class="flex items-center gap-2">
                            {pdf_btn}
                            <a href="./{folder}/{filename}" class="bg-blue-600 hover:bg-blue-500 text-white font-bold px-4 py-2 rounded-xl text-xs transition flex items-center gap-1.5 shadow-md shadow-blue-600/25">
                                Resolver <i data-lucide="arrow-right" class="w-3.5 h-3.5"></i>
                            </a>
                        </div>
                    </div>
                </div>
            """)

    ifce_n = len(math_data.get("6", {}).get("topics", []))
    ifsc_n = len(math_data.get("5", {}).get("topics", []))
    ifsp_n = len(math_data.get("7", {}).get("topics", []))

    provas_hub_html = f"""{get_head("Acervo de Provas Oficiais dos Institutos Federais | PartiuIF", rel_root=".", theme="dark-blue")}
{get_navbar(active_key="provas_hub", rel_root=".", is_exam=True)}

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-grow">
        
        <!-- Breadcrumbs -->
        <nav class="flex text-xs font-medium text-slate-400 mb-6" aria-label="Breadcrumb">
            <ol class="inline-flex items-center space-x-1 sm:space-x-2">
                <li><a href="./index.html" class="hover:text-sky-400 flex items-center gap-1"><i data-lucide="home" class="w-3.5 h-3.5"></i> Início</a></li>
                <li><span class="text-slate-600">/</span></li>
                <li class="text-slate-200 font-semibold">Acervo de Provas Oficiais (Parte 2)</li>
            </ol>
        </nav>

        <!-- Hero Principal do Acervo de Provas -->
        <div class="gradient-hero-dark rounded-3xl p-6 sm:p-12 text-white mb-10 shadow-2xl relative overflow-hidden border border-slate-800">
            <div class="relative z-10 max-w-3xl">
                <span class="bg-blue-500/20 text-sky-300 border border-blue-400/30 text-xs font-extrabold px-3.5 py-1.5 rounded-full uppercase tracking-wider mb-4 inline-flex items-center gap-1.5">
                    <i data-lucide="shield-check" class="w-3.5 h-3.5 text-sky-400"></i> Acervo Oficial dos Exames de Classificação
                </span>
                
                <h1 class="text-3xl sm:text-5xl font-black tracking-tight mb-4 leading-tight">
                    Banco de Provas dos <span class="text-transparent bg-clip-text bg-gradient-to-r from-sky-400 to-blue-300">Institutos Federais</span>
                </h1>
                
                <p class="text-slate-300 text-sm sm:text-base mb-8 leading-relaxed">
                    Ambiente dedicado para simulação com os exames reais do <strong>IFCE</strong>, <strong>IFSC</strong> e <strong>IFSP</strong>. Resolva os cadernos online com resoluções KaTeX comentadas e baixe os PDFs originais para simular o tempo de prova oficial.
                </p>

                <div class="flex flex-wrap items-center gap-4">
                    <a href="#catalogo-provas" class="bg-blue-600 hover:bg-blue-500 text-white font-extrabold px-6 py-3.5 rounded-2xl text-sm transition flex items-center gap-2 shadow-lg shadow-blue-600/30">
                        <i data-lucide="layers" class="w-4 h-4"></i> Explorar as {total_official_exams} Provas
                    </a>
                    <a href="./index.html" class="bg-slate-800/90 hover:bg-slate-700 text-slate-200 font-bold px-6 py-3.5 rounded-2xl text-sm transition flex items-center gap-2 border border-slate-700">
                        <i data-lucide="arrow-left" class="w-4 h-4 text-emerald-400"></i> Voltar para Teoria (Parte 1)
                    </a>
                </div>
            </div>
        </div>

        <!-- Dashboard do Acervo (5 Métricas) -->
        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 mb-10">
            <div class="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-xl flex items-center gap-4">
                <div class="w-12 h-12 rounded-xl bg-blue-950/80 border border-blue-800/40 flex items-center justify-center text-sky-400 flex-shrink-0">
                    <i data-lucide="file-text" class="w-6 h-6"></i>
                </div>
                <div>
                    <span class="text-xs text-slate-400 font-medium block">Total de Provas</span>
                    <strong class="text-xl font-black text-white">{total_official_exams} Cadernos</strong>
                </div>
            </div>

            <div class="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-xl flex items-center gap-4">
                <div class="w-12 h-12 rounded-xl bg-blue-950/80 border border-blue-800/40 flex items-center justify-center text-sky-400 flex-shrink-0">
                    <i data-lucide="award" class="w-6 h-6"></i>
                </div>
                <div>
                    <span class="text-xs text-slate-400 font-medium block">Edições IFCE</span>
                    <strong class="text-xl font-black text-sky-400">{ifce_n} Provas</strong>
                </div>
            </div>

            <div class="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-xl flex items-center gap-4">
                <div class="w-12 h-12 rounded-xl bg-indigo-950/80 border border-indigo-800/40 flex items-center justify-center text-indigo-400 flex-shrink-0">
                    <i data-lucide="award" class="w-6 h-6"></i>
                </div>
                <div>
                    <span class="text-xs text-slate-400 font-medium block">Edições IFSC</span>
                    <strong class="text-xl font-black text-indigo-400">{ifsc_n} Provas</strong>
                </div>
            </div>

            <div class="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-xl flex items-center gap-4">
                <div class="w-12 h-12 rounded-xl bg-amber-950/80 border border-amber-800/40 flex items-center justify-center text-amber-400 flex-shrink-0">
                    <i data-lucide="award" class="w-6 h-6"></i>
                </div>
                <div>
                    <span class="text-xs text-slate-400 font-medium block">Edições IFSP</span>
                    <strong class="text-xl font-black text-amber-400">{ifsp_n} Provas</strong>
                </div>
            </div>

            <div class="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-xl flex items-center gap-4 col-span-2 md:col-span-1">
                <div class="w-12 h-12 rounded-xl bg-emerald-950/80 border border-emerald-800/40 flex items-center justify-center text-emerald-400 flex-shrink-0">
                    <i data-lucide="download-cloud" class="w-6 h-6"></i>
                </div>
                <div>
                    <span class="text-xs text-slate-400 font-medium block">Downloads em PDF</span>
                    <strong class="text-xl font-black text-emerald-400">100% Liberados</strong>
                </div>
            </div>
        </div>

        <!-- Seção de Acesso Rápido aos Blocos de Cada IF -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
            <div class="bg-slate-900/90 border border-slate-800 hover:border-blue-500/50 rounded-3xl p-6 sm:p-7 shadow-xl flex items-center justify-between transition">
                <div>
                    <div class="flex items-center gap-2 mb-2">
                        <span class="text-xs font-bold uppercase tracking-wider px-2.5 py-0.5 rounded-full bg-blue-500/20 text-sky-300 border border-blue-400/30">Ceará</span>
                        <span class="text-xs text-slate-400 font-medium">Bloco 6</span>
                    </div>
                    <h3 class="text-xl font-extrabold text-white mb-1">Provas Anteriores IFCE</h3>
                    <p class="text-slate-400 text-xs sm:text-sm">{ifce_n} edições completas com resoluções comentadas e PDFs.</p>
                </div>
                <a href="./bloco-6-provas-ifce/index.html" class="bg-blue-600 hover:bg-blue-500 text-white font-bold p-3 rounded-2xl transition shadow-lg shadow-blue-600/20 flex-shrink-0">
                    <i data-lucide="arrow-right" class="w-5 h-5"></i>
                </a>
            </div>

            <div class="bg-slate-900/90 border border-slate-800 hover:border-indigo-500/50 rounded-3xl p-6 sm:p-7 shadow-xl flex items-center justify-between transition">
                <div>
                    <div class="flex items-center gap-2 mb-2">
                        <span class="text-xs font-bold uppercase tracking-wider px-2.5 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-400/30">Santa Catarina</span>
                        <span class="text-xs text-slate-400 font-medium">Bloco 5</span>
                    </div>
                    <h3 class="text-xl font-extrabold text-white mb-1">Provas Anteriores IFSC</h3>
                    <p class="text-slate-400 text-xs sm:text-sm">{ifsc_n} edições completas com resoluções comentadas e PDFs.</p>
                </div>
                <a href="./bloco-5-provas-ifsc/index.html" class="bg-indigo-600 hover:bg-indigo-500 text-white font-bold p-3 rounded-2xl transition shadow-lg shadow-indigo-600/20 flex-shrink-0">
                    <i data-lucide="arrow-right" class="w-5 h-5"></i>
                </a>
            </div>

            <div class="bg-slate-900/90 border border-slate-800 hover:border-amber-500/50 rounded-3xl p-6 sm:p-7 shadow-xl flex items-center justify-between transition">
                <div>
                    <div class="flex items-center gap-2 mb-2">
                        <span class="text-xs font-bold uppercase tracking-wider px-2.5 py-0.5 rounded-full bg-amber-500/20 text-amber-300 border border-amber-400/30">São Paulo</span>
                        <span class="text-xs text-slate-400 font-medium">Bloco 7</span>
                    </div>
                    <h3 class="text-xl font-extrabold text-white mb-1">Provas Anteriores IFSP</h3>
                    <p class="text-slate-400 text-xs sm:text-sm">{ifsp_n} edições completas com resoluções comentadas e PDFs.</p>
                </div>
                <a href="./bloco-7-provas-ifsp/index.html" class="bg-amber-600 hover:bg-amber-500 text-white font-bold p-3 rounded-2xl transition shadow-lg shadow-amber-600/20 flex-shrink-0">
                    <i data-lucide="arrow-right" class="w-5 h-5"></i>
                </a>
            </div>
        </div>

        <!-- Seção Destacada: Pesquisa de Questões por Descritores da BNCC -->
        <section class="mb-12 bg-gradient-to-r from-blue-950/90 via-slate-900 to-indigo-950/90 border border-blue-800/50 rounded-3xl p-6 sm:p-8 shadow-2xl relative overflow-hidden">
            <div class="relative z-10">
                <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4 mb-5">
                    <div>
                        <span class="bg-emerald-500/20 text-emerald-300 border border-emerald-400/30 text-xs font-extrabold px-3 py-1 rounded-full uppercase tracking-wider mb-2.5 inline-flex items-center gap-1.5">
                            <i data-lucide="sparkles" class="w-3.5 h-3.5 text-emerald-400"></i> Banco Curricular Integrado
                        </span>
                        <h2 class="text-2xl sm:text-3xl font-black text-white">
                            Pesquisar Questões por Descritor BNCC
                        </h2>
                        <p class="text-slate-300 text-xs sm:text-sm mt-1 max-w-2xl">
                            Consulte nosso banco com todas as <strong>{total_exam_questions} questões oficiais</strong> catalogadas pelas habilidades da Base Nacional Comum Curricular (6º ao 9º ano).
                        </p>
                    </div>
                    <a href="./pesquisa.html" class="bg-emerald-600 hover:bg-emerald-500 text-white font-extrabold px-5 py-3 rounded-xl text-xs sm:text-sm transition flex items-center gap-2 shadow-lg shadow-emerald-600/25 flex-shrink-0 self-start lg:self-center">
                        <i data-lucide="search" class="w-4 h-4"></i> Abrir Motor de Busca
                    </a>
                </div>

                <!-- Formulário de Pesquisa Direta -->
                <form action="./pesquisa.html" method="GET" class="flex flex-col sm:flex-row items-center gap-3 mb-5">
                    <div class="relative flex-grow w-full">
                        <input type="text" name="q" placeholder="Digite uma habilidade ou tema (ex: EF09MA06, Teorema de Pitágoras, Porcentagem, Volume)..." class="w-full bg-slate-950/90 border border-slate-700 rounded-2xl px-4 py-3.5 pl-11 text-sm text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-500 transition shadow-inner">
                        <i data-lucide="search" class="w-5 h-5 text-slate-400 absolute left-3.5 top-3.5"></i>
                    </div>
                    <button type="submit" class="w-full sm:w-auto bg-blue-600 hover:bg-blue-500 text-white font-bold px-6 py-3.5 rounded-2xl text-sm transition flex items-center justify-center gap-2 shadow-md shadow-blue-600/25 flex-shrink-0">
                        Buscar Questões <i data-lucide="arrow-right" class="w-4 h-4"></i>
                    </button>
                </form>

                <!-- Tags / Atalhos de Descritores Populares -->
                <div>
                    <span class="text-xs font-bold text-slate-400 block mb-2">Atalhos rápidos por habilidades frequentes:</span>
                    <div class="flex flex-wrap gap-2">
                        <a href="./pesquisa.html?bncc=EF09MA09" class="px-2.5 py-1 rounded-lg text-xs bg-slate-900 hover:bg-slate-800 text-sky-300 border border-slate-700 transition flex items-center gap-1">
                            <i data-lucide="bookmark" class="w-3 h-3 text-emerald-400"></i> EF09MA09 (Eq. 2º Grau)
                        </a>
                        <a href="./pesquisa.html?bncc=EF08MA04" class="px-2.5 py-1 rounded-lg text-xs bg-slate-900 hover:bg-slate-800 text-sky-300 border border-slate-700 transition flex items-center gap-1">
                            <i data-lucide="bookmark" class="w-3 h-3 text-emerald-400"></i> EF08MA04 (Porcentagem)
                        </a>
                        <a href="./pesquisa.html?bncc=EF09MA14" class="px-2.5 py-1 rounded-lg text-xs bg-slate-900 hover:bg-slate-800 text-sky-300 border border-slate-700 transition flex items-center gap-1">
                            <i data-lucide="bookmark" class="w-3 h-3 text-emerald-400"></i> EF09MA14 (Pitágoras/Tales)
                        </a>
                        <a href="./pesquisa.html?bncc=EF08MA19" class="px-2.5 py-1 rounded-lg text-xs bg-slate-900 hover:bg-slate-800 text-sky-300 border border-slate-700 transition flex items-center gap-1">
                            <i data-lucide="bookmark" class="w-3 h-3 text-emerald-400"></i> EF08MA19 (Áreas Planas)
                        </a>
                        <a href="./pesquisa.html?bncc=EF09MA19" class="px-2.5 py-1 rounded-lg text-xs bg-slate-900 hover:bg-slate-800 text-sky-300 border border-slate-700 transition flex items-center gap-1">
                            <i data-lucide="bookmark" class="w-3 h-3 text-emerald-400"></i> EF09MA19 (Volume Cilindros)
                        </a>
                        <a href="./pesquisa.html?bncc=EF08MA08" class="px-2.5 py-1 rounded-lg text-xs bg-slate-900 hover:bg-slate-800 text-sky-300 border border-slate-700 transition flex items-center gap-1">
                            <i data-lucide="bookmark" class="w-3 h-3 text-emerald-400"></i> EF08MA08 (Sistemas 1º Grau)
                        </a>
                        <a href="./pesquisa.html?bncc=EF07MA18" class="px-2.5 py-1 rounded-lg text-xs bg-slate-900 hover:bg-slate-800 text-sky-300 border border-slate-700 transition flex items-center gap-1">
                            <i data-lucide="bookmark" class="w-3 h-3 text-emerald-400"></i> EF07MA18 (Equações 1º Grau)
                        </a>
                        <a href="./pesquisa.html?bncc=EF07MA01" class="px-2.5 py-1 rounded-lg text-xs bg-slate-900 hover:bg-slate-800 text-sky-300 border border-slate-700 transition flex items-center gap-1">
                            <i data-lucide="bookmark" class="w-3 h-3 text-emerald-400"></i> EF07MA01 (MMC / MDC)
                        </a>
                        <a href="./pesquisa.html?bncc=EF09MA05" class="px-2.5 py-1 rounded-lg text-xs bg-slate-900 hover:bg-slate-800 text-sky-300 border border-slate-700 transition flex items-center gap-1">
                            <i data-lucide="bookmark" class="w-3 h-3 text-emerald-400"></i> EF09MA05 (Juros Compostos)
                        </a>
                        <a href="./pesquisa.html?bncc=EF08MA22" class="px-2.5 py-1 rounded-lg text-xs bg-slate-900 hover:bg-slate-800 text-sky-300 border border-slate-700 transition flex items-center gap-1">
                            <i data-lucide="bookmark" class="w-3 h-3 text-emerald-400"></i> EF08MA22 (Probabilidade)
                        </a>
                    </div>
                </div>
            </div>
        </section>

        <!-- Barra de Ferramentas / Filtros Interativos do Catálogo -->
        <section id="catalogo-provas" class="mb-12">
            <div class="flex flex-col md:flex-row justify-between md:items-center gap-4 mb-6 pb-4 border-b border-slate-800">
                <div>
                    <h2 class="text-2xl font-black text-white flex items-center gap-2 border-l-4 border-blue-500 pl-3">
                        Catálogo Completo de Provas ({total_official_exams})
                    </h2>
                    <p class="text-xs sm:text-sm text-slate-400 mt-1 pl-3">Filtre por instituição ou digite o ano para encontrar rapidamente o caderno desejado.</p>
                </div>

                <!-- Filtros por Instituição -->
                <div class="flex flex-wrap items-center gap-2 bg-slate-900 p-1.5 rounded-2xl border border-slate-800">
                    <button onclick="filterExams('all')" id="btn-filter-all" class="filter-btn px-4 py-1.5 rounded-xl text-xs font-bold transition bg-blue-600 text-white shadow">
                        Todos ({total_official_exams})
                    </button>
                    <button onclick="filterExams('IFCE')" id="btn-filter-ifce" class="filter-btn px-4 py-1.5 rounded-xl text-xs font-semibold text-slate-400 hover:text-white transition">
                        IFCE ({ifce_n})
                    </button>
                    <button onclick="filterExams('IFSC')" id="btn-filter-ifsc" class="filter-btn px-4 py-1.5 rounded-xl text-xs font-semibold text-slate-400 hover:text-white transition">
                        IFSC ({ifsc_n})
                    </button>
                    <button onclick="filterExams('IFSP')" id="btn-filter-ifsp" class="filter-btn px-4 py-1.5 rounded-xl text-xs font-semibold text-slate-400 hover:text-white transition">
                        IFSP ({ifsp_n})
                    </button>
                </div>
            </div>

            <!-- Campo de Busca Instantânea -->
            <div class="relative mb-8">
                <input type="text" id="exam-search-input" placeholder="Buscar prova por ano ou termo (ex: 2024, 2022, Integrado, Tabuleiro)..." class="w-full bg-slate-900 border border-slate-800 rounded-2xl px-4 py-3.5 pl-11 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition shadow-inner">
                <i data-lucide="search" class="w-5 h-5 text-slate-500 absolute left-3.5 top-3.5"></i>
            </div>

            <!-- Grade de Provas -->
            <div id="exams-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {''.join(all_exam_cards)}
            </div>

            <div id="no-exams-found" class="hidden p-8 text-center bg-slate-900 border border-slate-800 rounded-2xl text-slate-400 text-sm">
                Nenhuma prova encontrada com os filtros selecionados.
            </div>
        </section>

    </main>

{get_footer(rel_root=".", is_exam=True)}

    <!-- Script Dedicado de Filtragem Interativa de Provas -->
    <script>
        let currentInstFilter = 'all';

        function filterExams(inst) {{
            currentInstFilter = inst;
            
            // Atualiza botões
            const buttons = document.querySelectorAll('.filter-btn');
            buttons.forEach(b => {{
                b.className = "filter-btn px-4 py-1.5 rounded-xl text-xs font-semibold text-slate-400 hover:text-white transition";
            }});
            const activeBtn = document.getElementById(`btn-filter-${{inst.toLowerCase()}}`);
            if (activeBtn) {{
                activeBtn.className = "filter-btn px-4 py-1.5 rounded-xl text-xs font-bold transition bg-blue-600 text-white shadow";
            }}

            applyFilters();
        }}

        function applyFilters() {{
            const searchVal = (document.getElementById('exam-search-input').value || '').toLowerCase().trim();
            const cards = document.querySelectorAll('.exam-card');
            let visibleCount = 0;

            cards.forEach(card => {{
                const cardInst = card.getAttribute('data-inst');
                const cardSearch = card.getAttribute('data-search') || '';

                const matchesInst = (currentInstFilter === 'all' || cardInst === currentInstFilter);
                const matchesSearch = (!searchVal || cardSearch.includes(searchVal));

                if (matchesInst && matchesSearch) {{
                    card.style.display = 'flex';
                    visibleCount++;
                }} else {{
                    card.style.display = 'none';
                }}
            }});

            const noFound = document.getElementById('no-exams-found');
            if (noFound) {{
                if (visibleCount === 0) {{
                    noFound.classList.remove('hidden');
                }} else {{
                    noFound.classList.add('hidden');
                }}
            }}
        }}

        document.addEventListener('DOMContentLoaded', () => {{
            const searchInput = document.getElementById('exam-search-input');
            if (searchInput) {{
                searchInput.addEventListener('input', applyFilters);
            }}
            const urlParams = new URLSearchParams(window.location.search);
            const instParam = urlParams.get('inst');
            if (instParam) {{
                filterExams(instParam.toUpperCase());
            }}
            updateGlobalProgress();
        }});
    </script>
</body>
</html>
"""
    with open("provas.html", "w", encoding="utf-8") as f:
        f.write(provas_hub_html)

    print("Generated provas.html successfully!")

# ==============================================================================
# 8. GERAÇÃO DA PÁGINA DE SIMULADO (simulado.html)
# ==============================================================================
def build_simulado_page():
    print("\n--- Generating Simulado Page (simulado.html) ---")

    sim_source_radios = ["""
        <label class="cursor-pointer p-3.5 rounded-xl border border-brand-500 bg-brand-50/60 flex items-center gap-3 text-sm font-semibold text-gray-900 transition hover:border-brand-500">
            <input type="radio" name="sim-source" value="all" checked class="text-brand-600 focus:ring-brand-500">
            <span>Todos os Blocos (Geral)</span>
        </label>
    """]

    for b_id, block in math_data.items():
        sim_source_radios.append(f"""
            <label class="cursor-pointer p-3.5 rounded-xl border border-gray-200 hover:border-brand-300 flex items-center gap-3 text-sm font-medium text-gray-800 transition">
                <input type="radio" name="sim-source" value="{b_id}" class="text-brand-600 focus:ring-brand-500">
                <span>{block['title']}</span>
            </label>
        """)

    simulado_html = f"""{get_head("Simulado Geral de Matemática | PartiuIF", rel_root=".", theme="green")}
{get_navbar(active_key="simulado", rel_root=".", is_exam=False)}

    <main class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-grow">
        
        <!-- CONTAINER 1: Configuração do Simulado (Visível Inicialmente) -->
        <div id="simulado-setup" class="space-y-8">
            <div class="bg-gradient-to-r from-brand-800 to-brand-950 rounded-3xl p-6 sm:p-10 text-white shadow-xl">
                <div class="flex items-center gap-3 mb-3">
                    <div class="w-12 h-12 bg-white/10 rounded-2xl flex items-center justify-center text-brand-300 border border-white/20">
                        <i data-lucide="award" class="w-6 h-6"></i>
                    </div>
                    <span class="bg-brand-500/30 text-brand-200 border border-brand-400/30 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">
                        Treino Oficial
                    </span>
                </div>
                <h1 class="text-3xl sm:text-4xl font-extrabold tracking-tight mb-3">Simulado IF de Matemática</h1>
                <p class="text-brand-100 text-sm sm:text-base max-w-2xl leading-relaxed">
                    Personalize seu simulado com questões retiradas do banco oficial dos {len(math_data)} blocos e das {total_official_exams} provas oficiais do IFCE, IFSC e IFSP. Ao final, veja seu desempenho e a resolução comentada de cada questão.
                </p>
            </div>

            <div class="bg-white border border-gray-200 rounded-3xl p-6 sm:p-8 shadow-sm space-y-6">
                <h2 class="text-xl font-bold text-gray-900 flex items-center gap-2 border-l-4 border-brand-600 pl-3">
                    Configurações do Simulado
                </h2>

                <!-- Seleção do Eixo / Fonte -->
                <div>
                    <label class="block text-xs font-bold text-gray-700 uppercase tracking-wider mb-2">Selecione o Eixo de Conteúdo:</label>
                    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3" id="sim-source-options">
                        {''.join(sim_source_radios)}
                    </div>
                </div>

                <!-- Quantidade de Questões -->
                <div>
                    <label class="block text-xs font-bold text-gray-700 uppercase tracking-wider mb-2">Quantidade de Questões:</label>
                    <div class="grid grid-cols-3 gap-3">
                        <label class="cursor-pointer p-3 rounded-xl border border-brand-500 bg-brand-50/60 text-center font-bold text-sm text-gray-900 transition flex items-center justify-center gap-2">
                            <input type="radio" name="sim-count" value="10" checked class="text-brand-600 focus:ring-brand-500">
                            <span>10 Questões (Express)</span>
                        </label>
                        <label class="cursor-pointer p-3 rounded-xl border border-gray-200 hover:border-brand-300 text-center font-medium text-sm text-gray-800 transition flex items-center justify-center gap-2">
                            <input type="radio" name="sim-count" value="20" class="text-brand-600 focus:ring-brand-500">
                            <span>20 Questões (Padrão)</span>
                        </label>
                        <label class="cursor-pointer p-3 rounded-xl border border-gray-200 hover:border-brand-300 text-center font-medium text-sm text-gray-800 transition flex items-center justify-center gap-2">
                            <input type="radio" name="sim-count" value="30" class="text-brand-600 focus:ring-brand-500">
                            <span>30 Questões (Intensivo)</span>
                        </label>
                    </div>
                </div>

                <div class="pt-4 border-t border-gray-100 flex justify-end">
                    <button onclick="startSimulado()" class="bg-brand-600 hover:bg-brand-700 text-white font-extrabold px-8 py-3.5 rounded-xl text-sm transition flex items-center gap-2 shadow-lg">
                        <i data-lucide="play" class="w-4 h-4"></i> Iniciar Simulado Agora
                    </button>
                </div>
            </div>
        </div>

        <!-- CONTAINER 2: Execução do Simulado (Oculto Inicialmente) -->
        <div id="simulado-running" class="hidden space-y-6">
            <div class="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm flex flex-col sm:flex-row justify-between sm:items-center gap-4">
                <div>
                    <span id="sim-progress-indicator" class="text-xs font-bold text-brand-700 bg-brand-50 px-2.5 py-1 rounded-lg border border-brand-100">
                        Questão 1 de 10
                    </span>
                    <span id="sim-topic-title" class="text-xs text-gray-500 ml-2 font-medium"></span>
                </div>

                <div class="flex items-center gap-2">
                    <button onclick="confirmExitSimulado()" class="text-xs text-gray-500 hover:text-red-600 px-3 py-1.5 rounded-lg border border-gray-200 hover:border-red-200 transition">
                        Cancelar Simulado
                    </button>
                    <button onclick="finishSimulado()" class="bg-brand-600 hover:bg-brand-700 text-white font-bold px-4 py-1.5 rounded-lg text-xs transition shadow-sm">
                        Finalizar e Corrigir
                    </button>
                </div>
            </div>

            <!-- Navegador de Bolinhas das Questões -->
            <div id="sim-palette" class="bg-white border border-gray-200 rounded-2xl p-4 shadow-sm flex flex-wrap gap-2">
                <!-- Preenchido pelo módulo simulado.js -->
            </div>

            <!-- Card da Questão Atual -->
            <div id="sim-question-card" class="bg-white border border-gray-200 rounded-2xl p-6 sm:p-8 shadow-sm">
                <!-- Preenchido dinamicamente pelo módulo simulado.js -->
            </div>

            <!-- Navegação Inferior do Simulado -->
            <div class="flex items-center justify-between gap-4">
                <button id="sim-prev-btn" onclick="prevSimQuestion()" class="bg-white border border-gray-200 hover:bg-gray-50 text-gray-700 font-semibold px-5 py-2.5 rounded-xl text-sm transition flex items-center gap-2 shadow-sm">
                    <i data-lucide="arrow-left" class="w-4 h-4"></i> Anterior
                </button>
                <button id="sim-next-btn" onclick="nextSimQuestion()" class="bg-brand-600 hover:bg-brand-700 text-white font-semibold px-5 py-2.5 rounded-xl text-sm transition flex items-center gap-2 shadow-sm">
                    Próxima <i data-lucide="arrow-right" class="w-4 h-4"></i>
                </button>
            </div>
        </div>

        <!-- CONTAINER 3: Resultados e Resoluções (Oculto Inicialmente) -->
        <div id="simulado-results" class="hidden space-y-8">
            <!-- Preenchido pelo módulo simulado.js -->
        </div>

    </main>

{get_footer(rel_root=".", is_exam=False)}

    <!-- Motor Dedicado do Simulado -->
    <script src="./assets/js/simulado.js"></script>
</body>
</html>
"""
    with open("simulado.html", "w", encoding="utf-8") as f:
        f.write(simulado_html)

    print("Generated simulado.html successfully!")

def build_pesquisa_page():
    print("\n--- Generating Pesquisa BNCC Page (pesquisa.html) ---")
    
    pesquisa_html = f"""{get_head("Banco de Questões por Descritor BNCC | PartiuIF", rel_root=".", theme="dark-blue")}
{get_navbar(active_key="pesquisa", rel_root=".", is_exam=True)}

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-grow">
        
        <!-- Breadcrumbs -->
        <nav class="flex text-xs font-medium text-slate-400 mb-6" aria-label="Breadcrumb">
            <ol class="inline-flex items-center space-x-1 sm:space-x-2">
                <li><a href="./index.html" class="hover:text-sky-400 flex items-center gap-1"><i data-lucide="home" class="w-3.5 h-3.5"></i> Início</a></li>
                <li><span class="text-slate-600">/</span></li>
                <li><a href="./provas.html" class="hover:text-sky-400">Provas Oficiais</a></li>
                <li><span class="text-slate-600">/</span></li>
                <li class="text-slate-200 font-semibold">Pesquisa por Descritor BNCC</li>
            </ol>
        </nav>

        <!-- Hero Header -->
        <div class="gradient-hero-dark rounded-3xl p-6 sm:p-10 text-white mb-8 shadow-2xl relative overflow-hidden border border-slate-800">
            <div class="relative z-10 max-w-3xl">
                <span class="bg-emerald-500/20 text-emerald-300 border border-emerald-400/30 text-xs font-extrabold px-3.5 py-1.5 rounded-full uppercase tracking-wider mb-4 inline-flex items-center gap-1.5">
                    <i data-lucide="bookmark-check" class="w-3.5 h-3.5 text-emerald-400"></i> Banco Curricular de Matemática
                </span>
                
                <h1 class="text-3xl sm:text-4xl font-black tracking-tight mb-3 leading-tight">
                    Pesquisa de Questões por <span class="text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 via-sky-300 to-blue-400">Descritores BNCC</span>
                </h1>
                
                <p class="text-slate-300 text-xs sm:text-sm leading-relaxed">
                    Explore nosso acervo completo com <strong>{total_exam_questions} questões reais</strong> aplicadas nos exames de seleção do <strong>IFCE</strong>, <strong>IFSC</strong> e <strong>IFSP</strong>, todas catalogadas e associadas às habilidades oficiais da BNCC (6º ao 9º ano).
                </p>
            </div>
        </div>

        <!-- Painel de Busca e Filtros Avançados -->
        <div class="bg-slate-900/90 border border-slate-800 rounded-3xl p-6 shadow-xl mb-8 space-y-4">
            
            <!-- Campo de Busca com Confirmação (Enter ou Botão) -->
            <form id="search-form" onsubmit="event.preventDefault(); applyFilters();" class="flex flex-col sm:flex-row items-center gap-3">
                <div class="relative flex-1 w-full">
                    <input type="text" id="search-text" placeholder="Digite termos ou código BNCC e pressione Enter ou clique em Buscar (ex: EF09MA09, Pitágoras, Volume)..." class="w-full bg-slate-950 border border-slate-700 rounded-2xl px-4 py-3.5 pl-11 pr-10 text-sm text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-500 transition shadow-inner">
                    <i data-lucide="search" class="w-5 h-5 text-slate-400 absolute left-3.5 top-3.5"></i>
                    <button type="button" id="clear-search-btn" onclick="clearSearchText()" class="hidden absolute right-3.5 top-3.5 text-slate-400 hover:text-white transition p-0.5 rounded-lg" title="Limpar busca">
                        <i data-lucide="x" class="w-4 h-4"></i>
                    </button>
                </div>
                <button type="submit" id="btn-submit-search" class="w-full sm:w-auto bg-emerald-600 hover:bg-emerald-500 active:scale-95 text-white font-bold px-6 py-3.5 rounded-2xl text-sm transition flex items-center justify-center gap-2 shadow-lg shadow-emerald-600/25 flex-shrink-0 cursor-pointer">
                    <i data-lucide="search" class="w-4 h-4"></i> Buscar Questões
                </button>
            </form>

            <!-- Controles de Filtros em Grade -->
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 pt-2">
                <!-- Dropdown de Habilidade BNCC -->
                <div>
                    <label for="filter-bncc" class="block text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-1.5 flex items-center gap-1">
                        <i data-lucide="bookmark" class="w-3.5 h-3.5 text-emerald-400"></i> Habilidade BNCC
                    </label>
                    <select id="filter-bncc" onchange="applyFilters()" class="w-full bg-slate-950 border border-slate-700 rounded-xl px-3 py-2.5 text-xs text-slate-200 focus:outline-none focus:ring-2 focus:ring-emerald-500 transition">
                        <option value="">Todas as Habilidades</option>
                    </select>
                </div>

                <!-- Dropdown de Unidade Temática -->
                <div>
                    <label for="filter-unidade" class="block text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-1.5 flex items-center gap-1">
                        <i data-lucide="layers" class="w-3.5 h-3.5 text-sky-400"></i> Unidade Temática
                    </label>
                    <select id="filter-unidade" onchange="applyFilters()" class="w-full bg-slate-950 border border-slate-700 rounded-xl px-3 py-2.5 text-xs text-slate-200 focus:outline-none focus:ring-2 focus:ring-sky-500 transition">
                        <option value="">Todas as Unidades</option>
                        <option value="Álgebra">Álgebra</option>
                        <option value="Geometria">Geometria</option>
                        <option value="Números">Números</option>
                        <option value="Grandezas e Medidas">Grandezas e Medidas</option>
                        <option value="Probabilidade e Estatística">Probabilidade e Estatística</option>
                    </select>
                </div>

                <!-- Dropdown de Ano Escolar -->
                <div>
                    <label for="filter-ano" class="block text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-1.5 flex items-center gap-1">
                        <i data-lucide="calendar" class="w-3.5 h-3.5 text-indigo-400"></i> Ano Escolar
                    </label>
                    <select id="filter-ano" onchange="applyFilters()" class="w-full bg-slate-950 border border-slate-700 rounded-xl px-3 py-2.5 text-xs text-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition">
                        <option value="">Todos os Anos</option>
                        <option value="6º ano">6º ano</option>
                        <option value="7º ano">7º ano</option>
                        <option value="8º ano">8º ano</option>
                        <option value="9º ano">9º ano</option>
                    </select>
                </div>

                <!-- Dropdown de Instituto -->
                <div>
                    <label for="filter-inst" class="block text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-1.5 flex items-center gap-1">
                        <i data-lucide="building-2" class="w-3.5 h-3.5 text-amber-400"></i> Instituto Federal
                    </label>
                    <select id="filter-inst" onchange="applyFilters()" class="w-full bg-slate-950 border border-slate-700 rounded-xl px-3 py-2.5 text-xs text-slate-200 focus:outline-none focus:ring-2 focus:ring-amber-500 transition">
                        <option value="">Todas as Instituições</option>
                        <option value="IFCE">IFCE (Ceará)</option>
                        <option value="IFSC">IFSC (Santa Catarina)</option>
                        <option value="IFSP">IFSP (São Paulo)</option>
                    </select>
                </div>
            </div>

            <div class="flex items-center justify-between pt-2 border-t border-slate-800">
                <span id="results-count" class="text-xs text-slate-400 font-medium">Carregando questões...</span>
                <button onclick="resetFilters()" class="text-xs text-slate-400 hover:text-white transition flex items-center gap-1 hover:underline">
                    <i data-lucide="rotate-ccw" class="w-3.5 h-3.5"></i> Limpar Filtros
                </button>
            </div>
        </div>

        <!-- Lista Dinâmica de Questões -->
        <div id="questions-container" class="space-y-6">
            <!-- Preenchido dinamicamente por pesquisa.js -->
        </div>

        <!-- Estado Vazio (Sem Resultados) -->
        <div id="empty-state" class="hidden text-center py-16 bg-slate-900/60 border border-slate-800 rounded-3xl p-8">
            <div class="w-14 h-14 bg-slate-800 text-slate-400 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <i data-lucide="search-x" class="w-7 h-7"></i>
            </div>
            <h3 class="text-lg font-bold text-white mb-2">Nenhuma questão encontrada</h3>
            <p class="text-xs sm:text-sm text-slate-400 max-w-md mx-auto mb-5">
                Não encontramos questões correspondentes aos critérios de busca selecionados. Tente ajustar os termos ou redefinir os filtros.
            </p>
            <button onclick="resetFilters()" class="bg-blue-600 hover:bg-blue-500 text-white font-bold px-5 py-2.5 rounded-xl text-xs sm:text-sm transition inline-flex items-center gap-2 shadow-md">
                <i data-lucide="rotate-ccw" class="w-4 h-4"></i> Redefinir Todos os Filtros
            </button>
        </div>

    </main>

{get_footer(rel_root=".", is_exam=True)}

    <!-- Script Dedicado de Pesquisa BNCC -->
    <script src="./assets/js/pesquisa.js"></script>
</body>
</html>
"""
    with open("pesquisa.html", "w", encoding="utf-8") as f:
        f.write(pesquisa_html)

    print("Generated pesquisa.html successfully!")

# ==============================================================================
# 9. EXECUÇÃO COMPLETA DO BUILD
# ==============================================================================
if __name__ == "__main__":
    sync_data_files()
    build_subtopic_pages()
    build_block_overview_pages()
    build_homepage()
    build_provas_hub()
    build_simulado_page()
    build_pesquisa_page()
    print("\n✅ Site build completed successfully with two separated sections!")

