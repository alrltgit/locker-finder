from ..utils.geo import find_distance

class LockerSearch:
    def __init__(self, repository):
        self.repository = repository

    def find_nearest_lockers(self, user_lon: float, user_lat: float, limit: int = 10) -> list:
        """
        Find 10 nearest lockers
        """
        nearest_lockers = []
        distances = []

        lockers = self.repository.get_all_lockers()

        for idx, locker in enumerate(lockers):
            distance = find_distance(user_lon, user_lat, locker.lon, locker.lat)

            if len(nearest_lockers) < limit:
                distances.append(distance)
                nearest_lockers.append(locker)
                continue

            max_dist = max(distances)

            if distance < max_dist:
                max_dist_idx = distances.index(max_dist)
                nearest_lockers[max_dist_idx] = locker
                distances[max_dist_idx] = distance

        return nearest_lockers