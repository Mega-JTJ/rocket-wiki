#!/usr/bin/env python3
"""Rebuild the Rocket Wiki with live data, then optionally deploy."""
from __future__ import annotations

import json
import os
import re
import sqlite3
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[2]
WIKI = WORKSPACE / "rocket-wiki"
DOCS = WIKI / "docs"
SKILLS_DIR = Path.home() / ".openclaw" / "plugin-skills"


def run(cmd: list[str], **kw) -> str:
    return subprocess.check_output(cmd, text=True, timeout=30, **kw).strip()


def timestamp() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")


def render_page(path: Path, replacements: dict[str, str]) -> None:
    """Replace comment markers in a page with generated content."""
    text = path.read_text()
    for marker, content in replacements.items():
        text = text.replace(marker, content)
    path.write_text(text)


# ── index.md ────────────────────────────────────────────────────

def build_index() -> None:
    ts_marker = "<!-- REBUILT_TS -->"
    spotlight_marker = "<!-- SIGNALDECK_SPOTLIGHT -->"
    
    ts_content = f"*{timestamp()}*"
    
    # Get latest SignalDeck rankings
    rankings_path = WORKSPACE / "projects" / "x-stock-signal-index" / "reports" / "state" / "latest_rankings.sha256"
    spotlight = ""
    rankings_md = WORKSPACE / "projects" / "x-stock-signal-index" / "reports" / "latest_rankings.md"
    if rankings_md.exists():
        lines = rankings_md.read_text().splitlines()[:25]
        spotlight = "\n".join(lines) + "\n\n*See [Reports](reports.md) for full output.*"
    else:
        spotlight = "*No rankings available yet. Next nightly refresh at 23:45 London.*"
    
    render_page(DOCS / "index.md", {ts_marker: ts_content, spotlight_marker: spotlight})


# ── projects.md ─────────────────────────────────────────────────

def build_projects() -> None:
    handles_marker = "<!-- SIGNALDECK_HANDLES -->"
    rs_marker = "<!-- RS_SCREENER_STATUS -->"
    ops_marker = "<!-- PERSONAL_OPS_STATUS -->"
    
    # SignalDeck handles
    handles_csv = WORKSPACE / "projects" / "x-stock-signal-index" / "inputs" / "guru_handles.csv"
    handles_text = ""
    if handles_csv.exists():
        handles_text = "| Handle | Active |\n|---|---|\n"
        for line in handles_csv.read_text().splitlines()[1:]:
            parts = [p.strip() for p in line.split(",")]
            if len(parts) >= 5:
                handle, _, _, _, active = parts[0], parts[1], parts[2], parts[3], parts[4]
                if active == "1":
                    handles_text += f"| {handle} | ✅ |\n"
    
    # RS Screener
    rs_text = "**Status:** Active. Nightly scan of US market universe with sector/industry mapping."
    
    # Personal Ops
    ops_text = ""
    rss_report = WORKSPACE / "personal_ops" / "rss_monitor" / "reports" / "latest.md"
    if rss_report.exists():
        ops_text = f"**RSS Digest:** Available (last generated: check [Reports](reports.md))\n\n"
    ops_text += "**Calendar:** Read-only Google Calendar integration active."
    
    render_page(DOCS / "projects.md", {
        handles_marker: handles_text,
        rs_marker: rs_text,
        ops_marker: ops_text,
    })


# ── reports.md ──────────────────────────────────────────────────

def build_reports() -> None:
    marker = "<!-- LATEST_REPORTS -->"
    lines = [f"*Generated {timestamp()}*\n"]
    
    # SignalDeck rankings
    rankings = WORKSPACE / "projects" / "x-stock-signal-index" / "reports" / "latest_rankings.md"
    if rankings.exists():
        lines.append("## 📈 SignalDeck Rankings")
        lines.append(f"[Latest rankings]({rankings}) (local file)\n")
    
    # RSS Digest
    rss = WORKSPACE / "personal_ops" / "rss_monitor" / "reports" / "latest.md"
    if rss.exists():
        lines.append("## 📰 RSS / News Digest")
        lines.append(f"[Latest digest]({rss}) (local file)\n")
    
    # Skills report
    skills_report = WORKSPACE / "reports" / "skills_discovery_2026-05-16.md"
    if skills_report.exists():
        lines.append("## 🛠 Skills Discovery Report")
        lines.append(f"[Skills report]({skills_report}) (local file)\n")
    
    if len(lines) == 1:
        lines.append("*No reports found. Run nightly jobs or triggers.*")
    
    render_page(DOCS / "reports.md", {marker: "\n".join(lines)})


# ── skills.md ───────────────────────────────────────────────────

def build_skills() -> None:
    marker = "<!-- ACTIVE_SKILLS -->"
    lines = []
    
    # Installed plugin skills
    if SKILLS_DIR.exists():
        for skill_dir in sorted(SKILLS_DIR.iterdir()):
            if skill_dir.is_dir():
                readme = skill_dir / "SKILL.md"
                if readme.exists():
                    content = readme.read_text()
                    # Extract frontmatter name/description
                    m_name = re.search(r"^name:\s*(.+)$", content, re.MULTILINE)
                    m_desc = re.search(r"^description:\s*(.+)$", content, re.MULTILINE)
                    name = m_name.group(1).strip() if m_name else skill_dir.name
                    desc = m_desc.group(1).strip()[:120] if m_desc else ""
                    lines.append(f"### {name}")
                    if desc:
                        lines.append(f"{desc}\n")
    
    if not lines:
        lines.append("*No local plugin skills found.*")
    
    lines.append("\n## SKILL.md Skills (from workspace)")
    lines.append("See the `SKILL.md` files loaded at session startup for bundled skills (gog, healthcheck, taskflow, etc.).")
    
    render_page(DOCS / "skills.md", {marker: "\n".join(lines)})


# ── cron-jobs.md ────────────────────────────────────────────────

def build_cron() -> None:
    marker = "<!-- CRON_JOBS -->"
    lines = []
    
    try:
        output = run(["openclaw", "cron", "list", "--json"])
        data = json.loads(output)
        jobs = data if isinstance(data, list) else data.get("jobs", [])
        if jobs:
            lines.append("| Name | Schedule | Next Run | Enabled |\n|---|---|---|---|")
            for job in jobs:
                name = job.get("name", "?")
                sched = job.get("schedule", {})
                kind = sched.get("kind", "?")
                if kind == "cron":
                    schedule_str = f"`{sched.get('expr','?')}` ({sched.get('tz','?')})"
                elif kind == "every":
                    schedule_str = f"every {sched.get('everyMs',0)//60000}min"
                else:
                    schedule_str = kind
                
                state = job.get("state", {})
                next_run = state.get("nextRunAtMs", 0)
                next_str = datetime.fromtimestamp(next_run/1000, UTC).strftime("%Y-%m-%d %H:%M") if next_run else "?"
                
                enabled = "✅" if job.get("enabled") else "❌"
                lines.append(f"| {name} | {schedule_str} | {next_str} | {enabled} |")
        else:
            lines.append("*No cron jobs configured.*")
    except Exception as e:
        lines.append(f"*Error fetching cron jobs: {e}*")
    
    render_page(DOCS / "cron-jobs.md", {marker: "\n".join(lines)})


# ── kanban.md ──────────────────────────────────────────────────

def build_kanban() -> None:
    marker = "<!-- KANBAN_BOARD -->"
    kanban_json = WIKI / "data" / "kanban.json"
    
    if not kanban_json.exists():
        render_page(DOCS / "kanban.md", {marker: "*Kanban data not found.*"})
        return
    
    data = json.loads(kanban_json.read_text())
    columns = data.get("columns", [])
    
    html_parts = ['<div class="kanban-board">']
    
    col_colors = {"backlog": "#37474f", "in-progress": "#1a237e", "done": "#1b5e20"}
    
    for col in columns:
        col_id = col.get("id", "")
        col_name = col.get("name", "?")
        bg = col_colors.get(col_id, col.get("color", "#333"))
        html_parts.append(f'<div class="kanban-column" style="background:{bg}">')
        html_parts.append(f'<h3>{col_name} <small>({len(col.get("cards",[]))})</small></h3>')
        
        for card in col.get("cards", []):
            priority = card.get("priority", "")
            priority_class = f"priority-{priority}" if priority else ""
            html_parts.append(f'<div class="kanban-card {priority_class}">')
            html_parts.append(f'<div>{card["title"]}</div>')
            tags = card.get("tags", [])
            if tags:
                html_parts.append('<div class="tags">')
                for tag in tags:
                    html_parts.append(f'<span class="tag">{tag}</span>')
                html_parts.append('</div>')
            html_parts.append('</div>')
        
        html_parts.append('</div>')
    
    html_parts.append('</div>')
    html_parts.append(f'<p style="font-size:0.8rem;color:var(--md-default-fg-color--light);margin-top:1rem;">Last updated: {timestamp()} · Edit <code>rocket-wiki/data/kanban.json</code></p>')
    
    render_page(DOCS / "kanban.md", {marker: "\n".join(html_parts)})


# ── system.md ───────────────────────────────────────────────────

def build_system() -> None:
    marker = "<!-- SYSTEM_STATUS -->"
    lines = [f"*Snapshot: {timestamp()}*\n"]
    
    # Host info
    try:
        hostname = run(["hostname"])
        lines.append(f"**Host:** `{hostname}`")
    except Exception:
        pass
    
    try:
        uname = run(["uname", "-a"])
        lines.append(f"**OS:** `{uname}`")
    except Exception:
        pass
    
    try:
        gw = run(["openclaw", "gateway", "status"])
        lines.append(f"\n### Gateway\n```\n{gw[:500]}\n```")
    except Exception as e:
        lines.append(f"\n*Gateway status unavailable: {e}*")
    
    # OpenClaw version
    try:
        ver = run(["openclaw", "--version"])
        lines.append(f"\n**OpenClaw:** `{ver}`")
    except Exception:
        pass
    
    # Node
    try:
        node_ver = run(["node", "--version"])
        lines.append(f"**Node:** `{node_ver}`")
    except Exception:
        pass
    
    render_page(DOCS / "system.md", {marker: "\n".join(lines)})


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
    
    # Deploy if requested
    if "--deploy" in sys.argv:
        print("Deploying to gh-pages...")
        subprocess.run([sys.executable, "-m", "mkdocs", "gh-deploy", "--force", "--message", f"Auto-rebuild {timestamp()}"], check=True, timeout=120)
        print("Deployed!")


if __name__ == "__main__":
    main()
