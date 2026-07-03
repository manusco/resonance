# Data Visualization and Charts

> A chart is an argument made of ink. It exists to answer one question faster than a table could, and every mark either serves that answer or gets in its way. Most charts fail not because the data is wrong but because the encoding fights the eye: the wrong channel carries the important number, the baseline lies, the color means nothing, and a legend forces a lookup the design should have removed. Encode by how the eye actually measures, tell the truth with proportion, and strip everything that is not the point.

## Contents
- The perceptual encoding hierarchy
- Let the question choose the chart
- Truthful axes and proportional ink
- Perceptual color for data
- Declutter: the data-ink ratio
- Direct labeling over legends
- Small multiples
- Exploratory dashboards vs explanatory charts
- Accessibility
- Responsive and interactive behavior
- The tells of a generated chart

## The perceptual encoding hierarchy

The eye reads some visual channels precisely and others only vaguely. This ranking is the foundation of the whole craft, established by how accurately people decode each channel back into a number:

1. **Position along a common scale.** The most accurate. A dot or bar end on a shared axis. This is why scatter plots and aligned bars win.
2. **Position on non-aligned scales.** Same channel, separate panels. Slightly harder because the eye bridges a gap. This is the cost small multiples pay for their clarity.
3. **Length.** A bar read by its own extent. Accurate, but only when it starts from zero, because length *is* the value.
4. **Angle and slope.** Pie slices and line gradients. The eye judges these loosely; two slices within ten percent of each other are hard to rank.
5. **Area.** Bubbles and treemaps. People systematically underread area, so a circle with four times the value looks maybe twice as big. Use only when position and length cannot.
6. **Color hue and saturation.** The weakest for quantity. Excellent for category and for a single called-out state, poor for "how much."

The discipline: **put the comparison that matters on the highest channel available.** If the reader's real question is "which is biggest," give them position or length, not area or color. When you catch yourself encoding the key variable as bubble size or a heat tint, you have usually pushed the most important number onto the weakest channel. Reserve the low channels for secondary dimensions.

## Let the question choose the chart

The chart type is not a style choice. It is dictated by the question the reader arrives with. Name the question first, then the form follows:

- **Comparison between items** (which is largest, rank them): bar chart, sorted by value, not alphabetically, unless the category has its own natural order.
- **Change over time** (trend, trajectory): line chart. Time on the x-axis, always left to right. Reserve area fill for when the magnitude under the line is itself the point.
- **Relationship between two variables** (does x drive y): scatter plot. Add a trend line only when it clarifies rather than implies causation.
- **Composition, part to whole** (what share): a stacked bar or, for one moment in time with very few parts, a pie. A pie with more than about five slices is a table wearing a costume. If parts change over time, use a stacked area or a set of stacked bars, never a row of pies.
- **Distribution** (spread, shape, outliers): histogram for one variable, box or violin for comparing distributions across groups.
- **Flow or movement between states**: Sankey or a slope chart.

Two rules override the menu. **A well-labeled table often beats a chart** when there are few numbers and the reader wants exact values; do not chart four numbers out of reflex. And **the goal decides everything**: the same dataset becomes a ranked bar to argue "we lead the category" and a line to argue "we are pulling away." Choose the form that carries your actual point, then make sure that point is honest.

## Truthful axes and proportional ink

The chart's credibility lives here. Break these and the design lies, whether or not you meant to.

- **Bar charts start at zero. No exceptions.** A bar encodes its value as length, so a truncated baseline exaggerates differences by exactly the amount you cropped. A jump from 52 to 54 on a bar chart with a baseline at 50 looks like a doubling. This is the single most common way charts deceive.
- **Line charts may use a non-zero baseline** because a line encodes value by position, not length, and a zoomed y-axis is the honest way to reveal a real but small movement. Make the zoom visible: label the axis clearly so no one mistakes the frame. When you crop, you are choosing the story; choose it in good faith.
- **Proportional ink, generally.** The amount of ink representing a value should scale with the value. This is why 3D bars, bars on a broken axis, and inflated bubble scales mislead: the ink no longer matches the number.
- **One y-axis where you can.** Dual axes let you manufacture a correlation by sliding two scales until the lines cross where you want. If you must show two series in different units, prefer indexing both to a common base (percent change from a start point) on a single axis.
- **Do not distort area.** When area does carry the value, scale by area, not by radius or by height, or large values balloon.
- **Order carries meaning.** Sorting bars by value is itself information. An unsorted categorical axis wastes the reader's most accurate channel on alphabetical noise.

## Perceptual color for data

Color in a chart is data, not decoration, so the same perceptual discipline from `color_and_contrast.md` applies: think in OKLCH lightness, because the eye reads lightness far more reliably than hue, and HSL will lie to you about which steps look even. Three scale types, three different jobs:

- **Sequential** (low to high of one quantity): a single hue ramped in even OKLCH lightness steps from light to dark. Even lightness spacing is what makes the steps *look* evenly spaced; ramps built in HSL clump and gap. Dark reads as "more" on a light background.
- **Diverging** (deviation from a meaningful center, like zero or a target): two sequential ramps meeting at a light, low-chroma midpoint. The center must sit at the value that matters, or the color misstates where neutral is. Keep the two arms balanced in lightness so neither side falsely dominates.
- **Categorical** (unordered groups): distinct hues held at roughly *equal* lightness and chroma, so no category looks heavier or more important than another. Unequal lightness in a categorical palette silently ranks things that have no rank. Cap it near seven or eight colors; beyond that, hues stop being distinguishable and you should group, facet, or directly label instead.

Colorblind safety is not optional. Red and green sit adjacent for the most common color vision deficiency, so a red-versus-green scale is unreadable for a meaningful slice of any audience. Build ramps that vary in **lightness as well as hue**, so they survive when hue is removed, and lean on blue-orange for diverging scales, which stays legible across the common deficiencies. The real test: **render the chart in grayscale.** If the categories or steps are still tellable apart, the encoding does not depend on hue. If they collapse into the same gray, redesign before shipping. Pair color with a second channel, position, a direct label, a shape, or a texture, so color is reinforcement, never the sole carrier of meaning.

## Declutter: the data-ink ratio

Every pixel that is not data is a tax on the reader's attention. Maximize the share of ink that carries information, and delete the rest without mercy.

- **Kill chartjunk.** No 3D extrusion, no drop shadows on bars, no gradient fills that carry no data, no decorative background images, no skeuomorphic gauges. These add nothing measurable and actively distort by adding ink that means nothing.
- **Gridlines recede or disappear.** They are scaffolding, not content. If you keep them, make them hairlines at low opacity so they sit far behind the data. Often you can drop them entirely and let a few labeled ticks do the work. Never let a gridline out-contrast the line it is meant to support.
- **Drop the chart border and heavy axis lines.** A full box around a plot is almost always removable. The data defines its own edges. An axis line can often go too once ticks are labeled.
- **Fewer ticks, rounder numbers.** The axis needs enough ticks to orient, not a label on every increment. Round to human numbers (0, 25, 50, 75, 100), not machine ones (0, 23.7, 47.4).
- **Redundant encoding is waste, not safety.** A legend that repeats what a direct label already says, an axis title restating an obvious unit: cut it. Say each thing once, in the place the eye already looks.

Restraint here mirrors the whole design philosophy: remove until the chart breaks, then add back the one thing it needed.

## Direct labeling over legends

A legend is a lookup table, and every glance at it is a round trip the reader's eye pays for: read the line, travel to the legend, match the color, travel back, lose the place. Remove the trip.

- **Label the thing at the thing.** Put each line's name at the end of that line. Tag the notable bar with its value on or beside it. The reader never leaves the data.
- **A legend is a fallback**, acceptable when direct labels would collide or when there are truly too many series to tag. Even then, order the legend to match the visual order of the series (topmost line, topmost legend entry) so the mapping is guessable.
- **Annotate the insight.** The strongest explanatory charts write the point on the chart: a short note pointing at the spike that says what happened and why. You are not making the reader find the story; you are telling it, with the evidence underneath. One well-placed sentence of annotation often does more than any amount of styling.
- **Label the outlier, not every point.** Call out what matters, the peak, the crossover, the anomaly, and let the rest stay quiet. Labeling everything is the same failure as bolding everything: nothing leads.

## Small multiples

When you need to compare many groups across the same variable, do not cram every series into one plot until it becomes a plate of spaghetti. Repeat one small chart once per group, in a grid.

- **Same scale on every panel, always.** The comparison only works if the axes are shared. The instant one panel rescales to fit its own data, the grid becomes a lie, because equal heights no longer mean equal values.
- **Sort the panels meaningfully.** Order the grid by a value that helps, size, recency, magnitude of change, so position in the grid is itself a signal, not arbitrary placement.
- **Keep each panel spare.** Label the axes once at the edge of the grid, not on all twelve panels. Each small chart carries only its own line and its own title. The power of the technique is that the shared structure fades and only the differences between panels light up.
- Small multiples trade one hard comparison (many lines, one axis) for many easy ones (one line each, read across a grid), spending only a little accuracy at the panel gap. For more than three or four series, this trade almost always wins over an overloaded single chart.

## Exploratory dashboards vs explanatory charts

These are two different products with two different bars, and confusing them is why most dashboards feel busy and most report charts feel thin.

- **Exploratory** is for finding: a dashboard or a notebook where the analyst does not yet know the answer. Density is acceptable, even useful. Interaction (filter, zoom, brush, drill) carries the load, because the reader steers. The designer's job is a clear default view, honest defaults, and controls that do not mislead. It is a tool.
- **Explanatory** is for telling: one chart, one point, aimed at a reader who will spend seconds, not minutes. Here you cut to a single clear message, annotate the takeaway, strip every non-essential mark, and remove interaction the reader does not need. It is an argument.
- **Do not ship an exploratory dashboard when the audience needed one explanatory chart.** A wall of twelve widgets handed to an executive is an abdication: you found no story, so you made them do it. When you know the point, make the point. Reserve the dashboard for the people whose job is to dig.
- A dashboard is not twelve charts on a screen. It is a hierarchy: the one or two numbers that matter most, large and first, then supporting detail below, with the same contrast discipline as any other design. Most dashboards fail the squint test because everything is the same size.

## Accessibility

A chart that only works for a sighted reader with typical color vision on a large screen is unfinished.

- **Contrast applies to data marks, not only text.** Lines, bars, and points must clear a meaningful contrast against the plot background, roughly the 3:1 that non-text UI needs, or thin light-on-light series vanish. Axis labels and annotations are text and answer to full text contrast.
- **Never encode by color alone.** Add a second channel: distinct line styles (solid, dashed), point shapes, direct labels, or texture. This serves colorblind readers and anyone glancing quickly, and it is the same rule the grayscale test enforces.
- **Provide the table.** Every chart should have an accessible equivalent of its data, a real data table behind or beneath it, so a screen reader and a keyboard user reach the numbers. The chart is a fast path to the data, not the only path.
- **Describe the chart in text.** A short text summary of the takeaway ("revenue rose each quarter, fastest in Q3") serves assistive tech and doubles as the annotation a sighted reader wants anyway. Give the image a real accessible name and description, not "chart.png."
- **Do not rely on hover to reveal essential values.** Hover tooltips are unavailable on touch and to keyboard users. Anything essential must be readable without them, through direct labels or the table.

## Responsive and interactive behavior

A chart lives at many sizes, and it must degrade with intent rather than by accident.

- **Reflow, do not just shrink.** A dense multi-series line chart squeezed onto a 360px phone becomes unreadable. Show fewer series, thin the ticks, rotate or truncate labels sensibly, or switch to a form that fits the width. The mobile chart is a redesign, not a scale transform.
- **Preserve the axis and the labels.** When space is tight, the first instinct is to drop labels; resist it. A chart with no readable axis is decoration. Cut data series or aggregate the time buckets before you cut the reader's ability to read the scale.
- **Interaction must add, never gate.** Tooltips, zoom, and filters are enhancements over a chart that already communicates its main point statically. If the core message only appears after the reader hovers or clicks, the default view has failed.
- **Motion clarifies transitions, it does not perform.** When data updates or a filter changes the view, animate marks from old position to new so the eye can track what moved, using real easing under 400ms as in `motion_and_feel.md`. Do not animate bars growing from zero on every load as a flourish; that is decoration that delays the read.
- **Respect reduced-motion and touch.** Honor the reduced-motion preference by cutting transition animation. Give touch its own affordances (tap to reveal, larger hit areas) rather than assuming a hoverable pointer.

## The tells of a generated chart

The chart equivalent of AI slop, refuse each on sight:

- A truncated bar-chart baseline that inflates small differences.
- The library's default rainbow categorical palette, unequal in lightness and hostile to colorblind readers.
- A legend the design should have replaced with direct labels.
- Heavy full gridlines and a boxed border out-contrasting the data.
- A pie chart with eight nearly equal slices.
- 3D bars, drop shadows, or gradient fills that carry no data.
- Dual y-axes staging a correlation that is not there.
- A twelve-widget dashboard shipped where one annotated chart was the answer.
- Every data point labeled, so none of them leads.
- No table fallback, no text summary, no non-color encoding.
