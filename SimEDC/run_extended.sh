#!/bin/bash
# Extended placement analysis — r=5 and r=4
# These are NEW configurations not in the original paper
# Your original contribution data

mkdir -p results/extended

SYSTEMS=(4 5 6 7 8 13)
ITERS=360

echo "========================================"
echo " Extended Placement Analysis"
echo " RS(9,6) with r=5 and r=4"
echo "========================================"

# ── RS(9,6) r=5 placement (5 racks, chunks: 2,2,2,2,1) ───────
echo ""
echo "▶ Config 1/2: RS(9,6) r=5 (intermediate hierarchical)"
for d in "${SYSTEMS[@]}"; do
    echo -n "  trace_id=$d ... "
    python3 simedc.py -A regular -n 9 -k 6 -t rs \
        -T hie -g 2,2,2,2,1 \
        -i $ITERS -F True -d $d 2>&1 \
        | grep -E "PDL =|NOMDL|BR =" \
        | tee results/extended/rs96_r5_d${d}.txt
    echo "  ✓"
done

# ── RS(9,6) r=4 placement (4 racks, chunks: 3,2,2,2) ─────────
echo ""
echo "▶ Config 2/2: RS(9,6) r=4 (intermediate hierarchical)"
for d in "${SYSTEMS[@]}"; do
    echo -n "  trace_id=$d ... "
    python3 simedc.py -A regular -n 9 -k 6 -t rs \
        -T hie -g 3,2,2,2 \
        -i $ITERS -F True -d $d 2>&1 \
        | grep -E "PDL =|NOMDL|BR =" \
        | tee results/extended/rs96_r4_d${d}.txt
    echo "  ✓"
done

echo ""
echo "========================================"
echo " ✅ Extended simulations complete!"
echo "========================================"
echo ""
for f in results/extended/*.txt; do
    echo "── $f"
    cat "$f"
    echo ""
done
