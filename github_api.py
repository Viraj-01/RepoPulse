import requests
import os
import re
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple, List

class GitHubAPI:
    """GitHub API client for fetching repository data"""
    
    def __init__(self, token: Optional[str] = None):
        """Initialize GitHub API client
        
        Args:
            token: GitHub personal access token for authenticated requests
        """
        self.base_url = "https://api.github.com"
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-Repo-Health-Dashboard"
        }
        
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"
    
    def parse_repo_url(self, url: str) -> Tuple[Optional[str], Optional[str]]:
        """Parse GitHub repository URL to extract owner and repo name
        
        Args:
            url: GitHub repository URL
            
        Returns:
            Tuple of (owner, repo) or (None, None) if invalid
        """
        # Remove trailing slash and .git extension
        url = url.rstrip('/').rstrip('.git')
        
        # Match GitHub URL patterns
        patterns = [
            r'https?://github\.com/([^/]+)/([^/]+)',
            r'git@github\.com:([^/]+)/([^/]+)',
            r'github\.com/([^/]+)/([^/]+)'
        ]
        
        for pattern in patterns:
            match = re.match(pattern, url)
            if match:
                return match.group(1), match.group(2)
        
        return None, None
    
    def make_request(self, endpoint: str) -> Dict:
        """Make authenticated request to GitHub API
        
        Args:
            endpoint: API endpoint (without base URL)
            
        Returns:
            JSON response data
            
        Raises:
            requests.RequestException: On API request failure
            ValueError: On API error responses
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        response = requests.get(url, headers=self.headers, timeout=30)
        
        if response.status_code == 404:
            raise ValueError("Repository not found. Please check the URL and ensure the repository is public.")
        elif response.status_code == 403:
            raise ValueError("API rate limit exceeded. Please provide a GitHub Personal Access Token.")
        elif response.status_code == 401:
            raise ValueError("Invalid GitHub token. Please check your Personal Access Token.")
        elif not response.ok:
            raise ValueError(f"GitHub API error: {response.status_code} - {response.text}")
        
        return response.json()
    
    def get_repository_data(self, owner: str, repo: str) -> Dict:
        """Fetch comprehensive repository data
        
        Args:
            owner: Repository owner
            repo: Repository name
            
        Returns:
            Dictionary containing repository data
        """
        # Get basic repository information
        repo_data = self.make_request(f"/repos/{owner}/{repo}")
        
        # Get additional data
        try:
            # Get contributors count
            contributors = self.make_request(f"/repos/{owner}/{repo}/contributors?per_page=1")
            repo_data['contributors_count'] = len(contributors) if isinstance(contributors, list) else 0
            
            # Get open pull requests count
            pulls = self.make_request(f"/repos/{owner}/{repo}/pulls?state=open&per_page=1")
            repo_data['open_prs_count'] = len(pulls) if isinstance(pulls, list) else 0
            
            # Get commit activity for last 30 days
            commit_activity = self.get_commit_activity(owner, repo)
            repo_data['commit_activity'] = commit_activity
            
            # Get recent issues and PRs for activity analysis
            recent_issues = self.get_recent_issues(owner, repo)
            recent_prs = self.get_recent_pulls(owner, repo)
            
            repo_data['recent_issues'] = recent_issues
            repo_data['recent_prs'] = recent_prs
            
        except Exception as e:
            # Continue with basic data if additional requests fail
            print(f"Warning: Could not fetch additional data: {e}")
            repo_data['contributors_count'] = 0
            repo_data['open_prs_count'] = 0
            repo_data['commit_activity'] = []
            repo_data['recent_issues'] = []
            repo_data['recent_prs'] = []
        
        return repo_data
    
    def get_commit_activity(self, owner: str, repo: str) -> List[Dict]:
        """Get commit activity for the last 30 days
        
        Args:
            owner: Repository owner
            repo: Repository name
            
        Returns:
            List of commit data for last 30 days
        """
        try:
            # Get commits from last 30 days
            since_date = (datetime.now() - timedelta(days=30)).isoformat()
            commits = self.make_request(f"/repos/{owner}/{repo}/commits?since={since_date}&per_page=100")
            
            if not isinstance(commits, list):
                return []
            
            # Process commit data by date
            commit_by_date = {}
            for commit in commits:
                if commit.get('commit', {}).get('author', {}).get('date'):
                    commit_date = commit['commit']['author']['date'][:10]  # Get YYYY-MM-DD
                    commit_by_date[commit_date] = commit_by_date.get(commit_date, 0) + 1
            
            # Convert to list format for charting
            activity_data = []
            for i in range(30):
                date = (datetime.now() - timedelta(days=29-i)).strftime('%Y-%m-%d')
                activity_data.append({
                    'date': date,
                    'commits': commit_by_date.get(date, 0)
                })
            
            return activity_data
            
        except Exception:
            return []
    
    def get_recent_issues(self, owner: str, repo: str, days: int = 30) -> List[Dict]:
        """Get recent issues for activity analysis
        
        Args:
            owner: Repository owner
            repo: Repository name
            days: Number of days to look back
            
        Returns:
            List of recent issues
        """
        try:
            since_date = (datetime.now() - timedelta(days=days)).isoformat()
            issues = self.make_request(f"/repos/{owner}/{repo}/issues?since={since_date}&per_page=100")
            
            if not isinstance(issues, list):
                return []
            
            # Filter out pull requests (GitHub API includes PRs in issues)
            return [issue for issue in issues if 'pull_request' not in issue]
            
        except Exception:
            return []
    
    def get_recent_pulls(self, owner: str, repo: str, days: int = 30) -> List[Dict]:
        """Get recent pull requests for activity analysis
        
        Args:
            owner: Repository owner
            repo: Repository name
            days: Number of days to look back
            
        Returns:
            List of recent pull requests
        """
        try:
            # Get all PRs (open and closed) from last 30 days
            pulls_open = self.make_request(f"/repos/{owner}/{repo}/pulls?state=open&per_page=50")
            pulls_closed = self.make_request(f"/repos/{owner}/{repo}/pulls?state=closed&per_page=50")
            
            all_pulls = []
            if isinstance(pulls_open, list):
                all_pulls.extend(pulls_open)
            if isinstance(pulls_closed, list):
                all_pulls.extend(pulls_closed)
            
            # Filter by date
            cutoff_date = datetime.now() - timedelta(days=days)
            recent_pulls = []
            
            for pr in all_pulls:
                if pr.get('created_at'):
                    created_date = datetime.fromisoformat(pr['created_at'].replace('Z', '+00:00'))
                    if created_date >= cutoff_date:
                        recent_pulls.append(pr)
            
            return recent_pulls
            
        except Exception:
            return []
