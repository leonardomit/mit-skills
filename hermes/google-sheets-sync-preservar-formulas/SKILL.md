---
name: google-sheets-sync-preservar-formulas
description: Atualiza Google Sheets a partir de planilhas-fonte locais preservando fórmulas de Total/Média. Use quando precisar sincronizar dados onde o destino tem fórmulas tipo =SUM(C7:N7) ou =AVERAGEIF(...) que precisam continuar funcionando.
---

# Google Sheets Sync — Preservar Fórmulas

## Quando usar

Sincronizar dados de planilhas-fonte locais (.xlsx, .numbers, .csv) com Google Sheets onde:
- O destino tem **fórmulas de Total/Média** que precisam continuar funcionando (=SUM, =AVERAGEIF)
- A fonte tem apenas os **valores mensais** (sem total)
- Você quer sobrescrever fonte → destino (estratégia "fonte sempre vence")

## O bug crítico a evitar

**NUNCA escreva strings formatadas como `"R$ 35.591,69"` em células que vão ser somadas por fórmulas.**

Por quê: a fórmula `=SUM(C7:N7)` no destino retorna **0** quando os operandos são texto. Strings de moeda "R$ 1.234,56" não são somadas — apenas números. O Sheets vai mostrar `R$ 0,00` no Total e seu dado está corrompido silenciosamente.

## Padrão correto

1. **Detectar se a região tem fórmulas** via Sheets API v4 com `valueRenderOption='FORMULA'` (cache por aba/região para performance).
2. **Se tem fórmula**: enviar **valores numéricos** (`35591.69`, não `"R$ 35.591,69"`) — a formatação visual (BRL currency) já está aplicada nas células via `userEnteredFormat.numberFormat` e o Sheets exibe corretamente.
3. **Se NÃO tem fórmula**: pode enviar string formatada.

## Snippet essencial

```python
from googleapiclient.discovery import build

def _tem_formula(service, sheet_id, aba, range_a1):
    r = service.spreadsheets().values().get(
        spreadsheetId=sheet_id,
        range=f'{aba}!{range_a1}',
        valueRenderOption='FORMULA'
    ).execute()
    for row in r.get('values', []):
        for cell in row:
            if cell and str(cell).startswith('='):
                return True
    return False

def _parse_numero(val):
    """'R$ 35.591,69' -> 35591.69; '15,0%' -> 0.15; '1.540' -> 1540."""
    if isinstance(val, (int, float)):
        return float(val)
    if not isinstance(val, str):
        return None
    s = val.strip()
    if s.endswith('%'):
        try: return float(s[:-1].replace(',', '.')) / 100
        except: return None
    s = s.replace('R$', '').replace(' ', '')
    if ',' in s and s.count(',') == 1:
        try: return float(s.replace('.', '').replace(',', '.'))
        except: return None
    try: return float(s)
    except: return None
```

## Referências

- **`references/macos-fs-deadlock.md`** — sintoma `Resource deadlock avoided [Errno 11]` em `openpyxl`/`file`/`xxd` no macOS. Diagnóstico + ordem de workarounds (`open -a Numbers` → aguardar → reiniciar). **Consultar PRIMEIRO quando o dry-run ou apply travar.**

## Outras lições aprendidas

- **Backup antes de qualquer escrita**: exportar via `https://docs.google.com/spreadsheets/d/{ID}/export?format=xlsx` com `google.auth.transport.requests.Request` (NÃO `requests.Request()` que não tem `.refresh()`).
- **`USER_ENTERED` vs `RAW`**: use `USER_ENTERED` para que fórmulas sejam interpretadas. Para sobrescrever valor sem interpretar fórmula, use `RAW`.
- **Chunks**: Sheets API aceita até 50000 cells por request, mas chunks de 500 evitam timeouts.
- **Confirmação interativa**: quando > 50 mudanças, peça confirmação. Capture `EOFError` para suportar execução sem TTY (cron, CI) — nesse caso, abortar ou exigir `--yes`.
- **Match de produtos por nome normalizado**: `uppercase + strip + collapse whitespace` resolve 99% dos casos. Para 1% residual, listar como warning.
- **Auto-detectar formato de fonte**: usar extensão do arquivo (`.xlsx`, `.numbers`, `.xls`) para escolher leitor (`openpyxl`, `numbers_parser`, `xlrd`).

## Workflow recomendado

1. **DRY-RUN primeiro**: `--dry-run` mostra contagem + amostra + warnings de itens não pareados.
2. **Aplicar**: `--yes` para auto-confirmar (use só após revisar dry-run).
3. **Validar**: ler 2-3 linhas via API com `FORMATTED_VALUE` para conferir visualmente, e checar que fórmulas de Total recalcularam (ex: Total = soma dos meses).

## Handling missing rows (`--add-missing`)

When source files contain indicators/products/clients absent from the destination Google Sheet:

- **B2B Mensal clients**: Several "unmatched" entries are actually KPI summary headers (`CLIENTES ATIVOS`, `FATURAMENTO B2B (R$)`, `Nº DE PEDIDOS`, `TICKET MÉDIO (R$)`) that already live in the KPI section. Do **not** append them as client rows.
- **Products (B2B / B2C)**: These are legitimate missing rows. When `--add-missing` is passed, append them at the end of the product list, writing numeric monthly values in columns C–N and the Total formula `=SUM(C{row}:N{row})` in column O (so existing Total formulas continue to work).

The script now accepts `--add-missing` (added 2026-07-14). Implementation of the append logic lives in `atualizar_kpi.py` (the concrete runner for this skill).

**Pitfall**: Never append summary/total rows as data rows — they break the "cliente" / "produto" section boundaries and corrupt downstream formulas.

## Comandos úteis

```bash
# Simular sem alterar
python3 script.py --dry-run

# Aplicar tudo (com confirmação)
python3 script.py

# Aplicar tudo (sem confirmação)
python3 script.py --yes

# Aplicar só uma aba
python3 script.py --only comercial --yes

# Adicionar linhas novas que existem na fonte mas não no destino
python3 script.py --add-missing --yes
```


## Dependências

- `openpyxl` (xlsx reader)
- `numbers_parser` (numbers reader)
- `gspread` + `google-auth` (Sheets write)
- `google-api-python-client` (Sheets API para detectar fórmulas)
- `requests` (backup export)
