from app.product.ags_erp_v3.ui.application import AGSERPV3Application


app = AGSERPV3Application()

print(app.boot())

print("MENU:")
print(app.menu.list())

print("DASHBOARD:")
print(app.dashboard.render())
