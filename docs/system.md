# 🖥 System Status

*Snapshot: 2026-05-19 05:55:57 UTC*

**Host:** `DESKTOP-4HQPOBC`
**OS:** `Linux DESKTOP-4HQPOBC 6.6.114.1-microsoft-standard-WSL2 #1 SMP PREEMPT_DYNAMIC Mon Dec  1 20:46:23 UTC 2025 x86_64 x86_64 x86_64 GNU/Linux`
**OpenClaw:** `OpenClaw 2026.5.7 (eeef486)`
**Node:** `v24.14.1`

### Gateway
```
Service: systemd user (enabled)
File logs: /tmp/openclaw/openclaw-2026-05-19.log
Command: /usr/bin/node /home/jtj/.npm-global/lib/node_modules/openclaw/dist/index.js gateway --port 18789
Service file: ~/.config/systemd/user/openclaw-gateway.service
Service env: OPENCLAW_GATEWAY_PORT=18789

Config (cli): ~/.openclaw/openclaw.json
Config (service): ~/.openclaw/openclaw.json

Gateway: bind=loopback (127.0.0.1), port=18789 (service args)
Probe target: ws://127.0.0.1:18789
Dashboard: http://127.0.0.1:18789/
Probe note: Loopback-only gateway; only local clients can connect.

Runtime: running (pid 10957, state active, sub running, last exit 0, reason 0)
Connectivity probe: ok
Capability: admin-capable

Listening: 127.0.0.1:18789
Troubles: run openclaw status
Troubleshooting: https://docs.openclaw.ai/troubleshooting
```
