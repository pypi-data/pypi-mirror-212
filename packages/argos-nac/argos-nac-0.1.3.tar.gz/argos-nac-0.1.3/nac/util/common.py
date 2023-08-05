from abc import ABC, abstractmethod
from logging import getLogger
from pathlib import Path
from re import Pattern
from typing import List

from nornir.core import Nornir
from nornir.core.inventory import Defaults, Host, Hosts, Inventory
from nornir.core.task import AggregatedResult, Task

from nac.model import Device, Site

LOGGER = getLogger(__name__)


class HostMapping(dict[Host, Device]):
    @staticmethod
    def from_site(site: Site, nornir_defaults: Defaults = Defaults()) -> 'HostMapping':
        mapping = HostMapping()
        for device in site.devices:
            management_interface = device.get_management_interface()
            if management_interface is not None:
                name = device.name if device.name else f"_device_{device.id}"
                host = Host(
                    name=name,
                    hostname=management_interface.ip_addresses[0].address.ip.exploded,  # type: ignore
                    defaults=nornir_defaults,
                )
                mapping[host] = device
            else:
                LOGGER.warning(
                    f'Device (id: {device.id}, name: "{device.name}") does not have a valid "Management Only" interface with associated IP address. Skipping its configuration.'
                )
        return mapping

    def get_hosts(self) -> Hosts:
        hosts = dict()
        for host in self.keys():
            hosts[host.name] = host
        return Hosts(hosts)


class InterfaceConfig(dict[str, list[str]]):
    '''Interface specific configs.'''


class Util(ABC):
    @staticmethod
    @abstractmethod
    def generate_config(task: Task, device: Device) -> List[str]:
        """Generate commands to achieve the desired device state for this protocol."""


class BaseNornirUtil:
    __registered: bool = False

    @staticmethod
    def __register_napalm_plugin() -> None:
        if not BaseNornirUtil.__registered:
            from nornir.core.plugins.connections import ConnectionPluginRegister
            from nornir_napalm.plugins.connections import CONNECTION_NAME, Napalm

            ConnectionPluginRegister.register(name=CONNECTION_NAME, plugin=Napalm)

    @staticmethod
    def nornir_setup(hosts: Hosts, defaults: Defaults = Defaults()) -> Nornir:
        from nornir.plugins.runners import SerialRunner

        BaseNornirUtil.__register_napalm_plugin()

        inv = Inventory(hosts=hosts, defaults=defaults)
        nornir = Nornir(inventory=inv, runner=SerialRunner())  # type: ignore
        return nornir

    @staticmethod
    def _filter_for_line(string: str, pattern: Pattern) -> List[str]:
        matches: List[str] = []
        for line in string.splitlines():
            match = pattern.match(line)
            if match is not None:
                matches.append(*match.groups())
        return matches


class BaseNAC(ABC):
    @staticmethod
    @abstractmethod
    def _configure_device(
        task: Task,
        mapping: HostMapping,
        backup_dir: Path | None,
        output_dir: Path | None,
        **kvargs,
    ) -> AggregatedResult:
        """Generate the commands necessary to set the device into the desired state.

        This function is called automatically for every host."""

    @staticmethod
    @abstractmethod
    def generate_config(task: Task, device: Device) -> List[str]:
        """Generate the commands necessary to set the device into the desired state."""

    def _configure_devices(
        self,
        *,
        nr: Nornir,
        **kvargs,
    ) -> AggregatedResult:
        '''Calls `_configure_device` for each host with the provide kvargs.'''
        try:
            # For each device, configure it
            return nr.run(task=self._configure_device, **kvargs)
        finally:
            nr.close_connections()
