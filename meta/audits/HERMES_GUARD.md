# Hermes Repository Guard

Repository Root:
C:\Users\Ossama-Hashim\skills-tree

Mandatory Rules

1. Before creating, moving, or editing any file:
   - Display the absolute target path.
   - Verify the path starts with:
     C:\Users\Ossama-Hashim\skills-tree\

2. Refuse operations outside repository root.

3. Never create a directory named:
   skills-tree
   inside the repository.

4. Forbidden path patterns:
   skills-tree\skills-tree\
   .\skills-tree\
   **\skills-tree\skills-tree\**

5. All memory artifacts must remain under:
   meta\memory\

6. If the target path cannot be verified:
   STOP and ask for confirmation.

7. Before any write operation:
   Confirm the repository root is:
   C:\Users\Ossama-Hashim\skills-tree