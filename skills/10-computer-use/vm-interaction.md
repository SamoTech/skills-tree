# Virtual Machine Interaction

**Category:** `computer-use`
**Skill Level:** `advanced`
**Stability:** `experimental`
**Added:** 2025-03

### Description

Operate inside VMs and sandboxed environments (VirtualBox, VMware, Docker desktops, E2B sandboxes) by connecting via RDP, VNC, or cloud APIs to execute GUI and terminal actions safely.

### Example

```python
# Using E2B cloud sandbox
from e2b_desktop import Desktop

desktop = Desktop()
# Take screenshot of sandbox
screenshot = desktop.screenshot()

# Run a command inside the VM
desktop.run_process('ls -la /home')

# Click inside the VM at coordinates
desktop.left_click(400, 300)

desktop.close()
```

### Related Skills

- [Screenshot Capture](screenshot-capture.md)
- [Terminal / Shell Interaction](terminal-interaction.md)
- [Window Management](window-management.md)
