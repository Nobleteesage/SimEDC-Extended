# Python 3.13 Patch Notes — SimEDC

## Overview

SimEDC was implemented under Python 2.7 and crashes on all current Python 3
environments. Four runtime incompatibilities in lib/state.py were identified
and resolved to restore SimEDC to full operational status under Python 3.13.

All four bugs share the same root cause: Python 3.0 changed the semantics of
the / operator for integer operands. In Python 2, a/b for integers returns an
integer. In Python 3 it returns a float, and floor division requires //.

## Bug Table

| Bug ID | Method | Expression | Failure | Fix |
|--------|--------|------------|---------|-----|
| BUG-01 | __init__ | num_disks / num_nodes | disks_per_node stored as float | Use // |
| BUG-02 | disk fail | range(self.disks_per_node) | TypeError: float not integer | range(int(...)) |
| BUG-03 | disk repair | subsystem_idx / disks_per_node | node_idx float — invalid bitmap index | Use // |
| BUG-04 | node ops | range(self.disks_per_node) | TypeError: float not integer | range(int(...)) |

## One-Command Patch

Apply to any clean SimEDC installation:

```bash
sed -i \
  's/self\.num_disks \/ self\.num_nodes/self.num_disks \/\/ self.num_nodes/g; \
   s/subsystem_idx \/ self\.disks_per_node/subsystem_idx \/\/ self.disks_per_node/g; \
   s/range(self\.disks_per_node)/range(int(self.disks_per_node))/g' \
  lib/state.py
```

## Additional Issue — Silent Trace Mode Failure

Without the -A regular flag, SimEDC runs in importance sampling mode and
produces empty result files with no error. Always use:

```bash
python3 simedc.py -A regular -n 9 -k 6 -t rs -T flat -i 360 -F True -d 4
```

## Verification

```bash
python3 simedc.py -n 9 -k 6 -t rs -T flat -i 36
# Should print PDL, NOMDL, BR without errors
```

## Environment Tested

- OS: Kali Linux kernel 6.x 64-bit
- Python: 3.13.0
- Platform: Intel Core i5, 8 GB RAM

Documented by Goriola-Obafemi Babatunde Sukanmi, SFedU, 2026.
Supervisor: Prof. Могилевская H.C
