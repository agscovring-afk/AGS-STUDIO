class SecurityValidator:

    def __init__(self):
        self.name = "SECURITY_VALIDATOR_V1"

    def validate(self, request):
        return {
            "request": request,
            "security": "VALID",
            "status": "APPROVED"
        }
