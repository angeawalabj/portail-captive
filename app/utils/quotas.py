from datetime import datetime, timedelta


def is_expired(expires_at):
    return bool(expires_at and datetime.utcnow() > expires_at)


def quota_time_exceeded(used_seconds: int, quota_seconds: int|None):
    return quota_seconds is not None and used_seconds >= quota_seconds


def quota_data_exceeded(used_bytes: int, quota_bytes: int|None):
    return quota_bytes is not None and used_bytes >= quota_bytes