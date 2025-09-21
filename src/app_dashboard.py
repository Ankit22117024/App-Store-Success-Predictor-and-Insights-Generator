# src/app_dashboard.py
# Author: Manak Chand Choudhary
# Date: 21 September 2025
# Description: This script creates a user-friendly web dashboard for the App Market
#              Intelligence System using Streamlit. It displays the executive report
#              and provides an interactive chat interface to the query engine.

import streamlit as st
import os
import sys
import glob

# --- Path Correction ---
# Add the 'src' directory to the Python path to allow for absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from phase4.query_engine import QueryEngine

# --- Configuration ---
REPORTS_DIR = os.path.join('generated_files', 'reports')

# --- Caching ---
# Cache the QueryEngine to prevent reloading the model on every interaction
@st.cache_resource
def load_engine():
    """Loads the QueryEngine and caches it."""
    engine = QueryEngine()
    if not engine.is_ready():
        st.error("Could not initialize the Query Engine. Please ensure the insight files from Phase 2 exist.")
        return None
    return engine

# --- Main Application ---

# Set page title and layout
st.set_page_config(page_title="App Success Predictor", layout="wide")

# Title for the dashboard
st.title("🚀 AI-Powered App Market Intelligence Dashboard")
st.markdown("Welcome! This dashboard provides AI-driven insights and an interactive query system to help you navigate the mobile app market.")

# Load the query engine
engine = load_engine()

if engine:
    # Create tabs for different sections
    tab1, tab2 = st.tabs(["📊 Executive Intelligence Report", "💬 Interactive Query System"])

    # --- Tab 1: Executive Report ---
    with tab1:
        st.header("Latest Executive Report")
        
        # Find the most recent report file
        try:
            report_files = glob.glob(os.path.join(REPORTS_DIR, '*.md'))
            if not report_files:
                st.warning("No executive reports found. Please run the Phase 3 report generator first.")
            else:
                latest_report = max(report_files, key=os.path.getctime)
                st.info(f"Displaying the latest report: **{os.path.basename(latest_report)}**")
                
                with open(latest_report, 'r', encoding='utf-8') as f:
                    report_content = f.read()
                
                st.markdown(report_content)
        except Exception as e:
            st.error(f"An error occurred while trying to load the report: {e}")

    # --- Tab 2: Interactive Query System ---
    with tab2:
        st.header("Ask a Question About the App Market")
        st.markdown("Interact with our AI to get specific answers based on the generated market insights.")

        # Initialize chat history in session state
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Accept user input
        if prompt := st.chat_input("What would you like to know?"):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = engine.answer_query(prompt)
                    st.markdown(response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
else:
    st.error("Dashboard could not be loaded. Please check the console for errors related to the Query Engine initialization.")
