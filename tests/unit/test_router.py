import pytest

from src.shared.http.http_request import HttpRequest
from src.shared.http.http_response import HttpResponse
from src.shared.http.router import Router
from tests.conftest import ReadMockFile


class TestRouter:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.event = ReadMockFile("http_event_mock.json").mock_parsed

    def test_class_controller(self):
        class ClassController:
            def __init__(self, req, res):
                self.req = req
                self.res = res

            def index(self):
                return self.res.status(200).send("Hello World")

        router = Router()
        router.get("/users/{id}", ClassController, "index")

        response = router.dispatch(HttpRequest(self.event), HttpResponse())

        assert response["statusCode"] == 200
        assert response["body"] == "Hello World"

    def test_invoke_class_controller(self):
        class InvokeClassController:
            def __init__(self, req, res):
                self.req = req
                self.res = res

            def __call__(self):
                return self.res.status(200).send("Hello World")

        router = Router()
        router.get("/users/{id}", InvokeClassController)

        response = router.dispatch(HttpRequest(self.event), HttpResponse())

        assert response["statusCode"] == 200
        assert response["body"] == "Hello World"

    def test_method_controller(self):
        def method_controller(req, res):
            return res.status(200).send("Hello World")

        router = Router()
        router.get("/users/{id}", method_controller)

        response = router.dispatch(HttpRequest(self.event), HttpResponse())

        assert response["statusCode"] == 200
        assert response["body"] == "Hello World"

    def test_invalid_route(self):
        class ClassController:
            def __init__(self, req, res):
                self.req = req
                self.res = res

            def index(self):
                return self.res.status(200).send("Hello World")

        router = Router()
        router.get("/invalid-route", ClassController, "index")

        response = router.dispatch(HttpRequest(self.event), HttpResponse())

        assert response["statusCode"] == 404
        assert response["body"] == "Not Found"


if __name__ == "__main__":
    pytest.main()
