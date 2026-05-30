# Docker Optimization Protocol

> "Small containers are secure containers."

## 1. Multi-Stage Builds

Never ship the SDK.

**Bad:**
```dockerfile
FROM node:18
COPY . .
RUN npm install
CMD ["npm", "start"]
```

**Elite:**
```dockerfile
# Build Stage
FROM node:18-alpine AS builder
WORKDIR /app
COPY . .
RUN npm ci && npm run build

# Run Stage
FROM node:18-alpine-slim
WORKDIR /app
COPY --from=builder /app/dist ./dist
# No devDependencies!
CMD ["node", "dist/server.js"]
```

## 2. Layer Caching

Order matters.
1.  Copy `package.json`.
2.  Run `npm install`.
3.  Copy Source Code.

Why? If you change `index.ts`, Docker doesn't need to re-run `npm install`.

## 3. The Root Ban

*   Do not run containers as `root`.
*   Add `USER node` (or create a user) in the final stage.

> 🔴 **Rule**: If your image is > 200MB (for a JS app), you failed optimization.
