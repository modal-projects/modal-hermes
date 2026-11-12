import json
import logging
import urllib.request
from typing import Any, Optional, Sequence

from providers import register_provider
from providers.base import ProviderProfile

logger = logging.getLogger(__name__)

_USER_AGENT = "hermes-modal/1.0.0"
_EFFORT_LADDER = ("none", "minimal", "low", "medium", "high", "xhigh", "max", "ultra")
_CATALOG: dict[str, dict[str, Any]] = {}


def _clamp_effort(
    effort: Optional[str], supported: Optional[Sequence[str]]
) -> Optional[str]:
    requested = str(effort or "").strip().lower()
    if not requested or not supported:
        return effort
    supported_norm = [
        lvl
        for lvl in (str(s).strip().lower() for s in supported)
        if lvl in _EFFORT_LADDER
    ]
    if not supported_norm or requested in supported_norm:
        return effort
    if requested not in _EFFORT_LADDER:
        return effort
    candidates = [level for level in supported_norm if level != "none"]
    if not candidates:
        return effort
    requested_idx = _EFFORT_LADDER.index(requested)
    below = [
        level
        for level in candidates
        if _EFFORT_LADDER.index(level) < requested_idx
    ]
    return (
        max(below, key=_EFFORT_LADDER.index)
        if below
        else min(candidates, key=_EFFORT_LADDER.index)
    )


class ModalProfile(ProviderProfile):
    def fetch_models(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float = 8.0,
    ) -> list[str] | None:
        effective_base = (base_url or "").strip() or self.base_url
        if not effective_base:
            return None
        req = urllib.request.Request(effective_base.rstrip("/") + "/models")
        if api_key:
            req.add_header("Authorization", f"Bearer {api_key}")
        req.add_header("Accept", "application/json")
        req.add_header("User-Agent", _USER_AGENT)
        for k, v in self.default_headers.items():
            req.add_header(k, v)
        try:
            from hermes_cli.urllib_security import open_credentialed_url

            with open_credentialed_url(req, timeout=timeout) as resp:
                data = json.loads(resp.read().decode())
            items = data if isinstance(data, list) else data.get("data", [])
            for item in items:
                if not isinstance(item, dict) or not item.get("id"):
                    continue
                entry: dict[str, Any] = {}
                for opt in item.get("reasoning_options") or ():
                    if (
                        isinstance(opt, dict)
                        and opt.get("type") == "effort"
                        and opt.get("values")
                    ):
                        entry["efforts"] = tuple(opt["values"])
                if isinstance(item.get("context_length"), int):
                    entry["context_length"] = item["context_length"]
                _CATALOG[item["id"]] = entry
            return [
                item["id"]
                for item in items
                if isinstance(item, dict) and item.get("id")
            ]
        except Exception as exc:
            logger.debug("fetch_models(%s): %s", self.name, exc, exc_info=True)
            return None

    def build_api_kwargs_extras(
        self,
        *,
        reasoning_config: dict | None = None,
        model: str | None = None,
        **context: Any,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        if not isinstance(reasoning_config, dict):
            return {}, {}
        if reasoning_config.get("enabled") is False:
            return {}, {"reasoning_effort": "none"}
        effort = str(reasoning_config.get("effort") or "").strip().lower()
        if not effort:
            return {}, {}
        entry = _CATALOG.get(model or "")
        if entry is not None:
            efforts = entry.get("efforts")
            if efforts is None:
                return {}, {}
            effort = _clamp_effort(effort, efforts) or ""
        return {}, ({"reasoning_effort": effort} if effort else {})

    def supported_reasoning_efforts(
        self, model: str | None
    ) -> tuple[str, ...] | None:
        entry = _CATALOG.get(model or "")
        return None if entry is None else entry.get("efforts", ())

    def get_model_context_length(self, model: str) -> int | None:
        entry = _CATALOG.get(model or "")
        return entry.get("context_length") if entry else None


modal = ModalProfile(
    name="modal",
    display_name="Modal",
    description="Modal Endpoints for OpenAI-compatible APIs",
    signup_url="https://modal.com/settings",
    env_vars=("MODAL_PROXY_TOKEN", "MODAL_BASE_URL"),
    base_url="https://inference.us-west.modal.direct/v1",
    metadata_hostnames=("modal.direct", "modal.run"),
    default_headers={"User-Agent": _USER_AGENT},
)

register_provider(modal)
