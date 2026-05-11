"""Smoke tests for the Python SDK. Run with: pytest sdk/python/tests/"""
import pytest
from viridis_mcp_client import ViridisMCP, ViridisMCPError
from viridis_mcp_client.types import InjectionDetectResult


def test_imports():
    from viridis_mcp_client import (
        ViridisMCP,
        AsyncViridisMCP,
        ViridisMCPError,
        InjectionDetectInput,
        InjectionDetectResult,
        CanonScanInput,
        CanonScanResult,
        MaxwellChallengeInput,
        MaxwellChallengeResult,
    )
    assert ViridisMCP is not None


def test_client_initialization():
    v = ViridisMCP(api_key="vrd_test_dummy")
    assert v._api_key == "vrd_test_dummy"
    assert v._endpoint == "https://mcp.viridis-security.com"
    assert hasattr(v, "injection")
    assert hasattr(v, "canon")
    assert hasattr(v, "maxwell")
    v.close()


def test_client_custom_endpoint():
    v = ViridisMCP(api_key="x", endpoint="http://localhost:8080")
    assert v._endpoint == "http://localhost:8080"
    v.close()


def test_result_from_response():
    payload = {
        "verdict": "attack",
        "probability": 0.99,
        "bitsAtRisk": 16,
        "operatingPoint": {"alpha": 1e-3, "beta": 1e-3},
        "matchedPatterns": ["VC-AI-PROMPT-0001"],
        "recommendedAction": "reject",
        "explainabilityToken": "expl_test",
        "signals": {"pattern": 0.99},
        "billing": {"cost": 0.001, "tier": "starter", "remaining": 49999},
        "backedBy": ["T-IB-02", "T-IB-06", "T-IB-01"],
    }
    r = InjectionDetectResult.from_response(payload)
    assert r.verdict == "attack"
    assert r.probability == 0.99
    assert r.bits_at_risk == 16
    assert r.recommended_action == "reject"
    assert "T-IB-02" in r.backed_by


def test_error_class():
    err = ViridisMCPError("rate_limit_exceeded", 429, {"tier": "free"})
    assert err.status == 429
    assert err.body["tier"] == "free"
