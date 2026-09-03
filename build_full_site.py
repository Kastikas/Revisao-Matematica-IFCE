import json
import os
import re

with open("mathData_augmented.json", "r", encoding="utf-8") as f:
    math_data = json.load(f)

block_folders = {
    "1": "bloco-1-numeros",
    "2": "bloco-2-algebra",
    "3": "bloco-3-geometria",
    "4": "bloco-4-medidas-e-estatistica",
    "5": "bloco-5-provas-ifsc",
    "6": "bloco-6-provas-ifce"
}

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
    blocks_nav = [
        ("home", f"{rel_root}/index.html", "Início", "home"),
        ("1", f"{rel_root}/bloco-1-numeros/index.html", "Bloco 1", "binary"),
        ("2", f"{rel_root}/bloco-2-algebra/index.html", "Bloco 2", "variable"),
        ("3", f"{rel_root}/bloco-3-geometria/index.html", "Bloco 3", "shapes"),
        ("4", f"{rel_root}/bloco-4-medidas-e-estatistica/index.html", "Bloco 4", "bar-chart-3"),
        ("5", f"{rel_root}/bloco-5-provas-ifsc/index.html", "Provas IFSC", "file-text"),
        ("6", f"{rel_root}/bloco-6-provas-ifce/index.html", "Provas IFCE", "award"),
    ]

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
    return f"""    <footer class="bg-brand-950 text-white border-t border-brand-800 mt-16 py-10">
        <div class="max-w-7xl mx-auto px-4 grid grid-cols-1 md:grid-cols-3 gap-8 text-sm">
            <div>
                <div class="flex items-center gap-2 text-lg font-bold text-brand-300 mb-2">
                    <i data-lucide="book-open-check" class="w-5 h-5"></i> PartiuIF - Matemática
                </div>
                <p class="text-brand-200 text-xs leading-relaxed">
                    Plataforma completa de revisão estruturada por subtópicos, teoria detalhada, fórmulas KaTeX e simulados com 21 provas oficiais do IFSC e IFCE.
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
                    <li><a href="{rel_root}/bloco-1-numeros/index.html" class="hover:text-white transition flex items-center gap-1">• Bloco 1: Números e Operações</a></li>
                    <li><a href="{rel_root}/bloco-2-algebra/index.html" class="hover:text-white transition flex items-center gap-1">• Bloco 2: Álgebra e Funções</a></li>
                    <li><a href="{rel_root}/bloco-3-geometria/index.html" class="hover:text-white transition flex items-center gap-1">• Bloco 3: Geometria Plana e Espacial</a></li>
                    <li><a href="{rel_root}/bloco-4-medidas-e-estatistica/index.html" class="hover:text-white transition flex items-center gap-1">• Bloco 4: Medidas, Prob. e Estatística</a></li>
                    <li><a href="{rel_root}/bloco-5-provas-ifsc/index.html" class="hover:text-white transition flex items-center gap-1">• Bloco 5: Provas Oficiais IFSC (2017-2026)</a></li>
                    <li><a href="{rel_root}/bloco-6-provas-ifce/index.html" class="hover:text-white transition flex items-center gap-1">• Bloco 6: Provas Oficiais IFCE (2023-2025)</a></li>
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

    <!-- Scripts da Aplicação -->
    <script src="{rel_root}/assets/js/data.js"></script>
    <script src="{rel_root}/assets/js/app.js"></script>
"""

# ==========================================
# 1. BUILD ALL 41 SUBTOPIC PAGES
# ==========================================
print("\n--- Generating 41 Subtopic Pages ---")

for b_id, block in math_data.items():
    folder = block_folders[b_id]
    os.makedirs(folder, exist_ok=True)
    topics = block["topics"]
    
    for idx, topic in enumerate(topics):
        t_id = topic["id"]
        title = topic["title"]
        filename = topic["filename"]
        target_path = os.path.join(folder, filename)
        
        # Determine previous and next topic links
        prev_topic = topics[idx - 1] if idx > 0 else None
        next_topic = topics[idx + 1] if idx < len(topics) - 1 else None

        # Build Key Points HTML
        key_points_html = "".join([f"""
            <li class="flex items-start gap-2 text-xs sm:text-sm text-gray-700">
                <i data-lucide="check" class="w-4 h-4 text-brand-600 flex-shrink-0 mt-0.5"></i>
                <span>{point}</span>
            </li>
        """ for point in topic.get("keyPoints", [])])

        # Solved example
        solved_ex = topic.get("solvedExample", {})
        problem_txt = solved_ex.get("problem", "")
        sol_txt = solved_ex.get("solution", "")

        # Build Questions HTML
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

        # Sidebar list of topics
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

        # Prev/Next Buttons
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

        # PDF download button if topic has pdf
        pdf_download_btn = ""
        if topic.get("pdf"):
            sub_f = "ifce" if b_id == "6" else "ifsc"
            pdf_download_btn = f"""
                <a href="../provas/{sub_f}/{topic['pdf']}" download class="bg-brand-700 hover:bg-brand-800 text-white font-semibold px-4 py-2 rounded-xl text-sm transition flex items-center gap-2 shadow-sm">
                    <i data-lucide="file-down" class="w-4 h-4"></i> Baixar Prova Oficial (PDF)
                </a>
            """

        page_html = f"""{get_head(f"{title} - {block['title']} | PartiuIF", rel_root="..")}
{get_navbar(active_key=b_id, rel_root="..")}

    <main class="flex-grow max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        <!-- Breadcrumbs -->
        <nav class="flex items-center gap-2 text-xs sm:text-sm text-gray-500 mb-6 flex-wrap">
            <a href="../index.html" class="hover:text-brand-700 flex items-center gap-1"><i data-lucide="home" class="w-3.5 h-3.5"></i> Início</a>
            <span class="text-gray-300">/</span>
            <a href="./index.html" class="hover:text-brand-700">{block['title']}</a>
            <span class="text-gray-300">/</span>
            <span class="text-gray-800 font-semibold">{title}</span>
        </nav>

        <!-- Cabeçalho do Subtópico -->
        <div class="bg-white rounded-2xl p-6 sm:p-8 shadow-sm mb-8 border border-gray-200 flex flex-col md:flex-row justify-between md:items-center gap-4">
            <div>
                <div class="flex items-center gap-2 mb-2">
                    <span class="bg-brand-100 text-brand-800 text-xs font-bold px-3 py-1 rounded-full border border-brand-200">
                        BNCC: {topic.get('bncc', 'Revisão Geral')}
                    </span>
                    <span class="text-xs text-gray-500 font-medium">Subtópico 0{idx + 1} de 0{len(topics)}</span>
                </div>
                <h1 class="text-2xl sm:text-3xl font-extrabold text-gray-900">{title}</h1>
                <p class="text-gray-600 text-sm sm:text-base mt-2 max-w-3xl leading-relaxed">{topic.get('summary', '')}</p>
            </div>
            
            <div class="flex flex-col sm:flex-row md:flex-col lg:flex-row items-start sm:items-center gap-3">
                {pdf_download_btn}
                <button id="btn-toggle-done-{t_id}" onclick="toggleTopicDone('{t_id}')" class="px-4 py-2 rounded-xl text-sm font-semibold border bg-white text-gray-700 border-gray-300 hover:bg-gray-50 transition flex items-center gap-2 shadow-sm">
                    <i data-lucide="square" class="w-4 h-4 text-gray-400"></i> Marcar como Concluído
                </button>
            </div>
        </div>

        <!-- Layout de Conteúdo: 2 Colunas de Estudo + 1 Coluna Lateral -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            
            <!-- Coluna Principal de Estudos (2 Colunas) -->
            <div class="lg:col-span-2 space-y-8">
                
                <!-- 1. Teoria e Dicas -->
                <section class="bg-white border border-gray-200 rounded-2xl p-6 sm:p-8 shadow-sm">
                    <h2 class="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2.5 text-brand-800">
                        <i data-lucide="book-open" class="w-5 h-5 text-brand-600"></i> Teoria e Conceitos Chave
                    </h2>
                    <div class="text-gray-700 leading-relaxed text-sm sm:text-base mb-6 space-y-3">
                        <p>{topic.get('detailedTheory', '')}</p>
                    </div>
                    
                    <div class="bg-brand-50/70 border border-brand-200 rounded-xl p-5">
                        <h3 class="text-xs font-bold text-brand-900 uppercase tracking-wider mb-3 flex items-center gap-1.5">
                            <i data-lucide="lightbulb" class="w-4 h-4 text-brand-600"></i> Dicas Essenciais para o Exame IF
                        </h3>
                        <ul class="space-y-2">
                            {key_points_html}
                        </ul>
                    </div>
                </section>

                <!-- 2. Fórmulas Fundamentais -->
                <section class="bg-brand-900 text-white rounded-2xl p-6 sm:p-8 shadow-md border border-brand-800">
                    <h2 class="text-brand-300 text-xs font-bold uppercase tracking-wider mb-3 flex items-center gap-2">
                        <i data-lucide="sigma" class="w-4 h-4"></i> Fórmulas e Relações Fundamentais
                    </h2>
                    <div class="text-lg sm:text-2xl text-center py-4 px-2 bg-brand-950/60 rounded-xl overflow-x-auto text-brand-100 font-mono border border-brand-800">
                        $${topic.get('formula', '')}$$
                    </div>
                </section>

                <!-- 3. Exemplo Resolvido Passo a Passo -->
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

                <!-- 4. Exercícios de Fixação / Questões da Prova -->
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

                <!-- 5. Navegação Inferior de Tópicos -->
                <nav class="flex items-center justify-between gap-4 pt-4 border-t border-gray-200 flex-wrap">
                    {''.join(nav_buttons)}
                </nav>
            </div>

            <!-- Coluna Lateral (Sidebar com Subtópicos do Bloco) -->
            <div class="space-y-6">
                
                <!-- Card de Progresso do Bloco -->
                <div class="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm">
                    <h3 class="text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">Progresso no Bloco</h3>
                    <div class="flex justify-between text-xs text-gray-600 mb-1.5 font-medium">
                        <span>Conclusão</span>
                        <span id="block-progress-txt-{b_id}" class="font-bold text-brand-700">0%</span>
                    </div>
                    <div class="w-full bg-gray-100 rounded-full h-2.5 overflow-hidden">
                        <div id="block-progress-bar-{b_id}" class="bg-brand-600 h-full w-0 transition-all duration-500"></div>
                    </div>
                </div>

                <!-- Lista de Subtópicos do Bloco -->
                <div class="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm sticky top-20">
                    <div class="flex items-center justify-between mb-4 border-b pb-3">
                        <h3 class="text-sm font-bold text-gray-900 uppercase tracking-wider">Subtópicos do Bloco</h3>
                        <a href="./index.html" class="text-xs text-brand-600 hover:text-brand-800 font-semibold">Ver Todos</a>
                    </div>
                    <div class="space-y-1.5 custom-scrollbar max-h-[60vh] overflow-y-auto pr-1">
                        {''.join(sidebar_items)}
                    </div>
                    
                    <div class="mt-6 pt-4 border-t border-gray-100">
                        <a href="../simulado.html" class="w-full bg-brand-50 hover:bg-brand-100 text-brand-800 font-semibold py-2.5 px-4 rounded-xl text-xs transition flex items-center justify-center gap-1.5">
                            <i data-lucide="play" class="w-3.5 h-3.5"></i> Iniciar Simulado Geral
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

print("Generated all 41 subtopic pages successfully!")


# ==========================================
# 2. BUILD ALL 6 BLOCK OVERVIEW PAGES
# ==========================================
print("\n--- Generating 6 Block Overview Pages ---")

for b_id, block in math_data.items():
    folder = block_folders[b_id]
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
        
        pdf_btn = ""
        if topic.get("pdf"):
            sub_f = "ifce" if b_id == "6" else "ifsc"
            pdf_btn = f"""
                <a href="../provas/{sub_f}/{topic['pdf']}" download class="bg-gray-100 hover:bg-gray-200 text-gray-700 font-semibold px-3 py-2 rounded-xl text-xs transition flex items-center gap-1.5" title="Baixar Prova Oficial">
                    <i data-lucide="download" class="w-3.5 h-3.5 text-brand-700"></i> PDF Oficial
                </a>
            """

        topic_cards.append(f"""
            <div class="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm hover-card flex flex-col justify-between" data-topic-id="{t_id}">
                <div>
                    <div class="flex items-center justify-between mb-3">
                        <span class="text-xs font-bold text-brand-700 bg-brand-50 px-2.5 py-1 rounded-lg border border-brand-100">
                            Tópico 0{idx + 1}
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

    <main class="flex-grow max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        <!-- Breadcrumbs -->
        <nav class="flex items-center gap-2 text-xs sm:text-sm text-gray-500 mb-6">
            <a href="../index.html" class="hover:text-brand-700 flex items-center gap-1"><i data-lucide="home" class="w-3.5 h-3.5"></i> Início</a>
            <span class="text-gray-300">/</span>
            <span class="text-gray-800 font-semibold">{block['title']}</span>
        </nav>

        <!-- Banner do Bloco -->
        <div class="bg-gradient-to-r from-brand-800 to-brand-950 rounded-3xl p-6 sm:p-10 text-white shadow-xl mb-10 relative overflow-hidden">
            <div class="relative z-10 max-w-3xl">
                <div class="flex items-center gap-3 mb-4">
                    <div class="w-12 h-12 bg-white/10 rounded-2xl flex items-center justify-center text-brand-300 border border-white/20">
                        <i data-lucide="{block.get('icon', 'book')}" class="w-6 h-6"></i>
                    </div>
                    <div>
                        <span class="bg-brand-500/30 text-brand-200 border border-brand-400/30 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">
                            Eixo Temático
                        </span>
                    </div>
                </div>
                <h1 class="text-3xl sm:text-4xl font-extrabold tracking-tight mb-3">{block['title']}</h1>
                <p class="text-brand-100 text-sm sm:text-base mb-6 leading-relaxed">
                    {block.get('description', '')}
                </p>

                <!-- Progresso e Ações -->
                <div class="bg-brand-900/60 border border-brand-700/60 rounded-2xl p-4 sm:p-5 max-w-xl mb-6">
                    <div class="flex justify-between text-xs text-brand-200 mb-2 font-medium">
                        <span>Progresso de Conclusão do Bloco</span>
                        <span id="block-progress-txt-{b_id}" class="font-bold text-brand-300">0%</span>
                    </div>
                    <div class="w-full bg-brand-950 rounded-full h-3 overflow-hidden border border-brand-800">
                        <div id="block-progress-bar-{b_id}" class="bg-brand-400 h-full w-0 transition-all duration-500"></div>
                    </div>
                </div>

                <div class="flex flex-wrap items-center gap-3">
                    <a href="./{first_topic['filename']}" class="bg-white hover:bg-brand-50 text-brand-900 font-bold px-5 py-2.5 rounded-xl text-sm transition flex items-center gap-2 shadow">
                        <i data-lucide="play-circle" class="w-4 h-4 text-brand-700"></i> Começar pelo Tópico 01
                    </a>
                    <a href="../simulado.html" class="bg-brand-600 hover:bg-brand-500 text-white font-bold px-5 py-2.5 rounded-xl text-sm transition flex items-center gap-2 border border-brand-400/40">
                        <i data-lucide="award" class="w-4 h-4"></i> Fazer Simulado Geral
                    </a>
                </div>
            </div>
        </div>

        <!-- Seção de Subtópicos -->
        <div class="mb-12">
            <div class="flex flex-col sm:flex-row justify-between sm:items-center gap-4 mb-6">
                <div>
                    <h2 class="text-2xl font-bold text-gray-900 flex items-center gap-2 border-l-4 border-brand-600 pl-3">
                        Subtópicos e Provas
                    </h2>
                    <p class="text-xs sm:text-sm text-gray-500 mt-1 pl-3">Clique em qualquer subtópico para estudar a teoria, fórmulas, exemplos e resolver as questões.</p>
                </div>
                <span class="text-xs font-semibold px-3 py-1.5 rounded-xl bg-gray-100 text-gray-700 self-start sm:self-auto">
                    Total: {len(topics)} Subtópicos
                </span>
            </div>

            <!-- Grade de Cards de Subtópicos -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {''.join(topic_cards)}
            </div>
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

print("Generated all 6 block overview pages successfully!")

# ==========================================
# 3. BUILD HOMEPAGE (index.html)
# ==========================================
print("\n--- Generating Homepage (index.html) ---")

home_block_cards = []
for b_id, block in math_data.items():
    folder = block_folders[b_id]
    topics = block["topics"]
    
    # Preview top 3 topics
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

                <!-- Barra de Progresso do Bloco -->
                <div class="mb-5 bg-gray-50 border border-gray-100 p-3 rounded-xl">
                    <div class="flex justify-between text-xs text-gray-500 mb-1.5 font-medium">
                        <span>Progresso do Bloco</span>
                        <span id="block-progress-txt-{b_id}" class="font-bold text-brand-700">0%</span>
                    </div>
                    <div class="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
                        <div id="block-progress-bar-{b_id}" class="bg-brand-600 h-full w-0 transition-all duration-500"></div>
                    </div>
                </div>

                <!-- Subtópicos em Destaque -->
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

# Full directory of all 41 topics for home
all_topics_directory = []
for b_id, block in math_data.items():
    folder = block_folders[b_id]
    topics = block["topics"]
    
    topic_items = []
    for idx, t in enumerate(topics):
        topic_items.append(f"""
            <a href="./{folder}/{t['filename']}" class="p-3 rounded-xl border border-gray-200 hover:border-brand-400 hover:bg-brand-50/50 transition flex items-center justify-between group bg-white shadow-2xs">
                <div class="flex items-center gap-3 pr-2">
                    <i id="status-icon-{t['id']}" data-lucide="circle" class="w-4 h-4 text-gray-300 flex-shrink-0"></i>
                    <div>
                        <h5 class="text-xs sm:text-sm font-semibold text-gray-800 group-hover:text-brand-900">{t['title']}</h5>
                        <span class="text-[11px] text-gray-400">BNCC: {t.get('bncc', 'Revisão Geral')} &bull; {len(t.get('questions', []))} questões</span>
                    </div>
                </div>
                <i data-lucide="chevron-right" class="w-4 h-4 text-gray-300 group-hover:text-brand-600 flex-shrink-0"></i>
            </a>
        """)

    all_topics_directory.append(f"""
        <div class="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm mb-6">
            <div class="flex items-center justify-between mb-4 border-b border-gray-100 pb-3">
                <div class="flex items-center gap-2.5">
                    <div class="w-8 h-8 bg-brand-100 text-brand-800 rounded-lg flex items-center justify-center font-bold">
                        <i data-lucide="{block.get('icon', 'book')}" class="w-4 h-4 text-brand-700"></i>
                    </div>
                    <h4 class="font-bold text-gray-900 text-base sm:text-lg">{block['title']}</h4>
                </div>
                <a href="./{folder}/index.html" class="text-xs text-brand-700 hover:text-brand-900 font-semibold flex items-center gap-1">
                    Ver Bloco <i data-lucide="arrow-right" class="w-3 h-3"></i>
                </a>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                {''.join(topic_items)}
            </div>
        </div>
    """)

home_page_html = f"""{get_head("PartiuIF - Plataforma de Revisão de Matemática para o IF", rel_root=".")}
{get_navbar(active_key="home", rel_root=".")}

    <main class="flex-grow max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        <!-- Hero Banner Principal -->
        <div class="bg-gradient-to-r from-brand-800 via-brand-900 to-brand-950 rounded-3xl p-6 sm:p-12 text-white shadow-2xl mb-10 relative overflow-hidden">
            <div class="absolute -right-12 -bottom-12 opacity-10 text-white pointer-events-none hidden md:block">
                <i data-lucide="calculator" class="w-96 h-96"></i>
            </div>
            
            <div class="relative z-10 max-w-3xl">
                <span class="bg-brand-500/30 text-brand-200 border border-brand-400/30 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider mb-4 inline-flex items-center gap-1.5">
                    <i data-lucide="sparkles" class="w-3.5 h-3.5 text-brand-300"></i> Plataforma Oficial Multi-Páginas
                </span>
                
                <h1 class="text-3xl sm:text-5xl font-extrabold tracking-tight mb-4 leading-tight">
                    Matriz de Referência IF: Matemática
                </h1>
                
                <p class="text-brand-100 text-sm sm:text-base mb-8 leading-relaxed">
                    Preparação modular completa para o Exame de Classificação dos Institutos Federais. Cada subtópico possui sua própria página com teoria detalhada, fórmulas KaTeX, exemplos resolvidos e 293 exercícios salvos no navegador.
                </p>

                <div class="flex flex-wrap items-center gap-4">
                    <a href="./simulado.html" class="bg-white hover:bg-brand-50 text-brand-900 font-extrabold px-6 py-3.5 rounded-2xl text-sm transition flex items-center gap-2.5 shadow-lg hover:scale-102">
                        <i data-lucide="award" class="w-5 h-5 text-brand-700"></i> Iniciar Simulado Geral
                    </a>
                    <a href="#blocos" class="bg-brand-700/80 hover:bg-brand-700 text-white font-bold px-6 py-3.5 rounded-2xl text-sm transition flex items-center gap-2 border border-brand-500/30">
                        <i data-lucide="layers" class="w-5 h-5"></i> Explorar os 6 Blocos
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
                    <strong id="global-completed-count" class="text-xl font-black text-gray-900">0/41</strong>
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
                    <strong id="global-answered-questions" class="text-xl font-black text-blue-900">0/293</strong>
                </div>
            </div>

            <div class="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm flex items-center gap-4">
                <div class="w-12 h-12 rounded-xl bg-purple-100 flex items-center justify-center text-purple-700 flex-shrink-0">
                    <i data-lucide="file-text" class="w-6 h-6"></i>
                </div>
                <div>
                    <span class="text-xs text-gray-500 font-medium block">Provas Oficiais</span>
                    <strong class="text-xl font-black text-purple-900">21 Edições</strong>
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
                <input type="text" id="topic-search-input" placeholder="Digite para filtrar os 41 subtópicos..." class="w-full bg-gray-50 border border-gray-300 rounded-xl px-4 py-3 pl-11 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 focus:bg-white transition">
                <i data-lucide="search" class="w-5 h-5 text-gray-400 absolute left-3.5 top-3.5"></i>
            </div>
            
            <div id="search-results-container" class="hidden mt-4 pt-4 border-t border-gray-100 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                <!-- Preenchido dinamicamente pelo JS -->
            </div>
        </div>

        <!-- Grade dos 6 Blocos de Conteúdo -->
        <section id="blocos" class="mb-14">
            <div class="flex flex-col sm:flex-row justify-between sm:items-center gap-4 mb-6">
                <div>
                    <h2 class="text-2xl font-extrabold text-gray-900 flex items-center gap-2 border-l-4 border-brand-600 pl-3">
                        Blocos de Conteúdo
                    </h2>
                    <p class="text-xs sm:text-sm text-gray-500 mt-1 pl-3">Os 6 eixos essenciais com teoria, resolução passo a passo e simulados.</p>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {''.join(home_block_cards)}
            </div>
        </section>

        <!-- Índice Completo de Todos os 41 Subtópicos -->
        <section class="mb-12">
            <div class="mb-6">
                <h2 class="text-2xl font-extrabold text-gray-900 flex items-center gap-2 border-l-4 border-brand-600 pl-3">
                    Diretório Completo de Subtópicos (41 Páginas)
                </h2>
                <p class="text-xs sm:text-sm text-gray-500 mt-1 pl-3">Acesse cada página individual para estudar e resolver as questões com auto-salvamento.</p>
            </div>

            {''.join(all_topics_directory)}
        </section>

    </main>

{get_footer(rel_root=".")}

    <!-- Script de Busca Rápida -->
    <script>
        document.addEventListener('DOMContentLoaded', () => {{
            updateGlobalProgress();

            const searchInput = document.getElementById('topic-search-input');
            const searchResults = document.getElementById('search-results-container');

            if (searchInput && searchResults && window.mathData) {{
                const allTopicsList = [];
                for (let bId in mathData) {{
                    const block = mathData[bId];
                    block.topics.forEach(t => {{
                        allTopicsList.push({{
                            id: t.id,
                            title: t.title,
                            bncc: t.bncc || '',
                            summary: t.summary || '',
                            folder: t.folder,
                            filename: t.filename,
                            blockTitle: block.title
                        }});
                    }});
                }}

                searchInput.addEventListener('input', (e) => {{
                    const query = e.target.value.toLowerCase().trim();
                    if (!query) {{
                        searchResults.classList.add('hidden');
                        searchResults.innerHTML = '';
                        return;
                    }}

                    const filtered = allTopicsList.filter(t => 
                        t.title.toLowerCase().includes(query) || 
                        t.bncc.toLowerCase().includes(query) || 
                        t.summary.toLowerCase().includes(query) ||
                        t.blockTitle.toLowerCase().includes(query)
                    );

                    if (filtered.length === 0) {{
                        searchResults.classList.remove('hidden');
                        searchResults.innerHTML = '<div class="col-span-full p-4 text-center text-xs text-gray-500 bg-gray-50 rounded-xl">Nenhum subtópico encontrado com esse termo.</div>';
                    }} else {{
                        searchResults.classList.remove('hidden');
                        searchResults.innerHTML = filtered.map(t => `
                            <a href="./${{t.folder}}/${{t.filename}}" class="p-3 rounded-xl border border-brand-200 hover:border-brand-500 bg-brand-50/40 hover:bg-brand-50 transition flex items-center justify-between group">
                                <div>
                                    <span class="text-[10px] font-bold text-brand-700 uppercase block">${{t.blockTitle}}</span>
                                    <strong class="text-xs sm:text-sm font-semibold text-gray-900 group-hover:text-brand-900">${{t.title}}</strong>
                                </div>
                                <i data-lucide="arrow-right" class="w-4 h-4 text-brand-600 flex-shrink-0"></i>
                            </a>
                        `).join('');
                        if (window.lucide) lucide.createIcons();
                    }}
                }});
            }}
        }});
    </script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(home_page_html)

print("Generated homepage index.html successfully!")


# ==========================================
# 4. BUILD SIMULADO PAGE (simulado.html)
# ==========================================
print("\n--- Generating Simulado Page (simulado.html) ---")

simulado_html = f"""{get_head("Simulado Geral de Matemática | PartiuIF", rel_root=".")}
{get_navbar(active_key="simulado", rel_root=".")}

    <main class="flex-grow max-w-5xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        <!-- Breadcrumbs -->
        <nav class="flex items-center gap-2 text-xs sm:text-sm text-gray-500 mb-6">
            <a href="./index.html" class="hover:text-brand-700 flex items-center gap-1"><i data-lucide="home" class="w-3.5 h-3.5"></i> Início</a>
            <span class="text-gray-300">/</span>
            <span class="text-gray-800 font-semibold">Simulado IF</span>
        </nav>

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
                    Personalize seu simulado com questões retiradas do banco oficial dos 6 blocos e das 21 provas oficiais do IFSC e IFCE. Ao final, veja seu desempenho e a resolução comentada de cada questão.
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
                        <label class="cursor-pointer p-3.5 rounded-xl border border-brand-500 bg-brand-50/60 flex items-center gap-3 text-sm font-semibold text-gray-900 transition hover:border-brand-500">
                            <input type="radio" name="sim-source" value="all" checked class="text-brand-600 focus:ring-brand-500">
                            <span>Todos os Blocos (Geral)</span>
                        </label>
                        <label class="cursor-pointer p-3.5 rounded-xl border border-gray-200 hover:border-brand-300 flex items-center gap-3 text-sm font-medium text-gray-800 transition">
                            <input type="radio" name="sim-source" value="1" class="text-brand-600 focus:ring-brand-500">
                            <span>Bloco 1: Números</span>
                        </label>
                        <label class="cursor-pointer p-3.5 rounded-xl border border-gray-200 hover:border-brand-300 flex items-center gap-3 text-sm font-medium text-gray-800 transition">
                            <input type="radio" name="sim-source" value="2" class="text-brand-600 focus:ring-brand-500">
                            <span>Bloco 2: Álgebra</span>
                        </label>
                        <label class="cursor-pointer p-3.5 rounded-xl border border-gray-200 hover:border-brand-300 flex items-center gap-3 text-sm font-medium text-gray-800 transition">
                            <input type="radio" name="sim-source" value="3" class="text-brand-600 focus:ring-brand-500">
                            <span>Bloco 3: Geometria</span>
                        </label>
                        <label class="cursor-pointer p-3.5 rounded-xl border border-gray-200 hover:border-brand-300 flex items-center gap-3 text-sm font-medium text-gray-800 transition">
                            <input type="radio" name="sim-source" value="4" class="text-brand-600 focus:ring-brand-500">
                            <span>Bloco 4: Medidas & Estatística</span>
                        </label>
                        <label class="cursor-pointer p-3.5 rounded-xl border border-gray-200 hover:border-brand-300 flex items-center gap-3 text-sm font-medium text-gray-800 transition">
                            <input type="radio" name="sim-source" value="5" class="text-brand-600 focus:ring-brand-500">
                            <span>Bloco 5: Provas IFSC</span>
                        </label>
                        <label class="cursor-pointer p-3.5 rounded-xl border border-gray-200 hover:border-brand-300 flex items-center gap-3 text-sm font-medium text-gray-800 transition">
                            <input type="radio" name="sim-source" value="6" class="text-brand-600 focus:ring-brand-500">
                            <span>Bloco 6: Provas IFCE</span>
                        </label>
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
                <!-- Preenchido pelo JS -->
            </div>

            <!-- Card da Questão Atual -->
            <div id="sim-question-card" class="bg-white border border-gray-200 rounded-2xl p-6 sm:p-8 shadow-sm">
                <!-- Preenchido dinamicamente -->
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
            <!-- Preenchido pelo JS -->
        </div>

    </main>

{get_footer(rel_root=".")}

    <!-- Motor do Simulado em JavaScript -->
    <script>
        let currentSimQuestions = [];
        let currentSimAnswers = {{}}; // idx -> selectedOpt
        let currentSimIndex = 0;

        function startSimulado() {{
            const source = document.querySelector('input[name="sim-source"]:checked').value;
            const count = parseInt(document.querySelector('input[name="sim-count"]:checked').value, 10);

            let questionPool = [];
            for (let bId in mathData) {{
                if (source === "all" || source === bId) {{
                    const block = mathData[bId];
                    block.topics.forEach(t => {{
                        t.questions.forEach((q, qIdx) => {{
                            questionPool.push({{
                                ...q,
                                blockId: bId,
                                blockTitle: block.title,
                                topicId: t.id,
                                topicTitle: t.title,
                                originalQIdx: qIdx
                            }});
                        }});
                    }});
                }}
            }}

            if (questionPool.length === 0) {{
                showToast("Nenhuma questão encontrada para os critérios selecionados.", "error");
                return;
            }}

            // Embaralha as questões
            questionPool.sort(() => Math.random() - 0.5);
            currentSimQuestions = questionPool.slice(0, Math.min(count, questionPool.length));
            currentSimAnswers = {{}};
            currentSimIndex = 0;

            document.getElementById('simulado-setup').classList.add('hidden');
            document.getElementById('simulado-results').classList.add('hidden');
            document.getElementById('simulado-running').classList.remove('hidden');

            renderSimQuestionPalette();
            renderCurrentSimQuestion();
            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }}

        function renderSimQuestionPalette() {{
            const palette = document.getElementById('sim-palette');
            palette.innerHTML = currentSimQuestions.map((_, idx) => {{
                const isAnswered = currentSimAnswers.hasOwnProperty(idx);
                const isCurrent = (idx === currentSimIndex);
                let btnClasses = "w-8 h-8 rounded-lg text-xs font-bold transition flex items-center justify-center ";
                
                if (isCurrent) {{
                    btnClasses += "ring-2 ring-brand-600 bg-brand-600 text-white shadow-md ";
                }} else if (isAnswered) {{
                    btnClasses += "bg-brand-100 text-brand-900 border border-brand-300 ";
                }} else {{
                    btnClasses += "bg-gray-100 text-gray-700 hover:bg-gray-200 ";
                }}

                return `<button onclick="jumpToSimQuestion(${{idx}})" class="${{btnClasses}}">${{idx + 1}}</button>`;
            }}).join('');
        }}

        function renderCurrentSimQuestion() {{
            const q = currentSimQuestions[currentSimIndex];
            const qContainer = document.getElementById('sim-question-card');
            const indicator = document.getElementById('sim-progress-indicator');
            const topicTitle = document.getElementById('sim-topic-title');

            indicator.innerText = `Questão ${{currentSimIndex + 1}} de ${{currentSimQuestions.length}}`;
            topicTitle.innerText = `${{q.blockTitle}} &bull; ${{q.topicTitle}}`;

            const selectedOpt = currentSimAnswers[currentSimIndex];

            let optionsHtml = q.options.map((opt, optIdx) => {{
                const letter = String.fromCharCode(65 + optIdx);
                const isSelected = (selectedOpt === optIdx);
                const activeClass = isSelected ? "opt-selected" : "border-gray-200 hover:border-brand-300 hover:bg-brand-50/30";
                const iconName = isSelected ? "check-circle" : "circle";
                const iconClass = isSelected ? "w-4 h-4 text-brand-600 opt-icon" : "w-4 h-4 text-gray-300 opt-icon";

                return `
                    <button onclick="selectSimAnswer(${{currentSimIndex}}, ${{optIdx}})" class="w-full text-left p-3.5 rounded-xl border ${{activeClass}} transition text-sm text-gray-700 flex items-center justify-between group">
                        <span class="flex items-center gap-2"><strong class="text-brand-700 font-bold">${{letter}})</strong> ${{opt}}</span>
                        <i data-lucide="${{iconName}}" class="${{iconClass}}"></i>
                    </button>
                `;
            }}).join('');

            qContainer.innerHTML = `
                <div class="mb-2">
                    <span class="text-xs font-bold text-gray-400 uppercase tracking-wider block mb-2">${{q.topicTitle}}</span>
                    <p class="font-medium text-gray-800 text-base leading-relaxed mb-6">${{q.q}}</p>
                </div>
                <div class="space-y-2.5 mb-2">
                    ${{optionsHtml}}
                </div>
            `;

            // Botões anterior/próximo
            const prevBtn = document.getElementById('sim-prev-btn');
            const nextBtn = document.getElementById('sim-next-btn');

            if (currentSimIndex === 0) {{
                prevBtn.classList.add('opacity-50', 'pointer-events-none');
            }} else {{
                prevBtn.classList.remove('opacity-50', 'pointer-events-none');
            }}

            if (currentSimIndex === currentSimQuestions.length - 1) {{
                nextBtn.innerHTML = `Finalizar <i data-lucide="check" class="w-4 h-4"></i>`;
                nextBtn.onclick = finishSimulado;
            }} else {{
                nextBtn.innerHTML = `Próxima <i data-lucide="arrow-right" class="w-4 h-4"></i>`;
                nextBtn.onclick = nextSimQuestion;
            }}

            if (window.lucide) lucide.createIcons();
            renderLatex(qContainer);
            renderSimQuestionPalette();
        }}

        function selectSimAnswer(qIdx, optIdx) {{
            currentSimAnswers[qIdx] = optIdx;
            renderCurrentSimQuestion();
        }}

        function jumpToSimQuestion(idx) {{
            currentSimIndex = idx;
            renderCurrentSimQuestion();
        }}

        function prevSimQuestion() {{
            if (currentSimIndex > 0) {{
                currentSimIndex--;
                renderCurrentSimQuestion();
            }}
        }}

        function nextSimQuestion() {{
            if (currentSimIndex < currentSimQuestions.length - 1) {{
                currentSimIndex++;
                renderCurrentSimQuestion();
            }} else {{
                finishSimulado();
            }}
        }}

        function confirmExitSimulado() {{
            if (confirm("Deseja realmente sair deste simulado? Suas respostas não finalizadas serão perdidas.")) {{
                document.getElementById('simulado-running').classList.add('hidden');
                document.getElementById('simulado-setup').classList.remove('hidden');
                window.scrollTo({{ top: 0, behavior: 'smooth' }});
            }}
        }}

        function finishSimulado() {{
            const total = currentSimQuestions.length;
            const answeredCount = Object.keys(currentSimAnswers).length;
            
            if (answeredCount < total) {{
                if (!confirm(`Você respondeu ${{answeredCount}} de ${{total}} questões. Deseja finalizar mesmo assim?`)) {{
                    return;
                }}
            }}

            let correctCount = 0;
            let reviewHtml = [];

            currentSimQuestions.forEach((q, idx) => {{
                const userOpt = currentSimAnswers[idx];
                const hasAnswered = (userOpt !== undefined);
                const isCorrect = hasAnswered && (userOpt === q.correct);
                if (isCorrect) correctCount++;

                let optionsReview = q.options.map((opt, optIdx) => {{
                    const letter = String.fromCharCode(65 + optIdx);
                    let optClass = "p-3 rounded-xl border text-xs sm:text-sm flex items-center justify-between ";
                    let iconHtml = `<i data-lucide="circle" class="w-4 h-4 text-gray-300"></i>`;

                    if (optIdx === q.correct) {{
                        optClass += "bg-emerald-50 border-emerald-300 font-bold text-emerald-900";
                        iconHtml = `<i data-lucide="check-circle" class="w-4 h-4 text-emerald-600"></i>`;
                    }} else if (optIdx === userOpt && !isCorrect) {{
                        optClass += "bg-red-50 border-red-300 font-medium text-red-900";
                        iconHtml = `<i data-lucide="x-circle" class="w-4 h-4 text-red-600"></i>`;
                    }} else {{
                        optClass += "bg-white border-gray-200 text-gray-600 opacity-60";
                    }}

                    return `
                        <div class="${{optClass}}">
                            <span><strong>${{letter}})</strong> ${{opt}}</span>
                            ${{iconHtml}}
                        </div>
                    `;
                }}).join('');

                reviewHtml.push(`
                    <div class="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm">
                        <div class="flex items-center justify-between mb-3 pb-2 border-b border-gray-100">
                            <span class="text-xs font-bold uppercase tracking-wider text-brand-700">Questão ${{idx + 1}} de ${{total}}</span>
                            <span class="text-xs font-bold px-2.5 py-0.5 rounded-full ${{isCorrect ? 'bg-emerald-100 text-emerald-800' : 'bg-red-100 text-red-800'}}">
                                ${{isCorrect ? 'Correta' : 'Incorreta'}}
                            </span>
                        </div>
                        <span class="text-xs text-gray-400 block mb-2">${{q.blockTitle}} &bull; ${{q.topicTitle}}</span>
                        <p class="font-semibold text-gray-900 text-sm sm:text-base mb-4">${{q.q}}</p>
                        
                        <div class="space-y-2 mb-4">
                            ${{optionsReview}}
                        </div>

                        <div class="bg-gray-50 border border-gray-200 rounded-xl p-4 text-xs sm:text-sm text-gray-700 leading-relaxed">
                            <strong class="text-brand-900 block mb-1">Explicação Passo a Passo:</strong>
                            ${{q.explanation}}
                        </div>
                    </div>
                `);
            }});

            const percent = Math.round((correctCount / total) * 100);

            const resultsContainer = document.getElementById('simulado-results');
            resultsContainer.innerHTML = `
                <div class="bg-gradient-to-r from-brand-800 to-brand-950 rounded-3xl p-6 sm:p-10 text-white shadow-xl text-center">
                    <span class="bg-brand-500/30 text-brand-200 border border-brand-400/30 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider mb-3 inline-block">
                        Resultado do Simulado
                    </span>
                    <h1 class="text-3xl sm:text-4xl font-extrabold mb-2">Seu Desempenho Geral</h1>
                    <div class="my-6 inline-flex flex-col items-center bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20">
                        <span class="text-5xl sm:text-6xl font-black text-brand-300 mb-1">${{percent}}%</span>
                        <span class="text-sm text-brand-100 font-semibold">Você acertou ${{correctCount}} de ${{total}} questões</span>
                    </div>
                    <div class="flex justify-center gap-3">
                        <button onclick="window.location.reload()" class="bg-white hover:bg-brand-50 text-brand-900 font-bold px-6 py-3 rounded-xl text-sm transition shadow-lg">
                            Fazer Novo Simulado
                        </button>
                    </div>
                </div>

                <div class="space-y-6">
                    <h2 class="text-2xl font-bold text-gray-900 flex items-center gap-2 border-l-4 border-brand-600 pl-3">
                        Gabarito Detalhado e Resoluções
                    </h2>
                    ${{reviewHtml.join('')}}
                </div>
            `;

            document.getElementById('simulado-running').classList.add('hidden');
            resultsContainer.classList.remove('hidden');

            if (window.lucide) lucide.createIcons();
            renderLatex(resultsContainer);
            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }}

        // Se passado o parâmetro ?block=X na URL, pré-seleciona a fonte
        document.addEventListener('DOMContentLoaded', () => {{
            const urlParams = new URLSearchParams(window.location.search);
            const blockParam = urlParams.get('block');
            if (blockParam) {{
                const targetRadio = document.querySelector(`input[name="sim-source"][value="${{blockParam}}"]`);
                if (targetRadio) targetRadio.checked = true;
            }}
        }});
    </script>
</body>
</html>
"""

with open("simulado.html", "w", encoding="utf-8") as f:
    f.write(simulado_html)

print("Generated simulado.html successfully!")

