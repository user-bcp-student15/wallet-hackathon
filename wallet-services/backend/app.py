import os
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from flask import Flask, Response, jsonify, request


DEFAULT_W1_BASE_URL = "https://bcp-wallet-mock.yefri.workers.dev/groups/5"
DEFAULT_W1_KYC_URL = f"{DEFAULT_W1_BASE_URL}/kyc/verifications"


def forward_to_mock(upstream_request, timeout_seconds):
    try:
        upstream_response = urlopen(upstream_request, timeout=timeout_seconds)
    except HTTPError as error:
        upstream_response = error
    except (URLError, TimeoutError):
        return jsonify(error="KYC_UNAVAILABLE"), 503

    try:
        body = upstream_response.read()
        status = upstream_response.getcode()
        content_type = upstream_response.headers.get(
            "Content-Type", "application/json"
        )
    finally:
        upstream_response.close()

    return Response(body, status=status, content_type=content_type)


def build_mock_request(base_url, path, method, include_query=False):
    url = f"{base_url.rstrip('/')}/{path.lstrip('/')}"
    if include_query and request.query_string:
        url = f"{url}?{request.query_string.decode('latin-1')}"

    headers = {
        "User-Agent": request.headers.get(
            "User-Agent", "Wallet-Hackathon-Backend/1.0"
        )
    }
    for name in ("Content-Type", "Idempotency-Key"):
        if name in request.headers:
            headers[name] = request.headers[name]

    body = request.get_data(cache=False) if method in {"POST", "PUT", "PATCH"} else None
    return Request(url, data=body, headers=headers, method=method)


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        W1_BASE_URL=os.environ.get("W1_BASE_URL", DEFAULT_W1_BASE_URL),
        W1_KYC_URL=os.environ.get("W1_KYC_URL", DEFAULT_W1_KYC_URL),
        W1_TIMEOUT_SECONDS=10,
    )
    if test_config:
        app.config.update(test_config)

    @app.post("/crear-wallet")
    def crear_wallet():
        upstream_request = Request(
            app.config["W1_KYC_URL"],
            data=request.get_data(cache=False),
            headers={
                "Content-Type": request.headers.get(
                    "Content-Type", "application/json"
                ),
                "User-Agent": request.headers.get(
                    "User-Agent", "Wallet-Hackathon-Backend/1.0"
                ),
            },
            method="POST",
        )
        return forward_to_mock(upstream_request, app.config["W1_TIMEOUT_SECONDS"])

    @app.get("/consultar-kyc/<verification_id>")
    def consultar_kyc(verification_id):
        verification_url = (
            f"{app.config['W1_KYC_URL'].rstrip('/')}/"
            f"{quote(verification_id, safe='')}"
        )
        upstream_request = Request(
            verification_url,
            headers={
                "User-Agent": request.headers.get(
                    "User-Agent", "Wallet-Hackathon-Backend/1.0"
                )
            },
            method="GET",
        )
        return forward_to_mock(upstream_request, app.config["W1_TIMEOUT_SECONDS"])

    @app.post("/resolver-decision/<verification_id>")
    def resolver_decision(verification_id):
        decision_url = (
            f"{app.config['W1_KYC_URL'].rstrip('/')}/"
            f"{quote(verification_id, safe='')}/decision"
        )
        upstream_request = Request(
            decision_url,
            data=request.get_data(cache=False),
            headers={
                "Content-Type": request.headers.get(
                    "Content-Type", "application/json"
                ),
                "User-Agent": request.headers.get(
                    "User-Agent", "Wallet-Hackathon-Backend/1.0"
                ),
            },
            method="POST",
        )
        return forward_to_mock(upstream_request, app.config["W1_TIMEOUT_SECONDS"])

    @app.get("/consulta-estado-saldos/<wallet_id>")
    def consulta_estado_saldos(wallet_id):
        wallet_url = (
            f"{app.config['W1_BASE_URL'].rstrip('/')}/wallets/"
            f"{quote(wallet_id, safe='')}"
        )
        upstream_request = Request(
            wallet_url,
            headers={
                "User-Agent": request.headers.get(
                    "User-Agent", "Wallet-Hackathon-Backend/1.0"
                )
            },
            method="GET",
        )
        return forward_to_mock(upstream_request, app.config["W1_TIMEOUT_SECONDS"])

    @app.get("/payments")
    def list_payments():
        upstream_request = build_mock_request(
            app.config["W1_BASE_URL"], "/payments", "GET", include_query=True
        )
        return forward_to_mock(upstream_request, app.config["W1_TIMEOUT_SECONDS"])

    @app.post("/payments")
    def create_payment():
        upstream_request = build_mock_request(
            app.config["W1_BASE_URL"], "/payments", "POST"
        )
        return forward_to_mock(upstream_request, app.config["W1_TIMEOUT_SECONDS"])

    @app.get("/payments/<payment_id>")
    def get_payment(payment_id):
        upstream_request = build_mock_request(
            app.config["W1_BASE_URL"],
            f"/payments/{quote(payment_id, safe='')}",
            "GET",
        )
        return forward_to_mock(upstream_request, app.config["W1_TIMEOUT_SECONDS"])

    @app.get("/payments/<payment_id>/receipt")
    def get_payment_receipt(payment_id):
        upstream_request = build_mock_request(
            app.config["W1_BASE_URL"],
            f"/payments/{quote(payment_id, safe='')}/receipt",
            "GET",
        )
        return forward_to_mock(upstream_request, app.config["W1_TIMEOUT_SECONDS"])

    @app.get("/provider/payments/<payment_id>")
    def get_provider_payment(payment_id):
        upstream_request = build_mock_request(
            app.config["W1_BASE_URL"],
            f"/provider/payments/{quote(payment_id, safe='')}",
            "GET",
        )
        return forward_to_mock(upstream_request, app.config["W1_TIMEOUT_SECONDS"])

    @app.post("/qrs")
    def create_qr():
        upstream_request = build_mock_request(
            app.config["W1_BASE_URL"], "/qrs", "POST"
        )
        return forward_to_mock(upstream_request, app.config["W1_TIMEOUT_SECONDS"])

    @app.post("/qrs/resolve")
    def resolve_qr():
        upstream_request = build_mock_request(
            app.config["W1_BASE_URL"], "/qrs/resolve", "POST"
        )
        return forward_to_mock(upstream_request, app.config["W1_TIMEOUT_SECONDS"])

    return app


if __name__ == "__main__":
    create_app().run()