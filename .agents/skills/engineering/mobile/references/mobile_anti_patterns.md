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
| **Target below the applicable platform or accessibility criterion** | May be hard to activate in the actual context | Use target platform guidance and applicable accessibility criteria. WCAG 2.2 AA is 24×24 CSS px or spacing, with exceptions; iOS and Android guidance uses platform-specific point/dp units and may recommend larger targets |
| **Insufficient separation for the controls and context** | Accidental taps become more likely | Test spacing with realistic content and target devices; do not treat one gap value as universal |
| **Missing feedback for a meaningful pending operation** | The user cannot tell whether the action registered | Show status when waiting affects understanding or recovery; avoid redundant or disruptive loading UI for work that completes immediately |
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
