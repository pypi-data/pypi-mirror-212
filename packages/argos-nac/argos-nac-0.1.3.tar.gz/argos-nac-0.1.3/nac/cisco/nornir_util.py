import logging
import re
from pathlib import Path
from re import Pattern
from typing import Dict, List

from nornir.core.inventory import Host
from nornir.core.task import MultiResult, Task
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.tasks.files import write_file

from nac.util.common import BaseNornirUtil

LOGGER = logging.getLogger(__name__)


class CiscoNornirUtil(BaseNornirUtil):
    _config_map: Dict[Host, str] = {}
    _facts_map: Dict[Host, Dict[str, str]] = {}

    @staticmethod
    def get_device_config(task: Task) -> str:
        config = CiscoNornirUtil._config_map.get(task.host, None)
        if config is None:
            # Get current config
            result = task.run(task=napalm_get, getters=["config"])
            result.raise_on_error()
            config = result.result["config"]["running"]
            CiscoNornirUtil._config_map.setdefault(task.host, config)
        return config

    @staticmethod
    def get_device_facts(task: Task) -> Dict[str, str]:
        facts: Dict[str, str] = CiscoNornirUtil._facts_map.get(task.host, None)  # type: ignore
        if facts is None:
            result: MultiResult = task.run(task=napalm_get, getters=["facts"])
            result.raise_on_error()
            facts = result.result["facts"]
            CiscoNornirUtil._facts_map.setdefault(task.host, facts)
        return facts

    @staticmethod
    def backup_config(task: Task, path: str | Path) -> MultiResult:
        LOGGER.info(f'Taking backup of {task.host.name}')
        config = CiscoNornirUtil.get_device_config(task)

        Path(path).mkdir(parents=True, exist_ok=True)

        return task.run(task=write_file, content=config, filename=f"{path}/{task.host.name}.log")

    @staticmethod
    def _filter_config(task: Task, pattern: Pattern) -> List[str]:
        config = CiscoNornirUtil.get_device_config(task)
        return BaseNornirUtil._filter_for_line(config, pattern)

    @staticmethod
    def get_configured_vrf_names(task: Task) -> List[str]:
        return CiscoNornirUtil._filter_config(task, re.compile(pattern=r"^vrf definition (.+)"))

    @staticmethod
    def get_configured_bgp_asns(task: Task) -> List[str]:
        return CiscoNornirUtil._filter_config(task, re.compile(pattern=r"^router bgp (\d+)"))

    @staticmethod
    def fetch_platform(task: Task) -> str:
        facts: Dict[str, str] = CiscoNornirUtil.get_device_facts(task)
        vendor: str = facts["vendor"]
        vendor_map = {
            "cisco": "ios",
            "juniper": "junos",
            "palo_alto_networks": "panos",
        }
        return vendor_map[vendor.lower()]
