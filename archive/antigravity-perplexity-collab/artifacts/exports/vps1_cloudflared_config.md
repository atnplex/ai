# VPS1 Cloudflared Configuration

> **Source**: /etc/cloudflared/config.yml on VPS1
> **Date**: 2026-02-03
> **Note**: Credentials file path shown, actual credentials NOT included

```yaml
tunnel: debian
credentials-file: /home/alex/.cloudflared/81084d84-3978-42f0-aa37-6fc42d54fad4.json

ingress:
  - hostname: pihole-vps.atnplex.com
    service: http://localhost:80
  - hostname: atnplex.com
    service: http://172.19.0.80:80
  - service: http_status:404

edge-ip-version: "4"
```

## Notes

- Tunnel name in config (`debian`) doesn't match tunnel name in Cloudflare (`VPS`)
- Uses IPv4 edge only
- Default catch-all returns 404
