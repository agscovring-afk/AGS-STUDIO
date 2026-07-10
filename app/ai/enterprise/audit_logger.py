class AuditLogger:

    def log(self,event):

        return {
            "audit":event,
            "status":"RECORDED"
        }


logger = AuditLogger()
