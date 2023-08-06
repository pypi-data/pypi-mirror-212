from splathash.engine.context.application_context import ApplicationContext
from splathash.node.node import Node
from splathash.response.response_handler import UserResponseHandler

from .screens import FeelingScreen, FinalScreen, InvalidInputScreen, ReasonScreen


class RootHandler(UserResponseHandler):
    def get_node(self, context: ApplicationContext) -> Node:
        return FeelingScreen()


class FeelingScreenResponseHandler(UserResponseHandler):
    def get_node(self, context: ApplicationContext) -> Node:
        response = context.getData()
        context.update("feeling", response)
        if response in ["1", "2", "3"]:
            return ReasonScreen()
        return InvalidInputScreen()


class ReasonScreenResponseHandler(UserResponseHandler):
    def get_node(self, context: ApplicationContext) -> Node:
        response = context.getData()
        context.update("reason", response)
        if response in ["1", "2", "3"]:
            return FinalScreen()
        return InvalidInputScreen()
