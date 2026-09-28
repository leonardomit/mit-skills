# macOS APFS Filesystem Deadlock — quando a planilha não abre

**Sintoma:** Ao tentar ler um `.xlsx` (ou `.numbers`) com `openpyxl`, `numbers_parser`, ou mesmo `cat`/`xxd`/`file`, recebe `OSError: [Errno 11] Resource deadlock avoided`. O `lsof` no caminho retorna vazio (nenhum user-process segura o arquivo).

**Causa:** Camada VFS do APFS segurando o I/O — geralmente durante Time Machine backup pesado, iCloud sync (`cloudd`) indexando a pasta, ou Spotlight (`mds_stores`) reindexando após mudança de volume. Não é lock de user-process, é contenção no kernel.

## Diagnóstico (em ordem)

```bash
# 1. Confirma que NÃO é lock de user-process
lsof "/caminho/arquivo.xlsx"
# se vazio → não é lock de app

# 2. Confirma que o VFS está travado
file "/caminho/arquivo.xlsx"
# esperado: "Resource deadlock avoided"

# 3. Tenta ler bytes brutos
xxd "/caminho/arquivo.xlsx" | head -3
# esperado: "Resource deadlock avoided"

# 4. Tenta Python raw open
python3 -c "open('/caminho/arquivo.xlsx', 'rb').read(16)"
# esperado: OSError [Errno 11]

# Se os 4 confirmam → é deadlock APFS, não corrupção
```

## Workarounds que NÃO funcionam

| Tentativa | Resultado |
|---|---|
| `killall Finder` | ❌ Finder reinicia mas FS continua travado |
| `killall mds_stores` (sem sudo) | ❌ mds roda como root |
| `killall cloudd` (sem sudo) | ❌ cloudd roda como root |
| `pkill -f FinderSyncExtension` | ❌ só tira ícone do Google Drive |
| `mv arquivo.xlsx arquivo2.xlsx` | ⚠️ Metadata lê mas conteúdo continua travado |
| Aguardar 5–10 min | ⚠️ Às vezes funciona, às vezes não |

## Workaround que funciona SEM reiniciar (jun/2026 — confirmado)

**Abrir cada arquivo `.xlsx` no Numbers força o VFS a rehidratar os data blocks.** Depois disso, openpyxl volta a ler normalmente. Sintoma observado: o arquivo abre OK no Numbers (sem erro de "arquivo corrompido"), e na sequência a leitura Python volta a funcionar — o que prova que não era corrupção do zip, era contenção VFS que o app GUI conseguiu furar via path diferente de leitura.

```bash
# Abrir todos os arquivos travados de uma vez
open -a Numbers "/Users/usuario/Documents/Obsidian Vault/empresa/relatorio-a.xlsx"
open -a Numbers "/Users/usuario/Documents/Obsidian Vault/empresa/relatorios-b2b/_relatorio-b.xlsx"
open -a Numbers "/Users/usuario/Documents/Obsidian Vault/empresa/relatorios-b2b/relatorio-c_ PRODUTOS POR MÊS.xlsx"
open -a Numbers "/Users/usuario/Documents/Obsidian Vault/empresa/relatorios-b2c/relatorio-d_ PRODUTOS POR MÊS.xlsx"

# Aguardar 10-15s para os apps terminarem o load, depois testar:
python3 -c "import openpyxl; wb=openpyxl.load_workbook('...arquivo.xlsx...', data_only=True); print(wb.sheetnames)"
```

**Por que funciona:** Numbers usa APIs diferentes de I/O (`NSFileCoordinator`, leitura via File Manager do AppKit) que conseguem negociar handles com o VFS de um jeito que `open(2)` direto do Python não consegue.

**Quando NÃO funciona:** se o Numbers também reclamar que o arquivo está corrompido, aí é corrupção real do zip (não contenção VFS) — nesse caso, só restaurar do backup.

## Workaround que sempre funciona (último recurso)

**Reiniciar o Mac.** Resolve 100% dos casos de contenção VFS pura. Não é exagero — deadlock APFS no nível do VFS não tem unlock de user-space e nenhum app consegue destravar.

**Ordem de tentativa sugerida (do menos disruptivo ao mais):**
1. Abrir no Numbers (resolve na maioria dos casos)
2. Aguardar 15-20min (Time Machine / cloudd passam sozinhos às vezes)
3. Reiniciar o Mac

## Caso real (2026-06-26 — empresa) — UPDATED

Sessão de sync travou em 4 arquivos `.xlsx` simultaneamente no path `~/Documents/Obsidian Vault/empresa/`:

1. `relatorio-a.xlsx`
2. `_relatorio-b.xlsx`
3. `relatorio-c_ PRODUTOS POR MÊS.xlsx`
4. `relatorio-d_ PRODUTOS POR MÊS.xlsx`

Dry-run OK em 2 dos 4 (B2B Mensal + relatorio-c) — depois apply travou em todos. `killall Finder` não resolveu. Reinício do Mac também NÃO resolveu — todos os 4 continuaram travados pós-boot.

**Solução que funcionou:** `open -a Numbers` em cada arquivo, esperar 15s, e os 4 voltaram a ser lidos pelo openpyxl. Sync então rodou sem erros: 1.323 células aplicadas em 5,9s.

**Lições atualizadas:**
- Reinício do Mac NÃO é 100% — em jun/2026 falhou para resolver contenção VFS persistente
- Dry-run OK não garante apply OK — contenção VFS pode aparecer entre as duas execuções
- `open -a Numbers` é a primeira coisa a tentar, antes de perder 5-10min com reboot
- **Manter os arquivos `.xlsx` abertos no Numbers durante a sessão de sync** reduz chance de o problema voltar (o handle já está negociado)