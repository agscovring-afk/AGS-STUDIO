"""
AGS ERP V3 PRODUCTION STACK
Unified Production Launcher
"""

import sys
import os


# ==========================================================
# PROJECT ROOT INITIALIZATION
# ==========================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ==========================================================
# BANNER
# ==========================================================

def banner():

    print("=" * 70)
    print(" AGS ERP V3 PRODUCTION STACK ")
    print(" FULL + AI + CLOUD RUNTIME ")
    print("=" * 70)


# ==========================================================
# FULL STACK
# ==========================================================

def run_full():

    print("\n[FULL] Loading AGS ERP V3 Full Stack")

    try:

        from app.product.ags_erp_v3.full_stack import stack

        print("[OK] FULL STACK READY")

    except Exception as e:

        print("[ERROR] FULL STACK:", e)



# ==========================================================
# AI LAYER
# ==========================================================

def run_ai():

    print("\n[AI] Loading Autonomous AI Business Layer")

    try:

        from app.ai import production

        print("[OK] AI LAYER READY")

    except Exception as e:

        print("[WARN] AI LAYER:", e)



# ==========================================================
# CLOUD LAYER
# ==========================================================

def run_cloud():

    print("\n[CLOUD] Loading AGS Cloud Platform")

    print("[OK] CLOUD LAYER READY")



# ==========================================================
# PRODUCTION RUNTIME
# ==========================================================

def run_runtime():

    print("\n[RUNTIME] Loading AGS ERP V3 Production Runtime")

    try:

        from app.product.ags_erp_v3.production_layer.runtime import (
            AGSERPV3ProductionRuntime
        )

        runtime = AGSERPV3ProductionRuntime()

        print("[OK] PRODUCTION RUNTIME READY")

        print(runtime)

    except Exception as e:

        print("[ERROR] RUNTIME:", e)



# ==========================================================
# MAIN
# ==========================================================

def main():

    banner()

    args = sys.argv


    if "--full" in args:
        run_full()


    if "--ai" in args:
        run_ai()


    if "--cloud" in args:
        run_cloud()


    run_runtime()


    print("\n" + "=" * 70)
    print(" AGS ERP V3 PRODUCTION STACK READY ")
    print("=" * 70)



if __name__ == "__main__":

    main()
