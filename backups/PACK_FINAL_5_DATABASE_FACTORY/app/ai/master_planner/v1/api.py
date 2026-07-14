from .dispatcher import BuildDispatcher

dispatcher = BuildDispatcher()

def execute(target):

    return dispatcher.dispatch(target)
