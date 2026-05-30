# Protocol: Diagnostic Playbook
> **Focus**: Language-specific debugging commands and common error heuristics.
> **Resonance Phase**: Execution / Verification

This playbook provides deterministic execution commands for targeted debugging. When isolating a bug, favor using these native and purpose-built tools to expose the underlying system state. 

## 1. Quick System Diagnostics
When hunting infrastructure or environment failures:
*   **Check Port Bindings**: `lsof -i :PORT`
*   **Locate Process**: `ps aux | grep PROCESS_NAME`
*   **Monitor Disk Space**: `df -h`
*   **Real-time Process Monitor**: `top -l 1 | head -10`
*   **Watch File System Events**: `fswatch -r ./src`

## 2. Language-Specific Tooling

### JavaScript / TypeScript (Node.js & Web)
*   **Node.js Native Inspector**: `node --inspect-brk app.js` (Attach via `chrome://inspect`).
*   **Memory Leak Hunting**: Run V8 with forced garbage collection exposure: `node --expose-gc --max-old-space-size=4096 app.js`
*   **Deep Console Tracing**: 
    *   `console.trace('Call stack here')`
    *   `console.time('perf'); /* code block */ console.timeEnd('perf')`
    *   `console.log(JSON.stringify(obj, null, 2))`

### Python
*   **Native Breakpoint (Python 3.7+)**: Inject `breakpoint()` directly in code over `print` statements.
*   **Built-in Interactive Debugger**: `python -m pdb script.py`
*   **Memory Profiling**: `python -X tracemalloc script.py`
*   **Execution Profiling**: `python -m cProfile -s cumulative script.py`

### Network & APIs
*   **Verbose HTTP Tracing**: `curl -v https://api.example.com/endpoint`
*   **Performance Metrics (DNS, SSL, TTFB)**: `curl -w "@curl-format.txt" -o /dev/null -s https://example.com`
*   **DNS Resolution Check**: `dig example.com` or `nslookup example.com`
*   **Active Sockets & Listeners**: `netstat -tlnp`

### CSS / Paint Debugging
*   **Visual Box-Model Outline**: `* { outline: 1px solid red !important; }`
*   **Highlight Target Selectors**: `.debug { background: rgba(255,0,0,0.1) !important; }`

## 3. Heuristics: Common Error Patterns
Before diving deep into a stack trace, check these established heuristics:

| Error Signature | Likely Cause | Recommended Action |
| :--- | :--- | :--- |
| `Cannot read property of undefined` | Missing null check, or asynchronous data not yet loaded. | Inject optional chaining (`?.`), or structural validations (`zod`). |
| `ENOENT` | File or directory does not exist. | Verify path resolution (absolute vs relative), ensure target creates directory, check `existsSync()`. |
| `CORS error` | Backend rejecting preflight due to missing headers or invalid origin. | Add CORS middleware to backend, explicitly permit origin, headers, and methods. |
| `Module not found` | Path mapping is invalid, or dependency tree is corrupted. | Verify `tsconfig.json` paths, delete `node_modules` and lockfile, reinstall. |
| `Hydration mismatch (React)` | State inconsistency between Server Render and Client Hydration. | Suppress hydration warnings selectively, or wrap client-only logic in `useEffect`. |
| `Connection refused` | Upstream service is offline or listening on a different interface/port. | Check internal routing (`localhost` vs `127.0.0.1` vs `0.0.0.0`), ensure process is running. |
| `Permission denied` | Execution privileges, missing `.env` access, or firewall block. | Validate `chmod`, check system user level, review SELinux or active firewall rules. |
| `Segmentation fault` | Memory corruption, null pointer dereference, unbound array. | Run language specific lower-level memory checks. Validate pointer bounds. |
