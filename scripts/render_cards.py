#!/usr/bin/env python3
"""
Generate GitHub profile README cards:
  1. generated/stats.svg       - David's GitHub Stats
  2. generated/top-langs.svg   - Most Used Languages
  3. generated/calendar.svg    - 12-Month Contribution Calendar Activity

Zero third-party runtime dependency, fully self-hosted via GitHub Actions & Python stdlib.
"""

import os
import sys
import json
import subprocess
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date, datetime

USERNAME = os.environ.get("GH_USER", "davidyehuda45-byte")
TOKEN = os.environ.get("GITHUB_TOKEN", os.environ.get("GH_TOKEN", ""))

GRAPHQL_QUERY = """
query($u: String!) {
  user(login: $u) {
    name
    login
    repositories(first: 100, ownerAffiliations: [OWNER], isFork: false) {
      totalCount
      nodes {
        name
        stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges {
            size
            node {
              name
              color
            }
          }
        }
      }
    }
    pullRequests {
      totalCount
    }
    issues {
      totalCount
    }
    contributionsCollection {
      totalCommitContributions
      restrictedContributionsCount
      totalPullRequestReviewContributions
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            date
            contributionCount
          }
        }
      }
    }
  }
}
"""

def fetch_data():
    if TOKEN:
        try:
            req = urllib.request.Request(
                "https://api.github.com/graphql",
                data=json.dumps({"query": GRAPHQL_QUERY, "variables": {"u": USERNAME}}).encode("utf-8"),
                headers={
                    "Authorization": f"Bearer {TOKEN}",
                    "User-Agent": "david-profile-generator",
                    "Content-Type": "application/json"
                }
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                if "data" in result and result["data"].get("user"):
                    return result["data"]["user"]
                print("GraphQL error via urllib:", result, file=sys.stderr)
        except Exception as e:
            print(f"urllib fetch failed: {e}", file=sys.stderr)

    # Fallback to gh CLI if available
    try:
        proc = subprocess.run(
            ["gh", "api", "graphql", "-f", f"query={GRAPHQL_QUERY}", "-F", f"u={USERNAME}"],
            capture_output=True,
            text=True,
            check=True
        )
        result = json.loads(proc.stdout)
        return result["data"]["user"]
    except Exception as e:
        print(f"gh CLI fetch failed: {e}", file=sys.stderr)

    raise RuntimeError("Could not fetch user data from GitHub GraphQL API")


def render_stats_svg(user_data):
    name = "David's GitHub Stats"
    repos = user_data["repositories"]["nodes"]
    total_stars = sum(r.get("stargazerCount", 0) for r in repos)
    contrib = user_data["contributionsCollection"]
    total_commits = contrib.get("totalCommitContributions", 0)
    total_prs = user_data["pullRequests"]["totalCount"]
    total_issues = user_data["issues"]["totalCount"]
    total_repos = user_data["repositories"]["totalCount"]

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="495" height="195" viewBox="0 0 495 195" fill="none" role="img" aria-label="{name}">
  <style>
    .header {{ font: 600 18px 'Segoe UI', Ubuntu, Sans-Serif; fill: #4DA3FF; }}
    .stat-label {{ font: 600 13px 'Segoe UI', Ubuntu, Sans-Serif; fill: #C9D6EA; }}
    .stat-value {{ font: 700 13px 'Segoe UI', Ubuntu, Sans-Serif; fill: #C9D6EA; }}
    .icon {{ fill: #22D3EE; }}
    .bg {{ fill: #0B1220; stroke: #1B2A47; stroke-width: 1px; rx: 14px; }}
  </style>
  <rect class="bg" x="0.5" y="0.5" width="494" height="194" />
  
  <g transform="translate(25, 32)">
    <text class="header" x="0" y="0">{name}</text>
  </g>
  
  <!-- Stats rows -->
  <g transform="translate(25, 62)">
    <!-- Stars -->
    <g transform="translate(0, 0)">
      <svg class="icon" viewBox="0 0 16 16" width="16" height="16" x="0" y="-12">
        <path d="M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.751.751 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Z"/>
      </svg>
      <text class="stat-label" x="25" y="0">Total Stars Earned:</text>
      <text class="stat-value" x="200" y="0">{total_stars}</text>
    </g>
    
    <!-- Commits -->
    <g transform="translate(0, 24)">
      <svg class="icon" viewBox="0 0 16 16" width="16" height="16" x="0" y="-12">
        <path d="M10.5 7.75a2.5 2.5 0 1 1-5 0 2.5 2.5 0 0 1 5 0Zm1.43.75a4.002 4.002 0 0 1-7.86 0H.75a.75.75 0 1 1 0-1.5h3.32a4.002 4.002 0 0 1 7.86 0h3.32a.75.75 0 1 1 0 1.5h-3.32Z"/>
      </svg>
      <text class="stat-label" x="25" y="0">Total Commits (2026):</text>
      <text class="stat-value" x="200" y="0">{total_commits}</text>
    </g>
    
    <!-- PRs -->
    <g transform="translate(0, 48)">
      <svg class="icon" viewBox="0 0 16 16" width="16" height="16" x="0" y="-12">
        <path d="M1.5 3.25a2.25 2.25 0 1 1 3 2.122v5.256a2.251 2.251 0 1 1-1.5 0V5.372A2.25 2.25 0 0 1 1.5 3.25Zm5.677-.177L9.415.835a.75.75 0 0 1 1.06 0l2.238 2.238a.75.75 0 0 1 0 1.06L10.476 6.37a.75.75 0 0 1-1.06-1.06l.957-.96H8.25A2.75 2.75 0 0 0 5.5 7.1v2.528a2.25 2.25 0 1 1-1.5 0V7.1a4.25 4.25 0 0 1 4.25-4.25h2.127l-.958-.957a.75.75 0 0 1 0-1.06Z"/>
      </svg>
      <text class="stat-label" x="25" y="0">Total PRs:</text>
      <text class="stat-value" x="200" y="0">{total_prs}</text>
    </g>
    
    <!-- Issues -->
    <g transform="translate(0, 72)">
      <svg class="icon" viewBox="0 0 16 16" width="16" height="16" x="0" y="-12">
        <path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/>
        <path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/>
      </svg>
      <text class="stat-label" x="25" y="0">Total Issues:</text>
      <text class="stat-value" x="200" y="0">{total_issues}</text>
    </g>
    
    <!-- Contributed to -->
    <g transform="translate(0, 96)">
      <svg class="icon" viewBox="0 0 16 16" width="16" height="16" x="0" y="-12">
        <path d="M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1 0-1.5h1.75v-2h-8a1 1 0 0 0-.714 1.7.75.75 0 1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5v-9Zm10.5-1h-8a1 1 0 0 0-1 1v6.708A2.486 2.486 0 0 1 4.5 9h8V1.5Z"/>
      </svg>
      <text class="stat-label" x="25" y="0">Contributed to (repos):</text>
      <text class="stat-value" x="200" y="0">{total_repos}</text>
    </g>
  </g>
</svg>
"""
    return svg.strip()


def render_top_langs_svg(user_data):
    name = "Most Used Languages"
    repos = user_data["repositories"]["nodes"]
    
    lang_totals = {}
    lang_colors = {}
    
    for repo in repos:
        langs = repo.get("languages", {}).get("edges", [])
        for edge in langs:
            lname = edge["node"]["name"]
            lcolor = edge["node"].get("color") or "#8FA3BF"
            lsize = edge["size"]
            lang_totals[lname] = lang_totals.get(lname, 0) + lsize
            lang_colors[lname] = lcolor

    total_bytes = sum(lang_totals.values()) or 1
    sorted_langs = sorted(lang_totals.items(), key=lambda x: x[1], reverse=True)[:6]
    
    # Generate progress bar segments
    bar_width = 330
    bar_svg = []
    curr_x = 0
    for lname, lsize in sorted_langs:
        w = (lsize / total_bytes) * bar_width
        if w < 1:
            w = 1
        color = lang_colors.get(lname, "#8FA3BF")
        bar_svg.append(f'<rect x="{curr_x:.1f}" y="0" width="{w:.1f}" height="8" fill="{color}" />')
        curr_x += w

    # Progress bar with rounded container
    progress_bar = f"""
    <g transform="translate(25, 52)">
      <mask id="bar-mask">
        <rect x="0" y="0" width="{bar_width}" height="8" rx="4" fill="white" />
      </mask>
      <g mask="url(#bar-mask)">
        {''.join(bar_svg)}
      </g>
    </g>
    """

    # 2-column language list
    items_svg = []
    col_width = 165
    for idx, (lname, lsize) in enumerate(sorted_langs):
        col = idx % 2
        row = idx // 2
        x = col * col_width
        y = row * 26
        pct = (lsize / total_bytes) * 100
        color = lang_colors.get(lname, "#8FA3BF")
        items_svg.append(f"""
        <g transform="translate({x}, {y})">
          <circle cx="5" cy="5" r="5" fill="{color}" />
          <text class="lang-name" x="16" y="9">{lname}</text>
          <text class="lang-pct" x="145" y="9" text-anchor="end">{pct:.1f}%</text>
        </g>
        """)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="380" height="195" viewBox="0 0 380 195" fill="none" role="img" aria-label="{name}">
  <style>
    .header {{ font: 600 18px 'Segoe UI', Ubuntu, Sans-Serif; fill: #4DA3FF; }}
    .lang-name {{ font: 600 12px 'Segoe UI', Ubuntu, Sans-Serif; fill: #C9D6EA; }}
    .lang-pct {{ font: 400 12px 'Segoe UI', Ubuntu, Sans-Serif; fill: #8FA3BF; }}
    .bg {{ fill: #0B1220; stroke: #1B2A47; stroke-width: 1px; rx: 14px; }}
  </style>
  <rect class="bg" x="0.5" y="0.5" width="379" height="194" />
  
  <g transform="translate(25, 32)">
    <text class="header" x="0" y="0">{name}</text>
  </g>
  
  {progress_bar}
  
  <g transform="translate(25, 78)">
    {''.join(items_svg)}
  </g>
</svg>
"""
    return svg.strip()


def render_calendar_svg(user_data):
    cal = user_data["contributionsCollection"]["contributionCalendar"]
    total = cal.get("totalContributions", 0)
    weeks = cal.get("weeks", [])
    
    CELL = 11
    GAP = 3
    PITCH = CELL + GAP
    LEFT = 36
    TOP = 46
    
    LEVELS = ["#161F33", "#1C3A66", "#25519B", "#2E7DFF", "#7FB3FF"]
    
    def get_tier(c):
        if c <= 0: return 0
        if c <= 2: return 1
        if c <= 6: return 2
        if c <= 12: return 3
        return 4

    cells_svg = []
    month_labels = []
    last_month = None

    MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    for w_idx, week in enumerate(weeks):
        days = week.get("contributionDays", [])
        if not days:
            continue
        
        # Month label detection
        first_d = date.fromisoformat(days[0]["date"])
        if first_d.day <= 7 and first_d.month != last_month:
            last_month = first_d.month
            m_x = LEFT + w_idx * PITCH
            m_name = MONTH_NAMES[first_d.month - 1]
            month_labels.append(f'<text class="month-label" x="{m_x}" y="{TOP - 8}">{m_name}</text>')
        
        for d in days:
            d_obj = date.fromisoformat(d["date"])
            # weekday: Mon=0 .. Sun=6 -> Sun=0, Mon=1 .. Sat=6
            row = (d_obj.weekday() + 1) % 7
            cnt = d.get("contributionCount", 0)
            color = LEVELS[get_tier(cnt)]
            x = LEFT + w_idx * PITCH
            y = TOP + row * PITCH
            cells_svg.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" fill="{color}"><title>{d["date"]}: {cnt} contributions</title></rect>')

    width = LEFT + len(weeks) * PITCH + 20
    height = 170

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" role="img" aria-label="Contribution Activity">
  <style>
    .title {{ font: 700 13px 'Segoe UI', Ubuntu, Sans-Serif; fill: #4DA3FF; letter-spacing: 0.5px; }}
    .subtitle {{ font: 400 12px 'Segoe UI', Ubuntu, Sans-Serif; fill: #8FA3BF; }}
    .month-label {{ font: 500 10px 'Segoe UI', Ubuntu, Sans-Serif; fill: #8FA3BF; }}
    .day-label {{ font: 500 9px 'Segoe UI', Ubuntu, Sans-Serif; fill: #8FA3BF; }}
    .legend-text {{ font: 400 10px 'Segoe UI', Ubuntu, Sans-Serif; fill: #8FA3BF; }}
    .bg {{ fill: #0B1220; stroke: #1B2A47; stroke-width: 1px; rx: 14px; }}
  </style>
  <rect class="bg" x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" />
  
  <!-- Header -->
  <g transform="translate(25, 24)">
    <text class="title" x="0" y="0">CONTRIBUTION ACTIVITY</text>
    <text class="subtitle" x="180" y="0">({total} contributions in the last year)</text>
  </g>
  
  <!-- Legend -->
  <g transform="translate({width - 165}, 20)">
    <text class="legend-text" x="0" y="4">Less</text>
    <rect x="28" y="-4" width="10" height="10" rx="2" fill="{LEVELS[0]}" />
    <rect x="42" y="-4" width="10" height="10" rx="2" fill="{LEVELS[1]}" />
    <rect x="56" y="-4" width="10" height="10" rx="2" fill="{LEVELS[2]}" />
    <rect x="70" y="-4" width="10" height="10" rx="2" fill="{LEVELS[3]}" />
    <rect x="84" y="-4" width="10" height="10" rx="2" fill="{LEVELS[4]}" />
    <text class="legend-text" x="100" y="4">More</text>
  </g>
  
  <!-- Day labels (Mon, Wed, Fri) -->
  <g transform="translate({LEFT - 8}, {TOP})">
    <text class="day-label" x="0" y="{1 * PITCH + 9}" text-anchor="end">Mon</text>
    <text class="day-label" x="0" y="{3 * PITCH + 9}" text-anchor="end">Wed</text>
    <text class="day-label" x="0" y="{5 * PITCH + 9}" text-anchor="end">Fri</text>
  </g>
  
  <!-- Month labels -->
  <g>
    {''.join(month_labels)}
  </g>
  
  <!-- Grid -->
  <g>
    {''.join(cells_svg)}
  </g>
</svg>
"""
    return svg.strip()


def main():
    os.makedirs("generated", exist_ok=True)
    print("Fetching user data...")
    user_data = fetch_data()
    
    print("Rendering generated/stats.svg...")
    stats_svg = render_stats_svg(user_data)
    with open("generated/stats.svg", "w", encoding="utf-8") as f:
        f.write(stats_svg + "\n")
        
    print("Rendering generated/top-langs.svg...")
    top_langs_svg = render_top_langs_svg(user_data)
    with open("generated/top-langs.svg", "w", encoding="utf-8") as f:
        f.write(top_langs_svg + "\n")
        
    print("Rendering generated/calendar.svg...")
    calendar_svg = render_calendar_svg(user_data)
    with open("generated/calendar.svg", "w", encoding="utf-8") as f:
        f.write(calendar_svg + "\n")

    print("Validating generated SVGs...")
    for path in ["generated/stats.svg", "generated/top-langs.svg", "generated/calendar.svg"]:
        ET.parse(path)
        print(f"  ✓ {path} is valid XML")

    print("All cards generated successfully!")


if __name__ == "__main__":
    main()
