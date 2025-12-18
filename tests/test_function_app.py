import sys
import types
import unittest
from pathlib import Path


def _install_azure_functions_stub() -> None:
    """Provide a minimal azure.functions stub so tests can run offline.

    The real package is resolved via src/requirements.txt in Azure Functions,
    but local/unit tests shouldn't require PyPI access.
    """

    if "azure.functions" in sys.modules:
        return

    azure_mod = types.ModuleType("azure")
    functions_mod = types.ModuleType("azure.functions")

    class AuthLevel:
        ANONYMOUS = "ANONYMOUS"

    class HttpRequest:
        def __init__(self, *, method: str, url: str, headers: dict, params: dict, route_params: dict, body: bytes):
            self.method = method
            self.url = url
            self.headers = headers
            self.params = params
            self.route_params = route_params
            self._body = body

    class HttpResponse:
        def __init__(self, body: str, status_code: int = 200, headers=None, mimetype=None, charset: str = "utf-8"):
            self._body = body
            self.status_code = status_code
            self.headers = headers or {}
            self.mimetype = mimetype
            self.charset = charset

        def get_body(self) -> bytes:
            if isinstance(self._body, bytes):
                return self._body
            return str(self._body).encode(self.charset or "utf-8")

    class FunctionApp:
        def __init__(self, http_auth_level=None):
            self.http_auth_level = http_auth_level

        def route(self, *, route: str, methods=None):
            def decorator(fn):
                return fn

            return decorator

    functions_mod.AuthLevel = AuthLevel
    functions_mod.HttpRequest = HttpRequest
    functions_mod.HttpResponse = HttpResponse
    functions_mod.FunctionApp = FunctionApp

    azure_mod.functions = functions_mod
    sys.modules["azure"] = azure_mod
    sys.modules["azure.functions"] = functions_mod


_install_azure_functions_stub()

import azure.functions as func  # noqa: E402


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

import function_app  # noqa: E402


def _make_req(path: str, params: dict[str, str]) -> func.HttpRequest:
    return func.HttpRequest(
        method="GET",
        url=f"http://localhost{path}",
        headers={},
        params=params,
        route_params={},
        body=b"",
    )


class TestMultiply(unittest.TestCase):
    def test_multiply_ok(self):
        req = _make_req("/api/multiply", {"A": "3", "B": "4"})
        resp = function_app.multiply(req)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_body().decode("utf-8"), "12")

    def test_multiply_missing_a(self):
        req = _make_req("/api/multiply", {"B": "4"})
        resp = function_app.multiply(req)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_body().decode("utf-8"), "ERROR: Missing query parameter A")

    def test_multiply_invalid_b(self):
        req = _make_req("/api/multiply", {"A": "3", "B": "x"})
        resp = function_app.multiply(req)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_body().decode("utf-8"), "ERROR: Query parameter B must be an integer")


class TestDivide(unittest.TestCase):
    def test_divide_ok_trunc_toward_zero_pos(self):
        req = _make_req("/api/divide", {"A": "7", "B": "2"})
        resp = function_app.divide(req)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_body().decode("utf-8"), "3")

    def test_divide_ok_trunc_toward_zero_neg(self):
        req = _make_req("/api/divide", {"A": "-7", "B": "2"})
        resp = function_app.divide(req)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_body().decode("utf-8"), "-3")

    def test_divide_by_zero(self):
        req = _make_req("/api/divide", {"A": "7", "B": "0"})
        resp = function_app.divide(req)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_body().decode("utf-8"), "ERROR: Division by zero")

    def test_divide_missing_b(self):
        req = _make_req("/api/divide", {"A": "7"})
        resp = function_app.divide(req)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_body().decode("utf-8"), "ERROR: Missing query parameter B")


if __name__ == "__main__":
    unittest.main()
