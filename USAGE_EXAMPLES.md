# Q2BS Auditor - Usage Examples

Comprehensive examples for using the Q2BS Auditor toolkit.

## Quick Start

### 1. Fresh Scraping Run

Scrape from scratch and generate all reports:

```bash
python run.py
```

This will:
- Auto-detect maximum page number from the site
- Create a timestamped output directory
- Scrape all pages systematically
- Generate statistical reports
- Create visualizations
- Save checkpoints every 100 pages

### 2. Resume from Checkpoint

If your scraping was interrupted:

```bash
python run.py --resume
```

This will:
- Find the latest `q2b_audit_*` directory
- Load existing data
- Calculate which page to resume from
- Continue scraping without duplicates

### 3. Visualization Only

Regenerate reports and graphs without scraping:

```bash
python run.py --visualize-only
```

Use this when:
- You want updated graphs with new styling
- You've manually cleaned the CSV data
- You want to analyze a specific time period

## Sampling Strategies

### Sample 10% for Trend Analysis

```bash
python run.py --sample 10
```

This scrapes every 10th page, giving you 10% of data while capturing overall trends.

**When to use:**
- Quick trend analysis
- Testing data pipelines
- Resource-constrained environments

### Sample 1% for Testing

```bash
python run.py --sample 100
```

Scrapes every 100th page - useful for:
- Development and testing
- Validating scraping logic
- Quick smoke tests

## Archiving to Wayback Machine

### Archive 500 Random Articles

```bash
python run.py --archive 500
```

This will:
- Complete the scraping and analysis
- Select 500 random articles
- Submit each to Wayback Machine
- Save archive URLs for verification

### Combined: Resume and Archive

```bash
python run.py --resume --archive 1000
```

Resume scraping and archive 1,000 articles when complete.

## Similarity Analysis

### Basic Plagiarism Detection

After scraping, run similarity analysis:

```bash
python similarity_analyzer.py q2b_audit_20251210_120000
```

This generates:
- `similarity_report.json` - Overall statistics
- `similar_pairs.json` - High-similarity article pairs
- `duplicate_clusters.json` - Exact match groups
- `similarity_summary.csv` - Quick metrics

### Custom Similarity Threshold

For stricter duplicate detection (90% similarity):

```bash
python similarity_analyzer.py q2b_audit_20251210_120000 --threshold 0.90
```

For looser detection (75% similarity):

```bash
python similarity_analyzer.py q2b_audit_20251210_120000 --threshold 0.75
```

## Interactive Dashboard

### Launch Web Dashboard

```bash
streamlit run dashboard.py
```

Then open your browser to `http://localhost:8501`

The dashboard provides:
- Real-time metrics and KPIs
- Interactive date filtering
- Plotly-based charts (zoom, pan, export)
- Search functionality
- Checkpoint selection

### Dashboard Features

1. **Metrics Panel**: Total articles, avg per day, peak day, frequency
2. **Date Filter**: Explore specific time ranges
3. **Visualizations**:
   - Daily article production (bar chart)
   - Publication timeline (line graph)
   - Distribution histogram
   - Day-of-week analysis
   - Monthly trends
4. **Data Table**: Search and browse articles
5. **Checkpoint Switcher**: Compare different scraping runs

## Advanced Workflows

### Complete Forensic Investigation

```bash
# 1. Initial scraping with sampling
python run.py --sample 10 --archive 500

# 2. Similarity analysis
python similarity_analyzer.py q2b_audit_20251210_120000

# 3. Launch dashboard for exploration
streamlit run dashboard.py
```

### Resume After Crash

```bash
# Scraping crashed at page 15,000
# Just resume:
python run.py --resume

# The system automatically:
# - Loads existing 15,000 pages of data
# - Calculates resume page
# - Continues from page 15,001
```

### Production Pipeline (Automation)

For automated daily monitoring:

```bash
#!/bin/bash
# daily_audit.sh

# Resume if checkpoint exists, otherwise start fresh
python run.py --resume --sample 100 --archive 100

# Run similarity analysis on latest
LATEST=$(ls -td q2b_audit_* | head -1)
python similarity_analyzer.py "$LATEST"

# Optional: start dashboard on server
# streamlit run dashboard.py --server.port 8501 --server.headless true
```

## Data Analysis Examples

### Using Python/Pandas

```python
import pandas as pd

# Load articles
df = pd.read_csv('q2b_audit_20251210_120000/articles.csv')

# Basic stats
print(f"Total articles: {len(df):,}")
print(f"Date range: {df['date_parsed'].min()} to {df['date_parsed'].max()}")

# Articles per day
daily = df.groupby('date_parsed').size()
print(f"Average per day: {daily.mean():.0f}")
print(f"Peak day: {daily.max()} articles")

# Search for keywords
ai_articles = df[df['title'].str.contains('AI', case=False, na=False)]
print(f"Articles mentioning 'AI': {len(ai_articles)}")

# Most common page numbers (detect patterns)
page_dist = df['page_num'].value_counts().head(10)
print("Most common pages:", page_dist)
```

### Using CLI Tools

```bash
# Count total articles
wc -l q2b_audit_*/articles.csv

# Search for specific terms
grep -i "neural network" q2b_audit_*/articles.csv

# Extract unique dates
cut -d',' -f4 q2b_audit_*/articles.csv | sort -u | wc -l

# Articles per day
cut -d',' -f4 q2b_audit_*/articles.csv | sort | uniq -c
```

## Troubleshooting

### "No checkpoint directories found"

```bash
# Error when using --resume but no checkpoints exist
# Solution: Run without --resume to start fresh
python run.py
```

### "Could not determine max page from site"

```bash
# The website might be down or blocking requests
# Solution: Check the site manually or try later
curl https://www.q2bstudio.com/blog-empresa-aplicaciones
```

### Similarity analysis taking too long

```bash
# For large datasets (>10,000 articles), pairwise comparison is O(n²)
# Solution: Use exact match clustering only (automatic for large datasets)
# Or sample the data first
```

### Dashboard not loading data

```bash
# Ensure you're in the correct directory
cd /path/to/q2bs
streamlit run dashboard.py

# Dashboard looks for q2b_audit_* directories in current directory
```

## Performance Tips

### Faster Scraping

- Use `--sample` for initial testing
- Run on a machine with good internet connection
- Consider parallel runs on different page ranges (manual split)

### Efficient Analysis

- Similarity analysis: Skip for datasets >10,000 articles (use clustering only)
- Dashboard: Use date filters to focus on specific periods
- CSV files: Use pandas chunking for files >1GB

### Storage Management

```bash
# Checkpoint directories can grow large
# Keep only recent checkpoints:
ls -td q2b_audit_* | tail -n +6 | xargs rm -rf

# Or compress old ones:
tar -czf archives/q2b_audit_20251201.tar.gz q2b_audit_20251201_*
```

## Integration Examples

### With Jupyter Notebooks

```python
# analysis.ipynb
import sys
sys.path.append('/path/to/q2bs')

from q2b_studio_auditor import Q2BStudioAuditor
from similarity_analyzer import SimilarityAnalyzer

# Load existing checkpoint
auditor = Q2BStudioAuditor(create_output_dir=False)
auditor.load_checkpoint('q2b_audit_20251210_120000')

# Generate fresh report
report = auditor.generate_report()
print(f"Total articles: {report['total_articles']:,}")

# Run similarity analysis
analyzer = SimilarityAnalyzer('q2b_audit_20251210_120000', threshold=0.85)
similarity_report = analyzer.analyze()
```

### With cron for Monitoring

```bash
# Add to crontab (daily at 2 AM)
0 2 * * * cd /path/to/q2bs && python run.py --resume --sample 50 --archive 100 >> logs/daily_audit.log 2>&1
```

### API Integration (Future)

```python
# Example future API usage
from q2bs_auditor import Auditor

auditor = Auditor(target_url="https://example.com/blog")
auditor.scrape(sample_rate=0.1)
report = auditor.generate_report()
auditor.export_to_s3("s3://bucket/reports/")
```

## Hydra-Powered Visualization

### Basic Hydra Visualization

Generate visualizations with Hydra configuration management:

```bash
# Default configuration
python visualize_with_hydra.py checkpoint_dir=q2b_audit_20251210_120000
```

This provides the same visualizations as the standard pipeline but with full configuration control.

### Using Alternative Themes

```bash
# Dark color scheme
python visualize_with_hydra.py checkpoint_dir=q2b_audit_20251210_120000 visualization=dark
```

### Override Specific Parameters

```bash
# Change primary color
python visualize_with_hydra.py checkpoint_dir=q2b_audit_20251210_120000 'visualization.colors.primary="#FF0000"'

# High-resolution output for publications
python visualize_with_hydra.py checkpoint_dir=q2b_audit_20251210_120000 output.dpi=600

# Change chart dimensions
python visualize_with_hydra.py checkpoint_dir=q2b_audit_20251210_120000 visualization.dimensions.daily_articles.width=20

# Multiple overrides
python visualize_with_hydra.py checkpoint_dir=q2b_audit_20251210_120000 visualization=dark output.dpi=150 'visualization.colors.average_line="#00FF00"'
```

### Create Custom Color Scheme

Create a new file `config/visualization/custom.yaml`:

```yaml
# @package visualization
# Custom color scheme

defaults:
  - default

colors:
  primary: "#8B0000"      # Dark red
  secondary: "#006400"    # Dark green
  tertiary: "#00008B"     # Dark blue
  quaternary: "#8B4513"   # Saddle brown
  quinary: "#2F4F4F"      # Dark slate gray
  partial_day: "#A9A9A9"  # Dark gray
  average_line: "#FFD700" # Gold
```

Then use it:

```bash
python visualize_with_hydra.py checkpoint_dir=q2b_audit_20251210_120000 visualization=custom
```

### Configuration for Different Outputs

```bash
# For presentations (lower DPI, larger fonts)
python visualize_with_hydra.py checkpoint_dir=q2b_audit_20251210_120000 \
  output.dpi=150 \
  visualization.fonts.title=18 \
  visualization.fonts.xlabel=16

# For print publications (high DPI)
python visualize_with_hydra.py checkpoint_dir=q2b_audit_20251210_120000 \
  output.dpi=600 \
  visualization.chart_settings.line_width=2

# For social media (specific dimensions)
python visualize_with_hydra.py checkpoint_dir=q2b_audit_20251210_120000 \
  visualization.dimensions.daily_articles.width=10 \
  visualization.dimensions.daily_articles.height=10
```

### Hydra Benefits

1. **Reproducibility**: Configuration files version-controlled with code
2. **No Code Changes**: Adjust visualizations without modifying Python files
3. **Multiple Versions**: Generate different styles for different audiences
4. **Command-line Control**: Override any parameter on the fly
5. **Experiment Tracking**: Hydra automatically saves configurations in `outputs/` directory

### Advanced: Multiple Comparisons

Modify `config/visualization/default.yaml` to add more comparison sources:

```yaml
stats_summary:
  comparison_sources:
    - name: TechCrunch
      articles_per_day: 40
    - name: The Verge
      articles_per_day: 30
    - name: NY Times
      articles_per_day: 250
    - name: Medium (top authors)
      articles_per_day: 100
    - name: WordPress.com
      articles_per_day: 500
```

## Best Practices

1. **Always use sampling for testing** - Don't scrape 36,000 pages during development
2. **Archive important findings** - Use Wayback Machine to preserve evidence
3. **Version your checkpoints** - Keep important scraping runs for historical comparison
4. **Document your methodology** - Note sampling rates and dates in your reports
5. **Respect rate limits** - The default 0.5s delay is ethical and sufficient
6. **Monitor disk space** - Large scrapes can produce multi-GB CSV files
7. **Run similarity analysis offline** - Do it after scraping completes
8. **Use the dashboard for exploration** - It's faster than writing custom pandas scripts
9. **Use Hydra for visualization variants** - Generate multiple styles without code changes
10. **Keep config files in version control** - Track visualization settings with your code

## Support and Resources

- **GitHub Issues**: https://github.com/innermost47/q2bs/issues
- **Case Study**: https://dev.to/innermost_47/when-ai-content-systems-reproduce-content-without-attribution-a-documented-case-study-1h0g
- **Author**: Anthony CHARRETIER (https://anthony-charretier.fr)

## Next Steps

After mastering these examples:
1. Explore the source code to understand implementation details
2. Contribute improvements or adaptations for other sites
3. Publish your findings (with proper methodology documentation)
4. Consider extending the tool for your specific research needs
