---
name: "criacao-de-marca-e-manual"
description: "Cria ou revisa a identidade de uma marca: entrevista de voz e posicionamento, paleta, tipografia, logo, kit de marca (.md), manual da marca (Paper/HTML), design system com tokens, papelaria e kit web. Use quando pedirem \"criar marca\", \"kit de marca\", \"manual da marca\", \"brand book\", \"guia de voz\", \"design system da marca\", \"identidade visual\", \"papelaria\", ou para evoluir o logo/cores/fontes de uma marca existente."
---

# Criação de Marca e Manual da Marca

Método destilado de dois manuais reais: **Marca Alfa** (marca de empresa de um setor regulado, documentos de qualidade em .docx) e **mitsuo.io** (marca pessoal/portfólio — sites e apps, design system web com tema claro/escuro). Os dois seguem a mesma espinha: *entrevista → crítica → fundamento e voz → sistema visual → logo → entregáveis → checklist*.

Idioma padrão: português do Brasil. Seja direto. Em decisões de marca, ative o modo crítico: aponte a premissa mais fraca antes de validar.

---

## Fase 1 — Entrevista (antes de criar qualquer coisa)

Use AskUserQuestion em **3 rodadas de até 4 perguntas**, com opções concretas (e "Other" livre). Não pule para o visual antes de fechar a voz.

**Rodada 1 — Negócio e público**
- Qual negócio/marca? (empresa, marca pessoal, produto)
- Quem é o público prioritário? (multiselect: consumidor, B2B/revenda, profissionais, parceiros…)
- Que frase você mais quer ouvir de um cliente? ("entendem do assunto" / "resolvem rápido" / "se importam" / "são diferentes")
- Como você fala hoje no dia a dia? (informal / cordial-profissional / técnico quando precisa / espelha o cliente)

**Rodada 2 — Voz e valores**
- Onde está a diferença **de verdade hoje**? (produto, rigor, relação, "ainda construindo")
- O que a marca **nunca** diz? (multiselect: promessa milagrosa, urgência falsa, hype/gíria, jargão inacessível)
- Que bandeira defende mesmo quando custa venda?
- Personalidade: sóbria / calorosa / ousada / vibrante

**Rodada 3 — Visual e uso**
- Situação do logo: não tem / tem e quer evoluir / tem e mantém → **peça o arquivo (SVG de preferência)**
- Território visual (4 opções nomeadas e descritas, ex.: "natural sofisticado", "clínico moderno", "brasileiro contemporâneo", "papel e tinta editorial")
- Tratamento: "você" / "a gente" / neutro
- Canais principais (multiselect: social, WhatsApp/vendas, site, embalagem, documentos internos, apps)

Registre as respostas na memória do usuário/projeto antes de seguir.

---

## Fase 2 — Crítica (obrigatória)

Antes de escrever o kit, confronte as respostas:
- **Aspiração × realidade.** Se o diferencial é "ainda construindo", a marca **não pode afirmar superioridade** ("o melhor", "único"). A diferença declarável vira *postura* (honestidade, proximidade, rigor). Escreva isso como regra interna.
- **Setor regulado.** Saúde, suplementos, alimentos, finanças: as proibições de voz precisam espelhar a regulação (ex.: alegações fora da lista Anvisa).
- **Logo × território.** Se o logo existente conflita com a paleta escolhida (ex.: verde vibrante vs território terroso), ofereça 3 caminhos: *kit segue o logo* / *logo migra* / *híbrido* — e diga que meio-termo dilui. Deixe o usuário decidir.
- **Fontes.** Antes de prometer uma fonte, verifique disponibilidade (Google Fonts / instalada / ferramenta de design). Fonte paga (ex.: Codec Pro) quase nunca está disponível: proponha alternativa gratuita equivalente e registre a original como "pode substituir se instalada".

---

## Fase 3 — Fundamento e voz

**Fundamento**
- O que a marca é (1 frase) e **posicionamento em uma frase**.
- Públicos em ordem de tom.
- **Três princípios / "três ideias guiam tudo"** — curtos, com nome em negrito + 1 frase (mitsuo: "Assinatura, não decoração" / "Papel e tinta" / "Feito para usar"; Marca Alfa: "Simples e direto" / "Um toque de cor" / "Clareza antes de estilo").
- Bandeiras + nota estratégica interna (o que ainda não pode ser dito).

**Voz**
- Personalidade em uma linha ("Calorosa e próxima, com competência por trás").
- Tom base (4 bullets) e **ajuste por canal** (tabela canal → ajuste).
- **Assim, sim** (3 exemplos reais de frase) × **Nunca** (lista de proibições, com exemplos entre aspas).
- **Palavras: preferir × evitar** (tabela).
- Regras de escrita mecânicas quando houver interface/web (do mitsuo.io): pessoa do verbo, caixa de frase em títulos, formato de etiqueta (ex.: `PROJETO · 2026` em CAIXA ALTA mono com ponto médio), grafia fixa do nome ("sempre mitsuo.io, minúsculas, com o ponto"), sem emoji na interface.

---

## Fase 4 — Sistema visual

### Cor
- 5–7 cores com **nome próprio** (Azul Base, Areia, washi, sumi, shu…), hex e **papel semântico**: fundo, superfície, texto, texto secundário, marca, acento, linha/borda, foco, estados (info/sucesso/erro).
- Para web/app, defina **claro e escuro** por token (padrão mitsuo: tabela Nome | Claro | Escuro; a cor-assinatura não muda entre temas).
- **Proporção declarada** (60/30/10 na Marca Alfa; ~80/15/≤5 no mitsuo). A cor mais forte é rara de propósito.
- **Calcule o contraste WCAG** de cada combinação texto/fundo e registre: cor de marca com contraste < 4,5:1 **não** vai em texto pequeno — crie um token separado para texto (ex.: `shu-text`) ou restrinja a títulos ≥ 24px.
- Estados sempre carregam palavra/ícone além da cor.
- Branco puro e preto puro só com motivo; prefira fundo tingido (Areia, washi) e texto grafite/sumi.

### Tipografia
- Display + texto (+ mono se houver código/etiquetas). Máximo 2 famílias por peça (3 se mono for funcional).
- Escala nomeada (display-xl, display-l, title, heading, body-lg, body, body-strong, small, label, code) com tamanho/peso.
- Regras: tracking levemente negativo em títulos grandes; corpo mínimo 15–16px em tela; um display-xl por página; 60–75 caracteres por linha.

### Espaço, forma, linhas, movimento, ícones
- Espaço em múltiplos de 4 (space-1…space-n), gutters mobile/desktop.
- Raios nomeados (sm/md/lg/pill) e onde cada um vai. O mitsuo deriva os cantos do próprio selo — **derive a forma do logo** quando possível.
- Decida **bordas ou sombras** (mitsuo: bordas finas no lugar de sombras; Marca Alfa: sombras tingidas da cor estrutural, nunca preto). Foco visível obrigatório.
- Movimento mínimo (150ms ease-out), respeitar `prefers-reduced-motion`.
- Iconografia: traço, espessura, grade, família recomendada (ex.: Lucide 1.5px, currentColor). Sem emoji.

---

## Fase 5 — Logo

**Se existe logo:** avalie antes de propor redesign. Padrão recomendado: *evolução, não redesign* — manter formas, ajustar cor ao sistema, completar versões.

**Versões obrigatórias:** principal (cor), negativa, monocromática, símbolo/selo isolado, favicon/selo compacto (sem detalhes finos, para < 48px), wordmark sozinho quando fizer sentido.

**Regras a documentar:** área de proteção (em função de um elemento do logo), tamanho mínimo (tela e impresso), sobre quais fundos cada versão vai, e "não faça" (distorcer, recolorir, sombra/gradiente, fundo ruidoso, redesenhar letras). Liste pontos de atenção de leitura (ex.: "a folha sobre o o pode ser lida como acento").

**Técnico (SVG):**
- Recolorir trocando o `fill` no SVG; gere PNGs com ImageMagick (`convert -background none -density 300 x.svg -trim x.png`).
- **Ao extrair o SVG para `<symbol>`/inline, preserve `fill-rule:evenodd; clip-rule:evenodd`** do `<svg>` raiz — sem isso os furos (miolo do "a", "o") ficam fechados.
- Verifique cada versão renderizada antes de usar.

---

## Fase 6 — Entregáveis

Crie na ordem; o **.md é a fonte da verdade**, os demais derivam dele.

1. **Kit de marca (`kit-marca-<marca>.md`)** — seções: 1 Fundamento · 2 Voz · 3 Identidade visual (território, paleta, tipografia, logo) · 4 Checklist de aprovação. Data de "Última atualização" no topo e "(Atualizado AAAA-MM-DD)" em cada mudança.

2. **Manual da marca visual** — no Paper (se conectado) ou HTML autocontido. Pranchas 1440×900: Capa · Posicionamento · Voz · Cores · Tipografia · Logo · Checklist · Papelaria (cartão, timbrado, envelope, assinatura de e-mail). Crie os tokens no arquivo (cores, fontes, tamanhos, espaço, raio) e use `var(--token)` em tudo, para que trocar uma cor/fonte propague sozinho.

3. **Design system** — quando a sessão oferecer o tipo de artifact *Design System*, use-o com as seções do mitsuo: Overview (manual em texto) · Colors (claro/escuro) · Typography · Spacing · Corner radius · Shadows · Border · Components · Assets (conjuntos "Logos" e "Aplicações", cada um com README). Sem esse tipo: HTML persistido com paleta clicável e contraste calculado, escala tipográfica, espaço/raio/sombra, logo e não-faça, componentes (botões, selos de status, caixas de destaque, formulário, card, tabela, cabeçalho de documento), voz, checklist e **tokens exportáveis** (CSS, JSON e formato da ferramenta de documentos). Fontes: embuta woff2 em base64 (pacotes `@fontsource/<família>` via `npm pack`) porque o artifact não carrega Google Fonts.

4. **Papelaria** — cartão 90×50 mm (frente clara, verso marcante), timbrado A4, envelope DL 220×110 mm (frente discreta, aba com a marca), assinatura de e-mail (símbolo + fio + nome/cargo/contato; fallback Arial/Helvetica).

5. **Kit web/app** (marcas digitais) — `og-default.png` 1200×630, `avatar-400.png`, `icon-512.png`, `apple-touch-icon.png`, `favicon.svg`/`.ico`, e o snippet `<link rel="icon"…>`/`og:image` pronto para colar.

6. **Modelos .docx** (marcas com documentação) — papel timbrado e modelo-base gerados por script (docx-js), não à mão. Atenções:
   - **Google Docs quebra imagens flutuantes** (faixas de rodapé ancoradas na página): use imagem em linha.
   - O .docx só aparece com as fontes da marca se estiverem instaladas; avise o usuário.
   - Ao regerar documentos existentes a partir de .md: guarde backup zipado dos antigos, **compare o texto** (cobertura de n-gramas .md→novo e antigo→.md), preserve textos escritos à mão no Word (ex.: resumos da folha de rosto) e confira que o filtro de "cabeçalho duplicado" não apagou conteúdo real.

7. **Checklist de aprovação** (fecha o kit e o manual) — 6–8 itens sim/não: regulação/alegações, sem milagre, sem urgência falsa, voz (ler em voz alta: conversa ou anúncio?), honestidade (fiscal + especialista + cliente cético achariam correto?), visual só com tokens, clareza em 5 segundos. "Reprovou em um item, volta e ajusta."

---

## Regras de conduta

- **Nunca invente dados de contato** (telefone, endereço, CNPJ). Procure nos arquivos do usuário; se não achar, use placeholder visível (ex.: `(51) 0000-0000`) e liste o que falta no fechamento. Se fontes divergirem, pergunte qual vale.
- Mudanças de cor/fonte: atualize **todos** os lugares de uma vez — tokens do manual, kit .md, design system, assets PNG renderizados com o fundo antigo, e a ferramenta de documentos.
- Não gere arquivos que o usuário não pediu; ofereça. Respeite regras de publicação da pasta de destino (repositório, portal) e diga o que ficou pendente.
- Verifique visualmente cada entregável (screenshot do Paper, render PDF do .docx, preview do HTML) antes de dar por concluído.
- No fechamento, liste as decisões que ainda dependem do usuário (ex.: teste de leitura do logo, aprovação de nova cor de alerta).

---

## Referência rápida — os dois casos

| | Marca Alfa | mitsuo.io |
|---|---|---|
| Tipo | Empresa, setor regulado | Marca pessoal / portfólio web |
| Ideia central | "Produto sério, explicado com honestidade" | Selo **hanko** como assinatura de autor |
| Princípios | Simples e direto · Um toque de cor · Clareza antes de estilo | Assinatura, não decoração · Papel e tinta · Feito para usar |
| Paleta | Azul Base #2E6B9E, Azul Profundo #16324A, Amarelo Acento #F2B705, Azul Névoa #E3EDF4, Areia #EFECE5, Grafite #2B2926 — 60/30/10 | washi #F6F1E7 / sumi #1E1A16 / shu #C8381E (+ ai, kincha, hairline, focus), claro e escuro — ~80/15/≤5 |
| Tipografia | Fonte display + fonte de texto (Google Fonts) | Shippori Mincho B1 (display) + Zen Kaku Gothic New (texto) + JetBrains Mono (label/código) |
| Forma | Raios 8/16/28, sombras tingidas da cor de marca | Raios derivados do selo, bordas finas no lugar de sombras |
| Entregáveis extras | Papelaria completa, modelos .docx, checklist regulatório | Kit web (og, avatar, ícones, favicon) + snippet HTML, componentes (Button, ProjectCard, Seal, SiteHeader, Tag) |

