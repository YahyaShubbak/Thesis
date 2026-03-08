#!/usr/bin/env python3
"""
Achievement system for the thesis dashboard.

~100 achievements across categories, Cookie-Clicker-inspired tone.
6 tiers: bronze, silver, gold, diamond, mythic, transcendent.
Difficulty escalates steeply - later tiers are very hard to reach.
Some achievements are "shadow" (hidden until unlocked).
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"
HISTORY_FILE = DATA_DIR / "history.json"
ACHIEVEMENTS_FILE = DATA_DIR / "achievements.json"

# Tier order (for sorting and display)
TIER_ORDER = ["bronze", "silver", "gold", "diamond", "mythic", "transcendent"]


def _define_achievements():
    """Return list of all achievement definitions."""
    return [
        # =================================================================
        # WRITING MILESTONES (20)
        # =================================================================
        {"id": "hello_world", "name": "Hello World", "description": "Write your first sentence.", "hint": "Every thesis starts with a single word...", "emoji": "👋", "category": "Writing", "tier": "bronze", "hidden": False},
        {"id": "baby_steps", "name": "Baby Steps", "description": "Reach 100 words.", "hint": "Keep typing!", "emoji": "🐣", "category": "Writing", "tier": "bronze", "hidden": False},
        {"id": "getting_warmed_up", "name": "Getting Warmed Up", "description": "500 words and counting.", "hint": "The keyboard is warming up...", "emoji": "🔥", "category": "Writing", "tier": "bronze", "hidden": False},
        {"id": "first_thousand", "name": "The First Thousand", "description": "Four digits of pure knowledge.", "hint": "You could write a strong email!", "emoji": "🎯", "category": "Writing", "tier": "silver", "hidden": False},
        {"id": "page_one", "name": "Page One", "description": "Write your first full page (~300 words).", "hint": "The first of many.", "emoji": "📄", "category": "Writing", "tier": "bronze", "hidden": False},
        {"id": "verbose", "name": "Verbose", "description": "5,000 words -- you could fill a pamphlet.", "hint": "That is a solid blog post!", "emoji": "📝", "category": "Writing", "tier": "silver", "hidden": False},
        {"id": "wordy_mcwordface", "name": "Wordy McWordface", "description": "10,000 words! That is a novella.", "hint": "Double digits of thousands!", "emoji": "📚", "category": "Writing", "tier": "gold", "hidden": False},
        {"id": "fifteen_k", "name": "Quindecimille", "description": "15,000 words -- fancy Latin name for a big number.", "hint": "More than most bachelor theses!", "emoji": "🏅", "category": "Writing", "tier": "gold", "hidden": False},
        {"id": "twenty_k", "name": "Twenty Grand", "description": "20,000 words of accumulated wisdom.", "hint": "A small book!", "emoji": "💰", "category": "Writing", "tier": "gold", "hidden": False},
        {"id": "halfway", "name": "Halfway There", "description": "25,000 words -- the thesis is taking shape.", "hint": "Livin on a prayer... and caffeine.", "emoji": "⚡", "category": "Writing", "tier": "diamond", "hidden": False},
        {"id": "thirty_k", "name": "Thirty Thousand Leagues", "description": "30,000 words deep into science.", "hint": "Jules Verne would be impressed.", "emoji": "🌊", "category": "Writing", "tier": "diamond", "hidden": False},
        {"id": "thirty_five_k", "name": "Page Turner", "description": "35,000 words -- people could actually read this.", "hint": "Almost a real book!", "emoji": "📖", "category": "Writing", "tier": "diamond", "hidden": False},
        {"id": "unstoppable", "name": "Unstoppable Typist", "description": "40,000 words of relentless productivity.", "hint": "Your keyboard fears you.", "emoji": "🚀", "category": "Writing", "tier": "diamond", "hidden": False},
        {"id": "forty_five_k", "name": "So Close", "description": "45,000 words -- the finish line is in sight.", "hint": "Almost... there...", "emoji": "🏁", "category": "Writing", "tier": "diamond", "hidden": False},
        {"id": "magnum_opus", "name": "The Magnum Opus", "description": "50,000 words -- TARGET REACHED!", "hint": "You did it. Legend.", "emoji": "🏆", "category": "Writing", "tier": "mythic", "hidden": False},
        {"id": "novelist", "name": "The Novelist", "description": "60,000 words -- publish this as a book.", "hint": "Publishers are calling...", "emoji": "📖", "category": "Writing", "tier": "mythic", "hidden": False},
        {"id": "seventy_k", "name": "Seventy Thousand", "description": "70,000 words -- denser than some textbooks.", "hint": "Students will suffer reading this (lovingly).", "emoji": "📕", "category": "Writing", "tier": "mythic", "hidden": False},
        {"id": "war_and_peace", "name": "War and Peace (Almost)", "description": "80,000 words -- Tolstoy nods approvingly.", "hint": "Your thesis weighs more than your laptop.", "emoji": "⚔️", "category": "Writing", "tier": "transcendent", "hidden": False},
        {"id": "ninety_k", "name": "Approaching Infinity", "description": "90,000 words -- is there an end?", "hint": "The event horizon of thesis writing.", "emoji": "🌌", "category": "Writing", "tier": "transcendent", "hidden": False},
        {"id": "centennial", "name": "Centennial", "description": "100,000 words. A monument of science.", "hint": "You are become thesis, destroyer of free time.", "emoji": "💎", "category": "Writing", "tier": "transcendent", "hidden": False},

        # =================================================================
        # DAILY PRODUCTIVITY (8)
        # =================================================================
        {"id": "warm_up_day", "name": "Warm-Up Day", "description": "Write 100 words in a single day.", "hint": "A little goes a long way.", "emoji": "🌱", "category": "Productivity", "tier": "bronze", "hidden": False},
        {"id": "productive_day", "name": "Productive Day", "description": "Write 500 words in a single day.", "hint": "A solid day of work!", "emoji": "💪", "category": "Productivity", "tier": "silver", "hidden": False},
        {"id": "thousand_day", "name": "Thousand-Word Day", "description": "Write 1,000 words in a single day.", "hint": "Now that is a productive day!", "emoji": "🌟", "category": "Productivity", "tier": "gold", "hidden": False},
        {"id": "two_k_day", "name": "Double Feature", "description": "Write 2,000 words in a single day.", "hint": "Your fingers are on fire!", "emoji": "🔥", "category": "Productivity", "tier": "diamond", "hidden": False},
        {"id": "three_k_day", "name": "Triple Threat", "description": "Write 3,000 words in a single day.", "hint": "Are you even human?", "emoji": "⚡", "category": "Productivity", "tier": "mythic", "hidden": False},
        {"id": "five_k_day", "name": "Hypergraphia", "description": "Write 5,000 words in a single day.", "hint": "Medical condition or dedication? Yes.", "emoji": "🧬", "category": "Productivity", "tier": "transcendent", "hidden": False},
        {"id": "sprint_week", "name": "Sprint Week", "description": "Write 5,000 words total in one week.", "hint": "A week of focused writing.", "emoji": "🏃", "category": "Productivity", "tier": "gold", "hidden": False},
        {"id": "marathon_week", "name": "Marathon Week", "description": "Write 10,000 words total in one week.", "hint": "Sleep is optional.", "emoji": "🏃‍♂️", "category": "Productivity", "tier": "mythic", "hidden": False},

        # =================================================================
        # EDITING & DELETION (8)
        # =================================================================
        {"id": "first_delete", "name": "First Cut", "description": "Delete any words for the first time.", "hint": "Pruning begins.", "emoji": "✏️", "category": "Editing", "tier": "bronze", "hidden": False},
        {"id": "backspace_warrior", "name": "Backspace Warrior", "description": "Delete 100 words in a single day.", "hint": "Sometimes you have to destroy to create.", "emoji": "⌫", "category": "Editing", "tier": "bronze", "hidden": False},
        {"id": "kill_your_darlings", "name": "Kill Your Darlings", "description": "Delete 500 words in a single day.", "hint": "Faulkner would be proud.", "emoji": "🗡️", "category": "Editing", "tier": "silver", "hidden": False},
        {"id": "scorched_earth", "name": "Scorched Earth", "description": "Delete 1,000 words in a single day.", "hint": "A fresh start, courtesy of the Delete key.", "emoji": "🔥", "category": "Editing", "tier": "gold", "hidden": False},
        {"id": "nuclear_option", "name": "Nuclear Option", "description": "Delete 2,000 words in a single day.", "hint": "Entire sections... gone. Reduced to atoms.", "emoji": "☢️", "category": "Editing", "tier": "diamond", "hidden": False},
        {"id": "net_negative", "name": "Net Negative", "description": "End a day with fewer words than you started.", "hint": "Negative progress is still progress... right?", "emoji": "📉", "category": "Editing", "tier": "silver", "hidden": False},
        {"id": "the_editor", "name": "The Editor", "description": "Accumulate 5,000 total deleted words.", "hint": "You have killed a novella worth of text.", "emoji": "✂️", "category": "Editing", "tier": "gold", "hidden": False},
        {"id": "the_rewriter", "name": "The Rewriter", "description": "Accumulate 15,000 total deleted words.", "hint": "You have rewritten the thesis twice over.", "emoji": "🔄", "category": "Editing", "tier": "mythic", "hidden": False},

        # =================================================================
        # FIGURES (10)
        # =================================================================
        {"id": "first_figure", "name": "A Picture Says...", "description": "Add your first figure.", "hint": "...a thousand words you do not have to write!", "emoji": "🖼️", "category": "Figures", "tier": "bronze", "hidden": False},
        {"id": "three_figures", "name": "Triptych", "description": "3 figures -- a small gallery.", "hint": "Three perspectives on science.", "emoji": "🎭", "category": "Figures", "tier": "bronze", "hidden": False},
        {"id": "gallery_opening", "name": "Gallery Opening", "description": "5 figures -- a small exhibition.", "hint": "Curating your scientific gallery.", "emoji": "🎨", "category": "Figures", "tier": "silver", "hidden": False},
        {"id": "visual_storyteller", "name": "Visual Storyteller", "description": "10 figures -- a thousand words each.", "hint": "That is 10,000 words worth of pictures!", "emoji": "📊", "category": "Figures", "tier": "silver", "hidden": False},
        {"id": "fifteen_figs", "name": "Illustrated Edition", "description": "15 figures -- practically a picture book.", "hint": "Your advisor asks: more text?", "emoji": "📸", "category": "Figures", "tier": "gold", "hidden": False},
        {"id": "data_viz", "name": "Data Viz Enthusiast", "description": "20 figures -- you love showing data.", "hint": "Why write when you can plot?", "emoji": "📈", "category": "Figures", "tier": "gold", "hidden": False},
        {"id": "twentyfive_figs", "name": "Infographic PhD", "description": "25 figures -- your thesis is very visual.", "hint": "Each figure is a mini-paper!", "emoji": "🗺️", "category": "Figures", "tier": "diamond", "hidden": False},
        {"id": "museum_curator", "name": "Museum Curator", "description": "30 figures -- quite the collection.", "hint": "The Louvre called, they want their curator back.", "emoji": "🏛️", "category": "Figures", "tier": "diamond", "hidden": False},
        {"id": "forty_figs", "name": "Visual Encyclopedia", "description": "40 figures -- a reference work.", "hint": "Reviewers need a coffee break between figures.", "emoji": "📚", "category": "Figures", "tier": "mythic", "hidden": False},
        {"id": "pixel_perfectionist", "name": "Pixel Perfectionist", "description": "50 figures -- a visual masterpiece.", "hint": "Your thesis is basically an art gallery now.", "emoji": "✨", "category": "Figures", "tier": "transcendent", "hidden": False},

        # =================================================================
        # TABLES (5)
        # =================================================================
        {"id": "first_table", "name": "Tabled Discussion", "description": "Create your first table.", "hint": "Organized data is happy data.", "emoji": "📋", "category": "Tables", "tier": "bronze", "hidden": False},
        {"id": "two_tables", "name": "Double Entry", "description": "2 tables -- the data starts to organize.", "hint": "Bookkeeping intensifies.", "emoji": "📑", "category": "Tables", "tier": "bronze", "hidden": False},
        {"id": "data_organizer", "name": "Data Organizer", "description": "3 tables of organized data.", "hint": "Structure brings clarity!", "emoji": "🗂️", "category": "Tables", "tier": "silver", "hidden": False},
        {"id": "four_tables", "name": "Table Tennis", "description": "4 tables -- back and forth with data.", "hint": "Ping... pong... data.", "emoji": "🏓", "category": "Tables", "tier": "gold", "hidden": False},
        {"id": "excellent", "name": "Excel-lent", "description": "5 tables -- you love structure.", "hint": "Spreadsheet energy detected.", "emoji": "📊", "category": "Tables", "tier": "diamond", "hidden": False},

        # =================================================================
        # EQUATIONS (10)
        # =================================================================
        {"id": "emc2", "name": "E=mc2", "description": "Write your first equation.", "hint": "Physics intensifies.", "emoji": "🧮", "category": "Equations", "tier": "bronze", "hidden": False},
        {"id": "five_eqs", "name": "Handful of Formulas", "description": "5 equations -- getting mathematical.", "hint": "The math begins.", "emoji": "✍️", "category": "Equations", "tier": "bronze", "hidden": False},
        {"id": "math_inclined", "name": "Mathematically Inclined", "description": "10 equations -- the math is mathing.", "hint": "Variables assemble!", "emoji": "📐", "category": "Equations", "tier": "silver", "hidden": False},
        {"id": "fifteen_eqs", "name": "Derivation Station", "description": "15 equations -- you are deriving like a pro.", "hint": "d/dx everything.", "emoji": "🚉", "category": "Equations", "tier": "silver", "hidden": False},
        {"id": "proof_exercise", "name": "Proof Left as Exercise", "description": "25 equations -- your reviewer trembles.", "hint": "The proof is left as an exercise to the reader.", "emoji": "🎓", "category": "Equations", "tier": "gold", "hidden": False},
        {"id": "thirty_five_eqs", "name": "Equation Avalanche", "description": "35 equations -- they keep coming.", "hint": "You cannot stop the math.", "emoji": "🏔️", "category": "Equations", "tier": "gold", "hidden": False},
        {"id": "the_formula", "name": "The Formula", "description": "50 equations -- physics thesis confirmed.", "hint": "You are basically deriving reality.", "emoji": "⚗️", "category": "Equations", "tier": "diamond", "hidden": False},
        {"id": "seventy_five_eqs", "name": "Equation Singularity", "description": "75 equations -- approaching critical mass.", "hint": "Your thesis might collapse into a black hole of math.", "emoji": "🕳️", "category": "Equations", "tier": "mythic", "hidden": False},
        {"id": "maxwell_proud", "name": "Maxwell Would Be Proud", "description": "100 equations of pure elegance.", "hint": "You have out-equationed most textbooks.", "emoji": "⚡", "category": "Equations", "tier": "mythic", "hidden": False},
        {"id": "euler_reborn", "name": "Euler Reborn", "description": "150 equations -- you speak mathematics fluently.", "hint": "Leonhard Euler sends his regards.", "emoji": "♾️", "category": "Equations", "tier": "transcendent", "hidden": False},

        # =================================================================
        # CITATIONS (10)
        # =================================================================
        {"id": "citation_needed", "name": "Citation Needed", "description": "Add your first citation.", "hint": "[citation needed]", "emoji": "📎", "category": "Citations", "tier": "bronze", "hidden": False},
        {"id": "five_cites", "name": "Footnote Enthusiast", "description": "5 unique citations.", "hint": "You have read some papers!", "emoji": "📌", "category": "Citations", "tier": "bronze", "hidden": False},
        {"id": "ten_cites", "name": "Literature Dabbler", "description": "10 unique citations.", "hint": "Your Zotero is heating up.", "emoji": "🔖", "category": "Citations", "tier": "silver", "hidden": False},
        {"id": "well_read", "name": "Well-Read", "description": "25 unique citations.", "hint": "Knowledge on the shoulders of papers.", "emoji": "📖", "category": "Citations", "tier": "silver", "hidden": False},
        {"id": "literature_scholar", "name": "Literature Scholar", "description": "50 citations -- your bibliography is thick.", "hint": "Your reference list needs its own chapter.", "emoji": "🏫", "category": "Citations", "tier": "gold", "hidden": False},
        {"id": "seventy_five_cites", "name": "Reference Machine", "description": "75 citations -- still going.", "hint": "You cite in your sleep.", "emoji": "🤖", "category": "Citations", "tier": "gold", "hidden": False},
        {"id": "shoulders_giants", "name": "Standing on Shoulders", "description": "100 citations -- of giants.", "hint": "Newton, Einstein, and your bibliography.", "emoji": "🗼", "category": "Citations", "tier": "diamond", "hidden": False},
        {"id": "one_twenty_five_cites", "name": "Citation Connoisseur", "description": "125 citations -- refined taste in references.", "hint": "Only the finest references for your thesis.", "emoji": "🍷", "category": "Citations", "tier": "mythic", "hidden": False},
        {"id": "walking_bibliography", "name": "Walking Bibliography", "description": "150 citations -- you ARE the literature review.", "hint": "You have read more papers than your advisor.", "emoji": "🚶", "category": "Citations", "tier": "mythic", "hidden": False},
        {"id": "two_hundred_cites", "name": "The Library", "description": "200 citations -- a repository of human knowledge.", "hint": "The Library of Alexandria called. They are jealous.", "emoji": "🏛️", "category": "Citations", "tier": "transcendent", "hidden": False},

        # =================================================================
        # CHAPTER PROGRESS (10)
        # =================================================================
        {"id": "abstract_thinker", "name": "Abstract Thinker", "description": "Write the abstract (>150 words).", "hint": "The elevator pitch of your PhD.", "emoji": "💭", "category": "Chapters", "tier": "silver", "hidden": False},
        {"id": "abstract_polished", "name": "Abstract Perfection", "description": "Abstract exceeds 300 words.", "hint": "A refined summary of years of work.", "emoji": "💎", "category": "Chapters", "tier": "gold", "hidden": False},
        {"id": "and_so_it_begins", "name": "And So It Begins", "description": "Introduction > 1,000 words.", "hint": "The journey of a thousand pages starts here.", "emoji": "🚪", "category": "Chapters", "tier": "silver", "hidden": False},
        {"id": "intro_complete", "name": "Hook, Line and Sinker", "description": "Introduction > 3,000 words.", "hint": "The reader is hooked!", "emoji": "🎣", "category": "Chapters", "tier": "gold", "hidden": False},
        {"id": "theoretically_speaking", "name": "Theoretically Speaking", "description": "Theory chapter > 3,000 words.", "hint": "In theory, no difference between theory and practice.", "emoji": "🧠", "category": "Chapters", "tier": "gold", "hidden": False},
        {"id": "theory_mastery", "name": "Theory Mastery", "description": "Theory chapter > 8,000 words.", "hint": "You have written a textbook chapter.", "emoji": "🎓", "category": "Chapters", "tier": "mythic", "hidden": False},
        {"id": "lab_rat", "name": "Lab Rat", "description": "Experimental chapter > 2,000 words.", "hint": "Documenting the method to the madness.", "emoji": "🐀", "category": "Chapters", "tier": "gold", "hidden": False},
        {"id": "results_are_in", "name": "The Results Are In", "description": "Results + Discussion > 2,000 words.", "hint": "And the data says...", "emoji": "🔬", "category": "Chapters", "tier": "gold", "hidden": False},
        {"id": "results_flood", "name": "Data Deluge", "description": "Results + Discussion > 8,000 words.", "hint": "The data will not stop talking.", "emoji": "🌊", "category": "Chapters", "tier": "mythic", "hidden": False},
        {"id": "the_end_is_nigh", "name": "The End Is Nigh", "description": "Outlook/conclusion > 500 words.", "hint": "The light at the end of the tunnel!", "emoji": "🌅", "category": "Chapters", "tier": "silver", "hidden": False},

        # =================================================================
        # CONSISTENCY & STREAKS (10)
        # =================================================================
        {"id": "daily_grind", "name": "Daily Grind", "description": "Write on 3 consecutive days.", "hint": "Consistency is key!", "emoji": "☕", "category": "Streaks", "tier": "bronze", "hidden": False},
        {"id": "on_a_roll", "name": "On a Roll", "description": "Write on 7 consecutive days.", "hint": "A full week of productivity!", "emoji": "🎲", "category": "Streaks", "tier": "silver", "hidden": False},
        {"id": "ten_streak", "name": "Tenacious", "description": "Write on 10 consecutive days.", "hint": "Unstoppable!", "emoji": "🔟", "category": "Streaks", "tier": "silver", "hidden": False},
        {"id": "fortnight_focus", "name": "Fortnight of Focus", "description": "Write on 14 consecutive days.", "hint": "Two weeks straight. Impressive.", "emoji": "🔥", "category": "Streaks", "tier": "gold", "hidden": False},
        {"id": "three_week_streak", "name": "21-Day Habit", "description": "Write on 21 consecutive days.", "hint": "They say it takes 21 days to form a habit.", "emoji": "🧬", "category": "Streaks", "tier": "gold", "hidden": False},
        {"id": "monthly_marathon", "name": "Monthly Marathon", "description": "Write on 30 consecutive days.", "hint": "A full month. Legendary.", "emoji": "🏃", "category": "Streaks", "tier": "diamond", "hidden": False},
        {"id": "forty_five_streak", "name": "The Grinder", "description": "Write on 45 consecutive days.", "hint": "You have transcended normal dedication.", "emoji": "⚙️", "category": "Streaks", "tier": "mythic", "hidden": False},
        {"id": "sixty_streak", "name": "One with the Thesis", "description": "Write on 60 consecutive days.", "hint": "You ARE the thesis now.", "emoji": "🧘", "category": "Streaks", "tier": "mythic", "hidden": False},
        {"id": "ninety_streak", "name": "Thesis Monk", "description": "Write on 90 consecutive days.", "hint": "Three months of pure devotion.", "emoji": "🛕", "category": "Streaks", "tier": "transcendent", "hidden": False},
        {"id": "total_days_30", "name": "30 Days of Writing", "description": "Write on 30 distinct days (not necessarily consecutive).", "hint": "A month worth of effort!", "emoji": "📅", "category": "Streaks", "tier": "silver", "hidden": False},

        # =================================================================
        # TIME-BASED (6)
        # =================================================================
        {"id": "night_owl", "name": "Night Owl", "description": "Push a commit after midnight.", "hint": "The best ideas come at 2 AM... or do they?", "emoji": "🦉", "category": "Time", "tier": "bronze", "hidden": False},
        {"id": "early_bird", "name": "Early Bird", "description": "Push a commit before 6 AM.", "hint": "The early physicist catches the... data?", "emoji": "🐦", "category": "Time", "tier": "silver", "hidden": False},
        {"id": "weekend_warrior", "name": "Weekend Warrior", "description": "Commit on Sat and Sun in the same weekend.", "hint": "Rest is for the defended.", "emoji": "⚔️", "category": "Time", "tier": "silver", "hidden": False},
        {"id": "lunch_break_scholar", "name": "Lunch Break Scholar", "description": "Commit between 12:00 and 13:00.", "hint": "Who needs food when there is science?", "emoji": "🥪", "category": "Time", "tier": "bronze", "hidden": False},
        {"id": "witching_hour", "name": "Witching Hour", "description": "Commit between 3 AM and 4 AM.", "hint": "The veil between physics and madness is thin.", "emoji": "🧙", "category": "Time", "tier": "gold", "hidden": False},
        {"id": "five_different_hours", "name": "Around the Clock", "description": "Have commits across 12+ different hours of the day.", "hint": "You write at ALL hours.", "emoji": "🕐", "category": "Time", "tier": "gold", "hidden": False},

        # =================================================================
        # SHADOW / SECRET ACHIEVEMENTS (13)
        # =================================================================
        {"id": "shadow_oops", "name": "???", "description": "???", "hint": "Precision is everything...", "emoji": "🥚", "category": "Shadow", "tier": "silver", "hidden": True,
         "_secret_name": "Oops", "_secret_description": "Have a net word count decrease of exactly 1 word.", "_secret_emoji": "🤭"},
        {"id": "shadow_holiday", "name": "???", "description": "???", "hint": "Try working on a very special day...", "emoji": "🥚", "category": "Shadow", "tier": "gold", "hidden": True,
         "_secret_name": "No Life", "_secret_description": "Commit on Christmas, New Year Eve, or New Year Day.", "_secret_emoji": "🎄"},
        {"id": "shadow_nice", "name": "???", "description": "???", "hint": "Numbers are everywhere...", "emoji": "🥚", "category": "Shadow", "tier": "bronze", "hidden": True,
         "_secret_name": "Nice", "_secret_description": "Hit a legendary number in your metrics.", "_secret_emoji": "😏"},
        {"id": "shadow_zero", "name": "???", "description": "???", "hint": "What happens when nothing happens?", "emoji": "🥚", "category": "Shadow", "tier": "bronze", "hidden": True,
         "_secret_name": "Commit to Nothing", "_secret_description": "Make a commit that changes 0 words.", "_secret_emoji": "🫥"},
        {"id": "shadow_resurrection", "name": "???", "description": "???", "hint": "Persistence has its own reward.", "emoji": "🥚", "category": "Shadow", "tier": "gold", "hidden": True,
         "_secret_name": "Resurrection", "_secret_description": "Come back and write after a 30+ day gap.", "_secret_emoji": "🧟"},
        {"id": "shadow_observer", "name": "???", "description": "???", "hint": "The dashboard remembers everything...", "emoji": "🥚", "category": "Shadow", "tier": "silver", "hidden": True,
         "_secret_name": "The Observer", "_secret_description": "Accumulate 50+ total commits.", "_secret_emoji": "👁️"},
        {"id": "shadow_allnighter", "name": "???", "description": "???", "hint": "All work and no play?", "emoji": "🥚", "category": "Shadow", "tier": "diamond", "hidden": True,
         "_secret_name": "All-Nighter", "_secret_description": "Have commits at 11 PM, midnight, 1 AM, 2 AM, and 3 AM.", "_secret_emoji": "😵"},
        {"id": "shadow_palindrome", "name": "???", "description": "???", "hint": "Mirror, mirror...", "emoji": "🥚", "category": "Shadow", "tier": "silver", "hidden": True,
         "_secret_name": "Palindrome Day", "_secret_description": "Commit on a palindrome date.", "_secret_emoji": "🪞"},
        {"id": "shadow_friday13", "name": "???", "description": "???", "hint": "Superstition is just a word...", "emoji": "🥚", "category": "Shadow", "tier": "silver", "hidden": True,
         "_secret_name": "Paraskevidekatriaphobia", "_secret_description": "Commit on a Friday the 13th.", "_secret_emoji": "🔮"},
        {"id": "shadow_pi", "name": "???", "description": "???", "hint": "March has a very special day...", "emoji": "🥚", "category": "Shadow", "tier": "gold", "hidden": True,
         "_secret_name": "Pi Day", "_secret_description": "Commit on March 14th (3/14).", "_secret_emoji": "🥧"},
        {"id": "shadow_fibonacci", "name": "???", "description": "???", "hint": "Nature favorite sequence hides in your data...", "emoji": "🥚", "category": "Shadow", "tier": "gold", "hidden": True,
         "_secret_name": "Fibonacci", "_secret_description": "Have a total word count that is a Fibonacci number (within 5 words).", "_secret_emoji": "🐚"},
        {"id": "shadow_groundhog", "name": "???", "description": "???", "hint": "Didn't I do this already?", "emoji": "🥚", "category": "Shadow", "tier": "bronze", "hidden": True,
         "_secret_name": "Groundhog Day", "_secret_description": "Have two consecutive days with the exact same word count.", "_secret_emoji": "🦫"},
        {"id": "shadow_thesis_birthday", "name": "???", "description": "???", "hint": "Anniversaries come around once a year...", "emoji": "🥚", "category": "Shadow", "tier": "mythic", "hidden": True,
         "_secret_name": "Happy Birthday Thesis", "_secret_description": "Commit exactly one year after your first ever commit.", "_secret_emoji": "🎂"},
    ]


def _compute_streaks(daily_entries):
    """Compute max consecutive writing streak and total writing days."""
    if not daily_entries:
        return 0, 0

    dates = sorted(set(e["date"] for e in daily_entries if e.get("total_words", 0) > 0))
    if not dates:
        return 0, 0

    total_days = len(dates)
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

    return max_streak, total_days


def _has_comeback_after_gap(daily_entries, gap_days=30):
    """Check if there is a writing day after a gap of gap_days+."""
    dates = sorted(set(e["date"] for e in daily_entries))
    if len(dates) < 2:
        return False
    for i in range(1, len(dates)):
        d1 = datetime.strptime(dates[i - 1], "%Y-%m-%d")
        d2 = datetime.strptime(dates[i], "%Y-%m-%d")
        if (d2 - d1).days >= gap_days:
            return True
    return False


def _is_fibonacci(n, tolerance=5):
    """Check if n is within tolerance of a Fibonacci number."""
    a, b = 0, 1
    while b < n - tolerance:
        a, b = b, a + b
    return abs(b - n) <= tolerance or abs(a - n) <= tolerance


def _is_palindrome_date(date_str):
    """Check if date YYYY-MM-DD forms a palindrome when stripped of dashes."""
    stripped = date_str.replace("-", "")
    return stripped == stripped[::-1]


def _max_daily_added(daily):
    """Get the maximum words added in a single day."""
    return max((d.get("words_added", 0) for d in daily), default=0)


def _max_weekly_added(daily):
    """Get the maximum words added in any 7-day window."""
    if len(daily) < 2:
        return _max_daily_added(daily)
    max_week = 0
    dates_added = [(datetime.strptime(d["date"], "%Y-%m-%d"), d.get("words_added", 0)) for d in daily]
    for i in range(len(dates_added)):
        window_sum = 0
        for j in range(i, len(dates_added)):
            if (dates_added[j][0] - dates_added[i][0]).days >= 7:
                break
            window_sum += dates_added[j][1]
        max_week = max(max_week, window_sum)
    return max_week


def _has_groundhog(daily):
    """Check for two consecutive days with same total word count."""
    for i in range(1, len(daily)):
        if daily[i].get("total_words", -1) == daily[i - 1].get("total_words", -2):
            return True
    return False


def _has_thesis_birthday(commits, daily):
    """Check if there is a commit exactly 1 year after the first commit."""
    if not daily:
        return False
    first_date = daily[0]["date"]
    first_dt = datetime.strptime(first_date, "%Y-%m-%d")
    try:
        birthday = first_dt.replace(year=first_dt.year + 1)
    except ValueError:
        birthday = first_dt.replace(year=first_dt.year + 1, day=28)
    birthday_str = birthday.strftime("%Y-%m-%d")
    commit_dates = set(c.get("date", "") for c in commits)
    return birthday_str in commit_dates


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

    # Max single-day values
    max_daily_deleted = max((d.get("words_deleted", 0) for d in daily), default=0)
    max_daily_add = _max_daily_added(daily)
    max_week_add = _max_weekly_added(daily)

    # Any deletion at all
    has_any_delete = cumulative_deleted > 0

    # Net negative day
    has_net_negative = any(d.get("words_deleted", 0) > d.get("words_added", 0) for d in daily)

    # Streaks
    max_streak, total_writing_days = _compute_streaks(daily)

    # Commit hours
    commit_hours = set(c.get("hour", 12) for c in commits)
    distinct_hours = len(commit_hours)

    # Commit dates and weekdays
    commit_dates = [c.get("date", "") for c in commits]
    commit_dates_set = set(commit_dates)

    # Weekend warrior: check for Sat+Sun in same weekend
    has_weekend_warrior = False
    saturdays = set()
    sundays = set()
    for c in commits:
        wd = c.get("weekday", 0)
        d = c.get("date", "")
        if wd == 5:
            saturdays.add(d)
        elif wd == 6:
            sundays.add(d)
    for sat_str in saturdays:
        sat = datetime.strptime(sat_str, "%Y-%m-%d")
        sun = sat + timedelta(days=1)
        if sun.strftime("%Y-%m-%d") in sundays:
            has_weekend_warrior = True
            break

    # Time checks
    has_night_owl = any(h in commit_hours for h in [0, 1, 2, 3])
    has_early_bird = any(h in commit_hours for h in [4, 5])
    has_lunch = any(h == 12 for h in commit_hours)
    has_witching = any(h == 3 for h in commit_hours)

    # Holiday commits
    has_holiday = any(d.endswith("-12-25") or d.endswith("-12-31") or d.endswith("-01-01") for d in commit_dates)

    # Shadow checks
    has_exact_minus_one = any(
        d.get("words_deleted", 0) - d.get("words_added", 0) == 1 and d.get("words_deleted", 0) > 0
        for d in daily
    )

    has_nice = (citations == 69 or "1337" in str(total_words) or
                total_words == 42000 or equations == 42 or figures == 42)

    has_zero_change = any(
        d.get("words_added", 0) == 0 and d.get("words_deleted", 0) == 0
        for d in daily[1:]
    )

    has_comeback = _has_comeback_after_gap(daily, 30)
    has_observer = len(commits) >= 50
    all_nighter_hours = {23, 0, 1, 2, 3}
    has_all_nighter = all_nighter_hours.issubset(commit_hours)

    has_palindrome = any(_is_palindrome_date(d) for d in commit_dates)
    has_friday13 = any(
        datetime.strptime(d, "%Y-%m-%d").weekday() == 4 and datetime.strptime(d, "%Y-%m-%d").day == 13
        for d in commit_dates_set if d
    )
    has_pi_day = any(d.endswith("-03-14") for d in commit_dates)
    has_fibonacci_words = _is_fibonacci(total_words, 5) and total_words > 100
    has_groundhog = _has_groundhog(daily)
    has_thesis_birthday = _has_thesis_birthday(commits, daily)

    # Chapter word counts
    abstract_words = chapters.get("Abstract", 0)
    intro_words = chapters.get("Introduction", 0)
    theory_words = chapters.get("Theory", 0)
    experimental_words = chapters.get("Experimental", 0)
    results_words = chapters.get("Results", 0) + chapters.get("Discussion", 0)
    outlook_words = chapters.get("Outlook", 0)

    # Build condition map
    conditions = {
        # Writing milestones
        "hello_world": total_words >= 10,
        "baby_steps": total_words >= 100,
        "getting_warmed_up": total_words >= 500,
        "page_one": total_words >= 300,
        "first_thousand": total_words >= 1000,
        "verbose": total_words >= 5000,
        "wordy_mcwordface": total_words >= 10000,
        "fifteen_k": total_words >= 15000,
        "twenty_k": total_words >= 20000,
        "halfway": total_words >= 25000,
        "thirty_k": total_words >= 30000,
        "thirty_five_k": total_words >= 35000,
        "unstoppable": total_words >= 40000,
        "forty_five_k": total_words >= 45000,
        "magnum_opus": total_words >= 50000,
        "novelist": total_words >= 60000,
        "seventy_k": total_words >= 70000,
        "war_and_peace": total_words >= 80000,
        "ninety_k": total_words >= 90000,
        "centennial": total_words >= 100000,

        # Daily productivity
        "warm_up_day": max_daily_add >= 100,
        "productive_day": max_daily_add >= 500,
        "thousand_day": max_daily_add >= 1000,
        "two_k_day": max_daily_add >= 2000,
        "three_k_day": max_daily_add >= 3000,
        "five_k_day": max_daily_add >= 5000,
        "sprint_week": max_week_add >= 5000,
        "marathon_week": max_week_add >= 10000,

        # Editing
        "first_delete": has_any_delete,
        "backspace_warrior": max_daily_deleted >= 100,
        "kill_your_darlings": max_daily_deleted >= 500,
        "scorched_earth": max_daily_deleted >= 1000,
        "nuclear_option": max_daily_deleted >= 2000,
        "net_negative": has_net_negative,
        "the_editor": cumulative_deleted >= 5000,
        "the_rewriter": cumulative_deleted >= 15000,

        # Figures
        "first_figure": figures >= 1,
        "three_figures": figures >= 3,
        "gallery_opening": figures >= 5,
        "visual_storyteller": figures >= 10,
        "fifteen_figs": figures >= 15,
        "data_viz": figures >= 20,
        "twentyfive_figs": figures >= 25,
        "museum_curator": figures >= 30,
        "forty_figs": figures >= 40,
        "pixel_perfectionist": figures >= 50,

        # Tables
        "first_table": tables >= 1,
        "two_tables": tables >= 2,
        "data_organizer": tables >= 3,
        "four_tables": tables >= 4,
        "excellent": tables >= 5,

        # Equations
        "emc2": equations >= 1,
        "five_eqs": equations >= 5,
        "math_inclined": equations >= 10,
        "fifteen_eqs": equations >= 15,
        "proof_exercise": equations >= 25,
        "thirty_five_eqs": equations >= 35,
        "the_formula": equations >= 50,
        "seventy_five_eqs": equations >= 75,
        "maxwell_proud": equations >= 100,
        "euler_reborn": equations >= 150,

        # Citations
        "citation_needed": citations >= 1,
        "five_cites": citations >= 5,
        "ten_cites": citations >= 10,
        "well_read": citations >= 25,
        "literature_scholar": citations >= 50,
        "seventy_five_cites": citations >= 75,
        "shoulders_giants": citations >= 100,
        "one_twenty_five_cites": citations >= 125,
        "walking_bibliography": citations >= 150,
        "two_hundred_cites": citations >= 200,

        # Chapters
        "abstract_thinker": abstract_words >= 150,
        "abstract_polished": abstract_words >= 300,
        "and_so_it_begins": intro_words >= 1000,
        "intro_complete": intro_words >= 3000,
        "theoretically_speaking": theory_words >= 3000,
        "theory_mastery": theory_words >= 8000,
        "lab_rat": experimental_words >= 2000,
        "results_are_in": results_words >= 2000,
        "results_flood": results_words >= 8000,
        "the_end_is_nigh": outlook_words >= 500,

        # Streaks
        "daily_grind": max_streak >= 3,
        "on_a_roll": max_streak >= 7,
        "ten_streak": max_streak >= 10,
        "fortnight_focus": max_streak >= 14,
        "three_week_streak": max_streak >= 21,
        "monthly_marathon": max_streak >= 30,
        "forty_five_streak": max_streak >= 45,
        "sixty_streak": max_streak >= 60,
        "ninety_streak": max_streak >= 90,
        "total_days_30": total_writing_days >= 30,

        # Time-based
        "night_owl": has_night_owl,
        "early_bird": has_early_bird,
        "weekend_warrior": has_weekend_warrior,
        "lunch_break_scholar": has_lunch,
        "witching_hour": has_witching,
        "five_different_hours": distinct_hours >= 12,

        # Shadow
        "shadow_oops": has_exact_minus_one,
        "shadow_holiday": has_holiday,
        "shadow_nice": has_nice,
        "shadow_zero": has_zero_change,
        "shadow_resurrection": has_comeback,
        "shadow_observer": has_observer,
        "shadow_allnighter": has_all_nighter,
        "shadow_palindrome": has_palindrome,
        "shadow_friday13": has_friday13,
        "shadow_pi": has_pi_day,
        "shadow_fibonacci": has_fibonacci_words,
        "shadow_groundhog": has_groundhog,
        "shadow_thesis_birthday": has_thesis_birthday,
    }

    # Resolve achievements
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

        # Reveal hidden achievements when unlocked
        if unlocked and ach_def.get("hidden"):
            result["name"] = ach_def.get("_secret_name", result["name"])
            result["description"] = ach_def.get("_secret_description", result["description"])
            result["emoji"] = ach_def.get("_secret_emoji", result["emoji"])

        if unlocked:
            result["unlock_date"] = _find_unlock_date(ach_id, daily, commits, conditions)

        results[ach_id] = result

    return results


def _find_unlock_date(ach_id, daily, commits, conditions):
    """Heuristic: find the first date where the achievement condition became true."""
    if not daily:
        return None

    # Word milestone thresholds
    word_thresholds = {
        "hello_world": 10, "baby_steps": 100, "page_one": 300,
        "getting_warmed_up": 500, "first_thousand": 1000, "verbose": 5000,
        "wordy_mcwordface": 10000, "fifteen_k": 15000, "twenty_k": 20000,
        "halfway": 25000, "thirty_k": 30000, "thirty_five_k": 35000,
        "unstoppable": 40000, "forty_five_k": 45000, "magnum_opus": 50000,
        "novelist": 60000, "seventy_k": 70000, "war_and_peace": 80000,
        "ninety_k": 90000, "centennial": 100000,
    }
    if ach_id in word_thresholds:
        threshold = word_thresholds[ach_id]
        for d in daily:
            if d.get("total_words", 0) >= threshold:
                return d["date"]

    # Count thresholds (field, value)
    count_thresholds = {
        "first_figure": ("figures", 1), "three_figures": ("figures", 3),
        "gallery_opening": ("figures", 5), "visual_storyteller": ("figures", 10),
        "fifteen_figs": ("figures", 15), "data_viz": ("figures", 20),
        "twentyfive_figs": ("figures", 25), "museum_curator": ("figures", 30),
        "forty_figs": ("figures", 40), "pixel_perfectionist": ("figures", 50),
        "first_table": ("tables", 1), "two_tables": ("tables", 2),
        "data_organizer": ("tables", 3), "four_tables": ("tables", 4),
        "excellent": ("tables", 5),
        "emc2": ("equations", 1), "five_eqs": ("equations", 5),
        "math_inclined": ("equations", 10), "fifteen_eqs": ("equations", 15),
        "proof_exercise": ("equations", 25), "thirty_five_eqs": ("equations", 35),
        "the_formula": ("equations", 50), "seventy_five_eqs": ("equations", 75),
        "maxwell_proud": ("equations", 100), "euler_reborn": ("equations", 150),
        "citation_needed": ("citations", 1), "five_cites": ("citations", 5),
        "ten_cites": ("citations", 10), "well_read": ("citations", 25),
        "literature_scholar": ("citations", 50), "seventy_five_cites": ("citations", 75),
        "shoulders_giants": ("citations", 100), "one_twenty_five_cites": ("citations", 125),
        "walking_bibliography": ("citations", 150), "two_hundred_cites": ("citations", 200),
    }
    if ach_id in count_thresholds:
        field, threshold = count_thresholds[ach_id]
        for d in daily:
            if d.get(field, 0) >= threshold:
                return d["date"]

    # Daily added thresholds
    daily_add_thresholds = {
        "warm_up_day": 100, "productive_day": 500, "thousand_day": 1000,
        "two_k_day": 2000, "three_k_day": 3000, "five_k_day": 5000,
    }
    if ach_id in daily_add_thresholds:
        threshold = daily_add_thresholds[ach_id]
        for d in daily:
            if d.get("words_added", 0) >= threshold:
                return d["date"]

    # Deletion thresholds
    del_thresholds = {"backspace_warrior": 100, "kill_your_darlings": 500, "scorched_earth": 1000, "nuclear_option": 2000}
    if ach_id in del_thresholds:
        for d in daily:
            if d.get("words_deleted", 0) >= del_thresholds[ach_id]:
                return d["date"]

    if ach_id == "first_delete":
        for d in daily:
            if d.get("words_deleted", 0) > 0:
                return d["date"]
    if ach_id == "net_negative":
        for d in daily:
            if d.get("words_deleted", 0) > d.get("words_added", 0):
                return d["date"]
    if ach_id in ("the_editor", "the_rewriter"):
        threshold = 5000 if ach_id == "the_editor" else 15000
        cumul = 0
        for d in daily:
            cumul += d.get("words_deleted", 0)
            if cumul >= threshold:
                return d["date"]

    # Time-based
    if ach_id == "night_owl":
        for c in commits:
            if c.get("hour", 12) in [0, 1, 2, 3]:
                return c["date"]
    if ach_id == "early_bird":
        for c in commits:
            if c.get("hour", 12) in [4, 5]:
                return c["date"]
    if ach_id == "lunch_break_scholar":
        for c in commits:
            if c.get("hour", 12) == 12:
                return c["date"]
    if ach_id == "witching_hour":
        for c in commits:
            if c.get("hour", 12) == 3:
                return c["date"]

    # Fallback: latest date
    return daily[-1]["date"]


def evaluate_and_save(history_data):
    """Evaluate achievements and save to JSON."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Load previous state to detect new unlocks
    previous = {}
    if ACHIEVEMENTS_FILE.exists():
        with open(ACHIEVEMENTS_FILE) as f:
            prev_data = json.load(f)
            previous = prev_data.get("achievements", {})

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
