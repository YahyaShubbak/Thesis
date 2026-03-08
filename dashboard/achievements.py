#!/usr/bin/env python3
"""
Achievement system for the thesis dashboard.

50 achievements across categories, Cookie-Clicker-inspired tone.
4 tiers: bronze, silver, gold, diamond.
Some achievements are "shadow" (hidden until unlocked).
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"
HISTORY_FILE = DATA_DIR / "history.json"
ACHIEVEMENTS_FILE = DATA_DIR / "achievements.json"


def _define_achievements():
    """Return list of all 50 achievement definitions."""
    return [
        # =====================================================================
        # WRITING MILESTONES (12)
        # =====================================================================
        {
            "id": "hello_world",
            "name": "Hello World",
            "description": "Write your first sentence.",
            "hint": "Every thesis starts with a single word...",
            "emoji": "👋",
            "category": "Writing",
            "tier": "bronze",
            "hidden": False,
        },
        {
            "id": "baby_steps",
            "name": "Baby Steps",
            "description": "Reach 100 words.",
            "hint": "Keep typing, you're almost there!",
            "emoji": "🐣",
            "category": "Writing",
            "tier": "bronze",
            "hidden": False,
        },
        {
            "id": "getting_warmed_up",
            "name": "Getting Warmed Up",
            "description": "500 words and counting.",
            "hint": "The keyboard is warming up...",
            "emoji": "🔥",
            "category": "Writing",
            "tier": "bronze",
            "hidden": False,
        },
        {
            "id": "first_thousand",
            "name": "The First Thousand",
            "description": "Four digits of pure knowledge.",
            "hint": "1,000 words — you could write a strong email!",
            "emoji": "🎯",
            "category": "Writing",
            "tier": "silver",
            "hidden": False,
        },
        {
            "id": "verbose",
            "name": "Verbose",
            "description": "5,000 words — you could fill a pamphlet.",
            "hint": "That's a solid blog post!",
            "emoji": "📝",
            "category": "Writing",
            "tier": "silver",
            "hidden": False,
        },
        {
            "id": "wordy_mcwordface",
            "name": "Wordy McWordface",
            "description": "10,000 words! That's a novella.",
            "hint": "Double digits of thousands!",
            "emoji": "📚",
            "category": "Writing",
            "tier": "silver",
            "hidden": False,
        },
        {
            "id": "halfway",
            "name": "Halfway There",
            "description": "25,000 words — the thesis is taking shape.",
            "hint": "Livin' on a prayer... and caffeine.",
            "emoji": "⚡",
            "category": "Writing",
            "tier": "gold",
            "hidden": False,
        },
        {
            "id": "unstoppable",
            "name": "Unstoppable Typist",
            "description": "40,000 words of relentless productivity.",
            "hint": "Your keyboard fears you.",
            "emoji": "🚀",
            "category": "Writing",
            "tier": "gold",
            "hidden": False,
        },
        {
            "id": "magnum_opus",
            "name": "The Magnum Opus",
            "description": "50,000 words — a proper thesis!",
            "hint": "You hit the target. Legend.",
            "emoji": "🏆",
            "category": "Writing",
            "tier": "gold",
            "hidden": False,
        },
        {
            "id": "novelist",
            "name": "The Novelist",
            "description": "60,000 words — you could publish this as a book.",
            "hint": "Publishers are calling...",
            "emoji": "📖",
            "category": "Writing",
            "tier": "diamond",
            "hidden": False,
        },
        {
            "id": "war_and_peace",
            "name": "War and Peace (Almost)",
            "description": "80,000 words — Tolstoy nods approvingly.",
            "hint": "Your thesis weighs more than your laptop.",
            "emoji": "⚔️",
            "category": "Writing",
            "tier": "diamond",
            "hidden": False,
        },
        {
            "id": "centennial",
            "name": "Centennial",
            "description": "100,000 words. A monument of science.",
            "hint": "You are become thesis, destroyer of free time.",
            "emoji": "💎",
            "category": "Writing",
            "tier": "diamond",
            "hidden": False,
        },

        # =====================================================================
        # EDITING & DELETION (5)
        # =====================================================================
        {
            "id": "backspace_warrior",
            "name": "Backspace Warrior",
            "description": "Delete 100 words in a single day.",
            "hint": "Sometimes you have to destroy to create.",
            "emoji": "⌫",
            "category": "Editing",
            "tier": "bronze",
            "hidden": False,
        },
        {
            "id": "kill_your_darlings",
            "name": "Kill Your Darlings",
            "description": "Delete 500 words in a single day.",
            "hint": "Faulkner would be proud.",
            "emoji": "🗡️",
            "category": "Editing",
            "tier": "silver",
            "hidden": False,
        },
        {
            "id": "scorched_earth",
            "name": "Scorched Earth",
            "description": "Delete 1,000 words in a single day.",
            "hint": "A fresh start, courtesy of the Delete key.",
            "emoji": "🔥",
            "category": "Editing",
            "tier": "gold",
            "hidden": False,
        },
        {
            "id": "net_negative",
            "name": "Net Negative",
            "description": "End a day with fewer words than you started.",
            "hint": "Negative progress is still progress... right?",
            "emoji": "📉",
            "category": "Editing",
            "tier": "silver",
            "hidden": False,
        },
        {
            "id": "the_editor",
            "name": "The Editor",
            "description": "Accumulate 5,000 total deleted words.",
            "hint": "You've killed a novella's worth of text.",
            "emoji": "✂️",
            "category": "Editing",
            "tier": "gold",
            "hidden": False,
        },

        # =====================================================================
        # FIGURES (6)
        # =====================================================================
        {
            "id": "first_figure",
            "name": "A Picture Says...",
            "description": "Add your first figure.",
            "hint": "...a thousand words you don't have to write!",
            "emoji": "🖼️",
            "category": "Figures",
            "tier": "bronze",
            "hidden": False,
        },
        {
            "id": "gallery_opening",
            "name": "Gallery Opening",
            "description": "5 figures — a small exhibition.",
            "hint": "Curating your scientific gallery.",
            "emoji": "🎨",
            "category": "Figures",
            "tier": "silver",
            "hidden": False,
        },
        {
            "id": "visual_storyteller",
            "name": "Visual Storyteller",
            "description": "10 figures tell a thousand words each.",
            "hint": "That's 10,000 words worth of pictures!",
            "emoji": "📊",
            "category": "Figures",
            "tier": "silver",
            "hidden": False,
        },
        {
            "id": "data_viz",
            "name": "Data Viz Enthusiast",
            "description": "20 figures — you love showing data.",
            "hint": "Why write when you can plot?",
            "emoji": "📈",
            "category": "Figures",
            "tier": "gold",
            "hidden": False,
        },
        {
            "id": "museum_curator",
            "name": "Museum Curator",
            "description": "30 figures — quite the collection.",
            "hint": "The Louvre called, they want their curator back.",
            "emoji": "🏛️",
            "category": "Figures",
            "tier": "gold",
            "hidden": False,
        },
        {
            "id": "pixel_perfectionist",
            "name": "Pixel Perfectionist",
            "description": "50 figures — a visual masterpiece.",
            "hint": "Your thesis is basically a picture book now.",
            "emoji": "✨",
            "category": "Figures",
            "tier": "diamond",
            "hidden": False,
        },

        # =====================================================================
        # TABLES (3)
        # =====================================================================
        {
            "id": "first_table",
            "name": "Tabled Discussion",
            "description": "Create your first table.",
            "hint": "Organized data is happy data.",
            "emoji": "📋",
            "category": "Tables",
            "tier": "bronze",
            "hidden": False,
        },
        {
            "id": "data_organizer",
            "name": "Data Organizer",
            "description": "3 tables of organized data.",
            "hint": "Structure brings clarity!",
            "emoji": "🗂️",
            "category": "Tables",
            "tier": "silver",
            "hidden": False,
        },
        {
            "id": "excellent",
            "name": "Excel-lent",
            "description": "5 tables — you love structure.",
            "hint": "Spreadsheet energy detected.",
            "emoji": "📊",
            "category": "Tables",
            "tier": "gold",
            "hidden": False,
        },

        # =====================================================================
        # EQUATIONS (5)
        # =====================================================================
        {
            "id": "emc2",
            "name": "E=mc²",
            "description": "Write your first equation.",
            "hint": "Physics intensifies.",
            "emoji": "🧮",
            "category": "Equations",
            "tier": "bronze",
            "hidden": False,
        },
        {
            "id": "math_inclined",
            "name": "Mathematically Inclined",
            "description": "10 equations — the math is mathing.",
            "hint": "Variables assemble!",
            "emoji": "📐",
            "category": "Equations",
            "tier": "silver",
            "hidden": False,
        },
        {
            "id": "proof_exercise",
            "name": "Proof Left as Exercise",
            "description": "25 equations — your reviewer trembles.",
            "hint": "The proof is left as an exercise to the reader.",
            "emoji": "🎓",
            "category": "Equations",
            "tier": "gold",
            "hidden": False,
        },
        {
            "id": "the_formula",
            "name": "The Formula",
            "description": "50 equations — physics thesis confirmed.",
            "hint": "You're basically deriving reality at this point.",
            "emoji": "⚗️",
            "category": "Equations",
            "tier": "gold",
            "hidden": False,
        },
        {
            "id": "maxwell_proud",
            "name": "Maxwell Would Be Proud",
            "description": "100 equations of pure elegance.",
            "hint": "You've out-equationed most textbooks.",
            "emoji": "⚡",
            "category": "Equations",
            "tier": "diamond",
            "hidden": False,
        },

        # =====================================================================
        # CITATIONS (5)
        # =====================================================================
        {
            "id": "citation_needed",
            "name": "Citation Needed",
            "description": "Add your first citation.",
            "hint": "[citation needed]",
            "emoji": "📎",
            "category": "Citations",
            "tier": "bronze",
            "hidden": False,
        },
        {
            "id": "well_read",
            "name": "Well-Read",
            "description": "25 unique citations — you've done your homework.",
            "hint": "Knowledge stands on the shoulders of papers.",
            "emoji": "📖",
            "category": "Citations",
            "tier": "silver",
            "hidden": False,
        },
        {
            "id": "literature_scholar",
            "name": "Literature Scholar",
            "description": "50 citations — your bibliography is thick.",
            "hint": "Your reference list needs its own chapter.",
            "emoji": "🏫",
            "category": "Citations",
            "tier": "gold",
            "hidden": False,
        },
        {
            "id": "shoulders_giants",
            "name": "Standing on Shoulders",
            "description": "100 citations — of giants.",
            "hint": "Newton, Einstein, and now your bibliography.",
            "emoji": "🗼",
            "category": "Citations",
            "tier": "gold",
            "hidden": False,
        },
        {
            "id": "walking_bibliography",
            "name": "Walking Bibliography",
            "description": "150 citations — you ARE the literature review.",
            "hint": "You've read more papers than your advisor.",
            "emoji": "🚶",
            "category": "Citations",
            "tier": "diamond",
            "hidden": False,
        },

        # =====================================================================
        # CHAPTER PROGRESS (5)
        # =====================================================================
        {
            "id": "abstract_thinker",
            "name": "Abstract Thinker",
            "description": "Write the abstract (>150 words).",
            "hint": "The elevator pitch of your PhD.",
            "emoji": "💭",
            "category": "Chapters",
            "tier": "silver",
            "hidden": False,
        },
        {
            "id": "and_so_it_begins",
            "name": "And So It Begins",
            "description": "Introduction exceeds 1,000 words.",
            "hint": "The journey of a thousand pages begins with an introduction.",
            "emoji": "🚪",
            "category": "Chapters",
            "tier": "silver",
            "hidden": False,
        },
        {
            "id": "theoretically_speaking",
            "name": "Theoretically Speaking",
            "description": "Theory chapter surpasses 3,000 words.",
            "hint": "In theory, there is no difference between theory and practice.",
            "emoji": "🧠",
            "category": "Chapters",
            "tier": "gold",
            "hidden": False,
        },
        {
            "id": "results_are_in",
            "name": "The Results Are In",
            "description": "Results chapter exceeds 2,000 words.",
            "hint": "And the data says...",
            "emoji": "🔬",
            "category": "Chapters",
            "tier": "gold",
            "hidden": False,
        },
        {
            "id": "the_end_is_nigh",
            "name": "The End Is Nigh",
            "description": "Outlook/conclusion has 500+ words.",
            "hint": "The light at the end of the tunnel!",
            "emoji": "🌅",
            "category": "Chapters",
            "tier": "silver",
            "hidden": False,
        },

        # =====================================================================
        # CONSISTENCY & STREAKS (4)
        # =====================================================================
        {
            "id": "daily_grind",
            "name": "Daily Grind",
            "description": "Write on 3 consecutive days.",
            "hint": "Consistency is key!",
            "emoji": "☕",
            "category": "Streaks",
            "tier": "bronze",
            "hidden": False,
        },
        {
            "id": "on_a_roll",
            "name": "On a Roll",
            "description": "Write on 7 consecutive days.",
            "hint": "A full week of productivity!",
            "emoji": "🎲",
            "category": "Streaks",
            "tier": "silver",
            "hidden": False,
        },
        {
            "id": "fortnight_focus",
            "name": "Fortnight of Focus",
            "description": "Write on 14 consecutive days.",
            "hint": "Two weeks straight. Impressive.",
            "emoji": "🔥",
            "category": "Streaks",
            "tier": "gold",
            "hidden": False,
        },
        {
            "id": "monthly_marathon",
            "name": "Monthly Marathon",
            "description": "Write on 30 consecutive days.",
            "hint": "You're basically a thesis-writing machine.",
            "emoji": "🏃",
            "category": "Streaks",
            "tier": "diamond",
            "hidden": False,
        },

        # =====================================================================
        # TIME-BASED (3)
        # =====================================================================
        {
            "id": "night_owl",
            "name": "Night Owl",
            "description": "Push a commit after midnight.",
            "hint": "The best ideas come at 2 AM... or do they?",
            "emoji": "🦉",
            "category": "Time",
            "tier": "bronze",
            "hidden": False,
        },
        {
            "id": "early_bird",
            "name": "Early Bird",
            "description": "Push a commit before 6 AM.",
            "hint": "The early physicist catches the... data?",
            "emoji": "🐦",
            "category": "Time",
            "tier": "silver",
            "hidden": False,
        },
        {
            "id": "weekend_warrior",
            "name": "Weekend Warrior",
            "description": "Commit on both Saturday and Sunday in the same weekend.",
            "hint": "Rest is for the defended.",
            "emoji": "⚔️",
            "category": "Time",
            "tier": "silver",
            "hidden": False,
        },

        # =====================================================================
        # SHADOW / SECRET ACHIEVEMENTS (7) — hidden until unlocked!
        # =====================================================================
        {
            "id": "shadow_1",
            "name": "???",
            "description": "???",
            "hint": "Some mysteries reveal themselves...",
            "emoji": "🥚",
            "category": "Shadow",
            "tier": "silver",
            "hidden": True,
            "_secret_name": "Oops",
            "_secret_description": "Have a net word count decrease of exactly 1 word.",
            "_secret_emoji": "🤭",
        },
        {
            "id": "shadow_2",
            "name": "???",
            "description": "???",
            "hint": "Try working on a very special day...",
            "emoji": "🥚",
            "category": "Shadow",
            "tier": "gold",
            "hidden": True,
            "_secret_name": "No Life",
            "_secret_description": "Commit on Christmas Day, New Year's Eve, or your birthday (Dec 25, Dec 31, Jan 1).",
            "_secret_emoji": "🎄",
        },
        {
            "id": "shadow_3",
            "name": "???",
            "description": "???",
            "hint": "Numbers are everywhere...",
            "emoji": "🥚",
            "category": "Shadow",
            "tier": "bronze",
            "hidden": True,
            "_secret_name": "Nice",
            "_secret_description": "Have exactly 69 citations, or a word count containing 1337.",
            "_secret_emoji": "😏",
        },
        {
            "id": "shadow_4",
            "name": "???",
            "description": "???",
            "hint": "What happens when nothing happens?",
            "emoji": "🥚",
            "category": "Shadow",
            "tier": "bronze",
            "hidden": True,
            "_secret_name": "Commit to Nothing",
            "_secret_description": "Make a commit that changes 0 words (LaTeX-only change, reformatting).",
            "_secret_emoji": "🫥",
        },
        {
            "id": "shadow_5",
            "name": "???",
            "description": "???",
            "hint": "Persistence has its own reward.",
            "emoji": "🥚",
            "category": "Shadow",
            "tier": "gold",
            "hidden": True,
            "_secret_name": "Resurrection",
            "_secret_description": "Come back and write after a gap of 30+ days.",
            "_secret_emoji": "🧟",
        },
        {
            "id": "shadow_6",
            "name": "???",
            "description": "???",
            "hint": "The dashboard remembers everything...",
            "emoji": "🥚",
            "category": "Shadow",
            "tier": "silver",
            "hidden": True,
            "_secret_name": "The Observer",
            "_secret_description": "Have more than 100 total commits.",
            "_secret_emoji": "👁️",
        },
        {
            "id": "shadow_7",
            "name": "???",
            "description": "???",
            "hint": "All work and no play?",
            "emoji": "🥚",
            "category": "Shadow",
            "tier": "diamond",
            "hidden": True,
            "_secret_name": "All-Nighter",
            "_secret_description": "Have commits at 11 PM, midnight, 1 AM, 2 AM, and 3 AM (across all history).",
            "_secret_emoji": "😵",
        },
    ]


def _compute_streaks(daily_entries):
    """Compute writing streaks from daily entries."""
    if not daily_entries:
        return 0

    dates = sorted(set(e["date"] for e in daily_entries if e.get("total_words", 0) > 0))
    if not dates:
        return 0

    max_streak = 1
    current_streak = 1
    for i in range(1, len(dates)):
        d1 = datetime.strptime(dates[i - 1], "%Y-%m-%d")
        d2 = datetime.strptime(dates[i], "%Y-%m-%d")
        if (d2 - d1).days == 1:
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 1

    return max_streak


def _compute_max_gap(daily_entries):
    """Compute the maximum gap in days between consecutive entries."""
    dates = sorted(set(e["date"] for e in daily_entries))
    if len(dates) < 2:
        return 0
    max_gap = 0
    for i in range(1, len(dates)):
        d1 = datetime.strptime(dates[i - 1], "%Y-%m-%d")
        d2 = datetime.strptime(dates[i], "%Y-%m-%d")
        gap = (d2 - d1).days
        max_gap = max(max_gap, gap)
    return max_gap


def _has_comeback_after_gap(daily_entries, gap_days=30):
    """Check if there's a writing day after a gap of gap_days+."""
    dates = sorted(set(e["date"] for e in daily_entries))
    if len(dates) < 2:
        return False
    for i in range(1, len(dates)):
        d1 = datetime.strptime(dates[i - 1], "%Y-%m-%d")
        d2 = datetime.strptime(dates[i], "%Y-%m-%d")
        if (d2 - d1).days >= gap_days:
            return True
    return False


def check_achievements(history_data):
    """
    Evaluate all achievements against the history data.
    Returns dict of {achievement_id: {"unlocked": bool, "unlock_date": str or None, ...}}
    """
    daily = history_data.get("daily", [])
    commits = history_data.get("commits", [])

    if not daily:
        return {}

    latest = daily[-1]
    total_words = latest.get("total_words", 0)
    figures = latest.get("figures", 0)
    tables = latest.get("tables", 0)
    equations = latest.get("equations", 0)
    citations = latest.get("citations", 0)
    chapters = latest.get("chapters", {})

    # Cumulative deleted words
    cumulative_deleted = sum(d.get("words_deleted", 0) for d in daily)

    # Max single-day deletion
    max_daily_deleted = max((d.get("words_deleted", 0) for d in daily), default=0)

    # Net negative day
    has_net_negative = any(d.get("words_deleted", 0) > d.get("words_added", 0) for d in daily)

    # Streaks
    max_streak = _compute_streaks(daily)

    # Commit hours
    commit_hours = set(c.get("hour", 12) for c in commits)

    # Commit dates and weekdays
    commit_dates = [c.get("date", "") for c in commits]
    commit_weekdays_by_date = {}
    for c in commits:
        d = c.get("date", "")
        wd = c.get("weekday", 0)
        commit_weekdays_by_date[d] = wd

    # Weekend warrior: check for Sat+Sun in same weekend
    has_weekend_warrior = False
    saturdays = set()
    sundays = set()
    for c in commits:
        wd = c.get("weekday", 0)
        d = c.get("date", "")
        if wd == 5:  # Saturday
            saturdays.add(d)
        elif wd == 6:  # Sunday
            sundays.add(d)
    for sat_str in saturdays:
        sat = datetime.strptime(sat_str, "%Y-%m-%d")
        sun = sat + timedelta(days=1)
        if sun.strftime("%Y-%m-%d") in sundays:
            has_weekend_warrior = True
            break

    # Night owl (commit after midnight, i.e., hour 0-3)
    has_night_owl = any(h in commit_hours for h in [0, 1, 2, 3])
    # Early bird (commit before 6 AM, i.e., hour 4-5)
    has_early_bird = any(h in commit_hours for h in [4, 5])

    # Holiday commits
    holiday_dates = set()
    for d in commit_dates:
        if d.endswith("-12-25") or d.endswith("-12-31") or d.endswith("-01-01"):
            holiday_dates.add(d)
    has_holiday = len(holiday_dates) > 0

    # Shadow: exact -1
    has_exact_minus_one = any(
        d.get("words_deleted", 0) - d.get("words_added", 0) == 1
        and d.get("words_deleted", 0) > 0
        for d in daily
    )

    # Shadow: nice numbers
    has_nice = citations == 69 or "1337" in str(total_words)

    # Shadow: commit that changes 0 words
    has_zero_change = any(
        d.get("words_added", 0) == 0 and d.get("words_deleted", 0) == 0
        for d in daily[1:]  # skip first entry
    )

    # Shadow: comeback after 30+ day gap
    has_comeback = _has_comeback_after_gap(daily, 30)

    # Shadow: 100+ commits
    has_observer = len(commits) >= 100

    # Shadow: all-nighter (commits at 23, 0, 1, 2, 3)
    all_nighter_hours = {23, 0, 1, 2, 3}
    has_all_nighter = all_nighter_hours.issubset(commit_hours)

    # Chapter word counts
    abstract_words = chapters.get("Abstract", 0)
    intro_words = chapters.get("Introduction", 0)
    theory_words = chapters.get("Theory", 0)
    results_words = chapters.get("Results", 0) + chapters.get("Discussion", 0)
    outlook_words = chapters.get("Outlook", 0)

    # Build condition map
    conditions = {
        # Writing milestones
        "hello_world": total_words >= 10,
        "baby_steps": total_words >= 100,
        "getting_warmed_up": total_words >= 500,
        "first_thousand": total_words >= 1000,
        "verbose": total_words >= 5000,
        "wordy_mcwordface": total_words >= 10000,
        "halfway": total_words >= 25000,
        "unstoppable": total_words >= 40000,
        "magnum_opus": total_words >= 50000,
        "novelist": total_words >= 60000,
        "war_and_peace": total_words >= 80000,
        "centennial": total_words >= 100000,

        # Editing
        "backspace_warrior": max_daily_deleted >= 100,
        "kill_your_darlings": max_daily_deleted >= 500,
        "scorched_earth": max_daily_deleted >= 1000,
        "net_negative": has_net_negative,
        "the_editor": cumulative_deleted >= 5000,

        # Figures
        "first_figure": figures >= 1,
        "gallery_opening": figures >= 5,
        "visual_storyteller": figures >= 10,
        "data_viz": figures >= 20,
        "museum_curator": figures >= 30,
        "pixel_perfectionist": figures >= 50,

        # Tables
        "first_table": tables >= 1,
        "data_organizer": tables >= 3,
        "excellent": tables >= 5,

        # Equations
        "emc2": equations >= 1,
        "math_inclined": equations >= 10,
        "proof_exercise": equations >= 25,
        "the_formula": equations >= 50,
        "maxwell_proud": equations >= 100,

        # Citations
        "citation_needed": citations >= 1,
        "well_read": citations >= 25,
        "literature_scholar": citations >= 50,
        "shoulders_giants": citations >= 100,
        "walking_bibliography": citations >= 150,

        # Chapters
        "abstract_thinker": abstract_words >= 150,
        "and_so_it_begins": intro_words >= 1000,
        "theoretically_speaking": theory_words >= 3000,
        "results_are_in": results_words >= 2000,
        "the_end_is_nigh": outlook_words >= 500,

        # Streaks
        "daily_grind": max_streak >= 3,
        "on_a_roll": max_streak >= 7,
        "fortnight_focus": max_streak >= 14,
        "monthly_marathon": max_streak >= 30,

        # Time-based
        "night_owl": has_night_owl,
        "early_bird": has_early_bird,
        "weekend_warrior": has_weekend_warrior,

        # Shadow
        "shadow_1": has_exact_minus_one,
        "shadow_2": has_holiday,
        "shadow_3": has_nice,
        "shadow_4": has_zero_change,
        "shadow_5": has_comeback,
        "shadow_6": has_observer,
        "shadow_7": has_all_nighter,
    }

    # Find unlock dates (first date where condition became true)
    # We iterate through daily data chronologically
    achievements_defs = {a["id"]: a for a in _define_achievements()}
    results = {}

    for ach_id, unlocked in conditions.items():
        ach_def = achievements_defs.get(ach_id, {})
        result = {
            "id": ach_id,
            "unlocked": unlocked,
            "unlock_date": None,
            "name": ach_def.get("name", "???"),
            "description": ach_def.get("description", "???"),
            "hint": ach_def.get("hint", ""),
            "emoji": ach_def.get("emoji", "🥚"),
            "category": ach_def.get("category", ""),
            "tier": ach_def.get("tier", "bronze"),
            "hidden": ach_def.get("hidden", False),
        }

        # For hidden achievements that are unlocked, reveal their real info
        if unlocked and ach_def.get("hidden"):
            result["name"] = ach_def.get("_secret_name", result["name"])
            result["description"] = ach_def.get("_secret_description", result["description"])
            result["emoji"] = ach_def.get("_secret_emoji", result["emoji"])

        # Try to find the unlock date by scanning daily data
        if unlocked:
            result["unlock_date"] = _find_unlock_date(ach_id, daily, commits, conditions)

        results[ach_id] = result

    return results


def _find_unlock_date(ach_id, daily, commits, conditions):
    """Heuristic: find the first date where the achievement condition became true."""
    if not daily:
        return None

    # For word milestones, find first day total_words exceeded threshold
    word_thresholds = {
        "hello_world": 10, "baby_steps": 100, "getting_warmed_up": 500,
        "first_thousand": 1000, "verbose": 5000, "wordy_mcwordface": 10000,
        "halfway": 25000, "unstoppable": 40000, "magnum_opus": 50000,
        "novelist": 60000, "war_and_peace": 80000, "centennial": 100000,
    }
    if ach_id in word_thresholds:
        threshold = word_thresholds[ach_id]
        for d in daily:
            if d.get("total_words", 0) >= threshold:
                return d["date"]

    # Figure/table/equation/citation thresholds
    count_thresholds = {
        "first_figure": ("figures", 1), "gallery_opening": ("figures", 5),
        "visual_storyteller": ("figures", 10), "data_viz": ("figures", 20),
        "museum_curator": ("figures", 30), "pixel_perfectionist": ("figures", 50),
        "first_table": ("tables", 1), "data_organizer": ("tables", 3),
        "excellent": ("tables", 5),
        "emc2": ("equations", 1), "math_inclined": ("equations", 10),
        "proof_exercise": ("equations", 25), "the_formula": ("equations", 50),
        "maxwell_proud": ("equations", 100),
        "citation_needed": ("citations", 1), "well_read": ("citations", 25),
        "literature_scholar": ("citations", 50), "shoulders_giants": ("citations", 100),
        "walking_bibliography": ("citations", 150),
    }
    if ach_id in count_thresholds:
        field, threshold = count_thresholds[ach_id]
        for d in daily:
            if d.get(field, 0) >= threshold:
                return d["date"]

    # Deletion-based
    if ach_id == "backspace_warrior":
        for d in daily:
            if d.get("words_deleted", 0) >= 100:
                return d["date"]
    if ach_id == "kill_your_darlings":
        for d in daily:
            if d.get("words_deleted", 0) >= 500:
                return d["date"]
    if ach_id == "scorched_earth":
        for d in daily:
            if d.get("words_deleted", 0) >= 1000:
                return d["date"]
    if ach_id == "net_negative":
        for d in daily:
            if d.get("words_deleted", 0) > d.get("words_added", 0):
                return d["date"]
    if ach_id == "the_editor":
        cumul = 0
        for d in daily:
            cumul += d.get("words_deleted", 0)
            if cumul >= 5000:
                return d["date"]

    # Time-based: find the first commit at the relevant hour
    if ach_id == "night_owl":
        for c in commits:
            if c.get("hour", 12) in [0, 1, 2, 3]:
                return c["date"]
    if ach_id == "early_bird":
        for c in commits:
            if c.get("hour", 12) in [4, 5]:
                return c["date"]

    # For everything else, use the latest date as fallback
    return daily[-1]["date"]


def evaluate_and_save(history_data):
    """Evaluate achievements and save to JSON."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Load previous state to detect new unlocks
    previous = {}
    if ACHIEVEMENTS_FILE.exists():
        with open(ACHIEVEMENTS_FILE) as f:
            previous = json.load(f)

    current = check_achievements(history_data)

    # Detect newly unlocked
    newly_unlocked = []
    for ach_id, ach in current.items():
        if ach["unlocked"] and not previous.get(ach_id, {}).get("unlocked", False):
            newly_unlocked.append(ach)

    output = {
        "achievements": current,
        "total": len(current),
        "unlocked": sum(1 for a in current.values() if a["unlocked"]),
        "newly_unlocked": [a["id"] for a in newly_unlocked],
        "all_definitions": _define_achievements(),
    }

    with open(ACHIEVEMENTS_FILE, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Achievements: {output['unlocked']}/{output['total']} unlocked")
    if newly_unlocked:
        print(f"  NEW: {', '.join(a.get('name', a['id']) for a in newly_unlocked)}")

    return output


if __name__ == "__main__":
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE) as f:
            history = json.load(f)
        evaluate_and_save(history)
    else:
        print("No history.json found. Run collect_data.py first.")
