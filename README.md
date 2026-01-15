# watchline
Cognitive Lock / Attention Binding

## Thought Anchor (IntentBar)

A **transient cognitive overlay** for binding intent to attention.

Thought Anchor is a minimal Python tool that lets you enter a sensitive, one-line directive **in the terminal (masked)** and displays it as a **thin, always-on-top strip** at the top of your screen—**only as wide as the text**. No prompt history. No persistence. No noise.

This is not a note app.
This is not a reminder.
This is a **state control instrument**.

---

## What it does

1. Prompts you in the terminal for a message  
   - Input is **masked (`*`)**
   - Nothing lands in shell history
   - `Enter` or `Ctrl+C` submits immediately

2. Displays the message as:
   - A **borderless top-of-screen strip**
   - **Always on top**
   - **Centered**
   - **Sized exactly to the text**

3. Interaction:
   - **Click** the strip → copies text to clipboard
   - **Ctrl+C** (when focused) → copies
   - **Esc** → closes (no trace left behind)

When the window closes, the message is gone.

---

## Why this exists

Thought Anchor is designed for **human-factors control**, not productivity tracking.

It is useful when you need to:

- Lock yourself into a mode  
  (“PROD FREEZE”, “SLOW DOWN”, “LOG EVERYTHING”)

- Keep a sensitive directive out of:
  - terminal history
  - notes
  - screenshots
  - saved drafts

- Maintain a visible rule-of-engagement under stress
- Prevent context drift, impulse actions, or narrative hijack
- Hold a copyable payload without storing it anywhere permanent

This is **cockpit instrumentation for the brain**.

---

## Installation

Python 3.8+ required.

No external dependencies beyond the standard library.
