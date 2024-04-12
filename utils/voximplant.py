import json
import os

import requests
import sentry_sdk
from django.conf import settings

bank = "./bank/"
money = bank + "money"


def voximplant_has_money() -> bool:
    return os.path.exists(money)


def no_money():
    if voximplant_has_money():
        os.remove(money)
        settings.MEDSENGER_API_CLIENT.notify_admin(
            "У агента опросники по телефону закончились деньги💰 на счету воксимпланта!!!💳💵 "
            "Не удается совершить звонок, пациенты в отчаянии((( 😭😤🤬"
        )


def yeah_money():
    if not voximplant_has_money():
        if not os.path.exists(bank):
            os.makedirs(bank)
        open(money, 'w').close()
        settings.MEDSENGER_API_CLIENT.notify_admin(
            "У агента появились деньги на счету воксимпланта!!!💳💵 "
            "Теперь можно совершать звонки, пациенты в безопасности))) 😊👍🎉"
        )


def run_scenario(scenario_id: int, phone: str, call_id: int,
                 agent_token: str, connected_form_id: int) -> bool:
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
            'host': settings.HOST,
            'connected_form_id': connected_form_id
        }),
        'phone_number_id': settings.VOXIMPLANT_CALLER_ID
    }
    answer = requests.post(url, params=params, data=data).json()
    result = answer.get('success', False)
    if not result:
        error = answer.get('result', {}).get('error')
        if error == 'Insufficient funds on balance':
            no_money()
        else:
            sentry_sdk.capture_message(error)
        print(f"run_scenario failed: {answer}")
    else:
        yeah_money()
    return result
