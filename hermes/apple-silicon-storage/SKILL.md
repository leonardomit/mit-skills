---
name: apple-silicon-storage
description: "Use when expanding storage on Apple Silicon Macs."
category: apple
---

# Apple Silicon storage expansion

Internal NVMe on Apple Silicon Macs is **soldered**. Extra storage is always external. Diagnose the live machine first, then buy a **40 Gbps Thunderbolt 4 / USB4** enclosure + **M.2 2280 NVMe TLC with DRAM**, no factory heatsink.

## When to use

- "Quero por um SSD a mais no Mac Mini / MacBook / Studio"
- User sends a product screenshot of a dock, case, or SSD
- Disk almost full; Time Machine; ComfyUI/models/Docker eating the boot volume

Do **not** use for iCloud/Files-on-Demand cleanup only, or for price-watch crons (`product-price-monitor`).

## 1. Diagnose this Mac

Run, don't guess:

```bash
sysctl -n machdep.cpu.brand_string
system_profiler SPHardwareDataType SPStorageDataType SPThunderboltDataType
diskutil list
df -h /
```

Record: model identifier, chip (M4 vs M4 Pro), RAM, internal capacity/free, already-mounted externals, which ports are 40 Gb/s.

**This user's Mini** (detail in `references/mac-mini-m4.md`): M4 base `Mac16,10`, 16 GB, 256 GB soldered, 3× TB4 40 Gb/s on the **rear**, front USB-C is **10 Gb/s**. A WD Elements USB HDD is archive/Time Machine only.

## 2. What to buy

| Role | Buy | Reject |
|------|-----|--------|
| Case | USB4 / Thunderbolt 4 **40 Gbps** NVMe enclosure (Acasis TBU405 class; Intel JHL or proven ASM2464PD) | USB 3.0/3.2 **5–10 Gbps**, SATA 2.5"/3.5" docks (Orico 2-bay etc.), TBU405 **Air** if they might use the front port |
| SSD | M.2 **2280 NVMe**, **TLC + DRAM**, **no heatsink**. Peers: Kingston KC3000 (`SKC3000D`), Samsung 990 PRO, WD SN850X (`WDS…X0E` not `XHE`), Crucial T500, TeamGroup G70 PRO | QLC / DRAM-less budget (NV3, P3 Plus, WD Green), Gen5 (hot, wasted on TB4), any **with dissipador**, Fury Renegade **with** heatsink |
| Cable | Thunderbolt-logo cable that ships with the case | Random USB-C charge cables |
| Port | **Rear** TB4 on M4 Mini | Front USB-C (10 Gb/s) |

Capacity: 2 TB minimum if the boot disk is 256 GB and already full. 4 TB only if models/video justify it.

TB5 enclosures only on **M4 Pro / M4 Max** machines that actually have TB5.

## 3. Review a listing / screenshot

Before "pode comprar":

1. Interface number: **40 Gbps** vs 5/10/20.
2. Drive type: **NVMe M.2** vs SATA HDD/SSD bay.
3. Exact SKU: TBU405 vs TBU405 Air vs TBU405 Pro (fan).
4. SSD SKU: `…D` / `X0E` / no "heatsink" in the title.
5. **Landed price** on internacional: sticker + imposto (Remessa Conforme) + prazo. Compare to Kabum/Pichau/Amazon BR.
6. Seller/ratings only as a tie-break.

A 2-bay SATA dock is a **backup/archive** box, not a working disk. Say that in one line.

## 4. After it arrives

1. Plug **rear** TB4.
2. Disk Utility → Erase → **APFS** + GUID (Mac-only). ExFAT only if they must share with Windows.
3. Move heavy trees (ComfyUI, models, Docker, Downloads, VMs). Leave macOS + apps on internal.
4. Stay mounted (working disk, not a pendrive).
5. Time Machine on a **different** disk (the Elements HDD is fine for TM/archive). Never TM + scratch on the same SSD.

Apple Silicon can boot from external TB volumes if they ever want a clone; not required for extra space.

## Pitfalls

- Opening the chassis or promising an internal second SSD.
- Pairing a 40 Gbps case with QLC so sustained writes cliff after the SLC cache.
- Buying 990 EVO Plus / Lexar NM790 (no DRAM) when a KC3000-class drive is cheaper in BR — HMB is weaker in an enclosure.
- Comparing Kabum list price to Amazon "oferta" without checking marketplace seller + full tax.
- Using the existing USB HDD as the new working volume.

## Verification

- [ ] Live `system_profiler` / `df` captured before recommending.
- [ ] Case is 40 Gbps NVMe; SSD is 2280 TLC+DRAM without heatsink.
- [ ] Landed BR price quoted (PIX or sticker+imposto).
- [ ] User told which physical port to use.

## Support

- `references/mac-mini-m4.md` — this Mini's identity, port map, buy-list SKUs (refresh prices when shopping).
