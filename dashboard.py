#!/usr/bin/env python3
"""
Interactive Dashboard for Q2BSTUDIO Auditor

A Streamlit-based interactive visualization dashboard for exploring
industrial-scale content generation patterns.

Usage:
    streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import json
import glob
from datetime import datetime, timedelta


def load_latest_checkpoint():
    """Find and return the latest checkpoint directory."""
    checkpoints = sorted(glob.glob("q2b_audit_*"), reverse=True)
    checkpoints = [d for d in checkpoints if os.path.isdir(d)]
    return checkpoints[0] if checkpoints else None


def load_data(checkpoint_dir):
    """Load data from checkpoint directory."""
    csv_file = os.path.join(checkpoint_dir, "articles.csv")
    report_file = os.path.join(checkpoint_dir, "report.json")
    
    if not os.path.exists(csv_file):
        return None, None
    
    df = pd.read_csv(csv_file)
    
    report = None
    if os.path.exists(report_file):
        with open(report_file, 'r', encoding='utf-8') as f:
            report = json.load(f)
    
    return df, report


def main():
    st.set_page_config(
        page_title="Q2BSTUDIO Auditor Dashboard",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Header
    st.title("📊 Q2BSTUDIO Content Analysis Dashboard")
    st.markdown("**Interactive forensic analysis of industrial-scale automated content generation**")
    st.markdown("---")
    
    # Sidebar - Checkpoint selection
    st.sidebar.header("⚙️ Configuration")
    
    checkpoints = sorted(glob.glob("q2b_audit_*"), reverse=True)
    checkpoints = [d for d in checkpoints if os.path.isdir(d)]
    
    if not checkpoints:
        st.error("❌ No checkpoint directories found. Please run the scraper first.")
        st.stop()
    
    selected_checkpoint = st.sidebar.selectbox(
        "Select Dataset",
        checkpoints,
        index=0,
        help="Choose a checkpoint directory to analyze"
    )
    
    # Load data
    df, report = load_data(selected_checkpoint)
    
    if df is None:
        st.error(f"❌ Could not load data from {selected_checkpoint}")
        st.stop()
    
    # Data info
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📈 Dataset Info")
    st.sidebar.metric("Total Articles", f"{len(df):,}")
    st.sidebar.metric("Checkpoint", selected_checkpoint.replace("q2b_audit_", ""))
    
    # Main content
    
    # Summary metrics
    st.header("📊 Key Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Articles", f"{len(df):,}")
    
    # Calculate metrics for all columns
    known_dates = df[df['date_parsed'] != 'UNKNOWN_DATE']
    unique_days = 0
    avg_per_day = 0
    
    if len(known_dates) > 0:
        unique_days = known_dates['date_parsed'].nunique()
        if unique_days > 0:
            avg_per_day = len(known_dates) / unique_days
    
    with col2:
        if avg_per_day > 0:
            st.metric("Avg Articles/Day", f"{avg_per_day:,.0f}")
        else:
            st.metric("Avg Articles/Day", "N/A")
    
    with col3:
        if report and 'daily_statistics' in report:
            max_day = report['daily_statistics'].get('max_per_day', 0)
            st.metric("Peak Day", f"{max_day:,}")
        else:
            st.metric("Peak Day", "N/A")
    
    with col4:
        if avg_per_day > 0:
            seconds = 86400 / avg_per_day
            st.metric("Frequency", f"1 article / {seconds:.1f}s")
        else:
            st.metric("Frequency", "N/A")
    
    st.markdown("---")
    
    # Date filter
    st.header("🔍 Filter Data")
    
    known_dates = df[df['date_parsed'] != 'UNKNOWN_DATE'].copy()
    
    if len(known_dates) > 0:
        known_dates['date_parsed'] = pd.to_datetime(known_dates['date_parsed'])
        
        min_date = known_dates['date_parsed'].min()
        max_date = known_dates['date_parsed'].max()
        
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input(
                "Start Date",
                value=min_date,
                min_value=min_date,
                max_value=max_date
            )
        with col2:
            end_date = st.date_input(
                "End Date",
                value=max_date,
                min_value=min_date,
                max_value=max_date
            )
        
        # Filter data
        filtered_df = known_dates[
            (known_dates['date_parsed'] >= pd.to_datetime(start_date)) &
            (known_dates['date_parsed'] <= pd.to_datetime(end_date))
        ]
        
        st.info(f"📅 Showing {len(filtered_df):,} articles from {start_date} to {end_date}")
        
        st.markdown("---")
        
        # Visualizations
        st.header("📈 Visualizations")
        
        # Daily article count
        st.subheader("Daily Article Production")
        daily_counts = filtered_df.groupby(filtered_df['date_parsed'].dt.date).size().reset_index()
        daily_counts.columns = ['Date', 'Article Count']
        
        fig = px.bar(
            daily_counts,
            x='Date',
            y='Article Count',
            title='Articles Published Per Day',
            labels={'Article Count': 'Number of Articles', 'Date': 'Publication Date'},
            color='Article Count',
            color_continuous_scale='Reds'
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Timeline
        st.subheader("Publication Timeline")
        fig = px.line(
            daily_counts,
            x='Date',
            y='Article Count',
            title='Publication Timeline',
            markers=True
        )
        fig.add_hline(
            y=daily_counts['Article Count'].mean(),
            line_dash="dash",
            line_color="red",
            annotation_text=f"Average: {daily_counts['Article Count'].mean():.0f}"
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Distribution histogram
        st.subheader("Distribution Analysis")
        fig = px.histogram(
            daily_counts,
            x='Article Count',
            nbins=30,
            title='Distribution of Daily Article Counts',
            labels={'Article Count': 'Articles Per Day', 'count': 'Frequency'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Hourly pattern (if we had time data - simulated for demo)
        st.subheader("Publication Pattern")
        col1, col2 = st.columns(2)
        
        with col1:
            # Day of week analysis
            filtered_df['day_of_week'] = filtered_df['date_parsed'].dt.day_name()
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            day_counts = filtered_df['day_of_week'].value_counts().reindex(day_order, fill_value=0)
            
            fig = px.bar(
                x=day_counts.index,
                y=day_counts.values,
                title='Articles by Day of Week',
                labels={'x': 'Day', 'y': 'Article Count'},
                color=day_counts.values,
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Monthly trend
            filtered_df['year_month'] = filtered_df['date_parsed'].dt.to_period('M').astype(str)
            month_counts = filtered_df['year_month'].value_counts().sort_index()
            
            fig = px.bar(
                x=month_counts.index,
                y=month_counts.values,
                title='Articles by Month',
                labels={'x': 'Month', 'y': 'Article Count'},
                color=month_counts.values,
                color_continuous_scale='Greens'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Data table
        st.header("📋 Article Data")
        
        # Search
        search_term = st.text_input("🔍 Search articles by title", "")
        
        display_df = filtered_df.copy()
        if search_term:
            display_df = display_df[
                display_df['title'].str.contains(search_term, case=False, na=False)
            ]
        
        st.dataframe(
            display_df[['title', 'date_parsed', 'url']].head(100),
            use_container_width=True,
            height=400
        )
        
        st.info(f"Showing first 100 of {len(display_df):,} articles")
        
    else:
        st.warning("⚠️ No articles with valid dates found in this dataset.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
        <small>Q2BSTUDIO Auditor Dashboard | Documenting Industrial-Scale Automated Content Generation</small>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
