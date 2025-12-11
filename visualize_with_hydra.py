#!/usr/bin/env python3
"""
Visualization script using Hydra configuration management.

This script demonstrates how to use Hydra to configure visualizations
with different color schemes, dimensions, and other parameters.

Usage:
    # Use default configuration
    python visualize_with_hydra.py checkpoint_dir=q2b_audit_20251208_103810

    # Use dark color scheme
    python visualize_with_hydra.py checkpoint_dir=q2b_audit_20251208_103810 visualization=dark

    # Override specific colors
    python visualize_with_hydra.py checkpoint_dir=q2b_audit_20251208_103810 visualization.colors.primary=#FF0000

    # Change output DPI
    python visualize_with_hydra.py checkpoint_dir=q2b_audit_20251208_103810 output.dpi=600
"""

import hydra
from omegaconf import DictConfig, OmegaConf
import os
import json
from q2b_data_visualizer import Q2BDataVisualizer


@hydra.main(version_base=None, config_path="config", config_name="config")
def visualize(cfg: DictConfig) -> None:
    """
    Main visualization function using Hydra configuration.
    
    Args:
        cfg: Hydra configuration object containing all visualization settings
    """
    print("=" * 60)
    print("Q2BSTUDIO AUDITOR - HYDRA VISUALIZATION")
    print("=" * 60)
    
    # Print the configuration being used
    print("\nConfiguration:")
    print(OmegaConf.to_yaml(cfg))
    
    # Get checkpoint directory from config
    checkpoint_dir = cfg.get("checkpoint_dir", None)
    
    if not checkpoint_dir:
        print("\nError: Please specify checkpoint_dir")
        print("Example: python visualize_with_hydra.py checkpoint_dir=q2b_audit_YYYYMMDD_HHMMSS")
        return
    
    if not os.path.exists(checkpoint_dir):
        print(f"\nError: Checkpoint directory not found: {checkpoint_dir}")
        return
    
    # Load report data
    report_file = os.path.join(checkpoint_dir, "report.json")
    if not os.path.exists(report_file):
        print(f"\nError: Report file not found: {report_file}")
        print("Please run the scraper first to generate the report.")
        return
    
    with open(report_file, 'r', encoding='utf-8') as f:
        report = json.load(f)
    
    print(f"\nLoaded report from: {checkpoint_dir}")
    print(f"Total articles: {report['total_articles']:,}")
    print(f"Date range: {report['date_range']['earliest']} to {report['date_range']['latest']}")
    
    # Convert OmegaConf to regular dict for compatibility
    config_dict = OmegaConf.to_container(cfg, resolve=True)
    
    # Create visualizer with Hydra config
    visualizer = Q2BDataVisualizer(input_dir=checkpoint_dir, config=config_dict)
    
    # Generate visualizations
    print("\nGenerating visualizations with Hydra configuration...")
    visualizer.create_visualizations(report)
    
    print(f"\n✓ Visualization complete!")
    print(f"  Graphs saved in: {checkpoint_dir}/{cfg.output.graphs_dir}")
    print(f"  Theme: {cfg.style.theme}")
    print(f"  DPI: {cfg.output.dpi}")


if __name__ == "__main__":
    visualize()
