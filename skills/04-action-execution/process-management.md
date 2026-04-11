# Process Management

**Category:** `action-execution`  
**Skill Level:** `intermediate`  
**Stability:** `stable`

### Description

Start, stop, monitor, and interact with OS processes from within an agent workflow.

### Example

```python
import subprocess

# Start a background process
proc = subprocess.Popen(['python', 'server.py'], stdout=subprocess.PIPE)

# Check if running
if proc.poll() is None:
    print('Server is running')

# Terminate
proc.terminate()
```

### Related Skills

- [Shell Command](shell-command.md)
- [Terminal Interaction](../10-computer-use/terminal-interaction.md)
