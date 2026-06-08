# Assertion Layers Reference

> **Purpose**: Tests fail when they assert at the wrong layer. This reference defines the 6 assertion layers and provides framework-specific examples for choosing the right one.

## Contents

- [The 6 Layers](#the-6-layers)
- [Framework-Specific Examples](#framework-specific-examples)
- [Decision Flowchart](#decision-flowchart)
- [Common Mistakes](#common-mistakes)

## The 6 Layers

| Layer | What It Proves | When To Use | Risk If Misused |
|:---|:---|:---|:---|
| **1. Behavior** | End-to-end user journey works | Critical paths (login, checkout, signup) | Slow; use sparingly |
| **2. Visible State** | User sees the correct content/state | UI feedback, error messages, form states | None; this is the gold standard for UI |
| **3. Data State** | Database/session/store is correct | After mutations (create, update, delete) | Doesn't prove user saw anything |
| **4. Redirect Contract** | Request leads to correct destination | Auth flows, form submissions, error handling | Doesn't prove destination page works |
| **5. Rendered Output** | Page contains specific text/elements | Content verification, SEO checks | Breaks on markup changes |
| **6. Source Template** | Raw template/HTML structure is correct | Design system enforcement, accessibility | Breaks on every visual change |

> 🔴 **Rule**: Always assert at the **highest applicable layer**. Drop to lower layers only when the higher layer doesn't apply or can't be tested efficiently.

---

## Framework-Specific Examples

### React (Testing Library + Vitest/Jest)

**Layer 2 — Visible State (Preferred)**
```jsx
// ✅ Tests what the user sees
import { render, screen } from '@testing-library/react';

test('shows error when email is invalid', async () => {
  render(<LoginForm />);
  await userEvent.type(screen.getByLabelText('Email'), 'not-an-email');
  await userEvent.click(screen.getByRole('button', { name: 'Sign In' }));
  expect(screen.getByRole('alert')).toHaveTextContent('Please enter a valid email');
});
```

**Layer 6 — Source Template (Avoid)**
```jsx
// ❌ Breaks on any class name, wrapper, or markup change
test('renders login form', () => {
  const { container } = render(<LoginForm />);
  expect(container.querySelector('.login-form__input--email')).toBeTruthy();
  expect(container.innerHTML).toContain('<button class="btn-primary">');
});
```

**Layer 3 — Data State (When UI isn't the point)**
```jsx
// ✅ Correct use: testing a hook/store, not a component
test('addToCart updates cart state', () => {
  const { result } = renderHook(() => useCart());
  act(() => result.current.addItem({ id: 'abc', qty: 2 }));
  expect(result.current.items).toHaveLength(1);
  expect(result.current.total).toBe(2);
});
```

---

### Laravel / PHP (Pest/PHPUnit)

**Layer 1 — Behavior (E2E)**
```php
// ✅ Full user journey: login → redirect → see dashboard
test('authenticated user can access dashboard', function () {
    $user = User::factory()->create();

    $this->actingAs($user)
         ->get('/dashboard')
         ->assertOk()
         ->assertSee('Welcome back');
});
```

**Layer 4 — Redirect Contract**
```php
// ✅ Tests auth redirect precisely
test('guests are redirected to login', function () {
    $this->get('/dashboard')
         ->assertRedirect('/login'); // Exact destination, not just "is redirect"
});
```

**Layer 3 — Data State**
```php
// ✅ Tests that the mutation actually persisted
test('creating an application stores the record', function () {
    $user = User::factory()->create();

    $this->actingAs($user)
         ->post('/applications', ['company' => 'Acme', 'pitch' => 'We build rockets'])
         ->assertRedirect('/applications/success');

    $this->assertDatabaseHas('applications', [
        'user_id' => $user->id,
        'company' => 'Acme',
    ]);
});
```

**Layer 2 — Visible State (Blade assertions)**
```php
// ✅ Asserts what the user sees, not raw Blade syntax
test('error message appears for invalid input', function () {
    $this->post('/applications', []) // Missing required fields
         ->assertSessionHasErrors(['company', 'pitch']);

    // Better: follow redirect and check visible text
    $this->post('/applications', [])
         ->assertRedirect()
         ->followRedirects()
         ->assertSee('The company field is required');
});
```

**Layer 6 — Source Template (Avoid)**
```php
// ❌ Asserts raw Blade template output — breaks on any markup change
test('form has company field', function () {
    $response = $this->get('/applications/create');
    $this->assertStringContainsString(
        '<input type="text" name="company" class="form-input"',
        $response->getContent()
    );
});
```

---

### Astro / Static Site

**Layer 2 — Visible State (via Playwright)**
```typescript
// ✅ Tests what the visitor sees in the browser
test('homepage shows event date', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByRole('heading', { level: 1 })).toContainText('2026');
  await expect(page.locator('[data-testid="event-date"]')).toBeVisible();
});
```

**Layer 5 — Rendered Output (Acceptable for SEO/content)**
```typescript
// ✅ Acceptable: verifying SEO-critical content exists in rendered HTML
test('meta description exists', async ({ page }) => {
  await page.goto('/');
  const meta = page.locator('meta[name="description"]');
  await expect(meta).toHaveAttribute('content', /Premier GameTech/);
});
```

**Layer 5 — Rendered Output (For build-time checks)**
```typescript
// ✅ Acceptable: checking build output for critical content
import { readFile } from 'fs/promises';

test('sitemap includes all pages', async () => {
  const sitemap = await readFile('dist/sitemap.xml', 'utf-8');
  expect(sitemap).toContain('<loc>https://example.com/speakers</loc>');
  expect(sitemap).toContain('<loc>https://example.com/apply</loc>');
});
```

---

### Vue (Testing Library + Vitest)

**Layer 2 — Visible State (Preferred)**
```typescript
// ✅ Tests what user sees
import { render, screen } from '@testing-library/vue';

test('counter increments on click', async () => {
  render(Counter, { props: { initial: 0 } });
  await userEvent.click(screen.getByRole('button', { name: 'Increment' }));
  expect(screen.getByText('Count: 1')).toBeInTheDocument();
});
```

**Layer 6 — Source Template (Avoid)**
```typescript
// ❌ Asserts internal component structure
import { mount } from '@vue/test-utils';

test('has counter span', () => {
  const wrapper = mount(Counter);
  expect(wrapper.find('.counter__value').exists()).toBe(true); // Breaks on class rename
  expect(wrapper.html()).toContain('<span class="counter__value">0</span>');
});
```

---

## Decision Flowchart

```
Is this a critical user journey (login, checkout, signup)?
  → YES: Layer 1 (Behavior / E2E)
  → NO: ↓

Does the test verify what the user *sees* or *experiences*?
  → YES: Layer 2 (Visible State — getByRole, assertSee, getByText)
  → NO: ↓

Does the test verify data was correctly persisted or session state changed?
  → YES: Layer 3 (Data State — assertDatabaseHas, expect(store))
  → NO: ↓

Does the test verify the user lands on the right page/URL?
  → YES: Layer 4 (Redirect Contract — assertRedirect, expect(location))
  → NO: ↓

Does the test verify content exists in rendered HTML (SEO, accessibility)?
  → YES: Layer 5 (Rendered Output — toContain, meta tags, sitemap)
  → NO: ↓

Is the template structure itself the invariant you're guarding?
  → YES: Layer 6 (Source Template — only for design system enforcement)
  → NO: You probably don't need this test.
```

---

## Common Mistakes

| Mistake | Why It's Wrong | Fix |
|:---|:---|:---|
| `expect(response.status).toBe(200)` alone | Proves nothing about content or behavior | Add body/content assertions |
| Snapshot tests on full components | Break on every visual change; train devs to blindly update | Use Layer 2 assertions instead |
| `wrapper.html().toContain('<div class=')` | Couples test to markup structure | Use `getByRole`, `getByText`, or `assertSee` |
| `expect(spy).toHaveBeenCalledWith(...)` as sole assertion | Tests implementation, not outcome | Add a Layer 2 or 3 assertion alongside |
| `assertSessionHasErrors()` without following redirect | Proves validation ran, not that user saw the error | Follow redirect and `assertSee()` the message |
