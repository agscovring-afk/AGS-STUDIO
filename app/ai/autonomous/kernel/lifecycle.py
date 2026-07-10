from .kernel import kernel


class LifecycleManager:


    def boot(self):

        return kernel.start()


    def shutdown(self):

        return kernel.stop()


lifecycle = LifecycleManager()