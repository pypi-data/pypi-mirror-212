from enum import Enum


class CMDList(Enum):
    LIGHT_ONOFF = ['chip-tool', 'onoff']
    LEVEL_CTL = ['chip-tool', 'levelcontrol', 'move-to-level-with-on-off']
    CONNECT_THEAD = ['chip-tool', 'pairing', 'ble-thread']
    SET_ACL = ['chip-tool', 'accesscontrol', 'write', 'acl']
    WRITE_BINDING = ['chip-tool', 'binding', 'write', 'binding']
    CREATE_GROUP = ['chip-tool', 'groupsettings', 'add-group']
    CREATE_KEYSET = ['chip-tool', 'groupsettings', 'add-keysets']
    BIND_GROUP_KEYSET = ['chip-tool', 'groupsettings', 'bind-keyset']
    APPLY_KEYSET = ['chip-tool', 'groupkeymanagement', 'key-set-write']
    APPLY_KEYSET_MAP = ['chip-tool',
                        'groupkeymanagement', 'write', 'group-key-map']
    APPLY_GROUP = ['chip-tool', 'groups', 'add-group']
    CHECK_COMMAND_SUCCESS = 'echo $?'


class QueryCMDMapper(Enum):
    LIGHT_ONOFF = CMDList.LIGHT_ONOFF.name
    LEVEL_CONTROL = CMDList.LEVEL_CTL.name
    CONN_THREAD = CMDList.CONNECT_THEAD.name
    ACCESS_CONTROL = CMDList.SET_ACL.name
    SET_BINDING = CMDList.WRITE_BINDING.name
    CREATE_GROUP = CMDList.CREATE_GROUP.name
    CREATE_KEYSET = CMDList.CREATE_KEYSET.name
    BIND_GROUP_KEYSET = CMDList.BIND_GROUP_KEYSET.name
    APPLY_KEYSET = CMDList.APPLY_KEYSET.name
    APPLY_KEYSET_MAP = CMDList.APPLY_KEYSET_MAP.name
    APPLY_GROUP = CMDList.APPLY_GROUP.name

    CHECK_STATE = CMDList.CHECK_COMMAND_SUCCESS.name


def check_query_exists(query: str):
    return True if any(x for x in QueryCMDMapper if x.name == query) else False


def check_command_exists(query: str):
    return True if any(x for x in CMDList if x.name == query) else False


def get_query_prefix(query: str):
    return CMDList[QueryCMDMapper[query].value].value
