import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime as dt, timedelta
from typing import Optional, Dict, Any

# Constants
UNKNOWN_DATE = "UNKNOWN_DATE"


class Q2BDataVisualizer:
    def __init__(self, input_dir, config: Optional[Dict[str, Any]] = None):
        self.input_dir = input_dir
        self.config = config or self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """Return default configuration if no Hydra config provided."""
        return {
            "visualization": {
                "colors": {
                    "primary": "#FF6B6B",
                    "secondary": "#4ECDC4",
                    "tertiary": "#45B7D1",
                    "quaternary": "#FFA07A",
                    "quinary": "#98D8C8",
                    "partial_day": "#CCCCCC",
                    "average_line": "red"
                },
                "dimensions": {
                    "daily_articles": {"width": 14, "height": 8},
                    "timeline": {"width": 14, "height": 8},
                    "stats_summary": {"width": 16, "height": 12}
                },
                "fonts": {
                    "title": 14,
                    "xlabel": 14,
                    "ylabel": 14,
                    "legend": 12,
                    "annotation_large": 60,
                    "annotation_medium": 25,
                    "annotation_small": 18,
                    "tick_small": 8,
                    "tick_medium": 9,
                    "tick_large": 10
                },
                "chart_settings": {
                    "bar_alpha": 0.8,
                    "bar_edge_width": 1.5,
                    "line_width": 3,
                    "marker_size": 12,
                    "marker_edge_width": 2,
                    "peak_marker_size": 25,
                    "grid_alpha": 0.3
                },
                "labels": {
                    "max_days_full_labels": 15,
                    "max_days_half_labels": 30,
                    "max_days_fifth_labels": 90,
                    "max_days_tenth_labels": 180
                },
                "timeline": {
                    "x_axis_rotation": {
                        "max_days_no_rotation": 30,
                        "default_rotation": 45
                    }
                },
                "stats_summary": {
                    "background_color": "#f0f0f0",
                    "comparison_sources": [
                        {"name": "TechCrunch", "articles_per_day": 40},
                        {"name": "The Verge", "articles_per_day": 30},
                        {"name": "NY Times", "articles_per_day": 250}
                    ]
                }
            },
            "output": {
                "graphs_dir": "graphs",
                "dpi": 300,
                "bbox_inches": "tight"
            },
            "style": {
                "theme": "seaborn-v0_8-darkgrid"
            }
        }

    def create_visualizations(self, report):
        print("\nCreating visualizations...")

        graphs_dir = os.path.join(self.input_dir, self.config["output"]["graphs_dir"])
        os.makedirs(graphs_dir, exist_ok=True)

        plt.style.use(self.config["style"]["theme"])
        
        # Extract colors from config
        color_cfg = self.config["visualization"]["colors"]
        colors = [
            color_cfg["primary"],
            color_cfg["secondary"],
            color_cfg["tertiary"],
            color_cfg["quaternary"],
            color_cfg["quinary"]
        ]

        self.plot_daily_articles(report, graphs_dir, colors)
        self.plot_daily_timeline(report, graphs_dir, colors)
        self.plot_stats_summary(report, graphs_dir, colors)

        print(f"Graphs saved in: {graphs_dir}")

    def plot_daily_articles(self, report, output_dir, colors):
        daily_data = report["daily_statistics"]["articles_per_day"]

        if not daily_data:
            return

        # Get configuration values
        viz_cfg = self.config["visualization"]
        dims = viz_cfg["dimensions"]["daily_articles"]
        chart_cfg = viz_cfg["chart_settings"]
        color_cfg = viz_cfg["colors"]
        
        _, ax = plt.subplots(figsize=(dims["width"], dims["height"]))

        dates = list(daily_data.keys())
        counts = list(daily_data.values())

        earliest = report["date_range"]["earliest"]
        latest = report["date_range"]["latest"]

        bar_colors = []
        for date in dates:
            if date == earliest or date == latest:
                bar_colors.append(color_cfg["partial_day"])
            elif date == max(daily_data, key=daily_data.get):
                bar_colors.append(colors[1])
            else:
                bar_colors.append(colors[0])

        ax.bar(
            dates, counts, color=bar_colors, 
            alpha=chart_cfg["bar_alpha"], 
            edgecolor="black", 
            linewidth=chart_cfg["bar_edge_width"]
        )

        num_days = len(dates)

        important_indices = set()

        peak_date = max(daily_data, key=daily_data.get)
        if peak_date in dates:
            important_indices.add(dates.index(peak_date))

        important_indices.add(0)
        important_indices.add(len(dates) - 1)

        # Use label configuration
        label_cfg = viz_cfg["labels"]
        fonts_cfg = viz_cfg["fonts"]
        
        if num_days <= label_cfg["max_days_full_labels"]:
            indices_to_show = set(range(num_days))
            font_size = fonts_cfg["tick_large"]
        elif num_days <= label_cfg["max_days_half_labels"]:
            indices_to_show = set(range(0, num_days, 2)) | important_indices
            font_size = fonts_cfg["tick_medium"]
        elif num_days <= label_cfg["max_days_fifth_labels"]:
            indices_to_show = set(range(0, num_days, 5)) | important_indices
            font_size = fonts_cfg["tick_small"]
        elif num_days <= label_cfg["max_days_tenth_labels"]:
            indices_to_show = set(range(0, num_days, 10)) | important_indices
            font_size = fonts_cfg["tick_small"]
        else:
            indices_to_show = important_indices
            font_size = fonts_cfg["tick_medium"]

        for i, (date, count) in enumerate(zip(dates, counts)):
            if i in indices_to_show:
                label = f"{count:,}"
                if date == earliest or date == latest:
                    label += "\n(partial)"

                if num_days > label_cfg["max_days_tenth_labels"] and i in important_indices:
                    label = f"{date}\n{label}"

                ax.text(
                    i,
                    count + max(counts) * 0.02,
                    label,
                    ha="center",
                    va="bottom",
                    fontsize=font_size,
                    fontweight="bold",
                )

        avg = report["daily_statistics"]["average_per_day"]
        ax.axhline(
            y=avg,
            color=color_cfg["average_line"],
            linestyle="--",
            linewidth=2,
            label=f"Average: {avg:,.0f} articles/day (excl. partial days)",
            alpha=0.7,
        )

        ax.set_xlabel("Date", fontsize=fonts_cfg["xlabel"], fontweight="bold")
        ax.set_ylabel("Number of Articles", fontsize=fonts_cfg["ylabel"], fontweight="bold")

        date_range = f"{earliest} to {latest}"
        label_info = (
            f"\nShowing {len(indices_to_show)} of {num_days} days"
            if num_days > label_cfg["max_days_fifth_labels"]
            else ""
        )
        ax.set_title(
            f'Q2BSTUDIO: Daily Article Production\n"Industrial-Scale Automated Content Generation"\nData Period: {date_range}{label_info}\nNote: First and last days excluded from average (incomplete data)',
            fontsize=fonts_cfg["title"],
            fontweight="bold",
            pad=20,
        )

        ax.legend(fontsize=fonts_cfg["legend"], loc="upper left")
        ax.grid(True, alpha=chart_cfg["grid_alpha"], axis="y")

        if num_days <= 7:
            plt.xticks(rotation=0)
        elif num_days <= 31:
            plt.xticks(rotation=45, ha="right")
        elif num_days <= 90:
            tick_positions = list(range(0, num_days, 7))
            tick_labels = [dates[i] if i < len(dates) else "" for i in tick_positions]
            plt.xticks(tick_positions, tick_labels, rotation=45, ha="right")
        elif num_days <= 365:
            tick_positions = list(range(0, num_days, 30))
            tick_labels = [dates[i] if i < len(dates) else "" for i in tick_positions]
            plt.xticks(tick_positions, tick_labels, rotation=45, ha="right")
        elif num_days <= 730:
            tick_positions = list(range(0, num_days, 60))
            tick_labels = [dates[i] if i < len(dates) else "" for i in tick_positions]
            plt.xticks(tick_positions, tick_labels, rotation=45, ha="right")
        else:
            tick_positions = list(range(0, num_days, 180))
            tick_labels = [dates[i] if i < len(dates) else "" for i in tick_positions]
            plt.xticks(tick_positions, tick_labels, rotation=45, ha="right")

        plt.tight_layout()
        output_cfg = self.config["output"]
        plt.savefig(
            os.path.join(output_dir, "1_daily_articles.png"),
            dpi=output_cfg["dpi"],
            bbox_inches=output_cfg["bbox_inches"],
        )
        plt.close()

        print("Created: 1_daily_articles.png")

    def plot_daily_timeline(self, report, output_dir, colors):
        daily_data = report["daily_statistics"]["articles_per_day"]

        if not daily_data:
            return

        # Get configuration values
        viz_cfg = self.config["visualization"]
        dims = viz_cfg["dimensions"]["timeline"]
        chart_cfg = viz_cfg["chart_settings"]
        
        _, ax = plt.subplots(figsize=(dims["width"], dims["height"]))

        dates_str = list(daily_data.keys())

        valid_dates_str = [d for d in dates_str if d != UNKNOWN_DATE]
        if not valid_dates_str:
            print(
                f"No valid dates after filtering '{UNKNOWN_DATE}'. Skipping 2_timeline.png"
            )
            return

        valid_dates_str.sort()

        dates = [dt.strptime(d, "%Y-%m-%d") for d in valid_dates_str]
        counts = [daily_data[d_str] for d_str in valid_dates_str]

        earliest = report["date_range"]["earliest"]
        latest = report["date_range"]["latest"]

        ax.plot(
            dates,
            counts,
            marker="o",
            markersize=chart_cfg["marker_size"],
            linewidth=chart_cfg["line_width"],
            color=colors[3],
            label="Articles Published",
            markeredgecolor="black",
            markeredgewidth=chart_cfg["marker_edge_width"],
        )

        ax.fill_between(dates, counts, alpha=0.3, color=colors[3])

        dates_calc = [d for d in valid_dates_str if d != earliest and d != latest]
        if dates_calc:
            peak_date_str = max(dates_calc, key=lambda d: daily_data[d])
            max_idx = valid_dates_str.index(peak_date_str)

            ax.plot(
                dates[max_idx],
                counts[max_idx],
                marker="*",
                markersize=chart_cfg["peak_marker_size"],
                color="red",
                label=f"Peak: {counts[max_idx]:,} articles ({peak_date_str})",
                markeredgecolor="black",
                markeredgewidth=chart_cfg["marker_edge_width"],
            )

        num_days = (dates[-1] - dates[0]).days if dates else 0

        if num_days > 365 * 2:
            ax.xaxis.set_major_locator(mdates.YearLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
        elif num_days > 90:
            ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
        elif num_days > 30:
            ax.xaxis.set_major_locator(
                mdates.WeekdayLocator(byweekday=mdates.MO, interval=2)
            )
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
        else:
            ax.xaxis.set_major_locator(mdates.DayLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))

        fonts_cfg = viz_cfg["fonts"]
        ax.set_xlabel("Date", fontsize=fonts_cfg["xlabel"], fontweight="bold")
        ax.set_ylabel("Articles Published", fontsize=fonts_cfg["ylabel"], fontweight="bold")

        avg = report["daily_statistics"]["average_per_day"]
        avg_seconds = 86400 / avg if avg > 0 else 0

        date_range = f"{earliest} to {latest}"
        ax.set_title(
            f"Publication Timeline: {date_range}\nAverage: 1 article every {avg_seconds:.1f} seconds",
            fontsize=fonts_cfg["title"],
            fontweight="bold",
            pad=20,
        )

        ax.legend(fontsize=fonts_cfg["legend"], loc="best")
        ax.grid(True, alpha=chart_cfg["grid_alpha"])

        timeline_cfg = viz_cfg["timeline"]["x_axis_rotation"]
        if num_days > timeline_cfg["max_days_no_rotation"] or len(dates) > 10:
            plt.xticks(rotation=timeline_cfg["default_rotation"], ha="right")
        else:
            plt.xticks(rotation=0)

        plt.tight_layout()
        output_cfg = self.config["output"]
        plt.savefig(
            os.path.join(output_dir, "2_timeline.png"), 
            dpi=output_cfg["dpi"], 
            bbox_inches=output_cfg["bbox_inches"]
        )
        plt.close()

        print("Created: 2_timeline.png")

    def plot_stats_summary(self, report, output_dir, colors):
        # Get configuration values
        viz_cfg = self.config["visualization"]
        dims = viz_cfg["dimensions"]["stats_summary"]
        fonts_cfg = viz_cfg["fonts"]
        stats_cfg = viz_cfg["stats_summary"]

        daily_data = report["daily_statistics"]["articles_per_day"]
        valid_data = {k: v for k, v in daily_data.items() if k != UNKNOWN_DATE}

        last_4_weeks_data = {}
        last_4_weeks_total = 0
        last_4_weeks_peak = 0

        if valid_data:
            try:
                latest_date_str = max(valid_data.keys())
                latest_date = dt.strptime(latest_date_str, "%Y-%m-%d")
                four_weeks_ago = latest_date - timedelta(days=28)

                for date_str, count in valid_data.items():
                    date_obj = dt.strptime(date_str, "%Y-%m-%d")
                    if date_obj >= four_weeks_ago:
                        last_4_weeks_data[date_str] = count
                        last_4_weeks_total += count
                        if count > last_4_weeks_peak:
                            last_4_weeks_peak = count
            except:
                last_4_weeks_data = valid_data
                last_4_weeks_total = sum(valid_data.values())
                last_4_weeks_peak = max(valid_data.values()) if valid_data else 0

        num_days = len(last_4_weeks_data)
        last_4_weeks_avg = last_4_weeks_total / num_days if num_days > 0 else 0

        if last_4_weeks_data:
            earliest_4w = min(last_4_weeks_data.keys())
            latest_4w = max(last_4_weeks_data.keys())
            date_range_4w = f"{earliest_4w} to {latest_4w}"
        else:
            date_range_4w = "No data"

        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(dims["width"], dims["height"]))

        fig.suptitle(
            f"Q2BSTUDIO Content Farm: Statistical Analysis (Last 4 Weeks)\nPeriod: {date_range_4w}",
            fontsize=fonts_cfg["annotation_small"],
            fontweight="bold",
            y=0.98,
        )

        ax1.text(
            0.5,
            0.6,
            f"{last_4_weeks_total:,}",
            ha=stats_cfg["text_ha"],
            va=stats_cfg["text_va"],
            fontsize=fonts_cfg["annotation_large"],
            fontweight="bold",
            color=colors[0],
        )
        ax1.text(
            0.5,
            0.35,
            "Articles Published\n(Last 4 Weeks)",
            ha=stats_cfg["text_ha"],
            va=stats_cfg["text_va"],
            fontsize=fonts_cfg["annotation_small"],
            fontweight="bold",
        )
        ax1.axis("off")
        ax1.set_facecolor(stats_cfg["background_color"])

        ax2.text(
            0.5,
            0.6,
            f"{last_4_weeks_avg:,.0f}",
            ha=stats_cfg["text_ha"],
            va=stats_cfg["text_va"],
            fontsize=fonts_cfg["annotation_large"],
            fontweight="bold",
            color=colors[1],
        )
        ax2.text(
            0.5,
            0.35,
            "Articles Per Day\n(Last 4 Weeks Avg)",
            ha=stats_cfg["text_ha"],
            va=stats_cfg["text_va"],
            fontsize=fonts_cfg["annotation_small"],
            fontweight="bold",
        )
        seconds = 86400 / last_4_weeks_avg if last_4_weeks_avg > 0 else 0
        ax2.text(
            0.5,
            0.15,
            f"1 article every {seconds:.1f} seconds",
            ha=stats_cfg["text_ha"],
            va=stats_cfg["text_va"],
            fontsize=fonts_cfg["annotation_medium"],
            color="red",
            fontweight="bold",
        )
        ax2.axis("off")
        ax2.set_facecolor(stats_cfg["background_color"])

        ax3.text(
            0.5,
            0.6,
            f"{last_4_weeks_peak:,}",
            ha=stats_cfg["text_ha"],
            va=stats_cfg["text_va"],
            fontsize=fonts_cfg["annotation_large"],
            fontweight="bold",
            color=colors[2],
        )
        ax3.text(
            0.5,
            0.35,
            "Peak Day\n(Last 4 Weeks Max)",
            ha=stats_cfg["text_ha"],
            va=stats_cfg["text_va"],
            fontsize=fonts_cfg["annotation_small"],
            fontweight="bold",
        )
        peak_seconds = 86400 / last_4_weeks_peak if last_4_weeks_peak > 0 else 0
        ax3.text(
            0.5,
            0.15,
            f"1 article every {peak_seconds:.1f} seconds",
            ha=stats_cfg["text_ha"],
            va=stats_cfg["text_va"],
            fontsize=fonts_cfg["annotation_medium"],
            fontweight="bold",
            color="red",
        )
        ax3.axis("off")
        ax3.set_facecolor(stats_cfg["background_color"])

        # Build comparisons from config
        comparisons = [(src["name"], src["articles_per_day"]) for src in stats_cfg["comparison_sources"]]
        comparisons.append(("Q2BSTUDIO\n(Last 4 Weeks)", last_4_weeks_avg))

        names = [c[0] for c in comparisons]
        values = [c[1] for c in comparisons]

        chart_cfg = viz_cfg["chart_settings"]
        bars = ax4.barh(
            names,
            values,
            color=[colors[4]] * (len(comparisons) - 1) + [colors[0]],
            edgecolor="black",
            linewidth=chart_cfg["bar_edge_width"],
        )

        bars[-1].set_alpha(1.0)

        for i, (_, value) in enumerate(zip(names, values)):
            ax4.text(
                value + max(values) * 0.02,
                i,
                f"{value:,.0f}",
                va=stats_cfg["text_va"],
                fontsize=fonts_cfg["legend"],
                fontweight="bold",
            )

        ax4.set_xlabel("Articles Per Day", fontsize=fonts_cfg["legend"], fontweight="bold")
        ax4.set_title(
            "Comparison: Daily Output (Last 4 Weeks)\n(Industry estimates - conservative)",
            fontsize=fonts_cfg["title"],
            fontweight="bold",
            pad=10,
        )
        ax4.grid(True, alpha=chart_cfg["grid_alpha"], axis="x")

        plt.tight_layout()
        output_cfg = self.config["output"]
        plt.savefig(
            os.path.join(output_dir, "3_stats_summary.png"),
            dpi=output_cfg["dpi"],
            bbox_inches=output_cfg["bbox_inches"],
        )
        plt.close()

        print("Created: 3_stats_summary.png")
