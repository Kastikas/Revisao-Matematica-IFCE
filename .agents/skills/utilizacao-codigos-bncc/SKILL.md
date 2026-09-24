---
name: utilizacao-codigos-bncc
description: >-
  Utilize esta skill sempre que analisar, resolver, revisar ou catalogar questões de matemática no PartiuIF.
  Define o método obrigatório de decomposição passo a passo, identificando para cada passo os descritores
  da BNCC mobilizados, fundamentados no catálogo oficial (scripts/bncc_catalog.json) e no documento oficial
  BNCC Matemática.pdf.
---

# Skill: Utilização dos Códigos da BNCC e Resolução Passo a Passo

Esta skill normatiza o processo de análise, resolução e auditoria pedagógica de questões de processos seletivos e vestibulares técnicos (IFCE, IFSC, IFSP, IFMG, etc.). Toda resolução deve evidenciar com clareza **o encadeamento lógico de passos matemáticos** e **as habilidades da BNCC mobilizadas em cada um desses passos**.

---

## 1. Fonte Canônica de Habilidades e Termos Diretos

1. **Documento Base Oficial:** [`BNCC Matemática.pdf`](file:///home/ivanlrk/Projetos/revisao-site-ifce/BNCC%20Matemática.pdf) — Contém as 247 habilidades do Ensino Fundamental (1º ao 9º ano: `EF01MA01` a `EF09MA23`).
2. **Catálogo Estruturado do Projeto:** [`scripts/bncc_catalog.json`](file:///home/ivanlrk/Projetos/revisao-site-ifce/scripts/bncc_catalog.json).
   - Cada habilidade possui uma **noção direta** (`nocao`), que sintetiza em poucos termos objetivos o cerne conceitual do código, eliminando ambiguidades burocráticas.
   - Cada habilidade inclui `palavras_chave` para busca indexada rápida.

---

## 2. Metodologia Obrigatória de Resolução Passo a Passo

Ao resolver qualquer questão com o usuário ou ao auditar itens existentes, o agente **não deve** apresentar apenas a resposta pronta ou um bloco monolítico de equações. A resolução deve ser decomposta em etapas discretas, mapeando as habilidades envolvidas.

### Formato de Apresentação da Análise de Questão:

```markdown
### Questão [Número] — [Título / Instituição / Ano]
**Enunciado Oficial:** "[Texto literal com KaTeX padronizado]"
**Alternativas:** A) ... | B) ... | C) ... | D) ...
**Gabarito Oficial:** [Letra]

#### Decomposição do Raciocínio e Mapeamento BNCC:
- **Passo 1: Interpretação e Modelagem Inicial**
  - *Ação Matemática:* [O que é feito neste passo]
  - *Descritor BNCC Mobilizado:* `[CÓDIGO]` — **[Noção Direta]** (ex.: `EF04MA15` — Propriedades da igualdade e determinação de valor desconhecido).
  - *Fundamentação:* [Por que esta habilidade se aplica aqui].

- **Passo 2: Deduções Matemáticas / Transformações Algébricas**
  - *Ação Matemática:* [Dedução de fórmulas, relações ou simplificações]
  - *Descritor BNCC Mobilizado:* `[CÓDIGO]` — **[Noção Direta]**.

- **Passo 3: Operações Aritméticas / Resolução Operatória**
  - *Ação Matemática:* [Cálculo numérico, fração, equação, geometria]
  - *Descritor BNCC Mobilizado:* `[CÓDIGO]` — **[Noção Direta]**.

- **Passo 4: Conclusão e Equivalência com as Alternativas**
  - *Ação Matemática:* [Associação do valor encontrado à alternativa correta do gabarito oficial].

#### Classificação Curricular no PartiuIF:
- **Habilidade Focal (Principal):** `[CÓDIGO]` (alimenta o campo `bncc` no `mathData.json`)
- **Unidade Temática:** [Números | Álgebra | Geometria | Grandezas e medidas | Probabilidade e estatística]
- **Ano Escolar:** [1º ano a 9º ano]
- **Tópico Plataforma:** `[bX-tY]`
- **Habilidades Acessórias:** `[CÓDIGO_1]`, `[CÓDIGO_2]` (habilidades operatórias de suporte usadas nos passos intermediários).
```

---

## 3. Distinção: Habilidade Focal vs. Habilidades Acessórias

- **Habilidade Focal:** É a competência central avaliada pelo item. Responde à pergunta: *"Qual conceito matemático o examinador pretendeu testar nesta questão?"*. Esta é a habilidade que deve ser salva nos metadados da questão no `mathData.json` (`bncc`, `bnccDesc`, `unidadeTematica`, `anoEscolar`, `topicoId`).
- **Habilidades Acessórias:** São os saberes instrumentais prévios ou operatórios requeridos durante a execução (ex.: somar números naturais `EF01MA06`/`EF06MA03`, converter unidades de medida `EF06MA24`). Devem ser explicitadas na análise passo a passo para demonstrar a progressão pedagógica.

---

## 4. Exemplos Canônicos de Aplicação

### Exemplo 1: Prova IFCE 2025.2 — Questão 1 (Original 31)
* **Enunciado:** *"Sejam $x$ e $y$ números tais que os conjuntos $\{3, 5, 8\}$ e $\{x, y, 8\}$ são iguais. É correto afirmar que:"*
* **Alternativas:** A) $x = 8$ e $y = 5$ | B) $x + y = 8$ | C) $x = 3$ e $y = 8$ | D) $x = y$
* **Gabarito Oficial:** **B** ($x + y = 8$)

#### Decomposição e BNCC por Passo:
1. **Passo 1 (Modelagem da Igualdade de Conjuntos):**
   - *Ação:* Estabelecer que $\{3, 5, 8\} = \{x, y, 8\} \implies \{x, y\} = \{3, 5\}$. Os valores $x$ e $y$ são desconhecidos/indeterminados individualmente.
   - *BNCC Mobilizada:* `EF04MA15` — **Propriedades da igualdade e determinação de valor desconhecido**.
2. **Passo 2 (Operação Fundamental e Invariância Aditiva):**
   - *Ação:* Aplicar a operação fundamental de adição sobre os termos desconhecidos: $x + y = 3 + 5 = 8$, tornando a sentença $x + y = 8$ invariavelmente verdadeira.
   - *BNCC Mobilizada:* `EF04MA15` (focal) e `EF01MA06` / `EF02MA05` (fatos básicos da adição).
3. **Passo 3 (Verificação de Falsidade das Alternativas):**
   - *Ação:* Analisar as outras alternativas: $x=8$ é falso pois $8$ já está pareado; $x=y$ viola a cardinalidade do conjunto de 3 elementos.
- **Classificação Final:** Habilidade Focal: `EF04MA15` | Unidade: Álgebra | Ano: 4º ano | Tópico: `b2-t1`.

---

### Exemplo 2: Prova IFCE 2025.2 — Questão 3 (Original 33)
* **Enunciado:** *"Se $\overline{abcd}$ é o menor número de quatro algarismos divisível por $23$, então a soma $a + b + c + d$ vale:"*
* **Alternativas:** A) $1$ | B) $3$ | C) $2$ | D) $4$
* **Gabarito Oficial:** **D** ($4$)

#### Decomposição e BNCC por Passo:
1. **Passo 1 (Sistema de Numeração e Menor Número de 4 Algarismos):**
   - *Ação:* Reconhecer que o menor número positivo de 4 algarismos no sistema decimal é $1000$.
   - *BNCC Mobilizada:* `EF06MA02` — **Sistema de numeração decimal: base, ordens e valor posicional**.
2. **Passo 2 (Divisibilidade e Múltiplos):**
   - *Ação:* Efetuar $1000 \div 23 = 43{,}478\dots$ e determinar o primeiro múltiplo inteiro de 4 algarismos: $23 \times 44 = 1012$.
   - *BNCC Mobilizada:* `EF06MA05` — **Números primos, divisores, múltiplos e critérios de divisibilidade**.
3. **Passo 3 (Decomposição Posicional dos Algarismos):**
   - *Ação:* Decompor $1012$ em seus algarismos: $a=1, b=0, c=1, d=2$.
   - *BNCC Mobilizada:* `EF06MA02` (valor posicional e algarismos).
4. **Passo 4 (Soma dos Algarismos e Seleção do Gabarito):**
   - *Ação:* Somar os algarismos: $1 + 0 + 1 + 2 = 4$, correspondendo estritamente à alternativa D.
   - *BNCC Mobilizada:* `EF06MA03` (operações fundamentais).
- **Classificação Final:** Habilidade Focal: `EF06MA05` | Unidade: Números | Ano: 6º ano | Tópico: `b1-t3`.

---

## 5. Regras de Consulta ao Catálogo

1. Ao classificar ou resolver, busque primeiro no [`scripts/bncc_catalog.json`](file:///home/ivanlrk/Projetos/revisao-site-ifce/scripts/bncc_catalog.json) pelo campo `palavras_chave` ou pelo texto da `nocao`.
2. Verifique sempre o alinhamento com a Unidade Temática e o ano de progressão curricular.
3. Se um conceito exigir ancoragem em anos iniciais (1º ao 5º ano), utilize os códigos correspondentes (`EF01` a `EF05`) que agora constam integralmente no catálogo oficial do projeto.
