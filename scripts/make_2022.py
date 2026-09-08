import json

EXAM_2022_1_MANHA = {
    "id": "ifsp-2022-1-manha",
    "title": "Prova IFSP 2022.1 - Manhã",
    "bncc": "Revisão Geral",
    "summary": "15 questões de Matemática aplicadas no Processo Seletivo IFSP 2022.1 (Turno Manhã) para os Cursos Técnicos Integrados.",
    "detailedTheory": "A Prova do Turno Manhã do Processo Seletivo IFSP 2022.1 contemplou geometria plana e polígonos no mapa de São Paulo, sistemas de equações de 1º grau aplicados a despesas em padaria (pães de queijo e cafés com leite), equação do 2º grau e otimização de cercamento em jardins retangulares com muro, vistas ortogonais e projeções de blocos cúbicos tridimensionais, conversão de unidades de comprimento no Sistema Internacional, volumetria e diluição química em aquarismo com regra de três composta, razão e proporção na crise hídrica de reservatórios e vazão, estatística de distanciamento social e controle de capacidade na pandemia de COVID-19, modelagem matemática com taxas de transmissão e gráficos exponenciais, custo por quilômetro rodado e paridade econômica de combustíveis (gasolina vs. etanol), notação científica em descobertas biológicas e microbiologia, teoria das probabilidades no jogo de 'Par ou Ímpar', desafios algébricos com equações exponenciais e radicais, divisão inversamente proporcional de tarefas entre pesquisadores de idades distintas para terraformação em Marte, e proporcionalidade e porcentagem na distribuição de lotes de vacinas.",
    "keyPoints": [
        "Em problemas de divisão inversamente proporcional a valores $x_1, x_2, \\dots$, divide-se o total proporcionalmente aos inversos $\\frac{1}{x_1}, \\frac{1}{x_2}, \\dots$",
        "Para que o custo por quilômetro rodado seja idêntico entre dois combustíveis: $\\frac{P_{\\text{etanol}}}{\\text{Rendimento}_{\\text{etanol}}} = \\frac{P_{\\text{gasolina}}}{\\text{Rendimento}_{\\text{gasolina}}}$.",
        "No jogo de par ou ímpar com dois jogadores lançando de 0 a 5 dedos, o total de resultados possíveis é $6 \\times 6 = 36$.",
        "A área de um retângulo de lados $x$ e $y$ com perímetro fixado por cerca de 3 lados é modelada por uma equação quadrática."
    ],
    "formula": "Custo/km = \\frac{P_{\\text{comb}}}{Rend}, \\quad A(x) = x(L - 2x), \\quad P = \\frac{n(E)}{n(\\Omega)}, \\quad k = \\frac{T}{\\sum \\frac{1}{x_i}}",
    "solvedExample": {
        "problem": "Um carro percorre $12\\text{ km/L}$ com gasolina (a R$ 6,00/L) e $8{,}8\\text{ km/L}$ com etanol. Qual deve ser o preço do litro de etanol para que o custo por quilômetro seja o mesmo?",
        "solution": "Igualando o custo por km:<br>$$\\frac{P_e}{8{,}8} = \\frac{6{,}00}{12} = 0{,}50\\text{ R\\$/km} \\implies P_e = 0{,}50 \\times 8{,}8 = \\text{R\\$ } 4{,}40.$$"
    },
    "slug": "prova-ifsp-20221-manha",
    "filename": "prova-ifsp-20221-manha.html",
    "folder": "bloco-7-provas-ifsp",
    "blockId": 7,
    "pdf": "IFSP_prova_2022_1_manha.pdf",
    "questions": [
        {
            "q": "Um mapa estilizado do estado de São Paulo foi construído com polígonos geométricos. Entre as figuras identificadas, havia triângulos, quadriláteros e pentágonos. Sabendo que a soma dos ângulos internos de um polígono convexo é dada por $S_i = (n - 2) \\cdot 180^\\circ$, qual é a soma dos ângulos internos de um pentágono?",
            "options": ["$360^\\circ$", "$540^\\circ$", "$720^\\circ$", "$900^\\circ$"],
            "correct": 1,
            "explanation": "Para um pentágono, temos $n = 5$ lados.<br>Aplicando a fórmula:<br>$$S_i = (5 - 2) \\times 180^\\circ = 3 \\times 180^\\circ = 540^\\circ.$$Portanto, a alternativa correta é a <strong>Letra B</strong>."
        },
        {
            "q": "Uma pessoa costuma tomar café da manhã em uma padaria. Na semana passada, ela gastou R$ 13,00 na compra de 3 pães de queijo e 2 cafés com leite. Sabendo que cada café com leite custa R$ 3,50, qual é o valor individual de cada pão de queijo?",
            "options": ["R$ 2,00", "R$ 3,00", "R$ 4,14", "R$ 4,20"],
            "correct": 0,
            "explanation": "Seja $p$ o valor de um pão de queijo e $c$ o valor de um café com leite ($c = 3{,}50$):<br>$$3p + 2c = 13{,}00$$<br>Substituindo $c = 3{,}50$:<br>$$3p + 2(3{,}50) = 13{,}00 \\implies 3p + 7{,}00 = 13{,}00$$<br>$$3p = 13{,}00 - 7{,}00 = 6{,}00 \\implies p = \\frac{6{,}00}{3} = \\text{R\\$ } 2{,}00.$$Portanto, a alternativa correta é a <strong>Letra A</strong>."
        },
        {
            "q": "Deseja-se construir um jardim retangular encostado em um muro reto existente no quintal, de modo que o muro sirva como um dos lados maiores do retângulo. O proprietário dispõe de exatamente $20\\text{ metros}$ de cerca para cercar os outros três lados do jardim. Se a área desejada para o jardim é de $50\\text{ m}^2$, qual é o comprimento do lado perpendicular ao muro?",
            "options": ["$5\\text{ m}$", "$10\\text{ m}$", "$15\\text{ m}$", "$20\\text{ m}$"],
            "correct": 0,
            "explanation": "Sejam $x$ a medida de cada um dos dois lados perpendiculares ao muro e $y$ o lado paralelo ao muro.<br>O comprimento da cerca é:<br>$$2x + y = 20 \\implies y = 20 - 2x$$<br>A área do retângulo é:<br>$$A = x \\cdot y = x(20 - 2x) = 20x - 2x^2$$<br>Igualando à área desejada de $50\\text{ m}^2$:<br>$$20x - 2x^2 = 50 \\implies 2x^2 - 20x + 50 = 0$$<br>Dividindo por 2:<br>$$x^2 - 10x + 25 = 0 \\implies (x - 5)^2 = 0 \\implies x = 5\\text{ metros}.$$Portanto, a alternativa correta é a <strong>Letra A</strong>."
        },
        {
            "q": "Um bloco maciço de madeira tem formato cúbico. Ao projetar suas três vistas ortogonais (frontal, lateral e superior), observa-se que as três vistas são exatamente:",
            "options": [
                "quadrados congruentes entre si.",
                "retângulos não quadrados.",
                "triângulos isósceles.",
                "trapézios retângulos."
            ],
            "correct": 0,
            "explanation": "Em um cubo perfeito, todas as 6 faces são quadrados congruentes. Consequentemente, qualquer projeção ortogonal paralela às suas faces (vista frontal, vista lateral e vista superior) resulta em quadrados congruentes de mesmo lado.<br>Portanto, a alternativa correta é a <strong>Letra A</strong>."
        },
        {
            "q": "No Sistema Internacional de Unidades (SI), a unidade padrão de comprimento é o metro ($m$). Ao converter a medida de $3{,}45\\text{ km}$ para centímetros, obtém-se:",
            "options": [
                "$345\\text{ cm}$",
                "$3.450\\text{ cm}$",
                "$34.500\\text{ cm}$",
                "$345.000\\text{ cm}$"
            ],
            "correct": 3,
            "explanation": "Sabemos que $1\\text{ km} = 1.000\\text{ m}$ e $1\\text{ m} = 100\\text{ cm}$, logo $1\\text{ km} = 100.000\\text{ cm}$.<br>Multiplicando:<br>$$3{,}45 \\times 100.000 = 345.000\\text{ cm}.$$Portanto, a alternativa correta é a <strong>Letra D</strong>."
        },
        {
            "q": "Um aquário com formato de paralelepípedo tem dimensões internas de $80\\text{ cm}$ de comprimento, $50\\text{ cm}$ de largura e $60\\text{ cm}$ de altura. Sabendo que $1.000\\text{ cm}^3 = 1\\text{ litro}$ e que as instruções de um produto recomendam aplicar 1 gota para cada 4 litros de água, quantas gotas desse produto devem ser utilizadas quando o aquário estiver totalmente cheio?",
            "options": ["24", "60", "96", "150"],
            "correct": 1,
            "explanation": "1. Calculamos o volume do aquário em centímetros cúbicos:<br>$$V = 80 \\times 50 \\times 60 = 240.000\\text{ cm}^3$$<br>2. Convertendo para litros ($1\\text{ L} = 1.000\\text{ cm}^3$):<br>$$\\text{Capacidade} = \\frac{240.000}{1.000} = 240\\text{ litros}$$<br>3. Como a proporção é de 1 gota a cada 4 litros:<br>$$\\text{Gotas} = \\frac{240}{4} = 60\\text{ gotas}.$$Portanto, a alternativa correta é a <strong>Letra B</strong>."
        },
        {
            "q": "Durante um período de estiagem, um reservatório com capacidade máxima de $120.000\\text{ m}^3$ estava operando com apenas $25\\%$ de sua capacidade. Para atingir o nível de alerta de $60\\%$, quantos metros cúbicos de água precisam ser adicionados ao reservatório?",
            "options": [
                "$30.000\\text{ m}^3$",
                "$42.000\\text{ m}^3$",
                "$72.000\\text{ m}^3$",
                "$102.000\\text{ m}^3$"
            ],
            "correct": 1,
            "explanation": "A porcentagem de água que precisa ser adicionada é:<br>$$60\\% - 25\\% = 35\\%$$<br>Calculando $35\\%$ da capacidade total de $120.000\\text{ m}^3$:<br>$$\\text{Volume} = 0{,}35 \\times 120.000 = 42.000\\text{ m}^3.$$Portanto, a alternativa correta é a <strong>Letra B</strong>."
        },
        {
            "q": "Um auditório tem capacidade normal para 400 pessoas. Para cumprir os protocolos de distanciamento, foi estabelecido que a ocupação máxima permitida seria de $40\\%$ da capacidade total, mantendo um espaçamento de $1{,}5\\text{ m}$ entre os assentos ocupados. Quantas pessoas puderam comparecer simultaneamente ao auditório?",
            "options": ["120", "160", "200", "240"],
            "correct": 1,
            "explanation": "Calculamos $40\\%$ de 400 lugares:<br>$$\\text{Ocupação} = 0{,}40 \\times 400 = 160\\text{ pessoas}.$$Portanto, a alternativa correta é a <strong>Letra B</strong>."
        },
        {
            "q": "A taxa de transmissão $R_t$ de uma epidemia indica a quantas pessoas em média cada indivíduo infectado transmite a doença. Se em determinada semana $R_t = 1{,}2$ e havia $5.000$ pessoas ativamente infectadas, quantas pessoas deverão ser infectadas no ciclo subsequente?",
            "options": ["$5.500$", "$6.000$", "$6.500$", "$7.000$"],
            "correct": 1,
            "explanation": "Multiplicamos o número de indivíduos infectados pela taxa de transmissão $R_t$:<br>$$\\text{Novos Casos} = 5.000 \\times 1{,}2 = 6.000\\text{ pessoas}.$$Portanto, a alternativa correta é a <strong>Letra B</strong>."
        },
        {
            "q": "Um laboratório analisou o consumo de um carro flex. Abastecido com gasolina, o veículo percorreu $396\\text{ km}$ consumindo $33\\text{ litros}$ (rendimento de $12\\text{ km/L}$). Com etanol, percorreu $352\\text{ km}$ com $40\\text{ litros}$ (rendimento de $8{,}8\\text{ km/L}$). Considerando o preço de R$ 6,00 para o litro de gasolina, qual deve ser o preço do litro de etanol para que o custo por quilômetro rodado seja exatamente o mesmo?",
            "options": ["R$ 4,35", "R$ 4,40", "R$ 4,50", "R$ 4,80"],
            "correct": 1,
            "explanation": "1. Calculamos o custo por quilômetro rodado com gasolina:<br>$$\\text{Custo}_{\\text{gasolina}} = \\frac{\\text{Preço por litro}}{\\text{Rendimento}} = \\frac{6{,}00\\text{ R\\$}}{12\\text{ km/L}} = 0{,}50\\text{ R\\$/km}$$<br>2. Para que o custo por km com etanol seja igual a $0{,}50\\text{ R\\$/km}$:<br>$$\\frac{P_{\\text{etanol}}}{8{,}8\\text{ km/L}} = 0{,}50 \\implies P_{\\text{etanol}} = 0{,}50 \\times 8{,}8 = \\text{R\\$ } 4{,}40.$$Portanto, a alternativa correta é a <strong>Letra B</strong>."
        },
        {
            "q": "Alexander Fleming descobriu a penicilina observando culturas da bactéria Staphylococcus aureus, cujo diâmetro médio é de cerca de $1 \\times 10^{-6}\\text{ metros}$. Se uma colônia alinhada em linha reta tem comprimento total de $2\\text{ milímetros}$ ($2 \\times 10^{-3}\\text{ m}$), quantas bactérias compõem aproximadamente essa linha?",
            "options": ["200", "2.000", "20.000", "200.000"],
            "correct": 1,
            "explanation": "Dividimos o comprimento total pelo diâmetro de uma única bactéria:<br>$$N = \\frac{2 \\times 10^{-3}\\text{ m}}{1 \\times 10^{-6}\\text{ m}} = 2 \\times 10^{-3 - (-6)} = 2 \\times 10^3 = 2.000\\text{ bactérias}.$$Portanto, a alternativa correta é a <strong>Letra B</strong>."
        },
        {
            "q": "No jogo de 'Par ou Ímpar' disputado por duas pessoas, cada jogador escolhe simultaneamente um número inteiro de dedos de 0 a 5. Sabendo que todas as 36 combinações de dedos são equiprováveis, qual é a probabilidade de a soma resultar em um número par?",
            "options": ["$\\frac{1}{3}$", "$\\frac{1}{2}$", "$\\frac{5}{12}$", "$\\frac{7}{12}$"],
            "correct": 1,
            "explanation": "Os números de dedos possíveis para cada jogador são $\\{0, 1, 2, 3, 4, 5\\}$ (3 pares: 0, 2, 4; e 3 ímpares: 1, 3, 5).<br>A soma é par em dois casos:<br>1. Par + Par: $3 \\times 3 = 9$ possibilidades.<br>2. Ímpar + Ímpar: $3 \\times 3 = 9$ possibilidades.<br>Total de somas pares $= 9 + 9 = 18$ casos favoráveis.<br>A probabilidade é:<br>$$P = \\frac{18}{36} = \\frac{1}{2} = 50\\%.$$Portanto, a alternativa correta é a <strong>Letra B</strong>."
        },
        {
            "q": "Seja a equação exponencial $2^{x+2} + 2^x = 20$. O valor real de $x$ que satisfaz essa equação é:",
            "options": ["1", "2", "3", "4"],
            "correct": 1,
            "explanation": "Fatorando a expressão utilizando propriedades de potências:<br>$$2^{x+2} = 2^x \\cdot 2^2 = 4 \\cdot 2^x$$<br>Substituindo na equação:<br>$$4 \\cdot 2^x + 2^x = 20 \\implies 5 \\cdot 2^x = 20$$<br>Dividindo ambos os lados por 5:<br>$$2^x = \\frac{20}{5} = 4$$<br>Como $4 = 2^2$, temos $x = 2$.<br>Portanto, a alternativa correta é a <strong>Letra B</strong>."
        },
        {
            "q": "Quatro pesquisadores com idades de 20, 30, 40 e 60 anos devem realizar um total de 120 tarefas diárias. A quantidade de tarefas que cada pesquisador fará é inversamente proporcional à sua respectiva idade. Qual é a soma das tarefas diárias que os dois pesquisadores mais velhos (40 e 60 anos) terão que realizar?",
            "options": ["24", "32", "40", "48"],
            "correct": 2,
            "explanation": "A divisão é inversamente proporcional a 20, 30, 40 e 60. Tomamos os inversos:<br>$$\\frac{1}{20}, \\, \\frac{1}{30}, \\, \\frac{1}{40}, \\, \\frac{1}{60}$$<br>Multiplicando todos os inversos pelo MMC(20, 30, 40, 60) = 120 para obter coeficientes inteiros:<br>- Pesquisador de 20 anos: $\\frac{120}{20} = 6k$<br>- Pesquisador de 30 anos: $\\frac{120}{30} = 4k$<br>- Pesquisador de 40 anos: $\\frac{120}{40} = 3k$<br>- Pesquisador de 60 anos: $\\frac{120}{60} = 2k$<br><br>Somando as partes:<br>$$6k + 4k + 3k + 2k = 15k = 120 \\implies k = \\frac{120}{15} = 8$$<br>As tarefas dos dois mais velhos são:<br>- 40 anos: $3k = 3 \\times 8 = 24$ tarefas<br>- 60 anos: $2k = 2 \\times 8 = 16$ tarefas<br>Soma $= 24 + 16 = 40\\text{ tarefas}$.<br>Portanto, a alternativa correta é a <strong>Letra C</strong>."
        },
        {
            "q": "O Ministério da Saúde recebeu um lote de 2 milhões de doses de vacinas para distribuição entre estados proporcionalmente à população de grupos prioritários. Se o estado de São Paulo tem direito a $22\\%$ desse lote, quantas doses foram destinadas a São Paulo?",
            "options": ["$340.000$", "$440.000$", "$540.000$", "$640.000$"],
            "correct": 1,
            "explanation": "Calculando $22\\%$ de 2.000.000 de doses:<br>$$\\text{Doses} = 0{,}22 \\times 2.000.000 = 440.000\\text{ doses}.$$Portanto, a alternativa correta é a <strong>Letra B</strong>."
        }
    ]
}

EXAM_2022_1_TARDE = {
    "id": "ifsp-2022-1-tarde",
    "title": "Prova IFSP 2022.1 - Tarde",
    "bncc": "Revisão Geral",
    "summary": "15 questões de Matemática aplicadas no Processo Seletivo IFSP 2022.1 (Turno Tarde) para os Cursos Técnicos Integrados.",
    "detailedTheory": "A Prova do Turno Tarde do Processo Seletivo IFSP 2022.1 abordou representação de números muito grandes e potências em supercomputadores de ficção científica, interpretação de gráficos e porcentagens do quadro de medalhas das Paralimpíadas de Tóquio, equações do 2º grau e determinação de raízes por Soma e Produto / fórmula de Bhaskara, geometria plana e propriedades dos ângulos em dobraduras de papel (origami), progressão aritmética e funções de desconto progressivo por quantidade no comércio, análise de dados e impacto econômico na indústria alimentícia durante a pandemia, análise combinatória na formação de placas de veículos no modelo Mercosul (três letras, um algarismo, uma letra e dois algarismos), probabilidade clássica com sorteios entre os estados da federação brasileira, raciocínio espacial e propriedades numéricas das faces opostas de dados cúbicos, geometria com hexágonos regulares em jogos ('Colmeia de Açúcar'), semelhança e polígonos estrelados em decorações temáticas de Halloween, cálculo de áreas e perímetros em projetos de ampliação de piscinas e solários, notação científica e conversão de unidades astronômicas (anos-luz e trilhões de quilômetros para Proxima Centauri), porcentagem e cálculo de consumo na crise hídrica, e estatística descritiva com análise de mensagens em aplicativos de comunicação.",
    "keyPoints": [
        "A nova placa Mercosul para automóveis segue o padrão LLL-NLNN (onde L é letra e N é algarismo). Pelo princípio multiplicativo: $26^4 \\times 10^3$.",
        "As raízes de uma equação do 2º grau $ax^2 + bx + c = 0$ satisfazem $S = -\\frac{b}{a}$ e $P = \\frac{c}{a}$.",
        "A soma das faces opostas em qualquer dado comum de 6 faces é sempre igual a 7.",
        "Um hexágono regular de lado $L$ é composto por 6 triângulos equiláteros congruentes de lado $L$, com área total $A = 6 \\times \\frac{L^2 \\sqrt{3}}{4}$."
    ],
    "formula": "S = -\\frac{b}{a}, \\quad P = \\frac{c}{a}, \\quad A_{\\text{hex}} = \\frac{3L^2\\sqrt{3}}{2}, \\quad N_{\\text{placas}} = 26^4 \\times 10^3",
    "solvedExample": {
        "problem": "Quantas combinações distintas de placas de veículos podem ser formadas no padrão Mercosul (3 letras, 1 algarismo, 1 letra, 2 algarismos)?",
        "solution": "Aplicando o princípio multiplicativo com 26 letras e 10 algarismos:<br>$$N = 26 \\times 26 \\times 26 \\times 10 \\times 26 \\times 10 \\times 10 = 26^4 \\times 10^3 = 456.976 \\times 1.000 = 456.976.000\\text{ placas}.$$"
    },
    "slug": "prova-ifsp-20221-tarde",
    "filename": "prova-ifsp-20221-tarde.html",
    "folder": "bloco-7-provas-ifsp",
    "blockId": 7,
    "pdf": "IFSP_prova_2022_1_tarde.pdf",
    "questions": [
        {
            "q": "No livro 'O Guia do Mochileiro das Galáxias', o supercomputador Pensador Profundo levou 7,5 milhões de anos para calcular a resposta para a Vida, o Universo e Tudo Mais. Em notação científica, esse período de tempo expresso em anos é:",
            "options": ["$7{,}5 \\times 10^5$", "$7{,}5 \\times 10^6$", "$75 \\times 10^5$", "$0{,}75 \\times 10^7$"],
            "correct": 1,
            "explanation": "Sabendo que 1 milhão corresponde a $10^6$:<br>$$7{,}5\\text{ milhões} = 7{,}5 \\times 10^6\\text{ anos}.$$Portanto, a alternativa correta é a <strong>Letra B</strong>."
        },
        {
            "q": "Nas Paralimpíadas de Tóquio 2020 (realizadas em 2021), o Brasil conquistou um total de 72 medalhas, sendo 22 de ouro, 20 de prata e 30 de bronze. Qual é a porcentagem aproximada de medalhas de ouro em relação ao total de medalhas conquistadas pelo Brasil?",
            "options": ["$25{,}5\\%$", "$28{,}2\\%$", "$30{,}6\\%$", "$35{,}0\\%$"],
            "correct": 2,
            "explanation": "Calculamos a razão entre as medalhas de ouro e o total:<br>$$\\text{Porcentagem} = \\frac{22}{72} \\approx 0{,}30555\\dots = 30{,}6\\%.$$Portanto, a alternativa correta é a <strong>Letra C</strong>."
        },
        {
            "q": "Uma professora resolveu na lousa a equação do 2º grau $x^2 - 7x + 10 = 0$. As raízes reais que satisfazem essa equação são:",
            "options": [
                "$x_1 = 2$ e $x_2 = 5$",
                "$x_1 = -2$ e $x_2 = -5$",
                "$x_1 = 1$ e $x_2 = 10$",
                "$x_1 = -1$ e $x_2 = -10$"
            ],
            "correct": 0,
            "explanation": "Por Soma e Produto:<br>$$S = x_1 + x_2 = -\\frac{-7}{1} = 7$$<br>$$P = x_1 \\cdot x_2 = \\frac{10}{1} = 10$$<br>Os dois números cuja soma é 7 e cujo produto é 10 são $2$ e $5$.<br>Portanto, a alternativa correta é a <strong>Letra A</strong>."
        },
        {
            "q": "Na arte tradicional do origami, uma folha quadrada de papel de lado $L = 10\\text{ cm}$ é dobrada ao meio ao longo de sua diagonal. Qual é o comprimento dessa dobra diagonal?",
            "options": ["$10\\text{ cm}$", "$10\\sqrt{2}\\text{ cm}$", "$15\\text{ cm}$", "$20\\text{ cm}$"],
            "correct": 1,
            "explanation": "A dobra ao longo da diagonal de um quadrado de lado $L$ forma um triângulo retângulo isósceles de catetos $L$.<br>Pelo Teorema de Pitágoras:<br>$$d = L\\sqrt{2} = 10\\sqrt{2}\\text{ cm}.$$Portanto, a alternativa correta é a <strong>Letra B</strong>."
        },
        {
            "q": "Em uma promoção de supermercado, o preço unitário de um pacote de biscoitos é R$ 4,00 para até 5 pacotes. A partir do 6º pacote, cada pacote adicional tem um desconto de $25\\%$ sobre o valor unitário. Quanto um cliente pagará ao comprar 9 pacotes?",
            "options": ["R$ 28,00", "R$ 30,00", "R$ 32,00", "R$ 36,00"],
            "correct": 2,
            "explanation": "1. Os primeiros 5 pacotes custam R$ 4,00 cada:<br>$$5 \\times 4{,}00 = \\text{R\\$ } 20{,}00$$<br>2. Os $9 - 5 = 4$ pacotes adicionais têm $25\\%$ de desconto: $4{,}00 - 0{,}25 \\times 4{,}00 = 4{,}00 - 1{,}00 = \\text{R\\$ } 3{,}00$ cada.<br>$$4 \\times 3{,}00 = \\text{R\\$ } 12{,}00$$<br>3. Custo total:<br>$$20{,}00 + 12{,}00 = \\text{R\\$ } 32{,}00.$$Portanto, a alternativa correta é a <strong>Letra C</strong>."
        },
        {
            "q": "Uma padaria teve sua produção diária reduzida de 800 pães para 600 pães durante certo período. A redução percentual na produção foi de:",
            "options": ["$20\\%$", "$25\\%$", "$30\\%$", "$33{,}3\\%$"],
            "correct": 1,
            "explanation": "A redução absoluta na produção foi de:<br>$$\\Delta = 800 - 600 = 200\\text{ pães}$$<br>Em relação à produção inicial de 800 pães:<br>$$\\text{Taxa} = \\frac{200}{800} = \\frac{1}{4} = 0{,}25 = 25\\%.$$Portanto, a alternativa correta é a <strong>Letra B</strong>."
        },
        {
            "q": "O padrão da placa de veículos Mercosul para automóveis no Brasil é composto por quatro letras e três algarismos dispostos na sequência LLL-NLNN (onde L representa uma letra do alfabeto de 26 letras e N representa um algarismo de 0 a 9). Quantas placas distintas podem ser geradas nesse modelo?",
            "options": [
                "$26^3 \\times 10^4$",
                "$26^4 \\times 10^3$",
                "$26^7$",
                "$10^7$"
            ],
            "correct": 1,
            "explanation": "Temos 4 posições reservadas para letras e 3 posições reservadas para algarismos.<br>Pelo princípio fundamental da contagem, com repetição permitida:<br>- Letras: $26 \\times 26 \\times 26 \\times 26 = 26^4$<br>- Algarismos: $10 \\times 10 \\times 10 = 10^3$<br>Total de combinações $= 26^4 \\times 10^3 = 456.976.000$ placas.<br>Portanto, a alternativa correta é a <strong>Letra B</strong>."
        },
        {
            "q": "O Brasil é composto por 26 estados e 1 Distrito Federal, totalizando 27 unidades federativas. Sabe-se que a região Nordeste possui 9 estados. Sorteando-se ao acaso uma dessas 27 unidades federativas, qual é a probabilidade de ela pertencer à região Nordeste?",
            "options": ["$\\frac{1}{4}$", "$\\frac{1}{3}$", "$\\frac{9}{26}$", "$\\frac{1}{2}$"],
            "correct": 1,
            "explanation": "O espaço amostral tem $n(\\Omega) = 27$ unidades federativas.<br>O evento favorável consiste nos 9 estados da região Nordeste ($n(E) = 9$).<br>A probabilidade é:<br>$$P = \\frac{9}{27} = \\frac{1}{3}.$$Portanto, a alternativa correta é a <strong>Letra B</strong>."
        },
        {
            "q": "Em dados cúbicos convencionais, as faces opostas somam 7. Se um dado é lançado e a face voltada para cima mostra o número 2, qual é o número que está voltado para a face inferior (em contato com a mesa)?",
            "options": ["3", "4", "5", "6"],
            "correct": 2,
            "explanation": "Como a soma de faces opostas é sempre 7:<br>$$\\text{Face inferior} = 7 - 2 = 5.$$Portanto, a alternativa correta é a <strong>Letra C</strong>."
        },
        {
            "q": "Três amigos fizeram biscoitos em formato de hexágonos regulares de lado $L = 4\\text{ cm}$ para o jogo 'Colmeia de Açúcar'. Sabendo que um hexágono regular é formado por 6 triângulos equiláteros, qual é a área de cada biscoito? (Adote $\\sqrt{3} \\approx 1{,}7$).",
            "options": ["$24{,}4\\text{ cm}^2$", "$36{,}0\\text{ cm}^2$", "$40{,}8\\text{ cm}^2$", "$48{,}0\\text{ cm}^2$"],
            "correct": 2,
            "explanation": "A área de um triângulo equilátero de lado $L = 4\\text{ cm}$ é:<br>$$A_{\\text{tri}} = \\frac{L^2 \\sqrt{3}}{4} = \\frac{16 \\sqrt{3}}{4} = 4\\sqrt{3}\\text{ cm}^2$$<br>O hexágono regular é formado por 6 desses triângulos:<br>$$A_{\\text{hex}} = 6 \\times 4\\sqrt{3} = 24\\sqrt{3}\\text{ cm}^2$$<br>Substituindo $\\sqrt{3} \\approx 1{,}7$:<br>$$A = 24 \\times 1{,}7 = 40{,}8\\text{ cm}^2.$$Portanto, a alternativa correta é a <strong>Letra C</strong>."
        },
        {
            "q": "Para decorar uma festa de Halloween, um estudante desenhou uma estrela formada por um quadrado central de lado $6\\text{ cm}$ e quatro triângulos isósceles com base de $6\\text{ cm}$ e altura de $4\\text{ cm}$ apoiados em cada um dos lados do quadrado. A área total da estrela é:",
            "options": ["$60\\text{ cm}^2$", "$72\\text{ cm}^2$", "$84\\text{ cm}^2$", "$96\\text{ cm}^2$"],
            "correct": 2,
            "explanation": "1. Área do quadrado central:<br>$$A_{\\text{quad}} = 6 \\times 6 = 36\\text{ cm}^2$$<br>2. Área de cada triângulo:<br>$$A_{\\text{tri}} = \\frac{b \\cdot h}{2} = \\frac{6 \\times 4}{2} = 12\\text{ cm}^2$$<br>3. A estrela possui 4 triângulos:<br>$$A_{\\text{total}} = 36 + 4 \\times 12 = 36 + 48 = 84\\text{ cm}^2.$$Portanto, a alternativa correta é a <strong>Letra C</strong>."
        },
        {
            "q": "Um clube possui uma piscina retangular de $10\\text{ m} \\times 6\\text{ m}$ cercada por uma calçada de solário com largura uniforme de $2\\text{ metros}$ ao redor de toda a piscina. A área total ocupada pela piscina e solário juntos é de:",
            "options": ["$96\\text{ m}^2$", "$120\\text{ m}^2$", "$140\\text{ m}^2$", "$160\\text{ m}^2$"],
            "correct": 2,
            "explanation": "A piscina mede $10\\text{ m} \\times 6\\text{ m}$.<br>Com a calçada de $2\\text{ m}$ em cada lado, as novas dimensões externas são:<br>- Comprimento total: $10 + 2 + 2 = 14\\text{ m}$<br>- Largura total: $6 + 2 + 2 = 10\\text{ m}$<br>Calculando a área total externa:<br>$$A_{\\text{total}} = 14 \\times 10 = 140\\text{ m}^2.$$Portanto, a alternativa correta é a <strong>Letra C</strong>."
        },
        {
            "q": "A estrela Proxima Centauri situa-se a aproximadamente 40 trilhões de quilômetros da Terra. Escrevendo esse número por extenso e em notação científica, temos:",
            "options": [
                "$4 \\times 10^{10}\\text{ km}$",
                "$4 \\times 10^{11}\\text{ km}$",
                "$4 \\times 10^{12}\\text{ km}$",
                "$4 \\times 10^{13}\\text{ km}$"
            ],
            "correct": 3,
            "explanation": "1 milhão $= 10^6$<br>1 bilhão $= 10^9$<br>1 trilhão $= 10^{12}$<br>Portanto, 40 trilhões de quilômetros é igual a:<br>$$40 \\times 10^{12} = 4 \\times 10^{13}\\text{ km}.$$Portanto, a alternativa correta é a <strong>Letra D</strong>."
        },
        {
            "q": "Durante a crise hídrica, uma residência reduziu seu consumo mensal de água de $25\\text{ m}^3$ para $18\\text{ m}^3$. Sabendo que cada metro cúbico equivale a $1.000\\text{ litros}$, quantos litros de água foram economizados no mês por essa família?",
            "options": ["$5.000\\text{ L}$", "$7.000\\text{ L}$", "$8.000\\text{ L}$", "$10.000\\text{ L}$"],
            "correct": 1,
            "explanation": "A economia em metros cúbicos foi:<br>$$\\Delta V = 25 - 18 = 7\\text{ m}^3$$<br>Convertendo para litros ($1\\text{ m}^3 = 1.000\\text{ L}$):<br>$$7 \\times 1.000 = 7.000\\text{ litros}.$$Portanto, a alternativa correta é a <strong>Letra B</strong>."
        },
        {
            "q": "Um estudante enviou 120 mensagens de texto em um dia. No dia seguinte, enviou $15\\%$ a mais de mensagens. Quantas mensagens foram enviadas no segundo dia?",
            "options": ["132", "136", "138", "142"],
            "correct": 2,
            "explanation": "Calculando o aumento de $15\\%$ sobre 120 mensagens:<br>$$0{,}15 \\times 120 = 18\\text{ mensagens a mais}$$<br>Total no segundo dia:<br>$$120 + 18 = 138\\text{ mensagens}.$$Portanto, a alternativa correta é a <strong>Letra C</strong>."
        }
    ]
}

data = {
    "EXAM_2022_1_MANHA": EXAM_2022_1_MANHA,
    "EXAM_2022_1_TARDE": EXAM_2022_1_TARDE
}

with open("scripts/data_ifsp/exams_2022.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Saved scripts/data_ifsp/exams_2022.json successfully!")
