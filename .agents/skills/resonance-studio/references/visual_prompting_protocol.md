# Visual Prompting Protocol

> **Objective**: Define the physics and parameters of the image before generation.

## 1. The Universal Formula
Every prompt must answer these 4 questions:
1.  **Subject**: Who/What is it? (Adjectives + Noun).
2.  **Environment**: Where are they? (Background, Context).
3.  **Lighting**: How is it lit? (Softbox, Rembrant, Neon, Golden Hour).
4.  **Camera**: How is it shot? (Lens, Film Stock, Angle).

## 2. The JSON Structure (The Payload)
We do not send raw text. We send a `JSON Payload` to ensure reproducibility. This structure mimics the "Prompt-as-Code" standard found in elite repositories (e.g., Nano Banana Pro).

```json
{
  "meta": {
    "version": "1.0",
    "model": "Midjourney v6",
    "param_syntax": "raycast"
  },
  "prompt": {
    "subject": "A cybernetic samurai meditating in a neon garden",
    "environment": "Neo-Tokyo rooftop, raining, bioluminescent plants",
    "lighting": "Volumetric purple fog, rim light from hologram advertisements",
    "camera": "85mm lens, f/1.8, bokeh effect, cinematic grading",
    "style": ["Cyberpunk 2077", "Blade Runner", "Unreal Engine 5"]
  },
  "technical": {
    "ar": "16:9",
    "chaos": 20,
    "stylize": 250,
    "iw": 1.5
  },
  "negative_prompt": "text, watermark, blurry, low resolution, deformed hands, extra limbs"
}
```

## 3. Parametric Prompting (Raycast Standard)
For high-frequency assets (e.g., Blog Headers, Social Cards), use **Dynamic Arguments** to create reusable templates.

**Syntax:** `{argument name="variable_name" default="default_value"}`

**Example Template:**
```text
A minimal geometric {argument name="shape" default="cube"} floating in a {argument name="color" default="pastel blue"} void, soft studio lighting, 4k render.
```

## 4. The "Camera Bag" (Cheat Sheet)

### Lenses
*   **16mm / 24mm**: Wide angle. Dynamic, distortion, epic scale.
*   **35mm / 50mm**: "Human eye". Natural, documentary, street.
*   **85mm / 105mm**: Portrait. Flattering, compression, bokeh background.
*   **200mm**: Telephoto. intense compression, isolation.

### Lighting Setup
*   **Golden Hour**: Warm, soft, emotional (Sunset/Sunrise).
*   **Blue Hour**: Moody, cold, twilight.
*   **Rembrandt**: Dramatic triangle of light on cheek (Classic portrait).
*   **Butterfly**: Glamour lighting, shadow under nose.
*   **Volumetric**: God rays, fog, atmosphere.
*   **Chiaroscuro**: High contrast, deep shadows (Film Noir).

### Angles
*   **Eye Level**: Neutral, connection.
*   **Low Angle**: Heroic, dominant, powerful.
*   **High Angle**: Vulnerable, small.
*   **Dutch Angle**: Tilted, chaotic, uneasy.
*   **Top-Down (Knolling)**: Organized, layout, flat lay.

## 5. Parameter Cheatsheet (Midjourney/Flux)
*   `--ar 16:9` (Cinematic) / `--ar 9:16` (Social Story)
*   `--stylize 250` (Balanced) / `--stylize 750` (Artistic)
*   `--weird 0-3000` (introduce oddity)
*   `--tile` (Seamless patterns)
