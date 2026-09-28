# Mac Mini — keepawake (não é Tailscale)

Sintoma: acesso remoto (Tailscale, SSH, painéis 5051–5055, Claude Code, Orca) vai e volta. O Mini **dorme**.

## Sinais

- `pmset -g`: `sleep 1` na tomada; `networkoversleep 0`.
- `pmset -g log`: `Entering Sleep state due to 'Maintenance Sleep'` / `DarkWake from Deep Idle` (E_RX_IP_PACKET ARPT).
- Dezenas de sleep/wake por dia (ex. 67 sleeps num dia útil; 334 desde o boot).
- `en0` Ethernet **inactive**; só Wi‑Fi `en1`. SSID preferido 5 GHz: **Starlink**. Evitar **Starlink 2,4 GHz** (canal 11).
- `tailscale debug prefs`: `RunSSH: false`. Login Remoto pode estar On (sshd on-demand).

## Alvo (AC)

`sleep 0`, `SleepDisabled 1`, `networkoversleep 1`. LaunchAgent `local.keepawake` = `/usr/bin/caffeinate -ims`.

Plist: `~/Library/LaunchAgents/local.keepawake.plist`.

## Checklist (Terminal.app no Mini, uma senha)

```bash
sudo pmset -c sleep 0
sudo pmset -c disablesleep 1
sudo pmset -c networkoversleep 1
sudo systemsetup -setremotelogin on
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/local.keepawake.plist 2>/dev/null || launchctl kickstart -k gui/$(id -u)/local.keepawake
```

Conferir:

```bash
pmset -g | grep -E 'sleep|networkoversleep|SleepDisabled'
launchctl print gui/$(id -u)/local.keepawake | awk '/state =|pid =/'
pgrep -lf 'caffeinate -ims'
```

Mandar **linha por linha**. Colar tudo numa linha ainda aplica o `pmset`; o `launchctl` precisa do `$(id -u)` intacto.

`launchctl bootstrap` KeepAlive **é bloqueado** a partir do gateway Hermes. Kickstart pelo agente às vezes passa; bootstrap só no Terminal.app.

Ethernet `en0` ligado é mais estável que Wi‑Fi 2,4 GHz + sono.
