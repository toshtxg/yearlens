import os
from typing import Any


def get_supabase_client() -> Any | None:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        return None

    from supabase import create_client

    return create_client(url, key)

