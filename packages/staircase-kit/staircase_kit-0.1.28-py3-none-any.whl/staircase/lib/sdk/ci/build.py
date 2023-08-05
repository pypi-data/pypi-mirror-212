import sys
import time

from ..staircase_env import StaircaseEnvironment


async def build(ci_env: StaircaseEnvironment, url) -> str:
    r = await ci_env.http_client.async_request(
        "infra-builder/builds", "POST", data={"source_url": url}
    )
    r = await r.json()
    id_ = r["build_id"]

    while True:
        response = await ci_env.http_client.async_request(
            f"infra-builder/builds/{id_}"
        )
        response_body = await response.json()

        status = response_body.get("status")
        if status in ("IN_PROGRESS", "RUNNING"):
            time.sleep(15)
        elif status == "FAILED":
            if logs := response_body.get("logs"):
                logs = "".join(logs) if isinstance(logs, list) else logs
            raise BuildFailed(logs)
        else:
            url = response_body["artifacts_url"]
            return url


class BuildFailed(Exception):
    ...