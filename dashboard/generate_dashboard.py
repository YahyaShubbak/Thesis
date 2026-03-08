#!/usr/bin/env python3
"""
Generate the interactive Plotly thesis dashboard.

Reads history.json and achievements.json, creates Plotly charts,
and renders a self-contained HTML file via Jinja2 template.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

import plotly.graph_objects as go
from plotly.subplots import make_subplots

DASHBOARD_DIR = Path(__file__).resolve().parent
DATA_DIR = DASHBOARD_DIR / "data"
OUTPUT_DIR = DASHBOARD_DIR / "output"
TEMPLATE_FILE = DASHBOARD_DIR / "template.html"
HISTORY_FILE = DATA_DIR / "history.json"
ACHIEVEMENTS_FILE = DATA_DIR / "achievements.json"

# Dark theme colors
BG_COLOR = "#1a1a2e"
CARD_BG = "#16213e"
PLOT_BG = "#0f3460"
TEXT_COLOR = "#e0e0e0"
ACCENT = "#e94560"
ACCENT2 = "#0fa3b1"
GREEN = "#4ecca3"
RED = "#e94560"
GOLD = "#ffd700"

CHAPTER_COLORS = [
    "#e94560", "#0fa3b1", "#4ecca3", "#ffd700", "#ff6b6b",
    "#c084fc", "#fb923c", "#38bdf8", "#a3e635", "#f472b6", "#94a3b8",
]

TIER_COLORS = {
    "bronze": "#cd7f32",
    "silver": "#c0c0c0",
    "gold": "#ffd700",
    "diamond": "#b9f2ff",
}

PLOTLY_LAYOUT_DEFAULTS = dict(
    paper_bgcolor=BG_COLOR,
    plot_bgcolor=PLOT_BG,
    font=dict(color=TEXT_COLOR, family="Inter, system-ui, sans-serif"),
    margin=dict(l=50, r=30, t=50, b=40),
    hovermode="x unified",
    legend=dict(bgcolor="rgba(0,0,0,0.3)", bordercolor="rgba(255,255,255,0.1)", borderwidth=1),
)

AXIS_STYLE = dict(gridcolor="rgba(255,255,255,0.08)", zerolinecolor="rgba(255,255,255,0.1)")


def load_data():
    with open(HISTORY_FILE) as f:
        history = json.load(f)

    achievements = {"achievements": {}, "total": 0, "unlocked": 0, "newly_unlocked": [], "all_definitions": []}
    if ACHIEVEMENTS_FILE.exists():
        with open(ACHIEVEMENTS_FILE) as f:
            achievements = json.load(f)

    return history, achievements


def make_cumulative_word_chart(daily, word_target):
    """Chart 1: Cumulative word count over time with milestone markers."""
    dates = [d["date"] for d in daily]
    words = [d["total_words"] for d in daily]

    fig = go.Figure()

    # Main word count line
    fig.add_trace(go.Scatter(
        x=dates, y=words,
        mode="lines+markers",
        name="Total Words",
        line=dict(color=GREEN, width=3),
        marker=dict(size=4),
        fill="tozeroy",
        fillcolor="rgba(78, 204, 163, 0.1)",
    ))

    # Milestone lines
    milestones = [
        (10000, "10k", "rgba(255,255,255,0.2)"),
        (25000, "25k", "rgba(255,255,255,0.2)"),
        (40000, "40k", "rgba(255,255,255,0.2)"),
        (50000, "50k — TARGET", GOLD),
    ]
    for val, label, color in milestones:
        if val <= max(words) * 1.5 or val == word_target:
            fig.add_hline(y=val, line_dash="dash", line_color=color,
                          annotation_text=label, annotation_position="top right",
                          annotation_font_color=color)

    fig.update_layout(
        **PLOTLY_LAYOUT_DEFAULTS,
        title=dict(text="📝 Cumulative Word Count", font=dict(size=18)),
        yaxis_title="Words",
        xaxis=dict(
            rangeslider=dict(visible=True, bgcolor=PLOT_BG),
            rangeselector=dict(
                buttons=[
                    dict(count=7, label="1W", step="day", stepmode="backward"),
                    dict(count=1, label="1M", step="month", stepmode="backward"),
                    dict(count=3, label="3M", step="month", stepmode="backward"),
                    dict(count=6, label="6M", step="month", stepmode="backward"),
                    dict(count=1, label="1Y", step="year", stepmode="backward"),
                    dict(step="all", label="All"),
                ],
                bgcolor=CARD_BG,
                activecolor=ACCENT,
                font=dict(color=TEXT_COLOR),
            ),
            gridcolor="rgba(255,255,255,0.08)",
        ),
        yaxis=dict(gridcolor="rgba(255,255,255,0.08)"),
    )

    return fig.to_html(full_html=False, include_plotlyjs=False, div_id="chart-words")


def _aggregate_daily(daily, period="daily"):
    """Aggregate daily data into weekly or monthly buckets."""
    if period == "daily":
        return daily

    from collections import defaultdict
    buckets = defaultdict(lambda: {"words_added": 0, "words_deleted": 0})

    for d in daily:
        dt = datetime.strptime(d["date"], "%Y-%m-%d")
        if period == "weekly":
            # ISO week start (Monday)
            week_start = dt - timedelta(days=dt.weekday())
            key = week_start.strftime("%Y-%m-%d")
        elif period == "monthly":
            key = dt.strftime("%Y-%m-01")
        else:
            key = d["date"]

        buckets[key]["words_added"] += d.get("words_added", 0)
        buckets[key]["words_deleted"] += d.get("words_deleted", 0)

    result = []
    for date_key in sorted(buckets.keys()):
        result.append({
            "date": date_key,
            "words_added": buckets[date_key]["words_added"],
            "words_deleted": buckets[date_key]["words_deleted"],
        })
    return result


def make_daily_activity_chart(daily):
    """Chart 2: Daily writing activity (added/deleted) with aggregation toggle."""
    # We'll create three traces for each aggregation and use updatemenus to toggle
    figs_data = {}
    for period in ["daily", "weekly", "monthly"]:
        agg = _aggregate_daily(daily, period)
        figs_data[period] = {
            "dates": [d["date"] for d in agg],
            "added": [d["words_added"] for d in agg],
            "deleted": [-d["words_deleted"] for d in agg],  # negative for below-axis
        }

    fig = go.Figure()

    # Add all three versions, hide weekly and monthly by default
    for i, period in enumerate(["daily", "weekly", "monthly"]):
        visible = (period == "daily")
        fig.add_trace(go.Bar(
            x=figs_data[period]["dates"],
            y=figs_data[period]["added"],
            name=f"Added ({period})",
            marker_color=GREEN,
            visible=visible,
            showlegend=visible,
        ))
        fig.add_trace(go.Bar(
            x=figs_data[period]["dates"],
            y=figs_data[period]["deleted"],
            name=f"Deleted ({period})",
            marker_color=RED,
            visible=visible,
            showlegend=visible,
        ))

    # Create visibility toggles (6 traces total: 2 per period)
    buttons = []
    for idx, period in enumerate(["daily", "weekly", "monthly"]):
        vis = [False] * 6
        vis[idx * 2] = True
        vis[idx * 2 + 1] = True
        buttons.append(dict(
            label=period.capitalize(),
            method="update",
            args=[{"visible": vis},
                  {"showlegend": True}],
        ))

    fig.update_layout(
        **PLOTLY_LAYOUT_DEFAULTS,
        title=dict(text="📊 Daily Writing Activity", font=dict(size=18)),
        barmode="relative",
        yaxis_title="Words",
        updatemenus=[dict(
            type="buttons",
            direction="right",
            x=0.0, y=1.15,
            buttons=buttons,
            bgcolor=CARD_BG,
            font=dict(color=TEXT_COLOR),
            bordercolor="rgba(255,255,255,0.2)",
        )],
        xaxis=dict(gridcolor="rgba(255,255,255,0.08)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.08)"),
    )

    return fig.to_html(full_html=False, include_plotlyjs=False, div_id="chart-activity")


def make_chapter_breakdown_chart(daily):
    """Chart 3: Stacked area chart of chapter word counts over time."""
    dates = [d["date"] for d in daily]
    chapters_data = {}

    for d in daily:
        for ch_name, ch_words in d.get("chapters", {}).items():
            if ch_name not in chapters_data:
                chapters_data[ch_name] = []
            chapters_data[ch_name].append(ch_words)

    # Pad shorter arrays
    for ch_name in chapters_data:
        while len(chapters_data[ch_name]) < len(dates):
            chapters_data[ch_name].append(0)

    fig = go.Figure()

    # Sort chapters by their order in the thesis
    chapter_order = [
        "Abstract", "Abbreviations", "Introduction", "Theory", "Experimental",
        "Results", "Discussion", "Outlook", "Acknowledgments", "Declaration", "Appendix",
    ]
    sorted_chapters = [c for c in chapter_order if c in chapters_data]
    remaining = [c for c in chapters_data if c not in sorted_chapters]
    sorted_chapters += remaining

    for i, ch_name in enumerate(sorted_chapters):
        color = CHAPTER_COLORS[i % len(CHAPTER_COLORS)]
        fig.add_trace(go.Scatter(
            x=dates,
            y=chapters_data[ch_name],
            name=ch_name,
            stackgroup="one",
            line=dict(width=0.5, color=color),
            fillcolor=color.replace(")", ", 0.6)").replace("rgb", "rgba") if "rgb" in color else color,
        ))

    fig.update_layout(
        **PLOTLY_LAYOUT_DEFAULTS,
        title=dict(text="📚 Chapter Breakdown", font=dict(size=18)),
        yaxis_title="Words",
        xaxis=dict(gridcolor="rgba(255,255,255,0.08)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.08)"),
    )

    return fig.to_html(full_html=False, include_plotlyjs=False, div_id="chart-chapters")


def make_asset_tracker_chart(daily):
    """Chart 4: Multi-line chart for figures, tables, equations, citations, sections."""
    dates = [d["date"] for d in daily]

    assets = [
        ("Figures", "figures", "#e94560"),
        ("Tables", "tables", "#ffd700"),
        ("Equations", "equations", "#0fa3b1"),
        ("Citations", "citations", "#4ecca3"),
        ("Sections", "sections", "#c084fc"),
    ]

    fig = go.Figure()
    for name, key, color in assets:
        values = [d.get(key, 0) for d in daily]
        fig.add_trace(go.Scatter(
            x=dates, y=values,
            mode="lines+markers",
            name=name,
            line=dict(color=color, width=2),
            marker=dict(size=3),
        ))

    fig.update_layout(
        **PLOTLY_LAYOUT_DEFAULTS,
        title=dict(text="📦 Asset Tracker", font=dict(size=18)),
        yaxis_title="Count",
        xaxis=dict(gridcolor="rgba(255,255,255,0.08)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.08)"),
    )

    return fig.to_html(full_html=False, include_plotlyjs=False, div_id="chart-assets")


def make_page_gauge(current_pages, page_target):
    """Chart 5: Page count gauge."""
    if current_pages is None:
        current_pages = 0

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=current_pages,
        number=dict(font=dict(size=48, color=TEXT_COLOR)),
        delta=dict(reference=page_target, valueformat=".0f", increasing=dict(color=GREEN), decreasing=dict(color=RED)),
        title=dict(text="Pages Written", font=dict(size=16, color=TEXT_COLOR)),
        gauge=dict(
            axis=dict(range=[0, page_target + 50], tickcolor=TEXT_COLOR),
            bar=dict(color=GREEN if current_pages < page_target else GOLD),
            bgcolor=PLOT_BG,
            bordercolor="rgba(255,255,255,0.1)",
            steps=[
                dict(range=[0, page_target * 0.5], color="rgba(233, 69, 96, 0.2)"),
                dict(range=[page_target * 0.5, page_target * 0.8], color="rgba(255, 215, 0, 0.2)"),
                dict(range=[page_target * 0.8, page_target], color="rgba(78, 204, 163, 0.2)"),
            ],
            threshold=dict(line=dict(color=GOLD, width=4), thickness=0.75, value=page_target),
        ),
    ))

    fig.update_layout(
        paper_bgcolor=BG_COLOR,
        font=dict(color=TEXT_COLOR),
        margin=dict(l=30, r=30, t=60, b=20),
        height=280,
    )

    return fig.to_html(full_html=False, include_plotlyjs=False, div_id="chart-gauge")


def make_git_heatmap(commits):
    """Chart 6: GitHub-style contribution heatmap."""
    from collections import Counter

    # Count commits per date
    date_counts = Counter(c["date"] for c in commits)

    if not date_counts:
        return "<div id='chart-heatmap'><p style='color:#888;text-align:center;'>No commit data yet</p></div>"

    # Build a full calendar from first to last date
    all_dates = sorted(date_counts.keys())
    start = datetime.strptime(all_dates[0], "%Y-%m-%d")
    end = datetime.strptime(all_dates[-1], "%Y-%m-%d")

    # Align to Monday
    start = start - timedelta(days=start.weekday())

    weeks = []
    week_labels = []
    day_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    current = start
    week_data = [0] * 7
    week_idx = 0

    z_data = [[] for _ in range(7)]  # 7 rows (days of week)
    x_labels = []
    hover_texts = [[] for _ in range(7)]

    while current <= end + timedelta(days=6):
        dow = current.weekday()
        date_str = current.strftime("%Y-%m-%d")
        count = date_counts.get(date_str, 0)

        if dow == 0:  # Monday = new week column
            x_labels.append(current.strftime("%b %d"))

        if len(z_data[dow]) < len(x_labels):
            z_data[dow].append(count)
            hover_texts[dow].append(f"{date_str}: {count} commits")
        else:
            # Extend if needed
            while len(z_data[dow]) < len(x_labels):
                z_data[dow].append(0)
                hover_texts[dow].append("")
            if len(z_data[dow]) == len(x_labels):
                z_data[dow][-1] = count
                hover_texts[dow][-1] = f"{date_str}: {count} commits"

        current += timedelta(days=1)

    # Pad all rows to same length
    max_len = max(len(row) for row in z_data)
    for i in range(7):
        while len(z_data[i]) < max_len:
            z_data[i].append(0)
            hover_texts[i].append("")

    fig = go.Figure(go.Heatmap(
        z=z_data,
        x=x_labels,
        y=day_labels,
        hovertext=hover_texts,
        hoverinfo="text",
        colorscale=[
            [0, PLOT_BG],
            [0.01, "rgba(78, 204, 163, 0.2)"],
            [0.25, "rgba(78, 204, 163, 0.4)"],
            [0.5, "rgba(78, 204, 163, 0.6)"],
            [0.75, "rgba(78, 204, 163, 0.8)"],
            [1.0, GREEN],
        ],
        showscale=False,
        xgap=3,
        ygap=3,
    ))

    fig.update_layout(
        paper_bgcolor=BG_COLOR,
        plot_bgcolor=BG_COLOR,
        font=dict(color=TEXT_COLOR),
        title=dict(text="🗓️ Git Activity", font=dict(size=18)),
        margin=dict(l=50, r=20, t=50, b=20),
        height=220,
        yaxis=dict(autorange="reversed"),
        xaxis=dict(
            showgrid=False,
            nticks=20,
        ),
    )

    return fig.to_html(full_html=False, include_plotlyjs=False, div_id="chart-heatmap")


def generate():
    """Main generation routine."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    history, achievements_data = load_data()
    daily = history.get("daily", [])
    commits = history.get("commits", [])
    word_target = history.get("word_target", 50000)
    page_target = history.get("page_target", 150)
    current_pages = history.get("current_pages")

    print("Generating charts...")

    # Generate all chart HTML fragments
    chart_words = make_cumulative_word_chart(daily, word_target)
    chart_activity = make_daily_activity_chart(daily)
    chart_chapters = make_chapter_breakdown_chart(daily)
    chart_assets = make_asset_tracker_chart(daily)
    chart_gauge = make_page_gauge(current_pages, page_target)
    chart_heatmap = make_git_heatmap(commits)

    # Prepare achievement data for template
    all_achievements = achievements_data.get("achievements", {})
    total_achievements = achievements_data.get("total", 0)
    unlocked_count = achievements_data.get("unlocked", 0)
    newly_unlocked = achievements_data.get("newly_unlocked", [])

    # Summary stats
    latest = daily[-1] if daily else {}
    stats = {
        "total_words": latest.get("total_words", 0),
        "figures": latest.get("figures", 0),
        "tables": latest.get("tables", 0),
        "equations": latest.get("equations", 0),
        "citations": latest.get("citations", 0),
        "sections": latest.get("sections", 0),
        "pages": current_pages or "N/A",
        "total_commits": len(commits),
        "days_tracked": len(daily),
        "word_target": word_target,
        "page_target": page_target,
        "progress_pct": round(latest.get("total_words", 0) / word_target * 100, 1) if word_target else 0,
    }

    # Read template
    with open(TEMPLATE_FILE) as f:
        template_str = f.read()

    # Simple template rendering (avoiding Jinja2 dependency issues with {{ in JS)
    # We'll inject data as JSON into script tags
    html = template_str
    html = html.replace("{{CHART_WORDS}}", chart_words)
    html = html.replace("{{CHART_ACTIVITY}}", chart_activity)
    html = html.replace("{{CHART_CHAPTERS}}", chart_chapters)
    html = html.replace("{{CHART_ASSETS}}", chart_assets)
    html = html.replace("{{CHART_GAUGE}}", chart_gauge)
    html = html.replace("{{CHART_HEATMAP}}", chart_heatmap)
    html = html.replace("{{STATS_JSON}}", json.dumps(stats))
    html = html.replace("{{ACHIEVEMENTS_JSON}}", json.dumps(all_achievements))
    html = html.replace("{{NEWLY_UNLOCKED_JSON}}", json.dumps(newly_unlocked))
    html = html.replace("{{TOTAL_ACHIEVEMENTS}}", str(total_achievements))
    html = html.replace("{{UNLOCKED_COUNT}}", str(unlocked_count))
    html = html.replace("{{GENERATED_AT}}", history.get("generated_at", "unknown"))

    output_path = OUTPUT_DIR / "index.html"
    with open(output_path, "w") as f:
        f.write(html)

    print(f"Dashboard written to {output_path}")
    print(f"  Stats: {stats['total_words']} words, {stats['figures']} figures, "
          f"{stats['equations']} equations, {stats['citations']} citations")
    print(f"  Achievements: {unlocked_count}/{total_achievements}")


if __name__ == "__main__":
    generate()
