"""
Viridis MCP Client SDK (Python)

Open-source (Apache-2.0). Hosted endpoint at https://mcp.viridis-security.com.
Source: https://github.com/viridis-security/mcp-services-sdk

Backing theorems (Aristotle-verified Lean 4):
    T-IB-01..07, T-IB-09. See https://github.com/viridis-security/corpus.
"""

from viridis_mcp_client.client import ViridisMCP, AsyncViridisMCP, ViridisMCPError
from viridis_mcp_client.types import (
    InjectionDetectInput,
    InjectionDetectResult,
    CanonScanInput,
    CanonScanResult,
    MaxwellChallengeInput,
    MaxwellChallengeResult,
)

__version__ = "0.1.0"
__all__ = [
    "ViridisMCP",
    "AsyncViridisMCP",
    "ViridisMCPError",
    "InjectionDetectInput",
    "InjectionDetectResult",
    "CanonScanInput",
    "CanonScanResult",
    "MaxwellChallengeInput",
    "MaxwellChallengeResult",
]
