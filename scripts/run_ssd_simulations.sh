#!/bin/bash
# SSD and NVMe reliability simulations — FIXED VERSION
# Directly points to SSD/NVMe tracelib folders

SYSTEMS=(4 5 6 7 8 13)
ITERS=360

mkdir -p results/ssd results/nvme

run_config() {
    local TRACELIB_DIR=$1
    local OUTDIR=$2
    local LABEL=$3

    echo ""
    echo "========================================"
    echo " $LABEL Simulations"
    echo "========================================"

    # Backup original tracelib and replace with SSD/NVMe version
    cp -r lib/tracelib lib/tracelib_hdd_backup_$$

    # Clear existing tracelib contents and copy new ones
    rm -rf lib/tracelib/failure_events
    rm -rf lib/tracelib/transient_events
    rm -rf lib/tracelib/transient_repair
    cp -r $TRACELIB_DIR/failure_events   lib/tracelib/
    cp -r $TRACELIB_DIR/transient_events lib/tracelib/
    cp -r $TRACELIB_DIR/transient_repair lib/tracelib/

    echo "✅ Tracelib swapped to $LABEL"

    echo ""
    echo "▶ RS(9,6) Flat (r=9)"
    for d in "${SYSTEMS[@]}"; do
        echo -n "  trace_id=$d ... "
        python3 simedc.py -A regular -n 9 -k 6 -t rs -T flat \
            -i $ITERS -F True -d $d 2>&1 \
            | grep -E "PDL =|NOMDL \(bytes|BR =" \
            | tee $OUTDIR/rs96_flat_d${d}.txt
        echo " ✓"
    done

    echo ""
    echo "▶ RS(9,6) Hierarchical (r=3)"
    for d in "${SYSTEMS[@]}"; do
        echo -n "  trace_id=$d ... "
        python3 simedc.py -A regular -n 9 -k 6 -t rs -T hie -g 3,3,3 \
            -i $ITERS -F True -d $d 2>&1 \
            | grep -E "PDL =|NOMDL \(bytes|BR =" \
            | tee $OUTDIR/rs96_hie_d${d}.txt
        echo " ✓"
    done

    echo ""
    echo "▶ DRC(9,6,3)"
    for d in "${SYSTEMS[@]}"; do
        echo -n "  trace_id=$d ... "
        python3 simedc.py -A regular -n 9 -k 6 -t drc -T hie -g 3,3,3 \
            -i $ITERS -F True -d $d 2>&1 \
            | grep -E "PDL =|NOMDL \(bytes|BR =" \
            | tee $OUTDIR/drc963_d${d}.txt
        echo " ✓"
    done

    # Restore original HDD tracelib
    rm -rf lib/tracelib/failure_events
    rm -rf lib/tracelib/transient_events
    rm -rf lib/tracelib/transient_repair
    cp -r lib/tracelib_hdd_backup_$$/failure_events   lib/tracelib/
    cp -r lib/tracelib_hdd_backup_$$/transient_events lib/tracelib/
    cp -r lib/tracelib_hdd_backup_$$/transient_repair lib/tracelib/
    rm -rf lib/tracelib_hdd_backup_$$

    echo ""
    echo "✅ $LABEL complete! Tracelib restored to HDD."
    echo ""
    echo "── Results:"
    for f in $OUTDIR/*.txt; do
        echo "  $f:"
        cat "$f"
    done
}

# ── Run SSD simulations ───────────────────────────────────────
run_config "tracelib_ssd" "results/ssd" "SSD Failure Model"

# ── Run NVMe simulations ──────────────────────────────────────
run_config "tracelib_nvme" "results/nvme" "NVMe Failure Model"

echo ""
echo "========================================"
echo "🎉 ALL SSD AND NVMe SIMULATIONS DONE!"
echo "========================================"
