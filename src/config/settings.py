"""
Configuration settings for Music News Analyzer
"""
import os
from pathlib import Path


class Settings:
    """Application settings"""
    
    # Database Configuration
    mongodb_url: str = os.getenv("MONGODB_URL", "mongodb://admin:admin123@localhost:27017/music_news_db")
    mongodb_database: str = os.getenv("MONGODB_DATABASE", "music_news_db")
    
    # Scraping Configuration
    user_agent: str = os.getenv("USER_AGENT", "MusicNewsAnalyzer/1.0")
    request_delay: float = float(os.getenv("REQUEST_DELAY", "2.0"))
    max_concurrent_requests: int = int(os.getenv("MAX_CONCURRENT_REQUESTS", "5"))
    retry_attempts: int = int(os.getenv("RETRY_ATTEMPTS", "3"))
    
    # Data Processing
    min_article_length: int = int(os.getenv("MIN_ARTICLE_LENGTH", "100"))
    max_articles_per_source: int = int(os.getenv("MAX_ARTICLES_PER_SOURCE", "50"))
    
    # Development
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"


def get_project_root() -> Path:
    """Get project root directory"""
    return Path(__file__).parent.parent


# Global settings instance
settings = Settings()


if __name__ == "__main__":
    print("Settings loaded successfully:")
    print(f"MongoDB URL: {settings.mongodb_url}")
    print(f"Database: {settings.mongodb_database}")