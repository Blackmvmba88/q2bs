import time
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import json
import os
from collections import defaultdict
import locale
from urllib.parse import urlparse

try:
    locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")
except:
    try:
        locale.setlocale(locale.LC_TIME, "Spanish_Spain.1252")
    except:
        print("Warning: Could not set Spanish locale")


class Q2BStudioAuditor:
    def __init__(self, create_output_dir=True):
        self.base_url = "https://www.q2bstudio.com"
        self.blog_url = f"{self.base_url}/blog-empresa-aplicaciones"
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
                "Referer": "https://www.google.com/",
                "DNT": "1",
            }
        )
        self.articles = {}
        self.articles_by_date = defaultdict(list)
        self.validation_errors = 0

        if create_output_dir:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.output_dir = f"q2b_audit_{timestamp}"
            os.makedirs(self.output_dir, exist_ok=True)
            print(f"Output directory: {self.output_dir}")
        else:
            self.output_dir = None

    def validate_url(self, url):
        """Validate that a URL is properly formatted and belongs to the expected domain."""
        if not url or not isinstance(url, str):
            return False
        
        try:
            parsed = urlparse(url)
            # Check that URL has scheme and netloc
            if not parsed.scheme or not parsed.netloc:
                return False
            # Check that URL belongs to q2bstudio domain
            if "q2bstudio.com" not in parsed.netloc:
                return False
            return True
        except Exception:
            return False

    def validate_article_data(self, article_data):
        """Validate that article data contains all required fields and is properly formatted."""
        if not isinstance(article_data, dict):
            return False
        
        # Check required fields
        required_fields = ["url", "title", "date_raw", "date_parsed", "page_num"]
        for field in required_fields:
            if field not in article_data:
                return False
        
        # Validate URL
        if not self.validate_url(article_data["url"]):
            return False
        
        # Validate title is not empty
        if not article_data["title"] or article_data["title"] == "N/A":
            return False
        
        # Validate page number is positive
        if not isinstance(article_data["page_num"], int) or article_data["page_num"] < 1:
            return False
        
        return True

    def get_max_page_number(self):
        print("\nGetting maximum page number...")

        try:
            response = self.session.get(self.blog_url, timeout=15)
            soup = BeautifulSoup(response.content, "html.parser")

            pagination = soup.find("nav", {"aria-label": "Page navigation example"})
            if not pagination:
                print("Could not find pagination")
                return None

            page_links = pagination.find_all("a", class_="page-link")

            max_page = 1
            for link in page_links:
                href = link.get("href", "")
                if "/page/" in href:
                    try:
                        page_num = int(href.split("/page/")[-1])
                        if page_num > max_page:
                            max_page = page_num
                    except:
                        continue

            print(f"Maximum page number: {max_page:,}")
            return max_page

        except Exception as e:
            print(f"Error getting max page: {e}")
            return None

    def parse_spanish_date(self, date_str: str):
        """Parse Spanish-format date strings with improved validation."""
        if not date_str or date_str == "N/A":
            return "UNKNOWN_DATE"
        
        try:
            # Remove day of week if present (e.g., "lunes, 20 de enero de 2025")
            date_parts = date_str.split(",", 1)
            if len(date_parts) > 1:
                clean_date = date_parts[1].strip()
            else:
                clean_date = date_str.strip()
            
            # Validate the date format before parsing
            if "de" not in clean_date:
                return "UNKNOWN_DATE"
            
            date_obj = datetime.strptime(clean_date, "%d de %B de %Y")
            return date_obj.strftime("%Y-%m-%d")
        except ValueError as e:
            # Specific error for date parsing
            return "UNKNOWN_DATE"
        except Exception as e:
            # Catch any other unexpected errors
            return "UNKNOWN_DATE"

    def scrape_page(self, page_num):
        """Scrape a single page with improved validation."""
        url = f"{self.blog_url}/page/{page_num}" if page_num > 1 else self.blog_url
        articles_on_page = []

        try:
            response = self.session.get(url, timeout=15)
            soup = BeautifulSoup(response.content, "html.parser")
            article_items = soup.find_all("div", class_="item-new")

            for item in article_items:
                try:
                    link_elem = item.find("a", href=True)
                    if not link_elem:
                        continue

                    article_url = self.base_url + link_elem["href"]
                    
                    # Validate URL before proceeding
                    if not self.validate_url(article_url):
                        self.validation_errors += 1
                        continue
                    
                    title_elem = item.find("div", class_="title")
                    title = title_elem.get_text().strip() if title_elem else "N/A"
                    
                    tags_elem = item.find("div", class_="tags")
                    date_str = "N/A"
                    if tags_elem:
                        inner = tags_elem.find("div", class_="inner")
                        if inner:
                            text = inner.get_text().strip()
                            if "|" in text:
                                date_str = text.split("|")[1].strip()

                    parsed_date = self.parse_spanish_date(date_str)

                    article_data = {
                        "url": article_url,
                        "title": title,
                        "date_raw": date_str,
                        "date_parsed": parsed_date,
                        "page_num": page_num,
                    }

                    # Validate article data before adding
                    if self.validate_article_data(article_data):
                        articles_on_page.append(article_data)
                    else:
                        self.validation_errors += 1

                except Exception as e:
                    # Log specific parsing errors without stopping
                    self.validation_errors += 1
                    continue

            return articles_on_page

        except Exception as e:
            print(f"Error scraping page {page_num}: {e}")
            return []

    def scrape_all_pages(self, max_page, start_page=1, sample_every=1):
        print(f"\nStarting scraping...")
        print(f"Pages to scrape: {start_page} to {max_page}")
        print(f"Sampling: every {sample_every} page(s)")
        print("-" * 60)

        total_pages = ((max_page - start_page) // sample_every) + 1
        scraped = 0

        for page_num in range(start_page, max_page + 1, sample_every):
            scraped += 1
            print(f"\n[{scraped}/{total_pages}] - Scraping page {page_num:,}...")

            articles_on_page = self.scrape_page(page_num)

            if articles_on_page:
                print(f"Found {len(articles_on_page)} articles")
                for article in articles_on_page:
                    self.articles[article["url"]] = article
            else:
                print(f"No articles found")

            time.sleep(0.5)

            if scraped % 100 == 0:
                print(
                    f"\nProgress: {scraped}/{total_pages} pages scraped, "
                    f"{len(self.articles):,} articles collected"
                )
                self.save_checkpoint()

        print(f"\nScraping complete!")
        print(f"Total articles collected: {len(self.articles):,}")
        if self.validation_errors > 0:
            print(f"Validation errors skipped: {self.validation_errors}")

        self.rebuild_articles_by_date()

        self.save_checkpoint()

    def rebuild_articles_by_date(self):
        self.articles_by_date = defaultdict(list)
        for article in self.articles.values():
            self.articles_by_date[article["date_parsed"]].append(article)

    def save_checkpoint(self):
        print(f"Saving checkpoint ({len(self.articles):,} articles)...")

        checkpoint_file = os.path.join(self.output_dir, "checkpoint.json")
        with open(checkpoint_file, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "timestamp": datetime.now().isoformat(),
                    "articles_count": len(self.articles),
                    "articles": list(self.articles.values()),
                },
                f,
                indent=2,
                ensure_ascii=False,
            )

        csv_file = os.path.join(self.output_dir, "articles.csv")
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            fieldnames = [
                "url",
                "title",
                "date_raw",
                "date_parsed",
                "page_num",
                "archive_url",
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(self.articles.values())

        report = self.generate_report()
        report_file = os.path.join(self.output_dir, "report.json")
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        daily_file = os.path.join(self.output_dir, "daily_summary.csv")
        with open(daily_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Article Count"])
            for date in sorted(report["daily_statistics"]["articles_per_day"].keys()):
                count = report["daily_statistics"]["articles_per_day"][date]
                writer.writerow([date, count])

        print("Checkpoint saved: CSV, JSON, Report, Daily summary")

    def generate_report(self):
        print("\nGenerating report...")
        all_unique_articles = list(self.articles.values())

        sorted_articles = sorted(
            all_unique_articles,
            key=lambda x: (
                x["date_parsed"] if x["date_parsed"] != "UNKNOWN_DATE" else "9999-12-31"
            ),
        )

        daily_stats = defaultdict(int)

        for article in all_unique_articles:
            daily_stats[article["date_parsed"]] += 1

        known_date_articles_per_day = {
            date: count for date, count in daily_stats.items() if date != "UNKNOWN_DATE"
        }

        total_unique_articles = len(all_unique_articles)
        num_known_dates = len(known_date_articles_per_day)

        average_per_day = (
            sum(known_date_articles_per_day.values()) / num_known_dates
            if num_known_dates > 0
            else 0
        )
        max_per_day = (
            max(known_date_articles_per_day.values()) if num_known_dates > 0 else 0
        )
        min_per_day = (
            min(known_date_articles_per_day.values()) if num_known_dates > 0 else 0
        )

        report = {
            "generated_at": datetime.now().isoformat(),
            "total_articles": total_unique_articles,
            "date_range": {
                "earliest": (
                    sorted_articles[0]["date_parsed"] if sorted_articles else None
                ),
                "latest": (
                    sorted_articles[-1]["date_parsed"] if sorted_articles else None
                ),
            },
            "daily_statistics": {
                "dates": num_known_dates,
                "articles_per_day": dict(sorted(daily_stats.items())),
                "average_per_day": average_per_day,
                "max_per_day": max_per_day,
                "min_per_day": min_per_day,
            },
            "cleaning_summary": {
                "initial_article_count": total_unique_articles,
                "final_article_count": total_unique_articles,
                "duplicates_removed": 0,
                "deduplication_rate": "0.00%",
            },
        }

        return report

    def load_checkpoint(self, checkpoint_dir):
        """Load checkpoint with validation."""
        print(f"\nLoading checkpoint from: {checkpoint_dir}")

        checkpoint_file = os.path.join(checkpoint_dir, "checkpoint.json")
        if not os.path.exists(checkpoint_file):
            print(f"No checkpoint.json found in {checkpoint_dir}")
            return False

        try:
            with open(checkpoint_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Validate checkpoint data structure
            if not isinstance(data, dict):
                print("Invalid checkpoint format: not a dictionary")
                return False
            
            if "articles" not in data:
                print("Invalid checkpoint format: missing 'articles' key")
                return False
            
            articles_list = data.get("articles", [])
            if not isinstance(articles_list, list):
                print("Invalid checkpoint format: 'articles' is not a list")
                return False
            
            # Load articles with validation
            valid_count = 0
            invalid_count = 0
            for article in articles_list:
                # Validate each article before loading
                if self.validate_article_data(article):
                    self.articles[article["url"]] = article
                    valid_count += 1
                else:
                    invalid_count += 1

            self.rebuild_articles_by_date()

            self.output_dir = checkpoint_dir

            print(f"Loaded {valid_count:,} valid articles from checkpoint")
            if invalid_count > 0:
                print(f"Skipped {invalid_count:,} invalid articles from checkpoint")

            max_page_scraped = max(
                (article["page_num"] for article in self.articles.values()), default=0
            )
            print(f"Last scraped page: {max_page_scraped}")

            return max_page_scraped

        except json.JSONDecodeError as e:
            print(f"Error: Checkpoint file is not valid JSON: {e}")
            return False
        except Exception as e:
            print(f"Error loading checkpoint: {e}")
            return False

    def extract_article_id(self, url):
        try:
            parts = url.split("/")
            for i, part in enumerate(parts):
                if part == "nuestro-blog" and i + 1 < len(parts):
                    return int(parts[i + 1])
        except:
            pass
        return None

    def get_min_article_id(self):
        min_id = float("inf")
        for article in self.articles.values():
            article_id = self.extract_article_id(article["url"])
            if article_id and article_id < min_id:
                min_id = article_id

        return min_id if min_id != float("inf") else 0

    def calculate_resume_page(self, max_page, articles_per_page=9):
        min_id = self.get_min_article_id()
        if min_id == 0:
            return 1

        total_articles_estimated = max_page * articles_per_page

        articles_remaining = total_articles_estimated - min_id

        resume_page = articles_remaining // articles_per_page

        if resume_page < 1:
            resume_page = 1
        if resume_page > max_page:
            resume_page = max_page

        print(f"Min article ID scraped (last article): {min_id:,}")
        print(f"Total articles estimated: {total_articles_estimated:,}")
        print(f"Articles remaining: {articles_remaining:,}")
        print(f"Calculated resume page: {resume_page:,}")

        return resume_page
