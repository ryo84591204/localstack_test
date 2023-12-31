import logging
from typing import Dict

from localstack.aws.connect import connect_to
from localstack.utils.common import retry

LOG = logging.getLogger(__name__)


def await_sfn_execution_result(execution_arn: str, timeout_secs: int = 60) -> Dict:
    """Wait until the given SFN execution ARN is no longer in RUNNING status, then return execution result."""

    client = connect_to().stepfunctions

    def _get_result():
        result = client.describe_execution(executionArn=execution_arn)
        assert result["status"] != "RUNNING"
        return result

    return retry(_get_result, sleep=2, retries=timeout_secs / 2)
