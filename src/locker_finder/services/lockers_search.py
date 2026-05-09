from ..utils.geo import find_distance

def find_nearest_lockers(lockers: list, user_lon: float, user_lat: float) -> list:
    """
    Find 10 nearest lockers
    """
    nearest_lockers = []
    distances = []

    for idx, locker in enumerate(lockers):
        distance = find_distance(user_lon, user_lat, locker["lon"], locker["lat"])

        if len(nearest_lockers) != 10:
            distances.append(distance)
            nearest_lockers.append(locker)
            continue

        min_dist = min(distances)

        if distance > min_dist:
            min_dist_idx = distances.index(min_dist)
            nearest_lockers.pop(min_dist_idx)
            nearest_lockers.append(locker)

    return nearest_lockers