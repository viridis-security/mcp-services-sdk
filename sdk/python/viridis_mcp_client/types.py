"""Type definitions matching the Viridis MCP API responses."""
from dataclasses import dataclass, field
from typing import Literal, Optional, List, Dict, Any

Certainty = Literal["quick", "standard", "premium"]
Verdict = Literal["clean", "suspicious", "attack"]
Action = Literal["allow", "sanitize", "reject", "escalate"]


@dataclass
class InjectionDetectInput:
    input: str
    context: Optional[str] = None
    certainty: Certainty = "standard"
    agent_id: Optional[str] = None


@dataclass
class InjectionDetectResult:
    verdict: Verdict
    probability: float
    bits_at_risk: int
    operating_point: Dict[str, float]
    matched_patterns: List[str]
    recommended_action: Action
    explainability_token: str
    signals: Dict[str, float]
    billing: Dict[str, Any]
    backed_by: List[str] = field(default_factory=list)

    @classmethod
    def from_response(cls, d: Dict[str, Any]) -> "InjectionDetectResult":
        return cls(
            verdict=d["verdict"],
            probability=d["probability"],
            bits_at_risk=d["bitsAtRisk"],
            operating_point=d["operatingPoint"],
            matched_patterns=d.get("matchedPatterns", []),
            recommended_action=d["recommendedAction"],
            explainability_token=d.get("explainabilityToken", ""),
            signals=d.get("signals", {}),
            billing=d.get("billing", {}),
            backed_by=d.get("backedBy", []),
        )


@dataclass
class CanonScanInput:
    source: str
    language: str = "auto"
    certainty: Certainty = "standard"
    agent_id: Optional[str] = None


@dataclass
class CanonMatch:
    entry_id: str
    category: str
    severity: str
    bits_at_risk: int
    occurrences: List[Dict[str, Any]]
    mitigation: str
    references: List[str]


@dataclass
class CanonScanResult:
    matches: List[CanonMatch]
    total_occurrences: int
    canon_version: str
    scanned_lines: int
    operating_point: Dict[str, float]
    billing: Dict[str, Any]
    backed_by: List[str] = field(default_factory=list)

    @classmethod
    def from_response(cls, d: Dict[str, Any]) -> "CanonScanResult":
        return cls(
            matches=[
                CanonMatch(
                    entry_id=m["entryId"],
                    category=m["category"],
                    severity=m["severity"],
                    bits_at_risk=m["bitsAtRisk"],
                    occurrences=m.get("occurrences", []),
                    mitigation=m.get("mitigation", ""),
                    references=m.get("references", []),
                )
                for m in d.get("matches", [])
            ],
            total_occurrences=d["totalOccurrences"],
            canon_version=d.get("canonVersion", ""),
            scanned_lines=d.get("scannedLines", 0),
            operating_point=d.get("operatingPoint", {}),
            billing=d.get("billing", {}),
            backed_by=d.get("backedBy", []),
        )


@dataclass
class MaxwellChallengeInput:
    agent_id: str
    request_id: str
    injection_probability: float
    amplification: Optional[Literal["low", "medium", "high", "extreme"]] = None


@dataclass
class MaxwellChallengeResult:
    challenge_id: str
    scheme: str
    params: Dict[str, Any]
    amplification: str
    M: int
    salt_b64: str
    expires_at: str
    estimated_cost_ms: Dict[str, int]
    backed_by: List[str] = field(default_factory=list)

    @classmethod
    def from_response(cls, d: Dict[str, Any]) -> "MaxwellChallengeResult":
        return cls(
            challenge_id=d["challengeId"],
            scheme=d["scheme"],
            params=d.get("params", {}),
            amplification=d.get("amplification", ""),
            M=d.get("M", 1),
            salt_b64=d.get("saltB64", ""),
            expires_at=d.get("expiresAt", ""),
            estimated_cost_ms=d.get("estimatedCostMs", {}),
            backed_by=d.get("backedBy", []),
        )
