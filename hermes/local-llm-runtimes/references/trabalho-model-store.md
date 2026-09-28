# Trabalho model store (this Mac)

Volume: `/Volumes/Trabalho` (Kingston). Do not stage hard links on `/tmp` or the boot disk.

## Ollama blobs that are GGUF (local only)

Skip `*:cloud`. Deduplicate by blob digest (`gemma4:latest` == `gemma4:e4b`; `qwen3.5:latest` == `qwen3.5:9b`).

| Tag | Size | file_type (GGUF) | Notes |
|-----|------|------------------|-------|
| `gemma4:e4b` | 9.61 GB | 15 Q4_K_M | Vision+audio in-file; not LMS Hub 5 GB Q4 |
| `gemma4:e2b` | 7.16 GB | 15 Q4_K_M | |
| `hermes3:latest` | 4.66 GB | 2 Q4_0 | Hermes 3 Llama 3.1 8B |
| `qwen3.6:27b-q4_K_M` | 17.42 GB | 15 Q4_K_M | Too large as M4 16 GB default |
| `llama3.2:3b` | 2.02 GB | 15 Q4_K_M | |
| `qwen3.5:9b` | 6.59 GB | 15 Q4_K_M | |
| `qwen3.5:2b` | 2.74 GB | 7 Q8_0 | |
| `nomic-embed-text:latest` | 0.27 GB | F16 | LMS already has a smaller Q4 Hub copy — skip unless asked |

Import target keys used:

```
ollama/gemma4-e4b
ollama/gemma4-e2b
nousresearch/hermes-3-llama-3.1-8b
ollama/qwen3.6-27b-q4_k_m
ollama/llama-3.2-3b-instruct
ollama/qwen3.5-9b
ollama/qwen3.5-2b
```

LMS Hub (separate files, already downloaded): `google/gemma-4-e4b` + `mmproj-gemma-4-E4B-it-BF16.gguf`, `text-embedding-nomic-embed-text-v1.5`.

## Hermes

Provider `lmstudio` is already in `config.yaml` via `hermes config set` (api `http://127.0.0.1:1234/v1`, default `google/gemma-4-e4b`). Default chat model remains Grok unless the user switches.
