import os


log_level: str = os.environ.get(
    "HASSIO_LINUX_CONTROLLER_LOG_LEVEL",
    "INFO",
).upper()
url: str = os.environ.get(
    "HASSIO_LINUX_CONTROLLER_HASSIO_URL",
    "http://localhost:8123",
)
token: str = os.environ.get(
    "HASSIO_LINUX_CONTROLLER__HASSIO_BEARER_TOKEN",
    "<please set this token>",
)
interval_s: int = int(os.environ.get("HASSIO_LINUX_CONTROLLER_INTERVAL_S", 1))
display = os.environ.get("HASSIO_LINUX_CONTROLLER_DISPLAY_ID", ":0")
display_entitiy_id: str = os.environ.get(
    "HASSIO_LINUX_CONTROLLER_DISPLAY_ENTITY_ID",
    "",
)
invoke_shutdown_entitiy_id: str = os.environ.get(
    "HASSIO_LINUX_CONTROLLER_INVOKE_SHUTDOWN_ENTITY_ID",
    "",
)
invoke_reboot_entitiy_id: str = os.environ.get(
    "HASSIO_LINUX_CONTROLLER_INVOKE_REBOOT_ENTITY_ID",
    "",
)
dry_run: bool = os.environ.get(
    "HASSIO_LINUX_CONTROLLER_DRY_RUN",
    "false",
).lower() in ["yes", "true", "t", "1"]


headers = {
    "Authorization": f"Bearer {token}",
    "content-type": "application/json",
}
