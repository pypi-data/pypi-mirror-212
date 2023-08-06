from typing import Tuple

from splathash.data.node_response import MenuOption, NodeResponse
from splathash.engine.context.application_context import ApplicationContext
from splathash.node.node import Node

from .constants import Feeling, Reason


class FeelingScreen(Node):
    """Feeling screen."""

    def create_menu(self, context: ApplicationContext) -> Tuple[NodeResponse, str]:
        return (
            NodeResponse(
                message="How are you feeling?",
                options=[
                    MenuOption("1", "Happy"),
                    MenuOption("2", "Sad"),
                    MenuOption("3", "Unwell"),
                ],
            ),
            "feeling-handler",
        )


class ReasonScreen(Node):
    """Reason screen."""

    def create_menu(self, context: ApplicationContext) -> Tuple[NodeResponse, str]:
        feeling = Feeling(context.retrieve("feeling")).name
        return (
            NodeResponse(
                message=f"Why are you feeling {feeling}?",
                options=[
                    MenuOption("1", "Money"),
                    MenuOption("2", "Relationship"),
                    MenuOption("3", "Health"),
                ],
            ),
            "reason-handler",
        )


class FinalScreen(Node):
    """Final screen."""

    def create_menu(self, context: ApplicationContext) -> Tuple[NodeResponse, str]:
        feeling = Feeling(context.retrieve("feeling")).name
        reason = Reason(context.retrieve("reason")).name

        return (
            NodeResponse(
                message=f"You are feeling {feeling} because of {reason}.",
            ),
            "",
        )


class InvalidInputScreen(Node):
    """Invalid Input screen."""

    def create_menu(self, context: ApplicationContext) -> Tuple[NodeResponse, str]:
        return NodeResponse(message="Invalid input."), ""
