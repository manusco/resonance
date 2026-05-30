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

> 🔴 **Rule**: If you use `any`, you are fired. Use `unknown` or a Generic.
