#!/usr/bin/env python3
"""Streamlit dashboard for WeatherML."""

import streamlit as st


def main() -> None:
    st.set_page_config(page_title="WeatherML Dashboard", page_icon="🌤️", layout="wide")

    st.title("🌤️ WeatherML Dashboard")
    st.markdown("Explore weather prediction models and results.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Models Trained", value="0", delta="—")
    with col2:
        st.metric(label="Best MAE", value="—", delta="—")
    with col3:
        st.metric(label="Last Updated", value="—", delta="—")

    st.divider()
    st.subheader("Quick Start")
    st.markdown("""
    1. Run experiments in `notebooks/`
    2. Train models: `uv run python scripts/train.py`
    3. View results in this dashboard
    """)


if __name__ == "__main__":
    main()
