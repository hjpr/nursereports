
from dotenv import load_dotenv
from functools import wraps
from loguru import logger
from supabase import Client, create_client

import datetime
import time
import os

load_dotenv()
api_url: str = os.getenv("SUPABASE_URL")
api_key: str = os.getenv("SUPABASE_ANON_KEY")
jwt_key: str = os.getenv("SUPABASE_JWT_KEY")
supabase: Client = create_client(api_url, api_key)

def rate_limit(
        table: str,
        entry_limit: int,
        time_limit: int,
        ):
    """
    Provides a rate limiter when making supabase calls. Allows request
    to continue if rate limit not met, otherwise returns a dict with
    explanation of failure.
    
    Args:
        table: target table to limit
        entry_limit: number of entries allowed within time limit
        time_limit: timeout in minutes
    
    Returns:
        dict:
            success: bool
            status: user-readable reason for failure
    """
    def decorator(func):
        @wraps(func)
        def wrapper(data, *args, **kwargs):
            # Get unix time now
            current_unix_time = time.time()

            # Subtract time limit to search for entries within period
            exclusion_period = current_unix_time - (time_limit * 60)

            # Convert unix time to datetime object
            exclusion_obj = datetime.datetime.utcfromtimestamp(
                exclusion_period
            )

            # Convert datetime obj to PostgreSQL format
            exclusion_tz = exclusion_obj.strftime(
                "%Y-%m-%d %H:%M:%S %z"
            )

            response = supabase.from_(table).select('*')\
                .eq('user_id', data['user_id'])\
                .gte('created_at', exclusion_tz)\
                .order('created_at', desc=True)\
                .limit(entry_limit)
            if response['data']:
                logger.critical("Rate limit exceeded!")
                return {
                    "success": False,
                    "status": f"""Too many submissions. The limit is
                        {entry_limit} submission(s) per {time_limit * 60}
                        minutes."""
                }
            else:
                return func(*args, **kwargs)
        return wrapper
    return decorator