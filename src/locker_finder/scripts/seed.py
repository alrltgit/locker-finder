from src.locker_finder.clients.inpost_client import InPostClient

inpost_client = InPostClient()
print("\033[32mAdding data to the database. Please wait...\033[0m")
inpost_client.sync_lockers()
print("\033[32mData has been added\033[0m")
