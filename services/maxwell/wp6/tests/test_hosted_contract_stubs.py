# SPDX-License-Identifier: Apache-2.0
"""Blocked hosted cases; proposed local adapter observations, not an API schema.

No handler, HTTP client, environment secret, wallet or payment code is imported.
Replace the skip only after a named private baseline and isolated adapter exist.
"""

from collections.abc import Callable

import pytest

CaseRunner = Callable[[str], dict[str, object]]

pytestmark = pytest.mark.skip(
    reason="Authoritative hosted implementation and isolated local adapter unavailable"
)


def test_single_use_across_workers(hosted_case_runner: CaseRunner) -> None:
    result = hosted_case_runner("shared-store-race")
    assert result["accepted"] == 1
    assert result["replays_rejected"] == 1
    assert result["invalid_work_consumed"] is False


def test_state_expiry_and_failure_are_safe(hosted_case_runner: CaseRunner) -> None:
    result = hosted_case_runner("state-expiry-and-outage")
    assert result["expired_entries_retained"] == 0
    assert result["store_outage_authorized"] is False


def test_receipt_issue_verify_revoke(hosted_case_runner: CaseRunner) -> None:
    result = hosted_case_runner("receipt-lifecycle")
    assert result["valid_before_revoke"] is True
    assert result["valid_after_revoke"] is False
    assert result["wrong_principal_authorized"] is False


def test_captured_receipt_replay_restores_full_work(
    hosted_case_runner: CaseRunner,
) -> None:
    result = hosted_case_runner("captured-receipt-replay")
    assert result["receipt_revoked"] is True
    assert result["full_difficulty_required"] is True
    assert result["replay_authorized"] is False


def test_argon2_vectors_and_all_profiles(hosted_case_runner: CaseRunner) -> None:
    result = hosted_case_runner("argon2-known-vectors-and-profiles")
    assert result["independent_vectors_match"] is True
    assert result["sha256_proxy_accepted"] is False
    assert result["profiles_match_confirmed_contract"] is True


def test_payable_url_ignores_host_and_forwarded_headers(
    hosted_case_runner: CaseRunner,
) -> None:
    result = hosted_case_runner("owned-payable-alias")
    assert result["spoofed_headers_change_binding"] is False
    assert result["payment_mutations"] == 0


def test_remote_oracle_validation_and_local_fallback(
    hosted_case_runner: CaseRunner,
) -> None:
    result = hosted_case_runner("mocked-oracle-and-fallback")
    assert result["valid_remote_value_used"] is True
    assert result["invalid_or_unavailable_uses_local"] is True
    assert result["live_requests"] == 0
