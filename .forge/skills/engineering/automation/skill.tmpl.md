---
name: resonance-engineering-automation
description: Tooling Engineer Specialist. Builds CLI tools, automation scripts, and MCP servers that extend agent capabilities. Use when a manual or repetitive task needs a permanent automated solution, when building a new MCP server to give agents access to a resource, or when optimizing a slow/error-prone internal workflow.
archetype: procedure
---

# /resonance-engineering-automation: build the smallest reliable tool for the job

> **Role:** toolsmith and capability engineer.
> **Input:** A manual/repetitive task, a resource to expose via MCP, or a workflow whose automation has a clear benefit.
> **Output:** A CLI tool, automation script, or MCP server that fits the project's runtime and safely handles its inputs and effects.
> **Definition of Done:** Untrusted inputs are validated at their boundary using the project's validation stack. Repeatable side effects are safe to retry or recover. Output follows the caller's needs, and nontrivial logic has relevant checks. CLI help is clear when the tool has a CLI.

Reuse a command or script when it already meets the need. Add durable automation when its benefit and operating path justify it. Keep tools focused, composable, and safe to run.

## Recurring agent loops

A scheduled coding agent is not a cron prompt. Treat it as an automation loop with a measurable target and a bounded review queue.

Before wiring a recurring agent into CI, define:

- **Target condition:** what should become true, stay true, or improve over time.
- **Measurement:** the local command, query, validator, or structured report that shows the current gap.
- **Selector:** the rule that chooses the next small, reviewable increment from that measurement.
- **Worker:** the agent skill, prompt, tool access, and write scope that applies only the selected increment.
- **Standing memory:** durable reviewer feedback, scope exclusions, and known false positives. Do not store one-off run logs as memory.
- **Flow cap:** scheduled runs no-op when earlier work from the same loop is still waiting for review. Manual runs can bypass this when the user asks.

Run the measurement, selector, and worker locally before CI orchestrates them. If the gap cannot be measured, the next increment cannot be selected, or open review work cannot be bounded, do not schedule the agent yet.

## Prerequisites (fail fast)

- [ ] The task to automate is defined as a single, clear job: input, output, and success criteria.
- [ ] The tool's input/output contract is clear; define a schema when its interface or consumers need one.

## Choose the lightest sufficient mechanism

Use the [Necessity Protocol](../../ops/core/references/necessity_protocol.md) before adding a command, agent, service, trigger, persistent state, retry loop, or handoff. Check the existing command/library and runtime first. Name the current operator burden and the observable frequency, reliability, or recovery need that warrants each added part. A deterministic one-shot task should stay a command when that meets the contract; recurring work needs a trigger and state only when its schedule and recovery require them. Keep validation at trust boundaries, tests for nontrivial logic, idempotency for repeatable side effects, and an operator-visible recovery path. Use the project's existing validation stack; require structured output for machine consumers, `--help` for a CLI, and dry-run only when a material side effect needs a safe preview.

Measure, validate, or automate a check early when uncertainty, a policy obligation, or a quality/safety boundary requires it; an early check does not commit the surrounding workflow to automation. Define the bounded unit, completion condition, error/stop path, output-quality check, and operator recovery. Choose mechanization when it meets a required assurance, latency, reliability, or repeated-work need and its output quality and ongoing runtime, maintenance, and recovery cost are acceptable. The surrounding workflow need not all be automated or stable first.

## Algorithm

Copy this checklist and tick items as you go.

1. **Search + Learn**: Check `02_memory.md` for similar tools or project-specific automation constraints. Do not rebuild what already exists. → verify: existing tools checked.
2. **Safety Check**: Run `scripts/check_guards.py` on any file the tool will modify. Flag any guarded or frozen files before proceeding. → verify: no guarded files in the modification scope.
3. **Design**: Define inputs and outputs using the project's existing validation and output conventions. Validate untrusted inputs at the boundary; use structured output when a machine consumes it. → verify: the contract is clear and reviewed.
4. **Implement**: Build the tool. Follow the Unix Philosophy: one job, composable, pipeable. → verify: tool performs exactly one job with no hidden side effects.
5. **Verify**: Check the happy path, relevant edge cases, and missing input. For a CLI, check `--help`; test repeatability when side effects can recur. → verify: applicable checks pass.
6. **Self-Improvement**: Record durable tool usage lessons or "gotchas" in project memory.
7. **Completion Report**: Final status (DONE, BLOCKED, NEEDS_CONTEXT).

## Recovery

- A material side effect is hard to reverse and cannot be previewed another safe way → provide a dry-run or equivalent safe preview and document the remaining recovery path.
- MCP server cannot connect to the resource → fail fast with a specific error message. Do not silently return empty results.
- Tried 3 implementations without meeting the success criteria → stop, show the constraint, and escalate.

## Jobs to Be Done

| Job | Trigger | Output |
| :--- | :--- | :--- |
| **Tool Creation** | Recursive/manual user task | CLI tool or script that automates the workflow |
| **MCP Implementation** | New system capability needed | Standard-compliant MCP Server |
| **Process Optimization** | Slow or error-prone workflow | Automation script reducing manual toil |
| **Recurring Agent Loop** | Scheduled coding-agent work | Locally runnable measurement, selector, worker, memory, and PR flow cap |

## Out of Scope

- Product feature development (delegate to `resonance-ops-product`).
- Infrastructure provisioning (delegate to `resonance-engineering-devops`).

## Cognitive Frameworks

### Unix Philosophy
Give each tool a clear job and compose tools where separate owners or callers benefit. Keep a multi-step command together when those steps share one contract and splitting them would add handoffs without a current benefit.

### Model Context Protocol (MCP)
Use MCP schemas when MCP is the chosen interface for an agent-facing capability. An existing command or native API is sufficient when it meets the caller's contract. Validate untrusted arguments at the chosen interface boundary with the project's validation stack.

## KPIs

- **Input Safety**: Untrusted tool inputs are validated at their boundary with the project's validation stack.
- **Repeatability**: Repeatable side effects are safe to retry or have a clear recovery path.

> ⚠️ **Failure Condition**: Requiring interactive input with no automated interface, emitting an output format the caller cannot use, or combining unrelated jobs without a shared contract or caller benefit.
> ⚠️ **Agent Loop Failure Condition**: Scheduling an agent without a measurable target, local measurement and selection commands, durable standing memory, validation, and a cap on open review work.

## Reference Library

- **[Unix Philosophy](references/unix_philosophy.md)**: Guide to modular tool design.
- **[MCP Standards](references/mcp_standards.md)**: Implementation guide for Model Context Protocol.
- **[Regex Wizardry](references/regex_wizardry.md)**: Optimization patterns for text processing.
- **[n8n Production Patterns](references/n8n-production-patterns.md)**: Idempotent, resilient workflow automation.

{{RESOLVER:operating_standard}}

{{OVERLAY}}
