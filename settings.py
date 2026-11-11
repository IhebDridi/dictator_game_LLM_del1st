from os import environ


SESSION_CONFIGS = [
    dict(
        name='dictator_game',
        display_name="Dictator Game",
        app_sequence=['dictator_game'],
        num_demo_participants=100,
    ),
]


SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.01, participation_fee=6, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

LANGUAGE_CODE = 'en'

REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '9871076378040'

OPENAI_API_KEY = environ.get('OPENAI_API_KEY')
instructions_path='dictator_game/instructions_LLM.txt'
openai_model='gpt-4o-mini'

