---
name: local-llm-runtimes
description: "Use when sharing Ollama GGUFs with LM Studio."
version: 1.0.0
---

# Local LLM runtimes (Ollama + LM Studio + Hermes)

Use when the user wants one copy of a model on disk used by more than one runtime, or to add Ollama / LM Studio as a Hermes provider.

## Layout on this machine

| Runtime | User path | Real store |
|---------|-----------|------------|
| Ollama | `~/.ollama/models` | `/Volumes/Trabalho/Models/ollama` (`blobs/` + `manifests/`) |
| LM Studio | `~/.lmstudio/models` | `/Volumes/Trabalho/Models/lmstudio` |
| Hermes providers | `hermes config get providers` | `ollama-launch` → `:11434/v1`; `lmstudio` → `:1234/v1` |

Ollama **cloud** tags (`*:cloud`) have no `application/vnd.ollama.image.model` layer — skip them.

Same family name is not the same file. Example: LMS Hub `google/gemma-4-e4b` Q4_K_M (~5 GB + separate mmproj) ≠ Ollama `gemma4:e4b` (~9.6 GB, vision+audio tensors in one GGUF).

## Share Ollama weights with LM Studio (no extra GB)

Ollama blobs with magic `GGUF` are already llama.cpp files. Both stores sit on the same APFS volume (`/Volumes/Trabalho`), so **hard links** share inodes.

1. Map each local tag → model blob via `manifests/registry.ollama.ai/library/<name>/<tag>` layer `application/vnd.ollama.image.model` → `blobs/sha256-<hex>`.
2. Confirm `file` magic is `GGUF` and `df` shows the same filesystem for blob and `~/.lmstudio/models`.
3. Stage a **named** `.gguf` hard link **on that same volume** (not `/tmp` — `EXDEV` / errno 18).
4. Import without copying:

```bash
lms import -y --hard-link --user-repo <user>/<repo> /Volumes/Trabalho/Models/_stage/<name>.gguf
```

5. Delete only the staging directory entries. `stat` nlink on blob and LMS path should stay ≥ 2.
6. Confirm files with `find ~/.lmstudio/models -name '*.gguf'`, not `lms ls` alone.

**Never** run `lms import` without `--hard-link`, `--symbolic-link`, or `--copy`. Default **moves** the source — that would steal Ollama's blob.

CLI: `~/.lmstudio/bin/lms`.

## Wire LM Studio into Hermes

Do **not** patch `~/.hermes/config.yaml` (tool block). Use:

```bash
hermes config set providers.lmstudio.api 'http://127.0.0.1:1234/v1'
hermes config set providers.lmstudio.name 'LM Studio'
hermes config set providers.lmstudio.default_model 'google/gemma-4-e4b'
hermes config set providers.lmstudio.models '["google/gemma-4-e4b"]'
```

Do not change `model.default` unless asked. Gateway sessions need `/restart` before `/model lmstudio/...` sees the provider.

OpenAI-compatible ports seen here: **1234** (llama runtime, `*:1234`) and **1235** (`http-server-config.json`, app). Hermes uses **1234**. Server must be on and a model loaded (or JIT) before chat works.

## Pitfalls

- Hard-link staging on `/tmp` or the boot volume fails across devices. Stage under `/Volumes/Trabalho/Models/`.
- `du` after hard-link looks like LMS “grew” and Ollama “shrank”; inodes are shared — do not delete one side thinking it is a duplicate download.
- `lms ls` / Hub index can lag files on disk. Disk + `nlink` are source of truth.
- M4 16 GB: skip loading 27B-class GGUFs as default.

## Related

- `llama-cpp` — Hub GGUF discovery and llama-server, not Ollama/LMS sharing.
- Machine-specific import map: [references/trabalho-model-store.md](references/trabalho-model-store.md)
