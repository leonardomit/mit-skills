# Instagram image carousel ingest

When: public `instagram.com/p/...` multi-image post (not Reel/video).

## Symptoms that mean “use this path”

- yt-dlp: `Downloading N items` then each item `No video formats found!`
- info.json has `playlist_count`, `uploader`, likes — but no media files
- Jina: login wall + maybe cover alt only

## Preferred recipe (Playwright local) — proven 2026-08-13

yt-dlp media fails; Hermes `browser_console` URL harvest is **truncated mid-query-string**; canvas→`localhost` POST is CORS-blocked from instagram.com; `a.download` in the automation browser often only lands the **first** file in `~/Downloads`.

Use **Playwright + cached Chromium + `page.request.get(src)`** (shares the page cookie jar):

```bash
export PATH="$HOME/.agent-reach-venv/bin:$PATH"
# pip install playwright if missing; chromium cache often already present
```

```python
from playwright.sync_api import sync_playwright
import os, time, glob

out = "/tmp/ig-ingest-<shortcode>"
os.makedirs(out, exist_ok=True)
import glob
exe = (glob.glob(os.path.expanduser(
    "~/Library/Caches/ms-playwright/chromium-*/chrome-mac-arm64/"
    "Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
)) or ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"])[-1]
# glob the cache — do not pin chromium-NNNN

url = "https://www.instagram.com/p/<shortcode>/"
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=exe, headless=True)
    context = browser.new_context(
        viewport={"width": 1280, "height": 1600},
        user_agent=(
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ),
        locale="pt-BR",
    )
    page = context.new_page()
    page.goto(url, wait_until="domcontentloaded", timeout=60000)
    time.sleep(3)
    for sel in ['button:has-text("Fechar")', '[aria-label="Fechar"]', 'button[aria-label="Close"]']:
        try:
            page.locator(sel).first.click(timeout=2000)
            break
        except Exception:
            pass
    time.sleep(1)

    all_imgs = {}

    def harvest():
        items = page.evaluate(
            """() => {
          const out = [];
          for (const img of document.querySelectorAll('img')) {
            const w = img.naturalWidth || 0;
            if (w < 600) continue;
            const src = img.currentSrc || img.src || '';
            if (!(src.includes('cdninstagram') || src.includes('fbcdn'))) continue;
            const key = (src.match(/(\\d+_\\d+_[^/?]+)/) || [])[1] || src;
            out.push({src, w, h: img.naturalHeight, key});
          }
          return out;
        }"""
        )
        for it in items:
            k = it["key"]
            if k not in all_imgs or it["w"] > all_imgs[k]["w"]:
                all_imgs[k] = it

    harvest()
    for _ in range(12):
        try:
            page.locator('button[aria-label="Avançar"]').first.click(timeout=1500)
            time.sleep(1.0)
            harvest()
        except Exception:
            break
    for _ in range(12):
        try:
            page.locator('button[aria-label="Voltar"]').first.click(timeout=1500)
            time.sleep(0.8)
            harvest()
        except Exception:
            break

    big = [v for v in all_imgs.values() if v["w"] >= 1000]
    # insertion order ≈ first-seen while advancing
    for i, s in enumerate(big, 1):
        path = os.path.join(out, f"slide_{i:02d}.jpg")
        open(path, "wb").write(page.request.get(s["src"]).body())
        print("saved", path, os.path.getsize(path))
    browser.close()
```

### Why this shape

| Approach | Result |
|----------|--------|
| yt-dlp per slide | `No video formats found!` (expected) |
| `browser_console` return of long CDN URLs | Truncated (`eyJ2ZW...MyJ9`) — unusable curl |
| `fetch(cdn)` / `fetch(127.0.0.1)` from page | CORS / private-network block |
| canvas `toDataURL` + `<a download>` | Works once; multi-file often blocked in automation browser |
| Playwright `page.request.get(src)` after carousel walk | Full-res JPGs, all unique slides |

### After download

1. Optional: `yt-dlp --write-info-json` for author / likes / caption / `playlist_count`.
2. Vision **every** `slide_NN.jpg` — IG `alt` is garbled OCR; never ship a checklist from alt alone.
3. If a vision call returns no pixels, **stop looping vision**. OCR leftover JPGs with macOS Swift Vision (below) and merge.
4. Brief first. Catalog (`IMP-` / `REF-`) only after Salve. Then repeatable `--media` + `--notes "$(cat notes.txt)"` (bash eats `1)` lines). Explicit `slide_01.jpg` paths.

### OCR leftover slides (macOS)

When vision omits a file, run this once on the missing `slide_NN.jpg` — do not re-queue the same image through vision:

```swift
import Foundation
import Vision
import AppKit
func ocr(_ path: String) -> String {
    guard let img = NSImage(contentsOfFile: path),
          let tiff = img.tiffRepresentation,
          let ci = CIImage(data: tiff) else { return "NOIMAGE" }
    let req = VNRecognizeTextRequest()
    req.recognitionLevel = .accurate
    req.usesLanguageCorrection = true
    req.recognitionLanguages = ["pt-BR", "en-US"]
    let handler = VNImageRequestHandler(ciImage: ci, options: [:])
    do { try handler.perform([req]) } catch { return "ERR \(error)" }
    return (req.results ?? []).compactMap { $0.topCandidates(1).first?.string }.joined(separator: "\n")
}
```

Keep insertion order of first-seen CDN keys while advancing — a later harvest of the same key at higher width must not reshuffle slide numbers.

## Fallback: Hermes browser (OCR / metadata only)

1. Navigate post → Fechar dialog.
2. Console: Avançar/Voltar for count/order sanity (do not trust returned full CDN URLs).
3. `browser_vision` each slide if Playwright unavailable — screenshots as media, lower fidelity.

## Do not

- Treat yt-dlp image failure as “need OpenCLI/extension” when the post is public.
- Trust IG alt alone for technical numbered lists.
- Assume one forward pass is enough — **forward + back** harvest finds lazy slides (target count = `playlist_count`).
- Burn turns on OpenCLI for public carousels before Playwright.
