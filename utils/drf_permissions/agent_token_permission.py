from rest_framework.permissions import BasePermission

from forms.models import Call
from medsenger_agent.models import Contract


class AgentTokenPermission(BasePermission):
    """
    Checks for existence of Contract with agent_token from query params.
    """

    message = "`agent_token` query param invalid or does not exists."

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Call):
            agent_token = request.query_params.get('agent_token')
            return obj.connected_form.contract.agent_token == agent_token
        return True

    def has_permission(self, request, view):
        agent_token = request.query_params.get('agent_token')
        return Contract.objects.filter(agent_token=agent_token).exists()
