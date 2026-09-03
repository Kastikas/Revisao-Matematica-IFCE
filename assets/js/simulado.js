/**
 * PartiuIF - Motor de Simulado Oficial de Matemática
 * Gerencia o ciclo completo do simulado: configuração, embaralhamento,
 * navegação, correção automática e análise de desempenho.
 */

let currentSimQuestions = [];
let currentSimAnswers = {}; // idx -> selectedOptionIndex
let currentSimIndex = 0;

/**
 * Embaralhamento uniforme de Fisher-Yates (Knuth Shuffle)
 */
function shuffleArray(array) {
    const arr = [...array];
    for (let i = arr.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
}

/**
 * Inicia o simulado com base nas opções selecionadas pelo usuário
 */
function startSimulado() {
    const sourceRadio = document.querySelector('input[name="sim-source"]:checked');
    const countRadio = document.querySelector('input[name="sim-count"]:checked');

    if (!sourceRadio || !countRadio) return;

    const source = sourceRadio.value;
    const count = parseInt(countRadio.value, 10);

    let questionPool = [];
    for (let bId in mathData) {
        if (source === "all" || source === bId) {
            const block = mathData[bId];
            block.topics.forEach(t => {
                t.questions.forEach((q, qIdx) => {
                    questionPool.push({
                        ...q,
                        blockId: bId,
                        blockTitle: block.title,
                        topicId: t.id,
                        topicTitle: t.title,
                        originalQIdx: qIdx
                    });
                });
            });
        }
    }

    if (questionPool.length === 0) {
        showToast("Nenhuma questão encontrada para os critérios selecionados.", "error");
        return;
    }

    // Embaralhamento uniforme de Fisher-Yates
    questionPool = shuffleArray(questionPool);
    currentSimQuestions = questionPool.slice(0, Math.min(count, questionPool.length));
    currentSimAnswers = {};
    currentSimIndex = 0;

    const setupContainer = document.getElementById('simulado-setup');
    const resultsContainer = document.getElementById('simulado-results');
    const runningContainer = document.getElementById('simulado-running');

    if (setupContainer) setupContainer.classList.add('hidden');
    if (resultsContainer) resultsContainer.classList.add('hidden');
    if (runningContainer) runningContainer.classList.remove('hidden');

    renderSimQuestionPalette();
    renderCurrentSimQuestion();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

/**
 * Renderiza a paleta de navegação numerada das questões do simulado
 */
function renderSimQuestionPalette() {
    const palette = document.getElementById('sim-palette');
    if (!palette) return;

    palette.innerHTML = currentSimQuestions.map((_, idx) => {
        const isAnswered = currentSimAnswers.hasOwnProperty(idx);
        const isCurrent = (idx === currentSimIndex);
        let btnClasses = "w-8 h-8 rounded-lg text-xs font-bold transition flex items-center justify-center ";

        if (isCurrent) {
            btnClasses += "ring-2 ring-brand-600 bg-brand-600 text-white shadow-md ";
        } else if (isAnswered) {
            btnClasses += "bg-brand-100 text-brand-900 border border-brand-300 ";
        } else {
            btnClasses += "bg-gray-100 text-gray-700 hover:bg-gray-200 ";
        }

        return `<button onclick="jumpToSimQuestion(${idx})" class="${btnClasses}" aria-label="Ir para a questão ${idx + 1}">${idx + 1}</button>`;
    }).join('');
}

/**
 * Renderiza o card da questão atual do simulado
 */
function renderCurrentSimQuestion() {
    const q = currentSimQuestions[currentSimIndex];
    if (!q) return;

    const qContainer = document.getElementById('sim-question-card');
    const indicator = document.getElementById('sim-progress-indicator');
    const topicTitle = document.getElementById('sim-topic-title');

    if (indicator) indicator.innerText = `Questão ${currentSimIndex + 1} de ${currentSimQuestions.length}`;
    if (topicTitle) topicTitle.innerHTML = `${q.blockTitle} &bull; ${q.topicTitle}`;

    const selectedOpt = currentSimAnswers[currentSimIndex];

    let optionsHtml = q.options.map((opt, optIdx) => {
        const letter = String.fromCharCode(65 + optIdx);
        const isSelected = (selectedOpt === optIdx);
        const activeClass = isSelected ? "opt-selected" : "border-gray-200 hover:border-brand-300 hover:bg-brand-50/30";
        const iconName = isSelected ? "check-circle" : "circle";
        const iconClass = isSelected ? "w-4 h-4 text-brand-600 opt-icon" : "w-4 h-4 text-gray-300 opt-icon";

        return `
            <button onclick="selectSimAnswer(${currentSimIndex}, ${optIdx})" class="w-full text-left p-3.5 rounded-xl border ${activeClass} transition text-sm text-gray-700 flex items-center justify-between group">
                <span class="flex items-center gap-2"><strong class="text-brand-700 font-bold">${letter})</strong> ${opt}</span>
                <i data-lucide="${iconName}" class="${iconClass}"></i>
            </button>
        `;
    }).join('');

    if (qContainer) {
        qContainer.innerHTML = `
            <div class="mb-2">
                <span class="text-xs font-bold text-gray-400 uppercase tracking-wider block mb-2">${q.topicTitle}</span>
                <p class="font-medium text-gray-800 text-base leading-relaxed mb-6">${q.q}</p>
            </div>
            <div class="space-y-2.5 mb-2">
                ${optionsHtml}
            </div>
        `;
    }

    // Controle dos botões anterior/próximo
    const prevBtn = document.getElementById('sim-prev-btn');
    const nextBtn = document.getElementById('sim-next-btn');

    if (prevBtn) {
        if (currentSimIndex === 0) {
            prevBtn.classList.add('opacity-50', 'pointer-events-none');
        } else {
            prevBtn.classList.remove('opacity-50', 'pointer-events-none');
        }
    }

    if (nextBtn) {
        if (currentSimIndex === currentSimQuestions.length - 1) {
            nextBtn.innerHTML = `Finalizar <i data-lucide="check" class="w-4 h-4"></i>`;
            nextBtn.onclick = finishSimulado;
        } else {
            nextBtn.innerHTML = `Próxima <i data-lucide="arrow-right" class="w-4 h-4"></i>`;
            nextBtn.onclick = nextSimQuestion;
        }
    }

    if (window.lucide) lucide.createIcons();
    if (qContainer) renderLatex(qContainer);
    renderSimQuestionPalette();
}

/**
 * Registra a alternativa selecionada na questão atual
 */
function selectSimAnswer(qIdx, optIdx) {
    currentSimAnswers[qIdx] = optIdx;
    renderCurrentSimQuestion();
}

/**
 * Salta diretamente para uma questão específica da paleta
 */
function jumpToSimQuestion(idx) {
    if (idx >= 0 && idx < currentSimQuestions.length) {
        currentSimIndex = idx;
        renderCurrentSimQuestion();
    }
}

function prevSimQuestion() {
    if (currentSimIndex > 0) {
        currentSimIndex--;
        renderCurrentSimQuestion();
    }
}

function nextSimQuestion() {
    if (currentSimIndex < currentSimQuestions.length - 1) {
        currentSimIndex++;
        renderCurrentSimQuestion();
    } else {
        finishSimulado();
    }
}

/**
 * Confirma saída do simulado em andamento
 */
function confirmExitSimulado() {
    if (confirm("Deseja realmente sair deste simulado? Suas respostas não finalizadas serão perdidas.")) {
        const runningContainer = document.getElementById('simulado-running');
        const setupContainer = document.getElementById('simulado-setup');
        if (runningContainer) runningContainer.classList.add('hidden');
        if (setupContainer) setupContainer.classList.remove('hidden');
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

/**
 * Finaliza o simulado, calcula pontuação e exibe resolução passo a passo
 */
function finishSimulado() {
    const total = currentSimQuestions.length;
    const answeredCount = Object.keys(currentSimAnswers).length;

    if (answeredCount < total) {
        if (!confirm(`Você respondeu ${answeredCount} de ${total} questões. Deseja finalizar mesmo assim?`)) {
            return;
        }
    }

    let correctCount = 0;
    let blockPerformance = {}; // bId -> { title, correct, total }
    let reviewHtml = [];

    currentSimQuestions.forEach((q, idx) => {
        const userOpt = currentSimAnswers[idx];
        const hasAnswered = (userOpt !== undefined);
        const isCorrect = hasAnswered && (userOpt === q.correct);
        if (isCorrect) correctCount++;

        // Performance por bloco
        if (!blockPerformance[q.blockId]) {
            blockPerformance[q.blockId] = { title: q.blockTitle, correct: 0, total: 0 };
        }
        blockPerformance[q.blockId].total++;
        if (isCorrect) blockPerformance[q.blockId].correct++;

        let optionsReview = q.options.map((opt, optIdx) => {
            const letter = String.fromCharCode(65 + optIdx);
            let optClass = "p-3 rounded-xl border text-xs sm:text-sm flex items-center justify-between ";
            let iconHtml = `<i data-lucide="circle" class="w-4 h-4 text-gray-300"></i>`;

            if (optIdx === q.correct) {
                optClass += "bg-emerald-50 border-emerald-300 font-bold text-emerald-900";
                iconHtml = `<i data-lucide="check-circle" class="w-4 h-4 text-emerald-600"></i>`;
            } else if (optIdx === userOpt && !isCorrect) {
                optClass += "bg-red-50 border-red-300 font-medium text-red-900";
                iconHtml = `<i data-lucide="x-circle" class="w-4 h-4 text-red-600"></i>`;
            } else {
                optClass += "bg-white border-gray-200 text-gray-600 opacity-60";
            }

            return `
                <div class="${optClass}">
                    <span><strong>${letter})</strong> ${opt}</span>
                    ${iconHtml}
                </div>
            `;
        }).join('');

        reviewHtml.push(`
            <div class="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm">
                <div class="flex items-center justify-between mb-3 pb-2 border-b border-gray-100">
                    <span class="text-xs font-bold uppercase tracking-wider text-brand-700">Questão ${idx + 1} de ${total}</span>
                    <span class="text-xs font-bold px-2.5 py-0.5 rounded-full ${isCorrect ? 'bg-emerald-100 text-emerald-800' : 'bg-red-100 text-red-800'}">
                        ${isCorrect ? 'Correta' : 'Incorreta'}
                    </span>
                </div>
                <span class="text-xs text-gray-400 block mb-2">${q.blockTitle} &bull; ${q.topicTitle}</span>
                <p class="font-semibold text-gray-900 text-sm sm:text-base mb-4">${q.q}</p>
                
                <div class="space-y-2 mb-4">
                    ${optionsReview}
                </div>

                <div class="bg-gray-50 border border-gray-200 rounded-xl p-4 text-xs sm:text-sm text-gray-700 leading-relaxed">
                    <strong class="text-brand-900 block mb-1">Explicação Passo a Passo:</strong>
                    ${q.explanation}
                </div>
            </div>
        `);
    });

    const percent = Math.round((correctCount / total) * 100);

    // Cards de desempenho por bloco
    const performanceCards = Object.values(blockPerformance).map(bp => {
        const bpPercent = Math.round((bp.correct / bp.total) * 100);
        return `
            <div class="bg-white/10 rounded-xl p-3 text-left border border-white/10">
                <div class="text-[11px] text-brand-200 font-semibold truncate mb-1">${bp.title}</div>
                <div class="flex justify-between items-center">
                    <span class="text-lg font-extrabold text-white">${bpPercent}%</span>
                    <span class="text-xs text-brand-200 font-medium">${bp.correct}/${bp.total} acertos</span>
                </div>
            </div>
        `;
    }).join('');

    const resultsContainer = document.getElementById('simulado-results');
    if (resultsContainer) {
        resultsContainer.innerHTML = `
            <div class="bg-gradient-to-r from-brand-800 to-brand-950 rounded-3xl p-6 sm:p-10 text-white shadow-xl text-center">
                <span class="bg-brand-500/30 text-brand-200 border border-brand-400/30 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider mb-3 inline-block">
                    Resultado do Simulado
                </span>
                <h1 class="text-3xl sm:text-4xl font-extrabold mb-2">Seu Desempenho Geral</h1>
                
                <div class="my-6 inline-flex flex-col items-center bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20">
                    <span class="text-5xl sm:text-6xl font-black text-brand-300 mb-1">${percent}%</span>
                    <span class="text-sm text-brand-100 font-semibold">Você acertou ${correctCount} de ${total} questões</span>
                </div>

                <!-- Desempenho por Eixo Temático -->
                <div class="max-w-3xl mx-auto mb-6">
                    <h3 class="text-xs font-bold text-brand-200 uppercase tracking-wider mb-3">Desempenho por Conteúdo</h3>
                    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2.5">
                        ${performanceCards}
                    </div>
                </div>

                <div class="flex justify-center gap-3">
                    <button onclick="resetSimuladoUI()" class="bg-white hover:bg-brand-50 text-brand-900 font-bold px-6 py-3 rounded-xl text-sm transition shadow-lg flex items-center gap-2">
                        <i data-lucide="rotate-ccw" class="w-4 h-4"></i> Fazer Novo Simulado
                    </button>
                </div>
            </div>

            <div class="space-y-6">
                <h2 class="text-2xl font-bold text-gray-900 flex items-center gap-2 border-l-4 border-brand-600 pl-3">
                    Gabarito Detalhado e Resoluções
                </h2>
                ${reviewHtml.join('')}
            </div>
        `;
    }

    const runningContainer = document.getElementById('simulado-running');
    if (runningContainer) runningContainer.classList.add('hidden');
    if (resultsContainer) resultsContainer.classList.remove('hidden');

    if (window.lucide) lucide.createIcons();
    if (resultsContainer) renderLatex(resultsContainer);
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

/**
 * Reseta a visualização para a tela de configurações do simulado sem recarregar a página
 */
function resetSimuladoUI() {
    const resultsContainer = document.getElementById('simulado-results');
    const setupContainer = document.getElementById('simulado-setup');
    const runningContainer = document.getElementById('simulado-running');

    if (resultsContainer) resultsContainer.classList.add('hidden');
    if (runningContainer) runningContainer.classList.add('hidden');
    if (setupContainer) setupContainer.classList.remove('hidden');

    currentSimQuestions = [];
    currentSimAnswers = {};
    currentSimIndex = 0;

    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Pré-seleção com base em parâmetro de URL (?block=X)
document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const blockParam = urlParams.get('block');
    if (blockParam) {
        const targetRadio = document.querySelector(`input[name="sim-source"][value="${blockParam}"]`);
        if (targetRadio) targetRadio.checked = true;
    }
});
