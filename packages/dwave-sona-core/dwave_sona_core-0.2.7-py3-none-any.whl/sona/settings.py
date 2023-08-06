from typing import Any, Dict, Optional

from pydantic import BaseSettings, RedisDsn, root_validator


class Settings(BaseSettings):
    # Consumer settings
    SONA_CONSUMER_KAFKA_SETTING: Optional[Dict] = None
    SONA_CONSUMER_REDIS_URL: Optional[RedisDsn] = None
    SONA_CONSUMER_REDIS_GROUP: Optional[str] = "dwave.anonymous"

    # Producer settings
    SONA_PRODUCER_KAFKA_SETTING: Optional[Dict] = None
    SONA_PRODUCER_REDIS_URL: Optional[RedisDsn] = None

    # Storage settings
    SONA_STORAGE_DIR: str = "_tmp"
    SONA_STORAGE_SETTING: Dict = None
    SONA_STORAGE_BUCKET: str = "sona"
    SONA_STORAGE_LOCAL_ROOT: str = "_share"

    # Inferencer settings
    SONA_WORKER: str = "sona.workers.InferencerWorker"
    SONA_INFERENCER: str = None
    SONA_INFERENCER_TOPIC_PREFIX: str = "dwave.inferencer"

    @root_validator(pre=False)
    def load_settings(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        return values

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
