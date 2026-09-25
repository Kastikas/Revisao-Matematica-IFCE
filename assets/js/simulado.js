/**
 * PartiuIF - Motor de Simulado Oficial de Matemática Curricular (BNCC)
 * Gerencia o ciclo completo: configuração por Unidade Temática e Instituto,
 * embaralhamento Fisher-Yates, navegação com paleta, correção automática
 * e diagnóstico pedagógico por habilidades da BNCC.
 */

var currentSimQuestions = [];
var currentSimAnswers = {}; // idx -> selectedOptionIndex
var currentSimIndex = 0;
var currentSimStudentName = '';
var currentSimSource = '';
var currentSimFinishedAt = '';

/**
 * Sanitiza texto para inserção segura no HTML
 */
function escapeHtml(str) {
    if (!str) return '';
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

/**
 * Embaralhamento uniforme de Fisher-Yates (Knuth Shuffle)
 */
function shuffleArray(array) {
    var arr = array.slice();
    for (var i = arr.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
    return arr;
}

/**
 * Retorna classe e estilização do badge por Instituto Federal
 */
function getInstBadgeClass(inst) {
    switch (inst) {
        case 'IFCE':
            return 'bg-sky-500/20 text-sky-800 border-sky-300';
        case 'IFSC':
            return 'bg-amber-500/20 text-amber-900 border-amber-300';
        case 'IFSP':
            return 'bg-red-500/20 text-red-800 border-red-300';
        case 'IFMG':
            return 'bg-emerald-500/20 text-emerald-800 border-emerald-300';
        default:
            return 'bg-purple-500/20 text-purple-800 border-purple-300';
    }
}

/**
 * Renderiza o enunciado com estruturação semântica de blocos (parágrafos, manchetes,
 * citações/textos de apoio, afirmações romanas e comando final destacado).
 */
function renderQuestionText(qText, isDark) {
    if (!qText || typeof qText !== 'string') return '';
    var rawBlocks = qText.split('\n\n').map(function(b) { return b.trim(); }).filter(Boolean);
    if (!rawBlocks.length) return '';

    if (rawBlocks.length === 1) {
        var single = rawBlocks[0];
        if (single.indexOf('\n• ') !== -1 || single.indexOf('\nI. ') !== -1 || single.indexOf('\n1) ') !== -1 || single.indexOf('\n1. ') !== -1) {
            rawBlocks = single.split(/\n(?=[•\-]|\b(?:I|II|III|IV|V|VI|VII|VIII|IX|X)\.|\b\d+[\.\)])/).map(function(p) { return p.trim(); }).filter(Boolean);
        }
    }

    if (rawBlocks.length === 1) {
        var textColor = isDark ? 'text-slate-100' : 'text-gray-900';
        return '<div class="q-text-container"><p class="q-paragraph font-medium ' + textColor + ' text-sm sm:text-base leading-relaxed">' + rawBlocks[0] + '</p></div>';
    }

    var htmlParts = [];
    var totalBlocks = rawBlocks.length;

    for (var idx = 0; idx < totalBlocks; idx++) {
        var block = rawBlocks[idx];
        var isLast = (idx === totalBlocks - 1);

        // 1. Nota pedagógica
        if (block.indexOf('*(Nota pedagógica') === 0 || block.indexOf('*Nota pedagógica') === 0) {
            htmlParts.push(
                '<div class="q-pedagogical-note">' +
                    '<div class="flex items-center gap-1.5 font-bold mb-1 text-amber-600 dark:text-amber-400"><i data-lucide="info" class="w-4 h-4"></i> Nota Pedagógica</div>' +
                    '<div>' + block + '</div>' +
                '</div>'
            );
            continue;
        }

        // 2. Manchete / Título em negrito (**Título**)
        if (/^\*\*[^*]+\*\*$/.test(block)) {
            var titleText = block.replace(/^\*\*|\*\*$/g, '');
            htmlParts.push('<h4 class="q-headline">' + titleText + '</h4>');
            continue;
        }

        // 3. Fonte / Citação em itálico curta
        if (/^\*\(.*?\)\*$/.test(block) || /^\(?(?:Fonte:|Disponível em:|Publicado em).*?\)?$/i.test(block)) {
            htmlParts.push('<p class="q-source-text">' + block + '</p>');
            continue;
        }

        // 4. Afirmação romana (I., II., III...)
        var mRoman = block.match(/^(?:([I|V|X]+)\.|\(([I|V|X]+)\))\s+([\s\S]*)$/);
        if (mRoman) {
            var numeral = mRoman[1] || mRoman[2];
            var romanContent = mRoman[3];
            htmlParts.push(
                '<div class="q-item-card">' +
                    '<span class="q-item-badge">' + numeral + '</span>' +
                    '<span class="flex-1 min-w-0">' + romanContent + '</span>' +
                '</div>'
            );
            continue;
        }

        // 5. Passo numerado (1), 2) ou 1., 2.)
        var mNum = block.match(/^(?:(\d+)[\)\.]|Passo\s+(\d+)[:\.]?)\s+([\s\S]*)$/);
        if (mNum) {
            var num = mNum[1] || mNum[2];
            var numContent = mNum[3];
            htmlParts.push(
                '<div class="q-item-card">' +
                    '<span class="q-item-badge">' + num + '</span>' +
                    '<span class="flex-1 min-w-0">' + numContent + '</span>' +
                '</div>'
            );
            continue;
        }

        // 6. Lista com marcador (• ou - ou »)
        var mBullet = block.match(/^[•\-»]\s+([\s\S]*)$/);
        if (mBullet) {
            var bulletContent = mBullet[1];
            var bulletColor = isDark ? 'text-sky-400' : 'text-blue-600';
            htmlParts.push(
                '<div class="q-item-card">' +
                    '<span class="' + bulletColor + ' font-bold px-1.5 flex-shrink-0">•</span>' +
                    '<span class="flex-1 min-w-0">' + bulletContent + '</span>' +
                '</div>'
            );
            continue;
        }

        // 7. Citação longa / Texto motivador
        if ((block.charAt(0) === '“' || block.charAt(0) === '"') && block.length > 80) {
            htmlParts.push(
                '<blockquote class="q-support-card">' +
                    '<p class="italic leading-relaxed">' + block + '</p>' +
                '</blockquote>'
            );
            continue;
        }

        // 8. Comando final da questão
        var isPrompt = isLast && (
            block.endsWith('?') || block.endsWith(':') ||
            /\b(assinale|qual|pode-se afirmar|sabendo disso|nessas condições|segundo|de acordo|tendo como base|determine|calcule|o valor)\b/i.test(block)
        );

        if (isPrompt) {
            var promptColor = isDark ? 'text-slate-100' : 'text-gray-900';
            htmlParts.push('<p class="q-prompt ' + promptColor + ' text-sm sm:text-base">' + block + '</p>');
        } else {
            var pColor = isDark ? 'text-slate-200' : 'text-gray-800';
            htmlParts.push('<p class="q-paragraph font-medium ' + pColor + ' text-sm sm:text-base">' + block + '</p>');
        }
    }

    return '<div class="q-text-container">' + htmlParts.join('') + '</div>';
}

/**
 * Normaliza o nome da Unidade Temática para evitar inconsistências
 */
function normalizeUnidadeTematica(ut) {
    if (!ut) return 'Outros';
    var clean = ut.trim();
    if (clean.toLowerCase() === 'grandezas e medidas') {
        return 'Grandezas e Medidas';
    }
    return clean;
}

/**
 * Identifica se a questão pertence ao escopo curricular de Geometria Plana
 * (Ângulos, Triângulos, Polígonos, Círculo/Circunferência, Teorema de Pitágoras, Áreas e Perímetros Planos)
 */
function isGeometriaPlanaQuestion(q) {
    if (!q) return false;

    // Se for questão dos blocos teóricos conceituais
    if (q.blockId === '3') {
        return q.topicId === 'b3-t1' || q.topicId === 'b3-t2' || q.topicId === 'b3-t3';
    }
    if (q.blockId === '4') {
        return q.topicId === 'b4-t1';
    }

    var ut = normalizeUnidadeTematica(q.unidadeTematica || '');
    var desc = (q.bnccDesc || '').toLowerCase();
    var bncc = (q.bncc || '').toUpperCase();

    // Exclui geometria puramente espacial (cubos, prismas, pirâmides, vistas e volumes)
    if (bncc === 'EF06MA17' || bncc === 'EF09MA17') return false;
    var spatialKeywords = ['poliedro', 'prisma', 'pirâmide', 'vistas ortogonais', 'volumes de prismas', 'cilindro'];
    var hasSpatial = spatialKeywords.some(function(k) { return desc.indexOf(k) !== -1; });
    if (hasSpatial && desc.indexOf('área') === -1) {
        return false;
    }

    // Unidade Temática Geometria Oficial
    if (ut === 'Geometria') {
        return true;
    }

    // Grandezas e Medidas: áreas e perímetros de figuras planas
    if (ut === 'Grandezas e Medidas') {
        var mentionsPlana = (desc.indexOf('área') !== -1 || desc.indexOf('perímetro') !== -1 || desc.indexOf('figuras planas') !== -1);
        var mentionsVolume = (desc.indexOf('volume') !== -1 || desc.indexOf('capacidade') !== -1);
        if (mentionsPlana && !mentionsVolume) {
            return true;
        }
    }

    return false;
}

/**
 * Coleta todo o acervo de questões categorizadas do mathData
 */
function getAllQuestionsPool() {
    if (typeof mathData === 'undefined') {
        console.error('mathData não carregado.');
        return [];
    }

    var pool = [];
    var examBlocks = ['5', '6', '7', '8'];

    for (var bId in mathData) {
        if (!Object.prototype.hasOwnProperty.call(mathData, bId)) continue;
        var block = mathData[bId];
        if (!block || !block.topics) continue;

        var isExam = examBlocks.indexOf(String(bId)) !== -1;
        var inst = 'Teoria';

        if (isExam) {
            var bTitle = (block.title || '').toLowerCase();
            if (bTitle.indexOf('ifsc') !== -1) inst = 'IFSC';
            else if (bTitle.indexOf('ifsp') !== -1) inst = 'IFSP';
            else if (bTitle.indexOf('ifmg') !== -1) inst = 'IFMG';
            else inst = 'IFCE';
        }

        var defaultUt = 'Outros';
        if (bId === '1') defaultUt = 'Números';
        else if (bId === '2') defaultUt = 'Álgebra';
        else if (bId === '3') defaultUt = 'Geometria';
        else if (bId === '4') defaultUt = 'Grandezas e Medidas';

        block.topics.forEach(function(t) {
            var folder = t.folder || block.folder || ('bloco-' + bId);
            var filename = t.filename || '';
            var examUrl = './' + folder + '/' + filename;

            (t.questions || []).forEach(function(q, qIdx) {
                var ut = q.unidadeTematica ? normalizeUnidadeTematica(q.unidadeTematica) : defaultUt;
                pool.push({
                    q: q.q,
                    options: q.options || [],
                    correct: q.correct,
                    explanation: q.explanation || '',
                    image: q.image || q.imagem || null,
                    bncc: q.bncc || '',
                    bnccDesc: q.bnccDesc || '',
                    unidadeTematica: ut,
                    anoEscolar: q.anoEscolar || '',
                    inst: inst,
                    isOfficialExam: isExam,
                    blockId: bId,
                    blockTitle: block.title || '',
                    topicId: t.id || '',
                    topicTitle: t.title || '',
                    examUrl: examUrl,
                    qNumber: qIdx + 1,
                    originalQIdx: qIdx
                });
            });
        });
    }

    return pool;
}

/**
 * Filtra as questões com base no modo selecionado e na instituição
 */
function filterQuestions(pool, source, inst) {
    return pool.filter(function(q) {
        // Modo Teoria
        if (source === 'teoria_all') {
            return !q.isOfficialExam;
        }

        // Atividade Especial: Geometria Plana
        if (source === 'geometria_plana') {
            if (!isGeometriaPlanaQuestion(q)) return false;
            if (inst && inst !== 'all') {
                return q.inst === inst;
            }
            return true;
        }

        // Modos Oficiais BNCC
        if (!q.isOfficialExam) return false;

        // Filtro por Instituto (se selecionado diferente de 'all')
        if (inst && inst !== 'all' && q.inst !== inst) {
            return false;
        }

        // Filtro por Modo Curricular
        if (source === 'bncc_all') {
            return true;
        } else if (source === 'ut_algebra') {
            return q.unidadeTematica === 'Álgebra';
        } else if (source === 'ut_numeros') {
            return q.unidadeTematica === 'Números';
        } else if (source === 'ut_geometria') {
            return q.unidadeTematica === 'Geometria';
        } else if (source === 'ut_medidas') {
            return q.unidadeTematica === 'Grandezas e Medidas';
        } else if (source === 'ut_estatistica') {
            return q.unidadeTematica === 'Probabilidade e Estatística';
        }

        // Compatibilidade retroativa para blocos específicos (?block=X)
        if (source === q.blockId) {
            return true;
        }

        return true;
    });
}

/**
 * Atualiza a estimativa de questões disponíveis conforme os filtros selecionados
 */
function updatePoolEstimate() {
    var sourceRadio = document.querySelector('input[name="sim-source"]:checked');
    var instRadio = document.querySelector('input[name="sim-inst"]:checked');
    var estimateSpan = document.getElementById('sim-pool-estimate');
    var instContainer = document.getElementById('sim-inst-container');
    var studentContainer = document.getElementById('sim-student-container');
    var studentError = document.getElementById('sim-student-error');

    if (!sourceRadio || !estimateSpan) return;

    var source = sourceRadio.value;
    var inst = instRadio ? instRadio.value : 'all';

    // O campo de identificação do aluno aparece SOMENTE no simulado de Geometria Plana
    if (studentContainer) {
        if (source === 'geometria_plana') {
            studentContainer.classList.remove('hidden');
        } else {
            studentContainer.classList.add('hidden');
            if (studentError) studentError.classList.add('hidden');
        }
    }

    if (source === 'teoria_all') {
        if (instContainer) {
            instContainer.classList.add('opacity-40', 'pointer-events-none');
        }
    } else {
        if (instContainer) {
            instContainer.classList.remove('opacity-40', 'pointer-events-none');
        }
    }

    var allPool = getAllQuestionsPool();
    var filtered = filterQuestions(allPool, source, inst);

    var labelPrefix = (source === 'geometria_plana') ? 'Banco de Geometria Plana: ' : 'Banco disponível: ';
    estimateSpan.innerHTML = '<i data-lucide="database" class="w-3.5 h-3.5 inline text-brand-600 mr-1"></i> ' + labelPrefix + '<strong class="text-gray-900">' + filtered.length + ' questões</strong>';
    if (window.lucide) lucide.createIcons();
}

/**
 * Inicia o simulado com base nas opções selecionadas pelo usuário
 */
function startSimulado() {
    var sourceRadio = document.querySelector('input[name="sim-source"]:checked');
    var instRadio = document.querySelector('input[name="sim-inst"]:checked');
    var countRadio = document.querySelector('input[name="sim-count"]:checked');

    if (!sourceRadio || !countRadio) return;

    var source = sourceRadio.value;
    var inst = instRadio ? instRadio.value : 'all';
    var count = parseInt(countRadio.value, 10) || 10;

    // Se for o simulado específico de Geometria Plana, exige o nome do estudante
    if (source === 'geometria_plana') {
        var studentInput = document.getElementById('sim-student-name');
        var studentError = document.getElementById('sim-student-error');
        var nameVal = studentInput ? studentInput.value.trim() : '';

        if (!nameVal) {
            if (studentError) studentError.classList.remove('hidden');
            if (studentInput) {
                studentInput.focus();
                studentInput.classList.add('ring-2', 'ring-red-500', 'border-red-500');
            }
            return;
        }

        if (studentError) studentError.classList.add('hidden');
        if (studentInput) studentInput.classList.remove('ring-2', 'ring-red-500', 'border-red-500');
        currentSimStudentName = nameVal;
    } else {
        currentSimStudentName = '';
    }
    currentSimSource = source;

    var allPool = getAllQuestionsPool();
    var questionPool = filterQuestions(allPool, source, inst);

    if (questionPool.length === 0) {
        alert("Nenhuma questão encontrada para a combinação de filtros selecionada. Tente ajustar o Instituto ou o Eixo Temático.");
        return;
    }

    // Embaralhamento uniforme de Fisher-Yates
    questionPool = shuffleArray(questionPool);
    currentSimQuestions = questionPool.slice(0, Math.min(count, questionPool.length));
    currentSimAnswers = {};
    currentSimIndex = 0;

    var setupContainer = document.getElementById('simulado-setup');
    var resultsContainer = document.getElementById('simulado-results');
    var runningContainer = document.getElementById('simulado-running');
    var studentBadge = document.getElementById('sim-student-badge');
    var studentBadgeName = document.getElementById('sim-student-badge-name');

    if (setupContainer) setupContainer.classList.add('hidden');
    if (resultsContainer) resultsContainer.classList.add('hidden');
    if (runningContainer) runningContainer.classList.remove('hidden');

    if (currentSimStudentName && studentBadge && studentBadgeName) {
        studentBadgeName.textContent = currentSimStudentName;
        studentBadge.classList.remove('hidden');
    } else if (studentBadge) {
        studentBadge.classList.add('hidden');
    }

    renderSimQuestionPalette();
    renderCurrentSimQuestion();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

/**
 * Renderiza a paleta de navegação numerada das questões do simulado
 */
function renderSimQuestionPalette() {
    var palette = document.getElementById('sim-palette');
    if (!palette) return;

    palette.innerHTML = currentSimQuestions.map(function(_, idx) {
        var isAnswered = Object.prototype.hasOwnProperty.call(currentSimAnswers, idx);
        var isCurrent = (idx === currentSimIndex);
        var btnClasses = "w-8 h-8 rounded-lg text-xs font-bold transition flex items-center justify-center cursor-pointer ";

        if (isCurrent) {
            btnClasses += "ring-2 ring-brand-600 bg-brand-600 text-white shadow-md ";
        } else if (isAnswered) {
            btnClasses += "bg-brand-100 text-brand-900 border border-brand-300 ";
        } else {
            btnClasses += "bg-gray-100 text-gray-700 hover:bg-gray-200 ";
        }

        return '<button type="button" onclick="jumpToSimQuestion(' + idx + ')" class="' + btnClasses + '" aria-label="Ir para a questão ' + (idx + 1) + '">' + (idx + 1) + '</button>';
    }).join('');
}

function normalizeDriveImageUrl(url) {
    if (!url) return '';
    var match = url.match(/(?:drive\.google\.com\/(?:file\/d\/|open\?id=|uc\?export=view&id=)|lh3\.googleusercontent\.com\/d\/)([a-zA-Z0-9_-]+)/);
    if (match) {
        return 'https://lh3.googleusercontent.com/d/' + match[1];
    }
    return url;
}

function renderQuestionImageHtml(q) {
    var imgData = q.image || q.imagem;
    if (!imgData) return '';
    
    var rawSrc = typeof imgData === 'string' ? imgData.trim() : (imgData.src || '').trim();
    if (!rawSrc) return '';
    
    var alt = (typeof imgData === 'object' && imgData.alt) ? imgData.alt.trim() : 'Figura da questão';
    var caption = (typeof imgData === 'object' && imgData.caption) ? imgData.caption.trim() : '';
    
    var src = rawSrc;
    if (rawSrc.indexOf('drive.google.com') !== -1 || rawSrc.indexOf('lh3.googleusercontent.com') !== -1) {
        src = normalizeDriveImageUrl(rawSrc);
    } else if (rawSrc.indexOf('http://') !== 0 && rawSrc.indexOf('https://') !== 0 && rawSrc.indexOf('data:') !== 0) {
        src = './' + rawSrc.replace(/^(\.\/|\/)/, '');
    }
    
    var escapedAlt = alt.replace(/'/g, "\\'");
    return (
        '<div class="my-4 p-2 sm:p-3 rounded-2xl border border-gray-200 bg-white shadow-sm max-w-xl mx-auto flex flex-col items-center">' +
            '<img src="' + src + '" alt="' + alt + '" class="max-h-72 sm:max-h-96 w-auto max-w-full rounded-xl object-contain cursor-zoom-in hover:opacity-95 hover:scale-[1.01] transition duration-200" onclick="openImageModal(\'' + src + '\', \'' + escapedAlt + '\')" title="Clique para ampliar a imagem" loading="lazy">' +
            (caption ? '<p class="text-xs text-gray-500 mt-2 text-center italic">' + caption + '</p>' : '') +
        '</div>'
    );
}

/**
 * Renderiza o card da questão atual do simulado
 */
function renderCurrentSimQuestion() {
    var q = currentSimQuestions[currentSimIndex];
    if (!q) return;

    var qContainer = document.getElementById('sim-question-card');
    var indicator = document.getElementById('sim-progress-indicator');
    var topicTitle = document.getElementById('sim-topic-title');

    if (indicator) {
        indicator.innerText = 'Questão ' + (currentSimIndex + 1) + ' de ' + currentSimQuestions.length;
    }
    if (topicTitle) {
        if (q.isOfficialExam) {
            topicTitle.innerHTML = '<span class="font-bold text-gray-800">' + q.topicTitle + '</span> &bull; Questão ' + q.qNumber;
        } else {
            topicTitle.innerHTML = q.blockTitle + ' &bull; ' + q.topicTitle;
        }
    }

    var selectedOpt = currentSimAnswers[currentSimIndex];

    var optionsHtml = q.options.map(function(opt, optIdx) {
        var letter = String.fromCharCode(65 + optIdx);
        var isSelected = (selectedOpt === optIdx);
        var activeClass = isSelected ? "border-brand-600 bg-brand-50/70 shadow-sm" : "border-gray-200 hover:border-brand-300 hover:bg-brand-50/20";
        var iconName = isSelected ? "check-circle" : "circle";
        var iconClass = isSelected ? "w-5 h-5 text-brand-600 flex-shrink-0" : "w-5 h-5 text-gray-300 flex-shrink-0";

        return (
            '<button type="button" onclick="selectSimAnswer(' + currentSimIndex + ', ' + optIdx + ')" class="w-full text-left p-4 rounded-2xl border-2 ' + activeClass + ' transition text-sm text-gray-800 flex items-start justify-between gap-3 group cursor-pointer">' +
                '<span class="flex items-start gap-2.5 flex-1 min-w-0">' +
                    '<strong class="text-brand-700 font-extrabold text-sm flex-shrink-0 mt-0.5">' + letter + ')</strong> ' +
                    '<span class="flex-1 min-w-0 break-words leading-relaxed">' + opt + '</span>' +
                '</span>' +
                '<i data-lucide="' + iconName + '" class="' + iconClass + ' mt-0.5"></i>' +
            '</button>'
        );
    }).join('');

    var imgHtml = renderQuestionImageHtml(q);

    // Badges BNCC e Instituto
    var badgesHtml = '';
    var bnccDescHtml = '';

    if (q.isOfficialExam) {
        var instBadge = getInstBadgeClass(q.inst);
        badgesHtml = (
            '<div class="flex flex-wrap items-center gap-2 mb-3 pb-3 border-b border-gray-100">' +
                '<span class="text-xs font-extrabold px-2.5 py-0.5 rounded-lg border ' + instBadge + '">' +
                    q.inst +
                '</span>' +
                (q.bncc ? 
                    '<span class="text-xs font-mono font-bold px-2.5 py-0.5 rounded-lg bg-emerald-50 text-emerald-800 border border-emerald-300 inline-flex items-center gap-1">' +
                        '<i data-lucide="bookmark" class="w-3 h-3 text-emerald-600"></i> BNCC: ' + q.bncc +
                    '</span>' : '') +
                '<span class="text-xs font-semibold px-2 py-0.5 rounded-lg bg-gray-100 text-gray-700">' +
                    q.unidadeTematica +
                '</span>' +
            '</div>'
        );

        if (q.bncc && q.bnccDesc) {
            bnccDescHtml = (
                '<div class="bg-emerald-50/60 border border-emerald-200/80 rounded-xl p-3 text-xs text-emerald-950 flex items-start gap-2 mb-4 leading-relaxed">' +
                    '<i data-lucide="info" class="w-4 h-4 text-emerald-600 flex-shrink-0 mt-0.5"></i>' +
                    '<div><strong class="text-emerald-800">[' + q.unidadeTematica + (q.anoEscolar ? ' • ' + q.anoEscolar : '') + ']</strong> ' + q.bnccDesc + '</div>' +
                '</div>'
            );
        }
    } else {
        badgesHtml = (
            '<div class="flex flex-wrap items-center gap-2 mb-3 pb-3 border-b border-gray-100">' +
                '<span class="text-xs font-extrabold px-2.5 py-0.5 rounded-lg border ' + getInstBadgeClass('Teoria') + '">Fixação Teórica</span>' +
                '<span class="text-xs font-semibold px-2 py-0.5 rounded-lg bg-gray-100 text-gray-700">' + q.unidadeTematica + '</span>' +
            '</div>'
        );
    }

    if (qContainer) {
        qContainer.innerHTML = (
            '<div>' +
                badgesHtml +
                bnccDescHtml +
                renderQuestionText(q.q, false) +
                imgHtml +
            '</div>' +
            '<div class="space-y-2.5 my-4">' +
                optionsHtml +
            '</div>'
        );
    }

    // Controle dos botões anterior/próximo
    var prevBtn = document.getElementById('sim-prev-btn');
    var nextBtn = document.getElementById('sim-next-btn');

    if (prevBtn) {
        if (currentSimIndex === 0) {
            prevBtn.classList.add('opacity-40', 'pointer-events-none');
        } else {
            prevBtn.classList.remove('opacity-40', 'pointer-events-none');
        }
    }

    if (nextBtn) {
        if (currentSimIndex === currentSimQuestions.length - 1) {
            nextBtn.innerHTML = 'Finalizar Simulado <i data-lucide="check" class="w-4 h-4"></i>';
            nextBtn.onclick = finishSimulado;
        } else {
            nextBtn.innerHTML = 'Próxima Questão <i data-lucide="arrow-right" class="w-4 h-4"></i>';
            nextBtn.onclick = nextSimQuestion;
        }
    }

    if (window.lucide) lucide.createIcons();
    if (qContainer && window.renderLatex) renderLatex(qContainer);
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
        var runningContainer = document.getElementById('simulado-running');
        var setupContainer = document.getElementById('simulado-setup');
        if (runningContainer) runningContainer.classList.add('hidden');
        if (setupContainer) setupContainer.classList.remove('hidden');
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

/**
 * Finaliza o simulado, calcula pontuação e exibe resolução passo a passo com diagnóstico BNCC
 */
function finishSimulado() {
    var total = currentSimQuestions.length;
    var answeredCount = Object.keys(currentSimAnswers).length;

    if (answeredCount < total) {
        if (!confirm('Você respondeu ' + answeredCount + ' de ' + total + ' questões. Deseja finalizar mesmo assim?')) {
            return;
        }
    }

    var correctCount = 0;
    var utPerformance = {}; // ut -> { correct, total }
    var weakSkills = {};    // bncc -> { code, desc, ut, wrongCount }
    var reviewHtml = [];

    currentSimQuestions.forEach(function(q, idx) {
        var userOpt = currentSimAnswers[idx];
        var hasAnswered = (userOpt !== undefined);
        var isCorrect = hasAnswered && (userOpt === q.correct);
        if (isCorrect) correctCount++;

        // Performance por Unidade Temática
        var ut = q.unidadeTematica || 'Outros';
        if (!utPerformance[ut]) {
            utPerformance[ut] = { correct: 0, total: 0 };
        }
        utPerformance[ut].total++;
        if (isCorrect) {
            utPerformance[ut].correct++;
        } else if (q.bncc) {
            // Mapeia habilidade fraca para recomendação
            if (!weakSkills[q.bncc]) {
                weakSkills[q.bncc] = {
                    code: q.bncc,
                    desc: q.bnccDesc || '',
                    ut: ut,
                    wrongCount: 0
                };
            }
            weakSkills[q.bncc].wrongCount++;
        }

        var optionsReview = q.options.map(function(opt, optIdx) {
            var letter = String.fromCharCode(65 + optIdx);
            var optClass = "p-3.5 rounded-xl border text-xs sm:text-sm flex items-center justify-between ";
            var iconHtml = '<i data-lucide="circle" class="w-4 h-4 text-gray-300"></i>';

            if (optIdx === q.correct) {
                optClass += "bg-emerald-50 border-emerald-400 font-bold text-emerald-950";
                iconHtml = '<i data-lucide="check-circle" class="w-4 h-4 text-emerald-600"></i>';
            } else if (optIdx === userOpt && !isCorrect) {
                optClass += "bg-red-50 border-red-300 font-medium text-red-950";
                iconHtml = '<i data-lucide="x-circle" class="w-4 h-4 text-red-600"></i>';
            } else {
                optClass += "bg-white border-gray-200 text-gray-600 opacity-60";
            }

            return (
                '<div class="' + optClass + '">' +
                    '<span><strong>' + letter + ')</strong> ' + opt + '</span>' +
                    iconHtml +
                '</div>'
            );
        }).join('');

        var imgHtml = renderQuestionImageHtml(q);
        var originTitle = q.isOfficialExam ? (q.topicTitle + ' — Questão ' + q.qNumber) : (q.blockTitle + ' • ' + q.topicTitle);

        reviewHtml.push(
            '<div class="bg-white border border-gray-200 rounded-3xl p-4 sm:p-7 shadow-sm space-y-4">' +
                '<div class="flex flex-wrap items-center justify-between gap-2 pb-3 border-b border-gray-100">' +
                    '<div class="flex flex-wrap items-center gap-2">' +
                        '<span class="text-xs font-bold uppercase tracking-wider text-brand-700">Questão ' + (idx + 1) + ' de ' + total + '</span>' +
                        '<span class="text-xs font-bold px-2.5 py-0.5 rounded-lg border ' + getInstBadgeClass(q.inst) + '">' + q.inst + '</span>' +
                        (q.bncc ? '<span class="text-xs font-mono font-bold px-2 py-0.5 rounded-lg bg-emerald-50 text-emerald-800 border border-emerald-300">BNCC: ' + q.bncc + '</span>' : '') +
                    '</div>' +
                    '<span class="text-xs font-bold px-3 py-1 rounded-full ' + (isCorrect ? 'bg-emerald-100 text-emerald-800 border border-emerald-200' : 'bg-red-100 text-red-800 border border-red-200') + '">' +
                        (isCorrect ? 'Acertou' : 'Errou') +
                    '</span>' +
                '</div>' +

                '<div class="text-xs text-gray-500 font-medium flex items-center gap-1.5 min-w-0">' +
                    '<i data-lucide="archive" class="w-3.5 h-3.5 text-brand-600 flex-shrink-0"></i> <span class="truncate">' + originTitle + '</span>' +
                '</div>' +

                renderQuestionText(q.q, false) +
                imgHtml +

                '<div class="space-y-2">' +
                    optionsReview +
                '</div>' +

                '<div class="bg-slate-50 border border-slate-200 rounded-2xl p-4 text-xs sm:text-sm text-slate-700 leading-relaxed space-y-1">' +
                    '<strong class="text-slate-900 block font-bold flex items-center gap-1.5"><i data-lucide="lightbulb" class="w-4 h-4 text-amber-500"></i> Resolução Comentada:</strong>' +
                    '<div>' + q.explanation + '</div>' +
                '</div>' +
            '</div>'
        );
    });

    var percent = Math.round((correctCount / total) * 100);

    // Mensagem motivacional
    var performanceLevel = 'Excelente Domínio!';
    var performanceMsg = 'Parabéns! Seu desempenho demonstra sólida preparação para os processos seletivos dos Institutos Federais.';
    if (percent < 50) {
        performanceLevel = 'Atenção aos Pontos Fracos';
        performanceMsg = 'Revise os conteúdos em que você teve maior dificuldade utilizando as recomendações da BNCC abaixo.';
    } else if (percent < 75) {
        performanceLevel = 'Bom Desempenho!';
        performanceMsg = 'Você está no caminho certo! Com um reforço nas habilidades apontadas, sua nota subirá ainda mais.';
    }

    // Cards de Desempenho por Unidade Temática
    var utCards = Object.keys(utPerformance).map(function(ut) {
        var perf = utPerformance[ut];
        var utPercent = Math.round((perf.correct / perf.total) * 100);
        var barColor = utPercent >= 70 ? 'bg-emerald-500' : (utPercent >= 50 ? 'bg-amber-400' : 'bg-red-400');

        return (
            '<div class="bg-white/10 rounded-2xl p-4 text-left border border-white/15">' +
                '<div class="flex justify-between items-center mb-1.5">' +
                    '<span class="text-xs text-brand-100 font-bold truncate">' + ut + '</span>' +
                    '<span class="text-sm font-black text-white">' + utPercent + '%</span>' +
                '</div>' +
                '<div class="w-full bg-black/20 rounded-full h-2 mb-2 overflow-hidden">' +
                    '<div class="' + barColor + ' h-2 rounded-full transition-all duration-500" style="width: ' + utPercent + '%"></div>' +
                '</div>' +
                '<div class="text-[11px] text-brand-200">' + perf.correct + ' de ' + perf.total + ' acertos</div>' +
            '</div>'
        );
    }).join('');

    // Painel de Habilidades a Reforçar
    var weakSkillsList = Object.values(weakSkills);
    var weakSkillsHtml = '';

    if (weakSkillsList.length > 0) {
        var skillItems = weakSkillsList.map(function(sk) {
            return (
                '<div class="p-4 rounded-2xl bg-white border border-gray-200 shadow-sm flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">' +
                    '<div class="space-y-1">' +
                        '<div class="flex items-center gap-2">' +
                            '<span class="text-xs font-mono font-bold px-2 py-0.5 rounded bg-emerald-100 text-emerald-900 border border-emerald-300">BNCC: ' + sk.code + '</span>' +
                            '<span class="text-xs font-bold text-gray-600">[' + sk.ut + ']</span>' +
                        '</div>' +
                        '<p class="text-xs sm:text-sm text-gray-700 leading-snug">' + sk.desc + '</p>' +
                    '</div>' +
                    '<a href="./pesquisa.html?search=' + encodeURIComponent(sk.code) + '" target="_blank" class="flex-shrink-0 inline-flex items-center gap-1.5 px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-xs font-bold transition shadow-sm group cursor-pointer" title="Pesquisar mais questões desta habilidade">' +
                        '<i data-lucide="search" class="w-3.5 h-3.5"></i>' +
                        '<span>Praticar na Pesquisa BNCC</span>' +
                        '<i data-lucide="external-link" class="w-3 h-3 opacity-70 group-hover:opacity-100"></i>' +
                    '</a>' +
                '</div>'
            );
        }).join('');

        weakSkillsHtml = (
            '<div class="space-y-3">' +
                '<div class="flex items-center gap-2">' +
                    '<i data-lucide="alert-circle" class="w-5 h-5 text-amber-500"></i>' +
                    '<h3 class="text-lg font-bold text-gray-900">Recomendações de Estudo: Habilidades a Reforçar</h3>' +
                '</div>' +
                '<p class="text-xs sm:text-sm text-gray-600">Com base nas questões que você errou, recomendamos treinar especificamente estas habilidades do catálogo curricular:</p>' +
                '<div class="space-y-2.5">' + skillItems + '</div>' +
            '</div>'
        );
    } else {
        weakSkillsHtml = (
            '<div class="p-6 rounded-2xl bg-emerald-50 border border-emerald-200 text-emerald-900 flex items-center gap-3">' +
                '<i data-lucide="award" class="w-8 h-8 text-emerald-600 flex-shrink-0"></i>' +
                '<div>' +
                    '<h4 class="font-bold text-sm sm:text-base">Domínio Completo!</h4>' +
                    '<p class="text-xs sm:text-sm text-emerald-800">Você acertou todas as questões avaliadas e demonstrou excelente compreensão de todas as habilidades BNCC testadas.</p>' +
                '</div>' +
            '</div>'
        );
    }

    var resultsContainer = document.getElementById('simulado-results');
    if (resultsContainer) {
        var studentCertificateHtml = '';
        var actionButtonsHtml = '';
        var pageTitle = 'Seu Desempenho no Simulado';

        if (currentSimStudentName) {
            var now = new Date();
            var dateStr = now.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric' });
            var timeStr = now.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
            currentSimFinishedAt = dateStr + ' às ' + timeStr;
            pageTitle = 'Relatório de Desempenho da Atividade';

            studentCertificateHtml = (
                '<div class="bg-white/15 backdrop-blur-md rounded-2xl p-5 border border-white/20 text-left max-w-xl mx-auto shadow-inner">' +
                    '<div class="flex items-center gap-3.5">' +
                        '<div class="w-12 h-12 rounded-xl bg-white text-indigo-900 flex items-center justify-center font-black text-xl shadow flex-shrink-0">' +
                            '<i data-lucide="award" class="w-6 h-6 text-indigo-600"></i>' +
                        '</div>' +
                        '<div class="min-w-0 flex-grow">' +
                            '<span class="text-[11px] font-extrabold uppercase tracking-wider text-brand-200 block">Comprovante de Atividade Avaliativa</span>' +
                            '<h2 class="text-xl font-black text-white truncate">' + escapeHtml(currentSimStudentName) + '</h2>' +
                            '<p class="text-xs text-brand-100 flex flex-wrap items-center gap-x-2 gap-y-0.5 mt-0.5">' +
                                '<span>Atividade: <strong>Geometria Plana</strong></span>' +
                                '<span>&bull;</span>' +
                                '<span>Concluído em: <strong>' + currentSimFinishedAt + '</strong></span>' +
                            '</p>' +
                        '</div>' +
                    '</div>' +
                '</div>'
            );

            actionButtonsHtml = (
                '<button onclick="window.print()" class="bg-indigo-600 hover:bg-indigo-500 text-white font-bold px-6 py-3 rounded-xl text-sm transition shadow-lg flex items-center gap-2 cursor-pointer no-print">' +
                    '<i data-lucide="printer" class="w-4 h-4"></i> Imprimir / Salvar PDF' +
                '</button>' +
                '<button onclick="resetSimuladoUI()" class="bg-white hover:bg-brand-50 text-brand-900 font-bold px-6 py-3 rounded-xl text-sm transition shadow-lg flex items-center gap-2 cursor-pointer no-print">' +
                    '<i data-lucide="rotate-ccw" class="w-4 h-4"></i> Fazer Nova Atividade' +
                '</button>'
            );
        } else {
            actionButtonsHtml = (
                '<button onclick="resetSimuladoUI()" class="bg-white hover:bg-brand-50 text-brand-900 font-bold px-6 py-3 rounded-xl text-sm transition shadow-lg flex items-center gap-2 cursor-pointer">' +
                    '<i data-lucide="rotate-ccw" class="w-4 h-4"></i> Fazer Novo Simulado' +
                '</button>'
            );
        }

        resultsContainer.innerHTML = (
            '<div class="bg-gradient-to-r from-brand-800 to-brand-950 rounded-3xl p-6 sm:p-10 text-white shadow-xl text-center space-y-6">' +
                '<div>' +
                    '<span class="bg-brand-500/30 text-brand-200 border border-brand-400/30 text-xs font-bold px-3.5 py-1 rounded-full uppercase tracking-wider mb-3 inline-block">' +
                        performanceLevel +
                    '</span>' +
                    '<h1 class="text-3xl sm:text-4xl font-extrabold mb-1">' + pageTitle + '</h1>' +
                    '<p class="text-xs sm:text-sm text-brand-100 max-w-xl mx-auto">' + performanceMsg + '</p>' +
                '</div>' +

                studentCertificateHtml +

                '<div class="inline-flex flex-col items-center bg-white/10 backdrop-blur-md rounded-2xl px-8 py-5 border border-white/20 shadow-inner">' +
                    '<span class="text-5xl sm:text-6xl font-black text-brand-300 mb-1">' + percent + '%</span>' +
                    '<span class="text-sm text-brand-100 font-semibold">Você acertou ' + correctCount + ' de ' + total + ' questões</span>' +
                '</div>' +

                '<div>' +
                    '<h3 class="text-xs font-bold text-brand-200 uppercase tracking-wider mb-3">Aproveitamento por Unidade Temática BNCC</h3>' +
                    '<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 max-w-3xl mx-auto">' +
                        utCards +
                    '</div>' +
                '</div>' +

                '<div class="pt-2 flex justify-center gap-3">' +
                    actionButtonsHtml +
                '</div>' +
            '</div>' +

            weakSkillsHtml +

            '<div class="space-y-6 pt-4">' +
                '<h2 class="text-2xl font-bold text-gray-900 flex items-center gap-2 border-l-4 border-brand-600 pl-3">' +
                    'Gabarito Detalhado e Resoluções Passo a Passo' +
                '</h2>' +
                reviewHtml.join('') +
            '</div>'
        );
    }

    var runningContainer = document.getElementById('simulado-running');
    if (runningContainer) runningContainer.classList.add('hidden');
    if (resultsContainer) resultsContainer.classList.remove('hidden');

    if (window.lucide) lucide.createIcons();
    if (resultsContainer && window.renderLatex) renderLatex(resultsContainer);
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

/**
 * Reseta a visualização para a tela de configurações do simulado sem recarregar a página
 */
function resetSimuladoUI() {
    var resultsContainer = document.getElementById('simulado-results');
    var setupContainer = document.getElementById('simulado-setup');
    var runningContainer = document.getElementById('simulado-running');

    if (resultsContainer) resultsContainer.classList.add('hidden');
    if (runningContainer) runningContainer.classList.add('hidden');
    if (setupContainer) setupContainer.classList.remove('hidden');

    currentSimQuestions = [];
    currentSimAnswers = {};
    currentSimIndex = 0;

    updatePoolEstimate();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Inicialização e escuta de eventos
document.addEventListener('DOMContentLoaded', function() {
    // Escuta mudanças de fonte e de instituto
    var sourceRadios = document.querySelectorAll('input[name="sim-source"]');
    for (var i = 0; i < sourceRadios.length; i++) {
        sourceRadios[i].addEventListener('change', updatePoolEstimate);
    }

    var instRadios = document.querySelectorAll('input[name="sim-inst"]');
    for (var j = 0; j < instRadios.length; j++) {
        instRadios[j].addEventListener('change', updatePoolEstimate);
    }

    // Escuta digitação no campo de identificação do aluno
    var studentInput = document.getElementById('sim-student-name');
    if (studentInput) {
        studentInput.addEventListener('input', function() {
            var errorEl = document.getElementById('sim-student-error');
            if (studentInput.value.trim().length > 0) {
                if (errorEl) errorEl.classList.add('hidden');
                studentInput.classList.remove('ring-2', 'ring-red-500', 'border-red-500');
            }
        });
        studentInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                startSimulado();
            }
        });
    }

    // Parâmetro de URL (?source=X ou ?mode=X ou ?block=X ou ?inst=X)
    var urlParams = new URLSearchParams(window.location.search);
    var sourceParam = urlParams.get('source') || urlParams.get('mode') || urlParams.get('block');
    var instParam = urlParams.get('inst');

    if (sourceParam) {
        var targetRadio = document.querySelector('input[name="sim-source"][value="' + sourceParam + '"]');
        if (targetRadio) {
            targetRadio.checked = true;
        }
    }
    if (instParam) {
        var targetInst = document.querySelector('input[name="sim-inst"][value="' + instParam + '"]');
        if (targetInst) {
            targetInst.checked = true;
        }
    }

    updatePoolEstimate();
});
