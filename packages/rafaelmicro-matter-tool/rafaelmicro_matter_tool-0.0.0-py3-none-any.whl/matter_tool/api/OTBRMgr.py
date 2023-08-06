from .struct import OTBRData as OTBRDhelpper
from ..extlib.CMDAccess.CMDAccess import CMDAccess
from ..extlib.TyperExt.TyperExt import TyperExt


class OTBRMgr:

    def __init__(self) -> None:
        self._CMDAccess = CMDAccess()
        self._TyperExt = TyperExt()
        pass

    def pass_hex(self, context):
        rsp = context[0].split('\r\n')[0]
        return rsp

    def pass_data(self, context):
        check_list = [
            "Active_Timestamp", "Channel", "Channel_Mask",
            "Ext_PAN_ID", "Mesh_Local_Prefix", "Network_Key",
            "Network_Name", "PAN_ID", "PSKc", "Security_Policy"
        ]
        single_tag = []
        for row in context[0].split('\r\n'):
            for item in row.split(': '):
                single_tag.append(item)
        rsp = {}
        for i in range(len(single_tag)):
            target_key = single_tag[i].replace(" ", "_")
            if (target_key in check_list):
                rsp[target_key] = single_tag[i+1]
        return rsp

    def pass_state(self, context):
        rsp = context[0].split('\r\n')[0]
        return rsp

    CMDList = OTBRDhelpper.CMDList
    PasserMapper = {
        CMDList.OT_DATA_HEX.name: pass_hex,
        CMDList.OT_DATA.name: pass_data,
        CMDList.OT_STATE.name: pass_state,
    }

    def data_passer(self, ContextType: OTBRDhelpper.CMDList, context: str) -> None:
        if not OTBRDhelpper.check_command_exists(ContextType.value):
            self._TyperExt.raise_error(1, 'Command not exists')
        rsp = self.PasserMapper[ContextType.value](self, context)
        return rsp

    def handle_command(self, ContextType: OTBRDhelpper.CMDList) -> None:
        resbin = self._CMDAccess.handle_OT_CMD(ContextType)
        result = self.data_passer(ContextType, resbin)
        self._TyperExt.attach_log(str(result), self._TyperExt.Colors.GREEN)
        self._TyperExt.attach_log('Success: Execute command',
                                  self._TyperExt.Colors.GREEN)
        return result
