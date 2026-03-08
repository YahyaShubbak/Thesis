#!/usr/bin/env python3
"""
Collect thesis writing metrics from git history.

Walks all commits, extracts .tex files, counts words/figures/tables/equations/
citations/sections per day, and stores results in data/history.json.
Incremental: skips commits already processed.
"""

import json
import os
import re
import subprocess
import sys
import tempfile
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = Path(__file__).resolve().parent / "data"
HISTORY_FILE = DATA_DIR / "history.json"

# .tex content files to track (relative to repo root)
CONTENT_FILES = [
    "content/00_abstract.tex",
    "content/01_introduction.tex",
    "content/02_theory.tex",
    "content/03_experimental.tex",
    "content/04_results.tex",
    "content/05_results_discussion.tex",
    "content/07_ausblick.tex",
    "content/08_danksagung.tex",
    "content/09_eigenstaendigkeit.tex",
    "content/a_anhang.tex",
    "content/Abbreviations.tex",
]

# Friendly chapter names for display
CHAPTER_NAMES = {
    "content/00_abstract.tex": "Abstract",
    "content/01_introduction.tex": "Introduction",
    "content/02_theory.tex": "Theory",
    "content/03_experimental.tex": "Experimental",
    "content/04_results.tex": "Results",
    "content/05_results_discussion.tex": "Discussion",
    "content/07_ausblick.tex": "Outlook",
    "content/08_danksagung.tex": "Acknowledgments",
    "content/09_eigenstaendigkeit.tex": "Declaration",
    "content/a_anhang.tex": "Appendix",
    "content/Abbreviations.tex": "Abbreviations",
}


def git(*args, cwd=None):
    """Run a git command and return stdout."""
    result = subprocess.run(
        ["git"] + list(args),
        capture_output=True,
        text=True,
        cwd=cwd or REPO_ROOT,
    )
    return result.stdout.strip()


def get_all_commits():
    """Get all commits in chronological order: [(sha, datetime_str, hour, weekday)]."""
    log = git("log", "--format=%H %aI", "--reverse")
    if not log:
        return []
    commits = []
    for line in log.splitlines():
        parts = line.split(" ", 1)
        if len(parts) == 2:
            sha, iso_date = parts
            try:
                dt = datetime.fromisoformat(iso_date)
                commits.append((sha, dt.strftime("%Y-%m-%d"), dt.hour, dt.weekday()))
            except ValueError:
                continue
    return commits


def get_file_at_commit(sha, filepath):
    """Get contents of a file at a specific commit, or None if it doesn't exist."""
    result = subprocess.run(
        ["git", "show", f"{sha}:{filepath}"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    if result.returncode == 0:
        return result.stdout
    return None


# ---------------------------------------------------------------------------
# Word counting: pure-Python fallback (no texcount dependency)
# ---------------------------------------------------------------------------

# Patterns to strip from LaTeX before counting words
_STRIP_PATTERNS = [
    re.compile(r"\\begin\{(?:equation|align|gather|multline|math|displaymath)\*?\}.*?\\end\{(?:equation|align|gather|multline|math|displaymath)\*?\}", re.DOTALL),
    re.compile(r"\$\$.*?\$\$", re.DOTALL),
    re.compile(r"\$.*?\$"),
    re.compile(r"\\\[.*?\\\]", re.DOTALL),
    re.compile(r"\\(?:label|ref|eqref|cref|Cref|autoref|pageref|cite|parencite|textcite|autocite|citeauthor|citeyear|nocite|printbibliography)\{[^}]*\}"),
    re.compile(r"\\(?:includegraphics|input|include|bibliography|graphicspath|usepackage|documentclass|newcommand|renewcommand|DeclareSIUnit|sisetup)(?:\[[^\]]*\])?\{[^}]*\}"),
    re.compile(r"\\(?:begin|end)\{[^}]*\}(?:\[[^\]]*\])?(?:\{[^}]*\})?"),
    re.compile(r"\\(?:chapter|section|subsection|subsubsection|paragraph)\*?\{([^}]*)\}", re.DOTALL),
    re.compile(r"\\(?:textbf|textit|emph|underline|textrm|textsc|textsf|texttt)\{([^}]*)\}"),
    re.compile(r"\\(?:SI|si|qty|unit|num)\{[^}]*\}(?:\{[^}]*\})?"),
    re.compile(r"\\[a-zA-Z]+"),
    re.compile(r"[{}\\~^_&%#]"),
]


def count_words_simple(tex_content):
    """Count words in LaTeX content using a simple strip-and-count approach."""
    if not tex_content:
        return 0
    text = re.sub(r"%.*$", "", tex_content, flags=re.MULTILINE)
    for pat in _STRIP_PATTERNS:
        text = pat.sub(" ", text)
    words = text.split()
    words = [w for w in words if len(w) > 1 or w.isalpha()]
    return len(words)


def try_texcount(tex_content):
    """Try using texcount if available, fall back to simple counting."""
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".tex", delete=False) as f:
            f.write(tex_content)
            f.flush()
            result = subprocess.run(
                ["texcount", "-1", "-sum", "-merge", "-q", f.name],
                capture_output=True,
                text=True,
                timeout=10,
            )
            os.unlink(f.name)
            if result.returncode == 0:
                # texcount -1 outputs a single number
                for line in result.stdout.strip().splitlines():
                    line = line.strip()
                    # Take the first number found
                    m = re.match(r"(\d+)", line)
                    if m:
                        return int(m.group(1))
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        pass
    return count_words_simple(tex_content)


def count_words(tex_content):
    """Count words - tries texcount first, falls back to pure Python."""
    if not tex_content:
        return 0
    return try_texcount(tex_content)


# ---------------------------------------------------------------------------
# Metric extraction via regex
# ---------------------------------------------------------------------------

def count_figures(tex_content):
    if not tex_content:
        return 0
    envs = len(re.findall(r"\\begin\{figure\}", tex_content))
    graphics = len(re.findall(r"\\includegraphics", tex_content))
    return max(envs, graphics)


def count_tables(tex_content):
    if not tex_content:
        return 0
    return len(re.findall(r"\\begin\{table\}", tex_content))


def count_equations(tex_content):
    if not tex_content:
        return 0
    envs = re.findall(
        r"\\begin\{(?:equation|align|gather|multline|displaymath)\*?\}", tex_content
    )
    display = re.findall(r"\\\[", tex_content)
    # Don't count inline $ $ as equations
    return len(envs) + len(display)


def count_citations(tex_content):
    """Count unique citation keys."""
    if not tex_content:
        return set()
    keys = set()
    for m in re.finditer(
        r"\\(?:cite|parencite|textcite|autocite|citeauthor|citeyear|nocite)\{([^}]+)\}",
        tex_content,
    ):
        for key in m.group(1).split(","):
            key = key.strip()
            if key:
                keys.add(key)
    return keys


def count_sections(tex_content):
    if not tex_content:
        return 0
    return len(
        re.findall(r"\\(?:chapter|section|subsection|subsubsection)\*?\{", tex_content)
    )


def extract_metrics_for_commit(sha):
    """Extract all metrics for a single commit by reading .tex files."""
    all_text = ""
    chapter_words = {}
    total_figures = 0
    total_tables = 0
    total_equations = 0
    all_citations = set()
    total_sections = 0

    for filepath in CONTENT_FILES:
        content = get_file_at_commit(sha, filepath)
        if content is None:
            continue

        all_text += content + "\n"
        chapter_name = CHAPTER_NAMES.get(filepath, filepath)
        chapter_words[chapter_name] = count_words(content)
        total_figures += count_figures(content)
        total_tables += count_tables(content)
        total_equations += count_equations(content)
        all_citations |= count_citations(content)
        total_sections += count_sections(content)

    # Also check thesis.tex itself for any inline content
    thesis_tex = get_file_at_commit(sha, "thesis.tex")
    if thesis_tex:
        all_text += thesis_tex + "\n"

    total_words = sum(chapter_words.values())

    return {
        "total_words": total_words,
        "chapters": chapter_words,
        "figures": total_figures,
        "tables": total_tables,
        "equations": total_equations,
        "citations": len(all_citations),
        "citation_keys": sorted(all_citations),
        "sections": total_sections,
    }


def get_page_count():
    """Try to get page count from compiled PDF."""
    pdf_paths = [
        REPO_ROOT / "technical" / "build" / "thesis.pdf",
        REPO_ROOT / "thesis.pdf",
    ]
    for pdf_path in pdf_paths:
        if pdf_path.exists():
            try:
                result = subprocess.run(
                    ["pdfinfo", str(pdf_path)],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                if result.returncode == 0:
                    for line in result.stdout.splitlines():
                        if line.startswith("Pages:"):
                            return int(line.split(":")[1].strip())
            except (FileNotFoundError, subprocess.TimeoutExpired, ValueError):
                continue
    return None


def collect():
    """Main collection routine."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Load existing data
    existing = {"daily": [], "commits": [], "last_commit_sha": None, "current_pages": None}
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE) as f:
            existing = json.load(f)

    last_sha = existing.get("last_commit_sha")

    # Get all commits
    all_commits = get_all_commits()
    if not all_commits:
        print("No commits found.")
        return

    # Find where to start (incremental)
    start_idx = 0
    if last_sha:
        for i, (sha, _, _, _) in enumerate(all_commits):
            if sha == last_sha:
                start_idx = i + 1
                break

    new_commits = all_commits[start_idx:]
    if not new_commits:
        print("No new commits to process.")
        # Still update page count
        pages = get_page_count()
        if pages is not None:
            existing["current_pages"] = pages
            with open(HISTORY_FILE, "w") as f:
                json.dump(existing, f, indent=2)
        return

    print(f"Processing {len(new_commits)} new commits (of {len(all_commits)} total)...")

    # Group commits by day, keeping the LAST commit of each day
    daily_commits = {}
    commit_log = existing.get("commits", [])

    for sha, date_str, hour, weekday in new_commits:
        daily_commits[date_str] = (sha, hour, weekday)
        commit_log.append({
            "sha": sha,
            "date": date_str,
            "hour": hour,
            "weekday": weekday,
        })

        # Progress
        idx = new_commits.index((sha, date_str, hour, weekday))
        if (idx + 1) % 20 == 0 or idx == len(new_commits) - 1:
            print(f"  Indexed {idx + 1}/{len(new_commits)} commits...")

    # Build existing daily map
    daily_map = {}
    for entry in existing.get("daily", []):
        daily_map[entry["date"]] = entry

    # Process each new day
    days_to_process = sorted(daily_commits.keys())
    print(f"Extracting metrics for {len(days_to_process)} days...")

    for i, date_str in enumerate(days_to_process):
        sha, hour, weekday = daily_commits[date_str]
        metrics = extract_metrics_for_commit(sha)
        daily_map[date_str] = {
            "date": date_str,
            "sha": sha,
            "hour": hour,
            "weekday": weekday,
            **metrics,
        }
        if (i + 1) % 10 == 0 or i == len(days_to_process) - 1:
            print(f"  Processed {i + 1}/{len(days_to_process)} days...")

    # Sort daily entries chronologically
    daily_sorted = [daily_map[k] for k in sorted(daily_map.keys())]

    # Compute deltas between consecutive days
    for i in range(len(daily_sorted)):
        if i == 0:
            daily_sorted[i]["words_added"] = daily_sorted[i]["total_words"]
            daily_sorted[i]["words_deleted"] = 0
        else:
            prev = daily_sorted[i - 1]["total_words"]
            curr = daily_sorted[i]["total_words"]
            net = curr - prev
            if net >= 0:
                daily_sorted[i]["words_added"] = net
                daily_sorted[i]["words_deleted"] = 0
            else:
                daily_sorted[i]["words_added"] = 0
                daily_sorted[i]["words_deleted"] = abs(net)

    # Page count from PDF (if available)
    pages = get_page_count()

    # Assemble output
    output = {
        "daily": daily_sorted,
        "commits": commit_log,
        "last_commit_sha": all_commits[-1][0],
        "current_pages": pages,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "word_target": 50000,
        "page_target": 150,
    }

    with open(HISTORY_FILE, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Done! {len(daily_sorted)} daily entries, {len(commit_log)} commits total.")
    print(f"  Current words: {daily_sorted[-1]['total_words']}")
    print(f"  Current figures: {daily_sorted[-1]['figures']}")
    print(f"  Current tables: {daily_sorted[-1]['tables']}")
    print(f"  Current citations: {daily_sorted[-1]['citations']}")
    if pages:
        print(f"  Current pages: {pages}")


if __name__ == "__main__":
    collect()
