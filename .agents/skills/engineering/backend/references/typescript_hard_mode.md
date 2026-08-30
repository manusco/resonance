# TypeScript Hard Mode Protocol

> "If it fits, it sits. But make it fit TIGHT."

## 1. Branded Types (The Nominal Hack)
TypeScript is structural. `string` is `string`. But `UserId` != `PostId`.

```typescript
declare const __brand: unique symbol
type Brand<K, T> = K & { [__brand]: T }

export type UserId = Brand<string, 'UserId'>
export type PostId = Brand<string, 'PostId'>

function getUser(id: UserId) { ... }

// Usage
const id = "123" as UserId // Valid
const postId = "456" as PostId
getUser(postId) // ERROR. Safe.
```

## 2. Generics with Inference
Don't make users type `<User>`. Let TS infer it.

**Bad:**
```typescript
function getRow<T>(data: T[]) { ... }
getRow<User>(users)
```

**Elite:**
```typescript
function getRow<T extends { id: string }>(data: T[]) { ... }
getRow(users) // Inferred.
```

## 3. The `const` Assertion
Freeze literal values for discrimination.

```typescript
const routes = {
  HOME: '/',
  ADMIN: '/admin'
} as const;

type Route = typeof routes[keyof typeof routes]; // '/' | '/admin'
```

## 4. Derived Types (Single Source of Truth)
Never write a type manually if you can derive it from Zod or Code.

*   `type User = z.infer<typeof UserSchema>`
*   `type Props = ComponentProps<typeof Button>`

## 5. Preserve Type Evidence

Do not take a precise value, widen it to `unknown`, `object`, `{}`, or an open
dictionary, then cast it back later. That pattern deletes evidence the compiler
already had and replaces it with trust.

**Bad:**
```typescript
const rawUser: unknown = { id: "u_123", email: "a@example.com" }
const user = rawUser as User
```

**Good:**
```typescript
const user = UserSchema.parse({ id: "u_123", email: "a@example.com" })
```

For known in-process values, keep inference or use `satisfies` when you need to
check a contract without losing literal information.

```typescript
const handlers = {
  invoicePaid: handleInvoicePaid,
} satisfies Record<string, Handler>
```

`unknown` is correct at trust boundaries: request bodies, webhooks, file input,
message queues, third-party SDK responses, and `catch` causes. Parse it once at
the boundary, then pass the named domain type through the rest of the code.

Every remaining `as` assertion must have a reason the type system cannot express:
a branded constructor, a parser invariant, or a narrow interop boundary. If the
same result can be produced with parsing, inference, `satisfies`, or `as const`,
the assertion is not justified.

> **Rule**: Never use `any`. Use `unknown` only at a boundary, and do not erase
> known type evidence only to reconstruct it with `as`.
