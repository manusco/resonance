# Load Testing Protocol (k6)

> "It works for 1 user. What about 10,000?"

## 1. The Thresholds

Define failure before testing.
*   **p95 Latency**: < 500ms.
*   **Error Rate**: < 1%.

## 2. This Script (k6)

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 20 }, // Ramp up
    { duration: '1m', target: 20 },  // Stay
    { duration: '10s', target: 0 },  // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],
  },
};

export default function () {
  const res = http.get('https://api.example.com');
  check(res, { 'status was 200': (r) => r.status == 200 });
  sleep(1);
}
```

## 3. The Scenarios

1.  **Smoke Test**: Minimal load to verify script logic.
2.  **Load Test**: Expected traffic peak.
3.  **Stress Test**: Find the breaking point (Crash the server).
4.  **Soak Test**: Run for 24h (Find Memory Leaks).

> 🔴 **Rule**: Stress test BEFORE Black Friday, not during.
