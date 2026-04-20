# The Juice Checklist (Plasma Standard)

> "Juice" is the non-functional feedback that makes interaction satisfying.
> **Rule**: Every Primary Action (Jump, Shoot, Hit) must have at least 3 layers of juice.

## 1. Visual Juice

| Technique | Description | Implementation Guide |
| :--- | :--- | :--- |
| **Squash & Stretch** | Character distorts on impulse | Identify `Y-scale` on Jump (0.8 -> 1.2). |
| **Flash** | Sprite turns white/red on hit | Shader property `_FlashAmount` 0 -> 1 -> 0 over 0.1s. |
| **Particles** | Debris generated on impact | Emit 5-10 particles at contact point. Random velocity. |
| **Screen Shake** | Camera offset on impact | `camera.pos += random_vec2(trauma^2)`. Decay trauma. |
| **Freeze Frame** | Game pauses on heavy hit | `timeScale = 0` for 0.05s-0.1s. |
| **Tweening** | Non-linear movement | Use `BackOut` for spawn, `Elastic` for UI. |

## 2. Audio Juice

| Technique | Description | Implementation Guide |
| :--- | :--- | :--- |
| **Pitch Variation** | Randomize pitch per play | `pitch = base_pitch + random(-0.1, 0.1)`. Prevents fatigue. |
| **Layering** | Multiple sounds for one event | Impact = `Thud.wav` + `Crunch.wav` + `Whoosh.wav` (Low volume). |
| **Ducking** | Lower music volume on impact | Sidechain compression on heavy SFX. |

## 3. UI Juice

| Technique | Description | Implementation Guide |
| :--- | :--- | :--- |
| **Button Response** | Scale down on press | Scale 1.0 -> 0.95 on `pointerDown`. |
| **Hover State** | Scale up/Glow on hover | Scale 1.0 -> 1.05 on `pointerEnter`. |
| **Count-up** | Numbers tick up, dont jump | `lerp(current, target, dt * speed)`. |
