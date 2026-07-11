from app.product.ags_erp_v3.ui.application import AGSERPV3DesktopApp


app = AGSERPV3DesktopApp()

print(app.boot())

print("="*40)
print("AGS ERP V3 MODULE SCREENS")
print("="*40)

for module in app.modules_list():
    print("-", module)

print("="*40)
print(app.modules.open("CRM"))
print(app.modules.open("Dashboard"))
