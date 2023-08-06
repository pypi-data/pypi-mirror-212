from enum import Enum
import json
import re
from prettytable import PrettyTable
from .OTBRMgr import OTBRMgr
from ..extlib.CMDAccess.CMDAccess import CMDAccess
from ..extlib.TyperExt.TyperExt import TyperExt
from ..module.data.MatterDM import MatterDM
from .struct import OTBRData as OTBRhelpper
from .struct import ChipToolData as ChipToolhelpper
import dataclasses
from dataclasses import dataclass


class ChipToolMgr:
    def __init__(self) -> None:
        self._TyperExt = TyperExt()
        self._OTBRMgr = OTBRMgr()
        self._MatterDM = MatterDM()

    def get_thread_network(self) -> None:
        return self._OTBRMgr.handle_command(OTBRhelpper.QueryCMDMapper.HEX)

    def list_node_profile(self):
        self._TyperExt.attach_log(
            "=== [Matter Profile] Node ===",
            self._TyperExt.Colors.BRIGHT_YELLOW)
        self.clear_failed_data()
        node_list = self._MatterDM.get_node_list()
        nodeid = []
        name = []
        devicetype = []
        status = []
        fabric = []
        for node in node_list["matter"]["node"]:
            nodeid.append(node["nodeid"])
            name.append(node["name"])
            devicetype.append(node["devicetype"])
            status.append(node["status"])
            fabric.append(node["fabric"])
        tab = PrettyTable()
        tab.add_column('nodeid', nodeid, align='r', valign='t')
        tab.add_column('name', name, align='r', valign='t')
        tab.add_column('devicetype', devicetype, align='r', valign='t')
        tab.add_column('status', status, align='r', valign='t')
        tab.add_column('fabric', fabric, align='r', valign='t')
        self._TyperExt.attach_log(tab, self._TyperExt.Colors.GREEN)

    def list_binding_profile(self):
        self._TyperExt.attach_log(
            "=== [Matter Profile] Binding List ===",
            self._TyperExt.Colors.BRIGHT_YELLOW)
        self.clear_failed_data()
        binding_list = self._MatterDM.get_fully_binding_list()
        name = []
        fabric = []
        nodeid = []
        target_name = []
        target_id = []
        endpoint = []
        for binding in binding_list["matter"]["binding"]:
            name.append(binding["name"])
            fabric.append(binding["fabric"])
            nodeid.append(binding["nodeid"])
            target_name.append(binding["target_name"])
            target_id.append(binding["target_id"])
            endpoint.append(binding["endpoint"])
        tab = PrettyTable()
        tab.add_column('name', name, align='r', valign='t')
        tab.add_column('fabric', fabric, align='r', valign='t')
        tab.add_column('nodeid', nodeid, align='r', valign='t')
        tab.add_column('target_name', target_name, align='r', valign='t')
        tab.add_column('target_id', target_id, align='r', valign='t')
        tab.add_column('endpoint', endpoint, align='r', valign='t')
        self._TyperExt.attach_log(tab, self._TyperExt.Colors.GREEN)

    def list_group_mapper_profile(self):
        self._TyperExt.attach_log(
            "=== [Matter Profile] Group Mapper List ===",
            self._TyperExt.Colors.BRIGHT_YELLOW)
        self.clear_failed_data()
        group_mapper_list = self._MatterDM.get_fully_group_mapper_list()
        name = []
        group_id = []
        target_id = []
        target_name = []
        target_type = []
        target_endpoint = []
        status = []
        for group_mapper in group_mapper_list["matter"]["group_mapper"]:
            name.append(group_mapper["name"])
            group_id.append(group_mapper["group_id"])
            target_id.append(group_mapper["target_id"])
            target_name.append(group_mapper["target_name"])
            target_type.append(group_mapper["target_type"])
            target_endpoint.append(group_mapper["target_endpoint"])
            status.append(group_mapper["status"])
        tab = PrettyTable()
        tab.add_column('name', name, align='r', valign='t')
        tab.add_column('group_id', group_id, align='r', valign='t')
        tab.add_column('target_id', target_id, align='r', valign='t')
        tab.add_column('target_name', target_name, align='r', valign='t')
        tab.add_column('target_type', target_type, align='r', valign='t')
        tab.add_column('target_endpoint', target_endpoint,
                       align='r', valign='t')
        tab.add_column('status', status, align='r', valign='t')
        self._TyperExt.attach_log(tab, self._TyperExt.Colors.GREEN)

    def list_acl_profile(self):
        self._TyperExt.attach_log(
            "=== [Matter Stack] Access Control List ===",
            self._TyperExt.Colors.BRIGHT_YELLOW)
        self.clear_failed_data()
        acl_list = self._MatterDM.get_fully_acl_list()
        name = []
        fabric = []
        nodeid = []
        target_name = []
        target_id = []
        privilege = []
        auto_mode = []
        for acl in acl_list["matter"]["acl"]:
            name.append(acl["name"])
            fabric.append(acl["fabric"])
            nodeid.append(acl["nodeid"])
            target_name.append(acl["target_name"])
            target_id.append(acl["target_id"])
            privilege.append(acl["privilege"])
            auto_mode.append(acl["auto_mode"])
        tab = PrettyTable()
        tab.add_column('name', name, align='r', valign='t')
        tab.add_column('fabric', fabric, align='r', valign='t')
        tab.add_column('nodeid', nodeid, align='r', valign='t')
        tab.add_column('target_name', target_name, align='r', valign='t')
        tab.add_column('target_id', target_id, align='r', valign='t')
        tab.add_column('privilege', privilege, align='r', valign='t')
        tab.add_column('auto_mode', auto_mode, align='r', valign='t')
        self._TyperExt.attach_log(tab, self._TyperExt.Colors.GREEN)

    def list_group_profile(self):
        self._TyperExt.attach_log(
            "=== [Matter Stack] Access Control List ===",
            self._TyperExt.Colors.BRIGHT_YELLOW)
        self.clear_failed_data()
        group_list = self._MatterDM.get_fully_group_list()
        name = []
        group_id = []
        group_keyset_id = []
        epochkey0 = []
        epochkey1 = []
        epochkey2 = []
        for group in group_list["matter"]["group"]:
            name.append(group["name"])
            group_id.append(group["group_id"])
            group_keyset_id.append(group["group_keyset_id"])
            epochkey0.append(group["epochkey0"])
            epochkey1.append(group["epochkey1"])
            epochkey2.append(group["epochkey2"])
        tab = PrettyTable()
        tab.add_column('name', name, align='r', valign='t')
        tab.add_column('group_id', group_id, align='r', valign='t')
        tab.add_column('group_keyset_id', group_keyset_id,
                       align='r', valign='t')
        tab.add_column('epochkey0', epochkey0, align='r', valign='t')
        tab.add_column('epochkey1', epochkey1, align='r', valign='t')
        tab.add_column('epochkey2', epochkey2, align='r', valign='t')
        self._TyperExt.attach_log(tab, self._TyperExt.Colors.GREEN)

    def get_profile(self, name):
        return self._MatterDM.get_node("name", name)

    def get_acl(self, name):
        return self._MatterDM.get_acl_list("name", name)

    def get_binding(self, name):
        return self._MatterDM.get_binding_list("name", name)

    def get_group(self, key, data):
        return self._MatterDM.get_group(key, data)

    def get_match_group(self, key, data):
        return self._MatterDM.get_match_group_list(key, data)

    def get_group_mapper(self, key, data):
        return self._MatterDM.get_group_mapper_list(key, data)

    def new_node_profile(self, *args, **kwargs):
        node = self._MatterDM.create_node(
            name=kwargs['name'], devicetype=kwargs['devicetype'], status="Pending")
        status = self._MatterDM.add_node(node)
        return node

    def new_acl_profile(self, *args, **kwargs):
        acl = self._MatterDM.create_acl(
            name=kwargs['name'], nodeid=kwargs['nodeid'], fabric=kwargs['fabric'],
            target_name=kwargs['target_name'], target_id=kwargs['target_id'],
            privilege=kwargs['privilege'], auto_mode=kwargs['auto_mode']
        )
        return acl

    def new_binding_profile(self, *args, **kwargs):
        binding = self._MatterDM.create_binding(
            name=kwargs['name'], fabric=kwargs['fabric'],
            nodeid=kwargs['nodeid'], target_name=kwargs['target_name'],
            target_id=kwargs['target_id'], endpoint=kwargs['endpoint']
        )
        return binding

    def new_group_profile(self, *args, **kwargs):
        group = self._MatterDM.create_group(name=kwargs['name'])
        status = self._MatterDM.add_group(group)
        return group

    def new_group_mapper_profile(self, *args, **kwargs):
        group_mapper = self._MatterDM.create_group_mapper(
            name=kwargs['name'], group_id=kwargs['group_id'],
            target_id=kwargs['target_id'], target_name=kwargs['target_name'],
            target_type=kwargs['target_type'], target_endpoint=kwargs['target_endpoint'],
            status=kwargs['status']
        )
        self._MatterDM.add_group_mapper(group_mapper)
        return group_mapper

    def apply_acl_profile(self, acl):
        self._MatterDM.add_acl(acl)

    def apply_binding_profile(self, binding):
        self._MatterDM.add_binding(binding)

    def update_profile(self, node):
        self._MatterDM.update_node(node)

    def update_group_profile(self, group):
        self._MatterDM.update_group_mapper(group)

    def unique_profile(self, target, key):
        return list(set(item[key] for item in target))

    def clear_failed_data(self):
        self._MatterDM.clear_failed_node()
        self._MatterDM.clear_failed_group_mapper()


class ChipToolLightMgr:
    class OnoffAction(Enum):
        ON = 'on'
        OFF = 'off'
        TOGGLE = 'toggle'

    def __init__(self) -> None:
        self._TyperExt = TyperExt()
        self._CMDAccess = CMDAccess()
        self._ChipToolMgr = ChipToolMgr()

    def onoff_passer(self, *args, **kwargs) -> None:
        return ChipToolhelpper.CMDList.LIGHT_ONOFF.value + [
            str(kwargs["contain"]["action"]),
            str(kwargs["contain"]["nodeid"]),
            str(kwargs["contain"]["endpoint"])
        ]

    def level_passer(self, *args, **kwargs) -> None:
        return ChipToolhelpper.CMDList.LEVEL_CTL.value + [
            str(kwargs["contain"]["level"]),
            str(kwargs["contain"]["transition"]),
            "0", "0",
            str(kwargs["contain"]["nodeid"]),
            str(kwargs["contain"]["endpoint"])
        ]

    def acl_passer(self, *args, **kwargs) -> None:
        # self._TyperExt.attach_log(json.dumps(
        #     ChipToolhelpper.CMDList.SET_ACL.value + [
        #         kwargs["contain"]["acl"],
        #         str(kwargs["contain"]["light_id"]),
        #         str(kwargs["contain"]["endpoint"])
        #     ]), self._TyperExt.Colors.BRIGHT_MAGENTA)
        return ChipToolhelpper.CMDList.SET_ACL.value + [
            kwargs["contain"]["acl"],
            str(kwargs["contain"]["light_id"]),
            str(kwargs["contain"]["endpoint"])
        ]

    def acl_json_passer(self, acl_list) -> None:
        rsp = [{
            "fabricIndex": acl_list[0]['fabric'],
            "privilege": 3, "authMode": 2,
            "subjects": [], "targets": None}, {
            "fabricIndex": acl_list[0]['fabric'],
            "privilege": 3, "authMode": 3,
            "subjects": [], "targets": None
        }]
        for acl in acl_list:
            if acl['target_id'] == 112233:
                rsp.append({
                    "fabricIndex": acl_list[0]['fabric'],
                    "privilege": 5, "authMode": 2,
                    "subjects": [acl['target_id']], "targets": None
                })
            elif (acl["privilege"] == 3 and acl["auto_mode"] == 2):
                rsp[0]["subjects"].append(acl['target_id'])
            elif (acl["privilege"] == 3 and acl["auto_mode"] == 3):
                rsp[1]["subjects"].append(acl['target_id'])
        # self._TyperExt.attach_log(
        #     "="*50, self._TyperExt.Colors.BRIGHT_MAGENTA)
        # self._TyperExt.attach_log(json.dumps(
        #     rsp), self._TyperExt.Colors.BRIGHT_MAGENTA)
        return json.dumps(rsp)

    def command_passer(self, context_type, *args, **kwargs) -> None:
        cancat_dict = {
            ChipToolhelpper.QueryCMDMapper.LIGHT_ONOFF: self.onoff_passer,
            ChipToolhelpper.QueryCMDMapper.LEVEL_CONTROL: self.level_passer,
            ChipToolhelpper.QueryCMDMapper.ACCESS_CONTROL: self.acl_passer,
        }
        return cancat_dict[context_type](contain=kwargs["contain"])

    def handle_command(self, context_type: ChipToolhelpper.QueryCMDMapper, *args, **kwargs) -> None:
        command = self.command_passer(context_type, contain=kwargs)
        status, result = self._CMDAccess.send_command(command)
        return status, result

    def onoff(self, action, light_name, endpoint) -> None:
        self._ChipToolMgr.clear_failed_data()
        if not (any(x for x in self.OnoffAction if x.value == action)):
            self._TyperExt.raise_error(1, 'Invailed action type')
        light_node = self._ChipToolMgr.get_profile(light_name)
        status, result = self.handle_command(ChipToolhelpper.QueryCMDMapper.LIGHT_ONOFF,
                                             action=action, nodeid=light_node['nodeid'],
                                             endpoint=endpoint)
        if not (status == 0):
            self._TyperExt.raise_error(1, 'Failed: Connect failed')

        self._TyperExt.attach_log("The node: " + light_name + ", action: " + str(action),
                                  self._TyperExt.Colors.GREEN)

    def level(self, level, light_name, endpoint, transition) -> None:
        self._ChipToolMgr.clear_failed_data()
        light_node = self._ChipToolMgr.get_profile(light_name)
        status, result = self.handle_command(ChipToolhelpper.QueryCMDMapper.LEVEL_CONTROL,
                                             level=level, nodeid=light_node['nodeid'],
                                             transition=transition, endpoint=endpoint)
        if not (status == 0):
            self._TyperExt.raise_error(1, 'Failed: Connect failed')

        self._TyperExt.attach_log("The node: " + light_name + ", set level: " + str(level),
                                  self._TyperExt.Colors.GREEN)

    def set_acl(self, light_node, switch_node) -> None:
        acl = self._ChipToolMgr.get_acl(light_node["name"])

        target_acl = {
            "name": light_node["name"], "fabric": light_node["fabric"],
            "nodeid": light_node["nodeid"], "target_name": switch_node["name"],
            "target_id": switch_node["nodeid"], "privilege": 3, "auto_mode": 2,
        }
        if (target_acl not in acl):
            acl.append(target_acl)
        else:
            self._TyperExt.attach_log(
                "ACL already existed", self._TyperExt.Colors.BRIGHT_MAGENTA)

        # self._TyperExt.attach_log(json.dumps(
        #     acl), self._TyperExt.Colors.BRIGHT_MAGENTA)
        status, result = self.handle_command(
            ChipToolhelpper.QueryCMDMapper.ACCESS_CONTROL,
            acl=self.acl_json_passer(acl),
            light_id=light_node["nodeid"],
            endpoint=0
        )
        if not (status == 0):
            self._TyperExt.raise_error(1, 'Failed: set light ACL failed')

        acl = self._ChipToolMgr.new_acl_profile(
            name=light_node["name"], fabric=light_node["fabric"],
            nodeid=light_node["nodeid"], target_name=switch_node["name"],
            target_id=switch_node["nodeid"], privilege=3, auto_mode=2
        )
        self._ChipToolMgr.apply_acl_profile(acl)

    def set_group_acl(self, node, group) -> None:
        acl = self._ChipToolMgr.get_acl(node["name"])
        target_acl = {
            "name": node["name"], "fabric": node["fabric"],
            "nodeid": node["nodeid"], "target_name": group["name"],
            "target_id": group["nodeid"], "privilege": 3, "auto_mode": 3,
        }
        if (target_acl not in acl):
            acl.append(target_acl)
        else:
            self._TyperExt.attach_log(
                "ACL already existed", self._TyperExt.Colors.BRIGHT_MAGENTA)

        # self._TyperExt.attach_log(json.dumps(
        #     acl), self._TyperExt.Colors.BRIGHT_MAGENTA)
        status, result = self.handle_command(
            ChipToolhelpper.QueryCMDMapper.ACCESS_CONTROL,
            acl=self.acl_json_passer(acl),
            light_id=node["nodeid"],
            endpoint=0
        )
        if not (status == 0):
            self._TyperExt.raise_error(1, 'Failed: set light ACL failed')

        acl = self._ChipToolMgr.new_acl_profile(
            name=node["name"], nodeid=node["nodeid"], fabric=node["fabric"],
            target_name=group["name"], target_id=group["nodeid"],
            privilege=3, auto_mode=3
        )
        self._ChipToolMgr.apply_acl_profile(acl)


class ChipToolSwitchMgr:
    @dataclass
    class GroupKeySet():
        groupKeySetID: int
        groupKeySecurityPolicy: int
        epochKey0: str
        epochStartTime0: int
        epochKey1: str
        epochStartTime1: int
        epochKey2: str
        epochStartTime2: int

    def __init__(self) -> None:
        self._TyperExt = TyperExt()
        self._CMDAccess = CMDAccess()
        self._ChipToolMgr = ChipToolMgr()
        self._ChipToolLightMgr = ChipToolLightMgr()

    def binding_passer(self, *args, **kwargs) -> None:
        self._TyperExt.attach_log(json.dumps(
            ChipToolhelpper.CMDList.WRITE_BINDING.value + [
                kwargs["contain"]["binding_list"],
                str(kwargs["contain"]["nodeid"]),
                str(kwargs["contain"]["endpoint"])
            ]), self._TyperExt.Colors.BRIGHT_MAGENTA)
        return ChipToolhelpper.CMDList.WRITE_BINDING.value + [
            kwargs["contain"]["binding_list"],
            str(kwargs["contain"]["nodeid"]),
            str(kwargs["contain"]["endpoint"])
        ]

    def group_passer(self, *args, **kwargs) -> None:
        self._TyperExt.attach_log(json.dumps(
            ChipToolhelpper.CMDList.CREATE_GROUP.value + [
                str(kwargs["contain"]["name"]),
                str(kwargs["contain"]["group_id"])
            ]), self._TyperExt.Colors.BRIGHT_MAGENTA)
        return ChipToolhelpper.CMDList.CREATE_GROUP.value + [
            str(kwargs["contain"]["name"]),
            str(kwargs["contain"]["group_id"])
        ]

    def keyset_passer(self, *args, **kwargs) -> None:
        self._TyperExt.attach_log(json.dumps(
            ChipToolhelpper.CMDList.CREATE_KEYSET.value + [
                str(kwargs["contain"]["group_keyset_id"]),
                str(kwargs["contain"]["groupKeySecurityPolicy"]),
                str(kwargs["contain"]["epochStartTime0"]),
                'hex:'+str(kwargs["contain"]["epochKey0"])
            ]), self._TyperExt.Colors.BRIGHT_MAGENTA)
        return ChipToolhelpper.CMDList.CREATE_KEYSET.value + [
            str(kwargs["contain"]["group_keyset_id"]),
            str(kwargs["contain"]["groupKeySecurityPolicy"]),
            str(kwargs["contain"]["epochStartTime0"]),
            'hex:'+str(kwargs["contain"]["epochKey0"])
        ]

    def bind_group_keyset_passer(self, *args, **kwargs) -> None:
        self._TyperExt.attach_log(json.dumps(
            ChipToolhelpper.CMDList.BIND_GROUP_KEYSET.value + [
                str(kwargs["contain"]["group_id"]),
                str(kwargs["contain"]["group_keyset_id"])
            ]), self._TyperExt.Colors.BRIGHT_MAGENTA)
        return ChipToolhelpper.CMDList.BIND_GROUP_KEYSET.value + [
            str(kwargs["contain"]["group_id"]),
            str(kwargs["contain"]["group_keyset_id"])
        ]

    def apply_keyset_passer(self, *args, **kwargs) -> None:
        self._TyperExt.attach_log(json.dumps(
            ChipToolhelpper.CMDList.APPLY_KEYSET.value + [
                kwargs["contain"]["group_key_set"],
                str(kwargs["contain"]["target_nodeid"]),
                str(kwargs["contain"]["target_endpoint"])
            ]), self._TyperExt.Colors.BRIGHT_MAGENTA)
        return ChipToolhelpper.CMDList.APPLY_KEYSET.value + [
            kwargs["contain"]["group_key_set"],
            str(kwargs["contain"]["target_nodeid"]),
            str(kwargs["contain"]["target_endpoint"])
        ]

    def apply_keyset_map_passer(self, *args, **kwargs) -> None:
        self._TyperExt.attach_log(json.dumps(
            ChipToolhelpper.CMDList.APPLY_KEYSET_MAP.value + [
                kwargs["contain"]["group_key_map_list"],
                str(kwargs["contain"]["target_nodeid"]),
                str(kwargs["contain"]["target_endpoint"])
            ]), self._TyperExt.Colors.BRIGHT_MAGENTA)
        return ChipToolhelpper.CMDList.APPLY_KEYSET_MAP.value + [
            kwargs["contain"]["group_key_map_list"],
            str(kwargs["contain"]["target_nodeid"]),
            str(kwargs["contain"]["target_endpoint"])
        ]

    def apply_group_passer(self, *args, **kwargs) -> None:
        self._TyperExt.attach_log(json.dumps(
            ChipToolhelpper.CMDList.APPLY_GROUP.value + [
                str(kwargs["contain"]["groupId"]),
                str(kwargs["contain"]["group_name"]),
                str(kwargs["contain"]["target_nodeid"]),
                str(kwargs["contain"]["target_endpoint"])
            ]), self._TyperExt.Colors.BRIGHT_MAGENTA)
        return ChipToolhelpper.CMDList.APPLY_GROUP.value + [
            str(kwargs["contain"]["groupId"]),
            str(kwargs["contain"]["group_name"]),
            str(kwargs["contain"]["target_nodeid"]),
            str(kwargs["contain"]["target_endpoint"])
        ]

    def binding_json_passer(self, binding_list) -> None:
        rsp = []
        for binding in binding_list:
            rsp.append({
                "fabricIndex": binding['fabric'], "node": binding["target_id"],
                "endpoint": binding["endpoint"], "cluster": 6
            })
        # self._TyperExt.attach_log(
        #     "="*50, self._TyperExt.Colors.BRIGHT_MAGENTA)
        # self._TyperExt.attach_log(json.dumps(
        #     rsp), self._TyperExt.Colors.BRIGHT_MAGENTA)
        return json.dumps(rsp)

    def keyset_map_json_passer(self, nodeid, fabric) -> None:
        group_mapper_list = self._ChipToolMgr.get_group_mapper(
            "target_id", nodeid)
        group_list = self._ChipToolMgr.unique_profile(
            group_mapper_list, "name")
        rows = []
        for group_item in group_list:
            rows += self._ChipToolMgr.get_match_group(
                "name", group_item)
        rsp = []
        for item in rows:
            # self._TyperExt.attach_log(json.dumps(
            #     item), self._TyperExt.Colors.BRIGHT_CYAN)
            rsp.append({
                "fabricIndex": fabric, "groupId": item["group_id"],
                "groupKeySetID": item["group_keyset_id"]
            })
        # self._TyperExt.attach_log(
        #     "="*50, self._TyperExt.Colors.BRIGHT_MAGENTA)
        # self._TyperExt.attach_log(json.dumps(
        #     rsp), self._TyperExt.Colors.BRIGHT_MAGENTA)
        return json.dumps(rsp)

    def group_binding_json_passer(self, nodeid, group_id) -> None:
        group_mapper_list = self._ChipToolMgr.get_group_mapper(
            "target_id", nodeid)
        group_list = self._ChipToolMgr.unique_profile(
            group_mapper_list, "group_id")
        rsp = []
        for group in group_list:
            rsp.append({"group": group})
        rsp.append({"group": group_id})
        # self._TyperExt.attach_log(
        #     "="*50, self._TyperExt.Colors.BRIGHT_MAGENTA)
        # self._TyperExt.attach_log(json.dumps(
        #     rsp), self._TyperExt.Colors.BRIGHT_MAGENTA)
        return json.dumps(rsp)

    def command_passer(self, context_type, *args, **kwargs) -> None:
        cancat_dict = {
            ChipToolhelpper.QueryCMDMapper.SET_BINDING: self.binding_passer,
            ChipToolhelpper.QueryCMDMapper.CREATE_GROUP: self.group_passer,
            ChipToolhelpper.QueryCMDMapper.CREATE_KEYSET: self.keyset_passer,
            ChipToolhelpper.QueryCMDMapper.BIND_GROUP_KEYSET: self.bind_group_keyset_passer,
            ChipToolhelpper.QueryCMDMapper.APPLY_KEYSET: self.apply_keyset_passer,
            ChipToolhelpper.QueryCMDMapper.APPLY_KEYSET_MAP: self.apply_keyset_map_passer,
            ChipToolhelpper.QueryCMDMapper.APPLY_GROUP: self.apply_group_passer,
        }
        return cancat_dict[context_type](contain=kwargs["contain"])

    def handle_command(self, context_type: ChipToolhelpper.QueryCMDMapper, *args, **kwargs) -> None:
        command = self.command_passer(context_type, contain=kwargs)
        status, result = self._CMDAccess.send_command(command)
        return status, result

    def set_binding(self, light_name, light_endpoint, switch_name, switch_endpoint):
        self._ChipToolMgr.clear_failed_data()
        light_node = self._ChipToolMgr.get_profile(light_name)
        switch_node = self._ChipToolMgr.get_profile(switch_name)
        self._ChipToolLightMgr.set_acl(
            light_node=light_node, switch_node=switch_node)

        binding_list = self._ChipToolMgr.get_binding(switch_node["name"])
        target_bind = {
            "name": switch_node["name"], "fabric": light_node['fabric'],
            "nodeid": switch_node["nodeid"], "endpoint": switch_endpoint,
            "target_name": light_node["name"], "target_id": light_node["nodeid"],
            "endpoint": light_endpoint,
        }
        if (target_bind not in binding_list):
            binding_list.append(target_bind)
        else:
            self._TyperExt.attach_log(
                'binding already in binding list', self._TyperExt.Colors.GREEN)

        status, result = self.handle_command(
            ChipToolhelpper.QueryCMDMapper.SET_BINDING,
            binding_list=self.binding_json_passer(binding_list),
            nodeid=switch_node["nodeid"], endpoint=switch_endpoint
        )
        if not (status == 0):
            self._TyperExt.raise_error(1, 'Failed: set switch binding failed')

        binding = self._ChipToolMgr.new_binding_profile(
            name=switch_node['name'], fabric=switch_node['fabric'],
            nodeid=switch_node['nodeid'], endpoint=switch_endpoint,
            target_name=light_node['name'], target_id=light_node['nodeid'],
            target_endpoint=light_endpoint
        )
        self._ChipToolMgr.apply_binding_profile(binding)
        self._TyperExt.attach_log('Success: Execute command',
                                  self._TyperExt.Colors.GREEN)

    def gen_group(self, group_name):
        self._ChipToolMgr.clear_failed_data()
        group = self._ChipToolMgr.new_group_profile(name=group_name)
        status, result = self.handle_command(
            ChipToolhelpper.QueryCMDMapper.CREATE_GROUP,
            name=group.name, group_id=group.group_id)
        if not (status == 0):
            self._TyperExt.raise_error(1, 'Failed: Create Group failed')

        status, result = self.handle_command(
            ChipToolhelpper.QueryCMDMapper.CREATE_KEYSET,
            group_keyset_id=group.group_keyset_id, groupKeySecurityPolicy=0,
            epochStartTime0=2220000, epochKey0=group.epochkey0
        )
        if not (status == 0):
            self._TyperExt.raise_error(1, 'Failed: Create GroupKeySet failed')

        status, result = self.handle_command(
            ChipToolhelpper.QueryCMDMapper.BIND_GROUP_KEYSET,
            group_id=group.group_id, group_keyset_id=group.group_keyset_id
        )
        if not (status == 0):
            self._TyperExt.raise_error(1, 'Failed: Bind Group-Keyset failed')

        self._TyperExt.attach_log(f"The group {str(group_name)} success created",
                                  self._TyperExt.Colors.GREEN)
        self._TyperExt.attach_log('Success: Execute command',
                                  self._TyperExt.Colors.GREEN)

    def add_group(self, group_name, target_type, target_name, target_endpoint):
        self._ChipToolMgr.clear_failed_data()
        target_type = target_type.upper()
        target_node = self._ChipToolMgr.get_profile(target_name)
        group = self._ChipToolMgr.get_group("name", group_name)

        group_mapper = self._ChipToolMgr.new_group_mapper_profile(
            name=group['name'], group_id=group['group_id'],
            target_id=target_node['nodeid'], target_name=target_name,
            target_type=target_type, target_endpoint=target_endpoint,
            status="Init"
        )
        group_mapper.status = "Panding"
        self._ChipToolMgr.update_group_profile(group_mapper)

        GKS = self.GroupKeySet(
            groupKeySetID=group['group_id'], groupKeySecurityPolicy=0,
            epochKey0=group['epochkey0'], epochStartTime0=2220000,
            epochKey1=group['epochkey1'], epochStartTime1=2220001,
            epochKey2=group['epochkey2'], epochStartTime2=2220002,
        )
        self._TyperExt.attach_log('Execute: APPLY_KEYSET',
                                  self._TyperExt.Colors.BRIGHT_CYAN)
        status, result = self.handle_command(
            ChipToolhelpper.QueryCMDMapper.APPLY_KEYSET,
            group_key_set=json.dumps(dataclasses.asdict(GKS)),
            target_nodeid=target_node['nodeid'], target_endpoint="0"
        )
        if not (status == 0):
            self._TyperExt.raise_error(1, 'Failed: APPLY_KEYSET failed')

        self._TyperExt.attach_log('Execute: APPLY_KEYSET_MAP',
                                  self._TyperExt.Colors.BRIGHT_CYAN)
        status, result = self.handle_command(
            ChipToolhelpper.QueryCMDMapper.APPLY_KEYSET_MAP,
            group_key_map_list=self.keyset_map_json_passer(
                target_node["nodeid"], target_node["fabric"]),
            target_nodeid=target_node["nodeid"], target_endpoint="0"
        )
        if not (status == 0):
            self._TyperExt.raise_error(1, 'Failed: APPLY_KEYSET_MAP failed')

        self._TyperExt.attach_log('Execute: APPLY_GROUP',
                                  self._TyperExt.Colors.BRIGHT_CYAN)
        status, result = self.handle_command(
            ChipToolhelpper.QueryCMDMapper.APPLY_GROUP,
            groupId=group['group_id'], group_name=group['name'],
            target_nodeid=target_node['nodeid'], target_endpoint=target_endpoint
        )
        if not (status == 0):
            self._TyperExt.raise_error(1, 'Failed: APPLY_GROUP failed')

        self._TyperExt.attach_log(target_type.upper(),
                                  self._TyperExt.Colors.BRIGHT_CYAN)
        if target_type == "LIGHT":
            self._TyperExt.attach_log('Execute: LIGHT ACL',
                                      self._TyperExt.Colors.BRIGHT_CYAN)
            group["nodeid"] = group['group_id']
            self._ChipToolLightMgr.set_group_acl(target_node, group)
        elif target_type == "SWITCH":
            self._TyperExt.attach_log('Execute: SWITCH Group binding',
                                      self._TyperExt.Colors.BRIGHT_CYAN)
            group_binding_list = self.group_binding_json_passer(
                target_node["nodeid"], group['group_id'])
            status, result = self.handle_command(
                ChipToolhelpper.QueryCMDMapper.SET_BINDING,
                binding_list=group_binding_list,
                nodeid=target_node["nodeid"], endpoint=target_endpoint
            )
            if not (status == 0):
                self._TyperExt.raise_error(
                    1, 'Failed: SWITCH srt binding failed')

        group_mapper.status = "Success"
        self._ChipToolMgr.update_group_profile(group_mapper)
        self._TyperExt.attach_log(f"The group {str(group_name)} success add",
                                  self._TyperExt.Colors.GREEN)
        self._TyperExt.attach_log('Success: Execute command',
                                  self._TyperExt.Colors.GREEN)


class ChipToolConnectMgr:
    def __init__(self) -> None:
        self._TyperExt = TyperExt()
        self._CMDAccess = CMDAccess()
        self._ChipToolMgr = ChipToolMgr()

    def command_passer(self, context_type, *args, **kwargs) -> None:
        if context_type == ChipToolhelpper.QueryCMDMapper.CONN_THREAD:
            return ChipToolhelpper.CMDList.CONNECT_THEAD.value + [
                str(kwargs["contain"]["nodeid"]),
                "hex:"+kwargs["contain"]["otbr_hex"],
                str(kwargs["contain"]["pincode"]),
                str(kwargs["contain"]["discriminator"]),
                "--ble-adapter",
                str(kwargs["contain"]["ble_adapter"])
            ]
        else:
            return

    def handle_command(self, context_type: ChipToolhelpper.CMDList, *args, **kwargs) -> None:
        kwargs["otbr_hex"] = self._ChipToolMgr.get_thread_network()
        command = self.command_passer(context_type, contain=kwargs)
        self._TyperExt.attach_log(str(json.dumps(command)),
                                  self._TyperExt.Colors.GREEN)
        status, result = self._CMDAccess.send_command(command)
        return status, result

    def connect(self, name, devicetype, pincode, discriminator, ble_adapter):
        self._ChipToolMgr.clear_failed_data()
        node = self._ChipToolMgr.new_node_profile(
            name=name, devicetype=devicetype)
        node.status = "Panding"
        self._ChipToolMgr.update_profile(node)
        status, result = self.handle_command(
            ChipToolhelpper.QueryCMDMapper.CONN_THREAD,
            nodeid=node.nodeid, pincode=pincode,
            discriminator=discriminator, ble_adapter=ble_adapter)
        if not (status == 0):
            self._TyperExt.raise_error(1, 'Failed: Connect failed')

        fabric_index = -1
        for row in result:
            match = re.search(r'FabricIndex (\d+)', row)
            if match:
                fabric_index = match.group(1)
                if (fabric_index):
                    # self._TyperExt.attach_log("FabricIndex " + str(fabric_index),
                    #                           self._TyperExt.Colors.BRIGHT_YELLOW)
                    break
        if (fabric_index == -1):
            self._TyperExt.raise_error(1, 'Failed: Connected Fabric not found')

        node.status = "Connected"
        node.fabric = fabric_index
        self._ChipToolMgr.update_profile(node)

        acl = self._ChipToolMgr.new_acl_profile(name=node.name, fabric=fabric_index,
                                                nodeid=node.nodeid, target_name="Admin",
                                                target_id=112233, privilege=5,
                                                auto_mode=2)
        self._ChipToolMgr.apply_acl_profile(acl=acl)

        self._TyperExt.attach_log("The node name: " + node.name +
                                  " already connnected",
                                  self._TyperExt.Colors.GREEN)
        self._TyperExt.attach_log('Success: Execute command',
                                  self._TyperExt.Colors.GREEN)
