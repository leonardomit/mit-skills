---
name: markitdown-to-md
description: Converte PDF, DOCX, PPTX e XLSX para Markdown com o MarkItDown antes de ler o conteúdo, para economizar tokens de contexto. Use esta skill sempre que o usuário enviar ou referenciar um arquivo .pdf, .docx, .pptx ou .xlsx e pedir para ler, resumir, analisar, extrair informações, revisar ou responder perguntas sobre ele — mesmo que o usuário não mencione "markitdown", "converter" ou "markdown" explicitamente. Não usar para .txt, .md, .csv ou .html, que já são texto puro e não se beneficiam da conversão.
---

# MarkItDown → Markdown antes de ler

## Por quê

PDF, DOCX, PPTX e XLSX são formatos binários/XML verbosos. Ler esses arquivos
diretamente (ex: via ferramentas de PDF que renderizam página como imagem, ou
extração bruta de XML) consome muito mais tokens do que precisa. O
[MarkItDown](https://github.com/microsoft/markitdown) da Microsoft extrai o
conteúdo relevante (texto, tabelas, estrutura de headings) e devolve Markdown
limpo e compacto — mesma informação, uma fração dos tokens.

## Quando usar

Sempre que o usuário enviar ou apontar para um arquivo `.pdf`, `.docx`,
`.pptx` ou `.xlsx` **e** pedir para fazer algo que exige ler o conteúdo
(resumir, analisar, extrair dados, responder perguntas, revisar, comparar
etc.). Não é necessário que o usuário peça a conversão explicitamente — a
conversão é um passo interno antes da leitura, não um pedido separado.

Não usar para arquivos que já são texto puro (`.txt`, `.md`, `.csv`, `.html`)
— a conversão não ajuda nesses casos e é só overhead.

## Passo a passo

1. **Localize o arquivo** de origem (geralmente em um diretório de uploads).

2. **Rode o script de conversão** em vez de ler o arquivo original direto:

   ```bash
   python3 <caminho-desta-skill>/scripts/convert_to_md.py "<caminho_do_arquivo>"
   ```

   - Em sucesso, o script imprime no stdout o caminho do `.md` gerado (mesmo
     diretório do original, com `.md` anexado ao nome completo — ex.:
     `relatorio.docx` vira `relatorio.docx.md` — para não colidir com outro
     arquivo de mesmo nome-base e extensão diferente).
   - Em falha, imprime `CONVERSION_FAILED: <motivo>` em stderr e sai com
     código 1.

3. **Se a conversão funcionar**, use a ferramenta `Read` no arquivo `.md`
   gerado — não no arquivo original. Esse `.md` é o que você deve usar para
   toda a análise/resumo pedida pelo usuário.

4. **Se falhar por dependência ausente** (mensagem menciona
   `MissingDependencyException` ou `pip install markitdown[...]`), instale a
   dependência uma vez e tente de novo:

   ```bash
   pip install --break-system-packages "markitdown[all]"
   python3 <caminho-desta-skill>/scripts/convert_to_md.py "<caminho_do_arquivo>"
   ```

5. **Se falhar por qualquer outro motivo** (arquivo corrompido, PDF
   escaneado sem texto extraível, etc.), não trave o fluxo: caia de volta
   para ler o arquivo original com as ferramentas normais (Read, ou a skill
   de `pdf`/`docx`/`pptx`/`xlsx` apropriada, se o pedido exigir manipulação
   e não só leitura) e avise brevemente que a conversão não foi possível.

## Limitações a ter em mente

- O MarkItDown extrai texto e estrutura, mas **perde formatação visual fina**
  (cores, fontes, layout exato). Se o usuário precisar editar ou manipular o
  arquivo original (não só ler), use a skill de formato apropriada (`docx`,
  `pptx`, `xlsx`, `pdf`) sobre o arquivo original — o `.md` é só para
  leitura/análise.
- Em PDFs escaneados (imagem sem camada de texto), o MarkItDown pode retornar
  pouco ou nenhum conteúdo. Nesse caso caia para a skill `pdf` (que tem rota
  de OCR) em vez de insistir na conversão.
- Tabelas grandes em XLSX viram tabelas Markdown — ainda mais compacto que
  ler célula por célula, mas para planilhas muito grandes considere se o
  pedido do usuário não exige antes um recorte (ex: só algumas abas/colunas)
  via a skill `xlsx`.
