# Asset Generation Pipeline

> **Objective**: A repeatable factory line for visual assets.

## Phase 1: Conceptualization (The "Brief")
Before generating, define:
1.  **Goal**: What is this image achieving? (Clicks? Trust? Awe?)
2.  **Format**: Where will it live? (Hero banner? Instagram Story? Icon?)
3.  **Constraints**: Does it need text space? Does it need a transparent background?

## Phase 2: Generation (The "Shoot")
1.  **Initial Batch**: Generate 4 variations using the `Visual Prompting Protocol`.
2.  **Seed Selection**: Pick the composition that works best, even if details are wrong.
3.  **Variation**: Run `V1-V4` on the winning seed to refine details.
4.  **Remix**: Use "Vary Region" (Inpainting) to fix hands, eyes, or remove artifacts.

## Phase 3: Post-Processing (The "Develop")
1.  **Upscale**: Use Light/Subtle upscale. excessively high upscales introduce artifacts.
2.  **Vectorize** (Optional): If it's a logo/icon, convert to SVG using Vectorizer.ai or similar.
3.  **text-removal**: Never let AI generate text. Remove it in post or prompt `--no text`.
4.  **Color Grade**: Quick pass in lightroom/photoshop to match brand hex codes if critical.

## Phase 4: Delivery
*   **Naming Convention**: `[Project]_[Type]_[Subject]_[Seed].png`
    *   *Example*: `Resonance_Hero_CyberpunkCity_s250.png`
