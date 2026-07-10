from app.ai.autonomous.erp_executor.erp_auto_executor import executor


modules = [

"companies",
"clients",
"projects",
"tenders",
"boq",
"quotations",
"invoices",
"payments",
"purchases",
"warehouse",
"reports",
"users",
"permissions"

]


result = executor.execute(modules)

print(result)
