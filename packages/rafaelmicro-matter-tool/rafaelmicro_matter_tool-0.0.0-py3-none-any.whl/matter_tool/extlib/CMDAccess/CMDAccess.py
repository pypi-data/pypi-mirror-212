import subprocess
import typer
from ..TyperExt.TyperExt import TyperExt
from ...api.struct import OTBRData as OTBRHelpper


class CMDAccess:

    def __init__(self) -> None:
        self._TyperExt = TyperExt()
        pass

    def send_command(self, command_list: list):
        try:
            cmd_handle = subprocess.Popen(
                command_list, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            rsp = []

            for line in cmd_handle.stdout:
                rsp.append(line.decode())
                typer.secho(line.decode(), nl=False, fg=typer.colors.RESET)
            status = cmd_handle.wait()
        except Exception as e:
            self._TyperExt.raise_error(1, str(e))
        return status, rsp

    def handle_OT_CMD(self, command: OTBRHelpper.QueryCMDMapper, *args, **kwargs):  # , *args, **kwargs
        if not (OTBRHelpper.check_query_exists(command.name)):
            self._TyperExt.raise_error(1, 'command not found ' + str(command))
        prefix = OTBRHelpper.get_query_prefix(command.name)
        status, rsp = self.send_command(prefix)
        return rsp
