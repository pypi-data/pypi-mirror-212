from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING

from django.db.models import Q

from better_translation.integrations.django.models import BaseMessage
from better_translation.storage import (
    BaseStorage,
    StorageMessage,
    StorageTranslation,
)

if TYPE_CHECKING:
    from collections.abc import Sequence
    from pathlib import Path


logger = logging.getLogger(__name__)


@dataclass(slots=True, kw_only=True)
class DjangoStorage(BaseStorage):
    message_model: type[BaseMessage]

    async def load(self) -> None:
        """Load translations from the storage to the memory."""
        logger.info("Loading messages from the database...")

        messages = self.message_model.objects.all().prefetch_related(
            "translations",
        )
        async for message in messages:
            translations = message.translations.all()
            if not translations:
                logger.warning(
                    "Message '%s' has no translations",
                    message,
                )
            else:
                logger.debug(
                    "Message '%s' has '%s' translations",
                    message,
                    len(translations),
                )

            self.storage[message.id] = self._get_storage_message(message)

        self.is_loaded = True

        logger.info("Messages loaded successfully")

    async def add_messages(self, messages: Sequence[StorageMessage]) -> None:
        """Add new messages to the storage.

        Ignores messages that are already in the storage.
        """
        if not self.is_loaded:
            await self.load()

        messages_to_create = set[BaseMessage]()

        for message in messages:
            if message.id in self.storage:
                logger.debug(
                    "Message '%s' is already in the storage",
                    message,
                )
                continue

            logger.info("Adding message '%s' to the storage", message)
            self.storage[message.id] = message
            messages_to_create.add(self._get_message_model(message))

        already_in_storage = self.message_model.objects.filter(
            id__in={message.id for message in messages_to_create},
        ).values_list("id", flat=True)

        await self.message_model.objects.abulk_create(
            [
                message
                for message in messages_to_create
                if message.id not in already_in_storage
            ],
        )

    async def add_messages_from_dirs(
        self,
        *dirs: Path,
        update_messages_usage: bool = False,
    ) -> list[StorageMessage]:
        messages: list[StorageMessage] = []
        for directory_path in dirs:
            messages.extend(self._extract_messages_from_dir(directory_path))

        await self.add_messages(messages)
        if update_messages_usage:
            await self.update_messages_usage(messages)

        return messages

    async def update_messages_usage(
        self,
        messages: Sequence[StorageMessage],
    ) -> None:
        logger.info("Finding unused messages...")

        messages_ids = {message.id for message in messages}
        unused_message_number = await self.message_model.objects.exclude(
            Q(id__in=messages_ids) & Q(is_dynamic=False),
        ).aupdate(is_used=False)

        await self.message_model.objects.filter(
            id__in=messages_ids,
        ).aupdate(is_used=True)

        logger.info(
            "Found %s unused messages",
            unused_message_number,
        )

    @staticmethod
    def _get_storage_message(message: BaseMessage) -> StorageMessage:
        return StorageMessage(
            id=message.id,
            default=message.default,
            default_plural=message.default_plural,
            context=message.context,
            has_plural=message.has_plural,
            is_dynamic=message.is_dynamic,
            translations={
                translation.locale: StorageTranslation(
                    singular=translation.singular,
                    plural=translation.singular,
                )
                for translation in message.translations.all()
            },
        )

    def _get_message_model(
        self,
        storage_message: StorageMessage,
    ) -> BaseMessage:
        return self.message_model(
            id=storage_message.id,
            default=storage_message.default,
            default_plural=storage_message.default_plural,
            context=storage_message.context,
            has_plural=storage_message.has_plural,
            is_dynamic=storage_message.is_dynamic,
        )
