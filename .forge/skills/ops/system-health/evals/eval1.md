---
query: "Run /system-health"
expected_behavior: "The agent runs npm test, npm run lint, and npm run build, then calculates a health score based on the weights. It checks qualitative flags like DRIFT_DETECTED and AUTH_INCONSISTENT before returning the report."
---
