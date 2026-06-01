# SimEDC-Extended

**Modernising and Extending SimEDC: Reliability Analysis of Erasure-Coded Data Centers Under HDD, SSD, and NVMe Failure Models**

> Goriola-Obafemi Babatunde Sukanmi
> Department of Applied Mathematics and Computer Science
> Supervisor: Prof. Могилевская H.C | Academic year 2025-2026

---

## Overview

This repository extends the SimEDC simulator (Zhang et al., IEEE TPDS 2020)
with four original contributions:

1. **Python 3.13 modernisation** — Four runtime incompatibilities in
   lib/state.py are identified, documented, and resolved with a reproducible
   patching methodology. See PATCH_NOTES.md.

2. **Synthetic HPC trace generation** — The original LANL failure traces are
   permanently offline. This repository provides a synthetic generator
   parameterised from the statistical models in the original paper, validated
   against the theoretical Weibull AFR of 10.42%.

3. **Extended placement analysis (r=4, r=5)** — The first empirical
   characterisation of the full placement spectrum for RS(9,6) codes under
   trace-driven failure conditions. Results reveal a consistent reliability
   gradient and a threshold between r=5 and r=4 for System 14.

4. **SSD and NVMe failure models** — Flash storage models from Backblaze Q4
   2023 (SSD AFR=0.98%, NVMe AFR=0.47%) confirm that DRC(9,6,3) maintains
   its reliability advantage under flash storage failure distributions.

---

## Key Findings

- DRC(9,6,3) with hierarchical placement achieves the lowest Blocked Ratio
  across all six HPC systems under HDD, SSD, and NVMe failure models.

- Reducing r from 9 to 5 to 4 to 3 produces a consistent monotonic
  improvement in Blocked Ratio. A reliability threshold exists between
  r=5 and r=4 for System 14.

- Flash storage reduces PDL by approximately two orders of magnitude
  compared to HDD for DRC configurations.

- The reliability hierarchy of the original study is preserved under
  flash storage failure distributions.

---

## Quickstart

```bash
git clone https://github.com/nobleteesage/SimEDC-Extended.git
cd SimEDC-Extended
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Smoke test
cd SimEDC
python3 simedc.py -n 9 -k 6 -t rs -T flat -i 36
```

---

## Simulation Configurations

| Config | n | k | r | Type | Flags |
|--------|---|---|---|------|-------|
| RS flat | 9 | 6 | 9 | Flat | -t rs -T flat |
| RS r=5 | 9 | 6 | 5 | Hierarchical | -t rs -T hie -g 2,2,2,2,1 |
| RS r=4 | 9 | 6 | 4 | Hierarchical | -t rs -T hie -g 3,2,2,2 |
| RS r=3 | 9 | 6 | 3 | Hierarchical | -t rs -T hie -g 3,3,3 |
| DRC(9,6,3) | 9 | 6 | 3 | Hierarchical | -t drc -T hie -g 3,3,3 |

---

## Python 3.13 Patch

```bash
sed -i \
  's/self\.num_disks \/ self\.num_nodes/self.num_disks \/\/ self.num_nodes/g; \
   s/subsystem_idx \/ self\.disks_per_node/subsystem_idx \/\/ self.disks_per_node/g; \
   s/range(self\.disks_per_node)/range(int(self.disks_per_node))/g' \
  SimEDC/lib/state.py
```

Always use -A regular for trace-driven simulation:

```bash
python3 simedc.py -A regular -n 9 -k 6 -t rs -T flat \
    -i 360 -F True -d 4
```

---

## Trace Validation

| System | Nodes | Duration | Est. AFR | Theoretical |
|--------|-------|----------|----------|-------------|
| 4 | 128 | 4.0 yr | 11.13% | ~10.42% |
| 5 | 128 | 3.5 yr | 10.94% | ~10.42% |
| 6 | 256 | 4.0 yr | 10.35% | ~10.42% |
| 7 | 256 | 4.0 yr | 8.59% | ~10.42% |
| 8 | 512 | 5.0 yr | 10.55% | ~10.42% |
| 14 | 1024 | 4.5 yr | 9.85% | ~10.42% |

---

## Citation

```bibtex
@misc{sukanmi2026simedc,
  author    = {Goriola-Obafemi Babatunde Sukanmi},
  title     = {SimEDC-Extended: Modernising and Extending SimEDC},
  year      = {2026},
  publisher = {GitHub},
  url       = {https://github.com/nobleteesage/SimEDC-Extended}
}
```

Original SimEDC paper:

```bibtex
@article{zhang2020simedc,
  author  = {Zhang, Mi and Han, Shujie and Lee, Patrick P. C.},
  title   = {SimEDC: A Simulator for the Reliability Analysis of
             Erasure-Coded Data Centers},
  journal = {IEEE Transactions on Parallel and Distributed Systems},
  volume  = {31},
  number  = {4},
  pages   = {905--918},
  year    = {2020},
  doi     = {10.1109/TPDS.2019.2946838}
}
```

---

## Related

- Original SimEDC: https://github.com/millyz/SimEDC
- Backblaze SSD Stats Q4 2023: https://www.backblaze.com/blog/ssd-stats-q4-2023

## License

MIT License. See LICENSE. The original SimEDC simulator is the work of
Zhang, Han, and Lee (CUHK) and is used under its original open-source terms.
