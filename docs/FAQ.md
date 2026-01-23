# ❓ Frequently Asked Questions (FAQ)

## 🎯 Onboarding

### Why do I need `.resonance`? Can't I just chat?
Most AI chats are "amnesiac"—they forget your project context after a session.
Resonance gives your agent a **Hard Drive**. The `.resonance/` folder stores your "Soul" (Vision) and "Memory" (Decisions) so the Agent gets smarter over time, instead of rebooting every day.

### Why do I have to run `/init`?
To "Interview" you. Resonance builds a custom profile for your project in `00_soul.md`. If you skip this, the agent is generic. If you run it, the agent acts like a hired expert who knows *exactly* what you are building.

---

## 🛠️ Usage

### Can I delete `.resonance/`?
Yes, but you will lobotomize the project. The Agent will forget everything it learned about your specific constraints.

### How do I update the rules?
Edit `.resonance/00_soul.md`. This is the "Constitution". Whatever you write there is Law for every Agent that touches this project.

### Can I run a system check manually?
Yes. You can verify your skills, workflows, and memory structure without invoking an LLM.

**Mac / Linux**:
```bash
chmod +x ./resonance.sh
./resonance.sh
```

**Windows (PowerShell)**:
```powershell
.\resonance.ps1
```

### I have my own way of doing things. Can I change the workflows?
Yes. Workflows in `.agent/workflows/` are just markdown files. Edit them to fit your team's style. Resonance is descriptive, not prescriptive.
