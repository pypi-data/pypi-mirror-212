from pathlib import Path
from typing import Iterable
from nornir.core import Nornir
from nornir.core.inventory import Defaults
from nornir.core.task import Task, MultiResult, AggregatedResult
from nornir_napalm.plugins.tasks import napalm_configure

from nac.cisco.protocols import BGPUtil, LDPUtil, VRFUtil
from nac.util.common import BaseNAC, HostMapping, InterfaceConfig

from ..model import *
from .nornir_util import CiscoNornirUtil

LOGGER = getLogger(__name__)


class CiscoNAC(BaseNAC):
    def __init__(self, host_mapping: HostMapping, defaults: Defaults, dry_run: bool) -> None:
        self.defaults = defaults
        self.host_mapping = host_mapping
        self.dry_run = dry_run

    def configure_devices(self, backup_dir: Path | None = None, output_dir: Path | None = None) -> AggregatedResult:
        LOGGER.info(f"Beginning device conifiguration run. Dry run: {self.dry_run}")
        nr: Nornir = CiscoNornirUtil.nornir_setup(hosts=self.host_mapping.get_hosts(), defaults=self.defaults)
        return self._configure_devices(
            nr=nr,
            mapping=self.host_mapping,
            backup_dir=backup_dir,
            output_dir=output_dir,
            dry_run=self.dry_run,
        )

    @staticmethod
    def _configure_device(
        task: Task, mapping: HostMapping, backup_dir: Path | None, output_dir: Path | None, dry_run: bool
    ) -> MultiResult:
        host = task.host
        device = mapping[host]
        host.platform = CiscoNornirUtil.fetch_platform(task)

        if backup_dir:
            result = CiscoNornirUtil.backup_config(task, path=backup_dir)
            result.raise_on_error()

        config = "\n".join(CiscoNAC.generate_config(task=task, device=device))

        if output_dir is not None:
            with open(output_dir / f'{host.name}.conf', 'w+') as f:
                f.write(config)

        # Apply config
        result: MultiResult = task.run(
            napalm_configure,
            dry_run=dry_run,
            replace=False,
            configuration=config,
        )
        return result

    @staticmethod
    def generate_config(task: Task, device: Device) -> List[str]:
        """Generate the commands necessary to set the device into the desired state."""
        # Gather config

        interface_config: InterfaceConfig = InterfaceConfig()

        config: List[str] = []
        config += VRFUtil.generate_config(task, device=device, interface_config=interface_config)
        config += LDPUtil.generate_config(task, device=device, interface_config=interface_config)
        config += BGPUtil.generate_config(task, device=device)

        config += CiscoNAC.generate_interface_config(
            interfaces=device.interfaces,
            interface_config=interface_config,
        )

        return config

    @staticmethod
    def generate_interface_config(interfaces: Iterable[Interface], interface_config: InterfaceConfig) -> List[str]:
        """Generate collected interface config.

        Note: IP address needs to be added after everything else due to VRF changes leading to "no ip address" being added by the router.
        """
        config: List[str] = []
        for i in interfaces:
            if i.name in interface_config.keys():
                config += [f"interface {i.name}"]
                config += interface_config[i.name]
                if i.ip_addresses is not None:
                    for ip in i.ip_addresses:
                        config += [f' ip address {ip.address.ip.exploded} {ip.address.netmask.exploded}']
        return config
