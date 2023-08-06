"""
Lifeguard integration with OpenAI
"""


class LifeguardOpenAIPlugin:
    def __init__(self, lifeguard_context):
        self.lifeguard_context = lifeguard_context


def init(lifeguard_context):
    LifeguardOpenAIPlugin(lifeguard_context)
