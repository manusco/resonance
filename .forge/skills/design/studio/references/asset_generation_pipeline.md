# Asset Generation Pipeline

> **Objective**: A repeatable line from brief to finished asset, independent of any one tool.

## Phase 1: Brief

Before generating, settle four things:

1.  **Goal**: what does this image do? (Earn a click, build trust, set a mood, carry information.)
2.  **Placement**: where does it live? (Hero banner, phone-first story, icon, print.)
3.  **Constraints**: does it need overlay room for copy? A transparent background? A fixed palette?
4.  **Aspect ratio**: fixed now, matched to the placement, before a single frame renders.

A vague brief produces a vague image. Name the job in one sentence and the rest of the pipeline has something to aim at.

## Phase 2: Generate

1.  **Batch**: produce a handful of variations from the structured prompt (see the Visual Prompting Protocol).
2.  **Choose the composition**: pick the frame whose composition and light are strongest, even if local details are wrong. Composition is hard to fix later; a bad hand is easy.
3.  **Refine on that direction**: hold the chosen frame and generate close variations of it, rather than starting over. You are converging, not re-rolling.
4.  **Region repair**: fix local flaws (hands, eyes, a stray artifact) by inpainting that region only, so the rest of the frame stays intact. If your tool calls this something specific, use that; the idea is repair-in-place, not a full regenerate.

## Phase 3: Finish

1.  **Upscale gently**: a light upscale preserves texture. Pushing scale too far invents detail and adds artifacts.
2.  **Vectorize when it should be vector**: for a logo, icon, or flat mark, trace it to clean vector paths so it scales without loss. Any capable vectorizer will do.
3.  **Keep real text out of the render**: models garble type. Exclude text from the prompt and set copy in layout instead, or hand it to `resonance-design-designer`.
4.  **Color pass if it is critical**: nudge the grade toward the exact brand values in whatever editor you have, only when the placement demands precision.

## Phase 4: Deliver

*   **Naming**: keep it descriptive and reproducible so the source is obvious later.
    *   Pattern: `[Project]_[Type]_[Subject]_[Seed].png`
    *   Example: `Resonance_Hero_HarborDawn_s3417.png`
*   **Save the recipe**: store the final structured prompt and its settings (seed, aspect ratio, stylization) next to the asset. An asset you cannot regenerate is a liability the next time the brief shifts.
