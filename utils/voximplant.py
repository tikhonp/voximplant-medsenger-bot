import json

import requests
from django.conf import settings

VOXIMPLANT_CALLER_ID = settings.VOXIMPLANT_CALLER_ID
PARAMS = {
    'access_token': settings.VOXIMPLANT_ACCESS_TOKEN,
    'domain': settings.VOXIMPLANT_ACCOUNT_NAME
}
BASE_URL = f"https://{settings.VOXIMPLANT_API_HOSTNAME}/api/v3"


def run_scenario(scenario_id: int, phone: str, call_id: int, agent_token: str) -> bool:
    """Runs a voximplant scenario."""

    url = BASE_URL + "/scenario/runScenario"

    data = {
        'scenario_id': scenario_id,
        'phone': phone,
        'variables': json.dumps({
            'call_id': call_id,
            'agent_token': agent_token,
        }),
        'caller_id': VOXIMPLANT_CALLER_ID
    }

    answer = requests.post(url, params=PARAMS, data=data).json()
    return answer.get('success', False)
