from app.ai.autonomous.workers.bridge import bridge


task = {

    "module":
    "client"

}


result = bridge.dispatch(
    "module_builder",
    task
)


print(result)
