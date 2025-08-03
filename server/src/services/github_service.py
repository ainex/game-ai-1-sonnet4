"""GitHub service for MCP (Model Context Protocol) integration."""

import os
import logging
import base64
from pathlib import Path
from functools import lru_cache
from typing import Optional, Dict, Any

# Set up logging first
logger = logging.getLogger(__name__)

# Secure environment loading
try:
    from dotenv import load_dotenv
    # Load .env from project root (3 levels up from this file)
    project_root = Path(__file__).parent.parent.parent.parent
    env_path = project_root / ".env"
    if env_path.exists():
        load_dotenv(env_path, override=False)  # Don't override existing env vars
        logger.info(f"✅ Loaded environment from {env_path}")
    else:
        logger.info("ℹ️ No .env file found, using system environment variables")
except ImportError:
    logger.warning("⚠️ python-dotenv not available, using system environment variables only")

try:
    import requests
    logger.info("✅ Requests library available for GitHub API")
except ImportError:
    logger.warning("⚠️ Requests library not available")
    requests = None


class GitHubService:
    """Service for GitHub API integration for MCP development."""

    def __init__(self) -> None:
        if requests is None:
            logger.warning("⚠️ GitHub service initialized without requests library")
            self._api_key = None
            self._base_url = "https://api.github.com"
        else:
            try:
                api_key = os.getenv("GITHUB_API_KEY")
                
                # Secure API key validation
                if not api_key:
                    logger.warning("⚠️ GITHUB_API_KEY not found - using mock mode")
                    self._api_key = None
                elif api_key == "mock_key_for_testing":
                    logger.warning("⚠️ Using mock API key - using mock mode")
                    self._api_key = None
                elif len(api_key) < 20:  # Basic validation
                    logger.error("❌ GITHUB_API_KEY appears invalid (too short) - using mock mode")
                    self._api_key = None
                elif not api_key.startswith("ghp_"):
                    logger.error("❌ GITHUB_API_KEY appears invalid (wrong format) - using mock mode")
                    self._api_key = None
                else:
                    # Mask API key in logs for security
                    masked_key = f"{api_key[:10]}...{api_key[-4:]}"
                    logger.info(f"🔑 Using GitHub API key: {masked_key}")
                    
                    self._api_key = api_key
                    self._base_url = "https://api.github.com"
                    logger.info("✅ GitHub service initialized successfully")
                    
            except Exception as e:
                logger.error(f"❌ GitHub service initialization failed: {e}")
                self._api_key = None

    def _get_headers(self) -> Dict[str, str]:
        """Get headers for GitHub API requests."""
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "AI-Gaming-Assistant/1.0"
        }
        if self._api_key:
            headers["Authorization"] = f"token {self._api_key}"
        return headers

    def get_repository_info(self, owner: str, repo: str) -> Optional[Dict[str, Any]]:
        """
        Get repository information for MCP context.
        
        Args:
            owner: Repository owner (username or organization)
            repo: Repository name
            
        Returns:
            Repository information or None if failed
        """
        logger.info(f"🔍 Getting repository info: {owner}/{repo}")
        
        if not self._api_key:
            logger.warning("⚠️ GitHub API key not available - returning mock data")
            return {
                "name": repo,
                "full_name": f"{owner}/{repo}",
                "description": "Mock repository for MCP development",
                "language": "Python",
                "stargazers_count": 42,
                "forks_count": 7,
                "updated_at": "2024-01-01T00:00:00Z"
            }
        
        try:
            url = f"{self._base_url}/repos/{owner}/{repo}"
            response = requests.get(url, headers=self._get_headers(), timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ Retrieved repository info for {owner}/{repo}")
                return data
            elif response.status_code == 404:
                logger.error(f"❌ Repository {owner}/{repo} not found")
                return None
            else:
                logger.error(f"❌ GitHub API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Failed to get repository info: {e}")
            return None

    def get_workflow_runs(self, owner: str, repo: str, workflow_id: str = None) -> Optional[list]:
        """
        Get workflow runs for MCP development context.
        
        Args:
            owner: Repository owner
            repo: Repository name
            workflow_id: Specific workflow ID (optional)
            
        Returns:
            List of workflow runs or None if failed
        """
        logger.info(f"🔍 Getting workflow runs: {owner}/{repo}")
        
        if not self._api_key:
            logger.warning("⚠️ GitHub API key not available - returning mock data")
            return [
                {
                    "id": 123456,
                    "name": "Mock Workflow",
                    "status": "completed",
                    "conclusion": "success",
                    "created_at": "2024-01-01T00:00:00Z"
                }
            ]
        
        try:
            if workflow_id:
                url = f"{self._base_url}/repos/{owner}/{repo}/actions/workflows/{workflow_id}/runs"
            else:
                url = f"{self._base_url}/repos/{owner}/{repo}/actions/runs"
            
            response = requests.get(url, headers=self._get_headers(), timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ Retrieved {len(data.get('workflow_runs', []))} workflow runs")
                return data.get('workflow_runs', [])
            else:
                logger.error(f"❌ GitHub API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Failed to get workflow runs: {e}")
            return None

    def create_mcp_context(self, owner: str, repo: str) -> Dict[str, Any]:
        """
        Create MCP context from GitHub repository data.
        
        Args:
            owner: Repository owner
            repo: Repository name
            
        Returns:
            MCP context dictionary
        """
        logger.info(f"🤖 Creating MCP context for {owner}/{repo}")
        
        repo_info = self.get_repository_info(owner, repo)
        workflow_runs = self.get_workflow_runs(owner, repo)
        
        mcp_context = {
            "repository": repo_info,
            "workflows": workflow_runs,
            "mcp_version": "1.0",
            "context_type": "github_repository",
            "timestamp": "2024-01-01T00:00:00Z"
        }
        
        logger.info(f"✅ MCP context created with {len(mcp_context)} sections")
        return mcp_context


@lru_cache(maxsize=1)
def get_github_service() -> "GitHubService":
    """Cached service instance."""
    return GitHubService() 