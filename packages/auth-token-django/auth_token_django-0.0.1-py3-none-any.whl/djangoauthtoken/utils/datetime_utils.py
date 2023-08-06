from datetime import datetime

def get_epoch(dt=None) -> int:
    """
    :param dt: A datetime aware object
    :return: An int object reprsenting time in epoch in utc
    """
    if not dt:
        dt = datetime.utcnow()
    return int(dt.timestamp() * 10000)

