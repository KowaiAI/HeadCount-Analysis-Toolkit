```
 │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │
 │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │
 │ │ ██  ██ ███████  █████  ████   ██████  █████  ██  ██ ██   ██ ████████│ │
 │ │ ██  ██ ██      ██   ██ ██  ██ ██     ██   ██ ██  ██ ███  ██    ██   │ │
 │ │ ██████ █████   ███████ ██  ██ ██     ██   ██ ██  ██ ██ █ ██    ██   │ │
 │ │ ██  ██ ██      ██   ██ ██  ██ ██     ██   ██ ██  ██ ██  ███    ██   │ │
 │ │ ██  ██ ███████ ██   ██ ████   ██████  █████   ████  ██   ██    ██   │ │
 │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │
 │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │
```  
```

### *When they won't publish the data, count it yourself.*

![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)
![MIT License](https://img.shields.io/badge/license-MIT-green.svg)
![Linux](https://img.shields.io/badge/platform-linux-lightgrey.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)

---

## 💡 What is HeadCount?

**HeadCount** is a toolkit for scraping public image databases and rapidly sorting them by category — built for investigating demographic disparities in public records.

| Feature | Description |
|---------|-------------|
| 🔍 **Scrape** | Pull images from JavaScript-rendered public databases |
| ⌨️ **Sort** | Keyboard-driven categorization (~1 sec per image) |
| 📊 **Count** | Aggregate results automatically |
| 🔄 **Resume** | Pick up where you left off |

---

## 🔥 The DC Investigation

> **DC is one of only 4 U.S. jurisdictions that refuses to publish racial data for its sex offender registry.**
>
> So we scraped 1,066 mugshots and counted ourselves.

### What We Found

| Race | DC Registry | National Avg |
|:-----|:-----------:|:------------:|
| Black | **87.6%** | 27% |
| White | **7.1%** | 72% |
| Hispanic | 4.3% | — |
| Asian | 0.4% | — |

### The Disparity

```
DC Registry:      ██░░░░░░░░░░░░░░░░░░  7% white

National Avg:     ██████████████░░░░░░ 72% white
```

**10x less white than the national average.**

---

## ⚡ Quick Start

```bash
# Clone
git clone https://github.com/KowaiAI/headcount.git && cd headcount

# Install
pip install selenium webdriver-manager requests pillow --break-system-packages
sudo apt install python3-tk python3-pil.imagetk

# Scrape
python3 scrapers/dc_registry.py

# Sort
python3 headcount.py

# Count
cd dc_photos_sorted && for dir in */; do echo "$dir $(ls "$dir" | wc -l)"; done
```

---

## 📦 Installation

### Debian / Ubuntu

```bash
pip install selenium webdriver-manager requests pillow --break-system-packages
sudo apt install python3-tk python3-pil.imagetk chromium-browser
```

### Arch Linux

```bash
pip install selenium webdriver-manager requests pillow --break-system-packages
sudo pacman -S tk python-pillow chromium
```

### macOS

```bash
brew install python-tk
pip3 install selenium webdriver-manager requests pillow
```

---

## 🎮 Usage

### Sorting Images

```bash
python3 headcount.py
```

**Keyboard controls:**

| Key | Action |
|:---:|--------|
| `B` | Black |
| `W` | White |
| `H` | Hispanic |
| `A` | Asian |
| `O` | Other |
| `S` | Skip |
| `Q` | Quit |

> **One keypress. No enter. No mouse. Fast.**

### Counting Results

```bash
cd dc_photos_sorted
for dir in */; do echo "$dir $(ls "$dir" | wc -l)"; done
```

Output:
```
black/     934
white/     76
hispanic/  46
asian/     4
other/     6
skip/      0
```

### Terminal Mode (No GUI)

```bash
python3 headcount_terminal.py
```

Opens images in your default viewer. Type + Enter.

---

## 🗂️ Repo Structure

```
headcount/
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── headcount.py            # GUI sorting tool
├── headcount_terminal.py   # Terminal sorting tool
├── docs/
│   └── investigation.md    # DC investigation writeup
└── scrapers/
    ├── dc_registry.py      # DC sex offender registry scraper
    └── template.py         # Template for new scrapers
```

After running the scraper and sorter, you'll have locally:
```
dc_photos/                  # Raw scraped images (gitignored)
dc_photos_sorted/           # Sorted output (gitignored)
├── black/
├── white/
├── hispanic/
├── asian/
├── other/
└── skip/
```

---

## 🔬 Methodology

For **defensible research**:

| Step | Why |
|------|-----|
| 📝 Document source | URL, date, limitations |
| 👤 Single rater | Consistency across all images |
| 👥 Second rater | Independent verification (10-20% sample) |
| 📊 Calculate agreement | Should be >90% |
| ⚠️ Acknowledge limits | Visual assessment ≠ self-identification |

---

## 🛠️ Adapting for Other Databases

HeadCount works on any image collection. See `scrapers/template.py` for a starting point.

**Potential applications:**
- Mugshot databases
- Public employee directories  
- Housing listings
- Any public image dataset

---

## ⚖️ Legal

**DO:**
- ✅ Use on public databases
- ✅ Aggregate statistical analysis
- ✅ Journalism & research

**DON'T:**
- ❌ Harass or contact individuals
- ❌ Access non-public databases
- ❌ Anything illegal

---

## 🤝 Contributing

PRs welcome for:

- [ ] New scrapers for public databases
- [ ] Windows / Mac support improvements
- [ ] Analysis & visualization tools
- [ ] Documentation & examples

---

## 📜 License

**MIT** — free to use, modify, and distribute.

---

**HeadCount** · *When they won't publish the data, count it yourself.*
