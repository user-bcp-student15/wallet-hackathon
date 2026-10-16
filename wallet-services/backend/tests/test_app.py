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

    def test_payment_history_forwards_wallet_id_query(self):
        response_body = b'[]'
        upstream_response = unittest.mock.Mock()
        upstream_response.read.return_value = response_body
        upstream_response.getcode.return_value = 200
        upstream_response.headers = {"Content-Type": "application/json"}

        with patch("app.urlopen", return_value=upstream_response) as mocked_urlopen:
            response = self.client.get("/payments?walletId=wallet-demo")

        forwarded_request = mocked_urlopen.call_args.args[0]
        self.assertEqual(forwarded_request.full_url, f"{DEFAULT_W1_BASE_URL}/payments?walletId=wallet-demo")
        self.assertEqual(forwarded_request.get_method(), "GET")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, response_body)

    def test_create_payment_forwards_body_and_idempotency_key(self):
        request_body = b'{"walletId":"wallet-demo","recipient":"contact-demo","amountCents":1500}'
        response_body = b'{"id":"payment-1","status":"PENDING"}'
        upstream_response = unittest.mock.Mock()
        upstream_response.read.return_value = response_body
        upstream_response.getcode.return_value = 202
        upstream_response.headers = {"Content-Type": "application/json"}

        with patch("app.urlopen", return_value=upstream_response) as mocked_urlopen:
            response = self.client.post(
                "/payments",
                data=request_body,
                content_type="application/json",
                headers={"Idempotency-Key": "wallet-demo-payment-001"},
            )

        forwarded_request = mocked_urlopen.call_args.args[0]
        self.assertEqual(forwarded_request.full_url, f"{DEFAULT_W1_BASE_URL}/payments")
        self.assertEqual(forwarded_request.get_method(), "POST")
        self.assertEqual(forwarded_request.data, request_body)
        self.assertEqual(
            forwarded_request.get_header("Idempotency-key"),
            "wallet-demo-payment-001",
        )
        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.data, response_body)

    def test_get_payment_forwards_payment_id(self):
        self.assert_get_proxy_forwards(
            "/payments/payment-001", "/payments/payment-001"
        )

    def test_payment_receipt_forwards_payment_id(self):
        self.assert_get_proxy_forwards(
            "/payments/payment-001/receipt", "/payments/payment-001/receipt"
        )

    def test_provider_payment_forwards_payment_id(self):
        self.assert_get_proxy_forwards(
            "/provider/payments/payment-001",
            "/provider/payments/payment-001",
        )

    def test_create_qr_forwards_body(self):
        request_body = b'{"merchantId":"merchant-demo","amountCents":2200}'
        self.assert_post_proxy_forwards("/qrs", request_body, 201)

    def test_resolve_qr_forwards_payload(self):
        request_body = b'{"payload":"qrmock:qr-001"}'
        self.assert_post_proxy_forwards("/qrs/resolve", request_body, 200)

    def assert_get_proxy_forwards(self, route, upstream_path):
        response_body = b'{"status":"SUCCEEDED"}'
        upstream_response = unittest.mock.Mock()
        upstream_response.read.return_value = response_body
        upstream_response.getcode.return_value = 200
        upstream_response.headers = {"Content-Type": "application/json"}

        with patch("app.urlopen", return_value=upstream_response) as mocked_urlopen:
            response = self.client.get(route)

        forwarded_request = mocked_urlopen.call_args.args[0]
        self.assertEqual(
            forwarded_request.full_url, f"{DEFAULT_W1_BASE_URL}{upstream_path}"
        )
        self.assertEqual(forwarded_request.get_method(), "GET")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, response_body)

    def assert_post_proxy_forwards(self, path, request_body, status):
        response_body = b'{"id":"mock-resource-001"}'
        upstream_response = unittest.mock.Mock()
        upstream_response.read.return_value = response_body
        upstream_response.getcode.return_value = status
        upstream_response.headers = {"Content-Type": "application/json"}

        with patch("app.urlopen", return_value=upstream_response) as mocked_urlopen:
            response = self.client.post(
                path, data=request_body, content_type="application/json"
            )

        forwarded_request = mocked_urlopen.call_args.args[0]
        self.assertEqual(forwarded_request.full_url, f"{DEFAULT_W1_BASE_URL}{path}")
        self.assertEqual(forwarded_request.get_method(), "POST")
        self.assertEqual(forwarded_request.data, request_body)
        self.assertEqual(response.status_code, status)
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