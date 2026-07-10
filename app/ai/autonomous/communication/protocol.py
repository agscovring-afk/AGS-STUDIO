from enum import Enum


class AgentAction(Enum):
    """
    Standard communication actions between agents
    """

    REQUEST = "REQUEST"
    RESPONSE = "RESPONSE"
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    DELEGATE = "DELEGATE"
    REPORT = "REPORT"
    UPDATE = "UPDATE"


class MessageProtocol:

    @staticmethod
    def create_request(task, data=None):
        return {
            "type": AgentAction.REQUEST.value,
            "task": task,
            "data": data
        }

    @staticmethod
    def create_response(result, data=None):
        return {
            "type": AgentAction.RESPONSE.value,
            "result": result,
            "data": data
        }

    @staticmethod
    def create_report(agent, status, details=None):
        return {
            "type": AgentAction.REPORT.value,
            "agent": agent,
            "status": status,
            "details": details
        }