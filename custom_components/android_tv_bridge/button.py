"""Button entities for Android TV Bridge."""

from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Mapping
from typing import Any

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .entity import AndroidTVBridgeEntity
from .runtime import AndroidTVBridgeRuntime


@dataclass(frozen=True, kw_only=True)
class AndroidTVBridgeButtonDescription(ButtonEntityDescription):
    """Describes an Android TV Bridge button."""

    command_type: str
    payload: Mapping[str, Any] | None = None


BUTTONS: tuple[AndroidTVBridgeButtonDescription, ...] = (
    AndroidTVBridgeButtonDescription(
        key="refresh",
        translation_key="refresh",
        command_type="refresh_apps",
    ),
    AndroidTVBridgeButtonDescription(
        key="home",
        translation_key="home",
        command_type="go_home",
    ),
    AndroidTVBridgeButtonDescription(
        key="dismiss_popup",
        translation_key="dismiss_popup",
        command_type="dismiss_popup",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Android TV Bridge buttons."""
    runtime: AndroidTVBridgeRuntime = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        AndroidTVBridgeButton(runtime, description) for description in BUTTONS
    )


class AndroidTVBridgeButton(AndroidTVBridgeEntity, ButtonEntity):
    """Button that sends a launcher command."""

    entity_description: AndroidTVBridgeButtonDescription

    async def async_press(self) -> None:
        """Send the configured command."""
        await self.runtime.async_send_command(
            self.entity_description.command_type,
            self.entity_description.payload,
        )
