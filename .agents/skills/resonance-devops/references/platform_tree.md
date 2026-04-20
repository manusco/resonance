# Platform Decision Tree

> "Don't maintain a server if you don't have to."

## 1. The Tree

```
Is it a standard Web App?
│
├── Yes (Next.js, Remix, React)
│   ├── Need globally distributed static assets? → **Vercel** / **Netlify**
│   ├── Need infinite scale/control? → **AWS SST** / **Flightcontrol**
│   └── Low budget / Hobby? → **Vercel Hobby** or **Coolify (VPS)**
│
├── No (Docker, Python, Go, Worker)
│   ├── Stateless? → **Google Cloud Run** or **Fly.io**
│   ├── Stateful (Disk needed)? → **Railway** or **Render**
│   └── Heavy Compute / Custom GPU? → **Hetzner VPS** (via Coolify)
│
└── Is it a Database?
    └── **NEVER HOST ON VPS** (Unless you are a DBA). Use Managed (Neon, Supabase).
```

## 2. The Directives

1.  **Vercel First**: For Frontend/Fullstack JS, Vercel is the gold standard for DX.
2.  **Fly.io Second**: For Docker/Backend API, Fly.io offers global edge routing.
3.  **Coolify (VPS) Third**: If costs explode (> $100/mo), migrate to Hetzner + Coolify.
