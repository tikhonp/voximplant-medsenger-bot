from rest_framework.exceptions import PermissionDenied

from medsenger_agent.models import Contract


class ContractByAgentTokenMixin:
    """Get contract by agent token or 403."""

    def get_contract(self) -> Contract:
        """Returns Contract instance or raises PermissionDenied."""

        try:
            return Contract.objects.get(agent_token=self.request.query_params.get('agent_token'))
        except Contract.DoesNotExist:
            raise PermissionDenied('`agent_token` is invalid or does not exists.')
