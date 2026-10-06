#!/usr/bin/env bash
# Usage: ./scripts/smoke_test.sh [base_url]
# Run against the running stack (default http://localhost:8080) at the end of a pipeline.
set -euo pipefail
BASE="${1:-http://localhost:8080}"

echo "Checking $BASE/api/health ..."
curl -fsS "$BASE/api/health" >/dev/null

echo "Checking $BASE/api/health/db ..."
curl -fsS "$BASE/api/health/db" >/dev/null

echo "Checking $BASE/api/tasks ..."
curl -fsS "$BASE/api/tasks" >/dev/null

echo "Checking frontend ..."
curl -fsS "$BASE/" >/dev/null

echo "Smoke test passed"
