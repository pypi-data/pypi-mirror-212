"""This module provides the RP To-Do database functionality."""
# rptodo/database.py

import configparser
import json
import dataclasses
from pathlib import Path
from typing import Any, Dict, List, NamedTuple
from ...error import DB_WRITE_ERROR, SUCCESS
from ...extlib.TyperExt.TyperExt import TyperExt

DEFAULT_DB_FILE_PATH = Path.home().joinpath(
    "." + Path.home().stem + "_EZMash.json"
)


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


class DBResponse(NamedTuple):
    todo_list: List[Dict[str, Any]]
    error: int


class DatabaseHandler:
    def __init__(self, db_path: Path = DEFAULT_DB_FILE_PATH) -> None:
        self._db_path = db_path
        self._TyperExt = TyperExt()

    def init_database(self):
        """Create the to-do database."""
        empty_data = {}
        with self._db_path.open("w") as db:
            db.write(json.dumps(empty_data))  # Empty to-do list

    def check_exist_or_create(self, obj, key, content):
        if key not in obj:
            obj[key] = content
        return obj

    def read_matter_cluster(self, group, cluster):
        profile = {}
        try:
            with self._db_path.open("r") as db:
                profile = json.load(db)
        except FileNotFoundError:
            self.init_database()
        # self._TyperExt.attach_log("======= read_matter_cluster =======",
        #                           self._TyperExt.Colors.WHITE)
        # self._TyperExt.attach_log(json.dumps(profile),
        #                           self._TyperExt.Colors.GREEN)
        self.check_exist_or_create(profile, group, {})
        self.check_exist_or_create(profile[group], cluster, [])
        return profile

    def read_matter_config_cluster(self):
        profile = {}
        try:
            with self._db_path.open("r") as db:
                profile = json.load(db)
        except FileNotFoundError:
            self.init_database()
        # self._TyperExt.attach_log("======= read_matter_config_cluster =======",
        #                           self._TyperExt.Colors.WHITE)
        # self._TyperExt.attach_log(json.dumps(profile),
        #                           self._TyperExt.Colors.GREEN)
        group = "matter"
        cluster = "config"
        content = {"max_nodeid": 0, "max_groupid": 0}
        self.check_exist_or_create(profile, group, {})
        self.check_exist_or_create(profile[group], cluster, content)
        return profile

    def read_single_matter_cluster(self, group, cluster, key, target_name):
        target_node = {}
        profile = self.read_matter_cluster(group, cluster)
        for node in profile[group][cluster]:
            if not node[key] == target_name:
                continue
            target_node = node
            break
        return target_node

    def read_match_matter_cluster(self, group, cluster, key, target_name):
        target_list = []
        profile = self.read_matter_cluster(group, cluster)
        for node in profile[group][cluster]:
            if not node[key] == target_name:
                continue
            target_list.append(node)
            break
        return target_list

    def write_matter_profile(self, group, cluster, data) -> DBResponse:
        profile = self.read_matter_cluster(group, cluster)
        if (dataclasses.asdict(data) not in profile[group][cluster]):
            profile[group][cluster].append(dataclasses.asdict(data))
            with self._db_path.open("w") as db:
                db.write(json.dumps(profile))
        self.read_matter_cluster(group, cluster)  # for testing
        return DBResponse(profile, SUCCESS)

    def modify_matter_profile(self, group, cluster, key, data) -> DBResponse:
        profile = self.read_matter_cluster(group, cluster)
        data = dataclasses.asdict(data)
        # self._TyperExt.attach_log(json.dumps(
        #     (group, cluster)), self._TyperExt.Colors.BRIGHT_MAGENTA)
        # self._TyperExt.attach_log(json.dumps(
        #     data), self._TyperExt.Colors.BRIGHT_MAGENTA)
        for idx in range(0, len(profile[group][cluster])):
            if (profile[group][cluster][idx][key] == data[key]):
                profile[group][cluster][idx] = data
                with self._db_path.open("w") as db:
                    db.write(json.dumps(profile))
                self.read_matter_cluster(group, cluster)  # for testing
                return DBResponse(profile, SUCCESS)
        return DBResponse(profile, DB_WRITE_ERROR)

    def update_matter_profile(self, group, cluster, data) -> DBResponse:
        profile = self.read_matter_cluster(group, cluster)
        profile[group][cluster] = data
        with self._db_path.open("w") as db:
            db.write(json.dumps(profile))
        self.read_matter_cluster(group, cluster)  # for testing
        return DBResponse(profile, SUCCESS)

    def write_matter_config_profile(self, config):
        profile = self.read_matter_config_cluster()
        profile['matter']['config'] = config
        with self._db_path.open("w") as db:
            db.write(json.dumps(profile))
        self.read_matter_config_cluster()  # for testing
        return DBResponse(profile, SUCCESS)


def get_database_path(config_file: Path) -> Path:
    """Return the current path to the to-do database."""
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["database"])


def init_database(db_path: Path) -> int:
    """Create the to-do database."""
    try:
        db_path.write_text("[]")  # Empty to-do list
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR
