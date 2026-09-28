# Nextcloud ops (after first `up`)

`.env` `NEXTCLOUD_ADMIN_PASSWORD` is first-boot only. To apply a new password:

```bash
docker exec -e OC_PASS='…' --user www-data nextcloud-app-1 \
  php occ user:resetpassword --password-from-env admin
```

Rejects passwords shorter than 10 characters.

## URLs

- Local: `http://127.0.0.1:8085`
- Public Funnel: `https://<tailnet-host>:8443` → 8085

Funnel public ports are only **443 / 8443 / 10000**. Funnel on **8085** does not work without Tailscale. Do not Funnel 443 (relatorio-a) or 5051–5055.

After changing the public host:

```bash
occ config:system:set overwriteprotocol --value=https
occ config:system:set overwritehost --value='<tailnet-host>:8443'
occ config:system:set overwrite.cli.url --value='https://<tailnet-host>:8443'
```
