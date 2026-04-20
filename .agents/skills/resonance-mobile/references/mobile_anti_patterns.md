# Mobile Anti-Patterns (The "Sins")

> **Objective**: Avoid common mobile pitfalls. "Mobile is NOT a small desktop."

## 1. Performance Sins
| ❌ NEVER DO | Why It's Wrong | ✅ ALWAYS DO |
|-------------|----------------|--------------|
| **ScrollView for long lists** | Renders ALL items, memory explodes | Use `FlatList` / `FlashList` |
| **Inline renderItem** | New function every render | `useCallback` + `React.memo` |
| **Missing keyExtractor** | Bugs on reorder | Unique, stable ID from data |
| **console.log in prod** | Blocks JS thread | Remove before release |

## 2. Touch/UX Sins
| ❌ NEVER DO | Why It's Wrong | ✅ ALWAYS DO |
|-------------|----------------|--------------|
| **Touch target < 44px** | Impossible to tap | Minimum 44pt (iOS) / 48dp (Android) |
| **Spacing < 8px** | Accidental taps | Minimum 8-12px gap |
| **No loading state** | User thinks app crashed | ALWAYS show loading feedback |
| **No offline handling** | Crash on signal loss | Graceful degradation |

## 3. Security Sins
| ❌ NEVER DO | Why It's Wrong | ✅ ALWAYS DO |
|-------------|----------------|--------------|
| **Auth in AsyncStorage** | Stolen on rooted device | `SecureStore` / `Keychain` |
| **Hardcoded API keys** | Reverse engineered | Env variables |
| **Skip SSL pinning** | MITM attacks | Pin certificates in prod |

## 4. Architecture Sins
| ❌ NEVER DO | Why It's Wrong | ✅ ALWAYS DO |
|-------------|----------------|--------------|
| **Business logic in UI** | Untestable | Service layer separation |
| **Global state abuse** | Complexity | Local state default |
