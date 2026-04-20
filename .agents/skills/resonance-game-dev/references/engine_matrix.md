# Engine Decision Matrix (2025 Edition)

> Do not choose an engine based on what you know. Choose based on what the *game* needs.

## 1. The Decision Tree

```
What is the core constraint?
│
├── "I need it on the Web instantly (No Install)"
│   ├── Is it 3D?
│   │   ├── Yes → **React Three Fiber (R3F)** or **PlayCanvas**
│   │   └── No  → **PixiJS** or **Phaser**
│   │
│   └── Is it High Performance (ECS)?
│       └── **Bevy (Rust -> Wasm)**
│
├── "I need to ship to Consoles/Steam"
│   ├── Is it 2D?
│   │   └── **Godot 4.x** (Best 2D workflow)
│   │
│   └── Is it 3D / High Fidelity?
│       ├── Needed: Nanite/Lumen? → **Unreal Engine 5**
│       └── Needed: Fast Iteration? → **Unity 6**
│
└── "I need to ship to Mobile (iOS/Android)"
    ├── Is it simple/UI heavy? → **React Native (Skia)**
    ├── Is it a game? → **Unity** (Proven) or **Godot** (Lightweight)
```

## 2. Engine Breakdown

| Engine | Ideal Use Case | Pros | Cons |
| :--- | :--- | :--- | :--- |
| **Unity 6** | Cross-platform, Mobile, VR | Massive Asset Store, C# ecosystem, easy hiring. | Bloated build size, chaotic render pipeline (URP/HDRP/Built-in). |
| **Unreal 5** | AAA, Shooter, Cinema | Nanite (Infinite poly), Lumen (Light), Blueprints. | Massive file size (100GB+ install), C++ difficulty. |
| **Godot 4** | Indie 2D, Open Source | Lightweight (<100MB), Nodes are intuitive, GDScript. | 3D performance lags behind UE/Unity, smaller console support. |
| **R3F (Web)** | Viral marketing, UI-heavy | No install, React integration, instant load. | Performance cap (JS single thread), no native editor. |
| **Bevy** | Tech demos, Simulation | Rust ECS is perfectly multithreaded. | Code-only (No Editor), steep Rust learning curve. |
