import json
import os
import re
from datetime import datetime

# ==============================================================================
# 1. CARREGAMENTO E SINCRONIZAÇÃO DE DADOS (Single Source of Truth)
# ==============================================================================
with open("mathData_augmented.json", "r", encoding="utf-8") as f:
    math_data = json.load(f)

# Métricas Globais Calculadas Dinamicamente
total_subtopics = sum(len(b["topics"]) for b in math_data.values())
total_questions = sum(sum(len(t["questions"]) for t in b["topics"]) for b in math_data.values())
total_official_exams = sum(
    len(b["topics"])
    for b in math_data.values()
    if any(k in b.get("title", "").lower() for k in ["provas", "oficiais"])
)

def sync_data_files():
    """Garante que mathData.json e assets/js/data.js estejam 100% sincronizados."""
    with open("mathData.json", "w", encoding="utf-8") as f:
        json.dump(math_data, f, ensure_ascii=False, indent=2)

    js_data_content = f"""/**
 * PartiuIF - Banco de Dados de Matemática Oficial
 * Contém os {len(math_data)} blocos, {total_subtopics} subtópicos e {total_questions} exercícios com resoluções KaTeX.
 * Gerado automaticamente por build_full_site.py - Fonte da verdade: mathData_augmented.json
 */
const mathData = {json.dumps(math_data, ensure_ascii=False, indent=2)};

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

def get_pdf_relative_path(pdf_filename):
    """Localiza o PDF oficial em qualquer subdiretório de provas/."""
    if not pdf_filename:
        return None
    provas_dir = "provas"
    if os.path.exists(provas_dir):
        for entry in os.listdir(provas_dir):
            full = os.path.join(provas_dir, entry, pdf_filename)
            if os.path.isfile(full):
                return f"../provas/{entry}/{pdf_filename}"
    return None

def get_navbar_label(b_id, block):
    """Gera um rótulo curto e elegante para o menu de navegação."""
    title = block.get("title", f"Bloco {b_id}")
    if "ifsc" in title.lower():
        return "Provas IFSC"
    elif "ifce" in title.lower():
        return "Provas IFCE"
    elif "provas" in title.lower():
        return f"Provas {title.split()[-1]}"
    return f"Bloco {b_id}"

# ==============================================================================
# 3. TEMPLATES REUTILIZÁVEIS (Head, Navbar, Footer)
# ==============================================================================
def get_head(title, rel_root="."):
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
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
<body class="bg-gray-50 text-gray-800 font-sans antialiased min-h-screen flex flex-col">
"""

def get_navbar(active_key="", rel_root="."):
    blocks_nav = [("home", f"{rel_root}/index.html", "Início", "home")]
    for b_id, block in math_data.items():
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

    return f"""    <!-- Header / Navbar Principal -->
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

                <!-- Ações do Usuário -->
                <div class="flex items-center gap-3">
                    <a href="{rel_root}/simulado.html" class="bg-brand-500 hover:bg-brand-400 text-white font-semibold px-3.5 py-1.5 rounded-lg text-sm transition flex items-center gap-1.5 shadow hover:shadow-md">
                        <i data-lucide="award" class="w-4 h-4"></i> Simulado IF
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
            <a href="{rel_root}/simulado.html" class="block px-3 py-2 rounded-md text-base font-bold bg-brand-600 text-white flex items-center gap-2 mt-2">
                <i data-lucide="award" class="w-4 h-4"></i> Simulado IF Geral
            </a>
        </div>
    </header>
"""

def get_footer(rel_root="."):
    footer_block_links = []
    for b_id, block in math_data.items():
        folder = get_block_folder(b_id, block)
        footer_block_links.append(f'<li><a href="{rel_root}/{folder}/index.html" class="hover:text-white transition flex items-center gap-1">• {block["title"]}</a></li>')

    return f"""    <footer class="bg-brand-950 text-white border-t border-brand-800 mt-16 py-10">
        <div class="max-w-7xl mx-auto px-4 grid grid-cols-1 md:grid-cols-3 gap-8 text-sm">
            <div>
                <div class="flex items-center gap-2 text-lg font-bold text-brand-300 mb-2">
                    <i data-lucide="book-open-check" class="w-5 h-5"></i> PartiuIF - Matemática
                </div>
                <p class="text-brand-200 text-xs leading-relaxed">
                    Plataforma completa de revisão estruturada por subtópicos, teoria detalhada, fórmulas KaTeX e simulados com {total_official_exams} provas oficiais do IFSC e IFCE.
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
# 4. GERAÇÃO DE PÁGINAS DE SUBTÓPICOS
# ==============================================================================
def build_subtopic_pages():
    print(f"\n--- Generating {total_subtopics} Subtopic Pages ---")
    
    for b_id, block in math_data.items():
        folder = get_block_folder(b_id, block)
        os.makedirs(folder, exist_ok=True)
        topics = block["topics"]
        
        for idx, topic in enumerate(topics):
            t_id = topic["id"]
            title = topic["title"]
            filename = topic["filename"]
            target_path = os.path.join(folder, filename)
            
            prev_topic = topics[idx - 1] if idx > 0 else None
            next_topic = topics[idx + 1] if idx < len(topics) - 1 else None

            # Pontos-Chave
            key_points_html = "".join([f"""
                <li class="flex items-start gap-2 text-xs sm:text-sm text-gray-700">
                    <i data-lucide="check" class="w-4 h-4 text-brand-600 flex-shrink-0 mt-0.5"></i>
                    <span>{point}</span>
                </li>
            """ for point in topic.get("keyPoints", [])])

            # Exemplo Resolvido
            solved_ex = topic.get("solvedExample", {})
            problem_txt = solved_ex.get("problem", "")
            sol_txt = solved_ex.get("solution", "")

            # Questões
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

            # Sidebar de Tópicos
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

            # Botões de Navegação Anterior / Próximo
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

            # Botão de Download do PDF Oficial
            pdf_path = get_pdf_relative_path(topic.get("pdf"))
            pdf_download_btn = ""
            if pdf_path:
                pdf_download_btn = f"""
                    <a href="{pdf_path}" download class="bg-brand-700 hover:bg-brand-800 text-white font-semibold px-4 py-2 rounded-xl text-sm transition flex items-center gap-2 shadow-sm">
                        <i data-lucide="download" class="w-4 h-4"></i> Baixar Prova em PDF
                    </a>
                """

            page_html = f"""{get_head(f"{title} - {block['title']} | PartiuIF", rel_root="..")}
{get_navbar(active_key=b_id, rel_root="..")}

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

                <!-- Exercícios de Fixação / Questões da Prova -->
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

{get_footer(rel_root="..")}

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

    print(f"Generated all {total_subtopics} subtopic pages successfully!")

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
        
        topic_cards = []
        for idx, topic in enumerate(topics):
            t_id = topic["id"]
            title = topic["title"]
            filename = topic["filename"]
            q_count = len(topic.get("questions", []))
            bncc = topic.get("bncc", "Revisão Geral")
            summary = topic.get("summary", "")
            
            pdf_path = get_pdf_relative_path(topic.get("pdf"))
            pdf_btn = ""
            if pdf_path:
                pdf_btn = f"""
                    <a href="{pdf_path}" download class="bg-gray-100 hover:bg-gray-200 text-gray-700 font-semibold px-3 py-2 rounded-xl text-xs transition flex items-center gap-1.5" title="Baixar Prova Oficial">
                        <i data-lucide="download" class="w-3.5 h-3.5 text-brand-700"></i> PDF Oficial
                    </a>
                """

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
                            {pdf_btn}
                            <a href="./{filename}" class="bg-brand-600 hover:bg-brand-700 text-white font-semibold px-4 py-2 rounded-xl text-xs transition flex items-center gap-1.5 shadow-sm">
                                Estudar <i data-lucide="arrow-right" class="w-3.5 h-3.5"></i>
                            </a>
                        </div>
                    </div>
                </div>
            """)

        block_page_html = f"""{get_head(f"{block['title']} | PartiuIF", rel_root="..")}
{get_navbar(active_key=b_id, rel_root="..")}

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-grow">
        <!-- Breadcrumbs -->
        <nav class="flex text-xs font-medium text-gray-500 mb-6" aria-label="Breadcrumb">
            <ol class="inline-flex items-center space-x-1 sm:space-x-2">
                <li><a href="../index.html" class="hover:text-brand-700 flex items-center gap-1"><i data-lucide="home" class="w-3.5 h-3.5"></i> Início</a></li>
                <li><span class="text-gray-400">/</span></li>
                <li class="text-gray-800 font-semibold">{block['title']}</li>
            </ol>
        </nav>

        <!-- Hero do Bloco -->
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
                <span id="block-progress-txt-{b_id}" class="text-brand-700">0% (0/{len(topics)})</span>
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

{get_footer(rel_root="..")}

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
# 6. GERAÇÃO DA HOMEPAGE (index.html)
# ==============================================================================
def build_homepage():
    print("\n--- Generating Homepage (index.html) ---")

    home_block_cards = []
    all_topics_directory = []

    for b_id, block in math_data.items():
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

    home_page_html = f"""{get_head("PartiuIF - Plataforma de Matemática para Institutos Federais", rel_root=".")}
{get_navbar(active_key="home", rel_root=".")}

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-grow">
        
        <!-- Hero Principal -->
        <div class="gradient-hero rounded-3xl p-6 sm:p-12 text-white mb-10 shadow-2xl relative overflow-hidden">
            <div class="relative z-10 max-w-3xl">
                <span class="bg-brand-500/30 text-brand-200 border border-brand-400/30 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider mb-4 inline-flex items-center gap-1.5">
                    <i data-lucide="sparkles" class="w-3.5 h-3.5 text-brand-300"></i> Plataforma Oficial Multi-Páginas
                </span>
                
                <h1 class="text-3xl sm:text-5xl font-extrabold tracking-tight mb-4 leading-tight">
                    Matriz de Referência IF: Matemática
                </h1>
                
                <p class="text-brand-100 text-sm sm:text-base mb-8 leading-relaxed">
                    Preparação modular completa para o Exame de Classificação dos Institutos Federais. Cada subtópico possui sua própria página com teoria detalhada, fórmulas KaTeX, exemplos resolvidos e {total_questions} exercícios salvos no navegador.
                </p>

                <div class="flex flex-wrap items-center gap-4">
                    <a href="./simulado.html" class="bg-white hover:bg-brand-50 text-brand-900 font-extrabold px-6 py-3.5 rounded-2xl text-sm transition flex items-center gap-2.5 shadow-lg hover:scale-102">
                        <i data-lucide="award" class="w-5 h-5 text-brand-700"></i> Iniciar Simulado Geral
                    </a>
                    <a href="#blocos" class="bg-brand-700/80 hover:bg-brand-700 text-white font-bold px-6 py-3.5 rounded-2xl text-sm transition flex items-center gap-2 border border-brand-500/30">
                        <i data-lucide="layers" class="w-5 h-5"></i> Explorar os {len(math_data)} Blocos
                    </a>
                </div>
            </div>
        </div>

        <!-- Dashboard de Status Rápido (4 Métricas) -->
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
                        <i data-lucide="search" class="w-5 h-5 text-brand-600"></i> Localizador Rápido de Subtópicos
                    </h3>
                    <p class="text-xs text-gray-500">Digite um tema (ex: Pitágoras, Frações, 2024.1, Áreas, Probabilidade) para acessar diretamente.</p>
                </div>
            </div>
            
            <div class="relative">
                <input type="text" id="topic-search-input" placeholder="Digite para filtrar os {total_subtopics} subtópicos..." class="w-full bg-gray-50 border border-gray-300 rounded-xl px-4 py-3 pl-11 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 focus:bg-white transition">
                <i data-lucide="search" class="w-5 h-5 text-gray-400 absolute left-3.5 top-3.5"></i>
            </div>
            
            <div id="search-results-container" class="hidden mt-4 pt-4 border-t border-gray-100 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                <!-- Preenchido dinamicamente pelo módulo app.js -->
            </div>
        </div>

        <!-- Grade dos Blocos de Conteúdo -->
        <section id="blocos" class="mb-14">
            <div class="flex flex-col sm:flex-row justify-between sm:items-center gap-4 mb-6">
                <div>
                    <h2 class="text-2xl font-extrabold text-gray-900 flex items-center gap-2 border-l-4 border-brand-600 pl-3">
                        Blocos de Conteúdo
                    </h2>
                    <p class="text-xs sm:text-sm text-gray-500 mt-1 pl-3">Os {len(math_data)} eixos essenciais com teoria, resolução passo a passo e simulados.</p>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {''.join(home_block_cards)}
            </div>
        </section>

        <!-- Diretório Completo de Todos os Subtópicos -->
        <section class="mb-12">
            <div class="mb-6">
                <h2 class="text-2xl font-extrabold text-gray-900 flex items-center gap-2 border-l-4 border-brand-600 pl-3">
                    Diretório Completo de Subtópicos ({total_subtopics} Páginas)
                </h2>
                <p class="text-xs sm:text-sm text-gray-500 mt-1 pl-3">Acesse cada página individual para estudar e resolver as questões com auto-salvamento.</p>
            </div>

            {''.join(all_topics_directory)}
        </section>

    </main>

{get_footer(rel_root=".")}

</body>
</html>
"""
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(home_page_html)

    print("Generated homepage index.html successfully!")

# ==============================================================================
# 7. GERAÇÃO DA PÁGINA DE SIMULADO (simulado.html)
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

    simulado_html = f"""{get_head("Simulado Geral de Matemática | PartiuIF", rel_root=".")}
{get_navbar(active_key="simulado", rel_root=".")}

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
                    Personalize seu simulado com questões retiradas do banco oficial dos {len(math_data)} blocos e das {total_official_exams} provas oficiais do IFSC e IFCE. Ao final, veja seu desempenho e a resolução comentada de cada questão.
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

{get_footer(rel_root=".")}

    <!-- Motor Dedicado do Simulado -->
    <script src="./assets/js/simulado.js"></script>
</body>
</html>
"""
    with open("simulado.html", "w", encoding="utf-8") as f:
        f.write(simulado_html)

    print("Generated simulado.html successfully!")

# ==============================================================================
# 8. EXECUÇÃO COMPLETA DO BUILD
# ==============================================================================
if __name__ == "__main__":
    sync_data_files()
    build_subtopic_pages()
    build_block_overview_pages()
    build_homepage()
    build_simulado_page()
    print("\n✅ Site build completed successfully with zero hardcoded paths!")
