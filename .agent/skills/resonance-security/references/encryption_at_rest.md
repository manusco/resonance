# Encryption At Rest Protocol

> "If they steal the disk, they steal noise."

## 1. Database (Transparent)

*   **AWS RDS / Cloud SQL**: Enable "Encrypted" flag with KMS Key.
*   **SQLite**: Use SQLCipher or OS-level encryption.

## 2. Application Level (Sensitive Fields)

PII (SSN, API Keys) must be encrypted BEFORE hitting the DB.

```typescript
// Write
const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
const encrypted = cipher.update(ssn, 'utf8', 'hex');

// Read
const decipher = crypto.createDecipheriv('aes-256-gcm', key, iv);
const decrypted = decipher.update(encrypted, 'hex', 'utf8');
```

## 3. Key Management (KMS)

*   **Never** hardcode keys in `.env`.
*   **Rotate** keys annually.
*   **Envelope Encryption**: Use a Master Key (KMS) to encrypt Data Keys.

> 🔴 **Rule**: Hashing != Encryption. Hash passwords (Argon2). Encrypt SSNs (AES).
