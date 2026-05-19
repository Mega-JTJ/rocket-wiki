# 🚀 Rocket Wiki

Jack's personal operating system — live dashboard of projects, research, automation, and tools.

Built and maintained by Rocket. Last rebuilt: *2026-05-19 05:55:51 UTC*.

---

## 🎯 Active Projects

| Project | Status | Last Updated |
|---|---|---|
| [SignalDeck](projects.md#signaldeck) | 🟢 Live | Nightly |
| [RS Screener](projects.md#rs-screener) | 🟢 Live | Nightly |
| [Deep Alpha](projects.md#deep-alpha) | 🟡 Dev | — |
| [Personal Ops](projects.md#personal-ops) | 🟢 Live | Daily / heartbeat |
| [Rocket Wiki](projects.md#rocket-wiki) | 🟢 Live | Hourly auto-rebuild |

## ⚡ Quick Links

- [📊 Latest Reports](reports.md)
- [📋 Kanban](kanban.md)
- [🛠 Active Skills](skills.md)
- [⏰ Cron Jobs](cron-jobs.md)
- [🖥 System Status](system.md)

## 📈 SignalDeck Spotlight

# SignalDeck Primary Report - Account-Led v1.2

Run date: 2026-05-18

## Model

Primary view is now account-led: identify the best accounts, show what they are picking now, then use ticker rankings as supporting context.

Ticker score combines: consensus, guru 30D track record where available, freshness decay, conviction/direction, detection confidence, post-signal outcome, and RS screener overlap. Unknown-direction chatter counts as mentions but contributes zero score.

Account alpha is winsorised at -75%/+100% per signal so one micro-cap moonshot cannot dominate the leaderboard.

## Account rankings

| Rank | Account | Robust alpha | Fresh 14d | 30D n | Robust avg 30D | Med 30D | Hit 30D | Robust avg 60D | Robust avg 90D |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | @ParadisLabs | 53.8 | 245 | 174 | 35.4% | 31.3% | 85% | 89.1% |  |
| 2 | @FinnStockinger | 27.6 | 122 | 267 | 15.0% | 7.4% | 60% | 34.1% | 35.9% |
| 3 | @frsinvesting | 23.6 | 27 | 6 | 13.8% | 6.5% | 100% |  |  |
| 4 | @Sandeman52 | 13.2 | 71 | 265 | 10.6% | 10.6% | 63% | 19.8% | -11.6% |
| 5 | @Kaizen_Investor | 11.7 | 68 | 555 | 8.4% | 4.7% | 57% | 12.7% | 3.9% |
| 6 | @BULLOFBRITAIN | 4.3 | 129 | 0 |  |  |  |  |  |
| 7 | @DeepValueBagger | 1.2 | 102 | 81 | 2.2% | 2.9% | 53% | 0.3% | -4.4% |
| 8 | @pepemoonboy | -0.6 | 152 | 287 | -0.8% | -2.4% | 46% | 3.9% | -0.9% |
| 9 | @daniel_koss | -5.2 | 50 | 134 | -2.1% | -6.1% | 37% | -3.2% | -5.4% |

*See [Reports](reports.md) for full output.*
