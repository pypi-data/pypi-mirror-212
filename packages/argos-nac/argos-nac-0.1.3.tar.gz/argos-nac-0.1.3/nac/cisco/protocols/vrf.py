from logging import getLogger
from typing import Iterable, Set

from nornir.core.task import Task

from nac.util.common import InterfaceConfig, Util

from ...model import *
from ..nornir_util import CiscoNornirUtil

LOGGER = getLogger(__name__)


class VRFUtil(Util):
    @staticmethod
    def generate_remove_config(task: Task, known_vrfs: Iterable[VRF]) -> List[str]:
        """Generate commands to purge all unknown vrfs from the device."""
        installed_vrfs: List[str] = CiscoNornirUtil.get_configured_vrf_names(task)
        known_vrf_names: List[str] = [vrf.name for vrf in known_vrfs]
        commands: List[str] = []

        for vrf in installed_vrfs:
            if vrf not in known_vrf_names:
                commands += [f"no vrf definition {vrf}"]
        LOGGER.debug(f"Found {len(commands)} vrfs to remove.")
        return commands

    @staticmethod
    def generate_config(task: Task, device: Device, interface_config: InterfaceConfig) -> List[str]:
        # Get known vrfs
        vrfs: Set[VRF] = set()
        config: List[str] = []
        for interface in device.interfaces:
            if interface.vrf is not None:
                vrfs.add(interface.vrf)

        # Remove unknown vrfs
        config += VRFUtil.generate_remove_config(task, known_vrfs=vrfs)

        # Set up VRFs
        for vrf in vrfs:
            # Define new VRF
            config.append(f"vrf definition {vrf.name}")

            if vrf.rd is not None:
                config.append(f" rd {vrf.rd}")

            config += [f" route-target export {t.name}" for t in vrf.export_targets]
            config += [f" route-target import {t.name}" for t in vrf.import_targets]

            # TODO: Source the following settings through netbox somehow
            config += [
                " address-family ipv4",
                " exit-address-family",
                " address-family ipv6",
                " exit-address-family",
            ]

        # Associate interface
        for interface in device.interfaces:
            interface_config.setdefault(interface.name, [])
            if interface.vrf is not None:
                interface_config[interface.name] += [f" vrf forwarding {interface.vrf.name}"]
            else:
                interface_config[interface.name] += [f" no vrf forwarding"]

        return config
