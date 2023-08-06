from pathlib import Path
from ...error import DB_WRITE_ERROR
from .Database import DatabaseHandler
from ...extlib.TyperExt.TyperExt import TyperExt
from dataclasses import dataclass

from .Database import DEFAULT_DB_FILE_PATH
import json
import secrets
from enum import Enum


class MatterDM:
    @dataclass
    class MatterNode():
        nodeid: int
        name: str
        devicetype: str
        status: str
        fabric: int

    @dataclass
    class MatterACL():
        name: str
        fabric: int
        nodeid: int
        target_name: str
        target_id: int
        privilege: int
        auto_mode: int

    @dataclass
    class MatterBinding():
        name: str
        fabric: int
        nodeid: int
        target_name: str
        target_id: int
        endpoint: int

    @dataclass
    class MatterGroup():
        name: str
        group_id: int
        group_keyset_id: int
        epochkey0: str
        epochkey1: str
        epochkey2: str

    @dataclass
    class MatterGroupMapper():
        name: str
        group_id: int
        target_id: int
        target_name: str
        target_type: str
        target_endpoint: int
        status: str

    class RecordState(Enum):
        INIT = 0
        PANDING = 1
        RUNNING = 2
        SUCCESS = 3
        FAILED = 4

    class DeviceType(Enum):
        UNKNOW = 0
        LIGHT = 1
        SWITCH = 2

    def __init__(self, db_path: Path = DEFAULT_DB_FILE_PATH) -> None:
        self._db = DatabaseHandler(db_path)
        self._TyperExt = TyperExt()
        self.nodeid_list = []
        self.name_list = []
        self.groupid_list = []
        self.group_name_list = []
        self.group_keyset_id = []

    def check_node_name_exist(self, name):
        return True if any(x for x in self.name_list if x == name) else False

    def check_group_mapper_name_exist(self, name):
        return True if any(x for x in self.group_name_list if x == name) else False

    def generate_nodeid(self):
        profile = self._db.read_matter_config_cluster()
        profile["matter"]["config"]["max_nodeid"] += 1
        id = profile["matter"]["config"]["max_nodeid"]
        self._db.write_matter_config_profile(profile["matter"]["config"])
        return id

    def generate_groupid(self):
        profile = self._db.read_matter_config_cluster()
        profile["matter"]["config"]["max_groupid"] += 1
        id = profile["matter"]["config"]["max_groupid"]
        self._db.write_matter_config_profile(profile["matter"]["config"])
        return id

    def generate_group_keyset_id(self):
        id = -1
        for idx in range(1, 10001):
            if idx not in self.group_keyset_id:
                id = idx
                break
        return id

    def update_check_list(self):
        # self._TyperExt.attach_log(
        #     "+++ node +++", self._TyperExt.Colors.BRIGHT_MAGENTA)  # for test
        self.nodeid_list = []
        self.name_list = []
        for group, cluster in [("matter", "node"), ("matter", "failed_node")]:
            read = self._db.read_matter_cluster(group, cluster)
            nodelist = read[group][cluster]
            for idx in range(0, len(nodelist)):
                # self._TyperExt.attach_log(json.dumps(
                #     nodelist[idx]), self._TyperExt.Colors.BRIGHT_MAGENTA)  # for test
                self.nodeid_list.append(nodelist[idx]["nodeid"])
                self.name_list.append(nodelist[idx]["name"])

        # self._TyperExt.attach_log(
        #     "+++ group +++", self._TyperExt.Colors.BRIGHT_MAGENTA)  # for test
        self.groupid_list = []
        self.group_name_list = []
        self.group_keyset_id = []
        for group, cluster in [("matter", "group")]:
            read = self._db.read_matter_cluster(group, cluster)
            nodelist = read[group][cluster]
            for idx in range(0, len(nodelist)):
                # self._TyperExt.attach_log(json.dumps(
                #     nodelist[idx]), self._TyperExt.Colors.BRIGHT_MAGENTA)  # for test
                self.groupid_list.append(nodelist[idx]["group_id"])
                self.group_name_list.append(nodelist[idx]["name"])
                self.group_keyset_id.append(nodelist[idx]["group_keyset_id"])

    def add_node(self, node: MatterNode):
        read = self._db.write_matter_profile("matter", "node", node)
        if read.error == DB_WRITE_ERROR:
            self._TyperExt.raise_error(1, 'Failed: DB_WRITE_ERROR')
            return read.error

    def add_acl(self, acl: MatterACL):
        read = self._db.write_matter_profile("matter", "acl", acl)
        if read.error == DB_WRITE_ERROR:
            self._TyperExt.raise_error(1, 'Failed: DB_WRITE_ERROR')
            return read.error

    def add_binding(self, binding: MatterBinding):
        read = self._db.write_matter_profile("matter", "binding", binding)
        if read.error == DB_WRITE_ERROR:
            self._TyperExt.raise_error(1, 'Failed: DB_WRITE_ERROR')
            return read.error

    def add_group(self, group: MatterGroup):
        read = self._db.write_matter_profile("matter", "group", group)
        if read.error == DB_WRITE_ERROR:
            self._TyperExt.raise_error(1, 'Failed: DB_WRITE_ERROR')
            return read.error

    def add_group_mapper(self, group_mapper: MatterGroupMapper):
        read = self._db.write_matter_profile(
            "matter", "group_mapper", group_mapper)
        if read.error == DB_WRITE_ERROR:
            self._TyperExt.raise_error(1, 'Failed: DB_WRITE_ERROR')
            return read.error

    def update_node(self, node: MatterNode):
        self.check_node_vailed(node)
        read = self._db.modify_matter_profile("matter", "node", "nodeid", node)
        if read.error == DB_WRITE_ERROR:
            self._TyperExt.raise_error(1, 'Failed: DB_WRITE_ERROR')
            return read.error

    def update_group_mapper(self, group_mapper: MatterGroupMapper):
        self.check_group_mapper_vailed(group_mapper)
        read = self._db.modify_matter_profile(
            "matter", "group_mapper", "group_id", group_mapper)
        if read.error == DB_WRITE_ERROR:
            self._TyperExt.raise_error(1, 'Failed: DB_WRITE_ERROR')
            return read.error

    def check_node_vailed(self, node: MatterNode):
        self.update_check_list()
        if node.nodeid == -1:
            self._TyperExt.raise_error(1, 'Failed: Invailed nodeid')
        status = self.check_node_name_exist(node.name)
        if not (status == 1):
            self._TyperExt.raise_error(1, 'Failed: Invailed device name')
        # self._TyperExt.attach_log(
        #     "node are vailed", self._TyperExt.Colors.GREEN)

    def check_group_mapper_vailed(self, group_mapper: MatterGroupMapper):
        self.update_check_list()
        if group_mapper.group_id == -1:
            self._TyperExt.raise_error(1, 'Failed: Invailed group_id')
        status = self.check_group_mapper_name_exist(group_mapper.name)
        if not (status == 1):
            self._TyperExt.raise_error(1, 'Failed: Invailed group name')
        # self._TyperExt.attach_log(
        #     "group are vailed", self._TyperExt.Colors.GREEN)

    def create_node(self, *args, **kwargs):
        node = self.MatterNode(
            name=kwargs['name'], devicetype=kwargs["devicetype"],
            nodeid=-1, status="Init", fabric=-1
        )
        self.update_check_list()
        status = self.check_node_name_exist(node.name)
        if status == 1:
            self._TyperExt.raise_error(1, 'Failed: Invailed device name')
        node.nodeid = self.generate_nodeid()
        if node.nodeid == -1:
            self._TyperExt.raise_error(1, 'Failed: Invailed nodeid')
        return node

    def create_acl(self, *args, **kwargs):
        acl = self.MatterACL(
            name=kwargs['name'], fabric=kwargs['fabric'], nodeid=kwargs['nodeid'],
            target_name=kwargs['target_name'], target_id=kwargs['target_id'],
            privilege=kwargs['privilege'], auto_mode=kwargs['auto_mode']
        )
        return acl

    def create_binding(self, *args, **kwargs):
        binding = self.MatterBinding(
            name=kwargs['name'], fabric=kwargs['fabric'], nodeid=kwargs['nodeid'],
            target_name=kwargs['target_name'], target_id=kwargs['target_id'],
            endpoint=kwargs['endpoint']
        )
        return binding

    def create_group(self, *args, **kwargs):
        group = self.MatterGroup(
            name=kwargs['name'], group_id=-1, group_keyset_id=-1,
            epochkey0=secrets.token_bytes(16).hex(),
            epochkey1=secrets.token_bytes(16).hex(),
            epochkey2=secrets.token_bytes(16).hex(),
        )
        self.update_check_list()
        status = self.check_node_name_exist(group.name)
        if status == 1:
            self._TyperExt.raise_error(1, 'Failed: Invailed group name')

        group.group_id = self.generate_groupid()
        if group.group_id == -1:
            self._TyperExt.raise_error(1, 'Failed: generate groupid failed')

        group.group_keyset_id = self.generate_group_keyset_id()
        if group.group_keyset_id == -1:
            self._TyperExt.raise_error(
                1, 'Failed: generate group_keyset_id failed')
        return group

    def create_group_mapper(self, *args, **kwargs):
        group_mapper = self.MatterGroupMapper(
            name=kwargs['name'], group_id=kwargs['group_id'],
            target_id=kwargs['target_id'], target_name=kwargs['target_name'],
            target_type=kwargs['target_type'], target_endpoint=kwargs['target_endpoint'],
            status=kwargs['status']
        )
        return group_mapper

    def get_fully_group_list(self):
        read = self._db.read_matter_cluster("matter", "group")
        # self._TyperExt.attach_log(json.dumps(
        #     group_list), self._TyperExt.Colors.GREEN)
        return read

    def get_group_list(self, key, data):
        read = self._db.read_matter_cluster("matter", "group")
        group_list = []
        for node in read["matter"]["group"]:
            if node[key] == data:
                group_list.append(node)
        # self._TyperExt.attach_log(json.dumps(
        #     group_list), self._TyperExt.Colors.GREEN)
        return group_list

    def get_fully_acl_list(self):
        read = self._db.read_matter_cluster("matter", "acl")
        # self._TyperExt.attach_log(json.dumps(
        #     acl_list), self._TyperExt.Colors.GREEN)
        return read

    def get_acl_list(self, key, data):
        read = self._db.read_matter_cluster("matter", "acl")
        acl_list = []
        for node in read["matter"]["acl"]:
            if node[key] == data:
                acl_list.append(node)
        # self._TyperExt.attach_log(json.dumps(
        #     acl_list), self._TyperExt.Colors.GREEN)
        return acl_list

    def get_node_list(self):
        read = self._db.read_matter_cluster("matter", "node")
        # self._TyperExt.attach_log(json.dumps(
        #     read), self._TyperExt.Colors.GREEN)
        return read

    def get_fully_binding_list(self):
        read = self._db.read_matter_cluster("matter", "binding")
        # self._TyperExt.attach_log(json.dumps(
        #     acl_list), self._TyperExt.Colors.GREEN)
        return read

    def get_binding_list(self, key, data):
        read = self._db.read_matter_cluster("matter", "binding")
        acl_list = []
        for node in read["matter"]["binding"]:
            if node[key] == data:
                acl_list.append(node)
        # self._TyperExt.attach_log(json.dumps(
        #     acl_list), self._TyperExt.Colors.GREEN)
        return acl_list

    def get_fully_group_mapper_list(self):
        read = self._db.read_matter_cluster("matter", "group_mapper")
        # self._TyperExt.attach_log(json.dumps(
        #     acl_list), self._TyperExt.Colors.GREEN)
        return read

    def get_group_mapper_list(self, key, data):
        read = self._db.read_matter_cluster("matter", "group_mapper")
        acl_list = []
        for node in read["matter"]["group_mapper"]:
            if node[key] == data:
                acl_list.append(node)
        # self._TyperExt.attach_log(json.dumps(
        #     acl_list), self._TyperExt.Colors.GREEN)
        return acl_list

    def get_match_group_list(self, key, data):
        group = self._db.read_match_matter_cluster(
            "matter", "group", key, data)
        if not group:
            self._TyperExt.raise_error(1, 'Failed: group name not found')
        # self._TyperExt.attach_log(
        #     "Access group success", self._TyperExt.Colors.GREEN)
        # self._TyperExt.attach_log(json.dumps(
        #     group), self._TyperExt.Colors.GREEN)
        return group

    def get_group(self, key, data):
        group = self._db.read_single_matter_cluster(
            "matter", "group", key, data)
        if not group:
            self._TyperExt.raise_error(1, 'Failed: group name not found')
        # self._TyperExt.attach_log(
        #     "Access group success", self._TyperExt.Colors.GREEN)
        # self._TyperExt.attach_log(json.dumps(
        #     group), self._TyperExt.Colors.GREEN)
        return group

    def get_node(self, key, data):
        node = self._db.read_single_matter_cluster(
            "matter", "node", key, data)
        if not node:
            self._TyperExt.raise_error(1, 'Failed: node name not found')
        # self._TyperExt.attach_log(
        #     "Access node success", self._TyperExt.Colors.GREEN)
        # self._TyperExt.attach_log(json.dumps(
        #     node), self._TyperExt.Colors.GREEN)
        return node

    def clear_failed_node(self):
        read = self._db.read_matter_cluster("matter", "node")
        # self._TyperExt.attach_log(json.dumps(
        #     read), self._TyperExt.Colors.GREEN)
        remove_list = []
        for idx in range(len(read["matter"]["node"])):
            if (not read["matter"]["node"][idx]['status'] == "Connected"):
                remove_list.append(idx)
        for ele in sorted(remove_list, reverse=True):
            del read["matter"]["node"][ele]
        self._db.update_matter_profile(
            "matter", "node", read["matter"]["node"])
        return read

    def clear_failed_group_mapper(self):
        read = self._db.read_matter_cluster("matter", "group_mapper")
        # self._TyperExt.attach_log(json.dumps(
        #     read), self._TyperExt.Colors.GREEN)
        remove_list = []
        for idx in range(len(read["matter"]["group_mapper"])):
            if (not read["matter"]["group_mapper"][idx]['status'] == "Success"):
                remove_list.append(idx)
        for ele in sorted(remove_list, reverse=True):
            del read["matter"]["group_mapper"][ele]
        self._db.update_matter_profile(
            "matter", "group_mapper", read["matter"]["group_mapper"])
        return read
