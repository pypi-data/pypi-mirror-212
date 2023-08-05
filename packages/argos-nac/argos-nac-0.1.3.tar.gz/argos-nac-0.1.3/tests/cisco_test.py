import json
from pathlib import Path

from nornir.core.inventory import Defaults
from nornir.core.task import Task
from pytest import MonkeyPatch

from nac.cisco import CiscoNAC, CiscoNornirUtil
from nac.model import *
from nac.util.common import HostMapping
from nac.util.graphql_util import GraphQLUtil

with open(Path(__file__).parent / "site_sample_data.json") as f:
    data = json.load(f)["data"]
    site: Site = GraphQLUtil._parse_query_data(data, site_id=1)
    mapping: HostMapping = HostMapping.from_site(site)


def get_device_config(task: Task):
    with open(Path(__file__).parent / "configs" / f"{task.host.name}.log") as f:
        return f.read()


def get_expected_config(task: Task) -> List[str]:
    with open(Path(__file__).parent / "configs" / f"{task.host.name}_expected.log") as f:
        return [s for s in f.read().split("\n") if s != "" and not s.startswith('!')]


def test_vrf_config_generation(monkeypatch: MonkeyPatch):
    ran_to_completion = 0

    def test(task: Task, mapping: HostMapping, **kvargs):
        nonlocal ran_to_completion
        monkeypatch.setitem(CiscoNornirUtil._config_map, task.host, get_device_config(task))
        device: Device = mapping[task.host]
        config: List[str] = CiscoNAC.generate_config(task=task, device=device)
        expected = get_expected_config(task)

        # Compare against expected config, disregarding order
        # TODO: is instantiation order not deterministic or why can the order change run to run?
        sorted_config = config.copy()
        sorted_config.sort()
        sorted_expected = expected.copy()
        sorted_expected.sort()
        for cmd, exp in zip(sorted_config, sorted_expected, strict=True):
            if not cmd == exp:
                print("\n")
                print(f"{'#'*20} EXPECTED {'#'*20}")
                print("\n".join(expected))
                print(f"{'#'*20} GOT {'#'*20}")
                print("\n".join(config))
                assert cmd == exp
        ran_to_completion += 1

    nac = CiscoNAC(host_mapping=mapping, defaults=Defaults(), dry_run=True)
    monkeypatch.setattr(nac, "_configure_device", test)
    nac.configure_devices()
    assert ran_to_completion == len(mapping), "One or more configuration dryruns failed to execute fully."
