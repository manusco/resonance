# Automated Linting Protocol

> "Robots are better at formatting than you."

## 1. The Pre-Commit Hook (Husky)

Do not rely on the developer to remember.
*   **Action**: Install `husky` and `lint-staged`.
*   **Config**:
    ```json
    "lint-staged": {
      "*.{ts,tsx}": ["eslint --fix", "prettier --write"]
    }
    ```

## 2. The Strictness Level

*   **ESLint**: `plugin:@typescript-eslint/recommended-requiring-type-checking`.
*   **No Unused Vars**: Errors, not warnings.
*   **No Console**: Errors in production builds.

## 3. The CI Gate

If `npm run lint` fails, the build fails.
*   **Result**: The PR Button is greyed out.

> 🔴 **Rule**: Never comment "indentation looks off". Let the linter fix it.
