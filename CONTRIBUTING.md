# Contributing to Q2BS Auditor

Thank you for your interest in contributing to Q2BS Auditor! This document provides guidelines for contributing to this forensic investigation tool.

## Code of Conduct

This project is dedicated to documenting and analyzing industrial-scale automated content generation in a **responsible and ethical manner**. All contributors must:

- Use the tool for research, documentation, and transparency purposes only
- Respect rate limits and server resources
- Follow ethical web scraping practices
- Contribute to making the tool more accurate, efficient, and useful
- Be respectful to other contributors and users

## Ways to Contribute

### 1. Bug Reports

If you find a bug, please open an issue with:
- **Clear title**: Describe the bug in one sentence
- **Steps to reproduce**: Exact commands and configuration
- **Expected vs actual behavior**
- **Environment**: OS, Python version, dependency versions
- **Logs**: Error messages or stack traces

Example:
```
Title: Similarity analyzer crashes on datasets >50,000 articles

Steps:
1. Scrape 50,000+ articles
2. Run: python similarity_analyzer.py q2b_audit_20251210_120000
3. Process crashes after ~1 hour

Expected: Complete analysis
Actual: MemoryError after 100M comparisons

Environment: Ubuntu 22.04, Python 3.11, 16GB RAM
```

### 2. Feature Requests

We welcome suggestions for improvements! Please include:
- **Use case**: Why is this feature needed?
- **Proposed solution**: How would it work?
- **Alternatives**: Have you considered other approaches?
- **Impact**: Who would benefit from this?

Priority areas:
- Multi-language content similarity detection
- Performance optimizations for large datasets
- Additional visualization types
- Machine learning-based clustering
- Export to additional formats (SQLite, Parquet, etc.)

### 3. Code Contributions

#### Getting Started

1. **Fork the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/q2bs.git
   cd q2bs
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv env
   source env/bin/activate  # On macOS/Linux
   pip install -r requirements.txt
   ```

3. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make your changes**
   - Follow the existing code style
   - Add docstrings to new functions
   - Update README.md if adding user-facing features
   - Test your changes thoroughly

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add feature: brief description"
   ```

6. **Push and create a pull request**
   ```bash
   git push origin feature/your-feature-name
   ```

#### Code Style Guidelines

- **PEP 8 compliance**: Follow Python's official style guide
- **Type hints**: Use type annotations for function parameters and returns
- **Docstrings**: Use Google-style docstrings
- **Comments**: Explain "why", not "what"
- **Variable names**: Descriptive names (e.g., `articles_per_day` not `apd`)

Example:

```python
def calculate_similarity(text1: str, text2: str, ngram_size: int = 3) -> float:
    """Calculate Jaccard similarity between two texts using n-grams.
    
    Args:
        text1: First text to compare
        text2: Second text to compare
        ngram_size: Size of character n-grams (default: 3)
        
    Returns:
        Similarity score between 0.0 and 1.0
        
    Examples:
        >>> calculate_similarity("hello world", "hello earth")
        0.625
    """
    # Implementation...
```

#### Testing

While we don't have a comprehensive test suite yet, please:
- Manually test your changes thoroughly
- Test with various dataset sizes
- Test edge cases (empty data, malformed inputs, etc.)
- Verify backwards compatibility

#### Pull Request Process

1. **Update documentation**: README, USAGE_EXAMPLES, docstrings
2. **Self-review**: Check your own code for issues
3. **Keep it focused**: One feature/fix per PR
4. **Describe your changes**: 
   - What problem does this solve?
   - How does it work?
   - Any breaking changes?
5. **Be responsive**: Address review feedback promptly

### 4. Documentation

Documentation improvements are highly valued! You can:
- Fix typos or clarify existing docs
- Add usage examples
- Improve API documentation
- Translate documentation (especially for Spanish content analysis)
- Create tutorials or guides

### 5. Testing and Validation

Help validate the tool:
- Test on different websites (with permission)
- Verify results against manual counts
- Test on different operating systems
- Test with various Python versions

## Development Priorities

### High Priority

1. **Performance optimization** for large datasets
   - Similarity analysis for 100k+ articles
   - Memory-efficient CSV processing
   - Parallel processing support

2. **Enhanced plagiarism detection**
   - Semantic similarity (not just character-based)
   - Cross-language plagiarism detection
   - Source attribution tracking

3. **Better error handling**
   - Graceful degradation
   - Clearer error messages
   - Recovery strategies

### Medium Priority

1. **Additional visualizations**
   - Network graphs of content similarity
   - Heatmaps of publication patterns
   - Time-series forecasting

2. **Export formats**
   - SQLite database export
   - Parquet for big data workflows
   - JSON-LD for linked data

3. **Configuration system**
   - YAML/TOML config files
   - Per-site configuration profiles
   - Custom rate limiting rules

### Future Ideas

1. **Machine learning integration**
   - Topic modeling
   - Content classification
   - Anomaly detection

2. **API server mode**
   - REST API for programmatic access
   - Webhook notifications
   - Real-time monitoring

3. **Multi-site support**
   - Unified framework for multiple targets
   - Cross-site similarity analysis
   - Comparative reporting

## Ethical Guidelines

### Do's ✅

- **Document methodology clearly** in your contributions
- **Respect robots.txt** and server resources
- **Use for research and transparency** purposes
- **Implement rate limiting** in any scraping code
- **Preserve evidence** through proper archiving
- **Share findings responsibly** with proper context

### Don'ts ❌

- **Don't overwhelm servers** with aggressive scraping
- **Don't use for malicious purposes** (DoS, unauthorized access)
- **Don't bypass security measures** or authentication
- **Don't scrape private/protected content**
- **Don't republish scraped content** without permission
- **Don't make false claims** about findings

## Recognition

Contributors will be:
- Acknowledged in commit messages
- Listed in future CONTRIBUTORS.md
- Credited in release notes for significant contributions
- Mentioned in academic citations where applicable

## Getting Help

- **Questions**: Open a GitHub Discussion
- **Bugs**: Open a GitHub Issue
- **Security**: Email contact@anthony-charretier.fr (not public issues)
- **General**: Comment on relevant issues or PRs

## Legal Compliance

By contributing, you agree that:
- Your contributions are your own original work
- Your contributions will be licensed under MIT License
- You've tested your code ethically and legally
- You haven't included any proprietary or sensitive data

## Resources

- **PEP 8**: https://pep8.org/
- **Google Python Style Guide**: https://google.github.io/styleguide/pyguide.html
- **Type Hints**: https://docs.python.org/3/library/typing.html
- **Ethical Web Scraping**: https://towardsdatascience.com/ethics-in-web-scraping-b96b18136f01

## Thank You!

Every contribution, no matter how small, helps make this tool better for researchers, journalists, and anyone interested in understanding industrial-scale automated content generation.

Your work contributes to **transparency, accountability, and understanding** in the digital content ecosystem.

---

**Happy Contributing!** 🚀

For questions or suggestions about these guidelines, please open an issue.
