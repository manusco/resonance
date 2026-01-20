# Framework Selection (2025 Edition)

> "Do not use Express just because you know it. Fit the tool to the constraint."

## 1. Node.js Ecosystem

| Scenario | Recommendation | Why? |
| :--- | :--- | :--- |
| **Edge / Serverless** (Cloudflare Workers, Vercel) | **Hono** | < 15kb, Web Standards compliant. Ultrafast startup. |
| **High Performance** (Microservices) | **Fastify** | 4x faster than Express. Strict Schema validation (Ajv). |
| **Enterprise / Monolith** (Strict Architecture) | **NestJS** | Angular-style DI. Opinionated. Enforces structure. |
| **Legacy / Tutorials** | **Express** | Huge ecosystem, but slow and bloated. Avoid for new apps. |

## 2. Python Ecosystem

| Scenario | Recommendation | Why? |
| :--- | :--- | :--- |
| **High Performance API** | **FastAPI** | Async native, Pydantic validation built-in. Modern standard. |
| **Full Stack Monolith** (CMS, Admin) | **Django** (Ninja) | "Batteries Included" (Auth, Admin, ORM). |
| **Microservices / Lightweight** | **Litestar** | Newer, faster alternative to FastAPI. |

## 3. The "Express Ban"

**If you are building a new project in 2025, default to Hono or Fastify.**
*   *Why?* Express does not support `async/await` error handling natively without patches, and it is bloated.
