# Q2BS Auditor - Project Structure

Understanding the codebase architecture and organization.

## Directory Structure

```
q2bs/
├── README.md                      # Main documentation
├── LICENSE                        # MIT License
├── requirements.txt               # Python dependencies
├── setup.py                       # PyPI package configuration
├── MANIFEST.in                    # Package file inclusion rules
├── .gitignore                     # Git exclusion patterns
│
├── QUICK_START.md                 # 5-minute getting started guide
├── USAGE_EXAMPLES.md              # Comprehensive usage examples
├── CONTRIBUTING.md                # Contribution guidelines
├── CHANGELOG.md                   # Version history
├── PROJECT_STRUCTURE.md           # This file
│
├── run.py                         # ⭐ Main entry point (reproducible pipeline)
├── main.py                        # Legacy interactive script
│
├── q2b_studio_auditor.py          # Core scraping engine
├── q2b_data_visualizer.py         # Static visualization generator
├── wayback_archiver.py            # Internet Archive integration
├── similarity_analyzer.py         # Plagiarism detection module
├── dashboard.py                   # Interactive Streamlit dashboard
│
├── sample_data/                   # Sample dataset for testing
│   ├── articles.csv
│   ├── daily_summary.csv
│   └── report.json
│
├── graphs/                        # Static visualizations (generated)
│   ├── 1_daily_articles.png
│   ├── 2_timeline.png
│   └── 3_stats_summary.png
│
└── q2b_audit_YYYYMMDD_HHMMSS/    # Output directories (generated, gitignored)
    ├── articles.csv
    ├── checkpoint.json
    ├── report.json
    ├── similarity_*.json
    └── graphs/
```

## Core Modules

### run.py (Main Pipeline)

**Purpose**: Unified entry point for the complete reproducible pipeline.

**Key Functions**:
- `_select_or_create_output_dir()`: Handle checkpoint resumption
- `run_scrape()`: Execute scraping phase
- `run_analysis_and_visualization()`: Generate reports and graphs
- `run_archiving()`: Archive to Wayback Machine
- `build_parser()`: CLI argument parsing
- `main()`: Pipeline orchestration

**CLI Arguments**:
- `--resume`: Resume from latest checkpoint
- `--visualize-only`: Skip scraping, regenerate visualizations
- `--sample N`: Scrape every N-th page
- `--archive K`: Archive K random articles

**Dependencies**: q2b_studio_auditor, q2b_data_visualizer, wayback_archiver

---

### q2b_studio_auditor.py (Scraping Engine)

**Purpose**: Core web scraping, data extraction, and checkpoint management.

**Class**: `Q2BStudioAuditor`

**Key Methods**:
- `__init__()`: Initialize session and output directory
- `get_max_page_number()`: Detect total pages from pagination
- `scrape_page()`: Extract articles from single page
- `scrape_all_pages()`: Orchestrate full scraping with checkpoints
- `parse_spanish_date()`: Handle Spanish date formats
- `validate_url()`: URL validation
- `validate_article_data()`: Data integrity checks
- `save_checkpoint()`: Periodic progress saving
- `load_checkpoint()`: Resume from saved state
- `generate_report()`: Statistical analysis
- `calculate_resume_page()`: Determine where to resume

**Rate Limiting**: 0.5s between requests, 5s retry delay

**Checkpointing**: Every 100 pages, includes articles.csv + checkpoint.json

---

### q2b_data_visualizer.py (Static Visualizations)

**Purpose**: Generate publication charts using matplotlib.

**Class**: `Q2BDataVisualizer`

**Key Methods**:
- `create_visualizations()`: Generate all charts
- `plot_daily_articles()`: Bar chart of daily production
- `plot_daily_timeline()`: Line graph with averages
- `plot_stats_summary()`: KPI comparison panel

**Output**: PNG files in `{output_dir}/graphs/`

**Dependencies**: matplotlib

---

### wayback_archiver.py (Evidence Preservation)

**Purpose**: Submit articles to Internet Archive's Wayback Machine.

**Class**: `WaybackArchiver`

**Key Methods**:
- `load_data()`: Load articles from CSV
- `archive_to_wayback()`: Submit single URL
- `check_existing_archive()`: Verify if already archived
- `archive_sample()`: Archive random sample
- `save_checkpoint()`: Save archiving progress
- `save_results()`: Export archive URLs

**Rate Limiting**: 3s between submissions

**Output**: articles_archived.csv, archive_report.json, wayback_urls.txt

---

### similarity_analyzer.py (Plagiarism Detection)

**Purpose**: Detect duplicate and similar content using n-gram analysis.

**Class**: `SimilarityAnalyzer`

**Key Methods**:
- `load_articles()`: Load dataset from CSV
- `normalize_text()`: Text preprocessing
- `generate_ngrams()`: Create character n-grams
- `calculate_jaccard_similarity()`: Similarity coefficient
- `find_similar_pairs()`: Pairwise comparison (O(n²))
- `cluster_by_exact_match()`: Fast exact duplicate detection
- `generate_report()`: Forensic statistics
- `save_results()`: Export JSON/CSV reports

**Thresholds**:
- Default similarity: 0.85 (85%)
- Pairwise comparison limit: 10,000 articles

**Output**: similarity_report.json, similar_pairs.json, duplicate_clusters.json

---

### dashboard.py (Interactive Interface)

**Purpose**: Web-based exploration using Streamlit and Plotly.

**Key Functions**:
- `load_latest_checkpoint()`: Auto-detect checkpoints
- `load_data()`: Load CSV and JSON
- `main()`: Dashboard UI

**Features**:
- KPI metrics (total articles, avg/day, peak, frequency)
- Date range filtering
- Interactive Plotly charts
- Article search
- Checkpoint selection

**Launch**: `streamlit run dashboard.py`

**Dependencies**: streamlit, plotly, pandas

---

### main.py (Legacy Interactive)

**Purpose**: Original interactive menu-driven script.

**Key Functions**:
- `validate_yes_no_input()`: User input validation
- `validate_numeric_input()`: Numeric validation
- `list_checkpoints()`: Find checkpoint directories
- `select_checkpoint()`: User checkpoint selection
- `main()`: Interactive workflow

**Status**: Maintained for backwards compatibility

---

## Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                         run.py                              │
│                    (Pipeline Orchestrator)                  │
└──────────────┬──────────────────────────────┬───────────────┘
               │                              │
               ▼                              ▼
    ┌──────────────────────┐      ┌──────────────────────┐
    │ Q2BStudioAuditor     │      │  WaybackArchiver     │
    │ (Scraping)           │      │  (Archiving)         │
    └──────────┬───────────┘      └──────────────────────┘
               │
               ▼
    ┌──────────────────────┐
    │ articles.csv         │
    │ checkpoint.json      │
    └──────────┬───────────┘
               │
               ├──────────────────────┐
               │                      │
               ▼                      ▼
    ┌──────────────────┐   ┌──────────────────────┐
    │ Q2BDataVisualizer│   │ SimilarityAnalyzer   │
    │ (Static Charts)  │   │ (Plagiarism)         │
    └──────────────────┘   └──────────┬───────────┘
                                      │
                                      ▼
                           ┌──────────────────────┐
                           │ similarity_*.json    │
                           │ duplicate_clusters   │
                           └──────────────────────┘
                                      │
                                      ▼
                           ┌──────────────────────┐
                           │ Dashboard (Streamlit)│
                           │ (Interactive View)   │
                           └──────────────────────┘
```

## Design Principles

### 1. Modularity
Each module has a single, clear responsibility:
- Scraping ≠ Visualization ≠ Analysis
- Can be used independently or in pipeline

### 2. Reproducibility
- Timestamped output directories
- Checkpoint system for resumption
- Version-controlled dependencies
- Configurable parameters via CLI

### 3. Ethical Scraping
- Rate limiting built-in
- Respects robots.txt
- User-Agent identification
- Exponential backoff

### 4. Data Integrity
- URL validation
- Article data validation
- Duplicate detection
- Error tracking

### 5. User Experience
- Clear CLI interface
- Progress reporting
- Helpful error messages
- Multiple entry points (CLI, interactive, dashboard)

## Extension Points

### Adding a New Visualization

1. Add method to `Q2BDataVisualizer`:
```python
def plot_new_chart(self, report, output_dir, colors):
    # Your plotting code
    plt.savefig(os.path.join(output_dir, "4_new_chart.png"))
```

2. Call in `create_visualizations()`:
```python
self.plot_new_chart(report, graphs_dir, colors)
```

### Adding a New Analysis Type

1. Create new module (e.g., `content_classifier.py`):
```python
class ContentClassifier:
    def __init__(self, input_dir):
        self.input_dir = input_dir
    
    def classify(self):
        # Your analysis logic
        pass
```

2. Integrate in `run.py`:
```python
from content_classifier import ContentClassifier

def run_classification(auditor):
    classifier = ContentClassifier(auditor.output_dir)
    classifier.classify()
```

### Adding a New Dashboard Tab

1. In `dashboard.py`, add new section:
```python
st.header("New Analysis")
# Your Streamlit components
```

### Adapting for Different Websites

1. Subclass `Q2BStudioAuditor`:
```python
class GenericAuditor(Q2BStudioAuditor):
    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url
    
    def scrape_page(self, page_num):
        # Site-specific scraping logic
        pass
```

## Performance Characteristics

| Operation | Time Complexity | Space Complexity | Notes |
|-----------|----------------|------------------|-------|
| Scraping | O(n) | O(n) | n = number of pages |
| Exact clustering | O(n) | O(n) | n = number of articles |
| Pairwise similarity | O(n²) | O(n²) | Limited to 10k articles |
| Visualization | O(n) | O(1) | For matplotlib charts |
| Dashboard | O(n) | O(n) | Interactive filtering |

## Dependencies Graph

```
run.py
├── q2b_studio_auditor.py
│   ├── requests
│   ├── beautifulsoup4
│   └── (standard library)
├── q2b_data_visualizer.py
│   └── matplotlib
├── wayback_archiver.py
│   └── requests
└── similarity_analyzer.py
    └── (standard library)

dashboard.py
├── streamlit
├── plotly
├── pandas
└── (standard library)
```

## Testing Strategy

Current approach (no automated tests yet):
- Manual validation on sample data
- Import verification
- CLI help text validation
- End-to-end pipeline testing

Future testing infrastructure:
- Unit tests for core functions
- Integration tests for pipeline
- Performance benchmarks
- Regression tests

## Deployment Options

### Local Development
```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
python run.py --sample 100
```

### Production Server
```bash
# Setup
pip install q2bs-auditor

# Automated daily runs
crontab -e
# Add: 0 2 * * * q2bs-audit --resume --sample 50 --archive 100

# Dashboard server
q2bs-dashboard --server.port 8501 --server.headless true
```

### Docker (Future)
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "run.py", "--sample", "100"]
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Code style guidelines
- Pull request process
- Feature request templates
- Bug report guidelines

## Support

- **Documentation**: Start with [README.md](README.md)
- **Examples**: See [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md)
- **Quick Start**: See [QUICK_START.md](QUICK_START.md)
- **Issues**: https://github.com/innermost47/q2bs/issues
- **Case Study**: https://dev.to/innermost_47/when-ai-content-systems-reproduce-content-without-attribution-a-documented-case-study-1h0g

---

Last updated: 2025-12-10
Version: 1.0.0
