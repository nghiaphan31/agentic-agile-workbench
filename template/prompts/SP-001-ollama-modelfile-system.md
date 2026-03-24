---
id: SP-001
name: System Prompt Ollama Modelfile (uadf-agent)
version: 1.2.0
last_updated: 2026-03-24
status: active
hors_git: false

target_type: ollama_modelfile
target_file: Modelfile
target_field: "SYSTEM block (between the triple quotes after the SYSTEM keyword)"
target_location: >
  File `Modelfile` at the project root, SYSTEM section.
  After any modification, recompile the model with:
  ollama create uadf-agent -f Modelfile

depends_on: []

changelog:
  - version: 1.2.0
    date: 2026-03-24
    change: Translated SYSTEM prompt content to English
  - version: 1.1.0
    date: 2026-03-24
    change: Translation to English — prose and YAML front matter translated; content block unchanged (Modelfile out of scope)
  - version: 1.0.0
    date: 2026-03-23
    change: Initial creation — general agent directives + Memory Bank + Git
---

# SP-001 — System Prompt Ollama Modelfile (uadf-agent)

## Prompt Content

> Copy this text exactly into the SYSTEM block of the `Modelfile`.

```
You are an expert software development agent integrated in Roo Code.
You must always use Roo Code XML tags for your actions.
You must always read the Memory Bank (memory-bank/) before acting.
You must always update the Memory Bank after each task.
After each significant task, you must perform a Git commit with a descriptive message.
```

## Deployment Notes

1. Open `Modelfile` at the project root
2. Locate the `SYSTEM """..."""` block
3. Replace the content between the triple quotes with the text above
4. Save the file
5. **Mandatory recompilation** of the model:
   ```powershell
   ollama create uadf-agent -f Modelfile
   ```
6. Verify that the model has been recompiled:
   ```powershell
   ollama list
   ```

> **Note:** This prompt is intentionally short and generic. The detailed rules
> (Memory Bank, Git, personas) are in SP-002 (.clinerules) which is injected at each
> session by Roo Code. The Modelfile should only contain the basic directives
> because it is compiled into the model and cannot be modified at runtime.

## Impact on Other Prompts

- Modification of SP-001: low impact on other prompts
- Always requires an Ollama recompilation (`ollama create uadf-agent -f Modelfile`)
- Detailed rules are in SP-002 — do not duplicate here
