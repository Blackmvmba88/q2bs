# Q2BS Auditor - Quick Start Guide

Get up and running in 5 minutes.

## Installation

```bash
# Clone repository
git clone https://github.com/innermost47/q2bs.git
cd q2bs

# Create virtual environment
python -m venv env
source env/bin/activate  # On macOS/Linux
# or: env\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

## Basic Usage

### 1. Run a Quick Test (Sample 1% of Data)

```bash
python run.py --sample 100
```

This will:
- Scrape every 100th page (1% sample)
- Complete in ~10 minutes
- Generate all reports and visualizations
- Create a `q2b_audit_YYYYMMDD_HHMMSS/` directory

### 2. View Results in Dashboard

```bash
streamlit run dashboard.py
```

Open browser to `http://localhost:8501` to explore data interactively.

### 3. Analyze for Plagiarism

```bash
python similarity_analyzer.py q2b_audit_YYYYMMDD_HHMMSS
```

View results in:
- `q2b_audit_*/similarity_report.json`
- `q2b_audit_*/duplicate_clusters.json`

## Common Commands

```bash
# Fresh scraping run (full dataset - takes hours!)
python run.py

# Resume from checkpoint
python run.py --resume

# Only regenerate visualizations
python run.py --visualize-only

# Sample 10% and archive 500 articles
python run.py --sample 10 --archive 500

# View help
python run.py --help
```

## Understanding Output

After running, you'll have a timestamped directory:

```
q2b_audit_20251210_120000/
├── articles.csv          # Complete dataset
├── report.json           # Statistics
├── graphs/               # PNG visualizations
└── similarity_*.json     # Plagiarism analysis (if run)
```

## Next Steps

- Read [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) for advanced usage
- Read [README.md](README.md) for complete documentation
- Launch `streamlit run dashboard.py` for interactive exploration

## Troubleshooting

**"ModuleNotFoundError"**: Install dependencies with `pip install -r requirements.txt`

**"No checkpoint directories found"**: Run `python run.py` first (without --resume)

**Takes too long**: Use `--sample 100` for faster testing (1% sample)

## Support

- GitHub Issues: https://github.com/innermost47/q2bs/issues
- Case Study: https://dev.to/innermost_47/when-ai-content-systems-reproduce-content-without-attribution-a-documented-case-study-1h0g

---

**Ready to start? Run:** `python run.py --sample 100`
