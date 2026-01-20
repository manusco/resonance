# NestJS Module Pattern (Enterprise)

> "Structure for scale."

## 1. The Atomic Module

Every feature is a module.

```typescript
// cats.module.ts
@Module({
  controllers: [CatsController],
  providers: [CatsService],
  exports: [CatsService], // Explicit Public API
})
export class CatsModule {}
```

## 2. Dependency Injection (DI)

Never import Service Classes directly. Use Interface Tokens.

```typescript
constructor(
  @Inject('ICatsRepository') private repo: ICatsRepository
) {}
```

## 3. The Guard / Interceptor / Pipe Trio

*   **Guard**: AuthN/AuthZ. (Can they pass?)
*   **Interceptor**: Logging / Response Mapping. (Wrap the execution).
*   **Pipe**: Validation / Transformation. (ZodParse).

> 🔴 **Rule**: Controllers should be empty. Move logic to Services.
