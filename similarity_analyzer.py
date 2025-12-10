#!/usr/bin/env python3
"""
Similarity Analysis Module for Q2BSTUDIO Auditor

Detects duplicate and similar content using:
- N-gram similarity analysis
- Title clustering
- Pattern detection for plagiarism forensics

This module enables automated detection of industrialized content duplication.
"""

import json
import csv
import os
from collections import defaultdict
from typing import List, Dict, Tuple, Set
import re


class SimilarityAnalyzer:
    """Analyzes article titles for similarity and duplication patterns."""

    def __init__(self, input_dir: str, similarity_threshold: float = 0.85):
        """
        Initialize the similarity analyzer.

        Args:
            input_dir: Directory containing articles.csv
            similarity_threshold: Threshold for flagging duplicates (0.0-1.0)
        """
        self.input_dir = input_dir
        self.similarity_threshold = similarity_threshold
        self.articles = []
        self.duplicates = []
        self.clusters = []

    def load_articles(self) -> bool:
        """Load articles from CSV file."""
        csv_file = os.path.join(self.input_dir, "articles.csv")
        
        if not os.path.exists(csv_file):
            print(f"Error: {csv_file} not found")
            return False

        print(f"Loading articles from {csv_file}...")
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            self.articles = list(reader)

        print(f"Loaded {len(self.articles):,} articles for analysis")
        return True

    def normalize_text(self, text: str) -> str:
        """
        Normalize text for comparison.
        
        - Convert to lowercase
        - Remove special characters
        - Normalize whitespace
        """
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http[s]?://\S+', '', text)
        
        # Keep only alphanumeric and spaces
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        
        # Normalize whitespace
        text = ' '.join(text.split())
        
        return text

    def generate_ngrams(self, text: str, n: int = 3) -> Set[str]:
        """
        Generate character n-grams from text.
        
        Args:
            text: Input text
            n: N-gram size (default: 3)
            
        Returns:
            Set of n-grams
        """
        text = self.normalize_text(text)
        if len(text) < n:
            return {text}
        
        ngrams = set()
        for i in range(len(text) - n + 1):
            ngrams.add(text[i:i+n])
        
        return ngrams

    def calculate_jaccard_similarity(self, set1: Set[str], set2: Set[str]) -> float:
        """
        Calculate Jaccard similarity between two sets.
        
        Jaccard similarity = |A ∩ B| / |A ∪ B|
        
        Returns:
            Similarity score (0.0 to 1.0)
        """
        if not set1 or not set2:
            return 0.0
        
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        
        if union == 0:
            return 0.0
        
        return intersection / union

    def find_similar_pairs(self, ngram_size: int = 3) -> List[Dict]:
        """
        Find pairs of articles with similar titles.
        
        Args:
            ngram_size: Size of character n-grams to use
            
        Returns:
            List of similar article pairs with similarity scores
        """
        print(f"\nAnalyzing title similarity (n-gram size: {ngram_size})...")
        print(f"Threshold: {self.similarity_threshold}")
        
        similar_pairs = []
        
        # Generate n-grams for all articles
        article_ngrams = []
        for article in self.articles:
            title = article.get("title", "")
            ngrams = self.generate_ngrams(title, n=ngram_size)
            article_ngrams.append((article, ngrams))
        
        # Compare all pairs
        total_comparisons = len(article_ngrams) * (len(article_ngrams) - 1) // 2
        print(f"Performing {total_comparisons:,} pairwise comparisons...")
        
        compared = 0
        for i in range(len(article_ngrams)):
            for j in range(i + 1, len(article_ngrams)):
                article1, ngrams1 = article_ngrams[i]
                article2, ngrams2 = article_ngrams[j]
                
                similarity = self.calculate_jaccard_similarity(ngrams1, ngrams2)
                
                if similarity >= self.similarity_threshold:
                    similar_pairs.append({
                        "article1": {
                            "title": article1.get("title", ""),
                            "url": article1.get("url", ""),
                            "date": article1.get("date_parsed", ""),
                        },
                        "article2": {
                            "title": article2.get("title", ""),
                            "url": article2.get("url", ""),
                            "date": article2.get("date_parsed", ""),
                        },
                        "similarity": round(similarity, 4),
                    })
                
                compared += 1
                if compared % 100000 == 0:
                    print(f"  Progress: {compared:,}/{total_comparisons:,} comparisons")
        
        self.duplicates = similar_pairs
        print(f"\nFound {len(similar_pairs):,} similar pairs (>= {self.similarity_threshold})")
        
        return similar_pairs

    def cluster_by_exact_match(self) -> List[List[Dict]]:
        """
        Cluster articles with identical normalized titles.
        
        Returns:
            List of clusters (each cluster is a list of articles)
        """
        print("\nClustering by exact title match...")
        
        # Group by normalized title
        title_groups = defaultdict(list)
        for article in self.articles:
            title = article.get("title", "")
            normalized = self.normalize_text(title)
            if normalized:
                title_groups[normalized].append(article)
        
        # Keep only clusters with 2+ articles
        clusters = [
            articles for articles in title_groups.values()
            if len(articles) >= 2
        ]
        
        # Sort by cluster size (largest first)
        clusters.sort(key=len, reverse=True)
        
        self.clusters = clusters
        
        total_duplicates = sum(len(cluster) for cluster in clusters)
        print(f"Found {len(clusters):,} clusters with {total_duplicates:,} total articles")
        
        if clusters:
            print(f"Largest cluster: {len(clusters[0])} articles with same title")
        
        return clusters

    def generate_report(self) -> Dict:
        """
        Generate comprehensive similarity analysis report.
        
        Returns:
            Dictionary containing all analysis results
        """
        print("\nGenerating similarity analysis report...")
        
        # Calculate statistics
        total_articles = len(self.articles)
        num_similar_pairs = len(self.duplicates)
        num_clusters = len(self.clusters)
        
        articles_in_clusters = sum(len(cluster) for cluster in self.clusters)
        unique_articles = total_articles - articles_in_clusters + num_clusters
        
        duplication_rate = (
            (articles_in_clusters / total_articles * 100) 
            if total_articles > 0 else 0
        )
        
        from datetime import datetime
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "input_directory": self.input_dir,
            "similarity_threshold": self.similarity_threshold,
            "total_articles_analyzed": total_articles,
            "exact_match_clusters": {
                "num_clusters": num_clusters,
                "total_articles_in_clusters": articles_in_clusters,
                "duplication_rate": f"{duplication_rate:.2f}%",
                "largest_cluster_size": len(self.clusters[0]) if self.clusters else 0,
            },
            "similar_pairs": {
                "num_pairs": num_similar_pairs,
                "threshold": self.similarity_threshold,
            },
            "uniqueness_analysis": {
                "truly_unique_articles": unique_articles,
                "uniqueness_rate": f"{(unique_articles / total_articles * 100):.2f}%" if total_articles > 0 else "0%",
            },
        }
        
        return report

    def save_results(self) -> None:
        """Save similarity analysis results to files."""
        print("\nSaving similarity analysis results...")
        
        # Save main report
        report = self.generate_report()
        report_file = os.path.join(self.input_dir, "similarity_report.json")
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"✓ Saved: {report_file}")
        
        # Save duplicate pairs
        if self.duplicates:
            duplicates_file = os.path.join(self.input_dir, "similar_pairs.json")
            with open(duplicates_file, "w", encoding="utf-8") as f:
                json.dump(self.duplicates, f, indent=2, ensure_ascii=False)
            print(f"✓ Saved: {duplicates_file} ({len(self.duplicates):,} pairs)")
        
        # Save clusters
        if self.clusters:
            clusters_file = os.path.join(self.input_dir, "duplicate_clusters.json")
            clusters_data = [
                {
                    "cluster_id": idx + 1,
                    "size": len(cluster),
                    "normalized_title": self.normalize_text(cluster[0].get("title", "")),
                    "articles": [
                        {
                            "title": article.get("title", ""),
                            "url": article.get("url", ""),
                            "date": article.get("date_parsed", ""),
                        }
                        for article in cluster
                    ],
                }
                for idx, cluster in enumerate(self.clusters[:100])  # Top 100 clusters
            ]
            
            with open(clusters_file, "w", encoding="utf-8") as f:
                json.dump(clusters_data, f, indent=2, ensure_ascii=False)
            print(f"✓ Saved: {clusters_file} (top 100 clusters)")
        
        # Save summary CSV
        summary_file = os.path.join(self.input_dir, "similarity_summary.csv")
        with open(summary_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Metric", "Value"])
            writer.writerow(["Total Articles", report["total_articles_analyzed"]])
            writer.writerow(["Exact Match Clusters", report["exact_match_clusters"]["num_clusters"]])
            writer.writerow(["Articles in Clusters", report["exact_match_clusters"]["total_articles_in_clusters"]])
            writer.writerow(["Duplication Rate", report["exact_match_clusters"]["duplication_rate"]])
            writer.writerow(["Similar Pairs (>={})".format(self.similarity_threshold), report["similar_pairs"]["num_pairs"]])
            writer.writerow(["Truly Unique Articles", report["uniqueness_analysis"]["truly_unique_articles"]])
            writer.writerow(["Uniqueness Rate", report["uniqueness_analysis"]["uniqueness_rate"]])
        print(f"✓ Saved: {summary_file}")

    def analyze(self) -> Dict:
        """
        Run complete similarity analysis pipeline.
        
        Returns:
            Analysis report dictionary
        """
        if not self.load_articles():
            return {}
        
        # Exact match clustering
        self.cluster_by_exact_match()
        
        # Similar pairs detection (only for reasonable dataset sizes)
        # Pairwise comparison is O(n²), so we limit by default to prevent memory issues
        # For larger datasets, consider sampling or using approximate algorithms
        max_articles_for_pairwise = 10000  # Configurable threshold
        
        if len(self.articles) <= max_articles_for_pairwise:
            self.find_similar_pairs(ngram_size=3)
        else:
            print(f"\nSkipping pairwise similarity (dataset too large: {len(self.articles):,} articles)")
            print(f"Pairwise similarity is O(n²) - limited to {max_articles_for_pairwise:,} articles")
            print("Consider sampling for large datasets or use exact match clustering only")
        
        # Generate and save results
        self.save_results()
        
        return self.generate_report()


def main():
    """CLI entry point for standalone similarity analysis."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Analyze article similarity for plagiarism detection"
    )
    parser.add_argument(
        "input_dir",
        help="Directory containing articles.csv"
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.85,
        help="Similarity threshold for flagging duplicates (0.0-1.0, default: 0.85)"
    )
    
    args = parser.parse_args()
    
    analyzer = SimilarityAnalyzer(args.input_dir, similarity_threshold=args.threshold)
    report = analyzer.analyze()
    
    if report:
        print("\n" + "=" * 60)
        print("SIMILARITY ANALYSIS COMPLETE")
        print("=" * 60)
        print(f"Total articles: {report['total_articles_analyzed']:,}")
        print(f"Exact match clusters: {report['exact_match_clusters']['num_clusters']:,}")
        print(f"Duplication rate: {report['exact_match_clusters']['duplication_rate']}")
        print(f"Uniqueness rate: {report['uniqueness_analysis']['uniqueness_rate']}")
        print(f"\nResults saved in: {args.input_dir}")


if __name__ == "__main__":
    main()
