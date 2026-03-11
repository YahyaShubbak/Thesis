# Thesis Quest — Standalone Game Concept

## Overview

**Thesis Quest** is a gamification layer for academic thesis writing. Students clone the tool into their LaTeX thesis repository and it tracks their git-based writing progress, awarding achievements and visualizing metrics — turning the long grind of thesis writing into a Cookie-Clicker-inspired progression game.

## Installation & Setup Flow

```
git clone <thesis-quest-repo> dashboard/
cd dashboard/
python3 setup.py   # or: ./init.sh
```

### First-Run Initialization (`setup.py`)

Interactive prompts on first run:

1. **Thesis type**: `Bachelor / Master / PhD (Dr.)`
   - Sets default word/page targets:
     - Bachelor: ~12,000 words / 40 pages
     - Master: ~25,000 words / 80 pages
     - PhD: ~50,000 words / 150 pages
   - Adjusts achievement thresholds accordingly (e.g. "The Magnum Opus" = target reached)

2. **Thesis topic** (free text, e.g. "Traveling Wave Magnetophoresis"):
   - Used for dashboard title/subtitle

3. **Field of study**: `Physics / Chemistry / Biology / Engineering / Computer Science / Mathematics / Other`
   - Loads a matching **achievement pack** (see below)

4. **Keyword stickers** (optional, comma-separated):
   - e.g. `"nanoparticles, thin films, magnetism, lab-on-a-chip"`
   - Used to flavor achievement names/descriptions in future AI-generated packs

5. **Git author name(s)**: auto-detected from `git log`, user confirms which are theirs.

6. **Content files**: auto-detected `.tex` files under `content/`, user confirms or edits the list.

Output: a `config.json` that stores all choices. Subsequent runs skip the wizard.

## Project Structure (Standalone)

```
thesis-quest/
├── README.md                  # How to install, configure, play
├── setup.py                   # First-run interactive wizard
├── config.json                # Generated: user choices & thresholds
├── collect_data.py            # Git history → history.json
├── achievements.py            # Achievement definitions + evaluation
├── generate_dashboard.py      # HTML dashboard generation
├── run.sh                     # One-command: collect → evaluate → generate → open
├── template.html              # Dashboard HTML template
├── packs/                     # Achievement packs by discipline
│   ├── base.py                # Universal achievements (word counts, streaks, time, editing)
│   ├── physics.py             # Physics-themed achievements
│   ├── chemistry.py           # Chemistry-themed (future)
│   ├── biology.py             # Biology-themed (future)
│   ├── cs.py                  # Computer Science-themed (future)
│   └── custom.py              # User-defined achievements (optional)
├── data/
│   ├── history.json
│   └── achievements.json
└── output/
    └── index.html
```

## Achievement Pack System

### Base Pack (universal, always loaded)

All non-domain-specific achievements that apply to any thesis:
- **Writing Milestones**: word count thresholds (scaled to thesis type)
- **Daily Productivity**: daily/weekly word output
- **Editing & Deletion**: revision milestones
- **Figures, Tables, Equations, Citations**: count-based
- **Chapter Progress**: chapter-specific word thresholds
- **Consistency & Streaks**: writing day streaks
- **Time-Based**: commit times (night owl, early bird, etc.)
- **Shadow/Secret**: fun hidden achievements

### Discipline Packs (one loaded based on field)

Each discipline pack adds ~15–25 themed achievements referencing concepts from that field.

**Example — Physics pack** (current):
- Dipole Moment, Exchange Coupling, Stoner-Wohlfarth, Brownian Motion, DLVO Force Balance, Superparamagnetic, Traveling Wave, etc.

**Example — Chemistry pack** (future):
- "First Reaction" (experimental chapter started), "Catalyst" (5-day writing streak), "Titration" (exactly hit a word target), "Noble Gas" (commit with 0 word changes), "Avogadro's Number" (reach 6,022 words), etc.

**Example — CS pack** (future):
- "Hello World" (first sentence), "Stack Overflow" (delete 1000 words then add 1500 in same day), "Big O" (10,000 words), "Recursion" (same word count two days in a row), "Merge Conflict" (large deletion + large addition in same day), etc.

### Custom Pack

Users can define their own achievements in `packs/custom.py` following a simple template:
```python
ACHIEVEMENTS = [
    {
        "id": "my_achievement",
        "name": "Custom Achievement",
        "description": "Do something specific.",
        "emoji": "⭐",
        "tier": "gold",
        "condition": lambda stats: stats["total_words"] >= 42000,
    },
]
```

## Thesis-Type Scaling

Achievement thresholds adapt to the thesis type:

| Achievement       | Bachelor | Master  | PhD     |
|-------------------|----------|---------|---------|
| Target Reached    | 12,000   | 25,000  | 50,000  |
| "Halfway There"   | 6,000    | 12,500  | 25,000  |
| Page One          | 250      | 300     | 300     |
| Sprint Week       | 2,500    | 4,000   | 5,000   |

A scaling factor is applied to word-count thresholds based on the ratio to PhD targets.

## How It Works — User Journey

1. Student clones Thesis Quest into their thesis repo
2. Runs `setup.py` — answers 5 questions, config is saved
3. Writes their thesis as usual (LaTeX + git commits)
4. Periodically runs `./run.sh` (or sets up a git hook / cron job)
5. Opens `output/index.html` — sees progress charts + achievement grid
6. Locked achievements shown as "?" cards (Cookie Clicker style) with hints
7. New achievements trigger toast notifications
8. Student is motivated by the progression system to keep writing

## Future Ideas (Out of Scope for Now)

- **Leaderboard**: opt-in anonymous comparison with other thesis writers
- **AI-generated achievement packs**: feed keywords and get themed achievements
- **VS Code extension**: show achievement toasts directly in the editor
- **Git hook integration**: auto-run on every commit
- **Progress sharing**: export a badge/image for social media
- **Multiplayer mode**: writing group challenges
- **Sound effects**: achievement unlock sounds like Cookie Clicker
- **Prestige system**: "defend" your thesis to prestige and reset achievements with multipliers
