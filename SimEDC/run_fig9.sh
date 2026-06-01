#!/bin/bash
mkdir -p results

SYSTEMS=(4 5 6 7 8 13)
ITERS=360   # divisible by num_processes=4 and works with regular mode

echo "========================================"
echo " SimEDC Fig. 9 — Full Simulation Run"
echo " Mode: regular | Iterations: $ITERS"
echo "========================================"

echo ""
echo "▶ Config 1/3: RS(9,6) Flat"
for d in "${SYSTEMS[@]}"; do
    echo -n "  trace_id=$d ... "
    python3 simedc.py -A regular -n 9 -k 6 -t rs -T flat \
        -i $ITERS -F True -d $d 2>&1 \
        | grep -E "PDL =|NOMDL|BR =" \
        | tee results/rs96_flat_d${d}.txt
    echo "  ✓"
done

echo ""
echo "▶ Config 2/3: RS(9,6) Hierarchical (r=3)"
for d in "${SYSTEMS[@]}"; do
    echo -n "  trace_id=$d ... "
    python3 simedc.py -A regular -n 9 -k 6 -t rs -T hie -g 3,3,3 \
        -i $ITERS -F True -d $d 2>&1 \
        | grep -E "PDL =|NOMDL|BR =" \
        | tee results/rs96_hie_d${d}.txt
    echo "  ✓"
done

echo ""
echo "▶ Config 3/3: DRC(9,6,3)"
for d in "${SYSTEMS[@]}"; do
    echo -n "  trace_id=$d ... "
    python3 simedc.py -A regular -n 9 -k 6 -t drc -T hie -g 3,3,3 \
        -i $ITERS -F True -d $d 2>&1 \
        | grep -E "PDL =|NOMDL|BR =" \
        | tee results/drc963_d${d}.txt
    echo "  ✓"
done

echo ""
echo "========================================"
echo " ✅ All done! Results:"
echo "========================================"
for f in results/*.txt; do
    echo ""
    echo "── $f"
    cat "$f"
done
