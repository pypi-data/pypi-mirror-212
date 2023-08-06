from .handlers import (
    FeelingScreenResponseHandler,
    ReasonScreenResponseHandler,
    RootHandler,
)


class USSDRoutes:
    baseTable = {
        "": lambda: RootHandler(),
        "feeling-handler": lambda: FeelingScreenResponseHandler(),
        "reason-handler": lambda: ReasonScreenResponseHandler(),
    }
