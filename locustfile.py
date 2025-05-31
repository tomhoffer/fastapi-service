import random

from locust import HttpUser, task


class GetRecordByIdUser(HttpUser):
    # Assuming record IDs exist in a range, e.g., 1 to 500,000
    # Adjust MIN_ID and MAX_ID based on your actual data if known.
    MIN_ID = 1
    MAX_ID = 10_000_000

    @task
    def get_random_record_by_id(self):
        if self.MAX_ID < self.MIN_ID:
            # Avoids error in random.randint if MAX_ID is not set appropriately
            print("Warning: MAX_ID is less than MIN_ID in Locust script. Skipping task.")
            return
            
        record_id = random.randint(self.MIN_ID, self.MAX_ID)
        self.client.get(f"/record/{record_id}", name="/record/[id]")
