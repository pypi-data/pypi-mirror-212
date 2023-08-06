from __future__ import annotations

import logging

from globus_sdk import exc

log = logging.getLogger(__name__)


class AuthAPIError(exc.GlobusAPIError):
    """
    Error class for the API components of Globus Auth.
    """
