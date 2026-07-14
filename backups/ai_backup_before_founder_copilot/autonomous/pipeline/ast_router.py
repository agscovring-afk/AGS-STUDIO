from app.ai.ast_engine.bridge import bridge


def execute_ast(request):

    text=str(request)

    if "AST ANALYZER" in text.upper():

        return bridge.execute(text)


    return None
