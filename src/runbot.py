#!/usr/bin/env python
import sentry_sdk

from bot.config import SENTRY_SDK_KEY, VERSION
from bot.configured import denis
from bot.runner import StoredRunner


if __name__ == '__main__':
    sentry_sdk.init(SENTRY_SDK_KEY, release=VERSION)
    StoredRunner(denis()).run()
