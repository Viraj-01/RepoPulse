import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from github_api import GitHubAPI
from health_calculator import HealthCalculator
from visualizations import create_gauge_chart, create_commits_timeline

# Page configuration
st.set_page_config(
    page_title="GitHub Repo Health Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'repo_data' not in st.session_state:
    st.session_state.repo_data = None
if 'health_score' not in st.session_state:
    st.session_state.health_score = None

def main():
    st.title("📊 GitHub Repository Health Dashboard")
    st.markdown("---")
    
    # Sidebar for inputs
    with st.sidebar:
        st.header("Repository Input")
        repo_url = st.text_input(
            "GitHub Repository URL",
            placeholder="https://github.com/owner/repo",
            help="Enter a valid GitHub repository URL"
        )
        
        st.markdown("### API Configuration")
        api_token = st.text_input(
            "GitHub Personal Access Token (Optional)",
            type="password",
            help="Increases rate limits. Leave empty for public access."
        )
        
        analyze_button = st.button("🔍 Analyze Repository", type="primary")
        
        if st.button("🗑️ Clear Results"):
            st.session_state.repo_data = None
            st.session_state.health_score = None
            st.rerun()
    
    # Main content area
    if analyze_button and repo_url:
        analyze_repository(repo_url, api_token)
    
    # Display results if available
    if st.session_state.repo_data:
        display_dashboard()
    else:
        display_welcome_screen()

def analyze_repository(repo_url, api_token=None):
    """Analyze the repository and store results in session state"""
    
    # Show loading spinner
    with st.spinner("🔄 Fetching repository data..."):
        try:
            # Initialize GitHub API
            github_api = GitHubAPI(api_token)
            
            # Extract owner and repo from URL
            owner, repo = github_api.parse_repo_url(repo_url)
            
            if not owner or not repo:
                st.error("❌ Invalid GitHub repository URL. Please use format: https://github.com/owner/repo")
                return
            
            # Fetch repository data
            repo_data = github_api.get_repository_data(owner, repo)
            
            # Calculate health score
            health_calculator = HealthCalculator()
            health_score = health_calculator.calculate_health_score(repo_data)
            
            # Store in session state
            st.session_state.repo_data = repo_data
            st.session_state.health_score = health_score
            
            st.success("✅ Repository analysis completed!")
            st.rerun()
            
        except requests.exceptions.RequestException as e:
            st.error(f"🌐 Network error: {str(e)}")
        except ValueError as e:
            st.error(f"❌ {str(e)}")
        except Exception as e:
            st.error(f"💥 Unexpected error: {str(e)}")

def display_welcome_screen():
    """Display welcome screen with instructions"""
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        ### 🚀 Welcome to GitHub Repository Health Dashboard
        
        This dashboard analyzes GitHub repositories and provides comprehensive health metrics including:
        
        - **Repository Statistics**: Stars, forks, watchers, issues, and pull requests
        - **Activity Analysis**: Recent commits, contributor activity, and engagement
        - **Health Score**: AI-powered scoring based on multiple factors
        - **Visual Analytics**: Interactive charts and metrics
        
        #### 📝 How to use:
        1. Enter a GitHub repository URL in the sidebar
        2. Optionally provide a GitHub Personal Access Token for higher rate limits
        3. Click "Analyze Repository" to fetch data
        4. Explore the interactive dashboard with detailed metrics
        
        #### 🔧 Example repositories to try:
        - `https://github.com/streamlit/streamlit`
        - `https://github.com/microsoft/vscode`
        - `https://github.com/facebook/react`
        """)

def display_dashboard():
    """Display the main dashboard with repository metrics"""
    
    repo_data = st.session_state.repo_data
    health_score = st.session_state.health_score
    
    # Repository header
    st.markdown(f"## 📋 {repo_data['full_name']}")
    
    if repo_data.get('description'):
        st.markdown(f"*{repo_data['description']}*")
    
    # Display language and topics
    col1, col2 = st.columns([1, 1])
    with col1:
        if repo_data.get('language'):
            st.markdown(f"**Primary Language:** {repo_data['language']}")
    with col2:
        if repo_data.get('topics'):
            topics_str = ", ".join(repo_data['topics'][:5])  # Show first 5 topics
            st.markdown(f"**Topics:** {topics_str}")
    
    st.markdown("---")
    
    # Health Score Section
    st.markdown("### 🎯 Repository Health Score")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Health score gauge
        gauge_fig = create_gauge_chart(health_score['total_score'])
        st.plotly_chart(gauge_fig, use_container_width=True)
    
    with col2:
        # Health score breakdown
        st.markdown("#### Score Breakdown:")
        
        score_components = [
            ("Activity Score", health_score['activity_score'], "Recent commits, issues, and PRs"),
            ("Popularity Score", health_score['popularity_score'], "Stars, forks, and watchers"),
            ("Community Score", health_score['community_score'], "Contributors and community engagement"),
            ("Maintenance Score", health_score['maintenance_score'], "Issue resolution and update frequency")
        ]
        
        for name, score, description in score_components:
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.markdown(f"**{name}**: {description}")
            with col_b:
                st.metric("", f"{score:.1f}/25")
    
    st.markdown("---")
    
    # Key Metrics
    st.markdown("### 📊 Key Metrics")
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    metrics = [
        (col1, "⭐ Stars", repo_data.get('stargazers_count', 0), None),
        (col2, "🔀 Forks", repo_data.get('forks_count', 0), None),
        (col3, "👀 Watchers", repo_data.get('watchers_count', 0), None),
        (col4, "🐛 Open Issues", repo_data.get('open_issues_count', 0), None),
        (col5, "🔄 Open PRs", repo_data.get('open_prs_count', 0), None),
        (col6, "👥 Contributors", repo_data.get('contributors_count', 0), None)
    ]
    
    for col, label, value, delta in metrics:
        with col:
            st.metric(label, f"{value:,}", delta)
    
    st.markdown("---")
    
    # Repository Information
    st.markdown("### ℹ️ Repository Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### General Information")
        info_data = {
            "Created": datetime.fromisoformat(repo_data['created_at'].replace('Z', '+00:00')).strftime('%B %d, %Y'),
            "Last Updated": datetime.fromisoformat(repo_data['updated_at'].replace('Z', '+00:00')).strftime('%B %d, %Y'),
            "Default Branch": repo_data.get('default_branch', 'main'),
            "License": repo_data.get('license', {}).get('name', 'Not specified') if repo_data.get('license') else 'Not specified',
            "Size": f"{repo_data.get('size', 0):,} KB"
        }
        
        for key, value in info_data.items():
            st.markdown(f"**{key}:** {value}")
    
    with col2:
        st.markdown("#### Repository Features")
        features = {
            "Has Issues": "✅" if repo_data.get('has_issues') else "❌",
            "Has Wiki": "✅" if repo_data.get('has_wiki') else "❌",
            "Has Pages": "✅" if repo_data.get('has_pages') else "❌",
            "Has Projects": "✅" if repo_data.get('has_projects') else "❌",
            "Archived": "⚠️ Yes" if repo_data.get('archived') else "✅ No",
            "Fork": "Yes" if repo_data.get('fork') else "No"
        }
        
        for feature, status in features.items():
            st.markdown(f"**{feature}:** {status}")
    
    # Commit Activity Chart
    if repo_data.get('commit_activity'):
        st.markdown("---")
        st.markdown("### 📈 Commit Activity (Last 30 Days)")
        
        commits_fig = create_commits_timeline(repo_data['commit_activity'])
        st.plotly_chart(commits_fig, use_container_width=True)
    
    # Repository URLs
    st.markdown("---")
    st.markdown("### 🔗 Repository Links")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"[🔗 Repository]({repo_data['html_url']})")
    
    with col2:
        if repo_data.get('homepage'):
            st.markdown(f"[🌐 Homepage]({repo_data['homepage']})")
    
    with col3:
        st.markdown(f"[📥 Clone URL]({repo_data['clone_url']})")

if __name__ == "__main__":
    main()
