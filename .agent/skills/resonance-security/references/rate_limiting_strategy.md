# Rate Limiting Strategy

> "Your API is a resource. Don't let one user eat the buffet."

## 1. The Sliding Window

Do not use "Fixed Window" (e.g., reset at 12:00). It allows bursts at 11:59 and 12:01.
Use **Sliding Window Log** (Redis).

## 2. The Tiers

1.  **Public (Unauth)**: 60 req / min by IP.
2.  **User (Auth)**: 1,000 req / min by UserID.
3.  **Critical Endpoints (Login)**: 5 req / min by IP + Username. (Prevents Brute Force).

## 3. The Headers

Tell the client their status.
*   `X-RateLimit-Limit`: 60
*   `X-RateLimit-Remaining`: 59
*   `X-RateLimit-Reset`: 1678888888 (Epoch)
*   **429 Too Many Requests**: Return strictly.

> 🔴 **Rule**: Rate limiting happens at the Edge (Middleware), not the Controller.
