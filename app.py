"""Extension declaration, capabilities, health check for Deel Connector."""
from __future__ import annotations
import json
from imperal_sdk import ChatExtension, Extension

ext = Extension(
    "deel-connector",
    version="0.1.0",
    display_name="Deel",
    icon="icon.svg",
    capabilities=["deel:manage"],
    description="Official Imperal connector for Deel (C28. Payroll & Benefits Administration). Manage operations securely."
)

chat = ChatExtension(ext)

@ext.health_check
async def health_check(ctx) -> dict:
    raw = await ctx.secrets.get("deel_connections")
    try:
        count = len(json.loads(raw)) if raw else 0
    except Exception:
        count = 0
    return {
        "healthy": True,
        "detail": f"{count} Deel connection(s) configured." if count else "Not connected yet."
    }
