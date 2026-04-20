# React Composition Patterns

> "Composition > Inheritance."

## 1. The Slot Pattern (Radix Style)

Instead of passing 50 props (`title`, `subtitle`, `onIconClick`), pass **Children**.

**Bad:**
```tsx
<Card title="Hello" subtitle="World" onAction={...} />
```

**Good (Compound Component):**
```tsx
<Card>
  <Card.Header>
    <Card.Title>Hello</Card.Title>
  </Card.Header>
  <Card.Content>World</Card.Content>
  <Card.Footer>
    <Button>Action</Button>
  </Card.Footer>
</Card>
```

## 2. Polymorphic Components (`as` prop)

Allow a component to change its underlying HTML tag.

```tsx
type Props<E extends React.ElementType> = {
  as?: E;
  children: React.ReactNode;
} & React.ComponentPropsWithoutRef<E>;

function Box<E extends React.ElementType = 'div'>({ as, ...props }: Props<E>) {
  const Component = as || 'div';
  return <Component {...props} />;
}

// Usage
<Box as="section">I am a section</Box>
<Box as="a" href="#">I am a link</Box>
```

## 3. Render Props (Inversion of Control)

Give the parent control over *how* to render data.

```tsx
<List
  items={users}
  renderItem={(user) => (
    <UserCard header={<Badge>{user.role}</Badge>} />
  )}
/>
```

## 4. The Mandate

*   **No Prop Drilling**: If you pass a prop down > 3 levels, use Composition (Slots) or Context.
*   **useEffect Ban**: Do not use `useEffect` for data fetching (Use SWR/TanStack). Do not use `useEffect` for derived state (Use `useMemo` or just variables).

> 🔴 **Rule**: If your component has > 10 props, it is doing too much. Break it up.
