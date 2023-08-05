import contextlib
import logging
import os

import attrs
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

import hkkang_utils.misc as misc_utils
import hkkang_utils.socket as socket_utils

# Load environment variables
misc_utils.load_dotenv(stack_depth=2)
# Get default access token
DEFAULT_ACCESS_TOKEN = (
    os.environ["SLACK_ACCESS_TOKEN"] if "SLACK_ACCESS_TOKEN" in os.environ else None
)

logger = logging.getLogger("SlackMessenger")


@attrs.define
class SlackMessenger:
    """Note that the default token is set by the environment variable SLACK_ACCESS_TOKEN."""

    channel: str = attrs.field()
    token: str = attrs.field(default=attrs.Factory(lambda: DEFAULT_ACCESS_TOKEN))
    append_src_info: bool = attrs.field(default=True)

    def __attrs_post_init__(self):
        if self.token is None:
            raise ValueError(
                "Please set token or set SLACK_ACCESS_TOKEN environment variable."
            )

    def send(self, text: str) -> None:
        return send_message(
            token=self.token,
            channel=self.channel,
            text=text,
            append_src_info=self.append_src_info,
        )


def send_message(
    channel: str,
    text: str,
    token: str = DEFAULT_ACCESS_TOKEN,
    append_src_info: bool = True,
) -> None:
    """Please follow the tutorial to get bot OAuthToken and setup the bot permissions.
    https://github.com/slackapi/python-slack-sdk/tree/main/tutorial
    """
    # Check if token is provided
    if token is None:
        raise ValueError(
            "Please set token or set SLACK_ACCESS_TOKEN environment variable."
        )
    # Create client
    client = WebClient(token=token)

    # Build message
    if append_src_info:
        ip = socket_utils.get_local_ip()
        host_name = socket_utils.get_host_name()
        text_with_prefix = f"Message from {host_name}({ip}):\n{text}"

    # Send message
    try:
        response = client.chat_postMessage(channel=channel, text=text_with_prefix)
        assert response["message"]["text"] == text_with_prefix
        logger.info(f"Sending message to channel {channel}: {text}")
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"], "channel_not_found"
        logger.info(f"Got an error: {e.response['error']}")


@contextlib.contextmanager
def notification(
    channel: str,
    success_msg: str = None,
    error_msg: str = None,
    token: str = DEFAULT_ACCESS_TOKEN,
):
    slack_messenger = SlackMessenger(channel=channel, token=token)
    try:
        yield slack_messenger
        if success_msg is not None:
            slack_messenger.send(success_msg)
    except Exception as e:
        if error_msg is not None:
            slack_messenger.send(f"{error_msg} ({e.__class__.__name__}: {e})")
        raise e


@contextlib.contextmanager
def slack_notification(*args, **kwargs):
    raise NotImplementedError("Please use notification instead of slack_notification")
