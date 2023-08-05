from logging import getLogger

from nornir.core.task import Task

from nac.util.common import InterfaceConfig, Util

from ...model import *
from ..nornir_util import CiscoNornirUtil

LOGGER = getLogger(__name__)


class LDPUtil(Util):
    @staticmethod
    def generate_remove_config(task: Task) -> List[str]:
        """Generate commands to purge previously set config from the device."""
        return ["no mpls label range"]

    @staticmethod
    def generate_config(task: Task, device: Device, interface_config: InterfaceConfig) -> List[str]:
        if device.ldp is None:
            return LDPUtil.generate_remove_config(task)
        else:
            ret = []
            if device.ldp.auto_range:
                ret += ["no mpls label range"]  # removes any hard-coded ranges, resulting in auto-range
            else:
                if device.ldp.label_start is None or device.ldp.label_end is None:
                    raise Exception(
                        f"Expected a range to be provided. Got: [{device.ldp.label_start};{device.ldp.label_end}]"
                    )
                ret += [f"mpls label range {device.ldp.label_start} {device.ldp.label_end}"]
            ret += LDPUtil.generate_enable_mpls_on_interface_config(device, interface_config)
            return ret

    @staticmethod
    def generate_enable_mpls_on_interface_config(
        device: Device,
        interface_config: InterfaceConfig,
    ) -> List[str]:
        ret: List[str] = []
        if device.ldp is not None:
            for interface in device.interfaces:
                interface_config.setdefault(interface.name, [])
                if interface in device.ldp.ldp_enabled_interfaces:
                    interface_config[interface.name] += [" mpls ip"]
                else:
                    interface_config[interface.name] += [" no mpls ip"]

        return ret
