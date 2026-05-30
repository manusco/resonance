# Zod Schema Patterns

> "Validate at the edges. Trust the core."

## 1. The Transformation (Parse, don't Verify)

Don't just check if existing data is valid. Transform it into a better format.

```typescript
const BooleanString = z.string()
  .transform((val) => val === 'true'); // "true" -> true

const DateString = z.string()
  .transform((str) => new Date(str)); // "2023-01-01" -> Date Object
```

## 2. The Refinement (Custom Logic)

```typescript
const Password = z.string()
  .min(8)
  .refine((val) => /[!@#$%]/.test(val), {
    message: "Must contain special character"
  });
```

## 3. The Environment Variable Schema

Never use `process.env.API_KEY` directly. It might be undefined.

```typescript
const EnvSchema = z.object({
  DATABASE_URL: z.string().url(),
  PORT: z.coerce.number().default(3000),
});

export const env = EnvSchema.parse(process.env);
// Now 'env.PORT' is guaranteed to be a number.
```

## 4. The Recursive Schema (JSON)

```typescript
type JSONValue = string | number | boolean | { [k: string]: JSONValue } | JSONValue[];

const JSONSchema: z.ZodType<JSONValue> = z.lazy(() =>
  z.union([z.string(), z.number(), z.boolean(), z.record(JSONSchema), z.array(JSONSchema)])
);
```

> 🔴 **Rule**: Inputs from API, Form, or Env MUST be Zod parsed.
