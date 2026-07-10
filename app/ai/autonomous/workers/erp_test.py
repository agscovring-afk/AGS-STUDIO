from app.ai.autonomous.workers.bridge import bridge


result = bridge.dispatch(

    "erp_builder",

    {
        "request":
        "Build Construction ERP"
    }

)


print(result)
