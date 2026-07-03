# Observability Pillars Done Right

## Contents
- Structured logging
- Metrics: RED and USE
- Distributed tracing and OpenTelemetry
- Context propagation
- Correlating the three pillars
- Sampling
- Cost and cardinality

## Structured logging

A log line is data, not prose. Emit machine-parseable events (JSON or logfmt) with stable keys, one event per line. A human grepping is the fallback; the primary consumer is a query engine.

Rules that hold up:
- One event per logical action. Do not spread one operation across five `info` lines; emit one wide event with many fields at the end.
- Stable, typed keys. `duration_ms` is a number every time, not sometimes `"1.2s"`. Downstream aggregation dies on inconsistent types.
- Always attach correlation IDs: `trace_id`, `span_id`, `request_id`, plus `service`, `version`, `env`. Without `trace_id` you cannot pivot from a log to its trace.
- Levels mean something. ERROR is "a human should look," WARN is "degraded but handled," INFO is "a notable state change," DEBUG is off in production by default and sampled when on.
- Log the decision, not the narration. "charged card, amount=4200 currency=eur result=declined reason=insufficient_funds" beats "About to charge the card..." followed by "Charge failed!".

What never goes in a log: secrets, tokens, passwords, full card numbers, raw PII, entire request or response bodies. Structured logging makes leaks queryable, which turns a mistake into a searchable index of it. Redact at the emit site, not in a downstream pipeline you might forget to configure.

Context over messages: prefer key/value context on the event over encoding facts into the message string. `user_tier=free region=eu-west-1` is filterable; "free user in Frankfurt" is not.

## Metrics: RED and USE

Metrics are cheap aggregate counters and histograms sampled over time. They answer "is it bad and since when," not "what happened to this one request." Keep labels low-cardinality.

Metric types:
- **Counter**: monotonic, only goes up (requests_total, errors_total). Rate is derived at query time.
- **Gauge**: a value that moves up and down (queue_depth, connections_active, memory_bytes).
- **Histogram**: bucketed distribution (request_duration). This is how you get real percentiles. Never average a latency; average hides the tail. A p99 histogram tells the truth an average buries.

**RED, for request-driven services** (APIs, microservices, anything with an inbound request):
- **Rate**: requests per second, per endpoint and status class.
- **Errors**: failed requests per second. Count both explicit failures (5xx) and implicit ones (a 200 carrying an error body, a wrong result).
- **Duration**: latency distribution as a histogram, split by success and error. A fast error still counts as a failure, not as good fast traffic.

RED is your default service dashboard. Three signals per endpoint tell you almost everything about how a service is serving.

**USE, for resources** (CPU, memory, disk, network, connection pools, thread pools, queues):
- **Utilization**: percent of time the resource was busy (or fraction of capacity used).
- **Saturation**: the queued work the resource cannot service yet (run-queue length, pool wait time). Saturation is the leading indicator; utilization can sit at 100% while still coping, but rising saturation means it stopped coping.
- **Errors**: error events for that resource (failed allocations, dropped packets, pool timeouts).

RED tells you the service is slow. USE tells you which resource to blame. Run both: symptom on the service, cause on the resources behind it.

Label discipline: a metric's cost scales with the number of unique label-value combinations (its cardinality), not with how often you record it. `http_requests_total{method, route_pattern, status_class}` is fine because each label has few values. `http_requests_total{user_id, full_url}` can explode into millions of series and take down the metrics backend. Use the route pattern (`/users/:id`), never the concrete path (`/users/8a3f...`). Put the concrete id on a trace or log instead.

## Distributed tracing and OpenTelemetry

A single request often crosses many services. A **trace** captures that one request end to end. A **span** is one timed unit of work inside the trace (an HTTP handler, a DB query, an outbound RPC, a cache lookup). Spans carry a name, start and end time, status, and attributes, and they nest: a parent span (the handler) contains child spans (the queries it made). The tree of spans is the anatomy of the request.

What a trace answers that metrics cannot: metrics say p99 latency doubled. The trace of one slow request shows the doubling came from a specific downstream call that now waits on a lock. Traces localize the problem in the call graph; metrics only tell you a problem exists.

Instrument with **OpenTelemetry (OTel)**: a vendor-neutral standard with three parts, an API (what you call in code), an SDK (the implementation that batches and exports), and OTLP (the wire protocol). Because it is neutral, you instrument once and can switch backends (Jaeger, Tempo, a hosted vendor) by reconfiguring the exporter, not by re-instrumenting. That is the whole point: no lock-in at the instrumentation layer.

Span hygiene:
- Name spans by operation, not by concrete value: `GET /users/:id`, not `GET /users/8a3f`. The concrete id is an attribute.
- Put high-cardinality facts on span attributes (`user.id`, `order.id`, `db.statement` summary). This is exactly where cardinality belongs; traces carry it cheaply where metrics cannot.
- Record the error on the span (status = error, plus an exception event) so a failed trace is filterable.
- Keep spans meaningful. A span per trivial function call is noise; a span per network hop or expensive operation is signal.

## Context propagation

A trace only reassembles if every service passes the trace identity to the next. **Context propagation** is carrying `trace_id` and the current `span_id` across each boundary so the receiver makes its spans children of the caller's span rather than starting a brand-new orphan trace.

- The standard is W3C Trace Context: the `traceparent` HTTP header (and `tracestate` for vendor data). OTel reads and writes it automatically for instrumented HTTP and gRPC clients.
- Async and queues are where propagation breaks. When you enqueue a job, inject `traceparent` into the message metadata; when you consume it, extract that context and continue the trace. Miss this and the worker's work shows up as a disconnected trace with no parent.
- Thread and coroutine hops inside one process also carry context. Most OTel SDKs handle this, but manual thread pools and detached tasks can drop it. If traces fracture into single-span orphans, suspect a boundary where context was not propagated.

A fractured trace is often worse than no trace: it looks like data but lies about causality. When traces do not connect, fixing propagation comes before anything else.

## Correlating the three pillars

The power is not any one pillar; it is pivoting between them on shared IDs.
- Every log line carries `trace_id` and `span_id`. From a suspicious log event you jump straight to the full trace it belongs to.
- Every trace carries the identifiers (user, order, region) that let you find the matching logs and the metric series.
- Exemplars link a metric histogram bucket to a sample trace_id, so from "the p99 bucket got worse" you jump to an actual slow request in that bucket.

The workflow during an incident: a metric or SLO burn alert fires (something is bad), you open the trace exemplars for the bad bucket (where in the call graph), you read the logs for that trace_id (what exactly happened). Metric to trace to log, in three clicks. Build your correlation IDs so that path exists before you need it.

## Sampling

You cannot store every trace at scale, and you should not try. Sampling keeps cost sane while preserving signal.
- **Head sampling**: decide at the start of the request (keep 1 in N). Simple and cheap, but it is blind to the outcome, so it can drop the rare error you most wanted.
- **Tail sampling**: buffer spans and decide after the request finishes, so you can keep all errors and all slow requests and downsample the boring fast successes. More infrastructure, far better signal.
- Keep 100% of errors and high-latency traces regardless of sample rate. The whole reason to trace is the pathological request; do not let sampling throw it away.

Logs and metrics have their own knobs: sample or rate-limit high-volume DEBUG logs; never sample the counters that feed your SLIs, or the SLI itself becomes an estimate.

## Cost and cardinality

Observability that bankrupts you gets turned off, and telemetry that is off explains nothing. Treat cost as a design constraint.
- Metrics: cost is per unique series (label combination). Guard label cardinality hard. One accidental unbounded label is the classic way to 100x a metrics bill overnight.
- Logs: cost is per volume ingested and retained. Drop or sample chatty DEBUG in production, keep ERROR and WARN. Shorten retention for high-volume low-value streams.
- Traces: cost is per span stored. Tail-sample to keep the interesting traces and shed the boring ones.

The general rule: metrics stay low-cardinality and always-on for aggregate health; traces and logs carry the high-cardinality detail and are sampled. Put each fact where it is cheap: aggregate counts on metrics, per-request specifics on traces and logs.
