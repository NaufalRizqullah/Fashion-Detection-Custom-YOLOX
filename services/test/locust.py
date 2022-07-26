

from services.test.locust import HttpUser, SequentialTaskSet, task


class YoloxTask(SequentialTaskSet):

    @task
    def detection(self):
        with open("test_image.jpeg", "rb") as image:
            self.client.post(
                "/v1/detect",
                files = {"im": image}
            )

class YoloxTaskV2(SequentialTaskSet):

    @task
    def detection(self):
        with open("../assets/test_image.jpeg", "rb") as image:
            self.client.post(
                "/v1/detectv2",
                files = {"im": image}
            )

class LoadTester(HttpUser):
    # define a host/web ti hit
    host = "https://simple-fashion-detection.herokuapp.com"

    # identify task according to class we created before, this mean we can pass more than one
    tasks = [YoloxTask, YoloxTaskV2]

