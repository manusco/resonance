#!/usr/bin/env python3
"""Legal state transitions for evidence-bound goals."""
from __future__ import annotations

GOAL_STATES = {"active", "blocked", "achieved", "cancelled"}
ATTEMPT_STATES = {"queued", "running", "waiting", "verifying", "succeeded", "failed", "cancelled"}
ACCEPTANCE_STATES = {"pending", "accepted", "rejected", "overridden"}

LEGAL_GOAL = {
    "active": {"blocked", "achieved", "cancelled"},
    "blocked": {"active", "cancelled"},
    "achieved": set(),
    "cancelled": set(),
}


def can_transition(current: str, target: str) -> bool:
    return target in LEGAL_GOAL.get(current, set())


def require_transition(current: str, target: str) -> None:
    if current not in GOAL_STATES:
        raise ValueError(f"unknown goal state: {current}")
    if target not in GOAL_STATES:
        raise ValueError(f"unknown goal state: {target}")
    if not can_transition(current, target):
        raise ValueError(f"illegal goal transition: {current} -> {target}")

