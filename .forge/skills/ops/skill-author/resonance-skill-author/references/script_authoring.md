# Script authoring (push fragility into code)

The Resonance bet: an LLM step is ~90% reliable, so five chained steps are ~59%.
Deterministic code does not compound error. When a step is fragile, order-sensitive,
or must be identical every time, write a script and have the skill run it.

## Solve, do not punt

A script handles its own error conditions. It does not fail and leave the model to
guess.

Good:
```python
def read_config(path):
    try:
        return open(path).read()
    except FileNotFoundError:
        print(f"{path} not found, creating default")
        open(path, "w").write("")
        return ""
```
Bad:
```python
def read_config(path):
    return open(path).read()   # explodes, model left to figure it out
```

## No voodoo constants

Every magic number carries its reason. If you cannot justify the value, the model
cannot either.

Good:
```python
REQUEST_TIMEOUT = 30   # slow CI runners occasionally need ~25s
MAX_RETRIES = 3        # most intermittent failures clear by the 2nd retry
```
Bad: `TIMEOUT = 47  # ?`

## Plan -> validate -> execute

For batch or destructive work, have the model emit a plan file, validate it with a
script, then execute. Catch errors before they touch anything real. Make validation
verbose: "field 'signature_date' not found; available: name, total, date_signed".

## Execute vs read

Be explicit about intent:
- "Run `analyze.py` to extract fields" (execute; output is cheap, code stays out of context).
- "See `analyze.py` for the algorithm" (read as reference).

## Portability

Scripts are the cross-tool, cross-model anchor; they run the same under any model.
Keep them stdlib where you can, forward-slash paths, no OS assumptions. A validator
or grader written once protects every skill, on every tool.