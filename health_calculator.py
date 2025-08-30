from datetime import datetime, timedelta
from typing import Dict, List
import math

class HealthCalculator:
    """Calculate repository health score based on various metrics"""
    
    def __init__(self):
        """Initialize health calculator with scoring weights"""
        self.weights = {
            'activity': 0.25,      # Recent activity (commits, issues, PRs)
            'popularity': 0.25,    # Stars, forks, watchers
            'community': 0.25,     # Contributors, community engagement
            'maintenance': 0.25    # Issue resolution, update frequency
        }
    
    def calculate_health_score(self, repo_data: Dict) -> Dict:
        """Calculate comprehensive health score for repository
        
        Args:
            repo_data: Repository data from GitHub API
            
        Returns:
            Dictionary containing total score and component scores
        """
        # Calculate individual component scores
        activity_score = self._calculate_activity_score(repo_data)
        popularity_score = self._calculate_popularity_score(repo_data)
        community_score = self._calculate_community_score(repo_data)
        maintenance_score = self._calculate_maintenance_score(repo_data)
        
        # Calculate weighted total score
        total_score = (
            activity_score * self.weights['activity'] * 4 +
            popularity_score * self.weights['popularity'] * 4 +
            community_score * self.weights['community'] * 4 +
            maintenance_score * self.weights['maintenance'] * 4
        )
        
        return {
            'total_score': min(100, max(0, total_score)),
            'activity_score': activity_score,
            'popularity_score': popularity_score,
            'community_score': community_score,
            'maintenance_score': maintenance_score
        }
    
    def _calculate_activity_score(self, repo_data: Dict) -> float:
        """Calculate activity score based on recent commits, issues, and PRs
        
        Args:
            repo_data: Repository data
            
        Returns:
            Activity score (0-25)
        """
        score = 0
        
        # Recent commits (0-10 points)
        commit_activity = repo_data.get('commit_activity', [])
        total_commits = sum(day.get('commits', 0) for day in commit_activity)
        
        if total_commits > 0:
            # Logarithmic scaling for commits
            commit_score = min(10, math.log(total_commits + 1) * 2)
            score += commit_score
        
        # Recent issues activity (0-8 points)
        recent_issues = repo_data.get('recent_issues', [])
        if recent_issues:
            # Score based on issue activity
            issue_score = min(8, len(recent_issues) * 0.5)
            score += issue_score
        
        # Recent PR activity (0-7 points)
        recent_prs = repo_data.get('recent_prs', [])
        if recent_prs:
            # Score based on PR activity
            pr_score = min(7, len(recent_prs) * 0.7)
            score += pr_score
        
        return min(25, score)
    
    def _calculate_popularity_score(self, repo_data: Dict) -> float:
        """Calculate popularity score based on stars, forks, and watchers
        
        Args:
            repo_data: Repository data
            
        Returns:
            Popularity score (0-25)
        """
        stars = repo_data.get('stargazers_count', 0)
        forks = repo_data.get('forks_count', 0)
        watchers = repo_data.get('watchers_count', 0)
        
        # Logarithmic scaling for popularity metrics
        star_score = min(15, math.log(stars + 1) * 1.5) if stars > 0 else 0
        fork_score = min(6, math.log(forks + 1) * 1.2) if forks > 0 else 0
        watcher_score = min(4, math.log(watchers + 1) * 0.8) if watchers > 0 else 0
        
        return star_score + fork_score + watcher_score
    
    def _calculate_community_score(self, repo_data: Dict) -> float:
        """Calculate community score based on contributors and engagement
        
        Args:
            repo_data: Repository data
            
        Returns:
            Community score (0-25)
        """
        score = 0
        
        # Contributors (0-15 points)
        contributors = repo_data.get('contributors_count', 0)
        if contributors > 0:
            # Logarithmic scaling for contributors
            contributor_score = min(15, math.log(contributors) * 3)
            score += contributor_score
        
        # Stars to forks ratio (0-5 points)
        stars = repo_data.get('stargazers_count', 0)
        forks = repo_data.get('forks_count', 0)
        
        if forks > 0 and stars > 0:
            ratio = stars / forks
            # Good ratio is typically 2-10
            if 2 <= ratio <= 10:
                ratio_score = 5
            elif 1 <= ratio < 2 or 10 < ratio <= 20:
                ratio_score = 3
            else:
                ratio_score = 1
            score += ratio_score
        elif stars > 0:
            score += 2  # Some points for having stars without forks
        
        # Community features (0-5 points)
        has_wiki = repo_data.get('has_wiki', False)
        has_issues = repo_data.get('has_issues', False)
        has_projects = repo_data.get('has_projects', False)
        has_pages = repo_data.get('has_pages', False)
        
        feature_score = sum([has_wiki, has_issues, has_projects, has_pages]) * 1.25
        score += feature_score
        
        return min(25, score)
    
    def _calculate_maintenance_score(self, repo_data: Dict) -> float:
        """Calculate maintenance score based on updates and issue resolution
        
        Args:
            repo_data: Repository data
            
        Returns:
            Maintenance score (0-25)
        """
        score = 0
        
        # Last update recency (0-10 points)
        updated_at = repo_data.get('updated_at')
        if updated_at:
            try:
                update_date = datetime.fromisoformat(updated_at.replace('Z', '+00:00'))
                days_since_update = (datetime.now(update_date.tzinfo) - update_date).days
                
                if days_since_update <= 7:
                    score += 10
                elif days_since_update <= 30:
                    score += 8
                elif days_since_update <= 90:
                    score += 5
                elif days_since_update <= 365:
                    score += 2
                # No points for repos not updated in over a year
                
            except (ValueError, TypeError):
                pass
        
        # Issue resolution ratio (0-10 points)
        open_issues = repo_data.get('open_issues_count', 0)
        
        # Estimate total issues (this is approximate since we don't have closed issues count)
        # We use a heuristic based on repository age and activity
        if open_issues == 0:
            score += 10  # Perfect score for no open issues
        else:
            # Score based on reasonable issue count for repository size/activity
            stars = repo_data.get('stargazers_count', 0)
            expected_issues = max(1, stars * 0.01)  # Rough heuristic
            
            if open_issues <= expected_issues:
                score += 8
            elif open_issues <= expected_issues * 2:
                score += 5
            elif open_issues <= expected_issues * 5:
                score += 2
            # No points for too many open issues
        
        # Repository health indicators (0-5 points)
        archived = repo_data.get('archived', False)
        has_license = repo_data.get('license') is not None
        has_description = bool(repo_data.get('description'))
        
        if not archived:
            score += 2
        if has_license:
            score += 1.5
        if has_description:
            score += 1.5
        
        return min(25, score)
