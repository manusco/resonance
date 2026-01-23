# Modern Component Patterns

> **Objective**: Standardize React component creation with Suspense-first architecture.

## 1. Core Principles

### 1. Lazy Load Everything Heavy
**❌ Anti-Pattern**: Importing everything at the top level.
**✅ Standard**: Lazy load heavy components (DataGrid, Charts, Editors).
```typescript
const HeavyChart = React.lazy(() => import('./HeavyChart'));
```

### 2. No Early Returns (Suspense)
**❌ Anti-Pattern**: `if (isLoading) return <Spinner />` (Causes layout shift).
**✅ Standard**: Use `<Suspense>` boundaries. Let the parent handle loading states.

### 3. useSuspenseQuery
**❌ Anti-Pattern**: handling `isLoading` and `error` manually in every component.
**✅ Standard**: Use `useSuspenseQuery`. It assumes success (data is defined) or throws to ErrorBoundary/Suspense.
```typescript
const { data } = useSuspenseQuery({ queryKey: ['user'], queryFn: fetchUser });
// 'data' is always defined here
```

### 4. File Organization
**Standard**: `features/` vs `components/`.
*   `features/{name}/`: Domain-specific logic (API, hooks, types).
*   `components/`: Reusable, domain-agnostic UI.

---

## 2. Component Template

```typescript
import React, { useCallback } from 'react';
import { Box, Paper } from '@mui/material';
import { useSuspenseQuery } from '@tanstack/react-query';
import type { User } from '~types/user';

interface UserCardProps {
    userId: string;
}

export const UserCard: React.FC<UserCardProps> = ({ userId }) => {
    // 1. Data Fetching (Suspense assumes success)
    const { data: user } = useSuspenseQuery({
        queryKey: ['user', userId],
        queryFn: () => userApi.get(userId),
    });

    // 2. Handlers
    const handleClick = useCallback(() => {
        console.log('Clicked', user.name);
    }, [user.name]);

    // 3. Render
    return (
        <Paper sx={{ p: 2 }}>
            <Box onClick={handleClick}>{user.name}</Box>
        </Paper>
    );
};
```
