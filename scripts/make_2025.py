import json

EXAM_2025_1_A = {
    "id": "ifsp-2025-1-a",
    "title": "Prova IFSP 2025.1 - Prova A",
    "bncc": "Revisão Geral",
    "summary": "15 questões de Matemática aplicadas no Processo Seletivo IFSP 2025.1 (Edital Nº 088/2024 - Prova A) para os Cursos Técnicos Integrados.",
    "detailedTheory": "A Prova A do Processo Seletivo IFSP 2025.1 contemplou potenciação com expoentes fracionários e radiciação, análise combinatória em tabuleiros (posicionamento de peças independentes), geometria plana com áreas de figuras compostas e canteiros quadrangulares, probabilidade com espaços amostrais equiprováveis e não equiprováveis, porcentagem e descontos sucessivos no comércio (Black Friday), equações lineares do 1º grau com representação gráfica no plano cartesiano, razão e proporção com consumo por aluno, análise de tabelas de preços e conversão de grandezas monetárias, Teorema de Pitágoras com números irracionais e ordenação, semelhança de triângulos e proporcionalidade de lados, geometria métrica da circunferência com arcos e ângulos centrais em triângulos equiláteros, trigonometria/Pitágoras na rampa do Planalto, grandezas inversamente proporcionais (velocidade e tempo) e notação científica de unidades de armazenamento de dados binários.",
    "keyPoints": [
        "A transformação de raiz em potência com expoente fracionário obedece à regra $\\sqrt[n]{a^m} = a^{\\frac{m}{n}}$.",
        "Em grandezas inversamente proporcionais, o produto entre as variáveis é constante: $v_1 \\cdot t_1 = v_2 \\cdot t_2$.",
        "Dois triângulos são semelhantes se seus lados correspondentes forem proporcionais (Caso LLL de semelhança).",
        "No plano cartesiano, a equação linear $ax + by = c$ representa uma reta cujos pontos podem ser determinados encontrando os interceptos com os eixos coordenados."
    ],
    "formula": "\\sqrt[n]{a^m} = a^{\\frac{m}{n}}, \\quad h^2 = a^2 + b^2, \\quad v_1 t_1 = v_2 t_2, \\quad P(E) = \\frac{n(E)}{n(\\Omega)}",
    "solvedExample": {
        "problem": "Um carro a $60\\text{ km/h}$ realiza uma viagem em $4\\text{ horas}$. Se a velocidade aumentar para $80\\text{ km/h}$, qual será o novo tempo de percurso?",
        "solution": "Como velocidade e tempo são inversamente proporcionais:<br>$$60 \\times 4 = 80 \\times t \\implies 240 = 80t \\implies t = \\frac{240}{80} = 3\\text{ horas}.$$"
    },
    "slug": "prova-ifsp-20251-a",
    "filename": "prova-ifsp-20251-a.html",
    "folder": "bloco-7-provas-ifsp",
    "blockId": 7,
    "pdf": "IFSP_prova_2025_1_a.pdf",
    "questions": [
        {
            "q": "Em uma aula de matemática, a professora passou para sua turma uma lista de exercícios, na qual era necessário calcular o valor decimal de $\\sqrt{7}$ e era permitido aos alunos o uso da calculadora. Um aluno falou que não iria conseguir realizar a atividade, pois a tecla de calcular raiz quadrada de sua calculadora estava quebrada. A professora sugeriu, então, que ele transformasse a raiz em potência com expoente fracionário. Qual a representação de $\\sqrt{7}$ que o aluno precisa utilizar?",
            "options": ["$2^{\\frac{1}{7}}$", "$2^{\\frac{7}{1}}$", "$7^{\\frac{2}{1}}$", "$7^{\\frac{1}{2}}$"],
            "correct": 3,
            "explanation": "Pela propriedade fundamental que relaciona radiciação e potenciação, temos que $\\sqrt[n]{a^m} = a^{\\frac{m}{n}}$.<br>No caso de $\\sqrt{7}$, o radicando tem expoente implícito $m = 1$ e o índice da raiz quadrada é $n = 2$:<br>$$\\sqrt{7} = \\sqrt[2]{7^1} = 7^{\\frac{1}{2}}$$Portanto, a alternativa correta é a <strong>Letra D</strong>."
        },
        {
            "q": "O jogo de xadrez possui peças brancas e pretas. Entre elas, existem as torres que se movimentam em linhas retas, tanto na vertical quanto na horizontal, quantas casas o jogador quiser. Em um tabuleiro especial de xadrez $4 \\times 4$, contendo 16 casas, a quantidade de maneiras que podemos colocar uma torre branca e outra torre preta nesse tabuleiro de modo que não estejam alinhadas na vertical ou na horizontal (impossibilitando um ataque mútuo) é:",
            "options": ["63", "112", "144", "160"],
            "correct": 2,
            "explanation": "Vamos analisar o princípio multiplicativo de contagem:<br>1. A primeira torre (branca) pode ser colocada em qualquer uma das $16$ casas do tabuleiro.<br>2. Ao ocupar uma casa, ela passa a atacar todas as casas da sua mesma linha (4 casas) e da sua mesma coluna (4 casas). Como a casa onde ela está pertence a ambas, o total de casas atacadas ou bloqueadas é $4 + 4 - 1 = 7$ casas.<br>3. Para que as torres não estejam na mesma linha nem na mesma coluna, a torre preta deve ser posicionada em uma das casas restantes: $16 - 7 = 9$ casas livres.<br>4. Multiplicando as possibilidades:<br>$$\\text{Total} = 16 \\times 9 = 144\\text{ maneiras}.$$Portanto, a alternativa correta é a <strong>Letra C</strong>."
        },
        {
            "q": "A figura representa um canteiro destinado a uma horta comunitária planejada por um campus do IFSP, dividida nas áreas I (plantação, com formato quadrado de lado $x$), II e III (circulação) e IV (cabana de materiais). Sabendo que $x > 0$, que a área destinada para a plantação (Área I) é de $81\\text{ m}^2$ e que as faixas de circulação têm largura de $1{,}1\\text{ m}$ ao redor, a área total do canteiro, em $\\text{m}^2$, é de:",
            "options": ["$1.806{,}25$", "$121{,}00$", "$117{,}00$", "$102{,}01$"],
            "correct": 3,
            "explanation": "1. A área da plantação (Área I) é um quadrado com área de $81\\text{ m}^2$:<br>$$x^2 = 81 \\implies x = 9\\text{ m}$$<br>2. Com as margens e áreas complementares de $1{,}1\\text{ m}$, o lado total do canteiro quadrado passa a ser:<br>$$L = 9 + 1{,}1 = 10{,}1\\text{ m}$$<br>3. Calculando a área total do canteiro quadrado:<br>$$\\text{Área Total} = L^2 = (10{,}1)^2 = 102{,}01\\text{ m}^2.$$Portanto, a alternativa correta é a <strong>Letra D</strong>."
        },
        {
            "q": "Um professor desenvolveu um dispositivo composto por um botão e um retângulo dividido em 6 partes de tamanhos iguais, numeradas de 1 a 6. Cada vez que o botão é pressionado, uma única parte fica iluminada. Cada uma das partes com um número par tem probabilidade $P$ de ficar iluminada e cada uma das partes com um número ímpar tem probabilidade $3P$. Quando o professor pressionar o botão, qual a probabilidade de que uma parte com um número primo fique iluminada?",
            "options": ["$\\frac{7}{12}$", "$\\frac{5}{6}$", "$\\frac{3}{4}$", "$\\frac{1}{2}$"],
            "correct": 0,
            "explanation": "1. Os números de 1 a 6 dividem-se em:<br>- Pares: $\\{2, 4, 6\\}$ (3 números, cada um com probabilidade $P$)<br>- Ímpares: $\\{1, 3, 5\\}$ (3 números, cada um com probabilidade $3P$)<br><br>2. A soma de todas as probabilidades do espaço amostral deve ser igual a 1:<br>$$3 \\cdot P + 3 \\cdot (3P) = 1 \\implies 3P + 9P = 12P = 1 \\implies P = \\frac{1}{12}$$<br>3. Os números primos entre 1 e 6 são $\\{2, 3, 5\\}$ (lembrando que 1 não é primo):<br>- O número 2 é par: probabilidade $= P = \\frac{1}{12}$<br>- O número 3 é ímpar: probabilidade $= 3P = \\frac{3}{12}$<br>- O número 5 é ímpar: probabilidade $= 3P = \\frac{3}{12}$<br><br>4. Somando as probabilidades favoráveis:<br>$$P(\\text{primo}) = P + 3P + 3P = 7P = 7 \\times \\frac{1}{12} = \\frac{7}{12}.$$Portanto, a alternativa correta é a <strong>Letra A</strong>."
        },
        {
            "q": "Se considerarmos que o preço inicial do litro da gasolina é de R$ 5,60, e que na Black Friday ocorra um desconto de 50%, é correto afirmar que:",
            "options": [
                "após um aumento de 40% e um desconto de 50% na Black Friday, o preço final do combustível será 10% menor que o preço inicial.",
                "após um aumento de 60% e um desconto de 50% na Black Friday, o preço final do combustível será 10% maior que o preço inicial.",
                "após um aumento de 70% e um desconto de 50% na Black Friday, o preço final do combustível será R$ 5,88.",
                "após um aumento de 100% e um desconto de 50% na Black Friday, o preço final do combustível será exatamente igual ao preço inicial."
            ],
            "correct": 3,
            "explanation": "Vamos analisar os fatores de multiplicação para cada percentual:<br>1. Um aumento de $100\\%$ corresponde a multiplicar o valor por $(1 + 1{,}00) = 2$. O preço passa a ser $2 \\times 5{,}60 = \\text{R\\$ } 11{,}20$.<br>2. Em seguida, um desconto de $50\\%$ corresponde a multiplicar por $(1 - 0{,}50) = 0{,}50$.<br>3. O preço final é:<br>$$\\text{Preço Final} = P_0 \\times 2 \\times 0{,}50 = P_0 \\times 1 = P_0$$<br>Logo, o preço final do combustível volta a ser exatamente igual ao preço inicial de R$ 5,60.<br>Portanto, a alternativa correta é a <strong>Letra D</strong>."
        },
        {
            "q": "Seja $2x - 2y = 4$ uma equação linear de 1º grau. A representação gráfica dessa equação no plano cartesiano é uma reta que intersecta os eixos cartesianos nos pontos:",
            "options": [
                "$(0, 2)$ e $(2, 0)$",
                "$(0, -2)$ e $(-2, 0)$",
                "$(2, 0)$ e $(0, -2)$",
                "$(0, 4)$ e $(4, 0)$"
            ],
            "correct": 2,
            "explanation": "Simplificando a equação $2x - 2y = 4$ dividindo todos os termos por 2:<br>$$x - y = 2 \\iff y = x - 2$$<br>Vamos determinar os interceptos com os eixos:<br>1. Intercepto com o eixo $x$ (onde $y = 0$):<br>$$x - 0 = 2 \\implies x = 2 \\implies (2, 0)$$<br>2. Intercepto com o eixo $y$ (onde $x = 0$):<br>$$0 - y = 2 \\implies y = -2 \\implies (0, -2)$$<br>Trata-se de uma reta crescente que corta o eixo $x$ em $2$ e o eixo $y$ em $-2$.<br>Portanto, a alternativa correta é a <strong>Letra C</strong>."
        },
        {
            "q": "Uma pessoa deseja comprar um ingresso para um show que terá 4 categorias: pista, pista premium, área vip e camarote. As formas de pagamento disponíveis são 3: Pix, cartão de débito e cartão de crédito. Considerando que todas as combinações são igualmente prováveis, qual a probabilidade de a pessoa comprar o ingresso de pista e pagar por Pix?",
            "options": ["$\\frac{1}{12}$", "$\\frac{1}{7}$", "$\\frac{1}{4}$", "$\\frac{1}{3}$"],
            "correct": 0,
            "explanation": "1. O espaço amostral $\\Omega$ é formado por todas as combinações entre categoria de ingresso e forma de pagamento:<br>$$n(\\Omega) = 4 \\times 3 = 12\\text{ combinações possíveis}$$<br>2. O evento desejado é escolher especificamente a categoria pista E pagamento por Pix:<br>$$n(E) = 1\\text{ combinação}$$<br>3. A probabilidade é dada por:<br>$$P = \\frac{n(E)}{n(\\Omega)} = \\frac{1}{12}.$$Portanto, a alternativa correta é a <strong>Letra A</strong>."
        },
        {
            "q": "Uma nutricionista observou que para 325 alunos eram consumidos $195\\text{ kg}$ de alimentos em um restaurante estudantil do IFSP. Certo dia, ela percebeu que para 210 alunos foram consumidos $126\\text{ kg}$. Com base nessas informações, a quantidade de alimento consumida por aluno, em gramas, é de:",
            "options": ["60", "600", "1.667", "26.460"],
            "correct": 1,
            "explanation": "Calculamos a taxa de consumo por aluno dividindo a massa total de alimento pelo número de alunos:<br>$$\\text{Consumo} = \\frac{195\\text{ kg}}{325\\text{ alunos}} = 0{,}6\\text{ kg por aluno}$$<br>Verificando para o segundo grupo de 210 alunos:<br>$$\\frac{126\\text{ kg}}{210\\text{ alunos}} = 0{,}6\\text{ kg por aluno}$$<br>Convertendo de quilogramas para gramas ($1\\text{ kg} = 1000\\text{ g}$):<br>$$0{,}6 \\times 1000 = 600\\text{ gramas por aluno}.$$Portanto, a alternativa correta é a <strong>Letra B</strong>."
        },
        {
            "q": "Um gerente construiu uma tabela com preços médios cotados em vários estados: no ES (Abacate R$ 1,70; Berinjela R$ 3,00; Limão Taiti R$ 3,50), em MG (R$ 3,25; R$ 3,00; R$ 3,50), no PR (R$ 3,50; R$ 4,20; R$ 3,00), no RJ (R$ 4,00; R$ 3,00; R$ 3,25), no RS (R$ 3,30; R$ 5,00; R$ 2,80), em SC (R$ 3,00; R$ 3,50; R$ 2,25) e em SP (R$ 2,50; R$ 3,60; R$ 2,20). Para a compra de $1\\text{ kg}$ de Abacate, $2\\text{ kg}$ de Berinjela e $3\\text{ kg}$ de Limão Taiti, é correto afirmar que:",
            "options": [
                "como os preços individuais dos três produtos são diferentes em cada um dos estados, os valores totais encontrados em todas as pesagens serão diferentes.",
                "o maior valor para a aquisição dos três produtos, a partir das pesagens indicadas, está em um estado em que pelo menos um produto é mais caro, quando comparado a outros estados.",
                "o menor valor para a aquisição dos três produtos é obtido em dois estados distintos.",
                "se em dois estados os valores totais das compras forem iguais, então os valores individuais de cada produto também serão iguais."
            ],
            "correct": 1,
            "explanation": "Calculando o custo total $V = 1 \\cdot P_{\\text{abacate}} + 2 \\cdot P_{\\text{berinjela}} + 3 \\cdot P_{\\text{limão}}$ em cada estado:<br>- ES: $1(1,70) + 2(3,00) + 3(3,50) = 1,70 + 6,00 + 10,50 = 18,20$<br>- MG: $1(3,25) + 2(3,00) + 3(3,50) = 3,25 + 6,00 + 10,50 = 19,75$<br>- PR: $1(3,50) + 2(4,20) + 3(3,00) = 3,50 + 8,40 + 9,00 = 20,90$<br>- RJ: $1(4,00) + 2(3,00) + 3(3,25) = 4,00 + 6,00 + 9,75 = 19,75$<br>- RS: $1(3,30) + 2(5,00) + 3(2,80) = 3,30 + 10,00 + 8,40 = 21,70$ (maior valor!)<br>- SC: $1(3,00) + 2(3,50) + 3(2,25) = 3,00 + 7,00 + 6,75 = 16,75$<br>- SP: $1(2,50) + 2(3,60) + 3(2,20) = 2,50 + 7,20 + 6,60 = 16,30$ (menor valor)<br><br>O maior valor ocorreu no RS (R$ 21,70), onde a berinjela tem o maior preço unitário da tabela (R$ 5,00).<br>Portanto, a alternativa correta é a <strong>Letra B</strong>."
        },
        {
            "q": "Um professor propôs aos alunos calcularem os valores $X$, $Y$ e $Z$ a partir do Teorema de Pitágoras ($h^2 = a^2 + b^2$):<br>1º Conjunto: $h = \\sqrt{3}$, $a = X$ e $b = 1$<br>2º Conjunto: $h = 5$, $a = 1$ e $b = Y$<br>3º Conjunto: $h = Z$, $a = 2$ e $b = \\sqrt{3}$<br>Ao colocar esses números irracionais em ordem crescente, a sequência correta é:",
            "options": ["$X, Z, Y$", "$X, Y, Z$", "$Y, X, Z$", "$Y, Z, X$"],
            "correct": 0,
            "explanation": "Aplicando o Teorema de Pitágoras $h^2 = a^2 + b^2$ em cada conjunto:<br>1. Para $X$: $(\\sqrt{3})^2 = X^2 + 1^2 \\implies 3 = X^2 + 1 \\implies X^2 = 2 \\implies X = \\sqrt{2} \\approx 1{,}414$<br>2. Para $Y$: $5^2 = 1^2 + Y^2 \\implies 25 = 1 + Y^2 \\implies Y^2 = 24 \\implies Y = \\sqrt{24} \\approx 4{,}899$<br>3. Para $Z$: $Z^2 = 2^2 + (\\sqrt{3})^2 \\implies Z^2 = 4 + 3 = 7 \\implies Z = \\sqrt{7} \\approx 2{,}646$<br><br>Comparando os radicandos: $2 < 7 < 24 \\implies \\sqrt{2} < \\sqrt{7} < \\sqrt{24}$, ou seja:<br>$$X < Z < Y$$Portanto, a alternativa correta é a <strong>Letra A</strong>."
        },
        {
            "q": "Dois triângulos $ABC$ e $DEF$ foram construídos de maneira que $DE = 2 \\cdot AB$, $DF = 2 \\cdot AC$ e $FE = 2 \\cdot BC$. Considerando essa informação, podemos afirmar que $ABC$ e $DEF$ são triângulos semelhantes porque:",
            "options": [
                "as medidas dos lados do triângulo ABC são proporcionais às medidas dos lados do triângulo DEF.",
                "nenhum dos dois triângulos possui um de seus ângulos internos igual a um ângulo reto.",
                "a medida da área do triângulo DEF é quatro vezes maior que a medida da área do triângulo ABC.",
                "a medida do perímetro do triângulo DEF é o dobro da medida do perímetro do triângulo ABC."
            ],
            "correct": 0,
            "explanation": "Pelo Caso LLL (Lado-Lado-Lado) de semelhança geométrica, dois triângulos são semelhantes se, e somente se, todos os seus lados homólogos forem proporcionais.<br>Como $\\frac{DE}{AB} = \\frac{DF}{AC} = \\frac{FE}{BC} = 2$, a razão de semelhança é constante e igual a 2, garantindo que os triângulos são semelhantes.<br>Portanto, a alternativa correta é a <strong>Letra A</strong>."
        },
        {
            "q": "Uma circunferência de centro $C$ tem diâmetro $AB$. Sobre o raio $CD$ construiu-se um triângulo equilátero unindo-se os pontos $B$ e $C$ ao ponto $D$, que está sobre a circunferência. Qual é a medida (em graus) do arco $\\widehat{AD}$?",
            "options": ["$60^\\circ$", "$90^\\circ$", "$120^\\circ$", "$180^\\circ$"],
            "correct": 2,
            "explanation": "1. Como os pontos $B$ e $D$ pertencem à circunferência de centro $C$, os segmentos $CB$ e $CD$ são raios: $CB = CD = R$.<br>2. O triângulo $BCD$ é equilátero, logo todos os seus ângulos internos medem $60^\\circ$, em particular o ângulo central $B\\widehat{C}D = 60^\\circ$.<br>3. Como $AB$ é diâmetro da circunferência, o ângulo raso central $A\\widehat{C}B = 180^\\circ$.<br>4. O ângulo central correspondente ao arco $\\widehat{AD}$ é suplementar a $B\\widehat{C}D$:<br>$$A\\widehat{C}D = 180^\\circ - 60^\\circ = 120^\\circ$$<br>Como a medida angular de um arco é igual à medida de seu ângulo central correspondente, o arco $\\widehat{AD}$ mede $120^\\circ$.<br>Portanto, a alternativa correta é a <strong>Letra C</strong>."
        },
        {
            "q": "Supondo que o triângulo retângulo $ABC$ é retângulo em $A$ com catetos $AC = 4\\text{ m}$ e $AB = 12\\sqrt{7}\\text{ m}$, quantos metros percorrerá uma pessoa que caminha em linha reta ao longo da rampa do ponto $B$ ao ponto $C$? (Dado: $(12\\sqrt{7})^2 = 1008$).",
            "options": ["$1024\\text{ m}$", "$1008\\text{ m}$", "$32\\text{ m}$", "$16\\text{ m}$"],
            "correct": 2,
            "explanation": "A distância percorrida de $B$ a $C$ corresponde à hipotenusa $BC$ do triângulo retângulo $ABC$.<br>Aplicando o Teorema de Pitágoras:<br>$$BC^2 = AC^2 + AB^2$$<br>Substituindo os valores dados:<br>$$BC^2 = 4^2 + (12\\sqrt{7})^2 = 16 + 1008 = 1024$$<br>Extraindo a raiz quadrada:<br>$$BC = \\sqrt{1024} = 32\\text{ metros}.$$Portanto, a alternativa correta é a <strong>Letra C</strong>."
        },
        {
            "q": "Um carro com velocidade constante de $60\\text{ km/h}$ pode fazer um determinado percurso em $4\\text{ horas}$. Se a velocidade do carro aumentasse para $80\\text{ km/h}$, em quantas horas ele faria o mesmo percurso?",
            "options": ["5,3", "3,0", "2,0", "1,3"],
            "correct": 1,
            "explanation": "Velocidade e tempo são grandezas inversamente proporcionais para uma distância fixa $d$:<br>$$d = v_1 \\cdot t_1 = 60\\text{ km/h} \\times 4\\text{ h} = 240\\text{ km}$$<br>Com a nova velocidade de $80\\text{ km/h}$:<br>$$t_2 = \\frac{d}{v_2} = \\frac{240\\text{ km}}{80\\text{ km/h}} = 3\\text{ horas}.$$Portanto, a alternativa correta é a <strong>Letra B</strong>."
        },
        {
            "q": "Considerando as unidades de armazenamento de dados binários em computação (onde $1\\text{ KB} = 2^{10}\\text{ bytes}$, $1\\text{ MB} = 2^{20}\\text{ bytes}$, $1\\text{ GB} = 2^{30}\\text{ bytes}$, $1\\text{ TB} = 2^{40}\\text{ bytes}$ e $1\\text{ PB} = 2^{50}\\text{ bytes}$), assinale a única afirmação correta:",
            "options": [
                "Dois Terabytes têm $2^{80}$ bytes.",
                "Um Gigabyte tem a metade da quantidade de bytes de um Exabyte.",
                "Um Megabyte tem o dobro da quantidade de bytes de um Kilobyte.",
                "Um Petabyte tem mais bytes que a soma de um Gigabyte com um Terabyte."
            ],
            "correct": 3,
            "explanation": "Vamos analisar cada alternativa:<br>1. Dois Terabytes: $2 \\times 2^{40} = 2^{41}\\text{ bytes} \\neq 2^{80}$ (Falsa).<br>2. Um Gigabyte ($2^{30}$) não é metade de um Exabyte ($2^{60}$); metade de $2^{60}$ seria $2^{59}$ (Falsa).<br>3. Um Megabyte ($2^{20} = 1.048.576\\text{ bytes}$) tem $1024$ vezes a quantidade de um Kilobyte ($2^{10} = 1024\\text{ bytes}$), e não o dobro (Falsa).<br>4. Um Petabyte equivale a $2^{50}\\text{ bytes} \\approx 1{,}126 \\times 10^{15}$. Já a soma de $1\\text{ GB} + 1\\text{ TB} = 2^{30} + 2^{40} \\approx 1{,}1 \\times 10^{12}\\text{ bytes}$. Como $2^{50}$ é ordens de grandeza maior que $2^{40} + 2^{30}$, a afirmação é verdadeira.<br>Portanto, a alternativa correta é a <strong>Letra D</strong>."
        }
    ]
}

EXAM_2025_1_B = {
    "id": "ifsp-2025-1-b",
    "title": "Prova IFSP 2025.1 - Prova B",
    "bncc": "Revisão Geral",
    "summary": "15 questões de Matemática aplicadas no Processo Seletivo IFSP 2025.1 (Edital Nº 088/2024 - Prova B) para os Cursos Técnicos Integrados.",
    "detailedTheory": "A Prova B do Processo Seletivo IFSP 2025.1 abordou padrões e sequências lógicas em peças de dominó, princípio fundamental da contagem na formação de senhas alfanuméricas com vogais e consoantes, geometria plana com áreas de figuras compostas (trapézio retângulo e galpão) e fração de área gramada, relações volumétricas e proporcionalidade cúbica em recipientes com variação de aresta, notação científica e operações com potências de base 10 em distâncias astronômicas de ida e volta, geometria analítica com cálculo de ponto médio de um segmento, progressões e modelagem de sequências em situações cotidianas, matemática financeira com descontos sucessivos de tarifas por hora, análise estatística com média aritmética de perdas populacionais no Censo do IBGE, conceitos e critérios de semelhança de triângulos (critérios LAL, AA e Teorema Fundamental), proporcionalidade direta no tempo de download de arquivos com conversão de minutos e segundos, estatística descritiva com determinação da moda e mediana em distribuição de frequências, valor numérico de expressões e sequências geradas por fluxogramas, construções geométricas com régua e compasso de triângulos equiláteros, e cálculo do raio de setores semicirculares com porcentagem de área total.",
    "keyPoints": [
        "Se a aresta de um cubo é multiplicada por um fator $k$, o volume é multiplicado pelo cubo do fator: $V' = k^3 \\cdot V$.",
        "O ponto médio $M(X_m, Y_m)$ entre dois pontos $A(x_1, y_1)$ e $B(x_2, y_2)$ é dado por $X_m = \\frac{x_1 + x_2}{2}$ e $Y_m = \\frac{y_1 + y_2}{2}$.",
        "A mediana de um conjunto ordenado com número par de elementos é a média aritmética dos dois termos centrais.",
        "A área de um semicírculo de raio $R$ é calculada por $A = \\frac{\\pi R^2}{2}$."
    ],
    "formula": "X_m = \\frac{x_1+x_2}{2}, \\quad Y_m = \\frac{y_1+y_2}{2}, \\quad V = a^3, \\quad A_{\\text{trap}} = \\frac{(B+b)h}{2}, \\quad A_{\\text{semi}} = \\frac{\\pi R^2}{2}",
    "solvedExample": {
        "problem": "Determine o raio de um jardim semicircular cuja área representa 5% de um terreno retangular de $30\\text{ m} \\times 20\\text{ m}$, adotando $\\pi = 3$.",
        "solution": "1. Área total do terreno: $A = 30 \\times 20 = 600\\text{ m}^2$.<br>2. Área do jardim: $5\\% \\text{ de } 600 = 0{,}05 \\times 600 = 30\\text{ m}^2$.<br>3. Área do semicírculo: $\\frac{\\pi R^2}{2} = 30 \\implies \\frac{3 R^2}{2} = 30 \\implies R^2 = 20 \\implies R = \\sqrt{20} = 2\\sqrt{5}\\text{ m}$."
    },
    "slug": "prova-ifsp-20251-b",
    "filename": "prova-ifsp-20251-b.html",
    "folder": "bloco-7-provas-ifsp",
    "blockId": 7,
    "pdf": "IFSP_prova_2025_1_b.pdf",
    "questions": [
        {
            "q": "O dominó é um jogo formado por 28 peças retangulares com duas metades pontuadas de 0 a 6. Um estudante organizou quatro peças sequenciais com as seguintes somas de pontos: peça 1 [1|2] soma 3; peça 2 [2|3] soma 5; peça 3 [3|4] soma 7; peça 4 [4|5] soma 9. Se o estudante quiser manter a regularidade identificada, para a quinta peça ele deverá escolher:",
            "options": [
                "qualquer peça em que a soma dos pontos seja 9.",
                "qualquer peça em que a soma dos pontos seja um número par.",
                "uma peça em que a soma dos pontos seja 11.",
                "uma peça em que a soma dos pontos seja 12."
            ],
            "correct": 2,
            "explanation": "A sequência formada pelas somas dos pontos de cada peça é:<br>$$3, \\, 5, \\, 7, \\, 9, \\dots$$Trata-se de uma progressão aritmética de primeiro termo $a_1 = 3$ e razão $r = 2$ (números ímpares consecutivos).<br>O quinto termo da sequência é:<br>$$a_5 = 9 + 2 = 11$$Portanto, o estudante deverá escolher uma peça cuja soma dos pontos seja 11 (como a peça [5|6]).<br>Portanto, a alternativa correta é a <strong>Letra C</strong>."
        },
        {
            "q": "Um adolescente deseja criar uma senha usando exatamente quatro letras minúsculas escolhidas entre as 26 do alfabeto. Ele decide que as duas primeiras letras serão consoantes diferentes entre si e que as duas últimas letras serão vogais também diferentes entre si. Nestas condições, quantas senhas diferentes ele pode criar?",
            "options": ["8.400", "11.025", "358.800", "456.976"],
            "correct": 0,
            "explanation": "No alfabeto de 26 letras da língua portuguesa, temos $5$ vogais (a, e, i, o, u) e $21$ consoantes.<br>Aplicando o princípio fundamental da contagem para as 4 posições da senha:<br>1. 1ª letra (consoante): $21$ opções.<br>2. 2ª letra (consoante diferente da 1ª): $20$ opções.<br>3. 3ª letra (vogal): $5$ opções.<br>4. 4ª letra (vogal diferente da 3ª): $4$ opções.<br><br>Multiplicando todas as possibilidades:<br>$$\\text{Total} = 21 \\times 20 \\times 5 \\times 4 = 420 \\times 20 = 8.400\\text{ senhas}.$$Portanto, a alternativa correta é a <strong>Letra A</strong>."
        },
        {
            "q": "Em um terreno com a forma de um trapézio retângulo com base menor de $12\\text{ m}$, base maior de $18\\text{ m}$ e altura total de $20\\text{ m}$ ($5\\text{ m} + 15\\text{ m}$), será construído um galpão retangular de dimensões $10\\text{ m} \\times 15\\text{ m}$. O empreiteiro decidiu que um terço da área externa ao galpão será pavimentado e os dois terços restantes serão cobertos com grama. A área que o gramado ocupará, em $\\text{m}^2$, é igual a:",
            "options": ["300", "150", "100", "50"],
            "correct": 2,
            "explanation": "1. Calculamos a área total do terreno em formato de trapézio retângulo:<br>$$A_{\\text{terreno}} = \\frac{(B + b) \\cdot h}{2} = \\frac{(18 + 12) \\cdot 20}{2} = \\frac{30 \\cdot 20}{2} = 300\\text{ m}^2$$<br>2. Calculamos a área ocupada pelo galpão retangular:<br>$$A_{\\text{galpão}} = 10 \\times 15 = 150\\text{ m}^2$$<br>3. A área externa ao galpão é:<br>$$A_{\\text{externa}} = 300 - 150 = 150\\text{ m}^2$$<br>4. Como dois terços ($2/3$) da área externa serão cobertos com grama:<br>$$A_{\\text{gramado}} = \\frac{2}{3} \\times 150 = 100\\text{ m}^2.$$Portanto, a alternativa correta é a <strong>Letra C</strong>."
        },
        {
            "q": "Desprezando a espessura de seus lados, sabe-se que um recipiente em formato cúbico de aresta igual a $10\\text{ cm}$ tem capacidade para armazenar $1\\text{ litro}$ de água. Nestas condições, quantos litros de água cabem em um recipiente cúbico cuja aresta é igual a $40\\text{ cm}$?",
            "options": ["120 litros", "4 litros", "64 litros", "640 litros"],
            "correct": 2,
            "explanation": "1. O volume de um cubo é dado por $V = a^3$.<br>Para aresta $a_1 = 10\\text{ cm}$, temos $V_1 = 10^3 = 1000\\text{ cm}^3 = 1\\text{ litro}$.<br><br>2. Para o novo cubo de aresta $a_2 = 40\\text{ cm}$, a razão entre as arestas é:<br>$$k = \\frac{40}{10} = 4$$<br>3. Pela propriedade de semelhança de sólidos tridimensionais, o volume varia com o cubo da razão linear de semelhança ($k^3$):<br>$$V_2 = k^3 \\cdot V_1 = 4^3 \\times 1\\text{ litro} = 64 \\times 1 = 64\\text{ litros}.$$Portanto, a alternativa correta é a <strong>Letra C</strong>."
        },
        {
            "q": "De acordo com dados astronômicos, a aproximação máxima teórica entre a Terra e Marte é de $54{,}6\\text{ milhões de quilômetros}$. Imagine que fosse possível viajar da Terra até Marte aproveitando essa aproximação máxima. Em notação científica, o total de quilômetros percorridos em uma viagem de ida e volta é de:",
            "options": ["$7{,}000 \\times 10^7$", "$5{,}460 \\times 10^7$", "$1{,}400 \\times 10^8$", "$1{,}092 \\times 10^8$"],
            "correct": 3,
            "explanation": "1. A distância de ida é de $54{,}6\\text{ milhões de km} = 54{,}6 \\times 10^6\\text{ km}$.<br>2. A viagem de ida e volta corresponde ao dobro dessa distância:<br>$$\\text{Distância Total} = 2 \\times (54{,}6 \\times 10^6) = 109{,}2 \\times 10^6\\text{ km}$$<br>3. Para converter para notação científica padrão ($1 \\le a < 10$):<br>$$109{,}2 \\times 10^6 = 1{,}092 \\times 10^2 \\times 10^6 = 1{,}092 \\times 10^8\\text{ km}.$$Portanto, a alternativa correta é a <strong>Letra D</strong>."
        },
        {
            "q": "Ao saltar de um avião, um paraquedista aterrissou exatamente no ponto médio entre uma árvore localizada no ponto $A(2, 3)$ e um rochedo localizado no ponto $B(4, -5)$. O ponto médio $M(X_m, Y_m)$ onde o paraquedista aterrissou é:",
            "options": ["$M(3, -1)$", "$M(3, 4)$", "$M(5, -1)$", "$M(3, -4)$"],
            "correct": 0,
            "explanation": "As coordenadas do ponto médio $M(X_m, Y_m)$ de um segmento com extremidades $A(x_1, y_1)$ e $B(x_2, y_2)$ são dadas pela média aritmética das respectivas coordenadas:<br>$$X_m = \\frac{x_1 + x_2}{2} = \\frac{2 + 4}{2} = \\frac{6}{2} = 3$$<br>$$Y_m = \\frac{y_1 + y_2}{2} = \\frac{3 + (-5)}{2} = \\frac{-2}{2} = -1$$<br>Portanto, o ponto médio é $M(3, -1)$.<br>A alternativa correta é a <strong>Letra A</strong>."
        },
        {
            "q": "Uma profissional desenvolveu um método de tranças em que o número de tranças se comporta como uma sequência aritmética com base no volume de cabelo: para volume 1 são 12 tranças, para volume 2 são 15 tranças, para volume 3 são 18 tranças. Se uma pessoa tiver volume de cabelo 8 na escala, qual o número máximo de tranças que é possível fazer?",
            "options": ["33", "38", "36", "43"],
            "correct": 0,
            "explanation": "A quantidade de tranças forma uma Progressão Aritmética (PA) onde:<br>- Primeiro termo: $a_1 = 12$<br>- Razão: $r = 15 - 12 = 3$<br><br>Aplicando a fórmula do termo geral da PA para $n = 8$:<br>$$a_n = a_1 + (n - 1) \\cdot r$$<br>$$a_8 = 12 + (8 - 1) \\cdot 3 = 12 + 7 \\cdot 3 = 12 + 21 = 33\\text{ tranças}.$$Portanto, a alternativa correta é a <strong>Letra A</strong>."
        },
        {
            "q": "Um grupo de amigos deseja alugar uma quadra de futebol de areia por 4 horas. O valor normal é de R$ 40,00 a hora. Pelo aplicativo, há uma promoção: na 2ª hora há um desconto de 5% sobre o valor da 1ª hora, e da 3ª hora em diante há um desconto de 10% sobre o valor da 1ª hora para cada hora. Qual será o valor total pago pelo grupo se contratarem pelo aplicativo?",
            "options": ["R$ 148,00", "R$ 150,00", "R$ 154,00", "R$ 160,00"],
            "correct": 1,
            "explanation": "Vamos calcular o custo de cada uma das 4 horas:<br>1. 1ª hora: $\\text{R\\$ } 40{,}00$<br>2. 2ª hora (desconto de 5% sobre R$ 40,00): $40{,}00 - 0{,}05 \\times 40{,}00 = 40{,}00 - 2{,}00 = \\text{R\\$ } 38{,}00$<br>3. 3ª hora (desconto de 10% sobre R$ 40,00): $40{,}00 - 0{,}10 \\times 40{,}00 = 40{,}00 - 4{,}00 = \\text{R\\$ } 36{,}00$<br>4. 4ª hora (desconto de 10% sobre R$ 40,00): $40{,}00 - 4{,}00 = \\text{R\\$ } 36{,}00$<br><br>Somando os valores das 4 horas:<br>$$\\text{Total} = 40{,}00 + 38{,}00 + 36{,}00 + 36{,}00 = \\text{R\\$ } 150{,}00.$$Portanto, a alternativa correta é a <strong>Letra B</strong>."
        },
        {
            "q": "Segundo dados do Censo Demográfico do IBGE divulgados em uma notícia sobre o Oeste Paulista, cinco cidades registraram as seguintes perdas populacionais entre 2010 e 2022: Irapuru perdeu 1.851 habitantes, Euclides da Cunha Paulista perdeu 1.661, Flora Rica perdeu 265, Santo Anastácio perdeu 2.512 e Rosana perdeu 2.251 habitantes. Com base nesses dados, a média de habitantes perdidos por esses cinco municípios é de:",
            "options": [
                "Ao todo, os cinco municípios perderam 17.331 habitantes.",
                "Entre os cinco municípios, aquele com maior queda percentual perdeu a maior quantidade absoluta de habitantes.",
                "Na região, o resultado 'a cidade encolheu' pode ser considerado como a mediana dos dados.",
                "Os cinco municípios da notícia perderam, em média, 1.708 habitantes cada."
            ],
            "correct": 3,
            "explanation": "Calculamos a soma das perdas absolutas de habitantes nos 5 municípios citados:<br>$$\\text{Soma} = 1.851 + 1.661 + 265 + 2.512 + 2.251 = 8.540\\text{ habitantes}$$<br>Calculamos a média aritmética dividindo pelo número de municípios (5):<br>$$\\text{Média} = \\frac{8.540}{5} = 1.708\\text{ habitantes por município}.$$Portanto, a afirmação correta é a da <strong>Letra D</strong>."
        },
        {
            "q": "Analise as afirmações sobre semelhança de triângulos:<br>[ ] Toda reta paralela a um dos lados do triângulo, que intercepta os outros dois lados, determina um segundo triângulo que não é semelhante ao primeiro.<br>[ ] Dizemos que dois triângulos são semelhantes se dois lados são proporcionais e os ângulos entre esses lados são congruentes.<br>[ ] Dois triângulos que possuem apenas dois ângulos correspondentes congruentes não podem ser considerados semelhantes.<br>[ ] O quociente comum entre as medidas dos lados correspondentes é chamado de razão de semelhança entre dois triângulos.<br>A sequência correta de Verdadeiro (V) ou Falso (F), de cima para baixo, é:",
            "options": ["V - V - F - F", "V - F - V - F", "F - V - F - V", "F - F - V - V"],
            "correct": 2,
            "explanation": "Analisando cada proposição:<br>1. [ F ] Pelo Teorema Fundamental da Semelhança, toda reta paralela a um dos lados interceptando os outros dois forma um triângulo que É semelhante ao original.<br>2. [ V ] Corresponde ao caso LAL (Lado-Ângulo-Lado) de semelhança de triângulos.<br>3. [ F ] Pelo caso AA (Ângulo-Ângulo), se dois triângulos possuem dois ângulos congruentes, eles já são garantidamente semelhantes (pois o terceiro ângulo também será congruente).<br>4. [ V ] Por definição, o quociente entre as medidas de lados homólogos é a razão de semelhança $k$.<br>A sequência obtida é F - V - F - V.<br>Portanto, a alternativa correta é a <strong>Letra C</strong>."
        },
        {
            "q": "Um computador demora 6 minutos e 20 segundos para fazer o download de um arquivo de $1\\text{ GB}$. Mantendo essa mesma velocidade de transferência constante, quanto tempo esse computador levará para baixar um arquivo de $2{,}2\\text{ GB}$?",
            "options": [
                "13 minutos e 56 segundos.",
                "13 minutos e 20 segundos.",
                "12 minutos e 40 segundos.",
                "14 minutos e 04 segundos."
            ],
            "correct": 0,
            "explanation": "1. Convertemos o tempo para segundos:<br>$$6\\text{ min e } 20\\text{ s} = 6 \\times 60 + 20 = 360 + 20 = 380\\text{ segundos}$$<br>2. Como o tamanho do arquivo e o tempo são grandezas diretamente proporcionais:<br>$$t = 380 \\times 2{,}2 = 836\\text{ segundos}$$<br>3. Convertendo de volta para minutos e segundos:<br>$$836 \\div 60 = 13\\text{ minutos e resto } 56\\text{ segundos}$$<br>Logo, o tempo total é de 13 minutos e 56 segundos.<br>Portanto, a alternativa correta é a <strong>Letra A</strong>."
        },
        {
            "q": "Um professor pesquisou a quantidade de livros lidos por 40 alunos no ano anterior:<br>0 livros: 2 alunos | 1 livro: 4 alunos | 2 livros: 7 alunos | 3 livros: 7 alunos | 4 livros: 10 alunos | 5 livros: 7 alunos | 6 livros: 3 alunos.<br>Sendo $Y$ e $Z$, respectivamente, a mediana e a moda da quantidade de livros lidos, o valor de $Y + Z$ é igual a:",
            "options": ["7,0", "7,5", "10", "10,5"],
            "correct": 1,
            "explanation": "1. Moda ($Z$): é o valor com maior frequência absoluta. A maior quantidade de alunos é $10$ (que leram $4$ livros). Logo:<br>$$Z = 4$$<br>2. Mediana ($Y$): como o total de alunos é $N = 40$ (número par), a mediana é a média entre o 20º e o 21º termos na lista ordenada.<br>Calculando as frequências acumuladas:<br>- Até 0 livros: 2 alunos (posições 1 a 2)<br>- Até 1 livro: 2 + 4 = 6 alunos (posições 3 a 6)<br>- Até 2 livros: 6 + 7 = 13 alunos (posições 7 a 13)<br>- Até 3 livros: 13 + 7 = 20 alunos (posições 14 a 20) $\\implies$ 20º aluno leu 3 livros.<br>- Até 4 livros: 20 + 10 = 30 alunos (posições 21 a 30) $\\implies$ 21º aluno leu 4 livros.<br>Logo, a mediana é:<br>$$Y = \\frac{3 + 4}{2} = 3{,}5$$<br>3. Calculando $Y + Z$:<br>$$Y + Z = 3{,}5 + 4 = 7{,}5.$$Portanto, a alternativa correta é a <strong>Letra B</strong>."
        },
        {
            "q": "Seguindo os passos de um fluxograma: 'Considere uma variável $n$; eleve $n$ ao quadrado; encontre o triplo do resultado; acrescente $3/2$; chame a expressão de $T_n$'. Qual das alternativas apresenta 3 termos consecutivos da sequência gerada ao atribuir $n = 1, 2, 3, 4, \\dots$?",
            "options": [
                "$\\frac{3}{2}, \\frac{9}{2}, \\frac{27}{2}$",
                "$\\frac{9}{2}, \\frac{18}{2}, \\frac{27}{2}$",
                "$\\frac{27}{2}, \\frac{57}{2}, \\frac{99}{2}$",
                "$\\frac{9}{2}, \\frac{57}{2}, \\frac{153}{2}$"
            ],
            "correct": 2,
            "explanation": "A expressão algébrica definida pelo fluxograma é:<br>$$T_n = 3n^2 + \\frac{3}{2} = \\frac{6n^2 + 3}{2}$$<br>Calculando os termos sucessivos para valores inteiros de $n$:<br>- Para $n = 1$: $T_1 = 3(1)^2 + 1{,}5 = 4{,}5 = \\frac{9}{2}$<br>- Para $n = 2$: $T_2 = 3(4) + 1{,}5 = 12 + 1{,}5 = 13{,}5 = \\frac{27}{2}$<br>- Para $n = 3$: $T_3 = 3(9) + 1{,}5 = 27 + 1{,}5 = 28{,}5 = \\frac{57}{2}$<br>- Para $n = 4$: $T_4 = 3(16) + 1{,}5 = 48 + 1{,}5 = 49{,}5 = \\frac{99}{2}$<br><br>Observamos que os termos $T_2, T_3, T_4$ formam a sequência consecutiva $\\frac{27}{2}, \\frac{57}{2}, \\frac{99}{2}$.<br>Portanto, a alternativa correta é a <strong>Letra C</strong>."
        },
        {
            "q": "Qual é a sequência lógica de passos para a construção com régua e compasso de um triângulo equilátero $ABC$ a partir de um segmento $AB$ sobre uma reta suporte?",
            "options": [
                "Construir a reta suporte com a régua; determinar o segmento AB; traçar duas circunferências com raio qualquer centradas em A e B; encontrar a interseção C; traçar AC e BC.",
                "Construir a reta suporte; determinar o segmento AB; traçar duas circunferências com raio maior que AB centradas em A e B; encontrar a interseção C; traçar AC e BC.",
                "Construir a reta suporte; determinar o segmento AB; traçar duas circunferências com raio menor que AB centradas em A e B; encontrar a interseção C; traçar AC e BC.",
                "Construir a reta suporte r com a régua. Sobre a reta r, determinar o segmento AB. Traçar, com o compasso, uma circunferência de centro A e raio AB. Traçar outra circunferência com centro em B e raio AB. Encontrar o ponto de interseção C entre essas circunferências. Com a régua, traçar os segmentos AC e BC."
            ],
            "correct": 3,
            "explanation": "Para que o triângulo $ABC$ seja equilátero, é indispensável que todas as distâncias sejam iguais, isto é, $AC = BC = AB$.<br>Para garantir isso com o compasso, a ponta-seca deve ser posicionada em $A$ com abertura exatamente igual a $AB$ (gerando todos os pontos a distância $AB$ de $A$), e em seguida em $B$ com abertura igual a $AB$. O ponto de interseção $C$ satisfará simultaneamente $AC = AB$ e $BC = AB$.<br>Portanto, a alternativa correta é a <strong>Letra D</strong>."
        },
        {
            "q": "Ao comprar um terreno retangular com dimensões de $30\\text{ m}$ por $20\\text{ m}$, a nova proprietária pretende fazer um jardim semicircular com $5\\%$ da área total do terreno. Adotando $\\pi = 3$, calcule a medida do raio $R$ a ser utilizado para o desenho do jardim.",
            "options": ["$5\\sqrt{2}\\text{ m}$", "$2\\sqrt{5}\\text{ m}$", "$\\sqrt{60}\\text{ m}$", "$\\sqrt{180}\\text{ m}$"],
            "correct": 1,
            "explanation": "1. Área total do terreno retangular:<br>$$A_{\\text{terreno}} = 30 \\times 20 = 600\\text{ m}^2$$<br>2. A área do jardim semicircular corresponde a $5\\%$ dessa área:<br>$$A_{\\text{jardim}} = 0{,}05 \\times 600 = 30\\text{ m}^2$$<br>3. A fórmula da área de um semicírculo de raio $R$ é $A = \\frac{\\pi R^2}{2}$. Substituindo com $\\pi = 3$:<br>$$\\frac{3 \\cdot R^2}{2} = 30 \\implies 3R^2 = 60 \\implies R^2 = 20$$<br>4. Extraindo a raiz quadrada e simplificando o radical:<br>$$R = \\sqrt{20} = \\sqrt{4 \\times 5} = 2\\sqrt{5}\\text{ metros}.$$Portanto, a alternativa correta é a <strong>Letra B</strong>."
        }
    ]
}

data = {
    "EXAM_2025_1_A": EXAM_2025_1_A,
    "EXAM_2025_1_B": EXAM_2025_1_B
}

with open("scripts/data_ifsp/exams_2025.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Saved scripts/data_ifsp/exams_2025.json successfully!")
