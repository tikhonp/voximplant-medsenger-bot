import json

import requests
from django.conf import settings


def run_scenario(scenario_id: int, phone: str, call_id: int, agent_token: str) -> bool:
    """Runs a voximplant scenario."""

    url = f"https://{settings.VOXIMPLANT_API_HOSTNAME}/api/v3/scenario/runScenario"
    params = {
        'access_token': settings.VOXIMPLANT_ACCESS_TOKEN,
        'domain': settings.VOXIMPLANT_ACCOUNT_NAME
    }
    data = {
        'scenario_id': scenario_id,
        'phone': phone,
        'variables': json.dumps({
            'call_id': call_id,
            'agent_token': agent_token,
            'host': settings.HOST
        }),
        'phone_number_id': settings.VOXIMPLANT_CALLER_ID
    }
    answer = requests.post(url, params=params, data=data).json()

    result = answer.get('success', False)
    if not result:
        if answer.get('result', {}).get('error') == 'Insufficient funds on balance':
            settings.MEDSENGER_API_CLIENT.notify_admin(
                "У агента опросники по телефону закончились деньги💰 на счету воксимпланта!!!💳💵 "
                "Не удается совершить звонок, пациенты в отчаянии((( 😭😤🤬"
            )
        print(f"run_scenario failed: {answer}")
    return result
