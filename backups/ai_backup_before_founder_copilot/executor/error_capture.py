class ErrorCapture:


    def capture(self, error):

        return {
            "error":
            str(error),
            "captured":
            True
        }


capture = ErrorCapture()
