#!/usr/bin/env python3
"""
Resonance - generic model CLI adapter for run_evals.py and improve.py.

Turns any OpenAI-compatible chat endpoint into the contract the eval tools expect
("read a prompt on stdin, print the completion on stdout"), with the lessons that
cost real debugging time baked in so nobody re-learns them:

  - Force UTF-8 on stdin AND stdout. On Windows the default is cp1252, which throws
    or corrupts on the non-ASCII bytes in skill bodies (the warning emoji, the euro
    sign, umlauts), turning a good answer into an empty one and a false zero score.
  - Send a browser User-Agent. Cloudflare-fronted gateways return 403 (error 1010)
    on a bare urllib User-Agent.
  - Send ONLY {model, messages} by default. Several gateways return 500 on a request
    that includes temperature or max_tokens.
  - Retry on 429 / 5xx / empty completion with backoff.

Configure with environment variables (never hardcode a key):
  MODEL_API_KEY   required; also read from OPENAI_API_KEY / ANTHROPIC_API_KEY /
                  OPENROUTER_API_KEY / OPENCODE_GO_API_KEY if MODEL_API_KEY is unset
  MODEL_BASE_URL  OpenAI-compatible root, e.g. https://api.openai.com/v1
  MODEL_NAME      e.g. gpt-4o, glm-5, deepseek-v4-pro
  MODEL_EXTRA     optional JSON of extra body params, only if your gateway accepts them

Usage:
  MODEL_BASE_URL=... MODEL_NAME=... MODEL_API_KEY=... \
  RESONANCE_MODEL_CMD="python .forge/exec/model_cli.py" \
  python .forge/run_evals.py --all --score
"""
import sys, os, json, time, urllib.request, urllib.error

try:
    sys.stdin.reconfigure(encoding="utf-8", errors="replace")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def env(*names, default=""):
    for n in names:
        v = os.environ.get(n)
        if v:
            return v
    return default


KEY = env("MODEL_API_KEY", "OPENAI_API_KEY", "ANTHROPIC_API_KEY", "OPENROUTER_API_KEY", "OPENCODE_GO_API_KEY")
BASE = env("MODEL_BASE_URL", default="https://api.openai.com/v1").rstrip("/")
MODEL = env("MODEL_NAME", default="gpt-4o")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")


def main():
    if not KEY:
        sys.stderr.write("model_cli: no API key (set MODEL_API_KEY)\n"); return 2
    prompt = sys.stdin.read()
    body = {"model": MODEL, "messages": [{"role": "user", "content": prompt}]}
    extra = env("MODEL_EXTRA")
    if extra:
        try:
            body.update(json.loads(extra))
        except Exception:
            pass
    data = json.dumps(body).encode("utf-8")
    headers = {"Authorization": "Bearer " + KEY, "Content-Type": "application/json",
               "Accept": "application/json", "User-Agent": UA}
    req = urllib.request.Request(BASE + "/chat/completions", data=data, headers=headers)
    n = 8
    for attempt in range(n):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                d = json.load(r)
            content = d["choices"][0]["message"]["content"]
            if not content and attempt < n - 1:
                time.sleep(min(30, 5 * (attempt + 1))); continue
            sys.stdout.write(content or "")
            return 0
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < n - 1:
                time.sleep(min(30, 5 * (attempt + 1))); continue
            sys.stderr.write(f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:300]}\n")
            return 1
        except Exception as e:
            if attempt < n - 1:
                time.sleep(min(30, 5 * (attempt + 1))); continue
            sys.stderr.write(f"error: {e}\n")
            return 1
    return 1


if __name__ == "__main__":
    sys.exit(main())
