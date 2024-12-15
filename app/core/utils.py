import uuid


def generate_unique_id() -> str:
    return uuid.uuid4().hex


def format_datetime(dt) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")
