from enum import Enum
import pathlib
import os
from loguru import logger
import typing
import functools


class Environ(str, Enum):
    PRODUCTION = "production"
    DEVELOPMENT = "development"


@functools.lru_cache(maxsize=1)
def determine_valid_environment_file(
    override_environment: str = None,
) -> typing.Tuple[Environ, str]:
    """Determines the best environment file to use based on standards.
    Args:
        override_environment (str, optional): Override the detection of what mode this application runs in. This does not affect the actual file to be read. Defaults to None.
    Returns:
        str: Path to Env.
    """

    _set_mode = Environ.PRODUCTION
    
    if (
        os.getenv("INVII_DEVELOPMENT") is not None
        or override_environment == "development"
        or override_environment == "dev"
        or pathlib.Path(".invii_dev_mode").exists()
    ):
        logger.debug("Development mode enabled")

        if pathlib.Path(".env.development.local").exists():
            return Environ.DEVELOPMENT, ".env.development.local"

        if pathlib.Path(".env.dev.local").exists():
            return Environ.DEVELOPMENT, ".env.dev.local"

        if pathlib.Path(".env.development").exists():
            return Environ.DEVELOPMENT, ".env.development"

        if pathlib.Path(".env.dev").exists():
            return Environ.DEVELOPMENT, ".env.dev"

        logger.warning(
            "Development Mode is enabled, however there is no development-specific environment file. Please create one of the following files: .env.development.local, .env.dev.local, .env.development, or .env.dev. .env (if present) will be used instead and application will be set in production mode."
        )
        _set_mode = Environ.DEVELOPMENT
    elif (
        os.getenv("INVII_PRODUCTION") is not None
        or override_environment == "production"
        or override_environment == "prod"
    ):
        logger.warning("Production mode enabled")
        if pathlib.Path(".env.production.local").exists():
            return Environ.PRODUCTION, ".env.production.local"
        if pathlib.Path(".env.prod.local").exists():
            return Environ.PRODUCTION, ".env.prod.local"
        if pathlib.Path(".env.production").exists():
            return Environ.PRODUCTION, ".env.production"
        if pathlib.Path(".env.prod").exists():
            return Environ.PRODUCTION, ".env.prod"

    if pathlib.Path(".env.local").exists():
        return _set_mode, ".env.local"

    
    if not pathlib.Path(".env").exists():
        raise Exception("No environment file found. Please create one of the following files: .env, .env.local, .env.production, .env.prod, .env.production.local, .env.prod.local, .env.development, .env.dev, .env.development.local, or .env.dev.local")
    
    logger.debug(f"{_set_mode.capitalize()} mode and no {_set_mode.capitalize()}-specific environment file found. Using .env")
    return _set_mode, ".env"