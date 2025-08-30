# GitHub Repository Health Dashboard

## Overview

A comprehensive Streamlit web application that analyzes GitHub repository health through metrics scoring and interactive visualizations. The application fetches repository data via the GitHub API, calculates health scores based on activity, popularity, community engagement, and maintenance quality, then presents results through an intuitive dashboard with gauge charts and timeline visualizations.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web framework for rapid dashboard development
- **Layout**: Wide layout with sidebar navigation for input controls
- **State Management**: Session state for persisting repository data and health scores across interactions
- **Responsive Design**: Mobile-friendly interface that adapts to different screen sizes

### Backend Architecture
- **Modular Design**: Separated into distinct modules for API interaction, health calculation, and visualizations
- **GitHub API Client**: Custom GitHubAPI class handling authentication, URL parsing, and rate limiting
- **Health Scoring Engine**: HealthCalculator class implementing weighted scoring algorithm across four dimensions:
  - Activity (25%): Recent commits, issues, and pull requests
  - Popularity (25%): Stars, forks, and watchers
  - Community (25%): Contributors and community engagement
  - Maintenance (25%): Issue resolution and update frequency
- **Visualization Engine**: Plotly-based charts including gauge charts and timeline visualizations

### Data Processing
- **Real-time Analysis**: On-demand repository analysis triggered by user input
- **Error Handling**: Robust handling of API rate limits, invalid repositories, and network issues
- **Data Transformation**: Raw GitHub API responses processed into structured metrics for scoring

### Authentication Strategy
- **Optional Token Authentication**: Supports GitHub Personal Access Tokens for increased rate limits
- **Fallback Public Access**: Functions without authentication for basic usage
- **Environment Variable Support**: Token can be provided via environment variables or UI input

## External Dependencies

### Core Libraries
- **Streamlit**: Web application framework for dashboard interface
- **Requests**: HTTP client library for GitHub API communication
- **Plotly**: Interactive visualization library for charts and graphs
- **Pandas**: Data manipulation and analysis library

### GitHub API Integration
- **GitHub REST API v3**: Primary data source for repository metrics
- **Rate Limiting**: Handles GitHub API rate limits (60 requests/hour unauthenticated, 5000 with token)
- **Authentication**: Optional GitHub Personal Access Token for enhanced access

### Visualization Components
- **Plotly Graph Objects**: Gauge charts for health score visualization
- **Plotly Express**: Timeline charts for commit activity tracking
- **Interactive Charts**: Real-time data exploration capabilities

### Development Environment
- **Python 3.7+**: Minimum runtime requirement
- **Port Configuration**: Configurable server port (default 5000)
- **Environment Variables**: Support for GITHUB_TOKEN configuration