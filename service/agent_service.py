from analize.health_agent import HealthAgent


class AgentService:

    def __init__(self):

        self.__agent = HealthAgent()

    def process_user_request(
            self,
            user_prompt,
            user_data):

        return self.__agent.process_request(
            user_prompt,
            user_data
        )