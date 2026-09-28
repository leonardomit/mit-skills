# After-install recipes (this Mini)

Volume: `/Volumes/Trabalho` — Acasis TBU405AIR on rear TB4 @ 40 Gb/s + Kingston KC3000 1 TB `SKC3000S/1024G`, APFS GPT.

## Relocate with copy + symlink

```bash
rsync -aH --extended-attributes SRC/ DEST/   # not --info=progress2 (openrsync)
mv SRC SRC.bak-interno
ln -s DEST SRC
# verify du -shL SRC, then rm -rf SRC.bak-interno
```

Typical targets: `~/.cache`, `~/.npm`, `~/Library/pnpm`, `~/.lmstudio/models`, `~/.ollama/models`.

Do **not** move `~/Apps` (launchd + fixed paths) or `~/.hermes`.

## Sparse Docker.raw (cross-volume)

`du` = allocated; `ls -lh` = virtual. Copy only non-zero 4 KiB pages:

```python
# src/dst paths; truncate dst to src size; read 1 MiB, write non-zero 4k pages
zeros = b"\x00" * 4096
```

Then:

```
quit Docker
mkdir -p /Volumes/Trabalho/Docker/vms/0/data
# place Docker.raw there
mv ~/Library/Containers/com.docker.docker/Data/vms \
   ~/Library/Containers/com.docker.docker/Data/vms.bak-interno
ln -s /Volumes/Trabalho/Docker/vms \
  ~/Library/Containers/com.docker.docker/Data/vms
open -a Docker
# docker info && docker ps  — then delete vms.bak-interno
```

File symlink of `Docker.raw` = VM stuck. `DiskPath` in `settings-store.json` = unknown setting.

## ExFAT → APFS archive copy

Walk top-level dirs; skip `$RECYCLE.BIN`, `.Spotlight-V100`, `.Trashes`, `.fseventsd`, `System Volume Information`, `._*`. On `ENOENT`/`OSError`, log and continue (dead iCloud placeholders inside old backups). Resume if dest size already matches. Do not erase the WD until `du` of the staging tree is in the same ballpark as `df` used on Elements (expect some skip).

TM: erase WD as one APFS container, two volumes sharing space (`Arquivo` + `Time Machine`). Never TM on Trabalho.
