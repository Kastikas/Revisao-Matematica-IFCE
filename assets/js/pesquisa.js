/**
 * PartiuIF - Motor de Pesquisa de Questões por Descritores BNCC
 * Permite filtrar e resolver 488 questões oficiais por habilidade, unidade temática, ano e instituição.
 */

var allExamQuestions = window.allExamQuestions || [];
var filteredQuestions = window.filteredQuestions || [];
var pesquisaSelections = window.pesquisaSelections || {};

const ITEMS_PER_PAGE = 50;
var currentPage = 1;

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    initQuestionPool();
    initFilters();
    parseUrlParams();
    setupSearchEvents();
    applyFilters(false);
});

function initQuestionPool() {
    if (typeof mathData === 'undefined') {
        console.error('mathData não carregado.');
        return;
    }

    allExamQuestions = [];
    const examBlocks = ['5', '6', '7', '8'];

    examBlocks.forEach(bId => {
        const block = mathData[bId];
        if (!block || !block.topics) return;

        const bTitle = block.title || '';
        let inst = 'IFCE';
        if (bTitle.toLowerCase().includes('ifsc')) inst = 'IFSC';
        else if (bTitle.toLowerCase().includes('ifsp')) inst = 'IFSP';
        else if (bTitle.toLowerCase().includes('ifmg')) inst = 'IFMG';

        block.topics.forEach(topic => {
            const folder = topic.folder || block.folder || `bloco-${bId}`;
            const filename = topic.filename || '';
            const examUrl = `./${folder}/${filename}`;

            (topic.questions || []).forEach((q, qIdx) => {
                const uniqueId = `${topic.id}-q${qIdx}`;
                allExamQuestions.push({
                    ...q,
                    uniqueId: uniqueId,
                    blockId: bId,
                    inst: inst,
                    examId: topic.id,
                    examTitle: topic.title,
                    examUrl: examUrl,
                    qNumber: qIdx + 1,
                    bncc: q.bncc || 'EF07MA18',
                    bnccDesc: q.bnccDesc || 'Equações polinomiais de 1º grau',
                    unidadeTematica: q.unidadeTematica || 'Álgebra',
                    anoEscolar: q.anoEscolar || '7º ano',
                    topicoId: q.topicoId || 'b2-t3'
                });
            });
        });
    });

    console.log(`Carregadas ${allExamQuestions.length} questões de exames oficiais.`);
}

function initFilters() {
    const selectBncc = document.getElementById('filter-bncc');
    if (!selectBncc) return;

    // Contabiliza questões por BNCC
    const bnccCounts = {};
    const bnccDescs = {};
    allExamQuestions.forEach(q => {
        bnccCounts[q.bncc] = (bnccCounts[q.bncc] || 0) + 1;
        bnccDescs[q.bncc] = q.bnccDesc;
    });

    const sortedCodes = Object.keys(bnccCounts).sort();
    sortedCodes.forEach(code => {
        const opt = document.createElement('option');
        opt.value = code;
        opt.textContent = `${code} (${bnccCounts[code]}) - ${bnccDescs[code].substring(0, 50)}...`;
        selectBncc.appendChild(opt);
    });
}

function parseUrlParams() {
    const params = new URLSearchParams(window.location.search);
    const bnccParam = params.get('bncc');
    const qParam = params.get('q');
    const unidadeParam = params.get('unidade');
    const anoParam = params.get('ano');
    const instParam = params.get('instituto');
    const pageParam = parseInt(params.get('page'), 10);

    if (bnccParam) {
        const select = document.getElementById('filter-bncc');
        if (select) select.value = bnccParam;
    }
    if (qParam) {
        const input = document.getElementById('search-text');
        if (input) input.value = qParam;
    }
    if (unidadeParam) {
        const select = document.getElementById('filter-unidade');
        if (select) select.value = unidadeParam;
    }
    if (anoParam) {
        const select = document.getElementById('filter-ano');
        if (select) select.value = anoParam;
    }
    if (instParam) {
        const select = document.getElementById('filter-inst');
        if (select) select.value = instParam;
    }
    if (pageParam && pageParam > 0) {
        currentPage = pageParam;
    }
    toggleClearButton();
}

function setupSearchEvents() {
    const searchForm = document.getElementById('search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', (e) => {
            e.preventDefault();
            applyFilters();
        });
    }

    const searchInput = document.getElementById('search-text');
    if (searchInput) {
        searchInput.addEventListener('input', toggleClearButton);
        searchInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                applyFilters();
            }
        });
    }
}

function clearSearchText() {
    const input = document.getElementById('search-text');
    if (input) {
        input.value = '';
        toggleClearButton();
        applyFilters();
    }
}

function toggleClearButton() {
    const input = document.getElementById('search-text');
    const clearBtn = document.getElementById('clear-search-btn');
    if (clearBtn && input) {
        if (input.value.trim().length > 0) {
            clearBtn.classList.remove('hidden');
        } else {
            clearBtn.classList.add('hidden');
        }
    }
}

function applyFilters(resetPage = true) {
    if (resetPage) {
        currentPage = 1;
    }

    const searchInput = document.getElementById('search-text');
    const bnccSelect = document.getElementById('filter-bncc');
    const unidadeSelect = document.getElementById('filter-unidade');
    const anoSelect = document.getElementById('filter-ano');
    const instSelect = document.getElementById('filter-inst');

    const searchVal = (searchInput ? searchInput.value : '').toLowerCase().trim();
    const bnccVal = bnccSelect ? bnccSelect.value : '';
    const unidadeVal = unidadeSelect ? unidadeSelect.value : '';
    const anoVal = anoSelect ? anoSelect.value : '';
    const instVal = instSelect ? instSelect.value : '';

    filteredQuestions = allExamQuestions.filter(q => {
        if (bnccVal && q.bncc !== bnccVal) return false;
        if (unidadeVal && q.unidadeTematica !== unidadeVal) return false;
        if (anoVal && q.anoEscolar !== anoVal) return false;
        if (instVal && q.inst !== instVal) return false;

        if (searchVal) {
            const matchSearch = q.q.toLowerCase().includes(searchVal) ||
                                (q.explanation && q.explanation.toLowerCase().includes(searchVal)) ||
                                q.bncc.toLowerCase().includes(searchVal) ||
                                q.bnccDesc.toLowerCase().includes(searchVal) ||
                                q.examTitle.toLowerCase().includes(searchVal);
            if (!matchSearch) return false;
        }

        return true;
    });

    renderResults();
    updateUrlParams();
}

function updateUrlParams() {
    const params = new URLSearchParams();
    const searchInput = document.getElementById('search-text');
    const bnccSelect = document.getElementById('filter-bncc');
    const unidadeSelect = document.getElementById('filter-unidade');
    const anoSelect = document.getElementById('filter-ano');
    const instSelect = document.getElementById('filter-inst');

    const searchVal = searchInput ? searchInput.value.trim() : '';
    const bnccVal = bnccSelect ? bnccSelect.value : '';
    const unidadeVal = unidadeSelect ? unidadeSelect.value : '';
    const anoVal = anoSelect ? anoSelect.value : '';
    const instVal = instSelect ? instSelect.value : '';

    if (bnccVal) params.set('bncc', bnccVal);
    if (searchVal) params.set('q', searchVal);
    if (unidadeVal) params.set('unidade', unidadeVal);
    if (anoVal) params.set('ano', anoVal);
    if (instVal) params.set('instituto', instVal);
    if (currentPage > 1) params.set('page', currentPage);

    const newUrl = window.location.pathname + (params.toString() ? '?' + params.toString() : '');
    window.history.replaceState({}, '', newUrl);
}

function resetFilters() {
    if (document.getElementById('search-text')) document.getElementById('search-text').value = '';
    if (document.getElementById('filter-bncc')) document.getElementById('filter-bncc').value = '';
    if (document.getElementById('filter-unidade')) document.getElementById('filter-unidade').value = '';
    if (document.getElementById('filter-ano')) document.getElementById('filter-ano').value = '';
    if (document.getElementById('filter-inst')) document.getElementById('filter-inst').value = '';
    toggleClearButton();
    currentPage = 1;
    applyFilters(true);
}

function filterByBnccBadge(code) {
    const select = document.getElementById('filter-bncc');
    if (select) {
        select.value = code;
        currentPage = 1;
        applyFilters(true);
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

function normalizeDriveImageUrl(url) {
    if (!url) return '';
    const match = url.match(/(?:drive\.google\.com\/(?:file\/d\/|open\?id=|uc\?export=view&id=)|lh3\.googleusercontent\.com\/d\/)([a-zA-Z0-9_-]+)/);
    if (match) {
        return `https://lh3.googleusercontent.com/d/${match[1]}`;
    }
    return url;
}

function renderQuestionImageDarkHtml(q) {
    const imgData = q.image || q.imagem;
    if (!imgData) return '';
    
    const rawSrc = typeof imgData === 'string' ? imgData.trim() : (imgData.src || '').trim();
    if (!rawSrc) return '';
    
    const alt = typeof imgData === 'object' && imgData.alt ? imgData.alt.trim() : 'Figura da questão';
    const caption = typeof imgData === 'object' && imgData.caption ? imgData.caption.trim() : '';
    
    let src = rawSrc;
    if (rawSrc.includes('drive.google.com') || rawSrc.includes('lh3.googleusercontent.com')) {
        src = normalizeDriveImageUrl(rawSrc);
    } else if (!rawSrc.startsWith('http://') && !rawSrc.startsWith('https://') && !rawSrc.startsWith('data:')) {
        src = `./${rawSrc.replace(/^(\.\/|\/)/, '')}`;
    }
    
    const escapedAlt = alt.replace(/'/g, "\\'");
    return `
        <div class="my-4 p-2 sm:p-3 rounded-2xl border border-slate-800 bg-slate-950/70 shadow-sm max-w-xl mx-auto flex flex-col items-center">
            <img src="${src}" alt="${alt}" class="max-h-72 sm:max-h-96 w-auto max-w-full rounded-xl object-contain cursor-zoom-in hover:opacity-95 hover:scale-[1.01] transition duration-200" onclick="openImageModal('${src}', '${escapedAlt}')" title="Clique para ampliar a imagem" loading="lazy">
            ${caption ? `<p class="text-xs text-slate-400 mt-2 text-center italic">${caption}</p>` : ''}
        </div>
    `;
}

function renderResults() {
    const container = document.getElementById('questions-container');
    const counter = document.getElementById('results-count');
    const emptyState = document.getElementById('empty-state');
    const paginationContainer = document.getElementById('pagination-container');

    if (!container) return;

    const total = filteredQuestions.length;
    const totalPages = Math.ceil(total / ITEMS_PER_PAGE) || 1;

    if (currentPage > totalPages) currentPage = totalPages;
    if (currentPage < 1) currentPage = 1;

    const startIdx = (currentPage - 1) * ITEMS_PER_PAGE;
    const endIdx = Math.min(startIdx + ITEMS_PER_PAGE, total);

    if (counter) {
        if (total === 0) {
            counter.innerHTML = 'Nenhuma questão encontrada';
        } else if (total <= ITEMS_PER_PAGE) {
            counter.innerHTML = `<span class="text-sky-400 font-bold">${total}</span> ${total === 1 ? 'questão encontrada' : 'questões encontradas'}`;
        } else {
            counter.innerHTML = `<span class="text-sky-400 font-bold">${total}</span> questões encontradas <span class="text-slate-500">•</span> Exibindo <span class="text-emerald-400 font-bold">${startIdx + 1}–${endIdx}</span> (página <span class="text-sky-300 font-bold">${currentPage}</span> de ${totalPages})`;
        }
    }

    if (total === 0) {
        container.innerHTML = '';
        if (emptyState) emptyState.classList.remove('hidden');
        if (paginationContainer) paginationContainer.classList.add('hidden');
        return;
    }

    if (emptyState) emptyState.classList.add('hidden');

    const pageQuestions = filteredQuestions.slice(startIdx, endIdx);

    container.innerHTML = pageQuestions.map((q, idx) => {
        const qId = q.uniqueId;
        const instBadge = q.inst === 'IFCE' 
            ? 'bg-blue-500/20 text-sky-300 border-blue-400/30' 
            : q.inst === 'IFSC' 
                ? 'bg-indigo-500/20 text-indigo-300 border-indigo-400/30' 
                : q.inst === 'IFMG'
                    ? 'bg-emerald-500/20 text-emerald-300 border-emerald-400/30'
                    : 'bg-amber-500/20 text-amber-300 border-amber-400/30';

        const selectedOpt = pesquisaSelections[qId];
        const optionsHtml = (q.options || []).map((opt, optIdx) => {
            const letter = String.fromCharCode(65 + optIdx);
            const isSelected = (selectedOpt === optIdx);
            const selectedClass = isSelected ? 'opt-selected border-blue-500 bg-blue-950/40' : '';
            const iconName = isSelected ? 'check-circle' : 'circle';
            const iconClass = isSelected ? 'w-4 h-4 text-blue-400 opt-icon flex-shrink-0' : 'w-4 h-4 text-slate-600 opt-icon group-hover:text-blue-400 flex-shrink-0';
            return `
                <button onclick="selectPesquisaOption('${qId}', ${optIdx})" id="btn-${qId}-${optIdx}" class="w-full text-left p-3.5 rounded-xl border border-slate-800 bg-slate-950/60 hover:border-blue-500 hover:bg-slate-800/60 transition text-sm text-slate-200 flex items-start justify-between gap-3 group ${selectedClass}">
                    <span class="flex items-start gap-2.5 flex-1 min-w-0">
                        <strong class="text-sky-400 font-bold flex-shrink-0 mt-0.5">${letter})</strong>
                        <span class="flex-1 min-w-0 break-words leading-relaxed">${opt}</span>
                    </span>
                    <i data-lucide="${iconName}" class="${iconClass} mt-0.5"></i>
                </button>
            `;
        }).join('');

        // Link de teoria
        const theoryFolderMap = {
            '1': 'bloco-1-numeros',
            '2': 'bloco-2-algebra',
            '3': 'bloco-3-geometria',
            '4': 'bloco-4-medidas-e-estatistica'
        };

        let theoryLink = '';
        if (q.topicoId && q.topicoId.startsWith('b')) {
            const bNum = q.topicoId.charAt(1);
            const folder = theoryFolderMap[bNum] || 'bloco-1-numeros';
            theoryLink = `
                <a href="./${folder}/index.html" target="_blank" class="text-xs text-sky-400 hover:text-sky-300 transition flex items-center gap-1.5" title="Revisar teoria deste bloco">
                    <i data-lucide="book-open" class="w-3.5 h-3.5"></i> Revisar Teoria
                </a>
            `;
        }

        return `
            <div class="exam-question-card bg-slate-900/90 border border-slate-800 rounded-2xl p-6 sm:p-7 shadow-xl space-y-4" id="card-${qId}">
                
                <!-- Cabeçalho com Localização da Prova e Selos BNCC -->
                <div class="flex flex-wrap items-center justify-between gap-2.5 pb-3 border-b border-slate-800/80">
                    <div class="flex flex-wrap items-center gap-2">
                        <!-- Onde se localiza -->
                        <a href="${q.examUrl}#q-container-${qId}" target="_blank" class="inline-flex items-center gap-1.5 px-3 py-1 rounded-xl text-xs font-extrabold bg-blue-950/90 text-sky-300 border border-blue-700/60 hover:bg-blue-900 transition shadow-sm group" title="Abrir na prova original completa">
                            <i data-lucide="archive" class="w-3.5 h-3.5 text-sky-400"></i>
                            <span>${q.examTitle} — Questão ${q.qNumber}</span>
                            <i data-lucide="external-link" class="w-3 h-3 opacity-70 group-hover:opacity-100"></i>
                        </a>

                        <!-- Selo do Instituto -->
                        <span class="text-[11px] font-bold px-2 py-0.5 rounded-md border ${instBadge}">
                            ${q.inst}
                        </span>
                    </div>

                    <div class="flex items-center gap-2 ml-auto">
                        <!-- Selo BNCC Clicável -->
                        <button onclick="filterByBnccBadge('${q.bncc}')" class="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-mono font-bold bg-emerald-950/90 text-emerald-300 border border-emerald-700/60 hover:bg-emerald-900 transition cursor-pointer shadow-sm" title="Clique para filtrar apenas esta habilidade">
                            <i data-lucide="bookmark" class="w-3 h-3 text-emerald-400"></i> BNCC: ${q.bncc}
                        </button>
                        ${theoryLink}
                    </div>
                </div>

                <!-- Descritor Oficial da Habilidade -->
                <div class="bg-slate-950/70 border border-slate-800/90 rounded-xl p-3 text-xs flex items-start gap-2 text-slate-300 leading-relaxed">
                    <i data-lucide="info" class="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5"></i>
                    <div>
                        <span class="font-bold text-emerald-400">[${q.unidadeTematica} • ${q.anoEscolar}]</span> ${q.bnccDesc}
                    </div>
                </div>

                <!-- Enunciado da Questão -->
                <p class="font-medium text-slate-100 text-sm sm:text-base leading-relaxed">
                    ${q.q}
                </p>

                ${renderQuestionImageDarkHtml(q)}

                <!-- Alternativas -->
                <div class="space-y-2" id="opts-${qId}">
                    ${optionsHtml}
                </div>

                <!-- Ações -->
                <div class="flex items-center justify-between gap-3 pt-2">
                    <button id="submit-btn-${qId}" onclick="submitPesquisaAnswer('${qId}', ${q.correct})" class="bg-blue-600 hover:bg-blue-500 text-white px-5 py-2.5 rounded-xl text-xs sm:text-sm font-bold transition flex items-center gap-1.5 shadow-md shadow-blue-600/25">
                        <i data-lucide="send" class="w-4 h-4"></i> Verificar Resposta
                    </button>
                    <a href="${q.examUrl}#q-container-${qId}" target="_blank" class="text-xs text-slate-400 hover:text-sky-300 flex items-center gap-1 transition">
                        <i data-lucide="file-text" class="w-3.5 h-3.5"></i> Caderno da Prova Completa &rarr;
                    </a>
                </div>

                <!-- Feedback / Resolução Comentada -->
                <div id="feedback-${qId}" class="hidden p-4 rounded-xl text-sm mt-3"></div>
            </div>
        `;
    }).join('');

    renderPagination(totalPages, total, startIdx, endIdx);

    if (window.lucide) lucide.createIcons();
    if (window.renderLatex) renderLatex(container);
}

function renderPagination(totalPages, total, startIdx, endIdx) {
    const paginationContainer = document.getElementById('pagination-container');
    const paginationInfo = document.getElementById('pagination-info');
    const paginationControls = document.getElementById('pagination-controls');

    if (!paginationContainer || !paginationControls) return;

    if (totalPages <= 1) {
        paginationContainer.classList.add('hidden');
        return;
    }

    paginationContainer.classList.remove('hidden');

    if (paginationInfo) {
        paginationInfo.innerHTML = `Mostrando <strong class="text-slate-200">${startIdx + 1}</strong> a <strong class="text-slate-200">${endIdx}</strong> de <strong class="text-slate-200">${total}</strong> questões`;
    }

    const pagesToShow = [];
    const maxVisibleButtons = 7;

    if (totalPages <= maxVisibleButtons) {
        for (let i = 1; i <= totalPages; i++) pagesToShow.push(i);
    } else {
        pagesToShow.push(1);
        if (currentPage > 3) {
            pagesToShow.push('...');
        }

        const startRange = Math.max(2, currentPage - 1);
        const endRange = Math.min(totalPages - 1, currentPage + 1);

        for (let i = startRange; i <= endRange; i++) {
            pagesToShow.push(i);
        }

        if (currentPage < totalPages - 2) {
            pagesToShow.push('...');
        }
        pagesToShow.push(totalPages);
    }

    let controlsHtml = '';

    // Botão Anterior
    const prevDisabled = currentPage === 1;
    controlsHtml += `
        <button 
            onclick="changePage(${currentPage - 1})" 
            ${prevDisabled ? 'disabled' : ''} 
            class="px-3 py-1.5 rounded-xl text-xs sm:text-sm font-semibold bg-slate-900 border border-slate-800 text-slate-300 hover:bg-slate-800 hover:text-white transition disabled:opacity-30 disabled:cursor-not-allowed disabled:hover:bg-slate-900 disabled:hover:text-slate-300 flex items-center gap-1 shadow-sm cursor-pointer"
            aria-label="Página anterior">
            <i data-lucide="chevron-left" class="w-4 h-4"></i>
            <span class="hidden sm:inline">Anterior</span>
        </button>
    `;

    // Botões de Páginas
    pagesToShow.forEach(p => {
        if (p === '...') {
            controlsHtml += `<span class="px-2 py-1 text-slate-500 font-bold select-none text-xs sm:text-sm">…</span>`;
        } else {
            const isActive = p === currentPage;
            if (isActive) {
                controlsHtml += `
                    <button class="px-3.5 py-1.5 rounded-xl text-xs sm:text-sm font-bold bg-blue-600 border border-blue-500 text-white shadow-md shadow-blue-600/30 cursor-default" aria-current="page">
                        ${p}
                    </button>
                `;
            } else {
                controlsHtml += `
                    <button onclick="changePage(${p})" class="px-3.5 py-1.5 rounded-xl text-xs sm:text-sm font-medium bg-slate-900 border border-slate-800 text-slate-300 hover:bg-slate-800 hover:text-white transition shadow-sm cursor-pointer">
                        ${p}
                    </button>
                `;
            }
        }
    });

    // Botão Próxima
    const nextDisabled = currentPage === totalPages;
    controlsHtml += `
        <button 
            onclick="changePage(${currentPage + 1})" 
            ${nextDisabled ? 'disabled' : ''} 
            class="px-3 py-1.5 rounded-xl text-xs sm:text-sm font-semibold bg-slate-900 border border-slate-800 text-slate-300 hover:bg-slate-800 hover:text-white transition disabled:opacity-30 disabled:cursor-not-allowed disabled:hover:bg-slate-900 disabled:hover:text-slate-300 flex items-center gap-1 shadow-sm cursor-pointer"
            aria-label="Próxima página">
            <span class="hidden sm:inline">Próxima</span>
            <i data-lucide="chevron-right" class="w-4 h-4"></i>
        </button>
    `;

    paginationControls.innerHTML = controlsHtml;
}

function changePage(newPage) {
    currentPage = newPage;
    renderResults();
    updateUrlParams();

    const target = document.getElementById('search-form') || document.getElementById('questions-container');
    if (target) {
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

function selectPesquisaOption(qId, optIdx) {
    pesquisaSelections[qId] = optIdx;
    const parent = document.getElementById(`opts-${qId}`);
    if (!parent) return;

    const buttons = parent.querySelectorAll('button');
    buttons.forEach(btn => {
        btn.classList.remove('opt-selected', 'border-blue-500', 'bg-blue-950/40');
        const icon = btn.querySelector('.opt-icon');
        if (icon) {
            icon.setAttribute('data-lucide', 'circle');
            icon.className = 'w-4 h-4 text-slate-600 opt-icon group-hover:text-blue-400 flex-shrink-0';
        }
    });

    const selectedBtn = document.getElementById(`btn-${qId}-${optIdx}`);
    if (selectedBtn) {
        selectedBtn.classList.add('opt-selected', 'border-blue-500', 'bg-blue-950/40');
        const icon = selectedBtn.querySelector('.opt-icon');
        if (icon) {
            icon.setAttribute('data-lucide', 'check-circle');
            icon.className = 'w-4 h-4 text-blue-400 opt-icon flex-shrink-0';
        }
    }
    if (window.lucide) lucide.createIcons();
}

function submitPesquisaAnswer(qId, correctIdx) {
    if (pesquisaSelections[qId] === undefined) {
        if (window.showToast) showToast('Selecione uma alternativa antes de verificar!', 'info');
        else alert('Selecione uma alternativa antes de verificar!');
        return;
    }

    const qObj = allExamQuestions.find(q => q.uniqueId === qId);
    const explanation = qObj ? (qObj.explanation || 'Resolução não informada.') : '';

    const selected = pesquisaSelections[qId];
    const isCorrect = (selected === correctIdx);
    const feedbackDiv = document.getElementById(`feedback-${qId}`);
    const parent = document.getElementById(`opts-${qId}`);

    if (parent) {
        const buttons = parent.querySelectorAll('button');
        buttons.forEach((btn, idx) => {
            btn.disabled = true;
            btn.classList.remove('border-blue-500', 'bg-blue-950/40');
            if (idx === correctIdx) {
                btn.classList.add('border-emerald-500', 'bg-emerald-950/50', 'text-emerald-200');
            } else if (idx === selected && !isCorrect) {
                btn.classList.add('border-rose-500', 'bg-rose-950/50', 'text-rose-200');
            }
        });
    }

    if (feedbackDiv) {
        feedbackDiv.classList.remove('hidden');
        if (isCorrect) {
            feedbackDiv.className = 'p-4 rounded-xl text-sm mt-3 bg-emerald-950/60 border border-emerald-800/80 text-emerald-200';
            feedbackDiv.innerHTML = `
                <div class="flex items-center gap-2 font-bold mb-2 text-emerald-400">
                    <i data-lucide="check-circle-2" class="w-5 h-5"></i> Resposta Correta! Parabéns!
                </div>
                <div class="leading-relaxed text-slate-200">${explanation}</div>
            `;
            if (window.showToast) showToast('Resposta Correta!', 'success');
        } else {
            feedbackDiv.className = 'p-4 rounded-xl text-sm mt-3 bg-rose-950/60 border border-rose-800/80 text-rose-200';
            feedbackDiv.innerHTML = `
                <div class="flex items-center gap-2 font-bold mb-2 text-rose-400">
                    <i data-lucide="x-circle" class="w-5 h-5"></i> Resposta Incorreta.
                </div>
                <div class="leading-relaxed text-slate-200 mb-2">A resposta correta é a alternativa <strong>${String.fromCharCode(65 + correctIdx)}</strong>.</div>
                <div class="leading-relaxed text-slate-300 text-xs sm:text-sm">${explanation}</div>
            `;
            if (window.showToast) showToast('Resposta Incorreta. Veja a resolução!', 'error');
        }

        if (window.lucide) lucide.createIcons();
        if (window.renderLatex) renderLatex(feedbackDiv);
    }
}
