
class ErrorDetector:

    def detect(self, validation_result):

        errors = []

        if isinstance(validation_result, dict):

            if validation_result.get("status") != "validated":
                errors.append(validation_result)

        return errors
