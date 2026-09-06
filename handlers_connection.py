"""Connection lifecycle for Deel Connector."""
from __future__ import annotations
import json, uuid
from imperal_sdk import ActionResult
from deel_client import DeelClient
from app import chat
from schemas import (
    NoParams,
    ConnectParams, ConnectionIdParams, ConnectionList, ConnectionRecord, DeleteResult
)

_SECRET = "deel_connections"

def _mask(value: str) -> str:
    return value[:4] + "…" + value[-4:] if len(value) > 10 else "***"

async def _load_connections(ctx) -> list[dict]:
    raw = await ctx.secrets.get(_SECRET)
    if not raw: return []
    try: data = json.loads(raw)
    except: return []
    return data if isinstance(data, list) else []

async def _save_connections(ctx, conns: list[dict]) -> None:
    await ctx.secrets.set(_SECRET, json.dumps(conns))

async def resolve_connection(ctx, connection_id: str = "") -> dict | None:
    conns = await _load_connections(ctx)
    if not conns: return None
    if not connection_id:
        for c in conns:
            if c.get("is_active"):
                return c
        return conns[0]
    for c in conns:
        if c["id"] == connection_id:
            return c
    return None

@chat.function(
    "connect_deel",
    "Connect Deel account via credentials.",
    action_type="write",
    chain_callable=True,
    event="deel-connector.connect_deel",
    effects=["create:connection"],
    data_model=ConnectParams
)
async def connect_deel(ctx, params: ConnectParams) -> ActionResult[ConnectionRecord]:
    """Connect a new Deel account."""
    client = DeelClient(
        api_token=params.api_token,
        base_url=params.base_url
    )
    v_res = await client.verify_auth()
    if v_res.get("status") == "error":
        return ActionResult.error(
            v_res.get("message", "Failed to connect to Deel"),
            code=v_res.get("code", "UNAUTHORIZED")
        )

    conns = await _load_connections(ctx)
    cid = f"deel_{uuid.uuid4().hex[:8]}"
    for c in conns:
        c["is_active"] = False

    rec = {
        "id": cid,
        "label": params.label or f"Deel ({cid})",
        "masked_key": _mask(params.api_token),
        "api_token": params.api_token,
        "base_url": client.base_url,
        "is_active": True
    }
    conns.append(rec)
    await _save_connections(ctx, conns)

    return ActionResult(
        data=ConnectionRecord(
            id=rec["id"],
            label=rec["label"],
            masked_key=rec["masked_key"],
            base_url=rec["base_url"],
            is_active=rec["is_active"]
        ),
        summary=f"Connected to Deel ({rec['label']})."
    )

@chat.function(
    "list_connections",
    "List connected Deel accounts.",
    action_type="read",
    chain_callable=True,
    data_model=NoParams
)
async def list_connections(ctx, params: NoParams) -> ActionResult[ConnectionList]:
    """List all connected Deel accounts."""
    conns = await _load_connections(ctx)
    records = [
        ConnectionRecord(
            id=c["id"],
            label=c.get("label", ""),
            masked_key=c.get("masked_key", "***"),
            base_url=c.get("base_url", ""),
            is_active=c.get("is_active", False)
        )
        for c in conns
    ]
    return ActionResult(
        data=ConnectionList(connections=records, total=len(records)),
        summary=f"Found {len(records)} connected Deel account(s)."
    )

@chat.function(
    "disconnect_deel",
    "Disconnect Deel account.",
    action_type="write",
    chain_callable=True,
    event="deel-connector.disconnect_deel",
    effects=["delete:connection"],
    data_model=ConnectionIdParams
)
async def disconnect_deel(ctx, params: ConnectionIdParams) -> ActionResult[DeleteResult]:
    """Disconnect a saved Deel account."""
    conns = await _load_connections(ctx)
    target = None
    if params.connection_id:
        target = next((c for c in conns if c["id"] == params.connection_id), None)
    elif conns:
        target = next((c for c in conns if c.get("is_active")), conns[0])

    if not target:
        return ActionResult.error("No matching Deel connection found to disconnect", code="NOT_FOUND")

    conns = [c for c in conns if c["id"] != target["id"]]
    if conns and not any(c.get("is_active") for c in conns):
        conns[0]["is_active"] = True
    await _save_connections(ctx, conns)

    return ActionResult(
        data=DeleteResult(
            id=target["id"],
            deleted=True,
            message=f"Disconnected Deel connection {target.get('label', target['id'])}."
        ),
        summary=f"Disconnected Deel connection {target.get('label', target['id'])}."
    )
