# Relocate heavy trees onto the working SSD

This Mini: volume `/Volumes/Trabalho` (Acasis TBU405AIR + KC3000 1 TB, rear TB4 40 Gb/s).

## rsync (macOS)

`/usr/bin/rsync` is openrsync 2.6.9. Do **not** pass `--info=progress2`.

```bash
rsync -aH --progress --extended-attributes "$SRC/" "$DST/"
mv "$SRC" "$SRC.bak-interno"
ln -s "$DST" "$SRC"
# verify via the symlink, then rm -rf "$SRC.bak-interno"
```

`--extended-attributes` when the source is ExFAT (WD Elements) — expect `._*` AppleDouble and `+x` on files; `chmod -R a-x,u+rwX,go+rX` on the dest if an app chokes.

## What already lives on Trabalho

| Home path | Dest |
|---|---|
| `~/.lmstudio/models` | `Models/lmstudio` |
| `~/.cache` | `Cache/home-cache` |
| `~/Library/pnpm` | `Cache/pnpm` |
| `~/.npm` | `Cache/npm` |
| `~/.ollama/models` | `Models/ollama` |

Do **not** move `~/Apps` (launchd + fixed ports) or `~/.hermes`.

## Ollama

Models may be on Elements (`/Volumes/Elements/models`) even when `OLLAMA_MODELS=~/.ollama/models` — the home dir is often leftover stubs (~220 KB).

1. Quit Ollama (`osascript -e 'quit app "Ollama"'`) so `ollama serve` is not holding the dir.
2. Copy Elements → `/Volumes/Trabalho/Models/ollama` (blob count must match).
3. Swap `~/.ollama/models` for a symlink.
4. Confirm `curl -m 8 http://127.0.0.1:11434/api/tags` lists the local models.
5. Only then delete `/Volumes/Elements/models`.

If the GUI serve hangs after “cloud disabled” with 0% CPU, start once with `OLLAMA_NO_CLOUD=1` against the real path to prove the trees; the hang was seen when swapping the dir under a live serve.

## Docker.raw (sparse)

`~/Library/Containers/com.docker.docker/Data/vms/0/data/Docker.raw`

- Apparent size ~228 GB, `du` ~9 GB. APFS `SEEK_HOLE` does **not** report those holes.
- **Broken:** `rsync -S`, `dd conv=sparse`, Python `SEEK_DATA` — dest balloons toward 100–200 GB.
- **Works:** read 1 MiB, write only non-zero 4 KiB pages, `truncate` dest to the apparent size. Expect dest `du` ≈ source `du`.
- **Broken:** `ln -s` over the original path. `com.docker.virtualization --disk …/Docker.raw` never reaches “VM has started”; engine `_ping` 500s.
- Relocate only after **Quit Docker** from the menu. Settings key (in the backend, not applied in the 2026-08-31 session): `"DiskPath": "/Volumes/Trabalho/Docker/Docker.raw"` in `~/Library/Group Containers/group.com.docker/settings-store.json`. Keep `Docker.raw.bak-interno` until `docker info` works.

## Time Machine vs Elements

Elements is **one ExFAT volume**. Disk Utility cannot shrink ExFAT to add APFS. In-place convert wipes it.

Safe path: copy archive onto Trabalho (check free space: used-on-Elements < free-on-Trabalho) → `eraseDisk` / partition GPT APFS (volume Arquivo + volume Time Machine) → copy archive back → `tmutil` to the TM volume. Never TM onto Trabalho.