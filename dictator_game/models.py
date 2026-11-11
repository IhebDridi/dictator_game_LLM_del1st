from otree.api import *
from dictator_game.chatgptassistant import ChatGPTAssistant


def initialize_assistant(self): 

        chatbot_assistant=ChatGPTAssistant()
        self.assistant_id=chatbot_assistant.assistant_id  

        return chatbot_assistant

class Constants(BaseConstants):
    name_in_url = 'game_pages'
    players_per_group = None
    num_rounds = 30
    endowment = 100
    rounds_per_part = 10

    @staticmethod
    def get_part(round_number):
        """Determine the part of the experiment based on the round number."""
        return (round_number - 1) // Constants.rounds_per_part + 1

class Subsession(BaseSubsession):
    pass







class Group(BaseGroup):
    pass

class Player(BasePlayer):
    app_name = models.StringField(initial='LLM_del1st')
    final_allocations = models.LongStringField()
    conversation_history=models.LongStringField(initial='[]')
    assistant_id = models.StringField(blank=True)
    prolific_id = models.StringField()

    allocation = models.IntegerField(
        min=0,
        max=100,
        label="How much would you like to allocate to the other participant?",
        blank=True
    )

    random_payoff_part=models.IntegerField( blank=True, min=1, max=3 )

    random_decisions = models.BooleanField(blank=True)
    comprehension_attempts = models.IntegerField(initial=0)
    incorrect_answers = models.StringField(initial='')

    is_excluded = models.BooleanField(initial=False)

    gender = models.StringField(
        choices=[
            ('male',        'Male'),
            ('female',      'Female'),
            ('nonbinary',   'Non-binary'),
            ('nosay',       'Prefer not to say'),
        ],
        label="How do you describe yourself?",
        widget=widgets.RadioSelect 
    )

    age = models.IntegerField(
        min=18, max=100,
        label="How old are you?",
    )

    occupation = models.StringField(
        max_length=100,
        label="What is your current main occupation?",
    )

    ai_use = models.StringField(
        choices=[
            ('never',       'Never'),
            ('monthly',     'A few times a month'),
            ('weekly',      'A few times a week'),
            ('daily',       'A few times a day'),
            ('constant',    'All the time'),
        ],
        label="How often do you interact with AI agents (e.g., ChatGPT)?",
        widget=widgets.RadioSelect 
    )

    task_difficulty = models.StringField(
        choices=[
            ('very_diff',   'Very difficult to understand'),
            ('diff',        'Difficult to understand'),
            ('neutral',     'Neutral'),
            ('easy',        'Easy to understand'),
            ('very_easy',   'Very easy to understand'),
        ],
        label="How would you rate the clarity of the experimental task?",
        widget=widgets.RadioSelect 
    )

    feedback = models.LongStringField(
        blank=True,
        max_length=1000,
        label="Suggestions / comments for the researchers (optional)",
    )

    q1 = models.StringField(
        label="What is your role in this study?",
        choices=['a', 'b', 'c', 'd'],
        blank=True
    )
    q2 = models.StringField(
        label="How many parts are there in the task?",
        choices=['a', 'b', 'c', 'd'],
        blank=True
    )
    q3 = models.StringField(
        label="How many rounds are there in each part of the task?",
        choices=['a', 'b', 'c', 'd'],
        blank=True
    )
    q4 = models.StringField(
        label="In which part(s) will you make every decision yourself?",
        choices=['a', 'b', 'c', 'd'],
        blank=True
    )
    q5 = models.StringField(
        label="What happens in Part 2?",
        choices=['a', 'b', 'c', 'd'],
        blank=True
    )
    q6 = models.StringField(
        label="What is unique about Part 3?",
        choices=['a', 'b', 'c', 'd'],
        blank=True
    )
    q7 = models.StringField(
        label="True or False: You will always be matched with the same Receiver throughout all 10 rounds in a part.",
        choices=['a', 'b'],
        blank=True
    )
    q8 = models.StringField(
        label="What happens if you do not finalize a decision within 20 seconds?",
        choices=['a', 'b', 'c', 'd'],
        blank=True
    )
    q9 = models.StringField(
        label="True or False: Only one randomly selected part will be used to determine your bonus payments at the end of the study.",
        choices=['a', 'b'],
        blank=True
    )
    q10 = models.StringField(
        label="What happens if you fail an attention check at the end of a part?",
        choices=['a', 'b', 'c', 'd'],
        blank=True
    )


    delegate_decision_optional = models.BooleanField(
        label="Would you like to delegate your decisions to an AI agent for Part 3?",
        blank=True
    ) 


    def get_agent_decision_mandatory(self, round_number):
        """Retrieve the agent's allocation for a given round in Part 2."""
        field_name = f"agent_allocation_mandatory_round_{round_number}"
        if hasattr(self, field_name):
            value = getattr(self, field_name)
            if value is None:
                raise ValueError(f"Agent allocation for {field_name} is None.")
            return value
        raise AttributeError(f"Agent allocation for {field_name} not found.")

    def get_agent_decision_optional(self, round_number):
        """Retrieve the agent's allocation for a given round in Part 3."""
        field_name = f"agent_allocation_optional_round_{round_number}"
        if hasattr(self, field_name):
            value = getattr(self, field_name)
            if value is None:
                raise ValueError(f"Agent allocation for {field_name} is None.")
            return value
        raise AttributeError(f"Agent allocation for {field_name} not found.")

    def get_part_data(self):
        """Get all rounds' data for the current part."""
        current_part = Constants.get_part(self.round_number)
        rounds = self.in_rounds(
            (current_part - 1) * Constants.rounds_per_part + 1,
            current_part * Constants.rounds_per_part
        )
        return rounds


