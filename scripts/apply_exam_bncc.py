
import json, re

with open('scripts/bncc_catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

with open('mathData_augmented.json', 'r', encoding='utf-8') as f:
    math_data = json.load(f)

def determine_bncc(q):
    text = q.get('q', '').lower()
    expl = q.get('explanation', '').lower()
    opts = ' '.join(q.get('options', [])).lower()
    combined = f'{text} {expl} {opts}'
    
    # 1. Trigonometria no triângulo retângulo
    if any(k in combined for k in ['seno', 'cosseno', 'tangente', '\sin', '\cos', '\tan', 'cateto oposto', 'cateto adjacente', 'sen(', 'cos(', 'tg(']):
        return 'EF09MA14'

    # 2. Teorema de Tales
    if any(k in combined for k in ['teorema de tales', 'feixe de retas paralelas', 'feixe de paralelas', 'retas paralelas r, s, t']):
        return 'EF09MA11'

    # 3. Semelhança de triângulos e polígonos
    if any(k in combined for k in ['semelhança de triângulos', 'triângulos semelhantes', 'razão de semelhança', 'polígonos semelhantes']):
        return 'EF09MA12'

    # 4. Teorema de Pitágoras e Direções Perpendiculares
    if any(k in combined for k in ['pitágoras', 'pitagoras', 'hipotenusa']):
        return 'EF09MA13'
    if 'triângulo retângulo' in combined and any(k in combined for k in ['cateto', 'catetos']):
        return 'EF09MA13'
    if any(k in combined for k in ['direções perpendiculares', 'trajeto perpendicular', 'linha reta entre os navios']):
        return 'EF09MA13'

    # 5. Geometria Analítica: Distância no Plano Cartesiano / Retas
    if any(k in combined for k in ['plano cartesiano', 'par ordenado', 'abscissa', 'ordenada', 'coordenadas do ponto', 'distância entre as retas', 'retas perpendiculares']):
        return 'EF09MA16'

    # 6. Círculo, Circunferência e Rodas
    if any(k in combined for k in ['circunferência', 'comprimento da circunferência', 'raio da circunferência', 'diâmetro da circunferência', 'corda da circunferência', 'arco da circunferência', 'setor circular']):
        return 'EF08MA16'
    if any(k in combined for k in ['roda gigante', 'pneu', 'raio do círculo', 'área do círculo']) or ('raio' in combined and '\pi' in combined) or ('diâmetro' in combined and '\pi' in combined):
        return 'EF08MA16'

    # 7. Geometria Espacial: Volume, Capacidade e Sólidos
    if any(k in combined for k in ['metro cúbico', 'metros cúbicos', 'm^3', 'cm^3', 'dm^3', 'litros', 'capacidade do reservatório', 'capacidade da caixa', 'capacidade em litros']):
        if any(k in combined for k in ['cilindro', 'cone', 'esfera', 'pirâmide', 'prisma', 'caixa', 'reservatório', 'aquário', 'piscina', 'volume', 'litro']):
            return 'EF08MA17'
    if any(k in combined for k in ['volume do prisma', 'volume do cilindro', 'volume do paralelepípedo', 'volume do cubo', 'volume da caixa', 'volume total', 'capacidade máxima', 'volume de um açude', 'minecraft']):
        return 'EF08MA17'
    if any(k in combined for k in ['volume do cone', 'volume da esfera', 'volume da pirâmide', 'área da superfície']):
        return 'EF09MA18'
    if any(k in combined for k in ['vista superior', 'vista frontal', 'vista lateral', 'vistas ortogonais']):
        return 'EF06MA20'
    if any(k in combined for k in ['poliedro', 'vértices, faces', 'relação de euler', 'planificação', 'dados de seis faces', 'faces opostas']):
        return 'EF06MA16'

    # 8. Variação Proporcional de Dimensões Geométricas
    if any(k in combined for k in ['duplicarmos o diâmetro', 'duplicar o raio', 'triplicar as arestas', 'se duplicarmos', 'se reduzirmos a']):
        return 'EF09MA19'

    # 9. Áreas de Figuras Planas
    if any(k in combined for k in ['área do triângulo', 'área do quadrado', 'área do retângulo', 'área do trapézio', 'área do losango', 'área da figura', 'área sombreada', 'área hachurada', 'área de lazer', 'área total', 'metros quadrados', 'hectares']) or re.search(r'\d+\s*(m\^2|cm\^2)', combined):
        if not any(k in combined for k in ['volume', 'litros', 'capacidade']):
            return 'EF07MA25'

    # 10. Perímetro
    if 'perímetro' in combined or 'perimetro' in combined:
        return 'EF06MA29'

    # 11. Polígonos e Ângulos
    if any(k in combined for k in ['soma dos ângulos internos', 'ângulo interno', 'ângulo externo', 'diagonais de um polígono', 'polígono regular', 'hexágono regular', 'pentágono regular', 'octógono', 'decágono', 'icoságono']):
        return 'EF08MA13'
    if any(k in combined for k in ['opostos pelo vértice', 'ângulos complementares', 'ângulos suplementares', 'bissetriz do ângulo', 'ângulos adjacentes', 'retas paralelas ( \parallel s$)']):
        return 'EF07MA22'
    if any(k in combined for k in ['triângulo isósceles', 'triângulo equilátero', 'condição de existência de um triângulo']) or ('soma dos ângulos' in combined and 'triângulo' in combined):
        return 'EF07MA23'
    if any(k in combined for k in ['paralelogramo', 'losango', 'trapézio']) and not 'área' in combined:
        return 'EF07MA24'

    # 12. Conjuntos e Diagrama de Venn
    if any(k in combined for k in ['diagrama de venn', 'n(a \cup b)', 'gostam de a', 'gostam de b', 'apenas a', 'apenas b', 'não gostam de nenhum', 'não praticam nenhum', 'lêem o jornal', 'conjuntos {', '{x, y} =', 'interseção de conjuntos', 'união de conjuntos', 'subconjunto', 'conjunto  =']):
        return 'EF09MA01'

    # 13. Sistemas de Equações do 1º Grau
    if any(k in combined for k in ['sistema de equações', 'sistema linear', 'sistema:', 'duas incógnitas', 'truffas a r$', 'pães de mel', 'duas opções de compra']):
        return 'EF08MA08'
    if any(k in combined for k in ['galinhas e vacas', 'patos e coelhos', 'cabeças e', 'notas de r$', 'cédulas de', 'moedas de', 'toalhas (médias e grandes)', 'em dois reservatórios que abastecem', 'foram vendidos 240 ingressos']):
        return 'EF08MA09'
    if re.search(r'[a-z]\s*[\+\-]\s*[a-z]\s*=\s*\d+', combined) and re.search(r'\d+[a-z]\s*[\+\-]\s*\d+[a-z]\s*=\s*\d+', combined):
        return 'EF08MA08'

    # 14. Sequências e Padrões Numéricos
    if any(k in combined for k in ['número de tranças', 'castelo com cartas', 'sequência', 'progressão', 'termo da sequência', 'termo geral']):
        return 'EF08MA06'

    # 15. Regra de Três Composta e Divisão Proporcional
    if any(k in combined for k in ['regra de três composta', 'regra de tres composta', 'máquinas trabalhando', 'produzem 900 peças em 4 horas', 'fabricando gelo trabalhando 9 horas por dia', 'em partes proporcionais', 'dividindo o número 684 em três partes', 'partes a, b e c']):
        return 'EF09MA05'

    # 16. Funções (Afim e Quadrática)
    if any(k in combined for k in ['vértice da parábola', 'ponto de máximo', 'ponto de mínimo', 'gráfico da função', 'função afim', 'função quadrática', 'função do 1º grau', 'função do 2º grau', 'f(x) =', 'p(x) =', 'v(x) =', 'taxa fixa de', 'salário mensal composto por uma parte fixa', 'a cada dia o valor final a']):
        return 'EF09MA08'

    # 17. Equações do 2º Grau
    if any(k in combined for k in ['bhaskara', 'baskara', 'equação do 2º grau', 'equação do segundo grau', 'equação quadrática', 'discriminante', 'raízes da equação', 'raízes reais', 'equação x^2']):
        return 'EF09MA06'
    if re.search(r'[a-z]\^2\s*[\+\-]\s*\d+', combined) and any(k in combined for k in ['solução', 'raízes', 'equação', 'determine']):
        return 'EF09MA06'

    # 18. Produtos Notáveis e Fatoração
    if any(k in combined for k in ['produtos notáveis', 'fatoração', 'fatorar', 'diferença de quadrados', 'trinômio quadrado perfeito', 'simplificando a expressão algébrica', 'expressão algébrica', 'polinômio', 'resto da divisão de']):
        return 'EF09MA09'

    # 19. Combinatória e Contagem
    if any(k in combined for k in ['quantos números pares', 'algarismos distintos', 'quantas maneiras', 'de quantas formas', 'anagramas', 'princípio fundamental da contagem', 'combinações possíveis', 'modos diferentes', 'jogam todos entre si', 'campeonato de voleibol, cada equipe jogou']):
        return 'EF08MA25'

    # 20. Probabilidade
    if any(k in combined for k in ['probabilidade', 'chances de', 'espaço amostral', 'ao acaso', 'sorteado']):
        return 'EF07MA28'

    # 21. Estatística
    if any(k in combined for k in ['moda', 'mediana']):
        return 'EF08MA22'
    if any(k in combined for k in ['média aritmética', 'média ponderada', 'media aritmetica', 'media ponderada', 'média das idades', 'média das notas', 'média salarial', 'média das temperaturas', 'média de']):
        return 'EF07MA36'
    if any(k in combined for k in ['gráfico de setores', 'gráfico de colunas', 'gráfico de barras', 'histograma', 'gráfico de linhas', 'tabela a seguir apresenta os dados']):
        return 'EF08MA23'

    # 22. Porcentagem e Juros
    if any(k in combined for k in ['juros compostos', 'rendimento composto', 'capitalização composta']):
        return 'EF09MA04'
    if any(k in combined for k in ['juros simples', 'taxa de juros', 'capital investido', 'rendimento mensal']):
        return 'EF08MA04'
    if any(k in combined for k in ['porcentagem', 'percentual', '% de aumento', '% de desconto', '% a mais', '% a menos', 'lucro de', 'desconto de', 'aumento de']) or '%' in text:
        return 'EF08MA04'

    # 23. Notação Científica, Potências e Radicais
    if any(k in combined for k in ['notação científica', 'notacao cientifica', 'ordem de grandeza', '10^']):
        return 'EF08MA01'
    if any(k in combined for k in ['expoente fracionário', 'racionalização de denominadores', 'simplificação de radicais', 'propriedades dos radicais', '4^{\frac{3}{2}}']):
        return 'EF09MA02'
    if any(k in combined for k in ['potenciação', 'potência', 'elevado a', '20^{100}', 'base 10', '12^4', 'expressão numérica (-3)^2']):
        return 'EF08MA01'
    if any(k in combined for k in ['raiz quadrada', 'raízes quadradas', '\sqrt']):
        return 'EF08MA02'

    # 24. Razão, Proporção e Escala
    if any(k in combined for k in ['escala de 1:', 'escala 1:', 'em um mapa na escala', 'velocidade média', 'velocidade constante de 60', 'densidade demográfica', 'km/h']):
        return 'EF07MA18'
    if any(k in combined for k in ['regra de três', 'regra de tres', 'diretamente proporcional', 'inversamente proporcional', 'razão e proporção', 'consome 4 litros de gasolina a cada 48 km', 'taxa de contágio indicava que 20 pessoas', 'trabalhadores realizam um serviço em 9 dias']):
        return 'EF07MA13'

    # 25. MMC e MDC
    if any(k in combined for k in ['mmc', 'mínimo múltiplo comum', 'voltarão a se encontrar', 'coincidirão', 'ao mesmo tempo novamente']):
        return 'EF06MA05'
    if any(k in combined for k in ['mdc', 'máximo divisor comum', 'maior tamanho possível sem sobras', 'divididos em partes iguais de maior tamanho']):
        return 'EF06MA05'
    if any(k in combined for k in ['número primo', 'números primos', 'divisibilidade', 'critério de divisibilidade', 'múltiplo de', 'divisível por']):
        return 'EF06MA04'

    # 26. Frações e Dízimas
    if any(k in combined for k in ['dízima periódica', 'fração geratriz']):
        return 'EF08MA03'
    if any(k in combined for k in ['fração irredutível', 'frações equivalentes', 'simplificação da fração']):
        return 'EF06MA07'
    if any(k in combined for k in ['fração', 'fracionária', 'do tanque', 'do total', 'restante', 'gastou', 'metade', 'um terço', 'dois quintos']):
        return 'EF06MA08'

    # 27. Medidas e Conversões
    if any(k in combined for k in ['duração da', 'iniciou às', 'terminou às', 'h min', 'quilogramas', 'toneladas', 'conversão de unidades', 'metros de comprimento', 'centímetros', 'minutos e 20 segundos', 'download de um arquivo', '1 dia = 24 h']):
        return 'EF06MA24'

    # 28. Inequações
    if any(k in combined for k in ['inequação', 'maior que zero', 'menor que zero', 'conjunto solução da inequação']):
        return 'EF07MA16'

    # 29. Sistema de numeração / Inteiros
    if any(k in combined for k in ['algarismo das unidades', 'algarismo da dezena', 'número de 4 algarismos', 'sistema de numeração']):
        return 'EF06MA01'
    if any(k in combined for k in ['expressão numérica', 'operações fundamentais', 'resolvendo a expressão']):
        return 'EF07MA03'

    # 30. Equações do 1º Grau
    if any(k in combined for k in ['equação do 1º grau', 'equação do primeiro grau', 'determine o valor de x', 'valor numérico de x', 'valor de x', 'satisfaz a equação', 'raiz da equação', 'valor de']):
        return 'EF07MA14'

    # Fallback contextual
    return 'EF07MA14'

tagged_count = 0
for b_id in ['5', '6', '7']:
    for t in math_data[b_id]['topics']:
        for q in t['questions']:
            code = determine_bncc(q)
            info = catalog[code]
            q['bncc'] = code
            q['bnccDesc'] = info['desc']
            q['unidadeTematica'] = info['unidade']
            q['anoEscolar'] = info['ano']
            q['topicoId'] = info['topicoId']
            tagged_count += 1

# Make sure blocks 1 to 4 questions do NOT have these fields
for b_id in ['1', '2', '3', '4']:
    for t in math_data[b_id]['topics']:
        for q in t['questions']:
            for k in ['bncc', 'bnccDesc', 'unidadeTematica', 'anoEscolar', 'topicoId']:
                if k in q:
                    del q[k]

with open('mathData_augmented.json', 'w', encoding='utf-8') as f:
    json.dump(math_data, f, indent=2, ensure_ascii=False)

print(f'Successfully updated mathData_augmented.json with {tagged_count} tagged exam questions!')
