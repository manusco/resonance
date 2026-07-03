# Visual Prompting Protocol

> **Objective**: Define the physics and parameters of an image before you generate, in terms that hold across any image model.

This protocol is model-neutral on purpose. It talks about aspect ratio, stylization strength, and exclusions as ideas, not as one product's flags. Whatever tool you use, map these concepts to its controls.

## 1. The universal formula

Every prompt answers four questions:

1.  **Subject**: who or what is it? (Adjectives + noun, doing something specific.)
2.  **Environment**: where is it? (Background, context, time of day.)
3.  **Light**: how is it lit? (Direction, quality, and source: soft key, hard rim, golden hour, single bare bulb.)
4.  **Camera**: how is it shot? (Focal length, aperture, medium or film stock, angle.)

Answer all four and the image has a spine. Skip one and the model fills it with its own average, which is where the generic look comes from.

## 2. Structure the prompt (fields, not prose)

Keep the prompt as separate fields so each can be edited without disturbing the rest. The point is control and reproducibility, not any particular file format. A plain structure like this travels between tools:

```
subject:      A weathered lighthouse keeper trimming a lamp wick
environment:  Cramped lantern room at dawn, salt-fogged glass, brass fittings
light:        Low warm sun through fog from the left, cool fill from the sky
camera:       50mm, f/2.8, slight low angle, muted natural grade
style:        Documentary photograph, fine film grain
exclude:      text, watermark, extra fingers, floating objects
```

Adjust one field at a time. Change `light` to test a mood, hold everything else, and the comparison is honest. Rewrite the whole thing at once and you learn nothing about what moved the result.

## 3. Reusable templates (parameterize the repeatable)

For high-frequency assets (blog headers, social cards), leave slots in the fields so one template serves many posts. Express slots however your tool allows; the idea is a fixed structure with named variables:

```
A minimal geometric [SHAPE] resting in a [COLOR] void, soft directional
studio light from the upper left, shallow depth, fine grain.
```

Fill `[SHAPE]` and `[COLOR]` per post. The composition, light, and finish stay constant, so the set stays coherent while the subject varies.

## 4. The camera bag

### Focal length
*   **Wide (roughly 16 to 24mm)**: dynamic, exaggerated depth, epic scale, edge distortion.
*   **Normal (roughly 35 to 50mm)**: close to human vision. Natural, documentary, street.
*   **Portrait (roughly 85 to 105mm)**: flattering compression, soft separated background.
*   **Telephoto (200mm and up)**: strong compression, isolation, flattened planes.

### Light
*   **Golden hour**: warm, soft, low sun. Emotional.
*   **Blue hour**: cool twilight. Moody, quiet.
*   **Rembrandt**: a small triangle of light on the shadowed cheek. Classic portrait.
*   **Butterfly**: light straight on and slightly above, a small shadow under the nose. Glamour.
*   **Volumetric**: visible beams through fog or dust. Atmosphere and depth.
*   **Chiaroscuro**: high contrast, deep shadow, one light. Noir drama.

### Angle
*   **Eye level**: neutral, direct, connective.
*   **Low angle**: makes the subject dominant and heroic.
*   **High angle**: makes the subject small or vulnerable.
*   **Tilted (dutch)**: uneasy, kinetic, off-balance.
*   **Top-down (flat lay)**: organized, schematic, good for layout.

## 5. Parameters, described not flagged

Map these to your model's controls; the names differ, the ideas do not.

*   **Aspect ratio**: match the placement. Wide for cinematic and hero; tall for phone-first stories and portraits; square for feeds and avatars.
*   **Stylization strength**: how far the model may drift from a literal reading. Low for faithful and product-accurate; high for expressive and artistic. Push it only when the brief wants interpretation.
*   **Variation / chaos**: how much spread across a batch. More spread to explore early, less to converge once a direction is set.
*   **Tiling**: for textures and repeating patterns that must wrap without a visible seam.
*   **Exclusions**: state what must not appear (text, watermark, extra limbs) rather than hoping the model omits it.
