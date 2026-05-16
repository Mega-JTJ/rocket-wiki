# 🖥 System

Host and configuration overview.

*Snapshot: 2026-05-16 16:58:08 UTC*

**Host:** `DESKTOP-4HQPOBC`
**OS:** `Linux DESKTOP-4HQPOBC 6.6.114.1-microsoft-standard-WSL2 #1 SMP PREEMPT_DYNAMIC Mon Dec  1 20:46:23 UTC 2025 x86_64 x86_64 x86_64 GNU/Linux`

### Gateway
```
Service: systemd user (enabled)
File logs: /tmp/openclaw/openclaw-2026-05-16.log
Command: /usr/bin/node /home/jtj/.npm-global/lib/node_modules/openclaw/dist/index.js gateway --port 18789
Service file: ~/.config/systemd/user/openclaw-gateway.service
Service env: OPENCLAW_GATEWAY_PORT=18789

Config (cli): ~/.openclaw/openclaw.json
Config (service): ~/.openclaw/openclaw.json

Gateway: bind=loopback (127.0.0.1), port=18789 (service args)
Probe target: ws://127.0.0.1:18789
Dashboard: http://127.0.0.1
```

**OpenClaw:** `OpenClaw 2026.5.7 (eeef486)`
**Node:** `v24.14.1`

*Run the rebuild script to populate.*
