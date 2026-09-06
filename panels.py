"""Panel UI for Deel Connector following UI_INTERFACE_STANDARD.md and AUTH_AND_CREDENTIALS_STANDARD.md."""
from __future__ import annotations
from imperal_sdk import ui
from app import ext

def _settings_button() -> ui.UINode:
    return ui.Button(
        "App settings",
        variant="secondary",
        size="sm",
        icon="settings",
        on_click=ui.Call("__panel__deel_settings")
    )

def _help_modal() -> ui.UINode:
    return ui.Modal(
        trigger=ui.Button("How do I connect Deel?", variant="ghost", size="sm"),
        title="Connecting Deel",
        children=[
            ui.Text(
                "1. Sign in to your Deel account at app.letsdeel.com.\n"
                "2. Navigate to Organization Settings > Integrations / Developer Center.\n"
                "3. Under API Tokens, generate a dedicated REST API Bearer Token.\n"
                "4. Paste your token above and click Connect Deel.",
                variant="body"
            )
        ]
    )

@ext.panel("deel_sidebar", slot="left")
async def deel_sidebar(ctx, **kwargs) -> ui.UINode:
    return ui.Stack(
        direction="v",
        gap=3,
        align="stretch",
        children=[
            ui.Text("Deel", variant="heading"),
            ui.Text("Manage global workforce, contracts, people, payroll runs, time-off and invoices via Deel REST API v2.", variant="caption"),
            ui.Divider(),
            ui.Form(
                submit_label="Connect Deel",
                action=ui.Call("connect_deel"),
                children=[
                    ui.Stack(
                        direction="v",
                        gap=2,
                        align="stretch",
                        children=[
                            ui.Text("API Bearer Token", variant="caption"),
                            ui.Input(
                                param_name="api_token",
                                placeholder="Enter Deel API Token",
                                value=""
                            ),
                            ui.Text("Connection Label (Optional)", variant="caption"),
                            ui.Input(
                                param_name="label",
                                placeholder="e.g. Acme Global Deel",
                                value=""
                            ),
                            ui.Text("Base URL (Optional)", variant="caption"),
                            ui.Input(
                                param_name="base_url",
                                placeholder="https://api.letsdeel.com/rest/v2",
                                value=""
                            )
                        ]
                    )
                ]
            ),
            _help_modal(),
            ui.Divider(),
            _settings_button()
        ]
    )
