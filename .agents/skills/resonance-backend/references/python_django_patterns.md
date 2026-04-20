# Python & Django Patterns

> "Explicit is better than implicit."

## 1. The Service Layer (Fat Models are Bad)

Don't put business logic in Views or Models. Put it in `services.py`.

```python
# services.py
def create_order(*, user: User, items: list[Item]) -> Order:
    with transaction.atomic():
        order = Order.objects.create(user=user)
        # ... logic
    return order
```

## 2. Pydantic (Type Safety)

Use Pydantic for all data transfer objects (DTOs).

```python
class CreateUserRequest(BaseModel):
    email: EmailStr
    age: PositiveInt
```

## 3. The N+1 Killer

Always use `select_related` (JOIN) and `prefetch_related` (2 Queries).

*   ❌ `for book in books: print(book.author.name)`
*   ✅ `books = Book.objects.select_related('author')`

> 🔴 **Rule**: Zero raw SQL strings. Use the ORM or a Builder.
