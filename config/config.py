import logging
import os
from dataclasses import dataclass
from environs import Env

logger = logging.getLogger(__name__)


@dataclass
class BotSettings:
    token: str


@dataclass
class LoggSettings:
    level: str
    format: str
    style: str


@dataclass
class Config:
    bot: BotSettings
    log: LoggSettings


# This function returns the configuration as an object of the Config class from the .env file.
def load_config(path: str | None = None) -> Config:
    env = Env()

    if path:
        if not os.path.exists(path):
            logger.warning(f"file '{path}' not found")
        else:
            logger.info(f"Reading env from '{path}'...")
    env.read_env(path)

    bot_token = env("BOT_TOKEN")
    if not bot_token:
        raise ValueError("BOT_TOKEN is empty or does not exist")

    logger.info("Configuration loaded successfully")
    return Config(
        bot=BotSettings(token=bot_token),
        log=LoggSettings(
            level=env("LOG_LEVEL"), format=env("LOG_FORMAT"), style=env("LOG_STYLE")
        ),
    )
