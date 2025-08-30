# 📊 GitHub Repository Health Dashboard

A comprehensive Streamlit dashboard for analyzing GitHub repository health with metrics, scoring, and interactive visualizations.

## 🚀 Features

- **Repository Analysis**: Enter any GitHub repository URL for instant analysis
- **Comprehensive Metrics**: Stars, forks, watchers, issues, pull requests, contributors
- **Health Scoring**: AI-powered scoring algorithm (0-100) based on:
  - Recent activity (commits, issues, PRs)
  - Community engagement (contributors, discussions)
  - Repository popularity (stars, forks, watchers)
  - Maintenance quality (update frequency, issue resolution)
- **Interactive Visualizations**:
  - Health score gauge chart
  - 30-day commit activity timeline
  - Detailed metric breakdowns
- **Error Handling**: Robust handling of API rate limits and invalid repositories
- **Mobile-Friendly**: Responsive design that works on all devices

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.7 or higher
- GitHub Personal Access Token (optional, but recommended for higher rate limits)

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd github-repo-health-dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install streamlit requests plotly pandas
   ```

3. **Set up GitHub token (optional)**
   ```bash
   export GITHUB_TOKEN=your_personal_access_token_here
   ```

4. **Run the application**
   ```bash
   streamlit run app.py --server.port 5000
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## 🌐 Deployment

### Streamlit Cloud Deployment

1. **Fork this repository** to your GitHub account

2. **Create a Streamlit Cloud account** at [share.streamlit.io](https://share.streamlit.io)

3. **Deploy the app**:
   - Click "New app" in Streamlit Cloud
   - Connect your GitHub account
   - Select this repository
   - Set the main file path to `app.py`
   - Click "Deploy"

4. **Configure secrets (optional)**:
   - In your Streamlit Cloud dashboard, go to app settings
   - Add secrets in TOML format:
     ```toml
     GITHUB_TOKEN = "your_personal_access_token_here"
     ```

### Alternative Deployment Options

#### Heroku
1. Create a `Procfile` in the root directory:
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. Create `runtime.txt`:
   ```
   python-3.9.16
   ```

3. Deploy using Heroku CLI or GitHub integration

#### Railway
1. Connect your GitHub repository to Railway
2. Railway will automatically detect the Streamlit app
3. Set environment variables as needed

## 📋 Usage Guide

### Basic Usage

1. **Enter Repository URL**: Paste any GitHub repository URL in the sidebar
   - Format: `https://github.com/owner/repository`
   - Examples: 
     - `https://github.com/streamlit/streamlit`
     - `https://github.com/microsoft/vscode`

2. **Optional: Add GitHub Token**: For higher rate limits and private repository access

3. **Click "Analyze Repository"**: The dashboard will fetch data and display results

### Understanding the Health Score

The health score (0-100) is calculated based on four components:

- **Activity Score (25%)**: Recent commits, issues, and pull requests
- **Popularity Score (25%)**: Stars, forks, and watchers
- **Community Score (25%)**: Number of contributors and community features
- **Maintenance Score (25%)**: Update frequency and issue resolution

### Score Interpretation

- **90-100**: Excellent - Very healthy, active repository
- **75-89**: Good - Well-maintained with regular activity
- **60-74**: Fair - Moderate activity, some areas for improvement
- **40-59**: Poor - Low activity, maintenance concerns
- **0-39**: Critical - Inactive or abandoned repository

## 🔧 Configuration

### GitHub API Rate Limits

- **Unauthenticated**: 60 requests per hour
- **Authenticated**: 5,000 requests per hour

To increase rate limits, provide a GitHub Personal Access Token:

1. Go to [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
2. Click "Generate new token"
3. Select scopes: `public_repo` (for public repositories)
4. Copy the token and add it to the application

### Environment Variables

- `GITHUB_TOKEN`: Your GitHub Personal Access Token

## 🐛 Troubleshooting

### Common Issues

1. **"Repository not found"**
   - Ensure the URL is correct and the repository is public
   - Check if the repository exists and hasn't been renamed

2. **"API rate limit exceeded"**
   - Add a GitHub Personal Access Token
   - Wait for the rate limit to reset (1 hour for unauthenticated requests)

3. **"Invalid GitHub token"**
   - Verify your token is correct and hasn't expired
   - Ensure the token has appropriate permissions

### Error Messages

The application provides detailed error messages for:
- Invalid repository URLs
- Network connectivity issues
- API rate limit violations
- Authentication failures

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing web app framework
- [GitHub API](https://docs.github.com/en/rest) for providing repository data
- [Plotly](https://plotly.com/) for interactive visualizations

## 📞 Support

If you encounter any issues or have questions:

1. Check the [troubleshooting section](#-troubleshooting)
2. Search [existing issues](../../issues)
3. Create a [new issue](../../issues/new) with detailed information

---

**Happy analyzing! 📊✨**
