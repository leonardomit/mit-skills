# Leonardo's Mac mini M4 — storage notes

Refresh prices when shopping. Hardware facts stay unless the machine changes.

## Identity

- Model: Mac mini (2024) · `Mac16,10` · MU9D3LL/A · Apple M4 10-core · 16 GB
- Internal: APPLE SSD AP0256Z, 256 GB soldered, APFS. Often ~10 GB free — treat as urgent.
- Rear: 3× Thunderbolt 4 / USB4 **40 Gb/s** (use these).
- Front: 2× USB-C **10 Gb/s** (do not put the fast SSD here).
- Existing external: WD Elements 1 TB USB (`Elements`, ExFAT) — archive / Time Machine only. TM **not configured** as of 2026-08-31; ExFAT is a poor TM target (prefer APFS partition if enabling).
- Working disk (installed): Acasis **TBU405AIR** on rear TB4 receptacle 1 at **40 Gb/s** + Kingston **KC3000 1 TB** `SKC3000S/1024G`, APFS GPT, volume **`/Volumes/Trabalho`**. Not the non-Air TBU405. Do not plug this enclosure in the front 10 Gb/s port.

## Buy list (working disk)

**Case (empty):** Acasis TBU405 40 Gbps NVMe (not Air). Confirm listing says Thunderbolt 4/3 + USB4 + M.2 NVMe.

- Kabum: https://www.kabum.com.br/produto/503281/case-externo-40gbps-ssd-nvme-m-2-acasis-thunderbolt-4-usb-4-0
- Amazon BR: https://www.amazon.com.br/dp/B0BBZT42HC
- Intl marketplace (AliExpress-class): compare **sticker + imposto**. ~R$ 263 + ~R$ 66 landed beat Kabum ~R$ 699 if seller is real TBU405.

**SSD 2 TB, no heatsink, TLC+DRAM (pick cheapest of these):**

- Kingston KC3000 `SKC3000D/2048G` — usually best BR price. Pichau: https://www.pichau.com.br/ssd-kingston-kc3000-2tb-m-2-2280-pcie-nvme-leitura-7000mb-s-gravacao-7000mb-s-skc3000d-2048g
- Samsung 990 PRO 2 TB (no heatsink)
- WD Black SN850X 2 TB `WDS200T2X0E` (not `XHE`)
- TeamGroup G70 PRO 2 TB
- Crucial T500 2 TB `CT2000T500SSD8`

Do not buy: Kingston NV3 as the “same class”; 990 EVO Plus if KC3000 is cheaper; Gen5; any heatsink SKU.

## After install

Plug rear TB4 → Disk Utility APFS GUID → move ComfyUI/models/Docker/Downloads/VMs → TM stays on Elements.
