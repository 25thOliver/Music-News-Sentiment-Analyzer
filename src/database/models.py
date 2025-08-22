"""
MongoDB models for Music News Analyzer
Defines document schemas and data validation
"""
from datetime import datetime, timezone
from typing import Optional, Dict, List, Any
from pydantic import BaseModel, Field, validator
from bson import ObjectId
import hashlib


class PyObjectId(ObjectId):
    """Custom ObjectId type for Pydantic models"""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class SentimentScore(BaseModel):
    """Sentiment analysis results"""
    compound: float = Field(..., ge=-1.0, le=1.0)
    positive: float = Field(..., ge=0.0, le=1.0)
    negative: float = Field(..., ge=0.0, le=1.0)
    neutral: float = Field(..., ge=0.0, le=1.0)
    analyzer: str = Field(default="vader")


class ArticleMetadata(BaseModel):
    """Additional article metadata"""
    word_count: Optional[int] = None
    read_time_minutes: Optional[int] = None
    language: Optional[str] = "en"
    tags: List[str] = Field(default_factory=list)
    genre: Optional[str] = None
    artist_mentions: List[str] = Field(default_factory=list)
    album_mentions: List[str] = Field(default_factory=list)


class SourceInfo(BaseModel):
    """Information about the article source"""
    name: str
    section: Optional[str] = None
    base_url: str
    crawl_timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Article(BaseModel):
    """Main article document model"""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    
    # Core content
    title: str = Field(..., min_length=1, max_length=500)
    content: str = Field(..., min_length=50)
    summary: Optional[str] = Field(None, max_length=1000)
    
    # Article metadata  
    author: Optional[str] = None
    published_date: Optional[datetime] = None
    url: str
    url_hash: str
    
    # Source information
    source: SourceInfo
    
    # Analysis results
    sentiment: Optional[SentimentScore] = None
    metadata: ArticleMetadata = Field(default_factory=ArticleMetadata)
    
    # Processing timestamps
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None
    processed_at: Optional[datetime] = None
    
    # Processing status
    processing_status: str = Field(default="raw")
    processing_errors: List[str] = Field(default_factory=list)

    @validator('url_hash', pre=True, always=True)
    def generate_url_hash(cls, v, values):
        """Generate URL hash if not provided"""
        if v is None and 'url' in values:
            return hashlib.md5(values['url'].encode()).hexdigest()
        return v

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: str}


# Collection names
ARTICLES_COLLECTION = "articles"
CRAWL_SESSIONS_COLLECTION = "crawl_sessions" 
PROCESSING_STATS_COLLECTION = "processing_stats"


if __name__ == "__main__":
    # Test model creation
    article = Article(
        title="Test Article",
        content="This is a test article content for the music news analyzer.",
        url="https://example.com/test-article",
        source=SourceInfo(
            name="Test Source",
            base_url="https://example.com"
        )
    )
    
    print("✅ Article model validation passed")
    print(f"Generated URL hash: {article.url_hash}")
    print(f"Created at: {article.created_at}")