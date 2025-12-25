import pytest

from src.shared.http.http_response import HttpResponse


class TestHttpResponse:
    def test_event_parsing(self):
        response = HttpResponse()
        response.set("custom-header", "my-custom-header")
        response.cookie("my-cookie=nham-nham")
        result = response.status(202).json(({"message": "Hello World!"}))

        assert result == {
            "statusCode": 202,
            "headers": {"custom-header": "my-custom-header", "Content-Type": "application/json"},
            "cookies": ["my-cookie=nham-nham"],
            "body": '{"message": "Hello World!"}',
            "isBase64Encoded": False
        }


if __name__ == "__main__":
    pytest.main()
