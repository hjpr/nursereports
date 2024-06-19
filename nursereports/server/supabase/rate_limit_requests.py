from ..secrets import api_key, api_url
from functools import wraps

import datetime
import httpx
import json
import time


def rate_limit_supabase(table: str, entry_limit: int, time_limit: int):
    """
    Provides a rate limiter when making supabase calls. Allows wrapped
    func to execute if rate limit not hit, otherwise returns dict. This
    follows expected behavior where wrapped func returns dict of same
    pattern.

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
        def wrapper(*args, **kwargs):
            access_token = args[0]
            current_unix_time = time.time()
            exclusion_period = current_unix_time - (time_limit * 60)
            exclusion_obj = datetime.datetime.utcfromtimestamp(exclusion_period)
            exclusion_tz = exclusion_obj.strftime("%Y-%m-%d %H:%M:%S %z")
            url = f"{api_url}/rest/v1/{table}?" + f"created_at=gte.{exclusion_tz}"
            headers = {
                "apikey": api_key,
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "Range": f"0-{entry_limit - 1}",
            }
            response = httpx.get(
                url=url,
                headers=headers,
            )
            if response.is_success:
                entries = json.loads(response.content)
                if entries:
                    return {
                        "success": False,
                        "status": f"""Too many submissions. The limit is
                            {entry_limit} submission(s) per {time_limit}
                            minute(s).""",
                    }
                else:
                    return func(*args, **kwargs)
            else:
                return {
                    "success": False,
                    "status": f"{response.status_code} - {response.reason_phrase}",
                }

        return wrapper

    return decorator
