import io
import unittest
from unittest.mock import patch
from urllib.error import HTTPError, URLError

from app import DEFAULT_W1_BASE_URL, DEFAULT_W1_KYC_URL, create_app


class WalletEndpointTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(
            {
                "TESTING": True,
                "W1_BASE_URL": DEFAULT_W1_BASE_URL,
                "W1_KYC_URL": DEFAULT_W1_KYC_URL,
            }
        )
        self.client = self.app.test_client()

    def test_forwards_request_and_returns_w1_success_unchanged(self):
        request_body = b'{"documentType":"TEST","document":"TEST-001"}'
        response_body = b'{"id":"verification-1","wallet_id":"wallet-1","scenario":"APPROVED","status":"ACTIVE"}'
        upstream_response = unittest.mock.Mock()
        upstream_response.read.return_value = response_body
        upstream_response.getcode.return_value = 201
        upstream_response.headers = {"Content-Type": "application/json"}

        with patch("app.urlopen", return_value=upstream_response) as mocked_urlopen:
            response = self.client.post(
                "/crear-wallet",
                data=request_body,
                content_type="application/json",
                headers={"User-Agent": "test-client/1.0"},
            )

        forwarded_request = mocked_urlopen.call_args.args[0]
        self.assertEqual(forwarded_request.full_url, DEFAULT_W1_KYC_URL)
        self.assertEqual(forwarded_request.get_method(), "POST")
        self.assertEqual(forwarded_request.data, request_body)
        self.assertEqual(
            forwarded_request.get_header("User-agent"), "test-client/1.0"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, response_body)

    def test_returns_w1_http_errors_unchanged(self):
        error_body = b'{"error":"INVALID_DOCUMENT"}'
        upstream_error = HTTPError(
            DEFAULT_W1_KYC_URL,
            400,
            "Bad Request",
            {"Content-Type": "application/json"},
            io.BytesIO(error_body),
        )

        with patch("app.urlopen", side_effect=upstream_error):
            response = self.client.post(
                "/crear-wallet",
                json={"documentType": "TEST", "document": "TEST-001"},
            )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, error_body)

    def test_get_forwards_id_and_returns_w1_success_unchanged(self):
        response_body = b'{"id":"verification-1","wallet_id":"wallet-1","scenario":"APPROVED","status":"ACTIVE"}'
        upstream_response = unittest.mock.Mock()
        upstream_response.read.return_value = response_body
        upstream_response.getcode.return_value = 200
        upstream_response.headers = {"Content-Type": "application/json"}

        with patch("app.urlopen", return_value=upstream_response) as mocked_urlopen:
            response = self.client.get(
                "/consultar-kyc/verification-1",
                headers={"User-Agent": "test-client/1.0"},
            )

        forwarded_request = mocked_urlopen.call_args.args[0]
        self.assertEqual(
            forwarded_request.full_url,
            f"{DEFAULT_W1_KYC_URL}/verification-1",
        )
        self.assertEqual(forwarded_request.get_method(), "GET")
        self.assertEqual(forwarded_request.get_header("User-agent"), "test-client/1.0")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, response_body)

    def test_get_returns_w1_not_found_unchanged(self):
        verification_url = f"{DEFAULT_W1_KYC_URL}/missing-id"
        error_body = b'{"error":"NOT_FOUND"}'
        upstream_error = HTTPError(
            verification_url,
            404,
            "Not Found",
            {"Content-Type": "application/json"},
            io.BytesIO(error_body),
        )

        with patch("app.urlopen", side_effect=upstream_error):
            response = self.client.get("/consultar-kyc/missing-id")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, error_body)

    def test_decision_forwards_id_and_body_to_w1(self):
        request_body = b'{"decision":"ACTIVE"}'
        response_body = b'{"id":"verification-1","wallet_id":"wallet-1","scenario":"MANUAL_REVIEW","status":"ACTIVE"}'
        upstream_response = unittest.mock.Mock()
        upstream_response.read.return_value = response_body
        upstream_response.getcode.return_value = 200
        upstream_response.headers = {"Content-Type": "application/json"}

        with patch("app.urlopen", return_value=upstream_response) as mocked_urlopen:
            response = self.client.post(
                "/resolver-decision/verification-1",
                data=request_body,
                content_type="application/json",
                headers={"User-Agent": "test-client/1.0"},
            )

        forwarded_request = mocked_urlopen.call_args.args[0]
        self.assertEqual(
            forwarded_request.full_url,
            f"{DEFAULT_W1_KYC_URL}/verification-1/decision",
        )
        self.assertEqual(forwarded_request.get_method(), "POST")
        self.assertEqual(forwarded_request.data, request_body)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, response_body)

    def test_wallet_balance_forwards_id_and_returns_w1_response(self):
        response_body = b'{"id":"wallet-1","status":"ACTIVE","balance":100000,"reserved":0,"available":100000,"currency":"PEN"}'
        upstream_response = unittest.mock.Mock()
        upstream_response.read.return_value = response_body
        upstream_response.getcode.return_value = 200
        upstream_response.headers = {"Content-Type": "application/json"}

        with patch("app.urlopen", return_value=upstream_response) as mocked_urlopen:
            response = self.client.get("/consulta-estado-saldos/wallet-1")

        forwarded_request = mocked_urlopen.call_args.args[0]
        self.assertEqual(
            forwarded_request.full_url,
            f"{DEFAULT_W1_BASE_URL}/wallets/wallet-1",
        )
        self.assertEqual(forwarded_request.get_method(), "GET")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, response_body)

    def test_maps_provider_unavailability_to_documented_error(self):
        with patch("app.urlopen", side_effect=URLError("provider unavailable")):
            response = self.client.post(
                "/crear-wallet",
                json={"documentType": "TEST", "document": "TEST-001"},
            )

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.get_json(), {"error": "KYC_UNAVAILABLE"})


if __name__ == "__main__":
    unittest.main()