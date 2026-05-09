import math

def find_distance(user_lon: float, user_lat: float, locker_lon: float, locker_lat: float) -> float:
    """
    Find distance from the user and the locker using Haversine formular
    """
    R = 6371

    phi1 = math.radians(user_lat)
    phi2 = math.radians(locker_lat)

    lat_dif = math.radians(locker_lat - user_lat)
    lon_dif = math.radians(locker_lon - user_lon)

    a = (
            math.sin(lat_dif / 2) ** 2
            + math.cos(phi1) * math.cos(phi2)
            * math.sin(lon_dif / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c