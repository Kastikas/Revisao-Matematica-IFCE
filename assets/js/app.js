/**
 * PartiuIF - Plataforma de Matemática (Motor Multi-páginas)
 * Gerenciamento de Estado, KaTeX, Toasts, Exercícios e Progresso
 */

// Estado Global
var completedTopics = window.completedTopics || JSON.parse(localStorage.getItem('partiuif_completed') || '[]');
var savedAnswers = window.savedAnswers || JSON.parse(localStorage.getItem('partiuif_answers') || '{}');
var userSelections = window.userSelections || {};

// Função Universal KaTeX
function renderLatex(element) {
    const target = element || document.body;
    if (window.renderMathInElement) {
        renderMathInElement(target, {
            delimiters: [
                { left: "$$", right: "$$", display: true },
                { left: "$", right: "$", display: false }
            ],
            throwOnError: false
        });
    }
}

// Sistema de Toasts
function showToast(message, type = "success") {
    let container = document.getElementById("toast-container");
    if (!container) {
        container = document.createElement("div");
        container.id = "toast-container";
        container.className = "fixed bottom-5 right-5 z-50 flex flex-col gap-2 pointer-events-none";
        document.body.appendChild(container);
    }
    
    const toast = document.createElement("div");
    let icon = "check-circle";
    let bgClass = "bg-brand-50 border-brand-200 text-brand-900";
    let iconClass = "text-brand-600";

    if (type === "info") {
        icon = "info";
        bgClass = "bg-blue-50 border-blue-200 text-blue-900";
        iconClass = "text-blue-600";
    } else if (type === "error") {
        icon = "alert-triangle";
        bgClass = "bg-red-50 border-red-200 text-red-900";
        iconClass = "text-red-600";
    }

    toast.className = `toast-enter pointer-events-auto flex items-center gap-3 p-4 rounded-xl border shadow-lg ${bgClass} font-medium text-sm transition-all duration-300`;
    toast.innerHTML = `<i data-lucide="${icon}" class="w-5 h-5 ${iconClass} flex-shrink-0"></i> <span>${message}</span>`;
    
    container.appendChild(toast);
    if (window.lucide) lucide.createIcons();

    setTimeout(() => {
        toast.style.opacity = "0";
        toast.style.transform = "translateX(100%)";
        setTimeout(() => toast.remove(), 300);
    }, 3200);
}

// Resolução de Exercícios
function selectOption(qId, optIdx) {
    if (savedAnswers.hasOwnProperty(qId)) return; // já respondida
    userSelections[qId] = optIdx;
    
    const isDark = document.body.classList.contains("dark") || document.body.getAttribute("data-theme") === "dark";
    const parent = document.getElementById(`opts-${qId}`);
    if (!parent) return;
    
    const buttons = parent.querySelectorAll("button");
    buttons.forEach(btn => {
        btn.classList.remove("opt-selected", "border-brand-500", "bg-brand-50", "border-blue-500", "bg-blue-950/40");
        const icon = btn.querySelector(".opt-icon");
        if (icon) {
            icon.setAttribute("data-lucide", "circle");
            icon.className = isDark ? "w-4 h-4 text-slate-500 opt-icon group-hover:text-blue-400" : "w-4 h-4 text-gray-300 opt-icon group-hover:text-brand-400";
        }
    });

    const selectedBtn = document.getElementById(`btn-${qId}-${optIdx}`);
    if (selectedBtn) {
        selectedBtn.classList.add("opt-selected");
        if (isDark) {
            selectedBtn.classList.add("border-blue-500", "bg-blue-950/40");
        }
        const selectedIcon = selectedBtn.querySelector(".opt-icon");
        if (selectedIcon) {
            selectedIcon.setAttribute("data-lucide", "check-circle");
            selectedIcon.className = isDark ? "w-4 h-4 text-blue-400 opt-icon" : "w-4 h-4 text-brand-600 opt-icon";
        }
    }
    if (window.lucide) lucide.createIcons();
}

function submitAnswer(blockId, topicId, qIdx) {
    const qId = `${topicId}-q${qIdx}`;
    if (userSelections[qId] === undefined) {
        showToast("Selecione uma alternativa antes de enviar!", "info");
        return;
    }

    const block = mathData[blockId];
    if (!block) return;
    const topic = block.topics.find(t => t.id === topicId);
    if (!topic) return;
    const question = topic.questions[qIdx];
    if (!question) return;

    const selected = userSelections[qId];
    const isCorrect = (selected === question.correct);

    // Salva no localStorage
    savedAnswers[qId] = { opt: selected, correct: isCorrect };
    localStorage.setItem("partiuif_answers", JSON.stringify(savedAnswers));
    
    if (isCorrect) {
        showToast("Resposta correta! Parabéns!", "success");
    } else {
        showToast("Resposta incorreta. Veja a explicação detalhada.", "error");
    }

    applyQuestionResultUI(qId, question, selected, isCorrect);
    updateGlobalProgress();
}

function applyQuestionResultUI(qId, question, selectedOpt, isCorrect) {
    const isDark = document.body.classList.contains("dark") || document.body.getAttribute("data-theme") === "dark";
    const feedbackDiv = document.getElementById(`feedback-${qId}`);
    if (feedbackDiv) {
        if (isCorrect) {
            if (isDark) {
                feedbackDiv.className = "p-4 rounded-xl text-sm mt-4 border bg-emerald-950/50 border-emerald-500/40 text-emerald-200";
                feedbackDiv.innerHTML = `<div class="flex items-center gap-1.5 font-bold text-emerald-400 mb-1"><i data-lucide="check-circle" class="w-4 h-4 text-emerald-400"></i> Correto!</div><div class="text-emerald-100 leading-relaxed">${question.explanation}</div>`;
            } else {
                feedbackDiv.className = "p-4 rounded-xl text-sm mt-4 border bg-green-50 border-green-200 text-green-900";
                feedbackDiv.innerHTML = `<div class="flex items-center gap-1.5 font-bold text-green-800 mb-1"><i data-lucide="check-circle" class="w-4 h-4 text-green-600"></i> Correto!</div><div class="text-green-800 leading-relaxed">${question.explanation}</div>`;
            }
        } else {
            if (isDark) {
                feedbackDiv.className = "p-4 rounded-xl text-sm mt-4 border bg-rose-950/50 border-rose-500/40 text-rose-200";
                feedbackDiv.innerHTML = `<div class="flex items-center gap-1.5 font-bold text-rose-400 mb-1"><i data-lucide="x-circle" class="w-4 h-4 text-rose-400"></i> Incorreto.</div><div class="text-rose-100 leading-relaxed">A resposta correta é a <strong class="text-white">Letra ${String.fromCharCode(65 + question.correct)}</strong>.<br><div class="mt-1">${question.explanation}</div></div>`;
            } else {
                feedbackDiv.className = "p-4 rounded-xl text-sm mt-4 border bg-red-50 border-red-200 text-red-900";
                feedbackDiv.innerHTML = `<div class="flex items-center gap-1.5 font-bold text-red-800 mb-1"><i data-lucide="x-circle" class="w-4 h-4 text-red-600"></i> Incorreto.</div><div class="text-red-900 leading-relaxed">A resposta correta é a <strong>Letra ${String.fromCharCode(65 + question.correct)}</strong>.<br><div class="mt-1">${question.explanation}</div></div>`;
            }
        }
        feedbackDiv.classList.remove("hidden");
        renderLatex(feedbackDiv);
    }

    const parent = document.getElementById(`opts-${qId}`);
    if (parent) {
        const buttons = parent.querySelectorAll("button");
        buttons.forEach((btn, idx) => {
            btn.disabled = true;
            btn.classList.remove("border-brand-500", "bg-brand-50", "border-blue-500", "bg-blue-950/40", "hover:border-brand-300", "group");
            btn.classList.add("cursor-not-allowed");
            
            const icon = btn.querySelector(".opt-icon");
            if (idx === selectedOpt) {
                if (isCorrect) {
                    btn.classList.add("opt-selected");
                    if (isDark) {
                        btn.classList.add("border-emerald-500", "bg-emerald-950/40", "text-emerald-200");
                    }
                    if (icon) {
                        icon.setAttribute("data-lucide", "check-circle");
                        icon.className = isDark ? "w-4 h-4 text-emerald-400 opt-icon" : "w-4 h-4 text-brand-600 opt-icon";
                    }
                } else {
                    btn.classList.add("opt-wrong");
                    if (isDark) {
                        btn.classList.add("border-rose-500", "bg-rose-950/40", "text-rose-200");
                    }
                    if (icon) {
                        icon.setAttribute("data-lucide", "x-circle");
                        icon.className = isDark ? "w-4 h-4 text-rose-400 opt-icon" : "w-4 h-4 text-red-600 opt-icon";
                    }
                }
            } else if (idx === question.correct) {
                if (isDark) {
                    btn.classList.add("border-emerald-500/60", "bg-emerald-950/30", "text-emerald-200", "font-medium");
                } else {
                    btn.classList.add("border-brand-400", "bg-emerald-50/70", "font-medium");
                }
                if (icon) {
                    icon.setAttribute("data-lucide", "check");
                    icon.className = isDark ? "w-4 h-4 text-emerald-400 opt-icon" : "w-4 h-4 text-brand-600 opt-icon";
                }
            } else {
                btn.classList.add("opacity-40");
            }
        });
    }

    const submitBtn = document.getElementById(`submit-btn-${qId}`);
    if (submitBtn) {
        submitBtn.style.display = "none";
    }

    if (window.lucide) lucide.createIcons();
}

// Inicializar respostas já salvas
function initQuestionStates(topicId, blockId) {
    if (!topicId || !blockId || !window.mathData) return;
    const block = mathData[blockId];
    if (!block) return;
    const topic = block.topics.find(t => t.id === topicId);
    if (!topic) return;

    topic.questions.forEach((q, qIdx) => {
        const qId = `${topicId}-q${qIdx}`;
        if (savedAnswers.hasOwnProperty(qId)) {
            const saved = savedAnswers[qId];
            applyQuestionResultUI(qId, q, saved.opt, saved.correct);
        }
    });
}

// Conclusão de Tópicos
function toggleTopicDone(topicId) {
    if (completedTopics.includes(topicId)) {
        completedTopics = completedTopics.filter(id => id !== topicId);
        showToast("Marcador de conclusão removido.", "info");
    } else {
        completedTopics.push(topicId);
        showToast("Prova/Tópico concluído com sucesso!", "success");
    }
    localStorage.setItem("partiuif_completed", JSON.stringify(completedTopics));
    
    updateTopicDoneButtonUI(topicId);
    updateGlobalProgress();
}

function updateTopicDoneButtonUI(topicId) {
    const btn = document.getElementById(`btn-toggle-done-${topicId}`);
    const isDone = completedTopics.includes(topicId);
    const isDark = document.body.classList.contains("dark") || document.body.getAttribute("data-theme") === "dark";
    if (btn) {
        if (isDone) {
            if (isDark) {
                btn.className = "px-4 py-2 rounded-xl text-sm font-semibold border bg-blue-900/40 text-blue-200 border-blue-600 hover:bg-blue-900/60 transition flex items-center gap-2 shadow-sm";
                btn.innerHTML = `<i data-lucide="check-square" class="w-4 h-4 text-blue-400"></i> Prova Concluída`;
            } else {
                btn.className = "px-4 py-2 rounded-xl text-sm font-semibold border bg-brand-100 text-brand-900 border-brand-300 hover:bg-brand-200 transition flex items-center gap-2 shadow-sm";
                btn.innerHTML = `<i data-lucide="check-square" class="w-4 h-4 text-brand-700"></i> Concluído`;
            }
        } else {
            if (isDark) {
                btn.className = "px-4 py-2 rounded-xl text-sm font-semibold border bg-slate-900 text-slate-300 border-slate-700 hover:bg-slate-800 transition flex items-center gap-2 shadow-sm";
                btn.innerHTML = `<i data-lucide="square" class="w-4 h-4 text-slate-500"></i> Marcar como Concluída`;
            } else {
                btn.className = "px-4 py-2 rounded-xl text-sm font-semibold border bg-white text-gray-700 border-gray-300 hover:bg-gray-50 transition flex items-center gap-2 shadow-sm";
                btn.innerHTML = `<i data-lucide="square" class="w-4 h-4 text-gray-400"></i> Marcar como Concluído`;
            }
        }
        if (window.lucide) lucide.createIcons();
    }
}

// Progresso Geral
function updateGlobalProgress() {
    if (!window.mathData) return;
    
    let totalTopics = 0;
    let totalQuestions = 0;
    let answeredQuestions = Object.keys(savedAnswers).length;
    let correctAnswers = 0;
    
    for (let k in savedAnswers) {
        if (savedAnswers[k].correct) correctAnswers++;
    }

    for (let bId in mathData) {
        const block = mathData[bId];
        totalTopics += block.topics.length;
        
        let completedInBlock = 0;
        block.topics.forEach(t => {
            totalQuestions += t.questions.length;
            const isDone = completedTopics.includes(t.id);
            if (isDone) completedInBlock++;

            // Atualiza ícones em listas de tópicos (se presentes na página)
            const iconEl = document.getElementById(`status-icon-${t.id}`);
            if (iconEl) {
                if (isDone) {
                    iconEl.setAttribute("data-lucide", "check-circle-2");
                    iconEl.className = "w-5 h-5 text-brand-600 flex-shrink-0";
                } else {
                    iconEl.setAttribute("data-lucide", "circle");
                    iconEl.className = "w-5 h-5 text-gray-300 flex-shrink-0";
                }
            }

            const badgeEl = document.getElementById(`status-badge-${t.id}`);
            if (badgeEl) {
                if (isDone) {
                    badgeEl.className = "text-xs font-semibold px-2 py-0.5 rounded-full bg-brand-100 text-brand-800 border border-brand-200 flex items-center gap-1";
                    badgeEl.innerHTML = `<i data-lucide="check" class="w-3 h-3 text-brand-700"></i> Concluído`;
                } else {
                    badgeEl.className = "text-xs font-medium px-2 py-0.5 rounded-full bg-gray-100 text-gray-600 border border-gray-200";
                    badgeEl.innerHTML = `Pendente`;
                }
            }
        });

        // Atualiza barras de progresso de bloco (se presentes)
        const blockPercent = Math.round((completedInBlock / block.topics.length) * 100);
        const blockProgressBar = document.getElementById(`block-progress-bar-${bId}`);
        const blockProgressTxt = document.getElementById(`block-progress-txt-${bId}`);
        if (blockProgressBar) blockProgressBar.style.width = `${blockPercent}%`;
        if (blockProgressTxt) blockProgressTxt.innerText = `${blockPercent}% (${completedInBlock}/${block.topics.length})`;
    }

    const percent = totalTopics > 0 ? Math.round((completedTopics.length / totalTopics) * 100) : 0;
    
    // Atualiza rodapé
    const footerBar = document.getElementById("footer-progress");
    const footerTxt = document.getElementById("footer-progress-text");
    if (footerBar) footerBar.style.width = `${percent}%`;
    if (footerTxt) footerTxt.innerText = `${percent}% concluído (${completedTopics.length}/${totalTopics} tópicos)`;

    // Atualiza badges no cabeçalho ou dashboard se existirem
    const globalCountEl = document.getElementById("global-completed-count");
    if (globalCountEl) globalCountEl.innerText = `${completedTopics.length}/${totalTopics}`;
    
    const globalPercentEl = document.getElementById("global-percent");
    if (globalPercentEl) globalPercentEl.innerText = `${percent}%`;
    
    const globalQuestionsEl = document.getElementById("global-answered-questions");
    if (globalQuestionsEl) globalQuestionsEl.innerText = `${answeredQuestions}/${totalQuestions}`;

    const globalExamsEl = document.getElementById("global-official-exams");
    if (globalExamsEl) {
        let totalOfficial = 0;
        for (let examBlockId in mathData) {
            const titleLower = (mathData[examBlockId].title || "").toLowerCase();
            if (titleLower.includes("provas") || titleLower.includes("oficiais")) {
                totalOfficial += mathData[examBlockId].topics.length;
            }
        }
        globalExamsEl.innerText = `${totalOfficial} Edições`;
    }

    if (window.lucide) lucide.createIcons();
}

function resetProgress() {
    if (confirm("ATENÇÃO: Você tem certeza que deseja zerar TODAS as suas respostas e tópicos concluídos? Essa ação não pode ser desfeita.")) {
        localStorage.removeItem("partiuif_completed");
        localStorage.removeItem("partiuif_answers");
        completedTopics = [];
        savedAnswers = {};
        showToast("Todo o progresso foi zerado com sucesso!", "info");
        setTimeout(() => {
            window.location.reload();
        }, 600);
    }
}

// Localizador Rápido de Subtópicos
function initTopicSearch() {
    const searchInput = document.getElementById('topic-search-input');
    const searchResults = document.getElementById('search-results-container');

    if (!searchInput || !searchResults || !window.mathData) return;

    const allTopicsList = [];
    for (let bId in mathData) {
        const block = mathData[bId];
        const defaultFolder = block.folder || (block.topics[0] && block.topics[0].folder) || `bloco-${bId}`;
        block.topics.forEach(t => {
            allTopicsList.push({
                id: t.id,
                title: t.title,
                bncc: t.bncc || '',
                summary: t.summary || '',
                folder: t.folder || defaultFolder,
                filename: t.filename,
                blockTitle: block.title
            });
        });
    }

    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase().trim();
        if (!query) {
            searchResults.classList.add('hidden');
            searchResults.innerHTML = '';
            return;
        }

        const filtered = allTopicsList.filter(t => 
            t.title.toLowerCase().includes(query) || 
            t.bncc.toLowerCase().includes(query) || 
            t.summary.toLowerCase().includes(query) ||
            t.blockTitle.toLowerCase().includes(query)
        );

        if (filtered.length === 0) {
            searchResults.classList.remove('hidden');
            searchResults.innerHTML = '<div class="col-span-full p-4 text-center text-xs text-gray-500 bg-gray-50 rounded-xl">Nenhum subtópico encontrado com esse termo.</div>';
        } else {
            searchResults.classList.remove('hidden');
            searchResults.innerHTML = filtered.map(t => `
                <a href="./${t.folder}/${t.filename}" class="p-3 rounded-xl border border-brand-200 hover:border-brand-500 bg-brand-50/40 hover:bg-brand-50 transition flex items-center justify-between group">
                    <div>
                        <span class="text-[10px] font-bold text-brand-700 uppercase block">${t.blockTitle}</span>
                        <strong class="text-xs sm:text-sm font-semibold text-gray-900 group-hover:text-brand-900">${t.title}</strong>
                    </div>
                    <i data-lucide="arrow-right" class="w-4 h-4 text-brand-600 flex-shrink-0"></i>
                </a>
            `).join('');
            if (window.lucide) lucide.createIcons();
        }
    });
}

// Configurações e Menu Mobile
function initMobileMenu() {
    const btn = document.getElementById("mobile-menu-btn");
    const menu = document.getElementById("mobile-menu");
    if (btn && menu) {
        btn.addEventListener("click", () => {
            menu.classList.toggle("hidden");
        });
    }
}

// Execução ao carregar a página
document.addEventListener("DOMContentLoaded", () => {
    initMobileMenu();
    initTopicSearch();
    if (window.lucide) lucide.createIcons();
    renderLatex();
    updateGlobalProgress();
});
