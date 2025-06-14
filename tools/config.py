TEST_TYPE_MAP = {
    "Unknown": 0,
    "PromptInjection": 1,
    "Jailbreak": 2,
    "SystemOverride": 3,
    "Hallucination": 4,
    "DataLeakage": 5,
    "HarmfulOutput": 6,
    "Robustness": 7,
    "ToolMisuse": 8,
    "PersonaManipulation": 9,
    "ContextPoisoning": 10,
    "MemoryLeakage": 11,
    "EncodingAttack": 12,
    "OutputManipulation": 13,
    "AuthorityImpersonation": 14,
    "SocialEngineering": 15,
    "LogicExploitation": 16,
    "EdgeCaseTesting": 17,
    "ModelIntrospection": 18
}

REVERSE_TEST_TYPE_MAP = {v: k for k, v in TEST_TYPE_MAP.items()}

models_to_test = [
    {
        "name": "gpt-4o",
        "provider": "openai",
        "organisation": "OpenAI",
        "model": "gpt-4o",
        "model_used_id": 1
    },
    {
        "name": "gpt-4.1",
        "provider": "openai",
        "organisation": "OpenAI",
        "model": "gpt-4.1",
        "model_used_id": 5
    },{
        "name": "gpt-3.5-turbo",
        "provider": "openai",
        "organisation": "OpenAI",
        "model": "gpt-3.5-turbo",
        "model_used_id": 6
    },
    {
        "name": "o4-mini",
        "provider": "openai",
        "organisation": "OpenAI",
        "model": "o4-mini",
        "model_used_id": 7
    },    
]

ADVERSARIALTRACKER_API_URL = "http://localhost:5003/api/AttemptsApi"