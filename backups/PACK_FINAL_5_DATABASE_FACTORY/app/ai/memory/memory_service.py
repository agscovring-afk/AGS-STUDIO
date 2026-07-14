from app.ai.memory.memory_manager import memory_manager
from app.ai.memory.memory_types import MemoryType


class MemoryService:
    """
    High level memory interface.
    Used by AI agents and modules.
    """

    def __init__(self):

        self.engine = memory_manager


    # ==========================
    # Store project memory
    # ==========================

    def remember_project(
        self,
        content,
        metadata=None
    ):

        return self.engine.remember(
            content=content,
            memory_type=MemoryType.PROJECT,
            metadata=metadata
        )


    # ==========================
    # Store module memory
    # ==========================

    def remember_module(
        self,
        module,
        content,
        metadata=None
    ):

        return self.engine.remember(
            content=content,
            module=module,
            memory_type=MemoryType.MODULE,
            metadata=metadata
        )


    # ==========================
    # Store agent memory
    # ==========================

    def remember_agent(
        self,
        agent,
        content,
        metadata=None
    ):

        return self.engine.remember(
            content=content,
            agent=agent,
            memory_type=MemoryType.AGENT,
            metadata=metadata
        )


    # ==========================
    # Store conversation
    # ==========================

    def remember_conversation(
        self,
        content,
        metadata=None
    ):

        return self.engine.remember(
            content=content,
            memory_type=MemoryType.CONVERSATION,
            metadata=metadata
        )


    # ==========================
    # Query
    # ==========================

    def search(
        self,
        keyword
    ):

        return self.engine.search(
            keyword
        )


    def agent_history(
        self,
        agent
    ):

        return self.engine.get_agent_memory(
            agent
        )


memory_service = MemoryService()