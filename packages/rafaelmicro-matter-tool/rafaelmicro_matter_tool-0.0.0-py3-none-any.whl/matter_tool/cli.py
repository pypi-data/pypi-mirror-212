import typer
from typing import Optional
from .api.ChipToolMgr import ChipToolMgr
from .api.ChipToolMgr import ChipToolLightMgr
from .api.ChipToolMgr import ChipToolSwitchMgr
from .api.ChipToolMgr import ChipToolConnectMgr
from .api.OTBRMgr import OTBRMgr
from .api.struct import OTBRData as CMDhelpper
from . import __app_name__, __version__

app = typer.Typer()

### Thread Command ###


@app.command(name="state")
def get_state() -> None:
    """[Thread] Get Thread Network state."""
    OTBRMgr().handle_command(CMDhelpper.QueryCMDMapper.STATE)


@app.command(name="dataset")
def get_dataset(
        hex: Optional[int] = typer.Option(
            0, "--hex", "-x",
            help="BLE adapter with HCI device [int]",
        )) -> None:
    """[Thread] Get Thread active dataset."""
    if (hex == 0):
        OTBRMgr().handle_command(CMDhelpper.QueryCMDMapper.DATA)
    else:
        OTBRMgr().handle_command(CMDhelpper.QueryCMDMapper.HEX)

### Matter Command ###


@app.command(name="connect")
def pair_thread(
        name: Optional[str] = typer.Argument(
            None, help="device alias",
        ),
        devicetype: Optional[str] = typer.Argument(
            None, help="device type",
        ),
        pincode: Optional[str] = typer.Argument(
            None, help="device pincode",
        ),
        discriminator: Optional[int] = typer.Argument(
            None, help="device long discriminator",
        ),
        ble_adapter: Optional[int] = typer.Option(
            0, "--ble-adapter", "-b",
            help="BLE adapter with HCI device [int]",
        ), ) -> None:
    """[Matter] Pair device with Thread."""
    ChipToolConnectMgr().connect(name, devicetype, pincode, discriminator, ble_adapter)


@app.command(name="gen_group")
def gen_group(
    group_name: Optional[str] = typer.Argument(
        None, help="Group name",
    ),
) -> None:
    """[Matter] Generate group."""
    ChipToolSwitchMgr().gen_group(group_name)
    return


@app.command(name="add_group")
def add_group(
    group_name: Optional[str] = typer.Argument(
        None, help="Group name",
    ),
    target_type: Optional[str] = typer.Argument(
        None, help="target device type",
    ),
    target_name: Optional[str] = typer.Argument(
        None, help="Connected target name",
    ),
    target_endpoint: Optional[int] = typer.Option(
        1, "--target-endpoint", "-l",
        help="target endpoint",
    ),
) -> None:
    """[Matter] Add device to group."""
    ChipToolSwitchMgr().add_group(group_name, target_type, target_name, target_endpoint)
    return


@app.command(name="onoff")
def get_state(
    action: Optional[str] = typer.Argument(
        'on', help="control light: [on/off/toggle]",
    ),
    light_name: Optional[str] = typer.Argument(
        None, help="target light name",
    ),
    endpoint: Optional[int] = typer.Argument(
        1, help="target endpoint",
    ),
) -> None:
    """[Matter] Onoff control Matter Light."""
    ChipToolLightMgr().onoff(action, light_name, endpoint)
    return


@app.command(name="level")
def get_state(
    level: Optional[int] = typer.Argument(
        0, help="target level",
    ),
    transition: Optional[int] = typer.Option(
        0, "--transition", "-t",
        help="transitiontime",
    ),
    light_name: Optional[str] = typer.Argument(
        None, help="target light name",
    ),
    endpoint: Optional[int] = typer.Argument(
        1, help="target endpoint",
    ),
) -> None:
    """[Matter] level control Matter Light."""
    ChipToolLightMgr().level(level, light_name, endpoint, transition)
    return


@app.command(name="show")
def get_state(
    display: Optional[int] = typer.Option(
        0, "--display-level", "-d",
        help="""
        Matter Profile Level:\n
        level 0 (default): display node profile\n
        level 1: display Matter profile\n
        level 2: display Matter profile and Matter stack information\n
        """,
    )
) -> None:
    """[Matter] show matter profile"""
    if (display == 1):
        ChipToolMgr().list_node_profile()
    elif (display == 1):
        ChipToolMgr().list_node_profile()
        ChipToolMgr().list_binding_profile()
        ChipToolMgr().list_group_mapper_profile()
    elif (display == 2):
        ChipToolMgr().list_node_profile()
        ChipToolMgr().list_binding_profile()
        ChipToolMgr().list_group_mapper_profile()
        ChipToolMgr().list_acl_profile()
        ChipToolMgr().list_group_profile()


@app.command(name="bind")
def get_state(
    light_name: Optional[str] = typer.Argument(
        None, help="Connected light name",
    ),
    light_endpoint: Optional[int] = typer.Option(
        1, "--light-endpoint", "-l",
        help="target light endpoint",
    ),
    switch_name: Optional[str] = typer.Argument(
        None, help="Connected switch name",
    ),
    switch_endpoint: Optional[int] = typer.Option(
        1, "--switch-endpoint", "-s",
        help="target switch endpoint",
    ),
) -> None:
    """[Matter] Set binding between light and switch."""
    ChipToolSwitchMgr().set_binding(
        light_name, light_endpoint, switch_name, switch_endpoint)
    return


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return
