"""HTTP client for Viridis MCP services. Sync + async variants."""
from typing import Optional, Any, Dict
import httpx

from viridis_mcp_client.types import (
    InjectionDetectInput,
    InjectionDetectResult,
    CanonScanInput,
    CanonScanResult,
    MaxwellChallengeInput,
    MaxwellChallengeResult,
)

DEFAULT_ENDPOINT = "https://mcp.viridis-security.com"
USER_AGENT = "viridis-mcp-client/0.1.0 (python)"


class ViridisMCPError(Exception):
    """Raised when the API returns an error response."""

    def __init__(self, message: str, status: int, body: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message)
        self.status = status
        self.body = body or {}


class _InjectionAPI:
    def __init__(self, client: "ViridisMCP") -> None:
        self._client = client

    def detect(
        self,
        input: str,
        context: Optional[str] = None,
        certainty: str = "standard",
        agent_id: Optional[str] = None,
    ) -> InjectionDetectResult:
        body: Dict[str, Any] = {"input": input, "certainty": certainty}
        if context is not None:
            body["context"] = context
        if agent_id is not None:
            body["agentId"] = agent_id
        d = self._client._request("POST", "/v1/injection/detect", body)
        return InjectionDetectResult.from_response(d)


class _CanonAPI:
    def __init__(self, client: "ViridisMCP") -> None:
        self._client = client

    def scan(
        self,
        source: str,
        language: str = "auto",
        certainty: str = "standard",
        agent_id: Optional[str] = None,
    ) -> CanonScanResult:
        body: Dict[str, Any] = {"source": source, "language": language, "certainty": certainty}
        if agent_id is not None:
            body["agentId"] = agent_id
        d = self._client._request("POST", "/v1/canon/scan", body)
        return CanonScanResult.from_response(d)


class _MaxwellAPI:
    def __init__(self, client: "ViridisMCP") -> None:
        self._client = client

    def challenge(
        self,
        agent_id: str,
        request_id: str,
        injection_probability: float,
        amplification: Optional[str] = None,
    ) -> MaxwellChallengeResult:
        body: Dict[str, Any] = {
            "agentId": agent_id,
            "requestId": request_id,
            "injectionProbability": injection_probability,
        }
        if amplification is not None:
            body["amplification"] = amplification
        d = self._client._request("POST", "/v1/maxwell/challenge", body)
        return MaxwellChallengeResult.from_response(d)


class ViridisMCP:
    """Synchronous client. Use AsyncViridisMCP for asyncio."""

    def __init__(self, api_key: str, endpoint: str = DEFAULT_ENDPOINT, timeout: float = 30.0) -> None:
        self._api_key = api_key
        self._endpoint = endpoint.rstrip("/")
        self._http = httpx.Client(
            timeout=timeout,
            headers={
                "Authorization": f"Bearer {api_key}",
                "User-Agent": USER_AGENT,
            },
        )
        self.injection = _InjectionAPI(self)
        self.canon = _CanonAPI(self)
        self.maxwell = _MaxwellAPI(self)

    def _request(self, method: str, path: str, body: Dict[str, Any]) -> Dict[str, Any]:
        r = self._http.request(method, self._endpoint + path, json=body)
        if r.status_code >= 400:
            try:
                body_json = r.json()
            except Exception:
                body_json = {"error": r.text}
            raise ViridisMCPError(body_json.get("error") or r.reason_phrase, r.status_code, body_json)
        return r.json()

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> "ViridisMCP":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()


class _AsyncInjectionAPI:
    def __init__(self, client: "AsyncViridisMCP") -> None:
        self._client = client

    async def detect(
        self,
        input: str,
        context: Optional[str] = None,
        certainty: str = "standard",
        agent_id: Optional[str] = None,
    ) -> InjectionDetectResult:
        body: Dict[str, Any] = {"input": input, "certainty": certainty}
        if context is not None:
            body["context"] = context
        if agent_id is not None:
            body["agentId"] = agent_id
        d = await self._client._request("POST", "/v1/injection/detect", body)
        return InjectionDetectResult.from_response(d)


class _AsyncCanonAPI:
    def __init__(self, client: "AsyncViridisMCP") -> None:
        self._client = client

    async def scan(
        self,
        source: str,
        language: str = "auto",
        certainty: str = "standard",
        agent_id: Optional[str] = None,
    ) -> CanonScanResult:
        body: Dict[str, Any] = {"source": source, "language": language, "certainty": certainty}
        if agent_id is not None:
            body["agentId"] = agent_id
        d = await self._client._request("POST", "/v1/canon/scan", body)
        return CanonScanResult.from_response(d)


class _AsyncMaxwellAPI:
    def __init__(self, client: "AsyncViridisMCP") -> None:
        self._client = client

    async def challenge(
        self,
        agent_id: str,
        request_id: str,
        injection_probability: float,
        amplification: Optional[str] = None,
    ) -> MaxwellChallengeResult:
        body: Dict[str, Any] = {
            "agentId": agent_id,
            "requestId": request_id,
            "injectionProbability": injection_probability,
        }
        if amplification is not None:
            body["amplification"] = amplification
        d = await self._client._request("POST", "/v1/maxwell/challenge", body)
        return MaxwellChallengeResult.from_response(d)


class AsyncViridisMCP:
    """Async/await client."""

    def __init__(self, api_key: str, endpoint: str = DEFAULT_ENDPOINT, timeout: float = 30.0) -> None:
        self._api_key = api_key
        self._endpoint = endpoint.rstrip("/")
        self._http = httpx.AsyncClient(
            timeout=timeout,
            headers={
                "Authorization": f"Bearer {api_key}",
                "User-Agent": USER_AGENT,
            },
        )
        self.injection = _AsyncInjectionAPI(self)
        self.canon = _AsyncCanonAPI(self)
        self.maxwell = _AsyncMaxwellAPI(self)

    async def _request(self, method: str, path: str, body: Dict[str, Any]) -> Dict[str, Any]:
        r = await self._http.request(method, self._endpoint + path, json=body)
        if r.status_code >= 400:
            try:
                body_json = r.json()
            except Exception:
                body_json = {"error": r.text}
            raise ViridisMCPError(body_json.get("error") or r.reason_phrase, r.status_code, body_json)
        return r.json()

    async def close(self) -> None:
        await self._http.aclose()

    async def __aenter__(self) -> "AsyncViridisMCP":
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()
