import traceback

import discord
from discord import Embed
from django.utils import timezone

from apps.alert_wing.managers.base_manager import BaseManager


class DiscordEmbedManager(BaseManager):
    """
    A class for managing Discord embed messages for exception handling.

    Args:
        exc (Exception): The exception instance.
        exc_id (str | int | None, optional): ID associated with the exception. Defaults to None.
        title (str, optional): Title of the embed. Defaults to an empty string.
        description (str, optional): Description of the embed. Defaults to an empty string.
        embed_color (discord.Color | None, optional): Color of the embed. Defaults to None.
        embed (discord.Embed | None, optional): Predefined discord.Embed object. Defaults to None.

    Attributes:
        exc (Exception): The exception instance.
        exc_id (str | int | None): ID associated with the exception.
        title (str): Title of the embed.
        description (str): Description of the embed.
        embed_color (discord.Color): Color of the embed.
        embed (discord.Embed): Discord embed object.

    Methods:
        setup_embed(): Sets up the discord.Embed object.
        _frame_summary_handler(frame_summary): Handles the formatting of a frame summary.
        format_exception(): Formats the exception and returns formatted text and extra detail.
        _embed_footer_data(): Generates data for the embed footer.
        set_data_for_delivery(): Prepares and returns the embed data as a dictionary.
    """

    def __init__(
        self,
        exc: Exception,
        exc_id: str | int | None = None,
        title: str = "",
        description: str = "",
        embed_color=None,
        embed: discord.Embed | None = None,
    ):
        if not exc:
            raise ValueError(
                "Exception instance must be provide (exc can't be None or falsy value)"
            )

        self.exc = exc
        self.exc_id = exc_id

        self.title = title
        self.description = description

        if embed_color:
            self.embed_color = embed_color
        else:
            self.embed_color = discord.Color.red()

        if embed:
            self.embed = embed
        else:
            self.embed = self.setup_embed()

    def setup_embed(self) -> discord.Embed:
        return Embed(
            title=self.title, description=self.description, colour=self.embed_color
        )

    def _frame_summary_handler(self, frame_summary: list):
        """
        Handle the formatting of a frame summary list.

        Args:
            frame_summary (traceback.FrameSummary): Frame summary object list.

        Returns:
            list: Formatted frame summary.
        """
        return traceback.format_list(frame_summary)

    def format_exception(self) -> tuple[str, str]:
        """
        Format the exception and return formatted text and extra detail.

        Returns:
            tuple[str, str]: Formatted exception and extra detail.
        """
        request = self.exc.__traceback__.tb_frame.f_locals.get("request")
        frame_summary_obj_list = traceback.extract_tb(self.exc.__traceback__)[-2:]

        formatted_frame_summary_list = self._frame_summary_handler(
            frame_summary_obj_list
        )

        formatted_exc = (
            f"{formatted_frame_summary_list[0]}\n"
            f"{formatted_frame_summary_list[1]}"
            f"{str(self.exc)}\n"
        )
        extra_detail = (
            f"Request API  -> {request.build_absolute_uri() if request is not None else None}\n"
            f"Request Method -> {request.method}"
        )
        return formatted_exc, extra_detail

    def _embed_footer_data(self):
        data = f"DateTime: {timezone.now()}"
        if self.exc_id:
            data = data + f" Error ID : {self.exc_id}"
        return data

    def set_data_for_delivery(self) -> dict:
        """
        Prepare and return the embed data as a dictionary.

        Returns:
            dict: Embed data as a dictionary.
        """
        formatted_exception, extra_detail = self.format_exception()
        self.embed.add_field(
            name=str(self.exc.__class__.__name__), value=formatted_exception
        )
        self.embed.add_field(name="Extra Detail", value=extra_detail, inline=False)
        self.embed.set_footer(text=self._embed_footer_data())
        return self.embed.to_dict()
