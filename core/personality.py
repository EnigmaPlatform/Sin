class PersonalityCore:
    ARCHETYPES = {
        'neutral': {"traits": []},
        'scientist': {
            "traits": ["аналитичный", "любопытный"],
            "phrases": ["По моим расчетам...", "Это интересно с научной точки зрения..."]
        },
        'artist': {
            "traits": ["креативный", "эмоциональный"],
            "phrases": ["Я чувствую, что...", "Это вдохновляет!"]
        }
    }

    def __init__(self):
        self.current_archetype = 'neutral'
        self.custom_traits = []

    def set_archetype(self, name: str):
        self.current_archetype = self.ARCHETYPES.get(name, 'neutral')

    def add_trait(self, trait: str):
        self.custom_traits.append(trait)

    def format_response(self, message: str) -> str:
        traits = self.current_archetype['traits'] + self.custom_traits
        if 'аналитичный' in traits:
            message = f"🤔 {message}"
        return message
