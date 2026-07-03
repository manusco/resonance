# Agent Design

> "Most tasks that look like they need an agent are a fixed pipeline in disguise."

An agent is a loop where the model decides the next action, calls a tool, reads the result, and decides again, until it declares the task done. This is genuinely powerful and genuinely expensive: every step is a model call, errors compound, and debugging a wrong path is hard. Reach for it last, not first.

## Contents
- Workflow vs. agent: the decision
- Anatomy of an agent
- Tool contracts
- The control loop and stop conditions
- Observability
- When NOT to use an agent
- Common failure modes

## 1. Workflow vs. Agent: The Decision

| | Workflow | Agent |
| :--- | :--- | :--- |
| **Path** | Known in advance, fixed steps | Depends on intermediate results |
| **Control** | You wrote the sequence | The model chooses each step |
| **Cost** | Predictable | Variable, higher |
| **Debuggability** | High: it is code | Low: the model improvised |
| **Use when** | You can draw the flowchart | You genuinely cannot |

The test: can you draw the steps as a flowchart before running it? If yes, build the workflow. A "summarize then translate then email" task is three chained model calls, not an agent. You only need an agent when the next step honestly cannot be known until you see the last step's result.

Default to a workflow. Justify the agent.

## 2. Anatomy Of An Agent

An agent is four parts:

1. **A goal**: what "done" means, stated in the prompt.
2. **Tools**: the actions it can take (search, read a file, call an API), each with a typed contract.
3. **A control loop**: model proposes an action, the runtime executes it, the result is fed back, repeat.
4. **Stop conditions**: how the loop ends (goal met, step limit, or failure).

The model is the planner. Your code is the runtime that executes tool calls safely and enforces the limits. Never let the model execute its own actions unchecked.

## 3. Tool Contracts

Tools are the agent's hands. Bad tools produce a flailing agent.

- **Narrow and specific**: `get_order_status(order_id)` beats a general `run_query(sql)`. Every capability you expose is attack surface and a chance to misfire.
- **Typed and validated**: define the input schema. Validate arguments before executing. A malformed tool call gets a clear error back, not a crash.
- **Clear descriptions**: the tool's name and description are how the model decides to use it. Vague descriptions cause wrong tool choice.
- **Return structured results with errors the model can act on**: "not found" and "rate limited" should come back as data the model can respond to, not as an exception that kills the loop.
- **Least privilege**: read-only where possible. Consequential actions (send, pay, delete) go behind a confirmation gate, not straight into the loop.

## 4. The Control Loop And Stop Conditions

An unbounded agent loop is a bug that bills you. Bound it:

- **Max steps**: a hard cap. If it has not finished in N steps, stop and report, do not run forever.
- **Explicit success condition**: a defined signal for "done", not "the model stopped talking".
- **Failure and give-up path**: repeated tool failure or no progress ends the loop and escalates. The agent must be able to say "I could not do this".
- **No-progress detection**: if the agent repeats the same action or oscillates between two, break. Loops are the classic agent failure.
- **Budget cap**: a per-run token or cost ceiling. Cross it, stop.

## 5. Observability

You cannot debug what you cannot see. An agent without tracing is unshippable.

- Log every step: the model's chosen action, the tool arguments, the tool result, the model's next decision.
- Make a single run replayable. When it goes wrong, you need to see exactly where the plan broke.
- Track per-run step count, cost, and outcome. Rising steps-per-task is a regression.

## 6. When NOT To Use An Agent

- The path is fixed: use a workflow. Cheaper, faster, debuggable.
- A single well-prompted call plus one tool does the job: do that.
- The task is high-stakes and low-tolerance for a wrong path (moving money, deleting data) without a human gate: do not hand it to an autonomous loop.
- You cannot yet measure whether it worked: build the eval first. An unmeasured agent is a random-action generator you are paying for.
- Latency matters and the task is simple: an agent's multi-step loop is slow. Do not use one where a direct call suffices.

## 7. Common Failure Modes

- **Infinite or oscillating loops**: no step cap, no no-progress check.
- **Tool sprawl**: 30 vague tools, the model picks wrong. Fewer, sharper tools.
- **Compounding errors**: an early wrong step poisons everything after. Validate intermediate results.
- **The runaway bill**: no budget cap on a variable-length loop.
- **Silent wrong completion**: the agent declares success on a task it botched. Grade the final output with an eval, do not trust "done".
- **Autonomous consequential actions**: an agent that sends or deletes without a human gate. Gate them.
