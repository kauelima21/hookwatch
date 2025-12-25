import pytest

from src.shared.http.http_request import HttpRequest
from tests.conftest import ReadMockFile


class TestHttpRequest:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.event = ReadMockFile("http_event_mock.json").mock_parsed

    def test_event_parsing(self):
        request = HttpRequest(self.event)
        assert request.method
        assert request.body
        assert request.headers
        assert request.query


if __name__ == "__main__":
    pytest.main()
