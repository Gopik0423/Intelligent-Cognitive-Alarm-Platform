import os
import json
import redis
from datetime import timedelta
import psycopg2
from psycopg2.extras import RealDictCursor
import time

# --- Database Setup Setup ---
DB_URL = os.getenv("DATABASE_URL", "postgresql://app_user:app_password@localhost:5432/app_db")
redis_client = redis.Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"), decode_responses=True)

def get_db_connection():
    return psycopg2.connect(DB_URL, cursor_factory=RealDictCursor)

def fetch_user_from_db(user_id):
    """Fallback: fetch user directly from PostgreSQL"""
    print(f"Cache miss for {user_id}. Fetching from DB...")
    # Simulated long-running DB query
    time.sleep(1) 
    
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            # Optimize DB queries by using selective fetching instead of SELECT *
            cursor.execute("SELECT id, username, email FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            
    return user

# --- Redis Caching Setup & Optimization ---
def get_user_profile(user_id):
    """
    Implements Cache-Aside pattern using Redis.
    Check cache first, if present return.
    If not present, fetch from database, populate cache, and then return.
    """
    cache_key = f"user_profile:{user_id}"
    
    # 1. Try fetching from Redis
    cached_data = redis_client.get(cache_key)
    
    if cached_data:
        print(f"Cache hit for {user_id}")
        return json.loads(cached_data)
        
    # 2. On Cache miss, fetch from DB
    db_data = fetch_user_from_db(user_id)
    
    if db_data:
        # 3. Store the result in Redis with a TTL (Time-To-Live) for caching optimization
        # Use a TTL of 30 minutes to prevent stale data and optimize memory usage
        redis_client.setex(
            cache_key,
            timedelta(minutes=30),
            json.dumps(dict(db_data))  
        )
        
    return db_data

def invalidate_user_cache(user_id):
    """Utility to clear cache when data is updated."""
    cache_key = f"user_profile:{user_id}"
    redis_client.delete(cache_key)

# Example Usage
if __name__ == "__main__":
    test_id = "sample-uuid-123"
    print("First call:", get_user_profile(test_id))
    print("Second call:", get_user_profile(test_id))
