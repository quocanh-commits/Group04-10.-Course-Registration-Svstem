from datetime import timezone, timedelta

# Việt Nam không có giờ mùa hè nên dùng múi giờ cố định, không cần thư viện tzdata
VN_TZ = timezone(timedelta(hours=7))


def to_local(dt):
    if dt is None:
        return None
    return dt.astimezone(VN_TZ) if dt.tzinfo else dt


def schedule_label(dt):
    local = to_local(dt)
    return f"{local:%A} · {local:%H:%M}" if local else ""


def slot_key(dt):
    """Hai lớp trùng lịch khi cùng thứ trong tuần và cùng giờ bắt đầu."""
    local = to_local(dt)
    return (local.weekday(), local.hour, local.minute)
