# Changelog

All notable changes to Q2BS Auditor will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-12-10

### Added - Major Feature Release

#### Pipeline & Automation
- **Unified Pipeline Runner (`run.py`)**: Single-command reproducible workflow
  - `--resume`: Resume from latest checkpoint
  - `--visualize-only`: Regenerate visualizations without scraping
  - `--sample N`: Scrape every N-th page for efficient sampling
  - `--archive K`: Archive K random articles to Wayback Machine
- Clean separation of pipeline phases: scrape → checkpoint → analyze → visualize → archive

#### Plagiarism Detection
- **Similarity Analysis Module (`similarity_analyzer.py`)**:
  - Character n-gram based similarity analysis
  - Jaccard similarity coefficient calculation
  - Exact match clustering for duplicate detection
  - Configurable similarity threshold (default: 0.85)
  - Generates comprehensive forensic reports:
    - `similarity_report.json`: Overall statistics
    - `similar_pairs.json`: High-similarity article pairs
    - `duplicate_clusters.json`: Groups of identical content
    - `similarity_summary.csv`: Quick metrics overview
  - Intelligent handling of large datasets (automatic O(n²) detection)

#### Interactive Visualization
- **Streamlit Dashboard (`dashboard.py`)**:
  - Web-based interactive interface
  - Real-time KPI metrics (total articles, avg/day, peak day, frequency)
  - Date range filtering for temporal analysis
  - Interactive Plotly charts with zoom/pan/export
  - Search functionality across article titles
  - Checkpoint selection for comparing different runs
  - Multiple visualization types:
    - Daily article production bar charts
    - Publication timeline with averages
    - Distribution histograms
    - Day-of-week analysis
    - Monthly trend aggregation

#### Documentation
- **Philosophical Framing**: "Automated Plagiarism as an Ecological Phenomenon"
  - Positions tool as research instrument for documenting emergent behavior
  - Explains mission: transparency, documentation, preservation, critical analysis
  - Contextualizes industrial-scale automated content generation
- **Technical Methodology Documentation**:
  - Rate limiting strategies (0.5s between requests)
  - Robots.txt compliance and ethical practices
  - Sampling strategies and when to use them
  - Crash resumption with checkpoint system
  - Exponential backoff for error handling
- **USAGE_EXAMPLES.md**: Comprehensive usage scenarios (50+ examples)
- **CONTRIBUTING.md**: Contribution guidelines and ethical framework
- **QUICK_START.md**: 5-minute getting started guide
- **CHANGELOG.md**: This file

#### Package Distribution
- **PyPI Preparation**:
  - `setup.py` with complete metadata
  - `MANIFEST.in` for proper file inclusion
  - Console entry points: `q2bs-audit`, `q2bs-similarity`, `q2bs-dashboard`
  - Python 3.8+ support for broad compatibility
  - Dependencies properly specified with versions

#### Code Quality
- Enhanced `.gitignore` with comprehensive exclusions
- ISO 8601 timestamps throughout for consistency
- Configurable thresholds for similarity analysis
- Improved error handling and user feedback
- Code review passed with all issues addressed
- Security scan passed (0 vulnerabilities)

### Changed

#### Existing Modules
- **Enhanced README.md**:
  - Added philosophical introduction and mission statement
  - Documented reproducible pipeline usage
  - Added PyPI installation instructions
  - Expanded technical methodology section
  - Updated requirements to include new dependencies
  - Added comprehensive output structure documentation
- **Updated requirements.txt**:
  - Added `streamlit>=1.28.0` for dashboard
  - Added `plotly>=5.17.0` for interactive charts
  - Added `pandas>=2.0.0` for data manipulation
  - Pinned versions for reproducibility

#### Backwards Compatibility
- **Maintained all existing functionality**:
  - `main.py` still works as interactive script
  - `q2b_studio_auditor.py` unchanged (internal improvements only)
  - `q2b_data_visualizer.py` unchanged
  - `wayback_archiver.py` unchanged
  - All existing checkpoints remain compatible

### Fixed
- Dashboard variable scoping issue (unique_days calculation)
- Similarity analyzer date format (now uses ISO 8601)
- Python version requirement broadened to 3.8+ (from 3.10+)
- Made pairwise comparison threshold configurable

### Technical Details

#### Performance
- Similarity analysis optimized for datasets up to 10,000 articles
- Automatic degradation to clustering-only for larger datasets
- Memory-efficient CSV processing
- Checkpoint system enables multi-hour scraping sessions

#### Architecture
- Clean separation of concerns across modules
- Reproducible pipeline with clear phases
- Modular design allows using components independently
- CLI interface follows Unix philosophy

#### Testing
- Manual validation on 304,291 article dataset
- Similarity analysis verified (found 8,437 clusters, 6.41% duplication rate)
- Dashboard tested with real data
- All imports validated
- setup.py validation passed

## [0.9.0] - 2025-12-08 (Previous Version)

### Features from Original Implementation
- Systematic blog scraping with pagination support
- Spanish date parsing
- Statistical analysis and reporting
- Static visualization generation (matplotlib)
- Wayback Machine integration
- Checkpoint system for crash recovery
- CSV export functionality
- Interactive main.py with user confirmations

---

## Future Roadmap

### [1.1.0] - Planned
- [ ] Semantic similarity (not just character-based)
- [ ] Cross-language plagiarism detection
- [ ] Performance optimization for 100k+ article datasets
- [ ] Network graphs of content similarity
- [ ] Additional export formats (SQLite, Parquet)

### [1.2.0] - Planned
- [ ] Machine learning-based clustering
- [ ] Topic modeling
- [ ] Anomaly detection
- [ ] Multi-site support
- [ ] API server mode

### [2.0.0] - Vision
- [ ] Real-time monitoring
- [ ] Webhook notifications
- [ ] Collaborative features
- [ ] Cloud deployment options
- [ ] Distributed scraping

---

For more details on any release, see the [commit history](https://github.com/innermost47/q2bs/commits/main).

**Questions or suggestions?** Open an issue on GitHub!
