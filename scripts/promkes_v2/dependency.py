from __future__ import annotations

from collections import defaultdict, deque
from typing import Iterable


class DependencyError(ValueError):
    pass


def validate_dag(edges: Iterable[tuple[str, str]]) -> list[str]:
    edges = list(edges)
    nodes = {n for e in edges for n in e}
    indegree = {n: 0 for n in nodes}
    adj = defaultdict(set)
    for source, dependent in edges:
        if not source or not dependent:
            return ["dependency edge contains empty node"]
        if dependent not in adj[source]:
            adj[source].add(dependent)
            indegree[dependent] += 1
    queue = deque(sorted(n for n, d in indegree.items() if d == 0))
    visited = 0
    while queue:
        node = queue.popleft()
        visited += 1
        for child in sorted(adj[node]):
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
    return [] if visited == len(nodes) else ["dependency graph contains a directed cycle"]


def reference_closure(edges: Iterable[tuple[str, str]], changed: str, *, reject_cycles: bool = True) -> set[str]:
    edges = list(edges)
    if reject_cycles:
        errors = validate_dag(edges)
        if errors:
            raise DependencyError("; ".join(errors))
    adj = defaultdict(set)
    for source, dependent in edges:
        adj[source].add(dependent)
    found, queue = set(), deque(sorted(adj.get(changed, set())))
    while queue:
        node = queue.popleft()
        if node == changed or node in found:
            continue
        found.add(node)
        queue.extend(sorted(adj[node]))
    return found


def audit_engine_against_spec(engine_closure, edges: list[tuple[str, str]], changed: str) -> tuple[bool, list[str]]:
    expected = reference_closure(edges, changed)
    try:
        actual = set(engine_closure(edges, changed))
    except Exception as exc:
        return False, [f"engine exception: {type(exc).__name__}: {exc}"]
    if actual != expected:
        return False, [f"independent oracle mismatch: missing={sorted(expected-actual)} extra={sorted(actual-expected)}"]
    return True, []


def invalidate_artifacts(artifacts: list[dict], edges: list[tuple[str, str]], changed: str) -> list[dict]:
    invalidated = reference_closure(edges, changed)
    by_id = {a["artifact_id"]: a for a in artifacts}
    missing = invalidated - set(by_id)
    if missing:
        raise DependencyError(f"missing dependent artifacts: {sorted(missing)}")
    result = [dict(a) for a in artifacts]
    for row in result:
        if row["artifact_id"] in invalidated:
            row["status"] = "INVALIDATED"
            row["validation_result"] = "NOT_RUN"
        # all unaffected items are preserved byte-for-byte at the record level
    return result
