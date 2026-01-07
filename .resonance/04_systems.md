# 04 Systems: The Machinery

## 1. External Systems & Integrations
*List all third-party APIs, services, and external tools that this project depends on.*

- **[System Name]**: [Purpose] (e.g., Stripe for payments, Supabase for DB)
    - *Auth*: [How do we authenticate?]
    - *Key Endpoints*: [Critical API paths]

## 2. Internal Subsystems
*Define the major logical components of the application.*

- **[Module Name]**: [Responsibility]
    - *Input*: [What data does it take?]
    - *Output*: [What does it produce?]
    - *Dependencies*: [What other modules does it need?]

## 3. Data Infrastructure
*Map the flow of data through the system.*

- **Database**: [Postgres / Firebase / Local JSON]
- **Storage**: [S3 / Local File System]
- **Caching**: [Redis / In-Memory]

## 4. Key Workflows
*Trace the most critical paths through the system.*

1.  **[Workflow Name]** (e.g., "User Signup")
    - Step 1: User submits form
    - Step 2: API validates input
    - Step 3: DB creates record
    - Step 4: Email service sends welcome

## 5. Development Environment
*How does this system run locally?*

- **Build System**: [Vite / Webpack / TSC]
- **Ports**: [Localhost:3000]
- **Env Variables**: [Which .env files are required?]
