from ..utils.geo import find_distance

def find_nearest_lockers(lockers: list, user_lon: float, user_lat: float) -> list:
    """
    Find 10 nearest lockers
    """
    nearest_lockers = []
    distances = []

    for idx, locker in enumerate(lockers):
        distance = find_distance(user_lon, user_lat, locker["lon"], locker["lat"])

        if len(nearest_lockers) < 5:
            distances.append(distance)
            nearest_lockers.append(locker)
            continue

        max_dist = max(distances)

        if distance < max_dist:
            max_dist_idx = distances.index(max_dist)
            nearest_lockers[max_dist_idx] = locker
            distances[max_dist_idx] = distance

    return nearest_lockers