from .base_agent import BaseAgent, AgentResponse


class EchoAgent(BaseAgent):
    def run(self, prompt: str, **kwargs) -> AgentResponse:
        return AgentResponse(text=prompt)
