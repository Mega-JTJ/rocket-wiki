# 🚀 Rocket Wiki

Jack's personal operating system — live dashboard of projects, research, automation, and tools.

Built and maintained by Rocket. Last rebuilt: *2026-05-16 16:58:03 UTC*.

---

## 🎯 Active Projects

| Project | Status | Last Updated |
|---|---|---|
| [SignalDeck](projects.md#signaldeck) | 🟢 Live | Nightly |
| [RS Screener](projects.md#rs-screener) | 🟢 Live | Nightly |
| [Deep Alpha](projects.md#deep-alpha) | 🟡 Dev | — |
| [Personal Ops](projects.md#personal-ops) | 🟢 Live | Heartbeat |
| [Rocket Wiki](projects.md#rocket-wiki) | 🟢 Live | Auto-rebuild |

## ⚡ Quick Links

- [📊 Latest Reports](reports.md)
- [🛠 Active Skills](skills.md)
- [⏰ Cron Jobs](cron-jobs.md)
- [🖥 System Status](system.md)

## 📈 SignalDeck Spotlight

# SignalDeck Primary Report - Account-Led v1.2

Run date: 2026-05-15

## Model

Primary view is now account-led: identify the best accounts, show what they are picking now, then use ticker rankings as supporting context.

Ticker score combines: consensus, guru 30D track record where available, freshness decay, conviction/direction, detection confidence, post-signal outcome, and RS screener overlap. Unknown-direction chatter counts as mentions but contributes zero score.

Account alpha is winsorised at -75%/+100% per signal so one micro-cap moonshot cannot dominate the leaderboard.

## Account rankings

| Rank | Account | Robust alpha | Fresh 14d | 30D n | Robust avg 30D | Med 30D | Hit 30D | Robust avg 60D | Robust avg 90D |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | @ParadisLabs | 56.6 | 198 | 165 | 37.2% | 32.1% | 87% | 89.1% |  |
| 2 | @FinnStockinger | 26.6 | 99 | 260 | 14.8% | 7.3% | 60% | 31.6% | 35.4% |
| 3 | @Sandeman52 | 13.9 | 69 | 256 | 11.5% | 10.7% | 64% | 19.1% | -11.6% |
| 4 | @Kaizen_Investor | 11.7 | 76 | 548 | 8.6% | 4.6% | 56% | 12.3% | 3.9% |
| 5 | @BULLOFBRITAIN | 7.0 | 126 | 0 |  |  |  |  |  |
| 6 | @DeepValueBagger | 1.2 | 64 | 81 | 2.2% | 2.9% | 53% | 0.3% | -4.4% |
| 7 | @pepemoonboy | -0.4 | 115 | 277 | -0.5% | -1.8% | 47% | 3.5% | -1.5% |
| 8 | @daniel_koss | -5.2 | 36 | 134 | -2.1% | -6.1% | 37% | -3.2% | -5.4% |
| 9 | @aleabitoreddit | -5.9 | 53 | 444 | -2.9% | -4.2% | 38% | -5.0% | -4.9% |

*See [Reports](reports.md) for full output.*

*Rebuilding... run the rebuild script to populate.*
