# Q2BSTUDIO Auditor

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

A Python-based forensic investigation tool for analyzing industrial-scale automated content generation systems. This is not just a scraper—it's a **systematic documentation framework** for observing emergent behavior in digital ecosystems where AI generates content at industrial scale, without attribution, without curation, and possibly without human supervision.

**This project transforms raw data into evidence, patterns into insights, and observations into reproducible science.**

## Background

This tool was created following the discovery that my technical article about [OBSIDIAN Neural](https://github.com/innermost47/ai-dj) (an open-source AI music VST plugin) was reproduced, translated, and republished with commercial links injected by Q2BSTUDIO's automated system.

When their blog showed 36,516+ pages of content, I developed this auditor to systematically document their publishing volume and patterns.

**Full case study:** https://dev.to/innermost_47/when-ai-content-systems-reproduce-content-without-attribution-a-documented-case-study-1h0g

## Automated Plagiarism as an Ecological Phenomenon

This project goes beyond simple content analysis. It documents a **behavioral pattern emerging in digital ecosystems**: automated systems producing publications at industrial rates without human supervision, creating what could be described as "machines writing for machines."

### The Mission

- **Transparency:** Making visible the scale and patterns of automated content generation
- **Documentation:** Creating verifiable, timestamped records of industrial-scale publishing
- **Preservation:** Archiving evidence for future analysis and accountability
- **Critical Analysis:** Identifying duplication patterns, plagiarism forensics, and content similarity at scale

### Why This Matters

When AI systems generate thousands of articles per day—each potentially derived from human-created content—we need tools to:

1. **Measure the scale** of automated content generation
2. **Detect patterns** of content duplication and plagiarism
3. **Preserve evidence** for accountability and transparency
4. **Analyze behavior** of systems operating without apparent human oversight

This is not about condemning technology. It's about **documenting it systematically** so we can understand its impact on information ecosystems, attribution, and the value of human creativity.

## Features

### Core Pipeline (Reproducible & Automated)
- **Unified Entry Point:** Single-command pipeline via `run.py` orchestrating the complete workflow
- **Systematic Blog Scraping:** Crawls through all pagination pages with configurable sampling
- **Data Extraction:** Captures article titles, URLs, publication dates, and page numbers
- **Checkpoint System:** Automatic progress saving with crash resumption capability
- **CSV Export:** Structured data export for further analysis

### Analysis & Forensics
- **Statistical Analysis:** Comprehensive reports on publication patterns and volume metrics
- **Similarity Detection:** N-gram based analysis to identify duplicate and plagiarized content
- **Clustering:** Automatic grouping of identical or near-identical articles
- **Duplication Rate:** Calculate percentage of unique vs. duplicated content
- **Plagiarism Forensics:** Flag articles with >85% similarity for investigation

### Visualization & Reporting
- **Static Visualizations:** Publication timelines, daily production charts, statistical summaries
- **Interactive Dashboard:** Streamlit-based web interface with date filters and drill-down analysis
- **Comparative Analysis:** Benchmark against major publishers (NY Times, TechCrunch, The Verge)
- **Real-time Metrics:** Articles per second, peak production days, frequency analysis

### Evidence Preservation
- **Wayback Machine Integration:** Automated archiving to Internet Archive
- **Configurable Sampling:** Archive subsets (e.g., 500 random articles) to preserve evidence
- **Archive Verification:** Track archive URLs and verification status
- **Timestamped Records:** All data includes capture timestamps for accountability

### Technical Excellence
- **Rate Limiting:** Controlled request rates to respect server resources
- **Robots.txt Compliance:** Ethical scraping with configurable delays
- **Exponential Backoff:** Automatic retry logic for failed requests
- **Spanish Date Parsing:** Multi-locale support for international content
- **Crash Recovery:** Resume from any point without data loss

## Requirements

- Python 3.8+
- pip (Python package manager)

### Python Dependencies

```bash
requests>=2.31.0
beautifulsoup4>=4.12.0
matplotlib>=3.7.0
streamlit>=1.28.0
plotly>=5.17.0
pandas>=2.0.0
hydra-core>=1.3.0
```

All dependencies are listed in `requirements.txt` and will be installed automatically.

**Note:** Hydra is a configuration management framework that enables flexible and reproducible visualizations through YAML configuration files.

## Installation

### Option 1: From Source (Development)

```bash
git clone https://github.com/innermost47/q2bs.git
cd q2bs
python -m venv env
source env/bin/activate  # On macOS/Linux
# or: env\Scripts\activate  # On Windows
pip install -r requirements.txt
```

### Option 2: Via pip (When Published to PyPI)

```bash
pip install q2bs-auditor
```

This will install the package and make the following commands available:
- `q2bs-audit` - Main pipeline runner
- `q2bs-similarity` - Similarity analysis tool
- `q2bs-dashboard` - Interactive dashboard

## Usage

### Reproducible Pipeline (Recommended - run.py)

The repository includes a **unified entry point** that orchestrates the complete pipeline in a single command. This makes the investigation **reproducible and auditable**: anyone can clone the repo and regenerate the same results.

```bash
# Fresh run: scrape → analyze → visualize
python run.py

# Resume from latest checkpoint and continue scraping
python run.py --resume

# Skip scraping, regenerate report + graphs only
python run.py --visualize-only

# Sample strategy: scrape every 10th page instead of all pages
python run.py --sample 10

# Archive 500 random articles to Wayback Machine
python run.py --archive 500

# Combined: resume, sample pages, and archive
python run.py --resume --sample 5 --archive 500
```

**Under the hood**, `run.py` orchestrates:
- `Q2BStudioAuditor` (scraping, checkpointing, statistics)
- `Q2BDataVisualizer` (graphs and timeline plots)
- `WaybackArchiver` (evidence preservation via Internet Archive)
- `SimilarityAnalyzer` (plagiarism detection - run separately)

### Legacy Interactive Mode (main.py)

The original interactive script with menu-driven prompts:

```bash
python main.py
```

This script will:
1. Detect the maximum number of blog pages (36,516+ as of December 2025)
2. Ask for confirmation before scraping
3. Scrape all articles systematically
4. Generate statistical reports
5. Create data visualizations
6. Optionally archive a sample to Wayback Machine

### Resume from Checkpoint

The auditor includes a checkpoint system that allows you to resume interrupted scraping sessions:

```bash
python main.py
```

When you run the script, you'll be presented with:

1. A list of existing checkpoint directories
2. Option to select a checkpoint to resume from
3. Option to start fresh (new scraping)
4. Option to visualize-only mode (skip scraping)

**The script automatically:**

- Calculates which page to resume from based on article IDs
- Avoids duplicate articles
- Continues in the same output directory
- Preserves all previously scraped data

**Example workflow:**

```
Available checkpoints:
0. Start fresh (new scraping)
1. q2b_audit_20251208_103810 - 242,191 articles - 2025-12-08T10:38:10

Select checkpoint number (0 for fresh start): 1
Visualize only (skip scraping)? (yes/no): no

Loading checkpoint from: q2b_audit_20251208_103810
Loaded 242,191 articles from checkpoint
Min article ID scraped (last article): 91,643
Calculated resume page: 27,373

Resuming from page 27,373
This will scrape 10,184 pages (from 27,373 to 37,556). Continue? (yes/no):
```

### Similarity Analysis (Plagiarism Detection)

Run forensic analysis to detect duplicate and plagiarized content:

```bash
python similarity_analyzer.py q2b_audit_YYYYMMDD_HHMMSS
```

Or with custom threshold:

```bash
python similarity_analyzer.py q2b_audit_YYYYMMDD_HHMMSS --threshold 0.90
```

**This will generate:**
- `similarity_report.json` - Overall statistics and metrics
- `similar_pairs.json` - Pairs of articles with high similarity (>= threshold)
- `duplicate_clusters.json` - Groups of exact or near-exact duplicates
- `similarity_summary.csv` - Summary metrics for quick review

**Key metrics:**
- **Exact match clusters:** Articles with identical normalized titles
- **Similar pairs:** Articles above similarity threshold (default 85%)
- **Duplication rate:** Percentage of articles that are duplicates
- **Uniqueness rate:** Percentage of truly unique content

### Interactive Dashboard

Launch the Streamlit dashboard for visual exploration:

```bash
streamlit run dashboard.py
```

**Features:**
- 📊 **Real-time metrics**: Total articles, avg per day, peak days, frequency
- 📅 **Date filtering**: Explore specific time ranges
- 📈 **Interactive charts**: Bar charts, timelines, histograms with Plotly
- 🔍 **Search**: Find articles by title keywords
- 📉 **Distribution analysis**: Daily patterns, day-of-week trends, monthly aggregates
- 🎯 **Checkpoint selection**: Switch between different scraped datasets

The dashboard runs in your browser and provides an intuitive interface for exploring the data without coding.

### Hydra-Powered Visualization (New!)

Use Hydra configuration management for advanced visualization customization:

```bash
# Basic usage with default configuration
python visualize_with_hydra.py checkpoint_dir=q2b_audit_20251208_103810

# Use dark theme color scheme
python visualize_with_hydra.py checkpoint_dir=q2b_audit_20251208_103810 visualization=dark

# Override specific colors
python visualize_with_hydra.py checkpoint_dir=q2b_audit_20251208_103810 'visualization.colors.primary="#FF0000"'

# Change output DPI for higher quality
python visualize_with_hydra.py checkpoint_dir=q2b_audit_20251208_103810 output.dpi=600

# Combine multiple overrides
python visualize_with_hydra.py checkpoint_dir=q2b_audit_20251208_103810 visualization=dark output.dpi=150
```

**Benefits of Hydra configuration:**
- 🎨 **Flexible styling**: Easy to switch between color schemes and themes
- ⚙️ **Reproducible**: All visualization parameters in versioned config files
- 🔧 **Command-line overrides**: Change any parameter without editing code
- 📁 **Multiple configs**: Create custom configurations for different use cases
- 🔄 **Composable**: Mix and match configuration groups

**Available configuration options:**
- Colors (primary, secondary, partial_day, average_line, etc.)
- Chart dimensions (width, height for each chart type)
- Fonts (title, labels, legend, annotations)
- Chart settings (alpha, line width, marker size, grid alpha)
- Output settings (DPI, bbox_inches, graphs directory)
- Label display thresholds
- Comparison sources (benchmarks)

Configuration files are located in `config/` directory. Create your own theme by adding a new YAML file in `config/visualization/`.

### Visualization-Only Mode

If you want to regenerate visualizations without re-scraping:

```bash
python run.py --visualize-only
```

This will:
- Load the latest checkpoint
- Regenerate all reports
- Create fresh visualizations
- Skip the scraping phase entirely

**Use cases:**
- Update graphs with new styling
- Generate reports after manual data cleaning
- Create visualizations for different time periods

### Output Structure

After running, you'll get a timestamped directory with comprehensive analysis results:

```
q2b_audit_YYYYMMDD_HHMMSS/
├── articles.csv                  # All articles with metadata
├── daily_summary.csv             # Articles per day aggregation
├── checkpoint.json               # Progress checkpoint for resumption
├── report.json                   # Statistical analysis report
│
├── archiving_checkpoint.json     # Wayback archiving progress
├── articles_archived.csv         # Articles with archive URLs
├── archive_report.json           # Archiving statistics
├── wayback_urls.txt              # List of Wayback URLs for verification
│
├── similarity_report.json        # Plagiarism detection statistics
├── similar_pairs.json            # Article pairs with high similarity
├── duplicate_clusters.json       # Groups of duplicate content
├── similarity_summary.csv        # Quick summary of duplication metrics
│
└── graphs/                       # Static visualizations
    ├── 1_daily_articles.png      # Daily production bar chart
    ├── 2_timeline.png            # Publication timeline graph
    └── 3_stats_summary.png       # Statistical summary comparison
```

**File descriptions:**
- **articles.csv**: Complete dataset with title, URL, date, page number
- **report.json**: Aggregate statistics, date ranges, daily averages
- **similarity_report.json**: Duplication rates, cluster counts, uniqueness metrics
- **duplicate_clusters.json**: Top 100 clusters of identical articles
- **similar_pairs.json**: Pairs of articles with >= threshold similarity

## Key Findings (December 2025)

Based on analysis of the period November 20 - December 7, 2025:

- **144,966 articles documented** (partial dataset - computer crashed during scraping)
- **8,401 articles per day** on average
- **Peak day:** 10,251 articles (December 4, 2025)
- **Frequency:** 1 article every 10.3 seconds

For comparison (industry estimates - approximate):

- TechCrunch: ~40 articles/day
- The Verge: ~30 articles/day
- The New York Times: ~250 articles/day

## Files Description

### `q2b_studio_auditor.py`

Core scraping engine that:

- Fetches blog pages systematically
- Parses article metadata
- Handles Spanish date formats
- Generates statistical reports
- Manages checkpoints

### `q2b_data_visualizer.py`

Visualization module that creates:

- Daily article production bar charts
- Publication timeline graphs
- Comparative statistics with major publishers
- All charts with proper labeling and context

### `wayback_archiver.py`

Archiving system that:

- Submits URLs to Wayback Machine
- Checks for existing archives
- Handles retry logic for failed submissions
- Exports archive URLs for verification

### `main.py`

Legacy interactive entry point that orchestrates:

- User confirmation workflow
- Scraping execution
- Report generation
- Visualization creation
- Optional archiving

### `run.py`

Modern unified pipeline runner:

- Command-line interface with argparse
- Reproducible single-command workflow
- Resume, visualize-only, and sampling modes
- Orchestrates all modules in a clean pipeline

### `similarity_analyzer.py`

Plagiarism detection module:

- N-gram similarity analysis (character-level)
- Jaccard similarity coefficient calculation
- Exact match clustering
- Duplicate pattern identification
- Forensic reporting

### `dashboard.py`

Interactive Streamlit dashboard:

- Web-based visual interface
- Real-time metric displays
- Interactive Plotly charts
- Date filtering and search
- Checkpoint selection

## Configuration

### Scraping Parameters

In `main.py`, you can adjust:

```python
# Scrape every Nth page (1 = all pages, 10 = every 10th page)
auditor.scrape_all_pages(max_page, start_page=1, sample_every=1)

# Archive sample size
archiver.archive_sample(sample_size=500)
```

### Technical Scraping Methodology

This tool implements **responsible and ethical web scraping** practices:

#### Rate Limiting
- **0.5 seconds** between page requests (controlled delay)
- **3 seconds** between Wayback Machine submissions
- **5 seconds** retry delay on timeouts
- Configurable via code for different target servers

#### Robots.txt Respect
While Q2BSTUDIO's robots.txt does not explicitly block crawling of blog pages, this tool:
- Uses human-like User-Agent strings
- Implements polite delays between requests
- Does not overwhelm servers with parallel requests
- Respects HTTP 429 (rate limit) responses with exponential backoff

#### Sampling Strategies
The tool supports flexible sampling to reduce load and focus analysis:

```bash
# Scrape all pages (default)
python run.py --sample 1

# Sample 10% of pages (every 10th page)
python run.py --sample 10

# Sample 1% for quick testing (every 100th page)
python run.py --sample 100
```

**When to sample:**
- **Testing:** Use high sampling (--sample 100) for quick validation
- **Trend analysis:** 10% sample (--sample 10) captures patterns without full scrape
- **Complete documentation:** Full scrape (--sample 1) for comprehensive evidence

#### Crash Resumption
The checkpoint system enables resilient scraping:
- **Automatic saves** every 100 pages
- **Resume from last checkpoint** using `--resume` flag
- **No duplicate articles** - resume calculates correct starting page
- **Preserves all progress** even after crashes or interruptions

#### Error Handling & Exponential Backoff
```python
# Pseudo-code of retry logic
for attempt in range(max_retries):
    try:
        response = session.get(url, timeout=15)
        return response
    except Timeout:
        wait_time = base_delay * (2 ** attempt)  # Exponential: 5s, 10s, 20s
        time.sleep(wait_time)
```

**Retry strategy:**
- Initial timeout: 15 seconds
- Max retries: 2 attempts
- Backoff: 5s → 10s → 20s
- Graceful degradation: Skip failed pages and continue

## Ethical Considerations

This tool was developed for legitimate investigative purposes:

- Documenting publicly available information
- Analyzing content patterns
- Preserving evidence of plagiarism
- Supporting transparency in automated publishing

**Please use responsibly:**

- Respect robots.txt directives
- Don't overwhelm servers with requests
- Use for research and documentation purposes
- Comply with applicable laws and terms of service

## Known Issues

### Wayback Machine Archiving

The Wayback Machine integration may experience issues:

- **Timeout errors:** The Internet Archive's save service can be slow
- **Rate limiting:** Heavy usage may trigger temporary blocks
- **Archive verification:** Some archived URLs may not be immediately accessible
- **Incomplete snapshots:** Not all pages successfully archive on first attempt

**Workaround:** The script saves all URLs to `wayback_urls.txt` so you can verify archives manually or re-submit failed URLs later.

### Large Dataset Handling

For very large scrapes (30,000+ pages):

- Consider using `sample_every` parameter to sample pages
- Monitor disk space (CSV files can grow large)
- Be prepared for multi-hour runtime
- The checkpoint system helps recover from crashes

## Data Analysis Tips

### Sample Visualizations

The tool generates three types of visualizations:

#### 1. Statistical Summary

![Stats Summary Example](graphs/3_stats_summary.png)

Shows total articles, daily average, and comparison with major publishers.

#### 2. Publication Timeline

![Timeline Example](graphs/2_timeline.png)

Displays article output over time with peak detection.

#### 3. Daily Production

![Daily Production Example](graphs/1_daily_articles.png)

Breakdown of articles per day with average line.

### Using the CSV Files

```python
import pandas as pd

# Load articles
df = pd.read_csv('q2b_audit_TIMESTAMP/articles.csv')

# Find articles by keyword
keyword_articles = df[df['title'].str.contains('AI', case=False)]

# Articles by date
daily_counts = df['date_parsed'].value_counts().sort_index()

# Most common page numbers (detect patterns)
page_distribution = df['page_num'].value_counts()
```

### Checking for Your Content

```python
# Search for specific phrases
your_phrases = ['your unique phrase', 'another phrase']
matches = df[df['title'].str.contains('|'.join(your_phrases), case=False)]
print(f"Found {len(matches)} potential matches")
```

## Publishing to PyPI

This project is structured as a proper Python package and can be published to PyPI for global distribution.

### Package Structure

The repository includes:
- `setup.py` - Package configuration and metadata
- Console entry points: `q2bs-audit`, `q2bs-similarity`, `q2bs-dashboard`
- Dependencies specification in `requirements.txt`
- README for PyPI long description

### To Publish (for maintainers)

```bash
# Install build tools
pip install build twine

# Build distribution packages
python -m build

# Upload to PyPI (requires credentials)
twine upload dist/*
```

### After Publishing

Users can install globally with:

```bash
pip install q2bs-auditor
```

And use commands directly:

```bash
q2bs-audit --resume --archive 500
q2bs-similarity q2b_audit_YYYYMMDD_HHMMSS
streamlit run $(python -c "import dashboard; print(dashboard.__file__)")
```

## Contributing

If you've experienced similar automated plagiarism or want to improve the tool:

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Submit a pull request

Particularly welcome:

- Multi-language content similarity detection
- Machine learning-based clustering
- Enhanced forensic reporting
- Performance optimizations for large datasets
- Additional data sources and comparative analysis

## Legal

This tool is provided for research, documentation, and investigative journalism purposes. Users are responsible for ensuring their use complies with applicable laws, including:

- Copyright law
- Computer fraud and abuse laws
- Terms of service agreements
- Data protection regulations

The author makes no warranties about the tool's functionality or the accuracy of data collected.

## Citation

If you use this tool in research or journalism, please cite:

```
CHARRETIER, A. (2025). Q2BSTUDIO Auditor.
GitHub: https://github.com/innermost47/q2bs
Case study: https://dev.to/innermost_47/when-ai-content-systems-reproduce-content-without-attribution-a-documented-case-study-1h0g
```

## Contact

- **Author:** Anthony CHARRETIER
- **Website:** https://anthony-charretier.fr
- **GitHub:** https://github.com/innermost47

## License

MIT License

Copyright (c) 2025 Anthony CHARRETIER

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
