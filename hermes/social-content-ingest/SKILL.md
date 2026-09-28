---
name: social-content-ingest
description: >-
  Use when user shares Instagram/X/YouTube/Reddit/web URLs to read or
  extract tips/tools/functions. Agent-Reach doctor + public yt-dlp/Jina
  first; OpenCLI only after extension connected.
---

# Social Content Ingest

Class of work: **turn a social/web URL into a usable brief** (thesis, tips, metadata) for Leonardo — research, implementable ideas, or creative refs — without defaulting to “install essay” when content can already be fetched.

## When to use

- User pastes Instagram Reel/post, X link, YouTube, Reddit, Bilibili, GitHub repo, article URL
- “Analisa esse post”, “o que ele ensina”, “salva como ideia/função/dica”
- Multi-platform lookup where Hermes `xurl` (X write API) is the wrong tool
- URL-only paste (no verb) = **brief**, not catalog `add`

## Do not use for

- Posting, liking, DMing on X → `xurl`
- Pure YouTube caption → blog/thread polish only → `youtube-content` (still OK to start here if they only want transcript summary)
- Ad swipe-file archive with Vault/Sheets → `referencias-criativos-ads`

## Workflow

1. **Doctor (multi-backend platforms)**  
   `export PATH="$HOME/.agent-reach-venv/bin:$HOME/.npm-global/bin:$HOME/.local/bin:$PATH"`  
   `agent-reach doctor --json` — pick `active_backend` per platform, then **confirm the binary on PATH** (`which twitter`, not the doctor label `twitter-cli`). Full ops: skill `hermes-agent-ecosystem` → `references/agent-reach-ops.md`.

2. **Route by URL**
   | URL kind | Prefer |
   |----------|--------|
   | Public IG **Reel/video** | `yt-dlp` media + info.json → frames (ffmpeg) + Whisper; Jina only as weak caption hint |
   | Public IG **image carousel** | Playwright local (§3b) — yt-dlp media fails; see `references/ig-image-carousel.md` |
   | YouTube | yt-dlp and/or `youtube-content` transcript script |
   | X write/official | `xurl` |
   | X cookie/CLI **read** | `$HOME/.local/bin/twitter tweet <id>` (full YAML). Compact `-c` truncates. Expand `t.co` with HTTP HEAD `Location`. OpenCLI only if that binary is missing |
   | Public GitHub repo | `gh repo view` + README; same brief shape as a post |
   | Generic article | Jina `https://r.jina.ai/URL` |
   | Login walls (IG feed, FB, Reddit search) | OpenCLI **after** extension connected |

3. **Public IG reel recipe (proven)**  
   ```bash
   mkdir -p /tmp/ig-ingest && cd /tmp/ig-ingest
   yt-dlp -o '%(id)s.%(ext)s' --write-info-json --write-thumbnail "$URL"
   ffmpeg -y -i *.mp4 -vf "fps=1/2,scale=720:-1" -frames:v 10 frame_%02d.jpg
   ffmpeg -y -i *.mp4 -vn -acodec libmp3lame -q:a 4 audio.mp3
   whisper audio.mp3 --model base --language pt --output_format txt
   ```  
   Vision on frames that carry title cards / numbered tips; merge with transcript + info.json (author, likes, caption).

3b. **Public IG image carousel (proven)**  
   yt-dlp often yields `No video formats found!` per slide even with correct `playlist_count`. Do **not** treat as OpenCLI install.

   **Prefer Playwright local** (full recipe in `references/ig-image-carousel.md`):
   1. Optional yt-dlp `--write-info-json` for author/likes/`playlist_count` only.
   2. Chromium from `~/Library/Caches/ms-playwright/chromium-*/…` (or Google Chrome); `pip install playwright` in agent-reach venv if needed.
   3. Open post → Fechar dialog → Avançar **and** Voltar harvest of `img` ≥600px (cdninstagram/fbcdn); dedupe by `/\d+_\d+_…/`.
   4. Download with `page.request.get(src)` → `slide_01.jpg` …  
      Do **not** rely on Hermes `browser_console` CDN URLs (truncated) or canvas→localhost (CORS) or multi `a.download` (often only first file).
   5. **Vision every slide** — IG `alt` is garbled; never ship a checklist from alt alone. If a vision result comes back without pixels, OCR the remaining JPGs with macOS Swift Vision (`references/ig-image-carousel.md` § OCR leftover slides) instead of looping vision.
   6. **Offer** catalog (IMP-/REF-). Run `add` only after Salve/salva/cataloga — not on URL paste. Then repeatable `--media` + `--notes "$(cat notes.txt)"`.

4. **Deliver**  
   Short PT-BR: author · hook/tese · bullets acionáveis · métricas se úteis · offer catalog (IMP- vs REF-).  
   Lead with **content**, not install status — unless blocked.  
   Do **not** `implementacoes_refs.py add` / `criativos_refs.py add` until the user says Salve/salva/cataloga/pode fazer. One URL paste = one brief.

5. **OpenCLI blocked**  
   One short block: Web Store install link + “responda pronto”.  
   Do **not** claim extension is active while `opencli doctor` shows disconnected.  
   Keep using yt-dlp public path when it already works; for image carousels prefer §3b before OpenCLI.

## OpenCLI activation (user one-click)

- Store: https://chromewebstore.google.com/detail/opencli/ildkmabpimmkaediidaifkhjpohdnifk  
- Or Load unpacked: `~/.opencli/extension`  
- Daemon alone (port 19825) is insufficient. Modern Chrome often ignores `--load-extension` automation — don’t burn a turn on dedicated profiles as “activated.”

## Pitfalls

- Jina on IG often returns login wall chrome — never sole source for Reels **or image carousels**.
- yt-dlp on **image carousels**: metadata/playlist may work; media dies with `No video formats found!` — expected → §3b Playwright, not yt-dlp upgrades or OpenCLI first.
- Hermes `browser_console` truncates long Instagram CDN query strings — unusable for curl; use Playwright `page.request.get`.
- IG carousel `alt` is partial OCR — always vision-verify numbered/technical slides.
- Login/signup dialog blocks carousel until closed; snapshot may show comments only until Fechar + Avançar.
- One forward pass can miss lazy slides — harvest **forward + back**; match `playlist_count`.
- `implementacoes_refs.py add`: `--media` is repeatable; numbered checklists in notes must come from a file (`cat notes.txt`), not unquoted heredoc with `1)` lines. Prefer explicit `slide_01.jpg` paths.
- Vault iCloud dataless (`EDEADLK` on template/note read) is a separate issue in `implementacoes_refs.py` / Obsidian path — hydrate with `brctl download` on templates if `add` fails after media copy.
- `agent-reach transcribe` needs Groq/OpenAI key; else local `whisper`.
- Bilibili: use bili-cli, not yt-dlp.
- Agent-Reach skill may live at `research/agent-reach` (symlink); load it for platform command tables, this skill for **ingest product workflow**.
- Whisper base PT mishears jargon (Issues→iXUS, PR, Biome) — prefer on-screen OCR for technical lists.
- Doctor label `twitter-cli` is not the binary — call `twitter` on `$HOME/.local/bin`; `twitter -c tweet` truncates, use uncompacted `twitter tweet ID` for thread text.
- Expand `t.co` with HEAD `Location` before putting links in the brief — the tweet body hides the real GitHub/x.ai dest.
- Do not `add` IMP-/REF- on a bare URL paste; Salve applies to the **last** URL, not every unsaved link in the thread.

## Support files

- `references/ig-image-carousel.md` — Playwright download recipe, failed-path matrix, handoff to IMP-/REF-

## Related

- `hermes-agent-ecosystem` / `references/agent-reach-ops.md`
- `research/agent-reach` (upstream platform refs)
- `youtube-content`, `xurl`, `referencias-criativos-ads`, `referencias-implementacoes`

