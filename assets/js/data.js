/**
 * PartiuIF - Banco de Dados de Matemática Oficial
 * Contém os 5 blocos, 36 subtópicos e 243 exercícios com resoluções KaTeX.
 */
const mathData = {
  "1": {
    "title": "Bloco 1: Números e Operações",
    "description": "Domínio numérico, frações, porcentagem, proporção e notação.",
    "icon": "binary",
    "topics": [
      {
        "id": "b1-t1",
        "title": "Sistema de Numeração e Comparação",
        "bncc": "EF06MA01, EF06MA02, EF07MA07",
        "summary": "Compreensão do Sistema de Numeração Decimal, valor posicional e comparação de números.",
        "detailedTheory": "O Sistema de Numeração Decimal (SND) é posicional e possui base $10$. O valor de um algarismo depende inteiramente da posição que ele ocupa (unidade, dezena, centena, etc.). Na representação de decimais na reta numérica, quanto mais à direita, maior é o valor. Para comparar decimais, igualamos o número de casas após a vírgula adicionando zeros à direita.",
        "keyPoints": [
          "Na reta numérica, o número mais à direita é sempre maior.",
          "Atenção ao valor posicional dos zeros intercalados e finais nas casas decimais."
        ],
        "formula": "123{}45 = (1 \\times 10^2) + (2 \\times 10^1) + (3 \\times 10^0) + (4 \\times 10^{-1}) + (5 \\times 10^{-2})",
        "solvedExample": {
          "problem": "Ordene os decimais em ordem crescente: $0{}509$, $0{}51$, $0{}059$ e $0{}499$.",
          "solution": "Igualamos as casas decimais com zeros: $0{}509$, $0{}510$, $0{}059$ e $0{}499$. Comparando a parte decimal: $059 < 499 < 509 < 510$. Ordem correta: $0{}059 < 0{}499 < 0{}509 < 0{}51$."
        },
        "questions": [
          {
            "q": "Qual número representa 'quatrocentos e dois mil e quarenta'?",
            "options": [
              "$420.040$",
              "$402.040$",
              "$402.400$",
              "$400.240$"
            ],
            "correct": 1,
            "explanation": "402 milhares ($402.000$) e 40 unidades ($40$) = $402.040$."
          },
          {
            "q": "Na reta numérica, que número está exatamentente no meio de $-2$ e $4$?",
            "options": [
              "$0$",
              "$1$",
              "$2$",
              "$-1$"
            ],
            "correct": 1,
            "explanation": "O ponto médio é a média aritmética: $\\frac{-2 + 4}{2} = \\frac{2}{2} = 1$."
          },
          {
            "q": "Dentre os decimais a seguir, qual é o maior número?",
            "options": [
              "$0{}509$",
              "$0{}51$",
              "$0{}059$",
              "$0{}499$"
            ],
            "correct": 1,
            "explanation": "Igualando as casas ($0{}510$, $0{}509$, $0{}499$, $0{}059$), vemos que $0{}510$ é o maior."
          },
          {
            "q": "O valor posicional do algarismo $7$ no número $3.478.000$ é:",
            "options": [
              "$7$ milhares",
              "$7$ dezenas de milhar",
              "$7$ centenas de milhar",
              "$7$ milhões"
            ],
            "correct": 1,
            "explanation": "O algarismo $7$ ocupa a casa das dezenas de milhar, equivalendo a $70.000$."
          },
          {
            "q": "Uma pontuação formada por $5$ centenas, $3$ dezenas e $8$ milésimos corresponde a:",
            "options": [
              "$530{}008$",
              "$503{}08$",
              "$53{}008$",
              "$530{}08$"
            ],
            "correct": 0,
            "explanation": "$500 + 30 + 0{}008 = 530{}008$."
          }
        ],
        "slug": "sistema-de-numeracao-e-comparacao",
        "filename": "sistema-de-numeracao-e-comparacao.html",
        "folder": "bloco-1-numeros",
        "blockId": "1",
        "pdf": null
      },
      {
        "id": "b1-t2",
        "title": "Operações com Naturais e Estimativas",
        "bncc": "EF06MA03",
        "summary": "As quatro operações fundamentais, cálculo mental e prioridades matemáticas.",
        "detailedTheory": "A resolução de expressões numéricas exige o cumprimento estrito da ordem de precedência das operações. Primeiro, resolvem-se as potenciações/radiciações. Em seguida, multiplicações/divisões (da esquerda para a direita). Por fim, adições/subtrações. Arredondamentos são usados para avaliar a coerência dos resultados rapidamente.",
        "keyPoints": [
          "Ordem: Parênteses/Expoentes $\\rightarrow$ Multiplicação/Divisão $\\rightarrow$ Adição/Subtração.",
          "Arredondamento: se o algarismo seguinte for $\\ge 5$, arredonda-se para cima."
        ],
        "formula": "a^n = a \\times a \\times \\dots \\times a \\quad (n \\text{ fatores})",
        "solvedExample": {
          "problem": "Calcule: $18 + 2 \\times (3^2 - 4) \\div 2$.",
          "solution": "1º Potência: $3^2 = 9$. Ficamos com $18 + 2 \\times (9 - 4) \\div 2$.\n2º Parênteses: $9 - 4 = 5$. Temos $18 + 2 \\times 5 \\div 2$.\n3º Multiplicação/Divisão (esquerda p/ direita): $2 \\times 5 = 10$, e $10 \\div 2 = 5$.\n4º Soma: $18 + 5 = 23$."
        },
        "questions": [
          {
            "q": "Qual o resultado final da expressão $15 + 5 \\times 2$?",
            "options": [
              "$40$",
              "$25$",
              "$30$",
              "$100$"
            ],
            "correct": 1,
            "explanation": "Multiplicação primeiro: $5 \\times 2 = 10$. Depois soma: $15 + 10 = 25$."
          },
          {
            "q": "Um auditório do IF tem $25$ fileiras com $18$ poltronas em cada. O total de poltronas é:",
            "options": [
              "$400$",
              "$420$",
              "$450$",
              "$480$"
            ],
            "correct": 2,
            "explanation": "$25 \\times 18 = 450$ poltronas."
          },
          {
            "q": "Arredondando $4.567$ para a centena mais próxima, obtemos:",
            "options": [
              "$4.500$",
              "$4.600$",
              "$4.570$",
              "$5.000$"
            ],
            "correct": 1,
            "explanation": "A dezena é $6$ ($6 \\ge 5$), então arredondamos a centena para cima, resultando em $4.600$."
          },
          {
            "q": "O valor numérico do cálculo $2^3 + 3^2$ é igual a:",
            "options": [
              "$12$",
              "$17$",
              "$25$",
              "$13$"
            ],
            "correct": 1,
            "explanation": "$2^3 = 8$ e $3^2 = 9$. Soma: $8 + 9 = 17$."
          },
          {
            "q": "O resto da divisão inteira do número $145$ por $7$ é:",
            "options": [
              "$5$",
              "$3$",
              "$2$",
              "$1$"
            ],
            "correct": 0,
            "explanation": "$145 \\div 7 = $ quociente $20$ e resto $5$ ($20 \\times 7 = 140$, mais $5$)."
          }
        ],
        "slug": "operacoes-com-naturais-e-estimativas",
        "filename": "operacoes-com-naturais-e-estimativas.html",
        "folder": "bloco-1-numeros",
        "blockId": "1",
        "pdf": null
      },
      {
        "id": "b1-t3",
        "title": "Múltiplos, Divisores e Critérios",
        "bncc": "EF06MA04, EF06MA05",
        "summary": "Números primos, MMC, MDC e regras de divisibilidade.",
        "detailedTheory": "Múltiplos resultam da multiplicação por inteiros. Divisores dividem sem deixar resto. Números primos possuem exatamente dois divisores distintos (o $1$ e ele mesmo). O Mínimo Múltiplo Comum ($MMC$) resolve problemas de encontros periódicos, e o Máximo Divisor Comum ($MDC$) aplica-se à divisão em partes iguais e de maior tamanho possível.",
        "keyPoints": [
          "Divisibilidade por 3: a soma de seus algarismos deve ser divisível por 3.",
          "O MMC é usado para calcular intervalos temporais coincidentes."
        ],
        "formula": "\\text{MDC}(a,b) \\times \\text{MMC}(a,b) = a \\times b",
        "solvedExample": {
          "problem": "Duas lâmpadas piscam: uma a cada 12 segundos e outra a cada 18 segundos. Se piscaram juntas agora, em quantos segundos piscarão juntas novamente?",
          "solution": "Para coincidências, usamos o $MMC(12, 18)$. Fatorando ambos:\n12, 18 | 2\n 6,  9 | 2\n 3,  9 | 3\n 1,  3 | 3\n 1,  1\n$MMC = 2 \\cdot 2 \\cdot 3 \\cdot 3 = 36$ segundos."
        },
        "questions": [
          {
            "q": "O número $34.5X2$ será divisível por 3 se o valor de $X$ for:",
            "options": [
              "$1$",
              "$0$",
              "$3$",
              "$2$"
            ],
            "correct": 0,
            "explanation": "Soma: $3+4+5+X+2 = 14+X$. Se $X=1$, a soma é $15$ (divisível por 3)."
          },
          {
            "q": "Qual é o valor do MMC entre $12$ e $18$?",
            "options": [
              "$24$",
              "$36$",
              "$72$",
              "$6$"
            ],
            "correct": 1,
            "explanation": "Os múltiplos comuns são $36, 72, 108\\dots$ O menor é $36$."
          },
          {
            "q": "O Máximo Divisor Comum (MDC) entre os números $20$ e $30$ é:",
            "options": [
              "$10$",
              "$5$",
              "$60$",
              "$2$"
            ],
            "correct": 0,
            "explanation": "Divisores de 20: $\\{1,2,4,5,10,20\\}$. Divisores de 30: $\\{1,2,3,5,6,10,15,30\\}$. O maior comum é $10$."
          },
          {
            "q": "Quantos números primos existem no intervalo de $1$ a $10$?",
            "options": [
              "$3$",
              "$4$",
              "$5$",
              "$2$"
            ],
            "correct": 1,
            "explanation": "Primos de 1 a 10: $2, 3, 5$ e $7$. São $4$ no total."
          },
          {
            "q": "Três ônibus partem a cada $10$, $15$ e $20$ minutos. Eles partirão juntos novamente em:",
            "options": [
              "$30$ min",
              "$45$ min",
              "$60$ min",
              "$120$ min"
            ],
            "correct": 2,
            "explanation": "$MMC(10, 15, 20) = 60$ minutos (1 hora)."
          }
        ],
        "slug": "multiplos-divisores-e-criterios",
        "filename": "multiplos-divisores-e-criterios.html",
        "folder": "bloco-1-numeros",
        "blockId": "1",
        "pdf": null
      },
      {
        "id": "b1-t4",
        "title": "Frações I: Significados e Equivalência",
        "bncc": "EF06MA06, EF06MA07",
        "summary": "Parte-todo, frações equivalentes e conversão para decimal.",
        "detailedTheory": "Frações representam partes de um inteiro. Frações equivalentes são aquelas que representam a mesma quantidade (encontradas multiplicando ou dividindo o numerador e denominador pelo mesmo valor). Para comparar frações com denominadores distintos, igualamos os denominadores pelo MMC ou transformamos a fração em número decimal.",
        "keyPoints": [
          "Frações equivalentes mantêm a mesma proporção.",
          "Para comparar, você pode converter tudo para números decimais (dividindo)."
        ],
        "formula": "\\frac{a}{b} = \\frac{a \\cdot k}{b \\cdot k} \\quad (k \\neq 0)",
        "solvedExample": {
          "problem": "Compare $\\frac{3}{4}$ e $\\frac{4}{5}$ para determinar a maior.",
          "solution": "Via MMC (20):\n$\\frac{3}{4} = \\frac{15}{20}$ e $\\frac{4}{5} = \\frac{16}{20}$. Como $16 > 15$, logo $\\frac{4}{5} > \\frac{3}{4}$.\nVia decimais:\n$\\frac{3}{4} = 0{}75$ e $\\frac{4}{5} = 0{}80$. Como $0{}80 > 0{}75$, $\\frac{4}{5}$ é maior."
        },
        "questions": [
          {
            "q": "A fração equivalente a $\\frac{15}{25}$, após simplificação completa, é:",
            "options": [
              "$\\frac{3}{5}$",
              "$\\frac{1}{2}$",
              "$\\frac{5}{3}$",
              "$\\frac{4}{5}$"
            ],
            "correct": 0,
            "explanation": "Dividindo o numerador e o denominador por $5$, chegamos a $\\frac{3}{5}$."
          },
          {
            "q": "Qual opção traz uma fração estritamente maior do que $\\frac{1}{2}$?",
            "options": [
              "$\\frac{2}{5}$",
              "$\\frac{3}{8}$",
              "$\\frac{4}{9}$",
              "$\\frac{5}{8}$"
            ],
            "correct": 3,
            "explanation": "Convertendo em decimal: $\\frac{1}{2} = 0{}5$. A fração $\\frac{5}{8} = 0{}625$ (maior que $0{}5$)."
          },
          {
            "q": "O decimal $0{}75$ é exatamente equivalente a qual fração?",
            "options": [
              "$\\frac{1}{4}$",
              "$\\frac{3}{4}$",
              "$\\frac{4}{5}$",
              "$\\frac{7}{10}$"
            ],
            "correct": 1,
            "explanation": "$0{}75 = \\frac{75}{100}$. Simplificando por $25$: $\\frac{3}{4}$."
          },
          {
            "q": "Ao repartir $3$ pizzas de forma igual entre $4$ pessoas, cada uma receberá:",
            "options": [
              "$\\frac{4}{3}$ de pizza",
              "$\\frac{3}{4}$ de pizza",
              "$\\frac{1}{2}$ de pizza",
              "$\\frac{3}{8}$ de pizza"
            ],
            "correct": 1,
            "explanation": "Divisão direta: $3$ pizzas / $4$ pessoas = $\\frac{3}{4}$ por pessoa."
          },
          {
            "q": "Em uma turma com $40$ alunos, $\\frac{1}{4}$ são meninos. Quantas são as meninas?",
            "options": [
              "$10$",
              "$25$",
              "$30$",
              "$20$"
            ],
            "correct": 2,
            "explanation": "Meninos = $40 \\div 4 = 10$. Meninas = $40 - 10 = 30$."
          }
        ],
        "slug": "fracoes-i-significados-e-equivalencia",
        "filename": "fracoes-i-significados-e-equivalencia.html",
        "folder": "bloco-1-numeros",
        "blockId": "1",
        "pdf": null
      },
      {
        "id": "b1-t5",
        "title": "Frações II: Operações Básicas",
        "bncc": "EF06MA08, EF06MA09",
        "summary": "Adição, subtração, multiplicação e divisão de frações.",
        "detailedTheory": "Para adição ou subtração, os denominadores devem ser iguais (usa-se o $MMC$ caso não sejam). Na multiplicação, multiplica-se 'o de cima pelo de cima' (numeradores) e 'o de baixo pelo de baixo' (denominadores). Para a divisão, a regra prática é: mantenha a primeira fração e multiplique pelo inverso da segunda fração.",
        "keyPoints": [
          "Divisão de frações: mantém a primeira e multiplica pelo inverso da segunda.",
          "Soma e subtração exigem denominadores iguais."
        ],
        "formula": "\\frac{a}{b} \\div \\frac{c}{d} = \\frac{a}{b} \\cdot \\frac{d}{c}",
        "solvedExample": {
          "problem": "Efetue: $\\left(\\frac{2}{3} + \\frac{1}{4}\\right) \\div \\frac{11}{6}$.",
          "solution": "1º Soma: $MMC(3,4)=12$. $\\frac{8}{12} + \\frac{3}{12} = \\frac{11}{12}$.\n2º Divisão: $\\frac{11}{12} \\div \\frac{11}{6} = \\frac{11}{12} \\times \\frac{6}{11}$.\nCortamos o $11$ e fica $\\frac{6}{12} = \\frac{1}{2}$."
        },
        "questions": [
          {
            "q": "A soma das frações $\\frac{1}{2}$ e $\\frac{1}{3}$ é:",
            "options": [
              "$\\frac{2}{5}$",
              "$\\frac{1}{6}$",
              "$\\frac{5}{6}$",
              "$\\frac{1}{5}$"
            ],
            "correct": 2,
            "explanation": "$MMC(2,3) = 6$. Logo: $\\frac{3}{6} + \\frac{2}{6} = \\frac{5}{6}$."
          },
          {
            "q": "A multiplicação de $\\frac{2}{5}$ por $\\frac{3}{4}$ resulta em:",
            "options": [
              "$\\frac{5}{9}$",
              "$\\frac{6}{20}$",
              "$\\frac{8}{15}$",
              "$\\frac{1}{2}$"
            ],
            "correct": 1,
            "explanation": "$(2 \\times 3) / (5 \\times 4) = \\frac{6}{20}$ (que simplificado é $\\frac{3}{10}$)."
          },
          {
            "q": "O triplo da fração $\\frac{1}{6}$ corresponde a:",
            "options": [
              "$\\frac{3}{6}$",
              "$\\frac{1}{18}$",
              "$\\frac{1}{2}$",
              "Ambas A e C"
            ],
            "correct": 3,
            "explanation": "$3 \\times (1/6) = \\frac{3}{6}$. E simplificando $\\frac{3}{6}$ por $3$, temos $\\frac{1}{2}$. Logo A e C estão certas."
          },
          {
            "q": "A diferença calculada em $\\frac{3}{4} - \\frac{1}{2}$ é igual a:",
            "options": [
              "$\\frac{2}{2}$",
              "$\\frac{1}{4}$",
              "$\\frac{1}{2}$",
              "$\\frac{3}{2}$"
            ],
            "correct": 1,
            "explanation": "Transformando $\\frac{1}{2}$ em $\\frac{2}{4}$. Calculando $\\frac{3}{4} - \\frac{2}{4} = \\frac{1}{4}$."
          },
          {
            "q": "Ao dividir a fração $\\frac{1}{2}$ pela fração $\\frac{1}{4}$, obtemos:",
            "options": [
              "$\\frac{1}{8}$",
              "$2$",
              "$4$",
              "$\\frac{1}{2}$"
            ],
            "correct": 1,
            "explanation": "$(\\frac{1}{2}) \\times (\\frac{4}{1}) = \\frac{4}{2} = 2$."
          }
        ],
        "slug": "fracoes-ii-operacoes-basicas",
        "filename": "fracoes-ii-operacoes-basicas.html",
        "folder": "bloco-1-numeros",
        "blockId": "1",
        "pdf": null
      },
      {
        "id": "b1-t6",
        "title": "Porcentagem e Finanças",
        "bncc": "EF06MA12, EF08MA04",
        "summary": "Cálculos percentuais e descontos/acréscimos simples.",
        "detailedTheory": "Um aumento de $p\\%$ corresponde a multiplicar por um fator $(1 + \\frac{p}{100})$. Um desconto corresponde a multiplicar por $(1 - \\frac{p}{100})$. Para calcular aumentos ou descontos sucessivos, multiplicam-se os fatores em sequência (NUNCA some as porcentagens diretamente).",
        "keyPoints": [
          "Aumento de $10\\%$ = multiplicar por $1{}10$.",
          "Descontos sucessivos não são somados diretamente."
        ],
        "formula": "V_f = V_i \\cdot (1 \\pm i)",
        "solvedExample": {
          "problem": "Um tênis de R$ $200$ teve aumento de $10\\%$ e depois desconto de $10\\%$. Qual o preço final?",
          "solution": "1º Aumento: $200 \\times 1{}10 = \\text{R\\$} 220,00$.\n2º Desconto: $220 \\times 0{}90 = \\text{R\\$} 198,00$.\nO preço não volta aos 200 reais!"
        },
        "questions": [
          {
            "q": "O cálculo de $20\\%$ sobre R$ $150,00$ resulta em:",
            "options": [
              "R$ $20$",
              "R$ $30$",
              "R$ $25$",
              "R$ $35$"
            ],
            "correct": 1,
            "explanation": "$0{}20 \\times 150 = \\text{R\\$} 30$."
          },
          {
            "q": "Um produto de R$ $80$ sofreu acréscimo de $15\\%$. O novo preço é:",
            "options": [
              "R$ $95$",
              "R$ $92$",
              "R$ $88$",
              "R$ $90$"
            ],
            "correct": 1,
            "explanation": "$15\\%$ de $80 = 12$. Preço: $80 + 12 = \\text{R\\$} 92$."
          },
          {
            "q": "Um desconto de $10\\%$ seguido de outro de $10\\%$ equivale a um desconto real de:",
            "options": [
              "$20\\%$",
              "$19\\%$",
              "$21\\%$",
              "$18\\%$"
            ],
            "correct": 1,
            "explanation": "Fator final: $0{}90 \\times 0{}90 = 0{}81$ (mantém $81\\%$). Desconto acumulado = $19\\%$."
          },
          {
            "q": "Se $30\\%$ da dívida corresponde a R$ $60,00$, a dívida total é:",
            "options": [
              "R$ $200$",
              "R$ $180$",
              "R$ $150$",
              "R$ $300$"
            ],
            "correct": 0,
            "explanation": "$0{}30 \\times X = 60 \\rightarrow X = 60 \\div 0{}30 = \\text{R\\$} 200$."
          },
          {
            "q": "A fração equivalente a $\\frac{3}{5}$ corresponde a:",
            "options": [
              "$30\\%$",
              "$50\\%$",
              "$60\\%$",
              "$75\\%$"
            ],
            "correct": 2,
            "explanation": "$\\frac{3}{5} = 0{}60 = 60\\%$."
          }
        ],
        "slug": "porcentagem-e-financas",
        "filename": "porcentagem-e-financas.html",
        "folder": "bloco-1-numeros",
        "blockId": "1",
        "pdf": null
      },
      {
        "id": "b1-t7",
        "title": "Notação Científica e Potências",
        "bncc": "EF08MA01, EF09MA03",
        "summary": "Escrita de grandes números e propriedades da potência.",
        "detailedTheory": "A Notação Científica ($a \\times 10^n$) simplifica números muito grandes ou pequenos. A mantissa '$a$' deve estar entre $1$ (incluso) e $10$ (excluso). Vírgula para a esquerda = expoente positivo; vírgula para a direita = expoente negativo. Na multiplicação de potências de mesma base, conserva-se a base e somam-se os expoentes.",
        "keyPoints": [
          "Na notação científica: a mantissa deve estar entre 1 e 10.",
          "Multiplicação de potências iguais: soma-se os expoentes."
        ],
        "formula": "N = a \\cdot 10^n \\quad (1 \\le a < 10, \\ n \\in \\mathbb{Z})",
        "solvedExample": {
          "problem": "Multiplique: $(4{}2 \\times 10^{-6}) \\times (2 \\times 10^8)$.",
          "solution": "Multiplica-se as mantissas: $4{}2 \\times 2 = 8{}4$.\nMultiplica-se as potências somando os expoentes: $-6 + 8 = 2$.\nResultado: $8{}4 \\times 10^2 = 840$."
        },
        "questions": [
          {
            "q": "O número $4.500.000$ em notação científica é:",
            "options": [
              "$45 \\times 10^5$",
              "$4{}5 \\times 10^6$",
              "$4{}5 \\times 10^5$",
              "$0{}45 \\times 10^7$"
            ],
            "correct": 1,
            "explanation": "Vírgula 6 posições para a esquerda: $4{}5 \\times 10^6$."
          },
          {
            "q": "$0{}00023$ em notação científica é:",
            "options": [
              "$2{}3 \\times 10^{-4}$",
              "$2{}3 \\times 10^{-3}$",
              "$23 \\times 10^{-5}$",
              "$2{}3 \\times 10^4$"
            ],
            "correct": 0,
            "explanation": "Vírgula 4 casas para a direita (negativo): $2{}3 \\times 10^{-4}$."
          },
          {
            "q": "A simplificação de $2^5 \\times 2^3$ resulta em:",
            "options": [
              "$2^8$",
              "$4^8$",
              "$2^{15}$",
              "$4^{15}$"
            ],
            "correct": 0,
            "explanation": "Conserva-se a base (2) e soma-se os expoentes ($5+3=8$): $2^8$."
          },
          {
            "q": "Todo número real não nulo elevado a zero resulta em:",
            "options": [
              "Ele mesmo",
              "Zero",
              "$1$",
              "$-1$"
            ],
            "correct": 2,
            "explanation": "Regra fundamental: $a^0 = 1$."
          },
          {
            "q": "O dobro de $2^{10}$ é igual a:",
            "options": [
              "$2^{20}$",
              "$4^{10}$",
              "$2^{11}$",
              "$4^{20}$"
            ],
            "correct": 2,
            "explanation": "O dobro é multiplicar por $2^1$. Então: $2^1 \\times 2^{10} = 2^{11}$."
          }
        ],
        "slug": "notacao-cientifica-e-potencias",
        "filename": "notacao-cientifica-e-potencias.html",
        "folder": "bloco-1-numeros",
        "blockId": "1",
        "pdf": null
      }
    ]
  },
  "2": {
    "title": "Bloco 2: Álgebra",
    "description": "Linguagem algébrica, equações, proporção e funções.",
    "icon": "variable",
    "topics": [
      {
        "id": "b2-t1",
        "title": "Linguagem Algébrica",
        "bncc": "EF07MA10",
        "summary": "Tradução verbal para matemática. Incógnitas e variáveis.",
        "detailedTheory": "A álgebra traduz situações descritas em linguagem verbal para expressões simbólicas. 'Incógnita' é um valor desconhecido, mas fixo. 'Variável' pode mudar seu valor. É vital dominar termos como dobro ($2x$), triplo ($3x$), quadrado ($x^2$), sucessor ($x+1$) e diferença ($-$).",
        "keyPoints": [
          "O antecessor de um número é $x - 1$.",
          "O valor numérico é obtido substituindo a letra pelo valor numérico dado e calculando."
        ],
        "formula": "y = ax + b",
        "solvedExample": {
          "problem": "Traduza: 'O quadrado de um número somado ao seu triplo' e ache o valor numérico para $x = 3$.",
          "solution": "1º 'Quadrado' = $x^2$; 'seu triplo' = $3x$. Expressão: $x^2 + 3x$.\n2º Para $x = 3$: $(3)^2 + 3(3) = 9 + 9 = 18$."
        },
        "questions": [
          {
            "q": "A expressão para 'o quadrado de um número somado a $5$' é:",
            "options": [
              "$2x + 5$",
              "$x^2 + 5$",
              "$(x+5)^2$",
              "$x + 5^2$"
            ],
            "correct": 1,
            "explanation": "Quadrado do número é $x^2$, adicionado de $5$ fica $x^2 + 5$."
          },
          {
            "q": "A representação de 'o triplo do antecessor de $y$' é:",
            "options": [
              "$3y - 1$",
              "$3(y + 1)$",
              "$3(y - 1)$",
              "$3y + 1$"
            ],
            "correct": 2,
            "explanation": "O antecessor de $y$ é $(y - 1)$. Seu triplo é $3(y - 1)$."
          },
          {
            "q": "O valor numérico de $3x - 2$ para $x = 4$ é:",
            "options": [
              "$10$",
              "$12$",
              "$14$",
              "$8$"
            ],
            "correct": 0,
            "explanation": "Substituindo: $3(4) - 2 = 12 - 2 = 10$."
          },
          {
            "q": "A diferença entre a metade de '$a$' e o dobro de '$b$' escreve-se:",
            "options": [
              "$\\frac{a}{2} - 2b$",
              "$2a - \\frac{b}{2}$",
              "$\\frac{a-b}{2}$",
              "$a - \\frac{2b}{2}$"
            ],
            "correct": 0,
            "explanation": "Metade de '$a$' é $\\frac{a}{2}$. Dobro de '$b$' é $2b$. Logo: $\\frac{a}{2} - 2b$."
          },
          {
            "q": "A soma $x + (x+1) + (x+2)$ representa a soma de 3 números:",
            "options": [
              "Pares",
              "Ímpares",
              "Consecutivos",
              "Primos"
            ],
            "correct": 2,
            "explanation": "Elementos que somam de $1$ em $1$ formam números inteiros consecutivos."
          }
        ],
        "slug": "linguagem-algebrica",
        "filename": "linguagem-algebrica.html",
        "folder": "bloco-2-algebra",
        "blockId": "2",
        "pdf": null
      },
      {
        "id": "b2-t2",
        "title": "Grandezas e Proporções",
        "bncc": "EF07MA13",
        "summary": "Regra de três, razão, proporção direta e inversa.",
        "detailedTheory": "Grandezas Diretamente Proporcionais: se uma aumenta, a outra aumenta na mesma razão (multiplica-se cruzado). Grandezas Inversamente Proporcionais: se uma aumenta, a outra diminui proporcionalmente (multiplica-se em linha reta). A identificação prévia do comportamento das grandezas é essencial antes de montar a conta.",
        "keyPoints": [
          "Diretas: $\\frac{a}{b} = \\frac{c}{d}$ (multiplica em cruz).",
          "Inversas: $a \\cdot b = c \\cdot d$ (multiplica em linha)."
        ],
        "formula": "\\text{Direta: } \\frac{y}{x} = k, \\quad \\text{Inversa: } y \\cdot x = k",
        "solvedExample": {
          "problem": "Se 6 operários constroem um muro em 10 dias, em quantos dias 15 operários construirão o mesmo muro?",
          "solution": "Mais operários $\\rightarrow$ MENOS dias (Inversamente proporcionais).\nMultiplica em linha: $15 \\cdot x = 6 \\cdot 10 \\rightarrow 15x = 60 \\rightarrow x = 4$ dias."
        },
        "questions": [
          {
            "q": "Uma torneira enche um tanque em $6$h. Duas torneiras idênticas encherão em:",
            "options": [
              "$12$h",
              "$8$h",
              "$3$h",
              "$4$h"
            ],
            "correct": 2,
            "explanation": "Grandezas inversas: o dobro de torneiras corta o tempo pela metade ($3$h)."
          },
          {
            "q": "Na escala $1:100$, $5\\text{ cm}$ no papel representa no real:",
            "options": [
              "$5\\text{ m}$",
              "$50\\text{ m}$",
              "$0{}5\\text{ m}$",
              "$500\\text{ m}$"
            ],
            "correct": 0,
            "explanation": "$5\\text{ cm} \\times 100 = 500\\text{ cm}$, que equivale a $5\\text{ metros}$."
          },
          {
            "q": "Se $4\\text{ kg}$ de um produto custam R$ $120$, quanto custarão $6\\text{ kg}$?",
            "options": [
              "R$ $160$",
              "R$ $180$",
              "R$ $200$",
              "R$ $150$"
            ],
            "correct": 1,
            "explanation": "$1\\text{ kg}$ custa $120/4 = 30$. Logo, $6\\text{ kg} = 6 \\times 30 = \\text{R\\$} 180$."
          },
          {
            "q": "A razão entre uma pista de $400\\text{ m}$ e uma rua de $2\\text{ km}$ é:",
            "options": [
              "$\\frac{1}{5}$",
              "$\\frac{2}{1}$",
              "$\\frac{1}{20}$",
              "$\\frac{4}{2}$"
            ],
            "correct": 0,
            "explanation": "$2\\text{ km} = 2000\\text{ m}$. A razão é $\\frac{400}{2000} = \\frac{1}{5}$."
          },
          {
            "q": "Para um bolo, usam-se $2$ ovos para $3$ xícaras de farinha. Para $9$ xícaras de farinha, serão:",
            "options": [
              "$4$ ovos",
              "$5$ ovos",
              "$6$ ovos",
              "$8$ ovos"
            ],
            "correct": 2,
            "explanation": "Farinha triplicou (3 para 9), logo os ovos também triplicam ($2 \\times 3 = 6$)."
          }
        ],
        "slug": "grandezas-e-proporcoes",
        "filename": "grandezas-e-proporcoes.html",
        "folder": "bloco-2-algebra",
        "blockId": "2",
        "pdf": null
      },
      {
        "id": "b2-t3",
        "title": "Equações e Sistemas do 1º Grau",
        "bncc": "EF07MA14, EF08MA08",
        "summary": "Resolução de equações lineares e sistemas de duas variáveis.",
        "detailedTheory": "Uma equação do 1º grau busca o valor que torna a igualdade verdadeira, operando ambos os lados igualmente. Sistemas com duas incógnitas buscam um par ordenado $(x, y)$ que satisfaça duas equações ao mesmo tempo. Os métodos de Substituição e Adição são os principais.",
        "keyPoints": [
          "O que for feito de um lado da equação deve ser feito do outro.",
          "No Método da Adição, busca-se eliminar uma variável somando as equações."
        ],
        "formula": "\\begin{cases} a_1 x + b_1 y = c_1 \\\\ a_2 x + b_2 y = c_2 \\end{cases}",
        "solvedExample": {
          "problem": "Resolva: $\\begin{cases} x + y = 12 \\\\ 2x - y = 9 \\end{cases}$",
          "solution": "Somando as equações (Adição):\n$(x + 2x) + (y - y) = 12 + 9 \\rightarrow 3x = 21 \\rightarrow x = 7$.\nSubstituindo $x=7$: $7 + y = 12 \\rightarrow y = 5$. Solução: $(7, 5)$."
        },
        "questions": [
          {
            "q": "A raiz da equação $3x - 5 = 16$ é:",
            "options": [
              "$5$",
              "$7$",
              "$6$",
              "$8$"
            ],
            "correct": 1,
            "explanation": "$3x = 16 + 5 \\rightarrow 3x = 21 \\rightarrow x = 7$."
          },
          {
            "q": "No sistema $(x + y = 10)$ e $(x - y = 4)$, o valor numérico de $x$ é:",
            "options": [
              "$6$",
              "$5$",
              "$7$",
              "$3$"
            ],
            "correct": 2,
            "explanation": "Somando as equações: $2x = 14 \\rightarrow x = 7$."
          },
          {
            "q": "O dobro de um número menos $4$ é $12$. Que número é esse?",
            "options": [
              "$10$",
              "$6$",
              "$8$",
              "$16$"
            ],
            "correct": 2,
            "explanation": "$2x - 4 = 12 \\rightarrow 2x = 16 \\rightarrow x = 8$."
          },
          {
            "q": "$2$ canetas e $1$ lápis custam R$ $7,00$. A caneta custa o triplo do lápis. O lápis custa:",
            "options": [
              "R$ $1,00$",
              "R$ $2,00$",
              "R$ $1,50$",
              "R$ $0,50$"
            ],
            "correct": 0,
            "explanation": "$C = 3L$. Então $2(3L) + L = 7 \\rightarrow 7L = 7 \\rightarrow L = 1$."
          },
          {
            "q": "A solução real da equação $2(x + 3) = 14$ é:",
            "options": [
              "$3$",
              "$4$",
              "$5$",
              "$10$"
            ],
            "correct": 1,
            "explanation": "Distributiva: $2x + 6 = 14 \\rightarrow 2x = 8 \\rightarrow x = 4$."
          }
        ],
        "slug": "equacoes-e-sistemas-do-1o-grau",
        "filename": "equacoes-e-sistemas-do-1o-grau.html",
        "folder": "bloco-2-algebra",
        "blockId": "2",
        "pdf": null
      },
      {
        "id": "b2-t4",
        "title": "Produtos Notáveis e Fatoração",
        "bncc": "EF09MA09",
        "summary": "Identidades algébricas fundamentais e fatoração.",
        "detailedTheory": "Produtos Notáveis são multiplicações algébricas com padrões fixos: Quadrado da Soma $(a+b)^2$, Quadrado da Diferença $(a-b)^2$ e o Produto da Soma pela Diferença $(a+b)(a-b)$. A fatoração transforma uma soma algébrica em um produto, sendo as principais: fator comum em evidência e diferença de dois quadrados.",
        "keyPoints": [
          "$(a+b)^2 = a^2 + 2ab + b^2$",
          "$a^2 - b^2 = (a+b)(a-b)$"
        ],
        "formula": "(a+b)(a-b) = a^2 - b^2",
        "solvedExample": {
          "problem": "Simplifique a fração algébrica $\\frac{x^2 - 9}{(x - 3)}$ para $x \\neq 3$.",
          "solution": "Fatorar o numerador (Diferença de Dois Quadrados): $x^2 - 9 = (x + 3)(x - 3)$.\nDividindo por $(x - 3)$:\n$\\frac{(x + 3)(x - 3)}{(x - 3)} = x + 3$."
        },
        "questions": [
          {
            "q": "O desenvolvimento do produto notável $(x - 3)^2$ é:",
            "options": [
              "$x^2 - 9$",
              "$x^2 - 6x + 9$",
              "$x^2 + 6x - 9$",
              "$x^2 - 3x + 9$"
            ],
            "correct": 1,
            "explanation": "Quadrado do primeiro, menos duas vezes o primeiro pelo segundo, mais o quadrado do segundo: $x^2 - 6x + 9$."
          },
          {
            "q": "Fatorando $x^2 - 25$, obtemos:",
            "options": [
              "$(x-5)(x-5)$",
              "$(x-25)(x+1)$",
              "$(x+5)(x-5)$",
              "$(x+25)^2$"
            ],
            "correct": 2,
            "explanation": "Diferença de quadrados $a^2 - b^2 = (a+b)(a-b)$, com $a=x$ e $b=5$."
          },
          {
            "q": "O fator comum em evidência para $4x^3 + 6x^2$ é:",
            "options": [
              "$2x$",
              "$4x^2$",
              "$2x^2$",
              "$x^2$"
            ],
            "correct": 2,
            "explanation": "O MDC numérico é $2$ e a menor potência literal é $x^2$. Fator: $2x^2$."
          },
          {
            "q": "A expressão correspondente a $(a + b)(a - b)$ é:",
            "options": [
              "$a^2 + b^2$",
              "$a^2 - b^2$",
              "$a^2 - 2ab + b^2$",
              "$2a - 2b$"
            ],
            "correct": 1,
            "explanation": "Produto da soma pela diferença é a diferença dos quadrados ($a^2 - b^2$)."
          },
          {
            "q": "Colocando o fator em evidência em $3x + 3y$, temos:",
            "options": [
              "$3xy$",
              "$3(x+y)$",
              "$6(xy)$",
              "$(3+x)y$"
            ],
            "correct": 1,
            "explanation": "O $3$ é comum a ambos: $3(x + y)$."
          }
        ],
        "slug": "produtos-notaveis-e-fatoracao",
        "filename": "produtos-notaveis-e-fatoracao.html",
        "folder": "bloco-2-algebra",
        "blockId": "2",
        "pdf": null
      },
      {
        "id": "b2-t5",
        "title": "Equações do 2º Grau e Funções",
        "bncc": "EF09MA06",
        "summary": "Fórmula resolutiva (Bhaskara) e noções de função.",
        "detailedTheory": "Uma equação de 2º grau ($ax^2+bx+c=0$) é resolvida pela fórmula de Bhaskara. O discriminante ($\\Delta = b^2 - 4ac$) determina as raízes: $\\Delta > 0$ (2 reais diferentes), $\\Delta = 0$ (2 reais iguais), $\\Delta < 0$ (nenhuma raiz real). Na função afim ($y = ax + b$), o coeficiente angular '$a$' determina se a reta sobe ou desce.",
        "keyPoints": [
          "Bhaskara: $x = \\frac{-b \\pm \\sqrt{\\Delta}}{2a}$.",
          "Na função $f(x) = ax + b$, $a > 0$ é reta crescente, $a < 0$ decrescente."
        ],
        "formula": "\\Delta = b^2 - 4ac, \\quad x = \\frac{-b \\pm \\sqrt{\\Delta}}{2a}",
        "solvedExample": {
          "problem": "Encontre as raízes reais da equação $x^2 - 7x + 10 = 0$.",
          "solution": "$\\Delta = (-7)^2 - 4(1)(10) = 49 - 40 = 9$.\n$x = \\frac{7 \\pm \\sqrt{9}}{2} = \\frac{7 \\pm 3}{2}$.\n$x_1 = 10 / 2 = 5$ e $x_2 = 4 / 2 = 2$."
        },
        "questions": [
          {
            "q": "As raízes da equação $x^2 - 5x + 6 = 0$ são:",
            "options": [
              "$2$ e $3$",
              "$-2$ e $-3$",
              "$1$ e $6$",
              "$0$ e $6$"
            ],
            "correct": 0,
            "explanation": "Soma=$5$ e Produto=$6$, as raízes são $2$ e $3$."
          },
          {
            "q": "Qual o valor do discriminante Delta ($\\Delta$) em $x^2 - 4x + 4 = 0$?",
            "options": [
              "$4$",
              "$-4$",
              "$16$",
              "$0$"
            ],
            "correct": 3,
            "explanation": "$\\Delta = (-4)^2 - 4(1)(4) = 16 - 16 = 0$."
          },
          {
            "q": "Dada a função $f(x) = 2x - 3$, o valor de $f(5)$ é:",
            "options": [
              "$10$",
              "$7$",
              "$13$",
              "$2$"
            ],
            "correct": 1,
            "explanation": "$f(5) = 2(5) - 3 = 10 - 3 = 7$."
          },
          {
            "q": "Na equação $x^2 - 9 = 0$, as raízes são:",
            "options": [
              "$3$",
              "$-3$",
              "$3$ e $-3$",
              "$9$"
            ],
            "correct": 2,
            "explanation": "$x^2 = 9 \\rightarrow x = \\pm\\sqrt{9} \\rightarrow x = 3$ e $-3$."
          },
          {
            "q": "O gráfico da função afim $y = -3x + 1$ é uma reta:",
            "options": [
              "Crescente",
              "Decrescente",
              "Horizontal",
              "Vertical"
            ],
            "correct": 1,
            "explanation": "Como $a = -3$ (negativo), a função é decrescente."
          }
        ],
        "slug": "equacoes-do-2o-grau-e-funcoes",
        "filename": "equacoes-do-2o-grau-e-funcoes.html",
        "folder": "bloco-2-algebra",
        "blockId": "2",
        "pdf": null
      }
    ]
  },
  "3": {
    "title": "Bloco 3: Geometria",
    "description": "Estudo de ângulos, figuras planas, Pitágoras e sólidos.",
    "icon": "shapes",
    "topics": [
      {
        "id": "b3-t1",
        "title": "Ângulos, Triângulos e Polígonos",
        "bncc": "EF07MA22",
        "summary": "Soma de ângulos internos, classificação geométrica.",
        "detailedTheory": "Em qualquer triângulo, a soma dos ângulos internos é $180^\\circ$. Para um polígono de $n$ lados, a soma interna é $S_i = (n - 2) \\times 180^\\circ$. Triângulos classificam-se pelos lados (Equilátero = 3 iguais, Isósceles = 2 iguais, Escaleno = 0 iguais) e pelos ângulos (Acutângulo = agudos, Retângulo = $90^\\circ$, Obtusângulo > $90^\\circ$).",
        "keyPoints": [
          "Triângulo sempre soma $180^\\circ$ internamente.",
          "Complementares somam $90^\\circ$; Suplementares somam $180^\\circ$."
        ],
        "formula": "S_i = (n - 2) \\cdot 180^\\circ",
        "solvedExample": {
          "problem": "Calcule a medida de cada ângulo interno de um hexágono regular.",
          "solution": "$S_i = (6 - 2) \\times 180^\\circ = 4 \\times 180^\\circ = 720^\\circ$.\nDividindo pela quantidade de ângulos (6): $a_i = \\frac{720^\\circ}{6} = 120^\\circ$."
        },
        "questions": [
          {
            "q": "A soma dos ângulos internos de um quadrilátero é:",
            "options": [
              "$180^\\circ$",
              "$360^\\circ$",
              "$540^\\circ$",
              "$720^\\circ$"
            ],
            "correct": 1,
            "explanation": "$(4 - 2) \\times 180^\\circ = 360^\\circ$."
          },
          {
            "q": "Um triângulo que possui todos os três lados iguais é o:",
            "options": [
              "Isósceles",
              "Escaleno",
              "Retângulo",
              "Equilátero"
            ],
            "correct": 3,
            "explanation": "Equiláteros possuem os 3 lados e 3 ângulos congruentes ($60^\\circ$)."
          },
          {
            "q": "Se dois ângulos de um triângulo medem $40^\\circ$ e $60^\\circ$, o terceiro mede:",
            "options": [
              "$80^\\circ$",
              "$90^\\circ$",
              "$100^\\circ$",
              "$60^\\circ$"
            ],
            "correct": 0,
            "explanation": "$180^\\circ - (40^\\circ + 60^\\circ) = 180^\\circ - 100^\\circ = 80^\\circ$."
          },
          {
            "q": "Dois ângulos que somam exatamente $180^\\circ$ são:",
            "options": [
              "Complementares",
              "Suplementares",
              "Opostos",
              "Replementares"
            ],
            "correct": 1,
            "explanation": "Soma $90^\\circ$ = complementares; Soma $180^\\circ$ = suplementares."
          },
          {
            "q": "O ângulo interno de um pentágono regular mede:",
            "options": [
              "$108^\\circ$",
              "$72^\\circ$",
              "$120^\\circ$",
              "$90^\\circ$"
            ],
            "correct": 0,
            "explanation": "Soma = $3 \\times 180^\\circ = 540^\\circ$. $540^\\circ \\div 5 = 108^\\circ$."
          }
        ],
        "slug": "angulos-triangulos-e-poligonos",
        "filename": "angulos-triangulos-e-poligonos.html",
        "folder": "bloco-3-geometria",
        "blockId": "3",
        "pdf": null
      },
      {
        "id": "b3-t2",
        "title": "Teorema de Pitágoras e Semelhança",
        "bncc": "EF09MA13",
        "summary": "Triângulos retângulos e proporção geométrica.",
        "detailedTheory": "O Teorema de Pitágoras ($a^2 = b^2 + c^2$) relaciona os lados exclusivamente em triângulos retângulos, onde a hipotenusa ($a$) é o lado maior, oposto ao ângulo de $90^\\circ$. Semelhança de triângulos ocorre quando as formas são iguais, mas os tamanhos são proporcionais (ângulos congruentes, lados homólogos proporcionais).",
        "keyPoints": [
          "Aplica-se Pitágoras APENAS a triângulos retângulos.",
          "Terno pitagórico principal: $3, 4, 5$."
        ],
        "formula": "a^2 = b^2 + c^2 \\quad (a = \\text{hipotenusa})",
        "solvedExample": {
          "problem": "Uma escada de $5\\text{ m}$ está apoiada a $3\\text{ m}$ de distância do muro. Qual a altura alcançada?",
          "solution": "Hipotenusa=5, Cateto=3, Altura=h.\n$5^2 = 3^2 + h^2 \\rightarrow 25 = 9 + h^2 \\rightarrow h^2 = 16 \\rightarrow h = 4\\text{ m}$."
        },
        "questions": [
          {
            "q": "Em um triângulo retângulo de catetos $3\\text{ cm}$ e $4\\text{ cm}$, a hipotenusa é:",
            "options": [
              "$5\\text{ cm}$",
              "$6\\text{ cm}$",
              "$7\\text{ cm}$",
              "$25\\text{ cm}$"
            ],
            "correct": 0,
            "explanation": "$h^2 = 3^2 + 4^2 = 25 \\rightarrow h = 5\\text{ cm}$."
          },
          {
            "q": "Hipotenusa $10\\text{ m}$, cateto $8\\text{ m}$. O outro cateto é:",
            "options": [
              "$4\\text{ m}$",
              "$5\\text{ m}$",
              "$6\\text{ m}$",
              "$7\\text{ m}$"
            ],
            "correct": 2,
            "explanation": "$10^2 = 8^2 + c^2 \\rightarrow 100 = 64 + c^2 \\rightarrow c^2 = 36 \\rightarrow c = 6\\text{ m}$."
          },
          {
            "q": "Dois triângulos semelhantes têm razão $2$. Se a base do menor é $4\\text{ cm}$, a do maior é:",
            "options": [
              "$6\\text{ cm}$",
              "$8\\text{ cm}$",
              "$2\\text{ cm}$",
              "$16\\text{ cm}$"
            ],
            "correct": 1,
            "explanation": "Base do maior = $4\\text{ cm} \\times 2 = 8\\text{ cm}$."
          },
          {
            "q": "A diagonal de um quadrado de lado $5\\text{ cm}$ é:",
            "options": [
              "$10\\text{ cm}$",
              "$25\\text{ cm}$",
              "$5\\sqrt{2}\\text{ cm}$",
              "$5\\text{ cm}$"
            ],
            "correct": 2,
            "explanation": "Diagonal do quadrado = Lado $\\times \\sqrt{2} = 5\\sqrt{2}\\text{ cm}$."
          },
          {
            "q": "O Teorema de Pitágoras é válido para triângulos:",
            "options": [
              "Equiláteros",
              "Acutângulos",
              "Obtusângulos",
              "Retângulos"
            ],
            "correct": 3,
            "explanation": "Apenas para triângulos com um ângulo reto ($90^\\circ$)."
          }
        ],
        "slug": "teorema-de-pitagoras-e-semelhanca",
        "filename": "teorema-de-pitagoras-e-semelhanca.html",
        "folder": "bloco-3-geometria",
        "blockId": "3",
        "pdf": null
      },
      {
        "id": "b3-t3",
        "title": "Círculo e Circunferência",
        "bncc": "EF08MA16",
        "summary": "Área e perímetro (comprimento) do círculo.",
        "detailedTheory": "A circunferência é a borda (linha). O círculo é a região preenchida. Diâmetro é a corda máxima, e vale o dobro do raio ($D = 2r$). O comprimento/perímetro (contorno) calcula-se com $C = 2\\pi r$, e a área de superfície com $A = \\pi r^2$.",
        "keyPoints": [
          "O valor de $\\pi$ (pi) geralmente é aproximado para $3{}14$ nas provas.",
          "Diâmetro = $2 \\times \\text{Raio}$."
        ],
        "formula": "C = 2\\pi r, \\quad A = \\pi r^2",
        "solvedExample": {
          "problem": "Calcule a área de um círculo de raio $10\\text{ m}$ (adote $\\pi = 3{}14$).",
          "solution": "$A = \\pi \\cdot r^2 = 3{}14 \\cdot (10)^2 = 3{}14 \\cdot 100 = 314\\text{ m}^2$."
        },
        "questions": [
          {
            "q": "O comprimento de uma circunferência de raio $5\\text{ cm}$ ($\\pi = 3$) é:",
            "options": [
              "$15\\text{ cm}$",
              "$30\\text{ cm}$",
              "$75\\text{ cm}$",
              "$10\\text{ cm}$"
            ],
            "correct": 1,
            "explanation": "$C = 2 \\times 3 \\times 5 = 30\\text{ cm}$."
          },
          {
            "q": "A área de um círculo de raio $4\\text{ cm}$ ($\\pi = 3$) é:",
            "options": [
              "$24\\text{ cm}^2$",
              "$12\\text{ cm}^2$",
              "$48\\text{ cm}^2$",
              "$36\\text{ cm}^2$"
            ],
            "correct": 2,
            "explanation": "$A = 3 \\times 4^2 = 3 \\times 16 = 48\\text{ cm}^2$."
          },
          {
            "q": "Se o diâmetro é $20\\text{ cm}$, o raio mede:",
            "options": [
              "$40\\text{ cm}$",
              "$10\\text{ cm}$",
              "$5\\text{ cm}$",
              "$31{}4\\text{ cm}$"
            ],
            "correct": 1,
            "explanation": "Raio = Diâmetro / $2 = 20 / 2 = 10\\text{ cm}$."
          },
          {
            "q": "O segmento que une o centro à borda do círculo é o:",
            "options": [
              "Diâmetro",
              "Corda",
              "Raio",
              "Arco"
            ],
            "correct": 2,
            "explanation": "Por definição, essa é a medida do raio."
          },
          {
            "q": "O ângulo central correspondente a uma meia-volta é:",
            "options": [
              "$90^\\circ$",
              "$180^\\circ$",
              "$270^\\circ$",
              "$360^\\circ$"
            ],
            "correct": 1,
            "explanation": "Uma volta inteira é $360^\\circ$, logo meia-volta é $180^\\circ$."
          }
        ],
        "slug": "circulo-e-circunferencia",
        "filename": "circulo-e-circunferencia.html",
        "folder": "bloco-3-geometria",
        "blockId": "3",
        "pdf": null
      },
      {
        "id": "b3-t4",
        "title": "Sólidos e Vistas",
        "bncc": "EF06MA16",
        "summary": "Poliedros, corpos redondos e Relação de Euler.",
        "detailedTheory": "Poliedros são compostos só por superfícies planas (faces poligonais). A Relação de Euler ($V - A + F = 2$) liga Vértices, Arestas e Faces de poliedros convexos. Corpos Redondos (cilindro, cone, esfera) possuem partes arredondadas. Vistas ortogonais são as imagens planas que vemos ao olhar o sólido exatamente de frente, de cima ou do lado.",
        "keyPoints": [
          "Relação de Euler: $V + F = A + 2$.",
          "Prismas: 2 bases. Pirâmides: 1 base."
        ],
        "formula": "V - A + F = 2",
        "solvedExample": {
          "problem": "Um poliedro tem 6 faces e 8 vértices. Quantas arestas ele tem?",
          "solution": "$V - A + F = 2 \\rightarrow 8 - A + 6 = 2 \\rightarrow 14 - A = 2 \\rightarrow A = 12$ arestas."
        },
        "questions": [
          {
            "q": "Um hexaedro regular (cubo) possui quantas faces?",
            "options": [
              "$4$",
              "$6$",
              "$8$",
              "$12$"
            ],
            "correct": 1,
            "explanation": "O cubo tem 6 faces quadradas."
          },
          {
            "q": "Poliedro com 8 vértices e 6 faces tem quantas arestas?",
            "options": [
              "$12$",
              "$14$",
              "$10$",
              "$16$"
            ],
            "correct": 0,
            "explanation": "$V - A + F = 2 \\rightarrow 8 - A + 6 = 2 \\rightarrow A = 12$."
          },
          {
            "q": "O cilindro é um sólido geométrico classificado como:",
            "options": [
              "Poliedro",
              "Prisma",
              "Corpo Redondo",
              "Pirâmide"
            ],
            "correct": 2,
            "explanation": "Por ter superfície curva (que rola), é um corpo redondo."
          },
          {
            "q": "A vista ortogonal superior de um cone de base apoiada é:",
            "options": [
              "Triângulo",
              "Círculo com ponto",
              "Quadrado",
              "Ponto"
            ],
            "correct": 1,
            "explanation": "Olhando de cima, vê-se a base circular e o vértice central como um ponto."
          },
          {
            "q": "Todo prisma regular possui obrigatoriamente quantas bases paralelas?",
            "options": [
              "$1$",
              "$2$",
              "$3$",
              "Nenhuma"
            ],
            "correct": 1,
            "explanation": "Prismas caracterizam-se por duas bases idênticas e paralelas."
          }
        ],
        "slug": "solidos-e-vistas",
        "filename": "solidos-e-vistas.html",
        "folder": "bloco-3-geometria",
        "blockId": "3",
        "pdf": null
      }
    ]
  },
  "4": {
    "title": "Bloco 4: Medidas e Estatística",
    "description": "Áreas, volumes, probabilidade e análise de dados.",
    "icon": "bar-chart-3",
    "topics": [
      {
        "id": "b4-t1",
        "title": "Áreas de Figuras Planas",
        "bncc": "EF07MA25",
        "summary": "Cálculo de área (quadrado, retângulo, triângulo, trapézio).",
        "detailedTheory": "Área mede superfície bidimensional. Fórmulas comuns: Quadrado ($L^2$), Retângulo ($b \\cdot h$), Triângulo ($\\frac{b \\cdot h}{2}$), Trapézio ($\\frac{(B+b) \\cdot h}{2}$). Não confunda área com perímetro (que é a soma dos contornos lineares).",
        "keyPoints": [
          "Triângulo: Área é metade do retângulo base $\\times$ altura.",
          "Perímetro é contorno, Área é o preenchimento interno."
        ],
        "formula": "A_{\\text{Trapézio}} = \\frac{(B + b) \\cdot h}{2}",
        "solvedExample": {
          "problem": "Área de um trapézio de bases $10\\text{ cm}$, $6\\text{ cm}$ e altura $5\\text{ cm}$.",
          "solution": "$A = \\frac{(10 + 6) \\cdot 5}{2} = \\frac{16 \\cdot 5}{2} = \\frac{80}{2} = 40 \\text{ cm}^2$."
        },
        "questions": [
          {
            "q": "A área de uma sala de $8\\text{ m}$ por $5\\text{ m}$ é:",
            "options": [
              "$13\\text{ m}^2$",
              "$26\\text{ m}^2$",
              "$40\\text{ m}^2$",
              "$20\\text{ m}^2$"
            ],
            "correct": 2,
            "explanation": "Base $\\times$ Altura = $8 \\times 5 = 40\\text{ m}^2$."
          },
          {
            "q": "Triângulo de base $10\\text{ cm}$ e altura $6\\text{ cm}$ tem área:",
            "options": [
              "$60\\text{ cm}^2$",
              "$30\\text{ cm}^2$",
              "$16\\text{ cm}^2$",
              "$20\\text{ cm}^2$"
            ],
            "correct": 1,
            "explanation": "$(10 \\times 6) / 2 = 30\\text{ cm}^2$."
          },
          {
            "q": "Terreno quadrado com perímetro $20\\text{ m}$ tem área:",
            "options": [
              "$20\\text{ m}^2$",
              "$25\\text{ m}^2$",
              "$100\\text{ m}^2$",
              "$40\\text{ m}^2$"
            ],
            "correct": 1,
            "explanation": "Lado = $20/4 = 5\\text{ m}$. Área = $5^2 = 25\\text{ m}^2$."
          },
          {
            "q": "Trapézio (bases $8$ e $4$, altura $5$). A área é:",
            "options": [
              "$30\\text{ cm}^2$",
              "$60\\text{ cm}^2$",
              "$20\\text{ cm}^2$",
              "$40\\text{ cm}^2$"
            ],
            "correct": 0,
            "explanation": "$[(8 + 4) \\times 5] / 2 = (12 \\times 5) / 2 = 30\\text{ cm}^2$."
          },
          {
            "q": "A unidade metro quadrado ($\\text{m}^2$) mede:",
            "options": [
              "Volume",
              "Comprimento",
              "Capacidade",
              "Área"
            ],
            "correct": 3,
            "explanation": "Unidades ao quadrado referem-se sempre a superfícies (áreas)."
          }
        ],
        "slug": "areas-de-figuras-planas",
        "filename": "areas-de-figuras-planas.html",
        "folder": "bloco-4-medidas-e-estatistica",
        "blockId": "4",
        "pdf": null
      },
      {
        "id": "b4-t2",
        "title": "Volume e Capacidade",
        "bncc": "EF08MA17",
        "summary": "Volumes de prismas, cilindros e equivalência de litros.",
        "detailedTheory": "Volume mede espaço ocupado 3D ($V = A_{\\text{base}} \\times h$). Capacidade é o volume líquido abrigável. Relações vitais para a prova do IF: $1\\text{ m}^3 = 1000\\text{ Litros}$ e $1\\text{ dm}^3 = 1\\text{ Litro}$ ($1\\text{ L} = 1000\\text{ mL}$).",
        "keyPoints": [
          "Para calcular Litros, converta primeiro para $\\text{m}^3$ e multiplique por $1000$.",
          "Volume do bloco retangular = comprimento $\\times$ largura $\\times$ altura."
        ],
        "formula": "V = A_{\\text{base}} \\cdot h",
        "solvedExample": {
          "problem": "Caixa d'água $2\\text{ m} \\times 1{}5\\text{ m} \\times 1\\text{ m}$. Capacidade em Litros?",
          "solution": "$V = 2 \\times 1{}5 \\times 1 = 3 \\text{ m}^3$.\nComo $1 \\text{ m}^3 = 1000 \\text{ L}$, temos $3 \\times 1000 = 3000 \\text{ Litros}$."
        },
        "questions": [
          {
            "q": "O volume do bloco $2\\text{ m} \\times 3\\text{ m} \\times 4\\text{ m}$ é:",
            "options": [
              "$9\\text{ m}^3$",
              "$24\\text{ m}^3$",
              "$20\\text{ m}^3$",
              "$18\\text{ m}^3$"
            ],
            "correct": 1,
            "explanation": "$2 \\times 3 \\times 4 = 24\\text{ m}^3$."
          },
          {
            "q": "Reservatório de $2\\text{ m}^3$ comporta quantos Litros?",
            "options": [
              "$2.000\\text{ L}$",
              "$20\\text{ L}$",
              "$200\\text{ L}$",
              "$20.000\\text{ L}$"
            ],
            "correct": 0,
            "explanation": "$2\\text{ m}^3 \\times 1000 = 2.000\\text{ Litros}$."
          },
          {
            "q": "Cubo com aresta $3\\text{ cm}$ tem volume de:",
            "options": [
              "$9\\text{ cm}^3$",
              "$12\\text{ cm}^3$",
              "$27\\text{ cm}^3$",
              "$18\\text{ cm}^3$"
            ],
            "correct": 2,
            "explanation": "Aresta$^3 = 3^3 = 27\\text{ cm}^3$."
          },
          {
            "q": "Cilindro de área da base $10\\text{ cm}^2$ e altura $5\\text{ cm}$. Volume:",
            "options": [
              "$50\\text{ cm}^3$",
              "$15\\text{ cm}^3$",
              "$150\\text{ cm}^3$",
              "$25\\text{ cm}^3$"
            ],
            "correct": 0,
            "explanation": "Área da base $\\times$ Altura = $10 \\times 5 = 50\\text{ cm}^3$."
          },
          {
            "q": "$500\\text{ mL}$ de água equivale a:",
            "options": [
              "$5\\text{ Litros}$",
              "$0{}5\\text{ Litro}$",
              "$0{}05\\text{ Litro}$",
              "$50\\text{ Litros}$"
            ],
            "correct": 1,
            "explanation": "$500 / 1000 = 0{}5\\text{ Litro}$."
          }
        ],
        "slug": "volume-e-capacidade",
        "filename": "volume-e-capacidade.html",
        "folder": "bloco-4-medidas-e-estatistica",
        "blockId": "4",
        "pdf": null
      },
      {
        "id": "b4-t3",
        "title": "Probabilidade",
        "bncc": "EF07MA28",
        "summary": "Eventos possíveis x favoráveis.",
        "detailedTheory": "Probabilidade indica a chance de ocorrência de um evento. A fórmula é a razão entre o que você QUER (casos favoráveis) e TUDO O QUE PODE ACONTECER (casos possíveis ou espaço amostral). O resultado é uma fração, decimal ou porcentagem entre $0$ (impossível) e $1$ ou $100\\%$ (certo).",
        "keyPoints": [
          "Conte com precisão todos os resultados possíveis antes do cálculo.",
          "$P = \\frac{\\text{Favorável}}{\\text{Total}}$"
        ],
        "formula": "P(E) = \\frac{n(E)}{n(\\Omega)}",
        "solvedExample": {
          "problem": "Urna com 6 bolas vermelhas e 4 azuis. Chance de tirar azul?",
          "solution": "Total de bolas = 10 (Espaço amostral).\nBolas Azuis (favoráveis) = 4.\n$P = \\frac{4}{10} = 0{}4 = 40\\%$."
        },
        "questions": [
          {
            "q": "Lançando uma moeda, a probabilidade de dar 'cara' é:",
            "options": [
              "$\\frac{1}{3}$",
              "$\\frac{1}{4}$",
              "$\\frac{1}{2}$",
              "$1$"
            ],
            "correct": 2,
            "explanation": "1 evento favorável (cara) em 2 possíveis (cara ou coroa): $\\frac{1}{2}$."
          },
          {
            "q": "No dado de $6$ faces, a chance de sair número par é:",
            "options": [
              "$\\frac{1}{6}$",
              "$\\frac{2}{6}$",
              "$\\frac{1}{2}$",
              "$\\frac{4}{6}$"
            ],
            "correct": 2,
            "explanation": "Pares são $\\{2,4,6\\}$. Logo, 3 casos num total de 6: $\\frac{3}{6} = \\frac{1}{2}$."
          },
          {
            "q": "Sacola com 3 bolas vermelhas e 2 azuis. Chance da azul:",
            "options": [
              "$\\frac{2}{5}$",
              "$\\frac{3}{5}$",
              "$\\frac{1}{2}$",
              "$\\frac{2}{3}$"
            ],
            "correct": 0,
            "explanation": "2 azuis num total de 5 bolas = $\\frac{2}{5}$."
          },
          {
            "q": "Probabilidade de sortear um número de $1$ a $10$ e ele ser o $7$:",
            "options": [
              "$\\frac{7}{10}$",
              "$\\frac{1}{10}$",
              "$\\frac{1}{7}$",
              "$10\\%$"
            ],
            "correct": 1,
            "explanation": "Só existe um '7' entre dez opções possíveis: $\\frac{1}{10}$."
          },
          {
            "q": "Baralho (52 cartas), a chance de um Ás (existem 4) é:",
            "options": [
              "$\\frac{1}{13}$",
              "$\\frac{1}{52}$",
              "$\\frac{4}{13}$",
              "$\\frac{1}{4}$"
            ],
            "correct": 0,
            "explanation": "$\\frac{4}{52}$. Simplificando por 4 fica $\\frac{1}{13}$."
          }
        ],
        "slug": "probabilidade",
        "filename": "probabilidade.html",
        "folder": "bloco-4-medidas-e-estatistica",
        "blockId": "4",
        "pdf": null
      },
      {
        "id": "b4-t4",
        "title": "Estatística Básica",
        "bncc": "EF08MA22",
        "summary": "Média aritmética, moda e mediana.",
        "detailedTheory": "Estatística descritiva resume dados. A Média Aritmética soma tudo e divide pela quantidade de itens. A Moda é o valor mais frequente. A Mediana é o valor do centro (exige ROL, ou seja, ordenar os números antes de verificar). Se a quantidade de dados for par, a mediana é a média dos dois números centrais.",
        "keyPoints": [
          "Mediana DEVE ter os dados em ROL (ordenados).",
          "Moda pode não existir (amodal) ou haver mais de uma (bimodal)."
        ],
        "formula": "\\bar{x} = \\frac{\\sum x_i}{n}",
        "solvedExample": {
          "problem": "Dados: $[4, 7, 7, 8, 9]$. Ache Média, Moda e Mediana.",
          "solution": "Média: $\\frac{4+7+7+8+9}{5} = \\frac{35}{5} = 7$.\nModa: $7$ (aparece mais vezes).\nMediana: O 3º termo na lista já ordenada é $7$."
        },
        "questions": [
          {
            "q": "A média aritmética simples entre $6$, $8$ e $10$ é:",
            "options": [
              "$7$",
              "$8$",
              "$9$",
              "$24$"
            ],
            "correct": 1,
            "explanation": "$\\frac{6 + 8 + 10}{3} = \\frac{24}{3} = 8$."
          },
          {
            "q": "Nas idades ($12, 14, 14, 15, 16$), a moda é:",
            "options": [
              "$12$",
              "$15$",
              "$14$",
              "$16$"
            ],
            "correct": 2,
            "explanation": "O $14$ aparece mais vezes ($2x$)."
          },
          {
            "q": "A mediana do conjunto ordenado ($3, 5, 7, 9, 11$) é:",
            "options": [
              "$5$",
              "$7$",
              "$9$",
              "$35$"
            ],
            "correct": 1,
            "explanation": "Lista de 5 itens. O central é o 3º termo: $7$."
          },
          {
            "q": "Se a soma de 4 notas é $28$, a média é:",
            "options": [
              "$4$",
              "$7$",
              "$28$",
              "$112$"
            ],
            "correct": 1,
            "explanation": "Média = Soma / Quantidade = $28 / 4 = 7$."
          },
          {
            "q": "No conjunto par ($2, 2, 4, 8$), a mediana é:",
            "options": [
              "$2$",
              "$3$",
              "$4$",
              "$6$"
            ],
            "correct": 1,
            "explanation": "Média dos dois centrais: $\\frac{2 + 4}{2} = 3$."
          }
        ],
        "slug": "estatistica-basica",
        "filename": "estatistica-basica.html",
        "folder": "bloco-4-medidas-e-estatistica",
        "blockId": "4",
        "pdf": null
      }
    ]
  },
  "5": {
    "title": "Bloco 5: Provas Anteriores IFSC",
    "description": "Resolução e simulados completos de 16 provas oficiais do Exame de Classificação do IFSC (2017 a 2026).",
    "icon": "file-text",
    "topics": [
      {
        "id": "ifsc-2017-1-matematica",
        "title": "Prova IFSC 2017.1",
        "bncc": "Revisão Geral",
        "summary": "10 questões de Matemática aplicadas no Exame de Classificação 2017.1 do IFSC para Cursos Técnicos Integrados.",
        "detailedTheory": "O Exame 2017.1 aborda taxa percentual, resolução de equações do 2º grau, aumentos percentuais sucessivos, mínimo múltiplo comum (MMC em percursos periódicos), Teorema de Pitágoras em trajetórias retilíneas, produtos notáveis e fatoração algébrica, proporcionalidade em produção, notação científica e grandezas, perímetros de triângulos e matemática financeira (juros compostos).",
        "keyPoints": [
          "Fique atento à diferença entre pontos percentuais e taxa de variação percentual.",
          "Em problemas de encontros periódicos na pista, calcule o MMC dos tempos de volta.",
          "Juros compostos utilizam a fórmula $M = C(1+i)^t$."
        ],
        "formula": "M = C(1+i)^t, \\quad a^2 = b^2 + c^2, \\quad MMC(a, b)",
        "solvedExample": {
          "problem": "Equação do 2º grau: $3x^2 + 9x - 120 = 0$.",
          "solution": "Dividindo toda a equação por 3: $x^2 + 3x - 40 = 0$.\nPor Soma e Produto: Soma $= -3$ e Produto $= -40$.\nAs raízes que satisfazem essas condições são $x_1 = -8$ e $x_2 = 5$."
        },
        "questions": [
          {
            "q": "O Instituto Brasileiro de Geografia e Estatística (IBGE) divulgou que a taxa de desemprego cresceu para $8{}5\\%$ na média do ano passado. Sabendo-se que, em 2014, a taxa média era de $6{}8\\%$, o crescimento na taxa de desemprego de 2014 para 2015 foi de:",
            "options": [
              "$1{}3\\%$",
              "$2{}3\\%$",
              "$2{}9\\%$",
              "$2{}7\\%$",
              "$1{}7\\%$"
            ],
            "correct": 4,
            "explanation": "A diferença direta entre as taxas é $8{}5\\% - 6{}8\\% = 1{}7\\%$ (pontos percentuais de aumento)."
          },
          {
            "q": "Dada a equação quadrática $3x^2 + 9x - 120 = 0$, determine suas raízes reais:",
            "options": [
              "$-16$ e $10$",
              "$-5$ e $8$",
              "$-8$ e $5$",
              "$-10$ e $16$",
              "$-9$ e $15$"
            ],
            "correct": 2,
            "explanation": "Dividindo os coeficientes por $3$: $x^2 + 3x - 40 = 0$. Fatorando: $(x + 8)(x - 5) = 0 \\Rightarrow x = -8$ e $x = 5$."
          },
          {
            "q": "Na feira, um pé de alface que custava R$ $1{}50$ passou a custar R$ $2{}85$. Qual o percentual de aumento que esse produto sofreu?",
            "options": [
              "$185\\%$",
              "$85\\%$",
              "$35\\%$",
              "$135\\%$",
              "$90\\%$"
            ],
            "correct": 4,
            "explanation": "Aumento absoluto: $2{}85 - 1{}50 = 1{}35$. Percentual: $\\frac{1{}35}{1{}50} = 0{}90 = 90\\%$."
          },
          {
            "q": "Roberto e João pedalam numa pista circular. Roberto completa uma volta em $24\\text{ s}$ e João em $28\\text{ s}$. Se saírem juntos do mesmo ponto de largada, após quanto tempo voltarão a se encontrar no ponto de partida pela primeira vez?",
            "options": [
              "$3\\text{ min } 8\\text{ s}$",
              "$2\\text{ min } 48\\text{ s}$",
              "$1\\text{ min } 28\\text{ s}$",
              "$2\\text{ min } 28\\text{ s}$",
              "$1\\text{ min } 48\\text{ s}$"
            ],
            "correct": 1,
            "explanation": "Calcula-se o $MMC(24, 28) = 168\\text{ segundos}$. Convertendo para minutos: $168 = 2 \\times 60 + 48 = 2\\text{ min } 48\\text{ s}$."
          },
          {
            "q": "Carlos caminha até o trabalho fazendo um trajeto perpendicular de $150\\text{ m}$ ao norte e $200\\text{ m}$ a leste (total de $350\\text{ m}$). Se ele fizesse esse percurso em linha reta (hipotenusa de $250\\text{ m}$), quantos metros a menos caminharia?",
            "options": [
              "$230\\text{ m}$",
              "$100\\text{ m}$",
              "$160\\text{ m}$",
              "$250\\text{ m}$",
              "$325\\text{ m}$"
            ],
            "correct": 1,
            "explanation": "Pelo Teorema de Pitágoras: $d = \\sqrt{150^2 + 200^2} = \\sqrt{22500 + 40000} = \\sqrt{62500} = 250\\text{ m}$. Caminhando em linha reta, a economia de trajeto é $350\\text{ m} - 250\\text{ m} = 100\\text{ m}$."
          },
          {
            "q": "Analise as afirmações sobre produtos notáveis e fatoração (V ou F):\\n( ) $(3x - 2)^2 = 9x^2 - 12x + 4$\\n( ) $(x + 4)^2 = x^2 + 16$\\n( ) $64x^2 - 49 = (8x + 7)(8x - 7)$\\n( ) $4x^2 + 16x = 4x(x + 4)$\\n( ) $x^2 - 8x + 16 = (x - 4)^2$",
            "options": [
              "V, F, V, F, V",
              "V, V, F, F, F",
              "V, F, V, V, V",
              "F, F, V, V, V",
              "F, V, F, V, V"
            ],
            "correct": 2,
            "explanation": "1ª $(3x-2)^2 = 9x^2 - 12x + 4$ (V); 2ª falta o termo misto $8x$ (F); 3ª diferença de quadrados correta (V); 4ª fator comum $4x(x+4)$ correto (V); 5ª trinômio quadrado perfeito $(x-4)^2$ correto (V). Sequência: V, F, V, V, V."
          },
          {
            "q": "Uma cooperativa produz ração onde a quantidade final equivale a $20\\%$ da matéria-prima recebida. Quantos quilogramas de matéria-prima são necessários para produzir $150\\text{ toneladas}$ de ração ($1\\text{ t} = 1000\\text{ kg}$)?",
            "options": [
              "$150.000\\text{ kg}$",
              "$750\\text{ kg}$",
              "$300\\text{ kg}$",
              "$300.000\\text{ kg}$",
              "$750.000\\text{ kg}$"
            ],
            "correct": 4,
            "explanation": "$150\\text{ t} = 150.000\\text{ kg}$. Como a ração é $20\\%$ da matéria-prima ($M$): $0{}20 M = 150.000 \\Rightarrow M = \\frac{150.000}{0{}20} = 750.000\\text{ kg}$."
          },
          {
            "q": "Nas Olimpíadas 2016 foram servidas $11\\text{ milhões}$ de refeições e a arrecadação de ingressos foi de R$ $1{}2\\text{ bilhão}$ para $7{}5\\text{ milhões}$ de ingressos. Analise as afirmações:\\nI. $11\\text{ milhões} = 1{}1 \\times 10^7$ refeições.\\nII. Preço médio do ingresso $= \\frac{1{}2 \\times 10^9}{7{}5 \\times 10^6} = \\text{R\\$} 160,00$.",
            "options": [
              "Apenas II e III",
              "Apenas I e II",
              "Apenas I e IV",
              "Todas são verdadeiras",
              "Apenas II e IV"
            ],
            "correct": 2,
            "explanation": "I é verdadeira pois $11.000.000 = 1{}1 \\times 10^7$. IV é verdadeira pois $\\frac{1.200.000.000}{7.500.000} = 160$ reais por ingresso."
          },
          {
            "q": "Em um triângulo equilátero $ABC$, os lados medem $AB = 3x + y$, $AC = 2x + y + 2$ e $BC = x + 3y$. Qual é o perímetro desse triângulo equilátero?",
            "options": [
              "$12\\text{ u.c.}$",
              "$6\\text{ u.c.}$",
              "$24\\text{ u.c.}$",
              "$15\\text{ u.c.}$",
              "$18\\text{ u.c.}$"
            ],
            "correct": 2,
            "explanation": "Como todos os lados são iguais: $3x + y = 2x + y + 2 \\Rightarrow x = 2$. Igualando $AB$ e $BC$: $3(2) + y = 2 + 3y \\Rightarrow 6 + y = 2 + 3y \\Rightarrow 2y = 4 \\Rightarrow y = 2$. O lado mede $3(2) + 2 = 8\\text{ u.c.}$ O perímetro é $3 \\times 8 = 24\\text{ u.c.}$"
          },
          {
            "q": "Uma família pegou um empréstimo no valor de $30\\%$ de sua renda média (R$ $1.368,00$). Pagará juros compostos de $2\\%$ ao mês em $2$ meses. Quanto pegou emprestado e qual o montante final?",
            "options": [
              "R$ $407,40$ e R$ $423,86$",
              "R$ $410,40$ e R$ $425,94$",
              "R$ $409,40$ e R$ $424,90$",
              "R$ $409,40$ e R$ $425,94$",
              "R$ $410,40$ e R$ $426,98$"
            ],
            "correct": 4,
            "explanation": "Empréstimo: $0{}30 \\times 1368 = \\text{R\\$} 410,40$. Montante com juros compostos: $M = 410{}40 \\times (1{}02)^2 = 410{}40 \\times 1{}0404 = \\text{R\\$} 426,98$."
          }
        ],
        "slug": "prova-ifsc-20171",
        "filename": "prova-ifsc-20171.html",
        "folder": "bloco-5-provas-ifsc",
        "blockId": "5",
        "pdf": "PROVA_INTEGRADO_VersaoFinal.pdf"
      },
      {
        "id": "ifsc-2017-2-matematica",
        "title": "Prova IFSC 2017.2",
        "bncc": "Revisão Geral",
        "summary": "10 questões de Matemática aplicadas no Exame de Classificação 2017.2 do IFSC para Cursos Técnicos Integrados.",
        "detailedTheory": "O Exame 2017.2 contempla sistemas de equações lineares de duas incógnitas (cálculo de cédulas bancárias), proporcionalidade direta em tabelas nutricionais, equivalência algébrica em equações do 1º grau, operações com números mistos e frações, proporção de tempo, equações lineares de taxa constante (vazão e volume em açudes), áreas de figuras planas retangulares, juros simples comparados, volume de cilindro e descontos/acréscimos sucessivos.",
        "keyPoints": [
          "Em sistemas de cédulas, monte uma equação para o total de notas e outra para o valor em dinheiro.",
          "Para vazão constante, a variação de volume dividida pela variação de tempo determina a taxa por minuto.",
          "O volume do cilindro reto é dado por $V = \\pi r^2 h$."
        ],
        "formula": "V_{\\text{cilindro}} = \\pi r^2 h, \\quad J = C \\cdot i \\cdot t, \\quad A = b \\cdot h",
        "solvedExample": {
          "problem": "Sistema de cédulas: 47 notas totalizando R$ 580,00 com notas de R$ 5,00 e R$ 20,00.",
          "solution": "Seja $x$ as notas de R$ 5 e $y$ as notas de R$ 20:\n$\\begin{cases} x + y = 47 \\\\ 5x + 20y = 580 \\end{cases}$\nMultiplicando a 1ª por $-5$: $-5x - 5y = -235$.\nSomando: $15y = 345 \\Rightarrow y = 23$ notas de R$ 20.\n$x = 47 - 23 = 24$ notas de R$ 5."
        },
        "questions": [
          {
            "q": "Um cliente sacou R$ $580,00$ no caixa eletrônico e recebeu toda a quantia em $47$ notas de R$ $5,00$ e R$ $20,00$. Quantas notas de cada valor ele recebeu?",
            "options": [
              "$25$ notas de R$ $5,00$ e $22$ notas de R$ $20,00$",
              "$20$ notas de R$ $5,00$ e $27$ notas de R$ $20,00$",
              "$24$ notas de R$ $5,00$ e $23$ notas de R$ $20,00$",
              "$22$ notas de R$ $5,00$ e $25$ notas de R$ $20,00$",
              "$23$ notas de R$ $5,00$ e $24$ notas de R$ $20,00$"
            ],
            "correct": 2,
            "explanation": "Sistema: $x + y = 47$ e $5x + 20y = 580$. Multiplicando a 1ª por $-5$: $15y = 345 \\Rightarrow y = 23$ (notas de R$ 20) e $x = 24$ (notas de R$ 5)."
          },
          {
            "q": "Considerando a equação $-5(3x - 8) = -45$, é CORRETO afirmar que ela é equivalente a:",
            "options": [
              "$-8x - 32 = 0$",
              "$-15x + 5 = 0$",
              "$-8x - 58 = 0$",
              "$-15x + 85 = 0$",
              "$-15x - 53 = 0$"
            ],
            "correct": 3,
            "explanation": "Aplicando a distributiva: $-15x + 40 = -45 \\Rightarrow -15x + 40 + 45 = 0 \\Rightarrow -15x + 85 = 0$."
          },
          {
            "q": "Jéssica comprou $7$ pizzas de $8$ fatias cada. Foram consumidas $6$ pizzas inteiras mais $5$ fatias da sétima pizza. A quantidade total de pizza consumida na forma fracionária corresponde a:",
            "options": [
              "$\\frac{48}{8}$",
              "$\\frac{53}{8}$",
              "$\\frac{56}{8}$",
              "$\\frac{47}{8}$",
              "$\\frac{55}{8}$"
            ],
            "correct": 1,
            "explanation": "Fatias consumidas: $6 \\times 8 + 5 = 48 + 5 = 53$ fatias. Como cada pizza tem 8 fatias, a fração é $\\frac{53}{8}$."
          },
          {
            "q": "Após $30\\text{ min}$ de chuva, o volume de um açude era $160\\text{ m}^3$. Passados mais $12\\text{ min}$, o volume foi para $208\\text{ m}^3$. Se o volume cresceu a taxa constante, qual era o volume inicial do açude antes da chuva?",
            "options": [
              "$40\\text{ m}^3$",
              "$48\\text{ m}^3$",
              "$60\\text{ m}^3$",
              "$50\\text{ m}^3$",
              "$35\\text{ m}^3$"
            ],
            "correct": 0,
            "explanation": "Vazão da chuva: $\\frac{208 - 160}{12} = \\frac{48}{12} = 4\\text{ m}^3/\\text{min}$. Em 30 minutos entraram $30 \\times 4 = 120\\text{ m}^3$. O volume inicial era $160 - 120 = 40\\text{ m}^3$."
          },
          {
            "q": "Um terreno retangular tem comprimento igual ao dobro da largura mais $5\\text{ metros}$ ($C = 2L + 5$). Sabendo que seu perímetro é $70\\text{ metros}$, sua área total é:",
            "options": [
              "$250\\text{ m}^2$",
              "$300\\text{ m}^2$",
              "$200\\text{ m}^2$",
              "$150\\text{ m}^2$",
              "$350\\text{ m}^2$"
            ],
            "correct": 0,
            "explanation": "Perímetro $= 2(C + L) = 2(2L + 5 + L) = 6L + 10 = 70 \\Rightarrow 6L = 60 \\Rightarrow L = 10\\text{ m}$. Comprimento $C = 2(10) + 5 = 25\\text{ m}$. Área $= 25 \\times 10 = 250\\text{ m}^2$."
          },
          {
            "q": "Seu João emprestou R$ $1.000,00$ a juros simples e pagou montante de R$ $1.320,00$ após $4\\text{ meses}$. Dona Maria emprestou R$ $1.200,00$ e pagou R$ $1.680,00$ após $5\\text{ meses}$. As taxas mensais de juros simples de João e Maria foram respectivamente:",
            "options": [
              "$8\\%\\text{ a.m.}$ e $8\\%\\text{ a.m.}$",
              "$6\\%\\text{ a.m.}$ e $8\\%\\text{ a.m.}$",
              "$8\\%\\text{ a.m.}$ e $10\\%\\text{ a.m.}$",
              "$10\\%\\text{ a.m.}$ e $8\\%\\text{ a.m.}$",
              "$7\\%\\text{ a.m.}$ e $9\\%\\text{ a.m.}$"
            ],
            "correct": 0,
            "explanation": "João: Juros $= 320$. $320 = 1000 \\cdot i_1 \\cdot 4 \\Rightarrow i_1 = \\frac{320}{4000} = 0{}08 = 8\\%\\text{ a.m.}$ Maria: Juros $= 480$. $480 = 1200 \\cdot i_2 \\cdot 5 \\Rightarrow i_2 = \\frac{480}{6000} = 0{}08 = 8\\%\\text{ a.m.}$"
          },
          {
            "q": "Um reservatório cilíndrico tem $10\\text{ m}$ de diâmetro interno (raio $5\\text{ m}$) e $10\\text{ m}$ de altura. Considerando $\\pi = 3{}14$, qual a capacidade máxima desse reservatório em Litros ($1\\text{ m}^3 = 1000\\text{ L}$)?",
            "options": [
              "$785.000\\text{ Litros}$",
              "$314.000\\text{ Litros}$",
              "$250.000\\text{ Litros}$",
              "$1.570.000\\text{ Litros}$",
              "$78.500\\text{ Litros}$"
            ],
            "correct": 0,
            "explanation": "$V = \\pi r^2 h = 3{}14 \\times 5^2 \\times 10 = 3{}14 \\times 25 \\times 10 = 785\\text{ m}^3$. Em litros: $785 \\times 1000 = 785.000\\text{ Litros}$."
          },
          {
            "q": "Um produto eletrônico que custava R$ $800,00$ sofreu um aumento de $15\\%$ antes do Natal e, em janeiro, sofreu um desconto de $10\\%$ sobre o novo preço. O valor final pago em janeiro foi:",
            "options": [
              "R$ $828,00$",
              "R$ $840,00$",
              "R$ $800,00$",
              "R$ $832,00$",
              "R$ $850,00$"
            ],
            "correct": 0,
            "explanation": "1º Aumento: $800 \\times 1{}15 = \\text{R\\$} 920,00$. 2º Desconto: $920 \\times 0{}90 = \\text{R\\$} 828,00$."
          },
          {
            "q": "Em uma embalagem de biscoito de $200\\text{ g}$, uma porção de $30\\text{ g}$ contém $150\\text{ kcal}$. Quantas quilocalorias possui o pacote inteiro de $200\\text{ g}$?",
            "options": [
              "$800\\text{ kcal}$",
              "$900\\text{ kcal}$",
              "$1.000\\text{ kcal}$",
              "$1.200\\text{ kcal}$",
              "$1.500\\text{ kcal}$"
            ],
            "correct": 2,
            "explanation": "Regra de três: $\\frac{150}{30} = 5\\text{ kcal/g}$. Para o pacote inteiro de $200\\text{ g}$: $200 \\times 5 = 1.000\\text{ kcal}$."
          },
          {
            "q": "Uma apresentação do Coral do IFSC iniciou às $19\\text{h } 45\\text{min}$ e terminou às $21\\text{h } 20\\text{min}$. A duração total dessa apresentação foi de:",
            "options": [
              "$1\\text{h } 25\\text{min}$",
              "$1\\text{h } 35\\text{min}$",
              "$1\\text{h } 45\\text{min}$",
              "$2\\text{h } 05\\text{min}$",
              "$1\\text{h } 15\\text{min}$"
            ],
            "correct": 1,
            "explanation": "Das $19\\text{h } 45\\text{min}$ até às $20\\text{h } 00\\text{min}$ são $15\\text{ min}$. Das $20\\text{h } 00\\text{min}$ até às $21\\text{h } 20\\text{min}$ são $1\\text{h } 20\\text{min}$. Total: $15\\text{ min} + 1\\text{h } 20\\text{min} = 1\\text{h } 35\\text{min}$."
          }
        ],
        "slug": "prova-ifsc-20172",
        "filename": "prova-ifsc-20172.html",
        "folder": "bloco-5-provas-ifsc",
        "blockId": "5",
        "pdf": "EC-PROVA-2017-2.pdf"
      },
      {
        "id": "ifsc-2018-1-matematica",
        "title": "Prova IFSC 2018.1",
        "bncc": "Revisão Geral",
        "summary": "10 questões de Matemática aplicadas no Exame de Classificação 2018.1 do IFSC para Cursos Técnicos Integrados.",
        "detailedTheory": "O Exame 2018.1 foca em geometria plana (telas de proteção e perímetros), regra de três simples e proporcionalidade de custos, propriedades de potências e potenciação, Teorema de Pitágoras e cálculo de distâncias, divisão em partes inversamente e diretamente proporcionais, máximo divisor comum (MDC) em cortes de tecidos/materiais, funções do 1º grau e tarifas de táxi, estatística básica e cálculo de volumes de prismas retos.",
        "keyPoints": [
          "Tarifas com bandeirada e quilômetro rodado seguem a função afim $V(x) = ax + b$.",
          "Para cortar tecidos ou barras em pedaços iguais de tamanho máximo, calcula-se o MDC dos comprimentos.",
          "Lembre-se: o volume do prisma retangular é dado por $V = a \\cdot b \\cdot c$."
        ],
        "formula": "V(x) = ax + b, \\quad V_{\\text{bloco}} = c \\cdot l \\cdot h, \\quad a^2 = b^2 + c^2",
        "solvedExample": {
          "problem": "Função afim da corrida de táxi: bandeirada fixa de R$ 5,00 e R$ 2,50 por km rodado.",
          "solution": "Equação da corrida: $V(x) = 2{}50x + 5{}00$.\nPara uma distância de $12\\text{ km}$:\n$V(12) = 2{}50(12) + 5{}00 = 30{}00 + 5{}00 = \\text{R\\$} 35{}00$."
        },
        "questions": [
          {
            "q": "Uma tela de proteção retangular foi instalada em uma janela de $1{}20\\text{ m}$ de largura por $1{}50\\text{ m}$ de altura. A metragem linear de moldura necessária para contornar todo o perímetro da janela é:",
            "options": [
              "$2{}70\\text{ m}$",
              "$5{}40\\text{ m}$",
              "$1{}80\\text{ m}$",
              "$3{}60\\text{ m}$",
              "$4{}80\\text{ m}$"
            ],
            "correct": 1,
            "explanation": "Perímetro do retângulo: $2 \\times (1{}20 + 1{}50) = 2 \\times 2{}70 = 5{}40\\text{ metros}$."
          },
          {
            "q": "Em uma corrida de táxi, cobra-se uma bandeirada fixa de R$ $5{}20$ mais R$ $2{}40$ por quilômetro rodado. Se um passageiro pagou R$ $41{}20$, quantos quilômetros foram percorridos?",
            "options": [
              "$12\\text{ km}$",
              "$15\\text{ km}$",
              "$18\\text{ km}$",
              "$20\\text{ km}$",
              "$14\\text{ km}$"
            ],
            "correct": 1,
            "explanation": "Equação: $2{}40x + 5{}20 = 41{}20 \\Rightarrow 2{}40x = 36{}00 \\Rightarrow x = \\frac{36}{2{}4} = 15\\text{ km}$."
          },
          {
            "q": "Um eletricista possui dois rolos de fios de $120\\text{ m}$ e $180\\text{ m}$. Ele deseja cortar ambos em pedaços de mesmo comprimento, sendo este o maior comprimento possível e sem sobras. Qual deve ser o comprimento de cada pedaço?",
            "options": [
              "$30\\text{ m}$",
              "$40\\text{ m}$",
              "$60\\text{ m}$",
              "$50\\text{ m}$",
              "$20\\text{ m}$"
            ],
            "correct": 2,
            "explanation": "O maior comprimento comum é o $MDC(120, 180)$. Como $120 = 60 \\times 2$ e $180 = 60 \\times 3$, o $MDC = 60\\text{ metros}$."
          },
          {
            "q": "A simplificação da expressão algébrica $\\frac{2^8 \\cdot 4^3}{8^4}$ resulta em:",
            "options": [
              "$2^2$",
              "$2^4$",
              "$2^1$",
              "$2^0$",
              "$2^3$"
            ],
            "correct": 0,
            "explanation": "Transformando tudo na base 2: $4^3 = (2^2)^3 = 2^6$ e $8^4 = (2^3)^4 = 2^{12}$. Numerador: $2^8 \\cdot 2^6 = 2^{14}$. Divisão: $\\frac{2^{14}}{2^{12}} = 2^{14-12} = 2^2 = 4$."
          },
          {
            "q": "Um mastro vertical de $12\\text{ m}$ de altura está fixado ao solo por um cabo de aço esticado preso a $9\\text{ m}$ de sua base. O comprimento do cabo de aço é:",
            "options": [
              "$15\\text{ m}$",
              "$13\\text{ m}$",
              "$16\\text{ m}$",
              "$21\\text{ m}$",
              "$14\\text{ m}$"
            ],
            "correct": 0,
            "explanation": "Por Pitágoras: $C^2 = 12^2 + 9^2 = 144 + 81 = 225 \\Rightarrow C = \\sqrt{225} = 15\\text{ metros}$."
          },
          {
            "q": "Uma piscina em formato de paralelepípedo retângulo tem dimensões de $8\\text{ m}$ de comprimento, $4\\text{ m}$ de largura e $1{}5\\text{ m}$ de profundidade. Sua capacidade total em Litros é:",
            "options": [
              "$48.000\\text{ L}$",
              "$24.000\\text{ L}$",
              "$36.000\\text{ L}$",
              "$40.000\\text{ L}$",
              "$52.000\\text{ L}$"
            ],
            "correct": 0,
            "explanation": "Volume: $V = 8 \\times 4 \\times 1{}5 = 48\\text{ m}^3$. Em litros ($1\\text{ m}^3 = 1000\\text{ L}$): $48 \\times 1000 = 48.000\\text{ Litros}$."
          },
          {
            "q": "Se $6$ máquinas trabalhando no mesmo ritmo produzem $900$ peças em $4\\text{ horas}$, quantas peças $8$ máquinas idênticas produzirão em $6\\text{ horas}$?",
            "options": [
              "$1.200$",
              "$1.500$",
              "$1.800$",
              "$2.000$",
              "$1.600$"
            ],
            "correct": 2,
            "explanation": "Produção por máquina-hora: $\\frac{900}{6 \\times 4} = \\frac{900}{24} = 37{}5\\text{ peças/máq\\cdot h}$. Para 8 máquinas em 6 horas: $8 \\times 6 \\times 37{}5 = 48 \\times 37{}5 = 1.800\\text{ peças}$."
          },
          {
            "q": "As notas de um aluno nas 4 avaliações do semestre foram $6{}0$, $7{}5$, $8{}0$ e $8{}5$. A média aritmética de suas notas é:",
            "options": [
              "$7{}25$",
              "$7{}50$",
              "$7{}75$",
              "$8{}00$",
              "$7{}00$"
            ],
            "correct": 1,
            "explanation": "Média $= \\frac{6{}0 + 7{}5 + 8{}0 + 8{}5}{4} = \\frac{30{}0}{4} = 7{}50$."
          },
          {
            "q": "Em uma loja, um televisor de R$ $2.400,00$ foi comprado com $20\\%$ de entrada e o restante dividido em $4$ parcelas iguais sem juros. O valor de cada parcela é:",
            "options": [
              "R$ $420,00$",
              "R$ $450,00$",
              "R$ $480,00$",
              "R$ $500,00$",
              "R$ $520,00$"
            ],
            "correct": 2,
            "explanation": "Entrada de $20\\% = 0{}20 \\times 2400 = \\text{R\\$} 480,00$. Restante: $2400 - 480 = \\text{R\\$} 1.920,00$. Valor de cada uma das 4 parcelas: $\\frac{1920}{4} = \\text{R\\$} 480,00$."
          },
          {
            "q": "Qual o valor de $x$ que satisfaz o sistema linear $\\begin{cases} 2x + 3y = 23 \\\\ x - y = 4 \\end{cases}$?",
            "options": [
              "$5$",
              "$6$",
              "$7$",
              "$8$",
              "$4$"
            ],
            "correct": 2,
            "explanation": "Da 2ª equação: $y = x - 4$. Substituindo na 1ª: $2x + 3(x - 4) = 23 \\Rightarrow 5x - 12 = 23 \\Rightarrow 5x = 35 \\Rightarrow x = 7$ (e $y = 3$)."
          }
        ],
        "slug": "prova-ifsc-20181",
        "filename": "prova-ifsc-20181.html",
        "folder": "bloco-5-provas-ifsc",
        "blockId": "5",
        "pdf": "20181-Prova.pdf"
      },
      {
        "id": "ifsc-2018-2-matematica",
        "title": "Prova IFSC 2018.2",
        "bncc": "Revisão Geral",
        "summary": "10 questões de Matemática aplicadas no Exame de Classificação 2018.2 do IFSC para Cursos Técnicos Integrados.",
        "detailedTheory": "O Exame 2018.2 aborda análise combinatória introdutória, proporções em escalas cartográficas, equações e polinômios do 2º grau, áreas de triângulos e figuras planas, Teorema de Tales e retas paralelas cortadas por transversais, matemática financeira com taxa de desconto comercial, problemas de frações compostas e interpretação estatística.",
        "keyPoints": [
          "Teorema de Tales: retas paralelas determinam segmentos proporcionais sobre transversais.",
          "Escala $1:E$: uma medida $d$ no mapa equivale a $d \\cdot E$ na realidade.",
          "Fique atento à soma e produto de raízes quadráticas ($S = -b/a$, $P = c/a$)."
        ],
        "formula": "\\frac{a}{b} = \\frac{c}{d}, \\quad S = -\\frac{b}{a}, \\quad P = \\frac{c}{a}",
        "solvedExample": {
          "problem": "Teorema de Tales: segmentos 4 e 6 em uma transversal e 6 e x na outra.",
          "solution": "Montando a proporção direta:\n$\\frac{4}{6} = \\frac{6}{x} \\Rightarrow 4x = 36 \\Rightarrow x = 9$."
        },
        "questions": [
          {
            "q": "Em um mapa na escala $1:50.000$, a distância entre duas cidades é de $6\\text{ cm}$. A distância real em linha reta entre essas cidades é de:",
            "options": [
              "$3\\text{ km}$",
              "$30\\text{ km}$",
              "$300\\text{ km}$",
              "$0{}3\\text{ km}$",
              "$12\\text{ km}$"
            ],
            "correct": 0,
            "explanation": "Distância real $= 6\\text{ cm} \\times 50.000 = 300.000\\text{ cm} = 3.000\\text{ m} = 3\\text{ km}$."
          },
          {
            "q": "Três retas paralelas são cortadas por duas retas transversais. Na primeira transversal os segmentos medem $6\\text{ cm}$ e $9\\text{ cm}$. Na segunda transversal, o segmento correspondente a $6$ mede $8\\text{ cm}$. O outro segmento mede:",
            "options": [
              "$10\\text{ cm}$",
              "$11\\text{ cm}$",
              "$12\\text{ cm}$",
              "$13\\text{ cm}$",
              "$14\\text{ cm}$"
            ],
            "correct": 2,
            "explanation": "Pelo Teorema de Tales: $\\frac{6}{9} = \\frac{8}{x} \\Rightarrow 6x = 72 \\Rightarrow x = 12\\text{ cm}$."
          },
          {
            "q": "A soma e o produto das raízes da equação do segundo grau $2x^2 - 10x + 8 = 0$ valem respectivamente:",
            "options": [
              "$5$ e $4$",
              "$-5$ e $-4$",
              "$10$ e $8$",
              "$5$ e $-4$",
              "$-10$ e $4$"
            ],
            "correct": 0,
            "explanation": "Soma: $S = -\\frac{b}{a} = -\\frac{-10}{2} = 5$. Produto: $P = \\frac{c}{a} = \\frac{8}{2} = 4$."
          },
          {
            "q": "Um terreno triangular tem base medindo $24\\text{ m}$ e altura relativa medindo $15\\text{ m}$. A área desse terreno é:",
            "options": [
              "$360\\text{ m}^2$",
              "$180\\text{ m}^2$",
              "$120\\text{ m}^2$",
              "$240\\text{ m}^2$",
              "$150\\text{ m}^2$"
            ],
            "correct": 1,
            "explanation": "Área do triângulo: $A = \\frac{b \\cdot h}{2} = \\frac{24 \\times 15}{2} = \\frac{360}{2} = 180\\text{ m}^2$."
          },
          {
            "q": "Quantos números pares de $3$ algarismos distintos podemos formar usando os algarismos $\\{1, 2, 3, 4, 5\\}$?",
            "options": [
              "$24$",
              "$36$",
              "$48$",
              "$12$",
              "$60$"
            ],
            "correct": 0,
            "explanation": "Para ser par, o último dígito deve ser $2$ ou $4$ (2 opções). Para a 1ª posição restam 4 algarismos e para a 2ª restam 3 algarismos. Total $= 4 \\times 3 \\times 2 = 24$ números."
          },
          {
            "q": "Um produto anunciado por R$ $450,00$ recebeu um desconto de $12\\%$ para pagamento à vista. Qual o valor pago à vista?",
            "options": [
              "R$ $396,00$",
              "R$ $386,00$",
              "R$ $400,00$",
              "R$ $405,00$",
              "R$ $390,00$"
            ],
            "correct": 0,
            "explanation": "Desconto: $0{}12 \\times 450 = \\text{R\\$} 54,00$. Valor pago: $450 - 54 = \\text{R\\$} 396,00$."
          },
          {
            "q": "Se $\\frac{2}{5}$ do tanque de combustível de um automóvel comporta $24\\text{ litros}$, a capacidade total desse tanque é:",
            "options": [
              "$48\\text{ L}$",
              "$50\\text{ L}$",
              "$60\\text{ L}$",
              "$64\\text{ L}$",
              "$70\\text{ L}$"
            ],
            "correct": 2,
            "explanation": "Capacidade total $T = 24 \\div \\frac{2}{5} = 24 \\times \\frac{5}{2} = 60\\text{ litros}$."
          },
          {
            "q": "O valor da expressão numérica $(-3)^2 - \\sqrt{64} + 2^3 \\div 4$ é:",
            "options": [
              "$1$",
              "$3$",
              "$5$",
              "$7$",
              "$-1$"
            ],
            "correct": 1,
            "explanation": "$(-3)^2 = 9$; $\\sqrt{64} = 8$; $2^3 \\div 4 = 8 \\div 4 = 2$. Calculando: $9 - 8 + 2 = 1 + 2 = 3$."
          },
          {
            "q": "A diagonal de um retângulo que possui lados de $6\\text{ cm}$ e $8\\text{ cm}$ mede:",
            "options": [
              "$10\\text{ cm}$",
              "$12\\text{ cm}$",
              "$14\\text{ cm}$",
              "$15\\text{ cm}$",
              "$9\\text{ cm}$"
            ],
            "correct": 0,
            "explanation": "Por Pitágoras: $d = \\sqrt{6^2 + 8^2} = \\sqrt{36 + 64} = \\sqrt{100} = 10\\text{ cm}$."
          },
          {
            "q": "Em uma pesquisa com $200$ pessoas sobre preferência entre dois produtos A e B: $120$ gostam de A, $100$ gostam de B e $40$ gostam de ambos. Quantas pessoas não gostam de nenhum?",
            "options": [
              "$20$",
              "$30$",
              "$40$",
              "$10$",
              "$50$"
            ],
            "correct": 0,
            "explanation": "Gostam de pelo menos um: $n(A \\cup B) = 120 + 100 - 40 = 180$. Não gostam de nenhum: $200 - 180 = 20$ pessoas."
          }
        ],
        "slug": "prova-ifsc-20182",
        "filename": "prova-ifsc-20182.html",
        "folder": "bloco-5-provas-ifsc",
        "blockId": "5",
        "pdf": "PROVA CORRETA - PUBLICAR.pdf"
      },
      {
        "id": "ifsc-2019-1-matematica",
        "title": "Prova IFSC 2019.1",
        "bncc": "Revisão Geral",
        "summary": "10 questões de Matemática aplicadas no Exame de Classificação 2019.1 do IFSC para Cursos Técnicos Integrados.",
        "detailedTheory": "O Exame 2019.1 aborda cálculo de áreas de figuras planas compostas (lajotamento e corte de áreas centrais), matemática financeira com descontos percentuais sucessivos, sistemas de equações de duas variáveis, potenciação e notação científica, semelhança de triângulos e sombras proporcionais, probabilidade em sorteios, capacidade e volumes geométricos, raízes de equações do 2º grau e conversões de unidades de velocidade.",
        "keyPoints": [
          "Para calcular a área com recortes, subtraia a área não pavimentada da área total do retângulo.",
          "Para converter $\\text{km/h}$ em $\\text{m/s}$, divida por $3{}6$.",
          "A probabilidade é a razão entre eventos favoráveis e o total de eventos possíveis."
        ],
        "formula": "A_{\\text{útil}} = A_{\\text{total}} - A_{\\text{recorte}}, \\quad P = \\frac{n(E)}{n(\\Omega)}, \\quad v = \\frac{\\Delta s}{\\Delta t}",
        "solvedExample": {
          "problem": "Conversão de velocidade: 72 km/h para m/s.",
          "solution": "Dividindo por 3,6:\n$72 \\div 3{}6 = 20\\text{ m/s}$."
        },
        "questions": [
          {
            "q": "Uma escola pretende colocar lajotas em um pátio retangular de $12\\text{ m} \\times 8\\text{ m}$, exceto em um canteiro central circular de raio $2\\text{ m}$ (adote $\\pi = 3{}14$). A área a ser lajotada é:",
            "options": [
              "$83{}44\\text{ m}^2$",
              "$96{}00\\text{ m}^2$",
              "$12{}56\\text{ m}^2$",
              "$75{}20\\text{ m}^2$",
              "$84{}50\\text{ m}^2$"
            ],
            "correct": 0,
            "explanation": "Área total do pátio: $12 \\times 8 = 96\\text{ m}^2$. Área do canteiro circular: $A = 3{}14 \\times 2^2 = 12{}56\\text{ m}^2$. Área lajotada: $96 - 12{}56 = 83{}44\\text{ m}^2$."
          },
          {
            "q": "Um produto que custava R$ $250,00$ sofreu um desconto de $20\\%$ e, na semana seguinte, um novo desconto de $10\\%$ sobre o valor já com desconto. O preço final é:",
            "options": [
              "R$ $175,00$",
              "R$ $180,00$",
              "R$ $190,00$",
              "R$ $200,00$",
              "R$ $170,00$"
            ],
            "correct": 1,
            "explanation": "1º Desconto ($20\\%$): $250 \\times 0{}80 = 200$. 2º Desconto ($10\\%$): $200 \\times 0{}90 = \\text{R\\$} 180,00$."
          },
          {
            "q": "Em uma fazenda há galinhas e vacas, totalizando $35$ cabeças e $100$ pés. Quantas galinhas e quantas vacas há na fazenda?",
            "options": [
              "$20$ galinhas e $15$ vacas",
              "$15$ galinhas e $20$ vacas",
              "$25$ galinhas e $10$ vacas",
              "$18$ galinhas e $17$ vacas",
              "$22$ galinhas e $13$ vacas"
            ],
            "correct": 0,
            "explanation": "Sistema: $g + v = 35$ e $2g + 4v = 100$. Multiplicando a 1ª por $-2$: $2v = 30 \\Rightarrow v = 15$ vacas e $g = 35 - 15 = 20$ galinhas."
          },
          {
            "q": "O valor da expressão com potências $\\frac{10^6 \\times 10^{-2}}{10^3}$ é igual a:",
            "options": [
              "$10$",
              "$100$",
              "$1.000$",
              "$0{}1$",
              "$1$"
            ],
            "correct": 0,
            "explanation": "Numerador: $10^{6 + (-2)} = 10^4$. Divisão: $\\frac{10^4}{10^3} = 10^{4-3} = 10^1 = 10$."
          },
          {
            "q": "Um poste de $6\\text{ m}$ de altura projeta no solo uma sombra de $4\\text{ m}$. No mesmo instante, a sombra projetada por um edifício vizinho é de $24\\text{ m}$. A altura do edifício é:",
            "options": [
              "$36\\text{ m}$",
              "$40\\text{ m}$",
              "$32\\text{ m}$",
              "$48\\text{ m}$",
              "$30\\text{ m}$"
            ],
            "correct": 0,
            "explanation": "Por semelhança de triângulos: $\\frac{H}{24} = \\frac{6}{4} \\Rightarrow 4H = 144 \\Rightarrow H = 36\\text{ metros}$."
          },
          {
            "q": "Em uma urna com $12$ bolas vermelhas, $8$ azuis e $10$ verdes, qual a probabilidade de se retirar, ao acaso, uma bola azul?",
            "options": [
              "$\\frac{4}{15}$",
              "$\\frac{1}{3}$",
              "$\\frac{2}{5}$",
              "$\\frac{1}{4}$",
              "$\\frac{8}{25}$"
            ],
            "correct": 0,
            "explanation": "Total de bolas $= 12 + 8 + 10 = 30$. Probabilidade de bola azul $= \\frac{8}{30} = \\frac{4}{15}$."
          },
          {
            "q": "Um reservatório com formato cúbico tem aresta medindo $2\\text{ metros}$. Quantos litros de água comportará quando estiver com $75\\%$ de sua capacidade total preenchida?",
            "options": [
              "$6.000\\text{ L}$",
              "$8.000\\text{ L}$",
              "$4.000\\text{ L}$",
              "$7.500\\text{ L}$",
              "$5.000\\text{ L}$"
            ],
            "correct": 0,
            "explanation": "Volume total $= 2^3 = 8\\text{ m}^3 = 8.000\\text{ Litros}$. Com $75\\%$ de capacidade: $8.000 \\times 0{}75 = 6.000\\text{ Litros}$."
          },
          {
            "q": "As raízes reais da equação $x^2 - 4x - 21 = 0$ são:",
            "options": [
              "$7$ e $-3$",
              "$-7$ e $3$",
              "$7$ e $3$",
              "$-7$ e $-3$",
              "$14$ e $-6$"
            ],
            "correct": 0,
            "explanation": "Discriminante $\\Delta = (-4)^2 - 4(1)(-21) = 16 + 84 = 100$. Raízes: $x = \\frac{4 \\pm 10}{2} \\Rightarrow x_1 = 7$ e $x_2 = -3$."
          },
          {
            "q": "Um veículo percorre uma distância de $180\\text{ km}$ em $2\\text{ horas e } 30\\text{ minutos}$. Sua velocidade média foi de:",
            "options": [
              "$72\\text{ km/h}$",
              "$80\\text{ km/h}$",
              "$75\\text{ km/h}$",
              "$90\\text{ km/h}$",
              "$65\\text{ km/h}$"
            ],
            "correct": 0,
            "explanation": "Tempo em horas: $2\\text{h } 30\\text{min} = 2{}5\\text{ horas}$. Velocidade média $= \\frac{180}{2{}5} = 72\\text{ km/h}$."
          },
          {
            "q": "O perímetro de um triângulo isósceles é $36\\text{ cm}$ e sua base mede $10\\text{ cm}$. A área desse triângulo é:",
            "options": [
              "$60\\text{ cm}^2$",
              "$120\\text{ cm}^2$",
              "$65\\text{ cm}^2$",
              "$50\\text{ cm}^2$",
              "$70\\text{ cm}^2$"
            ],
            "correct": 0,
            "explanation": "Os dois lados congruentes somam $36 - 10 = 26\\text{ cm}$, logo cada um mede $13\\text{ cm}$. A altura divide a base em dois segmentos de $5\\text{ cm}$. Por Pitágoras: $h = \\sqrt{13^2 - 5^2} = \\sqrt{169 - 25} = 12\\text{ cm}$. Área $= \\frac{10 \\times 12}{2} = 60\\text{ cm}^2$."
          }
        ],
        "slug": "prova-ifsc-20191",
        "filename": "prova-ifsc-20191.html",
        "folder": "bloco-5-provas-ifsc",
        "blockId": "5",
        "pdf": "2019 1 INT - PROVA.pdf"
      },
      {
        "id": "ifsc-2019-2-matematica",
        "title": "Prova IFSC 2019.2",
        "bncc": "Revisão Geral",
        "summary": "10 questões de Matemática aplicadas no Exame de Classificação 2019.2 do IFSC para Cursos Técnicos Integrados.",
        "detailedTheory": "O Exame 2019.2 trabalha vazão volumétrica em galão cilíndrico, propriedades de potências e fatores primos, soma e fração de raízes quadráticas, classificação de números primos e amigos, Teorema de Pitágoras e distâncias fracionárias de percurso aéreo, espaçamento máximo de postes com MDC, regra de três composta para produção, consumo de combustível e custos de viagem, sistemas lineares com 4 incógnitas e áreas sombreadas circulares com retângulos circunscritos.",
        "keyPoints": [
          "Em problemas de vazão, converta o volume em $\\text{m}^3$ para $\\text{cm}^3$ ($1\\text{ m}^3 = 10^6\\text{ cm}^3$) antes de dividir pela vazão.",
          "Para espaçamento igual de postes em todo o contorno, calcule o MDC das dimensões e divida o perímetro pelo MDC.",
          "Em sistemas cíclicos simétricos, somar todas as equações fornece a soma total das variáveis."
        ],
        "formula": "V_{\\text{cilindro}} = \\pi r^2 h, \\quad \\text{Postes} = \\frac{2(C + L)}{\\text{MDC}(C, L)}, \\quad a^2 = b^2 + c^2",
        "solvedExample": {
          "problem": "Postes na praça retangular de 195 m por 255 m nos vértices e com espaçamento máximo igual.",
          "solution": "MDC(195, 255): $195 = 15 \\times 13$ e $255 = 15 \\times 17$. MDC = 15 m.\nPerímetro $= 2(195 + 255) = 2(450) = 900\\text{ m}$.\nQuantidade mínima de postes $= 900 / 15 = 60$ postes."
        },
        "questions": [
          {
            "q": "Um galão cilíndrico de $0{}8\\text{ m}$ de diâmetro (raio $0{}4\\text{ m}$) e $1{}5\\text{ m}$ de altura está com $75\\%$ de sua capacidade preenchida com água. Um pequeno furo vaza $5\\text{ cm}^3$ de água por segundo. Adotando $\\pi = 3{}14$, o galão ficará vazio após:",
            "options": [
              "$7\\text{ horas e } 51\\text{ minutos}$",
              "$41\\text{ horas e } 52\\text{ minutos}$",
              "$628\\text{ horas}$",
              "$31\\text{ horas e } 24\\text{ minutos}$",
              "$15\\text{ horas e } 42\\text{ minutos}$"
            ],
            "correct": 3,
            "explanation": "Volume total: $V = 3{}14 \\times 0{}4^2 \\times 1{}5 = 0{}7536\\text{ m}^3 = 753.600\\text{ cm}^3$. Volume com $75\\% = 753.600 \\times 0{}75 = 565.200\\text{ cm}^3$. Tempo $= 565.200 / 5 = 113.040\\text{ segundos} = 1.884\\text{ minutos} = 31\\text{ horas e } 24\\text{ minutos}$."
          },
          {
            "q": "Uma fábrica de lápis vende caixas com $12$ unidades. As caixas são organizadas em caixotes com $12$ pilhas de $12$ caixas cada. Um caminhão transporta $12$ caixotes. A expressão que informa o total de lápis transportados por viagem é:",
            "options": [
              "$4 \\cdot 12^4$",
              "$4 \\cdot 12$",
              "$2^2 \\cdot 3$",
              "$2^6 \\cdot 3^4$",
              "$2^8 \\cdot 3^4$"
            ],
            "correct": 4,
            "explanation": "Total de lápis $= 12 \\times 12 \\times 12 \\times 12 = 12^4$. Fatorando $12 = 2^2 \\cdot 3$: $12^4 = (2^2 \\cdot 3)^4 = 2^8 \\cdot 3^4$."
          },
          {
            "q": "Dada a equação $-(3x - 2)(x - 6) = x(6 - x) + 8$, o quadrado da terça parte da soma de suas raízes é:",
            "options": [
              "$49/6$",
              "$14/9$",
              "$14/3$",
              "$7/3$",
              "$49/9$"
            ],
            "correct": 4,
            "explanation": "Desenvolvendo: $-(3x^2 - 20x + 12) = 6x - x^2 + 8 \\Rightarrow -3x^2 + 20x - 12 = -x^2 + 6x + 8 \\Rightarrow -2x^2 + 14x - 20 = 0 \\Rightarrow x^2 - 7x + 10 = 0$. Soma das raízes $= 7$. Terça parte $= 7/3$. Quadrado da terça parte $= (7/3)^2 = 49/9$."
          },
          {
            "q": "Analise as afirmações sobre números primos e divisibilidade (V ou F):\\n( ) Os números $220$ e $284$ são amigos (soma dos divisores próprios de um é igual ao outro).\\n( ) Todo número natural que termina em $6$ é divisível por $3$.\\n( ) O número $153$ possui $6$ divisores naturais.\\n( ) O número $14367$ é um número primo.\\n( ) O máximo divisor comum entre $510$ e $238$ é $34$.",
            "options": [
              "V – F – V – F – V",
              "V – F – F – V – F",
              "V – F – F – F – V",
              "F – V – F – V – F",
              "F – F – V – F – V"
            ],
            "correct": 0,
            "explanation": "1ª: 220 e 284 são amigos clássicos (V). 2ª: Falsa, ex: 16 termina em 6 e não é divisível por 3 (F). 3ª: $153 = 3^2 \\times 17^1 \\Rightarrow (2+1)(1+1) = 6$ divisores (V). 4ª: $1+4+3+6+7=21$ (divisível por 3, não é primo) (F). 5ª: $510 = 34 \\times 15$ e $238 = 34 \\times 7$, logo $MDC=34$ (V). Sequência: V - F - V - F - V."
          },
          {
            "q": "Um avião partiu da cidade A para B ($800\\text{ km}$) e depois para C ($600\\text{ km}$), com ângulo de $90^\\circ$ em B. Ao retornar de C para A (trajeto reto de $1000\\text{ km}$), o piloto mudou de rota no ponto P ao completar $2/5$ do trajeto de C para A. Sabendo que a distância de P a E é igual à distância de P a A, a distância de P a E é:",
            "options": [
              "$800\\text{ km}$",
              "$400\\text{ km}$",
              "$500\\text{ km}$",
              "$1000\\text{ km}$",
              "$600\\text{ km}$"
            ],
            "correct": 4,
            "explanation": "Por Pitágoras: $AC = \\sqrt{800^2 + 600^2} = 1000\\text{ km}$. Se completou $2/5$ do trajeto $CA$, percorreu $CP = \\frac{2}{5} \\times 1000 = 400\\text{ km}$. O segmento restante $PA = 1000 - 400 = 600\\text{ km}$. Como $PE = PA$, temos $PE = 600\\text{ km}$."
          },
          {
            "q": "Uma prefeitura instalará postes de iluminação igualmente espaçados em uma praça retangular de $195\\text{ m} \\times 255\\text{ m}$. Em cada vértice haverá um poste e a distância inteira entre postes consecutivos será a máxima possível. A quantidade mínima de postes necessária é:",
            "options": [
              "$52\\text{ postes}$",
              "$60\\text{ postes}$",
              "$56\\text{ postes}$",
              "$48\\text{ postes}$",
              "$44\\text{ postes}$"
            ],
            "correct": 1,
            "explanation": "Maior espaçamento $= MDC(195, 255) = 15\\text{ m}$. Perímetro $= 2(195 + 255) = 900\\text{ m}$. Quantidade mínima de postes $= \\frac{900}{15} = 60\\text{ postes}$."
          },
          {
            "q": "Uma máquina fabrica $5.625\\text{ kg}$ de gelo trabalhando $9\\text{ horas por dia}$ durante $5\\text{ dias}$. Quantas horas por dia deverá trabalhar para fabricar $5.000\\text{ kg}$ de gelo em $4\\text{ dias}$?",
            "options": [
              "$12\\text{ horas por dia}$",
              "$8\\text{ horas por dia}$",
              "$10\\text{ horas por dia}$",
              "$7\\text{ horas por dia}$",
              "$13\\text{ horas por dia}$"
            ],
            "correct": 2,
            "explanation": "Produção horária: $\\frac{5625}{9 \\times 5} = \\frac{5625}{45} = 125\\text{ kg/h}$. Para $5000\\text{ kg}$ em 4 dias: Horas totais $= \\frac{5000}{125} = 40\\text{ h}$. Horas por dia $= \\frac{40}{4} = 10\\text{ horas por dia}$."
          },
          {
            "q": "O carro de Marcos consome $4\\text{ litros}$ de gasolina a cada $48\\text{ km}$. Para uma viagem de ida e volta entre duas cidades distantes $360\\text{ km}$ entre si, com a gasolina a R$ $4{}50$ o litro, o gasto mínimo será:",
            "options": [
              "R$ $270,00$",
              "R$ $250,50$",
              "R$ $280,50$",
              "R$ $300,00$",
              "R$ $290,50$"
            ],
            "correct": 0,
            "explanation": "Rendimento: $\\frac{48}{4} = 12\\text{ km/L}$. Distância total (ida e volta): $360 \\times 2 = 720\\text{ km}$. Litros necessários: $\\frac{720}{12} = 60\\text{ L}$. Custo: $60 \\times 4{}50 = \\text{R\\$} 270,00$."
          },
          {
            "q": "Quatro amigas (Isabelle, Fabiana, Sofia e Clara) contaram seus montes de areia:\\n• Isabelle, Fabiana e Sofia: $27$ montes\\n• Fabiana, Sofia e Clara: $32$ montes\\n• Sofia, Clara e Isabelle: $28$ montes\\n• Clara, Isabelle e Fabiana: $33$ montes\\nQuantos montes de areia foram feitos pelas $4$ meninas juntas?",
            "options": [
              "$80\\text{ montes}$",
              "$120\\text{ montes}$",
              "$40\\text{ montes}$",
              "$60\\text{ montes}$",
              "$100\\text{ montes}$"
            ],
            "correct": 2,
            "explanation": "Somando as 4 equações, cada menina é contada 3 vezes: $3(I + F + S + C) = 27 + 32 + 28 + 33 = 120$. Portanto, $I + F + S + C = \\frac{120}{3} = 40\\text{ montes}$."
          },
          {
            "q": "Em uma quadra de basquete, a figura representa um retângulo $ABCD$ circuncrevendo a metade de uma circunferência de centro $O$ e raio $OA = r$. Se a área do retângulo $ABCD$ é $8\\text{ m}^2$, qual é a área do círculo completo?",
            "options": [
              "$4\\pi\\text{ m}^2$",
              "$16\\pi\\text{ m}^2$",
              "$8\\pi\\text{ m}^2$",
              "$6\\pi\\text{ m}^2$",
              "$10\\pi\\text{ m}^2$"
            ],
            "correct": 0,
            "explanation": "O retângulo tem comprimento $AB = 2r$ e altura $AD = r$. Sua área é $2r \\cdot r = 2r^2 = 8 \\Rightarrow r^2 = 4$. A área do círculo completo é $A = \\pi r^2 = 4\\pi\\text{ m}^2$."
          }
        ],
        "slug": "prova-ifsc-20192",
        "filename": "prova-ifsc-20192.html",
        "folder": "bloco-5-provas-ifsc",
        "blockId": "5",
        "pdf": "PROVA 2019.2 - FINAL.pdf"
      },
      {
        "id": "ifsc-2020-1-matematica",
        "title": "Prova IFSC 2020.1",
        "bncc": "Revisão Geral",
        "summary": "10 questões de Matemática aplicadas no Exame de Classificação 2020.1 do IFSC para Cursos Técnicos Integrados.",
        "detailedTheory": "Esta seção reúne as 10 questões originais de Matemática cobradas no Exame de Classificação do IFSC 2020.1: semelhança de triângulos na pirâmide de Queóps, propriedades de potências com bases compostas, conversão de tempo para decimais de hora, Teoria dos Conjuntos (Diagrama de Venn com 3 conjuntos), matemática financeira com comissão sobre vendas, geometria analítica plana e distâncias euclidianas, cálculo de IMC com raízes quadradas, Teorema de Pitágoras com incógnitas nos catetos e regra de três composta para atendimento ao público.",
        "keyPoints": [
          "Na semelhança de triângulos, monte a razão direta entre altura e sombra.",
          "No diagrama de Venn de 3 conjuntos, inicie sempre o preenchimento pela interseção central.",
          "Lembre-se: $(x^a)^b = x^{a \\cdot b}$."
        ],
        "formula": "\\frac{h_1}{s_1} = \\frac{h_2}{s_2}, \\quad (a^m)^n = a^{m \\cdot n}, \\quad \\text{IMC} = \\frac{P}{h^2}",
        "solvedExample": {
          "problem": "Potências equivalentes: compare $x = 20^{100}$ e $y = 400^{50}$.",
          "solution": "Como $400 = 20^2$, temos $y = (20^2)^{50} = 20^{100}$.\nLogo, $x = y$."
        },
        "questions": [
          {
            "q": "Sabendo que uma vara de $2\\text{ m}$ projeta uma sombra de $3\\text{ m}$, e a distância correspondente à sombra da pirâmide de Queóps é de $210\\text{ m}$, qual é a altura aproximada da pirâmide?",
            "options": [
              "$160\\text{ m}$",
              "$140\\text{ m}$",
              "$150\\text{ m}$",
              "$180\\text{ m}$",
              "$170\\text{ m}$"
            ],
            "correct": 1,
            "explanation": "Por semelhança de triângulos: $\\frac{H}{210} = \\frac{2}{3} \\Rightarrow 3H = 420 \\Rightarrow H = 140\\text{ m}$."
          },
          {
            "q": "Sabendo que $x = 20^{100}$ e $y = 400^{50}$, pode-se afirmar que:",
            "options": [
              "$x$ é igual a $y$.",
              "$x$ é a metade de $y$.",
              "$x$ é o dobro de $y$.",
              "$x$ é igual ao quadrado de $y$.",
              "$x$ é igual ao quádruplo de $y$."
            ],
            "correct": 0,
            "explanation": "Como $400 = 20^2$, reescrevemos $y = (20^2)^{50} = 20^{2 \\times 50} = 20^{100}$. Portanto, $x = y$."
          },
          {
            "q": "O índice olímpico para a prova da Maratona Feminina é de $2\\text{h } 29\\text{min } 30\\text{s}$. O valor correspondente expresso apenas na unidade de tempo horas é:",
            "options": [
              "$2{}5001\\text{h}$",
              "$2{}4899\\text{h}$",
              "$2{}4916\\text{h}$",
              "$2{}2930\\text{h}$",
              "$2{}5102\\text{h}$"
            ],
            "correct": 2,
            "explanation": "$30\\text{s} = 0{}5\\text{min}$. Temos $29{}5\\text{min} \\div 60 \\approx 0{}49166\\text{h}$. Somando com $2\\text{h}$ temos $2{}4916\\text{h}$."
          },
          {
            "q": "Pesquisa com $75$ estudantes: $5$ leram A, B e C; $7$ leram A e B; $8$ leram A e C; $6$ leram B e C; $10$ apenas A; $12$ apenas B; e $15$ apenas C. Quantos estudantes não leram nenhum dos três livros?",
            "options": [
              "$20$",
              "$12$",
              "$32$",
              "$15$",
              "$27$"
            ],
            "correct": 4,
            "explanation": "Interseções exclusivas: A e B apenas $= 7-5=2$; A e C apenas $= 8-5=3$; B e C apenas $= 6-5=1$. Total que leu pelo menos um: $10 + 12 + 15 + 2 + 3 + 1 + 5 = 48$. Não leram nenhum: $75 - 48 = 27$."
          },
          {
            "q": "Uma loja vende 5 produtos com preços: A (R$ 350), B (R$ 437,50), C (R$ 292,70), D (R$ 195) e E (R$ 280). O vendedor ganha salário fixo de R$ 1.080 mais 10% de comissão. É correto afirmar que:",
            "options": [
              "Vendendo 1 de cada, o valor adicional será superior a R$ 200,00.",
              "Vendendo 1 de cada, o valor adicional será mais de 20% do salário-base.",
              "Vendendo 5 de cada, seu salário total será superior a R$ 2.000,00.",
              "Vendendo 5 de cada, o adicional será mais de 70% do salário-base.",
              "Vendendo 5 de cada, o adicional será igual ao salário-base."
            ],
            "correct": 3,
            "explanation": "Soma de 1 unidade de cada: R$ $1.555,20$. Adicional unitário ($10\\%$) = R$ $155,52$. Vendendo 5 de cada, o adicional é $5 \\times 155,52 = \\text{R\\$} 777,60$. Como $70\\%$ do salário base ($1.080$) é R$ $756,00$, o adicional supera $70\\%$ do salário."
          },
          {
            "q": "A partir do desenho da peça plana, analise as afirmações: I. Coordenadas de H são $(120, 60)$; II. O segmento IJ mede $20\\sqrt{2}\\text{ cm}$; III. O arco BC mede $0,1\\pi\\text{ m}$; IV. O perímetro da peça é maior que $0,29\\text{ m}$. Quantas afirmações estão corretas?",
            "options": [
              "$0$",
              "$1$",
              "$2$",
              "$3$",
              "$4$ (todas)"
            ],
            "correct": 4,
            "explanation": "Todas as 4 afirmativas são verdadeiras com base nas cotas e aplicações do Teorema de Pitágoras e arcos circulares da peça."
          },
          {
            "q": "As distâncias entre as casas de Fábio e Saulo e Fábio e Carlos são $3\\text{ km}$ e $9\\text{ km}$. O arco de Saulo a Carlos tem centro em Ivan e ângulo reto em Fábio. Qual a distância entre as casas de Ivan (I) e Fábio (F)?",
            "options": [
              "$10\\text{ km}$",
              "$12\\text{ km}$",
              "$14\\text{ km}$",
              "$15\\text{ km}$",
              "$16\\text{ km}$"
            ],
            "correct": 1,
            "explanation": "Raio $R = IF + 3$. No triângulo retângulo em F: $R^2 = IF^2 + 9^2 \\Rightarrow (IF + 3)^2 = IF^2 + 81 \\Rightarrow 6IF + 9 = 81 \\Rightarrow 6IF = 72 \\Rightarrow IF = 12\\text{ km}$."
          },
          {
            "q": "Se uma pessoa possui IMC igual a $40\\text{ kg/m}^2$ e peso de $120\\text{ kg}$, o valor mais aproximado de sua altura ($h$) é:",
            "options": [
              "$1{}4\\text{ m}$",
              "$1{}5\\text{ m}$",
              "$1{}6\\text{ m}$",
              "$1{}7\\text{ m}$",
              "$1{}8\\text{ m}$"
            ],
            "correct": 3,
            "explanation": "$\\text{IMC} = \\frac{P}{h^2} \\Rightarrow 40 = \\frac{120}{h^2} \\Rightarrow h^2 = 3 \\Rightarrow h = \\sqrt{3} \\approx 1{}732\\text{ metros}$."
          },
          {
            "q": "Um triângulo retângulo possui catetos $(x-2)\\text{ m}$ e $(x+5)\\text{ m}$ e hipotenusa $(x+7)\\text{ m}$. João caminha pelos catetos e Maria pela hipotenusa. O trajeto de Maria em relação ao de João é:",
            "options": [
              "$6\\text{ metros menor}$",
              "$4\\text{ metros menor}$",
              "de mesma distância",
              "$4\\text{ metros maior}$",
              "$6\\text{ metros maior}$"
            ],
            "correct": 0,
            "explanation": "Por Pitágoras: $(x-2)^2 + (x+5)^2 = (x+7)^2 \\Rightarrow x^2 - 8x - 20 = 0 \\Rightarrow x = 10$. Catetos: $8$ e $15$ (João anda $23\\text{m}$). Hipotenusa: $17$ (Maria anda $17\\text{m}$). Diferença: $6\\text{ metros a menos}$ para Maria."
          },
          {
            "q": "$3$ colaboradores atendem $80$ alunos em $4\\text{ horas}$. Quantas horas $4$ colaboradores levariam para atender $160$ alunos no mesmo ritmo?",
            "options": [
              "$3\\text{ horas}$",
              "$5\\text{ horas}$",
              "$6\\text{ horas}$",
              "$8\\text{ horas}$",
              "$9\\text{ horas}$"
            ],
            "correct": 2,
            "explanation": "Regra de três composta: $\\frac{4}{x} = \\frac{4}{3} \\times \\frac{80}{160} = \\frac{4}{3} \\times \\frac{1}{2} = \\frac{4}{6} \\Rightarrow x = 6\\text{ horas}$."
          }
        ],
        "slug": "prova-ifsc-20201",
        "filename": "prova-ifsc-20201.html",
        "folder": "bloco-5-provas-ifsc",
        "blockId": "5",
        "pdf": "2020 1 INT PROVA_FINAL-1.pdf"
      },
      {
        "id": "ifsc-2022-1-matematica",
        "title": "Prova IFSC 2022.1",
        "bncc": "Revisão Geral",
        "summary": "10 questões de Matemática aplicadas no Exame de Classificação 2022.1 do IFSC para Cursos Técnicos Integrados.",
        "detailedTheory": "O Exame 2022.1 aborda simplificação de somas telescópicas pares e ímpares, ganho real com inflação e aumento salarial, geometria plana com circunferências tangentes a quadrados, polígonos e contagem geométrica, simplificação e raízes de polinômios fatorados, volume de cilindro com variação de raio e altura, propriedades da divisão euclidiana de inteiros, frações de áreas em retângulos e propriedades de números primos em coeficientes quadráticos.",
        "keyPoints": [
          "Para ganho real de salário com inflação, utilize a relação $(1 + i_{\\text{real}}) = \\frac{1 + i_{\\text{sal}}}{1 + i_{\\text{inf}}}$.",
          "Se a soma de dois primos é ímpar, um deles deve ser obrigatoriamente o número 2.",
          "A diferença entre a soma dos pares consecutivos e a soma dos ímpares consecutivos de 1 a 2022 é igual ao número de pares (1011)."
        ],
        "formula": "1 + i_{\\text{real}} = \\frac{1 + i_{\\text{sal}}}{1 + i_{\\text{inf}}}, \\quad V = \\pi r^2 h, \\quad S = x_1 + x_2",
        "solvedExample": {
          "problem": "Raízes primas de $x^2 - 55x + c = 0$.",
          "solution": "A soma das raízes é 55. Como 55 é ímpar, uma raiz prima é 2 e a outra é 53.\nO produto das raízes é $c = 2 \\times 53 = 106$."
        },
        "questions": [
          {
            "q": "Sofia simplificou a fração $\\frac{(2 + 4 + 6 + \\dots + 2022) - (1 + 3 + 5 + \\dots + 2021)}{2022 \\cdot 45 - 35 \\cdot 2022}$. A fração irredutível obtida é:",
            "options": [
              "$\\frac{1}{20}$",
              "$\\frac{1}{10}$",
              "$\\frac{1011}{2022}$",
              "$\\frac{1}{2}$",
              "$\\frac{2}{5}$"
            ],
            "correct": 0,
            "explanation": "O numerador é a soma de $1011$ diferenças $(2-1)+(4-3)+\\dots+(2022-2021) = 1011 \\times 1 = 1011$. O denominador é $2022(45 - 35) = 2022 \\times 10 = 20220$. Fração: $\\frac{1011}{20220} = \\frac{1}{20}$."
          },
          {
            "q": "Em 2021, o salário de Antônio aumentou $26\\%$, enquanto os preços subiram $20\\%$. Quanto aumentou o poder de compra real de Antônio?",
            "options": [
              "$6\\%$",
              "$5\\%$",
              "$4{}8\\%$",
              "$5{}2\\%$",
              "$6{}2\\%$"
            ],
            "correct": 1,
            "explanation": "Fator real $= \\frac{1{}26}{1{}20} = 1{}05$, o que corresponde a um aumento real de $5\\%$."
          },
          {
            "q": "José Carlos desenhou um quadrado ABCD de lado $48\\text{ cm}$ e uma circunferência tangente aos lados. A distância máxima da circunferência aos vértices opostos é calculada por:",
            "options": [
              "$24\\text{ cm}$",
              "$48\\sqrt{2}\\text{ cm}$",
              "$24(\\sqrt{2} - 1)\\text{ cm}$",
              "$24\\sqrt{2}\\text{ cm}$",
              "$12\\text{ cm}$"
            ],
            "correct": 2,
            "explanation": "O raio é $r = 24\\text{ cm}$. A distância do centro ao vértice é a metade da diagonal: $24\\sqrt{2}$. A distância da borda ao vértice é $24\\sqrt{2} - 24 = 24(\\sqrt{2} - 1)\\text{ cm}$."
          },
          {
            "q": "Arthur desenhou um gato geométrico composto por polígonos regulares e triângulos retângulos. A soma dos ângulos internos de todas as faces poligonais totaliza:",
            "options": [
              "$1.080^\\circ$",
              "$1.260^\\circ$",
              "$1.440^\\circ$",
              "$1.800^\\circ$",
              "$2.160^\\circ$"
            ],
            "correct": 2,
            "explanation": "Somando as contribuições angulares dos triângulos ($180^\\circ$), quadriláteros ($360^\\circ$) e pentágonos da figura, totaliza-se $1.440^\\circ$."
          },
          {
            "q": "Observe a expressão polinomial $P(a) = (2 - a) - (4a - 3) - 5a(1 - a)$. Ao simplificar $P(a) = 0$, as raízes são:",
            "options": [
              "$1$ e $-1$",
              "$1$ e $1$",
              "$1$ e $-2$",
              "$0$ e $2$",
              "$-1$ e $2$"
            ],
            "correct": 0,
            "explanation": "Desenvolvendo: $2 - a - 4a + 3 - 5a + 5a^2 = 5a^2 - 10a + 5 = 5(a^2 - 2a + 1) = 5(a - 1)^2$. As raízes são reais e iguais a $1$."
          },
          {
            "q": "Uma piscina cilíndrica de diâmetro $D$ e altura $h$ tem volume $V$. Se duplicarmos o diâmetro e reduzirmos a altura pela metade, o novo volume será:",
            "options": [
              "$V$",
              "$2V$",
              "$4V$",
              "$V/2$",
              "$8V$"
            ],
            "correct": 1,
            "explanation": "O raio duplica ($2r$), logo a área da base quadruplica ($4A_b$). A altura cai pela metade ($h/2$). O novo volume é $4A_b \\times (h/2) = 2(A_b h) = 2V$."
          },
          {
            "q": "Leonardo pensou em um número, dividiu-o por $2021$ e obteve resto $1021$. Ao dividir o mesmo número por $43$, o resto obtido é:",
            "options": [
              "$32$",
              "$21$",
              "$15$",
              "$18$",
              "$25$"
            ],
            "correct": 0,
            "explanation": "$N = 2021q + 1021$. Como $2021 = 43 \\times 47$, o termo $2021q$ é divisível por $43$. Resta dividir $1021$ por $43$: $1021 = 43 \\times 23 + 32$. O resto é $32$."
          },
          {
            "q": "Lara dividiu um painel retangular em quatro retângulos menores. Três deles possuem áreas de $12\\text{ m}^2$, $18\\text{ m}^2$ e $24\\text{ m}^2$. A área do quarto retângulo é:",
            "options": [
              "$36\\text{ m}^2$",
              "$30\\text{ m}^2$",
              "$28\\text{ m}^2$",
              "$32\\text{ m}^2$",
              "$40\\text{ m}^2$"
            ],
            "correct": 0,
            "explanation": "Em uma grade $2 \\times 2$ de retângulos, o produto das áreas diagonais é igual: $A_1 \\times A_4 = A_2 \\times A_3 \\Rightarrow 12 \\times A_4 = 18 \\times 24 = 432 \\Rightarrow A_4 = 36\\text{ m}^2$."
          },
          {
            "q": "Graciele numerou círculos de $1$ a $16$ de modo que as somas das linhas fossem todas iguais. A soma constante obtida em cada linha é:",
            "options": [
              "$34$",
              "$38$",
              "$40$",
              "$42$",
              "$36$"
            ],
            "correct": 0,
            "explanation": "A soma de 1 a 16 é $\\frac{16 \\times 17}{2} = 136$. Distribuindo em 4 linhas simétricas: $\\frac{136}{4} = 34$."
          },
          {
            "q": "Ambas as raízes da equação $x^2 - 55x + c = 0$ são números primos. O único valor possível de $c$ é:",
            "options": [
              "$106$",
              "$110$",
              "$100$",
              "$114$",
              "$108$"
            ],
            "correct": 0,
            "explanation": "A soma das raízes é $55$ (número ímpar). A única forma de somar dois primos e obter ímpar é quando um dos primos é $2$. Logo, o outro primo é $55 - 2 = 53$. O valor de $c = 2 \\times 53 = 106$."
          }
        ],
        "slug": "prova-ifsc-20221",
        "filename": "prova-ifsc-20221.html",
        "folder": "bloco-5-provas-ifsc",
        "blockId": "5",
        "pdf": "PRV 2022.pdf"
      },
      {
        "id": "ifsc-2022-2-matematica",
        "title": "Prova IFSC 2022.2",
        "bncc": "Revisão Geral",
        "summary": "10 questões de Matemática aplicadas no Exame de Classificação 2022.2 do IFSC para Cursos Técnicos Integrados.",
        "detailedTheory": "O Exame 2022.2 aborda propriedades dos números reais e valor absoluto, semelhança e trigonometria em medição de altura da Torre Eiffel, proporcionalidade e porcentagens em taxas de transmissão de COVID-19, sistemas lineares de compras de toalhas, regra de três simples em diárias de trabalho, teoria dos conjuntos em turmas esportivas, equações quadráticas com relações entre raízes, cálculo de volumes de caixas e reservatórios de água, estudo de sinais de inequações produto de 1º grau e funções lineares de transporte intermunicipal.",
        "keyPoints": [
          "Para inequações produto $(x+5)(x-1)(x-2) > 0$, faça o quadro de sinais dos fatores.",
          "Em problemas de trabalho com dias proporcionais, monte a regra de três direta para o pagamento.",
          "Para determinar a altura da Torre Eiffel, some a altura dos olhos com o produto da distância pela tangente."
        ],
        "formula": "H = d \\cdot \\tan(\\theta) + h_{\\text{obs}}, \\quad (x-r_1)(x-r_2)(x-r_3) > 0, \\quad C(x) = ax + b",
        "solvedExample": {
          "problem": "Inequação produto: $(x+5)(x-1)(x-2) > 0$.",
          "solution": "As raízes são $-5$, $1$ e $2$.\nFazendo o varal de sinais:\nPara $x < -5$: $(-)(-)(-) = -$ (negativo)\nPara $-5 < x < 1$: $(+)(-)(-) = +$ (positivo)\nPara $1 < x < 2$: $(+)(+)(-) = -$ (negativo)\nPara $x > 2$: $(+)(+)(+) = +$ (positivo)\nSolução: $]-5, 1[ \\cup ]2, +\\infty[$."
        },
        "questions": [
          {
            "q": "Considerando que $x$ e $y$ são números reais quaisquer, analise as expressões sobre propriedades de potenciação e radiciação e assinale a alternativa com as sentenças verdadeiras:",
            "options": [
              "São verdadeiras I e IV",
              "São verdadeiras III e IV",
              "São verdadeiras I e II",
              "São verdadeiras II e III",
              "Todas são verdadeiras"
            ],
            "correct": 0,
            "explanation": "I e IV preservam rigorosamente a definição algébrica e a não negatividade do radicando para expoentes pares."
          },
          {
            "q": "Um observador a $300\\text{ m}$ da base da Torre Eiffel mira o topo sob ângulo cuja tangente vale $1{}08$. Se o teodolito está a $1{}5\\text{ m}$ do solo, a altura total da Torre é de aproximadamente:",
            "options": [
              "$300\\text{ m}$",
              "$324\\text{ m}$",
              "$350\\text{ m}$",
              "$360\\text{ m}$",
              "$325{}5\\text{ m}$"
            ],
            "correct": 4,
            "explanation": "Altura do topo em relação ao teodolito: $h_1 = 300 \\times 1{}08 = 324\\text{ m}$. Altura total: $324 + 1{}5 = 325{}5\\text{ metros}$."
          },
          {
            "q": "Em uma pesquisa epidemiológica sobre COVID-19, a taxa de contágio indicava que $20$ pessoas transmitiam para $25$ pessoas. Em uma comunidade com $400$ infectados, o total estimado de novas transmissões é:",
            "options": [
              "$450$",
              "$500$",
              "$550$",
              "$600$",
              "$480$"
            ],
            "correct": 1,
            "explanation": "Taxa: $\\frac{25}{20} = 1{}25$. Para 400 pessoas: $400 \\times 1{}25 = 500$ novos infectados."
          },
          {
            "q": "Uma microempreendedora comprou $100$ toalhas (médias e grandes) por R$ $1.800,00$. A toalha média custou R$ $15,00$ e a grande R$ $25,00$. Quantas toalhas grandes foram compradas?",
            "options": [
              "$30$",
              "$40$",
              "$50$",
              "$60$",
              "$35$"
            ],
            "correct": 0,
            "explanation": "Sistema: $m + g = 100$ e $15m + 25g = 1800$. Multiplicando a 1ª por $-15$: $10g = 300 \\Rightarrow g = 30$ toalhas grandes (e $m = 70$)."
          },
          {
            "q": "Dois trabalhadores realizam um serviço em $9\\text{ dias}$, recebendo R$ $10.000,00$. Quanto receberão se trabalharem por $15\\text{ dias}$ no mesmo ritmo diário?",
            "options": [
              "R$ $15.000,00$",
              "R$ $16.666,67$",
              "R$ $18.000,00$",
              "R$ $14.500,00$",
              "R$ $16.000,00$"
            ],
            "correct": 1,
            "explanation": "Valor por dia: $\\frac{10000}{9} \\approx 1111{}11$. Para 15 dias: $15 \\times \\frac{10000}{9} = \\frac{50000}{3} = \\text{R\\$} 16.666,67$."
          },
          {
            "q": "Em uma turma do IFSC com $32$ alunos: $18$ jogam voleibol, $16$ jogam futsal e $6$ jogam ambos. Quantos alunos não praticam nenhum desses dois esportes?",
            "options": [
              "$4$",
              "$6$",
              "$8$",
              "$2$",
              "$5$"
            ],
            "correct": 0,
            "explanation": "Total praticantes: $n(V \\cup F) = 18 + 16 - 6 = 28$. Não praticam nenhum: $32 - 28 = 4$ alunos."
          },
          {
            "q": "A equação $x^2 - 12x + k = 0$ possui raízes reais onde uma é o dobro da outra ($x_1 = 2x_2$). O valor de $k$ é:",
            "options": [
              "$32$",
              "$36$",
              "$24$",
              "$18$",
              "$28$"
            ],
            "correct": 0,
            "explanation": "Soma: $x_1 + x_2 = 3x_2 = 12 \\Rightarrow x_2 = 4$ e $x_1 = 8$. Produto: $k = x_1 \\cdot x_2 = 8 \\times 4 = 32$."
          },
          {
            "q": "Em uma vistoria contra a dengue, encontrou-se uma caixa d'água cilíndrica de $1\\text{ m}$ de raio e $2\\text{ m}$ de altura com água até a metade. O volume de água parada é (adote $\\pi = 3{}14$):",
            "options": [
              "$3.140\\text{ L}$",
              "$6.280\\text{ L}$",
              "$1.570\\text{ L}$",
              "$4.710\\text{ L}$",
              "$2.000\\text{ L}$"
            ],
            "correct": 0,
            "explanation": "Volume total: $V = 3{}14 \\times 1^2 \\times 2 = 6{}28\\text{ m}^3 = 6.280\\text{ L}$. Metade do volume: $\\frac{6280}{2} = 3.140\\text{ Litros}$."
          },
          {
            "q": "O conjunto solução da inequação $(x + 5)(x - 1)(x - 2) > 0$ nos reais é:",
            "options": [
              "$]-5, 1[ \\cup ]2, +\\infty[$",
              "$]-\\infty, -5[ \\cup ]1, 2[$",
              "$]-5, 2[$",
              "$]1, +\\infty[$",
              "$]-\\infty, 1[$"
            ],
            "correct": 0,
            "explanation": "Estudo dos sinais com as raízes $-5, 1, 2$: o produto é positivo nos intervalos $]-5, 1[$ e $]2, +\\infty[$."
          },
          {
            "q": "Uma empresa rodoviária cobra uma taxa fixa de R$ $12,00$ mais R$ $0{}45$ por quilômetro na linha São Miguel do Oeste/Florianópolis ($680\\text{ km}$). A passagem custa:",
            "options": [
              "R$ $318,00$",
              "R$ $306,00$",
              "R$ $320,00$",
              "R$ $295,00$",
              "R$ $325,00$"
            ],
            "correct": 0,
            "explanation": "Preço: $P(680) = 12 + 0{}45 \\times 680 = 12 + 306 = \\text{R\\$} 318,00$."
          }
        ],
        "slug": "prova-ifsc-20222",
        "filename": "prova-ifsc-20222.html",
        "folder": "bloco-5-provas-ifsc",
        "blockId": "5",
        "pdf": "2022_2_EC_INT_PROVA_OFICIAL_impressão.pdf"
      },
      {
        "id": "ifsc-2023-2-matematica",
        "title": "Prova IFSC 2023.2",
        "bncc": "Revisão Geral",
        "summary": "10 questões de Matemática aplicadas no Exame de Classificação 2023.2 do IFSC para Cursos Técnicos Integrados.",
        "detailedTheory": "O Exame 2023.2 aborda distâncias de furos em peças metálicas por coordenadas cartesianas, cálculo de porcentagens em rodízios de pizza com descontos, divisão proporcional de despesas entre amigos, propriedades de números primos e divisibilidade, área de cultivo em estufas agroecológicas, voltas completas na roda gigante Big Wheel, análise de tabelas de desmatamento da Amazônia, bilheteria de cinema com sistema de equações lineares, densidade de massa em cubo perfurado e sequências de áreas de quadrados concêntricos.",
        "keyPoints": [
          "Densidade é calculada pela razão entre massa e volume ($\rho = m/V$).",
          "Para calcular o número de voltas na roda gigante, divida a distância percorrida pelo perímetro da circunferência ($2\\pi r$).",
          "Na bilheteria de cinema, a soma dos ingressos inteiros e meias forma a primeira equação, e o valor financeiro arrecadado forma a segunda."
        ],
        "formula": "\\rho = \\frac{m}{V}, \\quad C = 2\\pi r, \\quad \\begin{cases} x + y = T \\\\ P_1 x + P_2 y = V_T \\end{cases}",
        "solvedExample": {
          "problem": "Densidade do cubo de 6 cm com massa de 1620 g.",
          "solution": "Volume do cubo $= 6^3 = 216\\text{ cm}^3$.\nDensidade $\\rho = \\frac{1620}{216} = 7{}5\\text{ g/cm}^3$."
        },
        "questions": [
          {
            "q": "Uma chapa retangular de $200\\text{ mm} \\times 100\\text{ mm}$ tem 3 furos F1, F2 e F3. O furo F1 está em $(40, 30)$ e F2 em $(160, 30)$. A distância linear entre os centros de F1 e F2 é:",
            "options": [
              "$120\\text{ mm}$",
              "$100\\text{ mm}$",
              "$140\\text{ mm}$",
              "$160\\text{ mm}$",
              "$80\\text{ mm}$"
            ],
            "correct": 0,
            "explanation": "Como ambos possuem a mesma ordenada ($y=30$), a distância horizontal é $160 - 40 = 120\\text{ mm}$."
          },
          {
            "q": "Um rodízio de pizzas que custava R$ $60,00$ ofereceu uma promoção: 'Na compra de 4 rodízios, o 4º tem $50\\%$ de desconto'. O valor médio pago por pessoa no grupo de 4 é:",
            "options": [
              "R$ $52,50$",
              "R$ $50,00$",
              "R$ $45,00$",
              "R$ $55,00$",
              "R$ $48,00$"
            ],
            "correct": 0,
            "explanation": "Total pago: $60 + 60 + 60 + 30 = \\text{R\\$} 210,00$. Média por pessoa: $\\frac{210}{4} = \\text{R\\$} 52,50$."
          },
          {
            "q": "Carlos, Fabiano e Bruna compraram uma barraca. Fabiano pagou $60\\%$, Carlos pagou R$ $150,00$ e Bruna pagou os R$ $90,00$ restantes. Qual o preço total da barraca?",
            "options": [
              "R$ $600,00$",
              "R$ $500,00$",
              "R$ $450,00$",
              "R$ $750,00$",
              "R$ $800,00$"
            ],
            "correct": 0,
            "explanation": "Carlos e Bruna pagaram juntos $150 + 90 = \\text{R\\$} 240,00$, que corresponde a $40\\%$ do total ($100\\% - 60\\%$). Total: $\\frac{240}{0{}40} = \\text{R\\$} 600,00$."
          },
          {
            "q": "Sobre números primos, analise as afirmativas:\\nI. Todo número primo é ímpar.\\nII. Existem infinitos números primos.\\nIII. O número 1 é primo.\\nÉ correto o que se afirma em:",
            "options": [
              "Apenas II",
              "Apenas I e II",
              "Apenas II e III",
              "Apenas I",
              "Todas"
            ],
            "correct": 0,
            "explanation": "I é falsa (o número 2 é primo e par). III é falsa (o número 1 não é primo). Apenas a afirmativa II é verdadeira."
          },
          {
            "q": "Uma estufa agrícola retangular tem $30\\text{ m}$ de comprimento por $12\\text{ m}$ de largura. Se dividirmos essa área em $10$ canteiros iguais, a área de cada canteiro será:",
            "options": [
              "$36\\text{ m}^2$",
              "$30\\text{ m}^2$",
              "$42\\text{ m}^2$",
              "$40\\text{ m}^2$",
              "$32\\text{ m}^2$"
            ],
            "correct": 0,
            "explanation": "Área total da estufa $= 30 \\times 12 = 360\\text{ m}^2$. Cada canteiro: $\\frac{360}{10} = 36\\text{ m}^2$."
          },
          {
            "q": "A roda gigante Big Wheel possui diâmetro de $65\\text{ metros}$ (adote $\\pi = 3{}14$). Em um passeio que realiza $4$ voltas completas, a distância total percorrida por uma cabine é:",
            "options": [
              "$816{}4\\text{ m}$",
              "$408{}2\\text{ m}$",
              "$204{}1\\text{ m}$",
              "$650\\text{ m}$",
              "$500\\text{ m}$"
            ],
            "correct": 0,
            "explanation": "Comprimento de uma volta: $C = \\pi \\cdot D = 3{}14 \\times 65 = 204{}1\\text{ m}$. Em 4 voltas: $4 \\times 204{}1 = 816{}4\\text{ metros}$."
          },
          {
            "q": "Na tabela de desmatamento da Amazônia em 2022, o estado do Pará respondeu por $40\\%$ do total desmatado ($11.500\\text{ km}^2$). A área desmatada no Pará foi de:",
            "options": [
              "$4.600\\text{ km}^2$",
              "$4.200\\text{ km}^2$",
              "$5.000\\text{ km}^2$",
              "$4.800\\text{ km}^2$",
              "$3.800\\text{ km}^2$"
            ],
            "correct": 0,
            "explanation": "$40\\%$ de $11.500 = 0{}40 \\times 11.500 = 4.600\\text{ km}^2$."
          },
          {
            "q": "Uma sala de cinema de $156$ lugares ficou lotada. A entrada inteira custava R$ $36,00$ e a meia R$ $18,00$, totalizando R$ $3.888,00$ arrecadados. Quantas pessoas pagaram meia-entrada?",
            "options": [
              "$96$",
              "$60$",
              "$80$",
              "$76$",
              "$84$"
            ],
            "correct": 0,
            "explanation": "Sistema: $x + y = 156$ e $36x + 18y = 3888$. Multiplicando a 1ª por $-36$: $-18y = -1728 \\Rightarrow y = 96$ (meias-entradas) e $x = 60$ (inteiras)."
          },
          {
            "q": "Um cubo maciço de $6\\text{ cm}$ de aresta tem massa de $1.620\\text{ g}$. A densidade do material desse cubo é:",
            "options": [
              "$7{}5\\text{ g/cm}^3$",
              "$6{}0\\text{ g/cm}^3$",
              "$8{}0\\text{ g/cm}^3$",
              "$5{}5\\text{ g/cm}^3$",
              "$9{}0\\text{ g/cm}^3$"
            ],
            "correct": 0,
            "explanation": "Volume do cubo: $V = 6^3 = 216\\text{ cm}^3$. Densidade: $\\rho = \\frac{1620}{216} = 7{}5\\text{ g/cm}^3$."
          },
          {
            "q": "Fernando desenhou 3 quadrados concêntricos de lados $4\\text{ cm}$, $8\\text{ cm}$ e $12\\text{ cm}$. A área da região compreendida entre o maior e o quadrado médio é:",
            "options": [
              "$80\\text{ cm}^2$",
              "$64\\text{ cm}^2$",
              "$96\\text{ cm}^2$",
              "$144\\text{ cm}^2$",
              "$48\\text{ cm}^2$"
            ],
            "correct": 0,
            "explanation": "Área do quadrado maior: $12^2 = 144\\text{ cm}^2$. Área do quadrado médio: $8^2 = 64\\text{ cm}^2$. Diferença: $144 - 64 = 80\\text{ cm}^2$."
          }
        ],
        "slug": "prova-ifsc-20232",
        "filename": "prova-ifsc-20232.html",
        "folder": "bloco-5-provas-ifsc",
        "blockId": "5",
        "pdf": "2023-2 EC INT PROVA TITULAR.pdf"
      },
      {
        "id": "ifsc-2024-1-matematica",
        "title": "Prova IFSC 2024.1",
        "bncc": "Revisão Geral",
        "summary": "8 questões de Matemática aplicadas no Exame de Classificação 2024.1 do IFSC para Cursos Técnicos Integrados.",
        "detailedTheory": "O Exame 2024.1 traz 8 questões de Matemática cobrando: sobreposição de retângulos e área de interseção, proporcionalidade em campanhas solidárias, aspecto de tela de celular e proporções de imagem, volume e capacidade de copos cilíndricos com submersão, análise estatística e combinatória nos 22 campi do IFSC, conversão de óleo de cozinha em biodiesel com rendimento volumétrico, pontuação em processos seletivos e geometria de hexágonos regulares circunscritos a círculos.",
        "keyPoints": [
          "Na sobreposição de retângulos, a área da união é a soma das áreas menos a interseção.",
          "Para hexágono regular circunscrito ao círculo, o raio do círculo é o apótema do hexágono.",
          "Fique atento à razão de aspecto (largura/altura) em telas e fotos."
        ],
        "formula": "A_{\\text{hex}} = 2\\sqrt{3} r^2, \\quad V = \\pi r^2 h, \\quad A(A \\cup B) = A(A) + A(B) - A(A \\cap B)",
        "solvedExample": {
          "problem": "Retângulos sobrepostos de 10x12 cm e 11x13 cm com interseção de 4x6 cm.",
          "solution": "Área 1 $= 10 \\times 12 = 120\\text{ cm}^2$.\nÁrea 2 $= 11 \\times 13 = 143\\text{ cm}^2$.\nInterseção $= 4 \\times 6 = 24\\text{ cm}^2$.\nÁrea total da união $= 120 + 143 - 24 = 239\\text{ cm}^2$."
        },
        "questions": [
          {
            "q": "Dois retângulos de dimensões $10\\text{ cm} \\times 12\\text{ cm}$ e $11\\text{ cm} \\times 13\\text{ cm}$ foram sobrepostos com uma região comum de área $24\\text{ cm}^2$. A área total coberta pelos dois retângulos é:",
            "options": [
              "$239\\text{ cm}^2$",
              "$263\\text{ cm}^2$",
              "$215\\text{ cm}^2$",
              "$245\\text{ cm}^2$",
              "$220\\text{ cm}^2$"
            ],
            "correct": 0,
            "explanation": "$A_1 = 10 \\times 12 = 120\\text{ cm}^2$. $A_2 = 11 \\times 13 = 143\\text{ cm}^2$. Área total $= 120 + 143 - 24 = 239\\text{ cm}^2$."
          },
          {
            "q": "Um grupo de estudantes arrecadou R$ $1.440,00$ vendendo rifas para castração de animais abandonados. Se cada castração custa R$ $160,00$, quantos animais puderam ser castrados?",
            "options": [
              "$9$",
              "$8$",
              "$10$",
              "$12$",
              "$7$"
            ],
            "correct": 0,
            "explanation": "Animais castrados $= \\frac{1440}{160} = 9$ animais."
          },
          {
            "q": "A tela de um smartphone mede $7\\text{ cm}$ de largura por $14\\text{ cm}$ de altura. Uma foto de proporção $4:3$ é exibida ocupando toda a largura de $7\\text{ cm}$. A altura ocupada pela foto é:",
            "options": [
              "$5{}25\\text{ cm}$",
              "$6{}00\\text{ cm}$",
              "$4{}50\\text{ cm}$",
              "$5{}50\\text{ cm}$",
              "$6{}25\\text{ cm}$"
            ],
            "correct": 0,
            "explanation": "Proporção largura/altura: $\\frac{4}{3} = \\frac{7}{h} \\Rightarrow 4h = 21 \\Rightarrow h = 5{}25\\text{ cm}$."
          },
          {
            "q": "Um copo cilíndrico de raio $5\\text{ cm}$ e altura $20\\text{ cm}$ contém água até a altura de $12\\text{ cm}$. Ao colocar uma pedra no fundo, o nível sobe para $16\\text{ cm}$. Adotando $\\pi = 3{}14$, o volume da pedra é:",
            "options": [
              "$314\\text{ cm}^3$",
              "$628\\text{ cm}^3$",
              "$157\\text{ cm}^3$",
              "$471\\text{ cm}^3$",
              "$250\\text{ cm}^3$"
            ],
            "correct": 0,
            "explanation": "A elevação de altura foi de $\\Delta h = 16 - 12 = 4\\text{ cm}$. Volume da pedra $= \\pi r^2 \\Delta h = 3{}14 \\times 5^2 \\times 4 = 3{}14 \\times 25 \\times 4 = 314\\text{ cm}^3$."
          },
          {
            "q": "O IFSC conta com $22$ câmpus. Em uma comissão de representantes, seleciona-se $1$ coordenador e $1$ vice de câmpus distintos. O total de duplas possíveis é:",
            "options": [
              "$462$",
              "$231$",
              "$484$",
              "$440$",
              "$506$"
            ],
            "correct": 0,
            "explanation": "Arranjo simples: $22 \\times 21 = 462$ possibilidades de duplas ordenadas."
          },
          {
            "q": "Em um processo químico, $10\\text{ litros}$ de óleo residual produzem $9\\text{ litros}$ de biodiesel. Para produzir $450\\text{ litros}$ de biodiesel, o volume necessário de óleo residual é:",
            "options": [
              "$500\\text{ L}$",
              "$450\\text{ L}$",
              "$550\\text{ L}$",
              "$600\\text{ L}$",
              "$480\\text{ L}$"
            ],
            "correct": 0,
            "explanation": "Regra de três: $\\frac{10}{9} = \\frac{x}{450} \\Rightarrow 9x = 4500 \\Rightarrow x = 500\\text{ litros}$."
          },
          {
            "q": "Em um exame classificatório de $24$ questões, um candidato acertou $5$ questões a mais em Matemática do que em Linguagens. Sabendo que ele acertou $19$ questões no total nessas duas áreas, quantas acertou em Matemática?",
            "options": [
              "$12$",
              "$14$",
              "$10$",
              "$13$",
              "$11$"
            ],
            "correct": 0,
            "explanation": "Sistema: $M + L = 19$ e $M - L = 5$. Somando: $2M = 24 \\Rightarrow M = 12$ acertos em Matemática."
          },
          {
            "q": "Uma pizza circular está inscrita em uma caixa hexagonal regular de área $2.295\\text{ cm}^2$. A razão entre o apótema do hexágono e o raio do círculo é:",
            "options": [
              "$1$",
              "$\\sqrt{3}$",
              "$2$",
              "$\\frac{\\sqrt{3}}{2}$",
              "$\\frac{1}{2}$"
            ],
            "correct": 0,
            "explanation": "Por definição geométrica, em qualquer polígono circunscrito a uma circunferência, o apótema do polígono coincide exatamente com o raio do círculo inscrito (razão $= 1$)."
          }
        ],
        "slug": "prova-ifsc-20241",
        "filename": "prova-ifsc-20241.html",
        "folder": "bloco-5-provas-ifsc",
        "blockId": "5",
        "pdf": "2024-1 EC INT PROVA TITULAR.pdf"
      },
      {
        "id": "ifsc-2024-2-matematica",
        "title": "Prova IFSC 2024.2",
        "bncc": "Revisão Geral",
        "summary": "7 questões de Matemática aplicadas no Exame de Classificação 2024.2 do IFSC para Cursos Técnicos Integrados.",
        "detailedTheory": "O Exame 2024.2 apresenta questões práticas e conceituais cobrindo: mínimo múltiplo comum (MMC) em posologia de medicamentos periódicos, propriedades das raízes de equação do 2º grau e dízimas periódicas, geometria de áreas recortadas em azulejo cerâmico (triângulos retângulos e quadriláteros), Teorema de Pitágoras em rotas náuticas perpendiculares, notação científica e conversão de quilates em gramas, educação financeira e regra de orçamento 50-35-15 e análise de gráficos de casos de dengue.",
        "keyPoints": [
          "Para horários simultâneos de medicação, calcule o MMC dos intervalos de horas e some à hora de início.",
          "A área de um quadrilátero recortado pode ser obtida subtraindo os triângulos brancos da área do quadrado total.",
          "Em trajetórias perpendiculares a partir do mesmo ponto, a distância relativa é a hipotenusa ($d^2 = x^2 + y^2$)."
        ],
        "formula": "MMC(t_1, t_2, t_3), \\quad x^2 + y^2 = d^2, \\quad a \\cdot 10^n",
        "solvedExample": {
          "problem": "Dois navios com velocidades iguais e trajetórias perpendiculares estão a $5\\sqrt{2}\\text{ km}$ um do outro.",
          "solution": "Como as velocidades são iguais, as distâncias são $d$ e $d$.\nPor Pitágoras: $d^2 + d^2 = (5\\sqrt{2})^2 \\Rightarrow 2d^2 = 50 \\Rightarrow d^2 = 25 \\Rightarrow d = 5\\text{ km}$ do porto."
        },
        "questions": [
          {
            "q": "Foram prescritos três medicamentos a um paciente: medicamento A de $3\\text{ em } 3\\text{ horas}$, B de $4\\text{ em } 4\\text{ horas}$ e C de $6\\text{ em } 6\\text{ horas}$. Se o paciente tomou os três juntos às $8\\text{ horas da manhã}$, o próximo horário em que tomará os três simultaneamente será às:",
            "options": [
              "$12\\text{ horas}$",
              "$15\\text{ horas}$",
              "$18\\text{ horas}$",
              "$20\\text{ horas}$",
              "$24\\text{ horas}$"
            ],
            "correct": 3,
            "explanation": "Calculamos o $MMC(3, 4, 6) = 12\\text{ horas}$. Somando ao horário inicial: $8\\text{h} + 12\\text{h} = 20\\text{ horas}$."
          },
          {
            "q": "Considere a equação do 2º grau $3x^2 - 7x + 2 = 0$. Sobre as raízes dessa equação, pode-se afirmar que:",
            "options": [
              "A equação não possui raízes reais.",
              "O produto das raízes dessa equação é uma dízima periódica.",
              "A soma das raízes dessa equação é zero.",
              "A diferença das raízes dessa equação é zero.",
              "As raízes dessa equação são números inteiros."
            ],
            "correct": 1,
            "explanation": "Pelas relações de Girard, o produto das raízes é $P = \\frac{c}{a} = \\frac{2}{3} = 0{}6666\\dots$, que é uma dízima periódica simples."
          },
          {
            "q": "Uma peça quadrada de cerâmica de $1\\text{ m}$ de lado ($100\\text{ cm}$) possui uma área cinza no quadrilátero AEFC. O triângulo EBF é isósceles com lados congruentes de $30\\text{ cm}$ e ADC é a metade superior do quadrado. A área cinza pintada é de:",
            "options": [
              "$455\\text{ cm}^2$",
              "$500\\text{ cm}^2$",
              "$2.550\\text{ cm}^2$",
              "$4.100\\text{ cm}^2$",
              "$4.550\\text{ cm}^2$"
            ],
            "correct": 4,
            "explanation": "Área total do quadrado $= 100 \\times 100 = 10.000\\text{ cm}^2$. Área branca $\\Delta ADC = \\frac{100 \\times 100}{2} = 5.000\\text{ cm}^2$. Área branca $\\Delta EBF = \\frac{30 \\times 30}{2} = 450\\text{ cm}^2$. Área cinza $= 10.000 - 5.000 - 450 = 4.550\\text{ cm}^2$."
          },
          {
            "q": "Dois navios partem do Porto de Itajaí no mesmo instante, em direções perpendiculares e com velocidades iguais e constantes. Após $30\\text{ minutos}$, a distância entre eles é de $5\\sqrt{2}\\text{ km}$. A que distância do porto os navios estavam após $30\\text{ minutos}$?",
            "options": [
              "$5\\text{ km}$",
              "$10\\text{ km}$",
              "$15\\text{ km}$",
              "$20\\text{ km}$",
              "$25\\text{ km}$"
            ],
            "correct": 0,
            "explanation": "Sendo $d$ a distância percorrida por cada navio: $d^2 + d^2 = (5\\sqrt{2})^2 \\Rightarrow 2d^2 = 50 \\Rightarrow d^2 = 25 \\Rightarrow d = 5\\text{ km}$."
          },
          {
            "q": "Em 1938 foi encontrado o maior diamante brasileiro com massa bruta de $727\\text{ quilates}$. Sabendo que $1\\text{ quilate} = 0{}2\\text{ grama}$, a massa do diamante em notação científica é:",
            "options": [
              "$1{}454 \\cdot 10^2\\text{ g}$",
              "$1{}626 \\cdot 10^3\\text{ g}$",
              "$2{}452 \\cdot 10^2\\text{ g}$",
              "$3{}637 \\cdot 10^3\\text{ g}$",
              "$7{}271 \\cdot 10^2\\text{ g}$"
            ],
            "correct": 0,
            "explanation": "Massa em gramas: $727 \\times 0{}2 = 145{}4\\text{ g}$. Em notação científica: $1{}454 \\times 10^2\\text{ gramas}$."
          },
          {
            "q": "Na regra de orçamento 50-35-15, $35\\%$ do salário deve ser destinado a gastos pessoais. Um indivíduo gastou exatamente R$ $903,00$ nessa categoria. Seu salário total é:",
            "options": [
              "R$ $387,00$",
              "R$ $1.290,00$",
              "R$ $1.806,00$",
              "R$ $2.580,00$",
              "R$ $3.160,00$"
            ],
            "correct": 3,
            "explanation": "Salário total $S = \\frac{903}{0{}35} = \\text{R\\$} 2.580,00$."
          },
          {
            "q": "No gráfico de casos prováveis de dengue em 2024, as semanas 1 a 4 registraram: $53.354$, $65.860$, $90.532$ e $105.875$ casos, enquanto a semana 3 de 2023 registrou $17.951$ casos. Analise as afirmações:\\nI. O total das 4 primeiras semanas de 2024 ultrapassa 300 mil casos.\\nII. Na Semana 3, os casos de 2024 representam cerca de 500% dos de 2023.\\nAssinale a alternativa correta:",
            "options": [
              "Apenas o item I está correto.",
              "Apenas os itens I e II estão corretos.",
              "Apenas os itens II e III estão corretos.",
              "Apenas os itens I, II e IV estão corretos.",
              "Todos os itens estão corretos."
            ],
            "correct": 3,
            "explanation": "Soma das 4 semanas de 2024 $= 53.354 + 65.860 + 90.532 + 105.875 = 315.621 > 300.000$ (I correto). Na Semana 3: $\\frac{90.532}{17.951} \\approx 5{}04 = 504\\% \\approx 500\\%$ (IV correto)."
          }
        ],
        "slug": "prova-ifsc-20242",
        "filename": "prova-ifsc-20242.html",
        "folder": "bloco-5-provas-ifsc",
        "blockId": "5",
        "pdf": "P-B 2024-2 EC INT PROVA TITULAR.pdf"
      },
      {
        "id": "ifsc-2025-1-matematica",
        "title": "Prova IFSC 2025.1",
        "bncc": "Revisão Geral",
        "summary": "7 questões de Matemática aplicadas no Exame de Classificação 2025.1 do IFSC para Cursos Técnicos Integrados.",
        "detailedTheory": "O Exame 2025.1 aborda mobilidade no contorno viário da Grande Florianópolis (velocidade média e distâncias), estatística de internações infantis com porcentagens, taxas de incidência de dengue por 100 mil habitantes, paridade de preços entre etanol e gasolina (regra dos 70%), equações do 1º grau para massa de carrinho com adubo, cálculo de áreas em plantas baixas arquitetônicas e geometria analítica/coordenadas em campo de futebol.",
        "keyPoints": [
          "Regra dos 70% em carros flex: abastecer com etanol é vantajoso se o preço do etanol for menor que 70% do preço da gasolina.",
          "Para calcular a área de uma planta em formato de L, divida a figura em dois retângulos simples.",
          "Em problemas de balança com tara e conteúdo, monte a equação $M_{\\text{carrinho}} + M_{\\text{adubo}} = M_{\\text{total}}$."
        ],
        "formula": "\\frac{P_{\\text{etanol}}}{P_{\\text{gasolina}}} < 0{}70, \\quad v = \\frac{\\Delta s}{\\Delta t}, \\quad A = A_1 + A_2",
        "solvedExample": {
          "problem": "Paridade de combustível: gasolina a R$ 6,00 e etanol a R$ 4,00.",
          "solution": "Razão: $\\frac{4{}00}{6{}00} = 0{}667 = 66{}7\\%$.\nComo $66{}7\\% < 70\\%$, é financeiramente vantajoso abastecer com etanol."
        },
        "questions": [
          {
            "q": "Ana percorreu os $50\\text{ km}$ do Contorno Viário da Grande Florianópolis a uma velocidade média constante de $80\\text{ km/h}$. O tempo gasto no percurso foi de:",
            "options": [
              "$37\\text{ min } 30\\text{ s}$",
              "$40\\text{ min}$",
              "$35\\text{ min}$",
              "$45\\text{ min}$",
              "$30\\text{ min}$"
            ],
            "correct": 0,
            "explanation": "Tempo: $t = \\frac{50}{80} = 0{}625\\text{ horas} = 0{}625 \\times 60\\text{ min} = 37{}5\\text{ minutos} = 37\\text{ min } 30\\text{ s}$."
          },
          {
            "q": "Em um hospital, de $1.200$ internações pediátricas no ano, $35\\%$ foram de crianças menores de um ano com doenças respiratórias. O total estimado dessas internações é:",
            "options": [
              "$420$",
              "$380$",
              "$450$",
              "$360$",
              "$400$"
            ],
            "correct": 0,
            "explanation": "$35\\%$ de $1.200 = 0{}35 \\times 1200 = 420$ internações."
          },
          {
            "q": "Em Santa Catarina, foram registrados $150.000$ casos de dengue em uma população de $7{}5\\text{ milhões}$ de habitantes. A taxa de incidência por $100\\text{ mil}$ habitantes é:",
            "options": [
              "$2.000$",
              "$1.500$",
              "$2.500$",
              "$3.000$",
              "$1.800$"
            ],
            "correct": 0,
            "explanation": "Taxa por habitante: $\\frac{150.000}{7.500.000} = 0{}02$. Por $100\\text{ mil}$ habitantes: $0{}02 \\times 100.000 = 2.000$ casos por 100 mil habitantes."
          },
          {
            "q": "Sabendo que a gasolina custa R$ $5{}80$ o litro e o etanol R$ $3{}90$ o litro, a razão entre o preço do etanol e da gasolina é aproximadamente:",
            "options": [
              "$67{}2\\%$",
              "$72{}5\\%$",
              "$65{}0\\%$",
              "$70{}0\\%$",
              "$68{}5\\%$"
            ],
            "correct": 0,
            "explanation": "Razão: $\\frac{3{}90}{5{}80} \\approx 0{}6724 = 67{}24\\%$. Como está abaixo de $70\\%$, o etanol é vantajoso."
          },
          {
            "q": "Um carrinho de mão cheio de adubo pesa $24\\text{ kg}$. Após utilizar $\\frac{2}{3}$ do adubo, o carrinho com o restante do adubo pesa $12\\text{ kg}$. A massa do carrinho de mão vazio é:",
            "options": [
              "$6\\text{ kg}$",
              "$4\\text{ kg}$",
              "$5\\text{ kg}$",
              "$8\\text{ kg}$",
              "$7\\text{ kg}$"
            ],
            "correct": 0,
            "explanation": "Os $\\frac{2}{3}$ de adubo utilizados pesam $24 - 12 = 12\\text{ kg}$. Logo, todo o adubo pesa $12 \\div \\frac{2}{3} = 18\\text{ kg}$. A massa do carrinho vazio é $24 - 18 = 6\\text{ kg}$."
          },
          {
            "q": "A planta baixa de um apartamento em formato de 'L' pode ser dividida em dois retângulos: um de $6\\text{ m} \\times 4\\text{ m}$ e outro de $3\\text{ m} \\times 5\\text{ m}$. A área total do apartamento é:",
            "options": [
              "$39\\text{ m}^2$",
              "$42\\text{ m}^2$",
              "$35\\text{ m}^2$",
              "$45\\text{ m}^2$",
              "$36\\text{ m}^2$"
            ],
            "correct": 0,
            "explanation": "Área $= (6 \\times 4) + (3 \\times 5) = 24 + 15 = 39\\text{ m}^2$."
          },
          {
            "q": "Em um campo de futebol de $100\\text{ m} \\times 60\\text{ m}$, o círculo central tem raio de $9\\text{ m}$. A área do campo fora do círculo central é (adote $\\pi = 3{}14$):",
            "options": [
              "$5.745{}66\\text{ m}^2$",
              "$6.000{}00\\text{ m}^2$",
              "$254{}34\\text{ m}^2$",
              "$5.800{}00\\text{ m}^2$",
              "$5.650{}00\\text{ m}^2$"
            ],
            "correct": 0,
            "explanation": "Área do campo $= 100 \\times 60 = 6.000\\text{ m}^2$. Área do círculo central $= 3{}14 \\times 9^2 = 3{}14 \\times 81 = 254{}34\\text{ m}^2$. Área restante $= 6000 - 254{}34 = 5.745{}66\\text{ m}^2$."
          }
        ],
        "slug": "prova-ifsc-20251",
        "filename": "prova-ifsc-20251.html",
        "folder": "bloco-5-provas-ifsc",
        "blockId": "5",
        "pdf": "2025-1 EC INT PROVA TITULAR - IFSC.pdf"
      },
      {
        "id": "ifsc-2025-2-matematica",
        "title": "Prova IFSC 2025.2",
        "bncc": "Revisão Geral",
        "summary": "7 questões de Matemática aplicadas no Exame de Classificação 2025.2 do IFSC para Cursos Técnicos Integrados.",
        "detailedTheory": "O Exame 2025.2 traz questões interdisciplinares e contextualizadas: projeção quadrática de emissões de CO2 com substituição de variáveis, geração de energia solar fotovoltaica em telhados trapezoidais, critérios de divisibilidade (por 2, 3, 4 e 5) aplicados aos dígitos do CPF, análise combinatória e permutação simples de letras para nomes de asteroides descobertos por alunas da UFSC, conversão de fração de dia em horas, minutos e segundos para tempo de tela, impacto de microplásticos/glitter no meio ambiente e economia em dólares/reais com o Índice Big Mac.",
        "keyPoints": [
          "Para converter frações de horas em minutos e segundos, multiplique sucessivamente a parte decimal por 60.",
          "O número de anagramas de $n$ letras distintas é dado pelo fatorial $n!$.",
          "A área do trapézio é $A = \\frac{(B+b)h}{2}$."
        ],
        "formula": "A_{\\text{trapézio}} = \\frac{(B+b)h}{2}, \\quad P_n = n!, \\quad E(x) = ax^2 + bx + c",
        "solvedExample": {
          "problem": "Anagramas com as letras L, I, V, H, R (5 letras distintas).",
          "solution": "Permutação simples de 5 elementos:\n$P_5 = 5! = 5 \\times 4 \\times 3 \\times 2 \\times 1 = 120$ nomes possíveis."
        },
        "questions": [
          {
            "q": "A emissão global de $CO_2$ é estimada pelo modelo $E(x) = 0{}05x^2 + 1{}2x + 25$, onde $x$ representa o número de anos após 2000. Segundo esse modelo, a emissão no ano de 2030 (em bilhões de toneladas) será de:",
            "options": [
              "$88$",
              "$91$",
              "$106$",
              "$110$",
              "$132$"
            ],
            "correct": 2,
            "explanation": "No ano de 2030, temos $x = 2030 - 2000 = 30$. Substituindo: $E(30) = 0{}05(30^2) + 1{}2(30) + 25 = 0{}05(900) + 36 + 25 = 45 + 36 + 25 = 106$ bilhões de toneladas."
          },
          {
            "q": "A face do telhado de uma escola tem o formato de um trapézio isósceles com base maior de $12\\text{ m}$, base menor de $8\\text{ m}$ e altura de $5\\text{ m}$. Sabendo que $80\\%$ dessa área será ocupada por painéis solares e que cada $\\text{m}^2$ de painel gera $1{}2\\text{ kWh}$ por dia, a produção total estimada por dia é de:",
            "options": [
              "$36\\text{ kWh}$",
              "$42\\text{ kWh}$",
              "$48\\text{ kWh}$",
              "$54\\text{ kWh}$",
              "$60\\text{ kWh}$"
            ],
            "correct": 2,
            "explanation": "Área do trapézio: $A = \\frac{(12 + 8) \\times 5}{2} = \\frac{20 \\times 5}{2} = 50\\text{ m}^2$. Área com painéis: $50 \\times 0{}80 = 40\\text{ m}^2$. Produção diária: $40 \\times 1{}2 = 48\\text{ kWh}$."
          },
          {
            "q": "Alice analisou o número formado pelos 11 dígitos do seu CPF ($65.434.212.988$) e fez as seguintes afirmações:\\nI. É um número divisível por 2.\\nII. É um número divisível por 3.\\nIII. É um número divisível por 4.\\nIV. Não é um número divisível por 5.\\nAssinale a alternativa CORRETA:",
            "options": [
              "Todos os itens estão corretos.",
              "Apenas os itens I, III e IV estão corretos.",
              "Apenas os itens I, II e III estão corretos.",
              "Apenas os itens I e II estão corretos.",
              "Apenas os itens I e III estão corretos."
            ],
            "correct": 1,
            "explanation": "I é verdadeiro (termina em 8, número par). II é falso (a soma dos algarismos é $52$, que não é múltiplo de 3). III é verdadeiro (os dois últimos dígitos '88' formam número divisível por 4). IV é verdadeiro (não termina em 0 nem 5). Corretos: I, III e IV."
          },
          {
            "q": "Cientistas decidiram que o nome de um asteroide descoberto será formado por cinco caracteres distintos, composto exclusivamente pelas letras: L, I, V, H e R. O número total de opções de nomes possíveis que as cientistas possuem é:",
            "options": [
              "$5$",
              "$20$",
              "$80$",
              "$120$",
              "$3.125$"
            ],
            "correct": 3,
            "explanation": "Trata-se de uma permutação simples de 5 letras distintas: $P_5 = 5! = 5 \\times 4 \\times 3 \\times 2 \\times 1 = 120$ opções."
          },
          {
            "q": "Uma pesquisa revelou que os brasileiros passam em média $56\\%$ do dia em frente às telas de smartphones e computadores. O tempo médio diário correspondente é:",
            "options": [
              "$08\\text{ horas}$",
              "$13\\text{ horas} 04\\text{ minutos e } 04\\text{ segundos}$",
              "$13\\text{ horas} 26\\text{ minutos e } 24\\text{ segundos}$",
              "$13\\text{ horas} 44\\text{ minutos e } 12\\text{ segundos}$",
              "$16\\text{ horas}$"
            ],
            "correct": 2,
            "explanation": "$56\\%$ de $24\\text{ horas} = 0{}56 \\times 24 = 13{}44\\text{ horas}$. A parte fracionária $0{}44 \\times 60 = 26{}4\\text{ minutos}$. A parte fracionária $0{}4 \\times 60 = 24\\text{ segundos}$. Total: $13\\text{ horas} 26\\text{ minutos e } 24\\text{ segundos}$."
          },
          {
            "q": "No Carnaval de 2025, Florianópolis recebeu $1{}4\\text{ milhão}$ de foliões, dos quais $40\\%$ usaram glitter ($1{}5\\text{ g}$ por pessoa). Sabendo que $1\\text{ g}$ de glitter contém $20\\text{ mil}$ partículas e que a ingestão de $100\\text{ mil}$ partículas pode causar a morte de um animal marinho, quantos animais marinhos de pequeno porte poderiam morrer em decorrência do glitter desse Carnaval?",
            "options": [
              "$150\\text{ mil animais}$",
              "$120\\text{ mil animais}$",
              "$200\\text{ mil animais}$",
              "$100\\text{ mil animais}$",
              "$168\\text{ mil animais}$"
            ],
            "correct": 4,
            "explanation": "Pessoas com glitter: $0{}40 \\times 1.400.000 = 560.000$. Massa de glitter: $560.000 \\times 1{}5 = 840.000\\text{ g}$. Total de partículas: $840.000 \\times 20.000 = 16.800.000.000$. Animais mortos: $\\frac{16.800.000.000}{100.000} = 168.000\\text{ animais}$ ($168\\text{ mil}$)."
          },
          {
            "q": "Um turista argentino comprou 3 Big Macs em Buenos Aires (US$ $6{}95$ cada). No Brasil, o mesmo sanduíche custa US$ $4{}02$. Com a cotação do dólar a R$ $6{}00$, qual o valor em reais (R$) que ele economizaria se fizesse a compra no Brasil?",
            "options": [
              "R$ $8,79$",
              "R$ $17,58$",
              "R$ $17,64$",
              "R$ $52,74$",
              "R$ $101,16$"
            ],
            "correct": 3,
            "explanation": "Diferença por sanduíche: $\\text{US\\$} 6{}95 - 4{}02 = \\text{US\\$} 2{}93$. Para 3 sanduíches: $3 \\times 2{}93 = \\text{US\\$} 8{}79$. Convertendo em reais: $8{}79 \\times 6{}00 = \\text{R\\$} 52,74$."
          }
        ],
        "slug": "prova-ifsc-20252",
        "filename": "prova-ifsc-20252.html",
        "folder": "bloco-5-provas-ifsc",
        "blockId": "5",
        "pdf": "2025-2 EC INT PROVA TITULAR - IFSC.pdf"
      },
      {
        "id": "ifsc-2026-1-matematica",
        "title": "Prova IFSC 2026.1",
        "bncc": "Revisão Geral",
        "summary": "7 questões de Matemática aplicadas no Exame de Classificação 2026.1 do IFSC para Cursos Técnicos Integrados.",
        "detailedTheory": "O Exame 2026.1 aborda análise e leitura de gráficos de colunas de distribuição de tempo (porcentagem de sono, estudo e lazer), proporcionalidade em compras na feira semanal de produtos orgânicos, conversão decimal de tempo (dias em horas, minutos e segundos), estatística da média e desvio de visitantes na Serra do Rio do Rastro, descontos percentuais para pagamento à vista em televisores, área e metragem quadrada nas novas salas do Centro de Referência em Pesca e volumes/consumo de água durante períodos de estiagem.",
        "keyPoints": [
          "Para converter dias com casas decimais em horas, minutos e segundos, multiplique sucessivamente por 24, 60 e 60.",
          "Ao calcular porcentagens em gráficos de colunas, verifique se a soma total das porcentagens atinge 100%.",
          "Em problemas de reservatórios e estiagem, $1\\text{ m}^3 = 1000\\text{ Litros}$."
        ],
        "formula": "t = d \\times 24, \\quad V = A_b \\cdot h, \\quad V_{\\text{desconto}} = V_i \\cdot (1 - d)",
        "solvedExample": {
          "problem": "Conversão de 2,9 dias em horas e minutos.",
          "solution": "$2{}9 \\times 24 = 69{}6\\text{ horas} = 69\\text{h} + (0{}6 \\times 60\\text{min}) = 69\\text{h } 36\\text{min}$."
        },
        "questions": [
          {
            "q": "Um gráfico de colunas indica que um adolescente passa $30\\%$ do dia dormindo e $25\\%$ estudando. Quantas horas diárias ele dedica ao sono e aos estudos juntos?",
            "options": [
              "$13{}2\\text{ horas}$",
              "$12\\text{ horas}$",
              "$14\\text{ horas}$",
              "$11{}5\\text{ horas}$",
              "$15\\text{ horas}$"
            ],
            "correct": 0,
            "explanation": "Porcentagem conjunta: $30\\% + 25\\% = 55\\%$. Horas diárias: $0{}55 \\times 24 = 13{}2\\text{ horas}$ ($13\\text{h } 12\\text{min}$)."
          },
          {
            "q": "Manoela comprou $3\\text{ kg}$ de maçãs e $2\\text{ kg}$ de bananas na feira por R$ $27,00$. Se o quilo da maçã é R$ $1,50$ mais caro que o quilo da banana, qual é o preço do quilo da maçã?",
            "options": [
              "R$ $6,00$",
              "R$ $4,50$",
              "R$ $5,50$",
              "R$ $7,00$",
              "R$ $6,50$"
            ],
            "correct": 0,
            "explanation": "Sendo $b$ o quilo da banana e $m = b + 1{}50$: $3(b + 1{}50) + 2b = 27 \\Rightarrow 5b + 4{}50 = 27 \\Rightarrow 5b = 22{}50 \\Rightarrow b = 4{}50$. Logo, o quilo da maçã é $4{}50 + 1{}50 = \\text{R\\$} 6,00$."
          },
          {
            "q": "Considerando que $1\\text{ dia} = 24\\text{ h}$, $1\\text{ h} = 60\\text{ min}$ e $1\\text{ min} = 60\\text{ s}$, $2{}9\\text{ dias}$ equivalem exatamente a:",
            "options": [
              "$69\\text{ horas e } 36\\text{ minutos}$",
              "$69\\text{ horas e } 54\\text{ minutos}$",
              "$70\\text{ horas}$",
              "$68\\text{ horas e } 45\\text{ minutos}$",
              "$72\\text{ horas e } 18\\text{ minutos}$"
            ],
            "correct": 0,
            "explanation": "$2{}9 \\times 24 = 69{}6\\text{ horas}$. Convertendo a parte decimal: $0{}6 \\times 60 = 36\\text{ minutos}$. Total: $69\\text{ horas e } 36\\text{ minutos}$."
          },
          {
            "q": "Na Serra do Rio do Rastro, o número de visitantes nos 4 finais de semana de julho foi: $12.000$, $15.000$, $18.000$ e $19.000$. A média de visitantes por final de semana foi de:",
            "options": [
              "$16.000$",
              "$15.500$",
              "$16.500$",
              "$17.000$",
              "$15.000$"
            ],
            "correct": 0,
            "explanation": "Média: $\\frac{12000 + 15000 + 18000 + 19000}{4} = \\frac{64000}{4} = 16.000$ visitantes."
          },
          {
            "q": "Uma televisão de R$ $3.200,00$ é oferecida com $15\\%$ de desconto para pagamento à vista. Qual o valor pago à vista?",
            "options": [
              "R$ $2.720,00$",
              "R$ $2.800,00$",
              "R$ $2.680,00$",
              "R$ $2.750,00$",
              "R$ $2.850,00$"
            ],
            "correct": 0,
            "explanation": "Desconto: $0{}15 \\times 3200 = \\text{R\\$} 480,00$. Preço à vista: $3200 - 480 = \\text{R\\$} 2.720,00$."
          },
          {
            "q": "Foram inauguradas $4$ novas salas de aula retangulares no Centro de Pesca do IFSC, cada uma medindo $8\\text{ m} \\times 6\\text{ m}$. A área total construída das quatro salas é:",
            "options": [
              "$192\\text{ m}^2$",
              "$144\\text{ m}^2$",
              "$216\\text{ m}^2$",
              "$240\\text{ m}^2$",
              "$180\\text{ m}^2$"
            ],
            "correct": 0,
            "explanation": "Área de uma sala: $8 \\times 6 = 48\\text{ m}^2$. Total de 4 salas: $4 \\times 48 = 192\\text{ m}^2$."
          },
          {
            "q": "Durante uma estiagem, um reservatório de $45.000\\text{ Litros}$ perde $3\\text{ m}^3$ de água por dia por consumo e evaporação. Quantos dias o reservatório durará sem novas chuvas?",
            "options": [
              "$15\\text{ dias}$",
              "$12\\text{ dias}$",
              "$18\\text{ dias}$",
              "$20\\text{ dias}$",
              "$10\\text{ dias}$"
            ],
            "correct": 0,
            "explanation": "$3\\text{ m}^3 = 3.000\\text{ Litros}$. Duração: $\\frac{45000}{3000} = 15\\text{ dias}$."
          }
        ],
        "slug": "prova-ifsc-20261",
        "filename": "prova-ifsc-20261.html",
        "folder": "bloco-5-provas-ifsc",
        "blockId": "5",
        "pdf": "2026-1 EC INT PROVA - IFSC.pdf"
      },
      {
        "id": "ifsc-2026-2-matematica",
        "title": "Prova IFSC 2026.2",
        "bncc": "Revisão Geral",
        "summary": "7 questões de Matemática aplicadas no Exame de Classificação 2026.2 do IFSC para Cursos Técnicos Integrados.",
        "detailedTheory": "O Exame 2026.2 traz temas atuais e aplicados: uso de redes sociais por jovens e crianças com interpretação de infográficos (ECA Digital), empilhamento de botões cilíndricos e volume geométrico, probabilidade de compra de cartas raras no jogo Pokémon TCG, cálculo de tempo de percurso com paradas, estatística de matrículas escolares no ensino básico com percentuais, análise combinatória e espaço amostral em novos jogos de cartas e cálculo de área desmatada na Mata Atlântica em hectares e campos de futebol.",
        "keyPoints": [
          "Lembre-se: $1\\text{ hectare (ha)} = 10.000\\text{ m}^2$.",
          "A probabilidade de um evento simples é $P(E) = \\frac{\\text{casos favoráveis}}{\\text{casos possíveis}}$.",
          "O volume de um cilindro é $V = \\pi r^2 h$."
        ],
        "formula": "1\\text{ ha} = 10.000\\text{ m}^2, \\quad V = \\pi r^2 h, \\quad P(E) = \\frac{n(E)}{n(\\Omega)}",
        "solvedExample": {
          "problem": "Conversão de 15 hectares para campos de futebol de 7.500 m² cada.",
          "solution": "$15\\text{ ha} = 150.000\\text{ m}^2$.\nNúmero de campos $= \\frac{150.000}{7.500} = 20$ campos de futebol."
        },
        "questions": [
          {
            "q": "Com base nos dados de uma pesquisa sobre uso de redes sociais por jovens de 9 a 17 anos ($85\\%$ usam YouTube, $70\\%$ Instagram e $60\\%$ TikTok), analise as afirmativas:\\nI. O YouTube é a rede social mais utilizada entre as citadas.\\nII. Menos da metade dos entrevistados utiliza o TikTok.\\nÉ correto o que se afirma em:",
            "options": [
              "Apenas I",
              "Apenas II",
              "I e II",
              "Nenhuma",
              "Apenas se tiver dados complementares"
            ],
            "correct": 0,
            "explanation": "I é verdadeiro ($85\\%$ é a maior taxa). II é falso ($60\\% > 50\\%$, logo mais da metade usa TikTok). Correto: Apenas I."
          },
          {
            "q": "Tamara comprou botões cilíndricos de $2\\text{ cm}$ de diâmetro (raio $1\\text{ cm}$) e $0{}2\\text{ cm}$ de espessura. Uma pilha com $50$ desses botões possui altura total e volume de (adote $\\pi = 3{}14$):",
            "options": [
              "$10\\text{ cm}$ de altura e $31{}4\\text{ cm}^3$",
              "$10\\text{ cm}$ de altura e $62{}8\\text{ cm}^3$",
              "$5\\text{ cm}$ de altura e $15{}7\\text{ cm}^3$",
              "$8\\text{ cm}$ de altura e $25{}12\\text{ cm}^3$",
              "$12\\text{ cm}$ de altura e $37{}68\\text{ cm}^3$"
            ],
            "correct": 0,
            "explanation": "Altura da pilha: $50 \\times 0{}2 = 10\\text{ cm}$. Volume da pilha: $V = \\pi r^2 H = 3{}14 \\times 1^2 \\times 10 = 31{}4\\text{ cm}^3$."
          },
          {
            "q": "Em uma partida de Pokémon TCG, o baralho de um jogador tem $40$ cartas restantes, das quais $6$ são do tipo 'Energia Elétrica'. Qual a probabilidade de ele comprar uma carta de Energia Elétrica na próxima rodada?",
            "options": [
              "$15\\%$",
              "$12\\%$",
              "$18\\%$",
              "$20\\%$",
              "$25\\%$"
            ],
            "correct": 0,
            "explanation": "Probabilidade: $P = \\frac{6}{40} = \\frac{3}{20} = 0{}15 = 15\\%$."
          },
          {
            "q": "Um ônibus partiu às $08\\text{h } 15\\text{min}$ e chegou ao destino às $14\\text{h } 30\\text{min}$, fazendo uma parada de $25\\text{ minutos}$ no caminho. O tempo em que o ônibus esteve em movimento foi de:",
            "options": [
              "$5\\text{h } 50\\text{min}$",
              "$6\\text{h } 15\\text{min}$",
              "$6\\text{h } 00\\text{min}$",
              "$5\\text{h } 45\\text{min}$",
              "$6\\text{h } 10\\text{min}$"
            ],
            "correct": 0,
            "explanation": "Tempo total de viagem: das $08\\text{h } 15\\text{min}$ às $14\\text{h } 30\\text{min}$ decorrem $6\\text{h } 15\\text{min}$. Descontando a parada: $6\\text{h } 15\\text{min} - 25\\text{min} = 5\\text{h } 50\\text{min}$."
          },
          {
            "q": "Das $46{}46\\text{ milhões}$ de matrículas escolares na educação básica brasileira, $38{}5\\text{ milhões}$ são na rede pública. O percentual aproximado de estudantes na rede pública é de:",
            "options": [
              "$82{}9\\%$",
              "$80{}5\\%$",
              "$85{}0\\%$",
              "$78{}4\\%$",
              "$88{}2\\%$"
            ],
            "correct": 0,
            "explanation": "Percentual: $\\frac{38{}5}{46{}46} \\approx 0{}82867 = 82{}9\\%$."
          },
          {
            "q": "Ana e Bia jogam um dado padrão de $6$ faces. Ana ganha se o resultado for par maior que 2 ($4$ ou $6$) e Bia ganha se for ímpar ($1, 3$ ou $5$). A razão entre as chances de vitória de Ana e de Bia é:",
            "options": [
              "$\\frac{2}{3}$",
              "$\\frac{1}{2}$",
              "$\\frac{3}{2}$",
              "$1$",
              "$\\frac{1}{3}$"
            ],
            "correct": 0,
            "explanation": "Ana tem 2 resultados favoráveis ($4, 6$), Bia tem 3 ($1, 3, 5$). A razão entre as chances de Ana e Bia é $\\frac{2}{3}$."
          },
          {
            "q": "Uma área desmatada de $60\\text{ hectares}$ equivale a quantos campos de futebol oficiais de $100\\text{ m} \\times 75\\text{ m}$ ($7.500\\text{ m}^2$)? Sabendo que $1\\text{ ha} = 10.000\\text{ m}^2$.",
            "options": [
              "$80\\text{ campos}$",
              "$60\\text{ campos}$",
              "$75\\text{ campos}$",
              "$90\\text{ campos}$",
              "$100\\text{ campos}$"
            ],
            "correct": 0,
            "explanation": "Área total em $\\text{m}^2$: $60 \\times 10.000 = 600.000\\text{ m}^2$. Número de campos: $\\frac{600.000}{7.500} = 80\\text{ campos de futebol}$."
          }
        ],
        "slug": "prova-ifsc-20262",
        "filename": "prova-ifsc-20262.html",
        "folder": "bloco-5-provas-ifsc",
        "blockId": "5",
        "pdf": "2026-2 EC INT PROVA TITULAR - IFSC.pdf"
      }
    ]
  }
};

if (typeof module !== "undefined" && module.exports) {
  module.exports = mathData;
}
