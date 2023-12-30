import os
import time
import pymongo

# Configuration from environment variables
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://dbstorage:27017')
DB_NAME = os.getenv('DB_NAME', 'cloneDetector')
INTERVAL = int(os.getenv('INTERVAL', '60'))

def main():
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DB_NAME]

    while True:

        print("Fetching new data...")

        files_count = db["files"].count_documents({})
        chunks_count = db["chunks"].count_documents({})
        candidates_count = db["candidates"].count_documents({})
        clones_count = db["clones"].count_documents({})

        latest_status = db["statusUpdates"].find().sort("_id", pymongo.DESCENDING).limit(1)

        print(f"Files: {files_count}, Chunks: {chunks_count}, Candidates: {candidates_count}, Clones: {clones_count}")
        for status in latest_status:
            print(f"Latest Status Update: {status['message']} at {status['timestamp']}")

        print("\n--- Done. Next fetch in " INTERVAL " s ---\n")

        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
