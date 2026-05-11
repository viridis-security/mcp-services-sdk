# Security Policy

## Reporting a vulnerability

Please report security vulnerabilities to **viridissecurity1@gmail.com** (subject line: `[SECURITY] mcp-services-sdk`).

If you find a vulnerability in the hosted service at `mcp.viridis-security.com` (e.g., authentication bypass, billing-bypass, customer-data exposure), please disclose responsibly and we will respond within 72 hours.

## Supported versions

Only the most recent release of `@viridis/mcp-client` is supported. We recommend keeping your dependency current; the hosted API maintains backwards compatibility within major versions.

## Encryption

All API traffic is TLS 1.2+. API keys are stored as SHA-256 hashes at rest. Webhook payloads use HMAC-SHA256 signatures.
