import random

from locust import HttpUser, task


class GetMultipleUsers(HttpUser):
    @task
    def get_multiple(self):
        self.client.get(f"/users?limit=10&offset={random.randint(a=0, b=500000)}")
