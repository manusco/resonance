# Rate Limiting Strategy

> **Objective**: Prevent Abuse, DDoS, and Resource Exhaustion.

## 1. Strategy Types

| Type | Use Case | Implementation |
| :--- | :--- | :--- |
| **Global (IP)** | Basic DDoS protection | 100 requests / 15 min per IP. |
| **User-Based** | Fair Usage Policy | 1000 requests / hour per `sub` (User ID). |
| **Endpoint-Specific** | Expensive Resources | 5 requests / min per IP for `/api/ai/generate`. |
| **Auth Brute-force** | Login Protection | 5 failed attempts / 30 min per Email/IP. |

## 2. Implementation Patterns

### Standard API Limiter (Redis + Express)
Use a centralized store (Redis) for distributed limiting.

```javascript
const rateLimit = require('express-rate-limit');
const RedisStore = require('rate-limit-redis');

const apiLimiter = rateLimit({
  store: new RedisStore({
    client: redisClient,
    prefix: 'rl:api:'
  }),
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per windowMs
  standardHeaders: true, // Return rate limit info in headers
  legacyHeaders: false,
  message: { error: 'Too many requests, please try again later.' }
});

app.use('/api/', apiLimiter);
```

### Tiered Rate Limiting
Differentiate limits based on user roles or subscription tiers.

```javascript
const limits = {
  free: { windowMs: 3600000, max: 100 },
  pro: { windowMs: 3600000, max: 1000 }
};

const tieredLimiter = async (req, res, next) => {
  const tier = req.user?.tier || 'free';
  const limit = limits[tier];
  // ... check limit against Redis ...
};
```

## 3. Headers Protocol

Always inform the client of their status:
*   `X-RateLimit-Limit`: The maximum number of requests allowed.
*   `X-RateLimit-Remaining`: The number of requests remaining.
*   `X-RateLimit-Reset`: The time at which the current window resets.
*   `Retry-After`: Seconds to wait before retrying (on 429).
