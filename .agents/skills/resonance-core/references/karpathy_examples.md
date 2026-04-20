# Karpathy Examples: Code Walkthroughs

> **Purpose**: Concrete ✅/❌ code examples for the 4 Karpathy behavioral guardrails.
> **Source**: Derived from [Andrej Karpathy's observations](https://x.com/karpathy/status/2015883857489522876) on LLM coding pitfalls.
> **Reference**: See [karpathy_rules.md](karpathy_rules.md) for the condensed principles.

---

## 1. Think Before Coding

### ❌ Anti-Pattern: Hidden Assumptions

**Request**: "Add a feature to export user data"

```python
# LLM silently assumes: ALL users, JSON format, local file, all fields
def export_users(format='json'):
    users = User.query.all()
    if format == 'json':
        with open('users.json', 'w') as f:
            json.dump([u.to_dict() for u in users], f)
```

**Problems**: Assumed scope (all users = privacy risk), assumed file location, assumed fields, assumed format.

### ✅ Pattern: Surface Assumptions First

```
Before implementing, I need to clarify:

1. Scope: Export ALL users or filtered subset? (privacy implications)
2. Format: Did you mean:
   - Download file in browser?
   - Background job with email notification?
   - API endpoint returning data?
3. Fields: Which user fields? (some may be sensitive)
4. Volume: How many users typically? (affects approach)

Simplest approach: An API endpoint returning paginated JSON.
What's your preference?
```

---

### ❌ Anti-Pattern: Multiple Interpretations (Pick Silently)

**Request**: "Make the search faster"

```python
# Silently picks "all of the above" — 200 lines of optimization
@lru_cache(maxsize=1000)
async def search(query: str) -> List[Result]:
    # caching + async + connection pooling all at once
```

### ✅ Pattern: Present Interpretations with Tradeoffs

```
"Make the search faster" could mean:

1. Faster response time (< 100ms instead of 500ms)
   → Add database indexes, cache frequent queries [2 hours]

2. Handle more concurrent searches (throughput)
   → Add async/await, connection pooling [4 hours]

3. Faster perceived speed (UX)
   → Show partial results, progressive loading [3 hours]

Current search: ~500ms for typical queries.
Which aspect matters most?
```

---

## 2. Simplicity First

### ❌ Anti-Pattern: Over-Abstraction

**Request**: "Add a function to calculate discount"

```python
from abc import ABC, abstractmethod
class DiscountStrategy(ABC):
    @abstractmethod
    def calculate(self, amount: float) -> float: pass

class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float):
        self.percentage = percentage
    def calculate(self, amount: float) -> float:
        return amount * (self.percentage / 100)

@dataclass
class DiscountConfig:
    strategy: DiscountStrategy
    min_purchase: float = 0.0
    max_discount: float = float('inf')

class DiscountCalculator:
    def __init__(self, config: DiscountConfig):
        self.config = config
    def apply_discount(self, amount: float) -> float:
        if amount < self.config.min_purchase:
            return 0
        discount = self.config.strategy.calculate(amount)
        return min(discount, self.config.max_discount)
# 30+ lines of setup for a single calculation
```

### ✅ Pattern: Write the Minimum

```python
def calculate_discount(amount: float, percent: float) -> float:
    """Calculate discount amount. percent should be 0-100."""
    return amount * (percent / 100)

# Usage
discount = calculate_discount(100.0, 10.0)  # $10 off
```

> **Rule**: Add complexity only when you actually need multiple discount types. If that requirement comes later, refactor then.

---

## 3. Surgical Changes

### ❌ Anti-Pattern: Drive-by Refactoring

**Request**: "Fix the bug where empty emails crash the validator"

```diff
  def validate_user(user_data):
-     # Check email format
-     if not user_data.get('email'):
+     """Validate user data."""           # ← unrequested docstring
+     email = user_data.get('email', '').strip()
+     if not email:
          raise ValueError("Email required")
-     if '@' not in user_data['email']:
+     if '@' not in email or '.' not in email.split('@')[1]:  # ← unrequested enhancement
          raise ValueError("Invalid email")
-     # Check username
-     if not user_data.get('username'):
+     username = user_data.get('username', '').strip()  # ← unrequested change
+     if not username:
          raise ValueError("Username required")
+     if len(username) < 3:                              # ← NOBODY ASKED FOR THIS
+         raise ValueError("Username too short")
```

**Problems**: Added docstring, enhanced email logic beyond the bug, rewrote username section nobody asked about.

### ✅ Pattern: Surgical Fix Only

```diff
  def validate_user(user_data):
      # Check email format
-     if not user_data.get('email'):
+     email = user_data.get('email', '')
+     if not email or not email.strip():
          raise ValueError("Email required")

      # Basic email validation
-     if '@' not in user_data['email']:
+     if '@' not in email:
          raise ValueError("Invalid email")

      # Check username  ← UNTOUCHED
      if not user_data.get('username'):
          raise ValueError("Username required")

      return True
```

**Only changed**: The specific lines that fix empty email handling.

---

### ❌ Anti-Pattern: Style Drift

**Request**: "Add logging to the upload function"

```diff
- def upload_file(file_path, destination):         # ← changed signature
+ def upload_file(file_path: str, destination: str) -> bool:  # ← unrequested type hints
+     """Upload file to destination with logging."""  # ← unrequested docstring
+     logger.info(f"Uploading {file_path}")
      try:
-         with open(file_path, 'rb') as f:         # ← changed quotes
+         with open(file_path, "rb") as f:
              data = f.read()
-         response = requests.post(destination, files={'file': data})
+         response = requests.post(destination, files={"file": data})  # ← changed quotes
-         if response.status_code == 200:           # ← reformatted logic
-             return True
-         else:
-             return False
+         success = response.status_code == 200     # ← unrequested refactor
+         return success
```

### ✅ Pattern: Match Existing Style

```diff
+ import logging
+ logger = logging.getLogger(__name__)

  def upload_file(file_path, destination):   # ← signature unchanged
+     logger.info(f'Starting upload: {file_path}')  # ← single quotes like the rest
      try:
          with open(file_path, 'rb') as f:   # ← style unchanged
              data = f.read()
          response = requests.post(destination, files={'file': data})
          if response.status_code == 200:
+             logger.info(f'Upload successful: {file_path}')
              return True
          else:
+             logger.error(f'Upload failed: {file_path}, status={response.status_code}')
              return False
      except Exception as e:
-         print(f"Error: {e}")
+         logger.exception(f'Upload error: {file_path}')
          return False
```

**Matched**: single quotes, no type hints, existing boolean pattern.

---

## 4. Goal-Driven Execution

### ❌ Anti-Pattern: Vague Approach

**Request**: "Fix the authentication system"

```
I'll fix the authentication system by:
1. Reviewing the code
2. Identifying issues
3. Making improvements
4. Testing the changes
[Proceeds with no clear success criteria]
```

### ✅ Pattern: Verifiable Goals with `→ verify:` Steps

```
To "fix authentication," I need to define success criteria.
What specific issue are we solving?

If the issue is "users stay logged in after password change":

Plan:
1. Write test: Change password → verify old session invalidated
   → verify: Test FAILS (reproduces the bug)

2. Implement: Invalidate sessions on password change
   → verify: Test PASSES

3. Check edge cases: Multiple active sessions, concurrent changes
   → verify: Additional tests PASS

4. Verify no regression: Existing auth tests still pass
   → verify: Full test suite GREEN

What's the specific auth issue you're seeing?
```

---

### ✅ Pattern: Reproduce-First Bug Fix

**Request**: "The sorting breaks when there are duplicate scores"

```python
# Step 1: Write a test that reproduces the issue FIRST
def test_sort_with_duplicate_scores():
    scores = [
        {'name': 'Alice', 'score': 100},
        {'name': 'Bob', 'score': 100},
        {'name': 'Charlie', 'score': 90},
    ]
    result = sort_scores(scores)
    # The bug: order is non-deterministic for ties
    assert result[0]['score'] == 100
    assert result[2]['score'] == 90

# → verify: Test fails with inconsistent ordering

# Step 2: Fix with stable sort
def sort_scores(scores):
    """Sort by score descending, then name ascending for ties."""
    return sorted(scores, key=lambda x: (-x['score'], x['name']))

# → verify: Test passes consistently
```

---

## Anti-Patterns Summary

| Principle | Anti-Pattern | Fix |
|-----------|-------------|-----|
| Think Before Coding | Silently assumes file format, fields, scope | List assumptions explicitly, ask for clarification |
| Simplicity First | Strategy pattern for single discount calculation | One function until complexity is actually needed |
| Surgical Changes | Reformats quotes, adds type hints while fixing a bug | Only change lines that fix the reported issue |
| Goal-Driven | "I'll review and improve the code" | "Write test for bug X → fail → fix → pass → no regressions" |
