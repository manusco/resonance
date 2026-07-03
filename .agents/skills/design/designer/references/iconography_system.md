# Iconography System

> Icons are the smallest unit of interface, and the eye reads them collectively before it reads any single one. A set feels crafted when every glyph shares the same skeleton: one grid, one stroke, one optical weight, one drawing hand. It feels bought-in-a-hurry the moment weights drift, corners disagree, and a circle sits a hair too small next to a square. As with type, what measures equal often looks wrong, so the icon grid is a starting point the eye is allowed to overrule. Build a system, tune it optically, and make every glyph earn its meaning before it earns its pixels.

## Contents
- The icon grid and keyline shapes
- Consistent stroke and optical weight
- Optical alignment and size correction
- The sizing scale and pixel-snapping
- Metaphor clarity and cultural neutrality
- When an icon needs a label
- Filled versus outlined semantics
- Build your own set or adopt one
- Accessibility
- Restrained icon motion

## The icon grid and keyline shapes

Every coherent set is drawn inside one grid with a fixed live area and padding. The grid is the shared skeleton that makes twenty glyphs by different hands read as one family.

- **A live area inside a padded box.** On a common 24px grid, the artwork lives inside roughly a 20px region with a 2px trim margin all around, so no icon crowds its own edge and adjacent icons keep even rhythm. Nothing draws into the trim except a deliberate overshoot.
- **Keyline shapes set the visual size.** Define a canonical circle, square, portrait rectangle, and landscape rectangle inside the live area, and size each glyph to the keyline its silhouette matches. A square-ish icon fills the square keyline; a round one fills the circle keyline, which is deliberately a touch larger than the square (see optical correction). This is what keeps a heart, a gear, and a document reading as the same size despite different outlines.
- **Snap to the grid, then break it on purpose.** Anchor strokes and centers to the grid so shapes feel structured, but never let the grid force a shape that looks wrong. The grid serves the eye, not the reverse.

## Consistent stroke and optical weight

Stroke is the loudest consistency signal in a set. A single wrong weight stands out more than a wrong metaphor.

- **One stroke width across the set,** defined against the base grid (commonly around 1.5 to 2px on a 24px grid) and scaled proportionally at other sizes. Mixing 1.5px and 2px strokes in one family reads as broken even when nothing else is wrong.
- **Match apparent weight, not just the number.** A glyph made of many short strokes (a list, a grid of dots) carries more total ink and looks heavier than a single-stroke glyph (an arrow) at the identical width. Lighten the busy one or simplify it so every icon lands at the same optical weight. This is the icon-scale version of the contrast budget: no glyph should shout louder than its neighbors by accident.
- **Consistent corner radius and terminals.** Pick one corner rounding and one line cap (round or butt) and hold them across every glyph. Corners and terminals are a signature; when they drift, the set loses its hand.
- **Consistent counters and joins.** Interior gaps, the space where strokes meet, the size of an arrowhead: standardize these the way a typeface standardizes its parts. A set is a small typeface, and the discipline is the same.

## Optical alignment and size correction

This is where a merely consistent set becomes a crafted one, and it is exactly the optical-over-mechanical logic from `optical_craft.md` applied at 24 pixels.

- **Round and pointed shapes must overshoot.** A circle drawn to the same bounding height as a square looks smaller, because the eye measures area at the widest point and a circle only touches its box at four points. Push circular and triangular glyphs roughly 2 to 5 percent past the square keyline so they read as equal size. This is why a well-drawn set does not sit on a rigid pixel grid; forcing every glyph to identical bounds makes the round ones look shrunken.
- **Center the visible ink, not the bounding box.** A glyph whose mass sits off to one side (a speech bubble with a tail, a bell, a magnifier) is optically centered by its ink, not its box. A play triangle in particular reads left-heavy when centered by bounds; nudge it right so its visual mass sits in the middle. The viewBox center is a suggestion, not the answer.
- **Balance visual weight around the center.** If a glyph is heavier on one side, the whole icon drifts. Adjust until the mass feels centered, even when the coordinates say it already is.
- **Align to the family, not just the frame.** When icons sit in a row beside text, align their optical centers to the text, and tune the gap to each glyph's weight, since a heavy icon wants a hair more air than a light one at the same nominal size.

## The sizing scale and pixel-snapping

Icons render at specific sizes, and the crispness a designer is judged on lives at small sizes where every subpixel shows.

- **A discrete size scale, not arbitrary scaling.** Define the sizes the set ships at (16, 20, 24, 32, 48) and design for them, rather than drawing once and letting the renderer scale to anything. An icon drawn at 24 and shrunk to 16 blurs and clots; the strokes merge and the counters fill.
- **Pixel-snapping and alignment to the grid.** At small sizes, strokes that do not align to the pixel grid render soft and gray instead of crisp. Snap strokes to whole or half pixels so a 1px line lands on one row of pixels, not smeared across two. This is why hand-tuned small icons look sharp and naively scaled ones look muddy.
- **Optical sizes, like a typeface.** The 16px version of an icon is not the 48px version scaled down. It wants fewer details, a slightly heavier relative stroke so it survives, and larger interior gaps so it does not fill in. Draw or at least tune a dedicated small size. Detail that reads at 48px becomes noise at 16px.
- **Scale stroke with size, proportionally.** Hold the stroke-to-glyph ratio roughly constant across the scale so the family stays recognizable, adjusting by eye at the smallest end where a strictly proportional stroke gets too thin.

## Metaphor clarity and cultural neutrality

A beautiful icon that no one can read is a failure. Meaning comes first; craft makes the meaning crisp.

- **Use the convention where one exists.** A magnifier means search, a trash can means delete, a gear means settings, a house means home. These are learned, and Jakob's law applies: users spend their time with other products, so novelty in a common icon costs comprehension for no gain. Innovate on your product, not on the trash-can glyph.
- **One concept per icon.** An icon trying to say "export the filtered report as PDF" becomes an unreadable pile of parts. If the meaning needs a sentence, it needs a label, not more strokes.
- **Beware the abstract concept.** Concrete objects (camera, calendar, lock) icon well. Abstract ideas (strategy, quality, synergy) do not, and forcing them produces the arbitrary glyphs that mean nothing without their caption. When a concept has no physical form, prefer a word.
- **Watch cultural specificity.** A mailbox with a flag, a specific currency sign, a gesture, a right-to-left directional assumption, a color with local meaning: these do not travel. Prefer widely understood forms, mirror directional icons for RTL layouts, and never let a hand gesture carry a critical action.
- **Test recognition without the label.** Show the glyph alone and ask what it does. If people cannot say, the metaphor is not carrying, and no amount of stroke tuning will fix a meaning the shape does not hold.

## When an icon needs a label

The honest default: an icon alone is ambiguous more often than designers admit. Recognition is worse than we assume, and confident-looking glyphs routinely fail a blind test.

- **Pair icon with text for anything important or infrequent.** A toolbar of unlabeled icons is a memory test. For primary navigation, destructive actions, and anything a user meets rarely, show the label. The icon then speeds recognition for return users while the word teaches first-timers.
- **Icon-only is earned, not assumed.** Reserve it for the few glyphs that are genuinely universal (close, play, search, back) or for dense expert tools where repeated use builds memory and space is scarce. Even then, a tooltip on hover and a real accessible name are mandatory, so the meaning is one hover or one screen-reader pass away.
- **The label is the primary signal; the icon supports it.** When both are present, the word carries meaning and the icon adds speed and recognizability. Design the pair so the icon reinforces the word, never competes with it.

## Filled versus outlined semantics

Fill is not only a style toggle; used with discipline it carries state, and used carelessly it just adds noise.

- **Outlined and filled as a state pair.** A common and legible pattern: outlined for the inactive or unselected state, filled for the active, selected, or current state. The filled bottom-nav tab, the filled bookmark once saved. The weight change reads instantly as "this one is on," carrying selection through a channel other than color, which also serves colorblind users.
- **Pick one base style and commit.** Whether the set is fundamentally outlined or fundamentally filled is a brand decision (outlined reads lighter and more technical, filled reads friendlier and more solid). Hold it across the set; a screen mixing outlined and filled icons with no semantic reason looks accidental.
- **Keep the pair optically matched.** A filled glyph carries more ink and looks heavier and larger than its outlined twin at the same bounds. Tune the filled version slightly so the switch between states does not make the icon jump in size or weight.
- **Do not overload fill with multiple meanings.** If fill signals selection, it cannot also signal a category, or the meaning blurs. One job per channel.

## Build your own set or adopt one

Most products should adopt a good open set and stay disciplined; a custom set is a real, ongoing commitment.

- **Adopt when the set is a tool, not the brand.** For app UI and dashboards, a mature open set (the kind with hundreds of consistent glyphs, multiple weights, and clear licensing) buys instant coverage and consistency you would spend months rebuilding. This is the right default. Never assemble a UI from mixed sources, one icon from here, one from there; the drifting stroke and grid announce it immediately.
- **Adopt as a system, not a grab bag.** Take the whole family so stroke, grid, and hand stay uniform. When the set lacks a glyph you need, draw the new one *to the adopted set's specs*, its grid, stroke, corner, and terminal, so it disappears into the family rather than standing out.
- **Build your own when icons are a brand asset.** A custom set is worth it when the iconography carries brand distinctiveness (a marketing surface, a product where the icon language is part of the identity) and you can fund the drawing, the optical tuning, the small-size versions, and the long tail of new glyphs forever. It is a typeface-sized undertaking, not a weekend.
- **Consistency beats bespoke.** A disciplined adopted set always beats a half-finished custom one. The failure mode of "we made our own" is a beautiful core of twelve icons surrounded by mismatched additions drawn under deadline. If you cannot hold the standard across the whole set and its future, adopt.

## Accessibility

An icon is not accessible because it is visible. The meaning has to reach every user and every input.

- **Every meaningful icon needs an accessible name.** An icon-only button must expose its purpose to assistive tech (an `aria-label` or equivalent, "Delete", "Search"), because a screen reader announces the name, not the shape. A purely decorative icon should be hidden from assistive tech so it is not announced as noise. Decide which each icon is.
- **A 44px hit target for a 20px glyph.** The visible icon can be small; the touchable area cannot. Give every interactive icon at least a 44 by 44px (or 48dp) hit target by padding the region around the glyph, even when the drawing is 20px. Fitts's law is unforgiving on touch, and a tiny tap target is the fastest way to make an interface feel cheap and frustrating.
- **Do not carry meaning by icon color alone.** A status conveyed only by a green versus red dot fails colorblind users. Pair it with a shape difference (the outlined-versus-filled or distinct glyphs), a label, or position, so the meaning survives without hue, exactly as the grayscale test demands elsewhere.
- **Icon contrast is real contrast.** A glyph must clear meaningful contrast against its background, near the 3:1 that non-text UI needs, or it disappears for low-vision users. A light-gray icon on white may look elegant and be effectively invisible.
- **Respect size at zoom.** Icons paired with text should scale with the text when the user zooms, not stay pinned at a fixed pixel size while the words around them grow.

## Restrained icon motion

Icons can move, and when the motion clarifies a change it is a mark of craft. When it performs, it is noise.

- **Animate meaningful transitions.** A hamburger morphing into a close X, a chevron rotating as a section expands, a checkbox drawing its check, a heart filling when favorited: each shows a state change and helps the eye follow what happened. This is motion doing its job, tied to a real transition.
- **Follow the motion physics.** Use real easing and keep it fast, under roughly 200 to 300ms for a small glyph, with natural deceleration, never a linear crawl, per `motion_and_feel.md`. A small element should feel quick; a slow icon animation reads as sluggish.
- **Restraint above all.** Do not loop, pulse, bounce, or spin icons for decoration or to beg for attention. A perpetually animating icon is visual noise that trains the eye to ignore it and undoes the calm the rest of the design worked for. Motion is a scalpel here, reserved for genuine state changes and the rare, earned moment of delight.
- **Honor reduced motion.** When the user asks for reduced motion, drop icon animation to a simple state swap. The meaning must never depend on the animation playing.
