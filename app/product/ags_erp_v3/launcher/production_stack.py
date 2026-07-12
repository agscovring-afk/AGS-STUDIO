from app.product.ags_erp_v3.production_layer.runtime import AGSERPV3ProductionRuntime
from app.product.ags_erp_v3.desktop_app.application import main as desktop_main


def start():

    print("=" * 70)
    print(" AGS ERP V3 PRODUCTION STACK ")
    print("=" * 70)

    print("[RUNTIME] Booting Production Runtime")

    runtime = AGSERPV3ProductionRuntime()

    result = runtime.boot()

    print(result)

    print()
    print("[GUI] Starting Desktop Application")

    desktop_main()


if __name__ == "__main__":
    start()