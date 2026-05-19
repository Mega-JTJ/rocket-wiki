#!/usr/bin/env python3
"""Rebuild the Rocket Wiki with live data, then optionally deploy.

This script is intentionally idempotent: it rewrites generated pages from
fresh data each run instead of replacing one-shot markers that disappear.
"""
from __future__ import annotations

import csv
import json
import os
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[2]
WIKI = WORKSPACE / "rocket-wiki"
DOCS = WIKI / "docs"
SKILLS_DIR = Path.home() / ".openclaw" / "plugin-skills"


def run(cmd: list[str], timeout: int = 30, **kw) -> str:
    return subprocess.check_output(cmd, text=True, timeout=timeout, **kw).strip()


def timestamp() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")


def write_page(name: str, content: str) -> None:
    (DOCS / name).write_text(content.rstrip() + "\n")


def read_text(path: Path, default: str = "") -> str:
    return path.read_text() if path.exists() else default


# ── index.md ────────────────────────────────────────────────────

def build_index() -> None:
    rankings_md = WORKSPACE / "projects" / "x-stock-signal-index" / "reports" / "latest_rankings.md"
    if rankings_md.exists():
        spotlight = "\n".join(rankings_md.read_text().splitlines()[:25])
        spotlight += "\n\n*See [Reports](reports.md) for full output.*"
    else:
        spotlight = "*No rankings available yet. Next nightly refresh at 23:45 London.*"

    write_page("index.md", f"""# 🚀 Rocket Wiki

Jack's personal operating system — live dashboard of projects, research, automation, and tools.

Built and maintained by Rocket. Last rebuilt: *{timestamp()}*.

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

{spotlight}
""")


# ── projects.md ─────────────────────────────────────────────────

def build_projects() -> None:
    handles_csv = WORKSPACE / "projects" / "x-stock-signal-index" / "inputs" / "guru_handles.csv"
    handles_rows: list[str] = []
    if handles_csv.exists():
        with handles_csv.open(newline="") as f:
            for row in csv.DictReader(f):
                active = str(row.get("active", row.get("Active", ""))).strip()
                handle = str(row.get("handle", row.get("Handle", ""))).strip()
                if handle and active in {"1", "true", "True", "yes", "Y"}:
                    handles_rows.append(f"| {handle} | ✅ |")
    handles_text = "| Handle | Active |\n|---|---|\n" + "\n".join(handles_rows) if handles_rows else "*No active handles found.*"

    rss = WORKSPACE / "personal_ops" / "rss_monitor" / "reports" / "latest.md"
    rss_text = "Available" if rss.exists() else "Not generated yet"

    write_page("projects.md", f"""# 🚀 Projects

## SignalDeck

X/Twitter idea and catalyst intake engine. Scrapes tracked accounts, extracts ticker signals, scores and ranks them.

**Path:** `projects/x-stock-signal-index/`

**Tracked accounts ({len(handles_rows)} active):**

{handles_text}

**Output:** Nightly rankings PDF pushed to Telegram at 23:45 London.

**Data flow:**
1. Nitter RSS / configured scrape source → recent posts from tracked accounts
2. Import → parse ticker mentions, direction, conviction
3. Score → multi-factor ranking algorithm
4. Report → PDF generation + Telegram delivery

---

## RS Screener

Price and relative-strength confirmation engine. Scans broad US market universe with sector/industry mapping and liquidity filters.

**Path:** workspace scripts/data under `scripts/`, `data/`, and `reports/`

**Status:** Active. Nightly scan of US market universe with sector/industry mapping.

---

## Deep Alpha

Extracts market-moving alpha from executive transcripts and interviews into structured data.

**Path:** `projects/deep_alpha/`

**Status:** 🟡 In development — transcript ingestion pipeline working, extraction model tuning in progress.

---

## Personal Ops

Cross-references Google Calendar, Contacts, and local context for relationship-aware reminders and prep notes.

**Path:** `personal_ops/`

**Capabilities:**
- Calendar context briefs
- RSS/news signal digest
- Event rules engine

**RSS Digest:** {rss_text}

**Calendar:** Read-only Google Calendar integration active.

---

## Rocket Wiki

This wiki itself. Auto-rebuilt and deployed hourly.

**Path:** `rocket-wiki/`  
**Deploy:** GitHub Pages
""")


# ── reports.md ──────────────────────────────────────────────────

def build_reports() -> None:
    lines = [f"# 📊 Reports\n", f"*Generated {timestamp()}*\n"]
    reports = [
        ("📈 SignalDeck Rankings", WORKSPACE / "projects" / "x-stock-signal-index" / "reports" / "latest_rankings.md", "Latest rankings"),
        ("📰 RSS / News Digest", WORKSPACE / "personal_ops" / "rss_monitor" / "reports" / "latest.md", "Latest digest"),
        ("💰 Rocket Money Report", WORKSPACE / "reports" / "money_report.md", "Latest money report"),
        ("🎯 TradingView Alert Plan", WORKSPACE / "reports" / "tradingview_alert_plan.md", "Latest alert plan"),
        ("🛠 Skills Discovery Report", WORKSPACE / "reports" / "skills_discovery_2026-05-16.md", "Skills report"),
    ]
    found = False
    for title, path, label in reports:
        if path.exists():
            found = True
            lines.append(f"## {title}")
            lines.append(f"[{label}]({path}) (local file)\n")
    if not found:
        lines.append("*No reports found. Run nightly jobs or triggers.*")
    write_page("reports.md", "\n".join(lines))


# ── skills.md ───────────────────────────────────────────────────

def build_skills() -> None:
    lines = ["# 🛠 Active Skills\n"]
    if SKILLS_DIR.exists():
        for skill_dir in sorted(SKILLS_DIR.iterdir()):
            readme = skill_dir / "SKILL.md"
            if not readme.exists():
                continue
            content = readme.read_text(errors="replace")
            name = skill_dir.name
            desc = ""
            for line in content.splitlines()[:40]:
                if line.lower().startswith("name:"):
                    name = line.split(":", 1)[1].strip() or name
                elif line.lower().startswith("description:"):
                    desc = line.split(":", 1)[1].strip()
            lines.append(f"### {name}")
            if desc:
                lines.append(desc[:160])
            lines.append("")
    if len(lines) == 1:
        lines.append("*No local plugin skills found.*\n")
    lines.append("## Bundled Skills")
    lines.append("Bundled skills are loaded by OpenClaw at session startup when relevant, including Google Workspace, healthcheck, taskflow, tmux, weather, and others.")
    write_page("skills.md", "\n".join(lines))


# ── cron-jobs.md ────────────────────────────────────────────────

def build_cron() -> None:
    lines = ["# ⏰ Cron Jobs\n", "Scheduled automation jobs.\n"]
    try:
        output = run(["openclaw", "cron", "list", "--json"])
        data = json.loads(output)
        jobs = data if isinstance(data, list) else data.get("jobs", [])
        if jobs:
            lines.append("| Name | Schedule | Next Run | Last Status | Enabled |")
            lines.append("|---|---|---|---|---|")
            for job in jobs:
                sched = job.get("schedule", {})
                if sched.get("kind") == "cron":
                    schedule_str = f"`{sched.get('expr','?')}` ({sched.get('tz','?')})"
                elif sched.get("kind") == "every":
                    schedule_str = f"every {sched.get('everyMs',0)//60000}min"
                else:
                    schedule_str = sched.get("kind", "?")
                state = job.get("state", {})
                next_ms = state.get("nextRunAtMs") or 0
                next_str = datetime.fromtimestamp(next_ms / 1000, UTC).strftime("%Y-%m-%d %H:%M UTC") if next_ms else "?"
                status = state.get("lastStatus") or state.get("lastRunStatus") or "?"
                enabled = "✅" if job.get("enabled") else "❌"
                lines.append(f"| {job.get('name','?')} | {schedule_str} | {next_str} | {status} | {enabled} |")
        else:
            lines.append("*No cron jobs configured.*")
    except Exception as e:
        lines.append(f"*Error fetching cron jobs: {e}*")
    write_page("cron-jobs.md", "\n".join(lines))


# ── kanban.md ──────────────────────────────────────────────────

def build_kanban() -> None:
    kanban_json = WIKI / "data" / "kanban.json"
    if not kanban_json.exists():
        write_page("kanban.md", "# 📋 Kanban\n\n*Kanban data not found.*")
        return
    data = json.loads(kanban_json.read_text())
    html_parts = ["# 📋 Kanban\n", '<div class="kanban-board">']
    col_colors = {"backlog": "#37474f", "in-progress": "#1a237e", "done": "#1b5e20"}
    for col in data.get("columns", []):
        col_id = col.get("id", "")
        bg = col_colors.get(col_id, col.get("color", "#333"))
        cards = col.get("cards", [])
        html_parts.append(f'<div class="kanban-column" style="background:{bg}">')
        html_parts.append(f'<h3>{col.get("name", "?")} <small>({len(cards)})</small></h3>')
        for card in cards:
            priority = card.get("priority", "")
            html_parts.append(f'<div class="kanban-card priority-{priority}">')
            html_parts.append(f'<div>{card.get("title", "Untitled")}</div>')
            if card.get("tags"):
                html_parts.append('<div class="tags">')
                for tag in card["tags"]:
                    html_parts.append(f'<span class="tag">{tag}</span>')
                html_parts.append('</div>')
            html_parts.append('</div>')
        html_parts.append('</div>')
    html_parts.append('</div>')
    html_parts.append(f'<p style="font-size:0.8rem;color:var(--md-default-fg-color--light);margin-top:1rem;">Last updated: {timestamp()} · Edit <code>rocket-wiki/data/kanban.json</code></p>')
    write_page("kanban.md", "\n".join(html_parts))


# ── system.md ───────────────────────────────────────────────────

def build_system() -> None:
    lines = ["# 🖥 System Status\n", f"*Snapshot: {timestamp()}*\n"]
    for label, cmd in [
        ("Host", ["hostname"]),
        ("OS", ["uname", "-a"]),
        ("OpenClaw", ["openclaw", "--version"]),
        ("Node", ["node", "--version"]),
    ]:
        try:
            lines.append(f"**{label}:** `{run(cmd)}`")
        except Exception as e:
            lines.append(f"**{label}:** unavailable ({e})")
    try:
        gw = run(["openclaw", "gateway", "status"], timeout=20)
        lines.append(f"\n### Gateway\n```\n{gw[:1000]}\n```")
    except Exception as e:
        lines.append(f"\n*Gateway status unavailable: {e}*")
    write_page("system.md", "\n".join(lines))


# ── Main ─────────────────────────────────────────────────────────

def main() -> None:
    os.chdir(WIKI)
    print(f"Rebuilding Rocket Wiki at {timestamp()}...")
    build_index()
    build_projects()
    build_reports()
    build_kanban()
    build_skills()
    build_cron()
    build_system()
    print("Content generated. Running mkdocs build...")
    subprocess.run([sys.executable, "-m", "mkdocs", "build"], check=True, timeout=60)
    print("Build complete: rocket-wiki/site/")
    if "--deploy" in sys.argv:
        print("Deploying to gh-pages...")
        subprocess.run([sys.executable, "-m", "mkdocs", "gh-deploy", "--force", "--message", f"Auto-rebuild {timestamp()}"], check=True, timeout=120)
        print("Deployed!")


if __name__ == "__main__":
    main()
