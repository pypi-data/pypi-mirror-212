from dataclasses import dataclass
from logging import getLogger

from nornir.core.task import Task

from nac.util.common import Util

from ...model import *
from ..nornir_util import CiscoNornirUtil

LOGGER = getLogger(__name__)


class BGPUtil(Util):
    @staticmethod
    def generate_remove_config(task: Task, known_asn: ASN | None) -> List[str]:
        """Generate commands to purge previously set config from the device."""
        installed_bgp_asns: List[str] = CiscoNornirUtil.get_configured_bgp_asns(task)
        commands: List[str] = []

        for asn in installed_bgp_asns:
            if known_asn is None or int(asn) != known_asn.asn:
                commands.append(f"no router bgp {asn}")
        LOGGER.debug(f"Found {len(commands)} bgps to remove.")
        return commands

    @staticmethod
    def generate_config(task: Task, device: Device) -> List[str]:
        if device.bgp_pe is None:
            return BGPUtil.generate_remove_config(task, known_asn=None)

        bgp_pe: BGP_PE = device.bgp_pe

        ret: List[str] = []
        ret += BGPUtil.generate_remove_config(task, known_asn=bgp_pe.asn)
        ret += [
            f"router bgp {bgp_pe.asn.asn}",
            " no bgp default ipv4-unicast",
            " address-family ipv4",
            " exit-address-family",
            " address-family ipv6",
            " exit-address-family",
        ]
        ret += BGPUtil.generate_vrf_subconfig(task, bgp_pe)
        ret += BGPUtil.generate_bgp_neighbour_subconfig(device)

        return ret

    @staticmethod
    def generate_bgp_neighbour_subconfig(device: Device) -> List[str]:
        """
        Precondition: device has a valid, not-None BGP_PE member field.
        """
        config: List[str] = []
        vpnv4_config: List[str] = []
        vpnv6_config: List[str] = []

        bgp_pe: BGP_PE = device.bgp_pe  # type: ignore
        mesh = bgp_pe.bgp_mesh
        if mesh is None:
            raise Exception(f'BGP PE instance of "{device.name}" does not appear to be part of any BGP mesh.')

        @dataclass
        class ValidatedNeighbour:
            address: IPvAnyInterface
            asn: ASN

        valid_neighbours: List[ValidatedNeighbour] = []

        for neighbour in mesh.bgp_mesh:
            if neighbour.id != bgp_pe.id:
                if neighbour.update_source_interface.ip_addresses is None:
                    raise Exception(
                        f'Expected "ip_addresses" list in BGP PE neighour with ID "{neighbour.id}" in mesh with ID "{mesh.id}".'
                    )
                for address in neighbour.update_source_interface.ip_addresses:
                    valid_neighbours.append(ValidatedNeighbour(address=address.address, asn=neighbour.asn))

        for neighbour in valid_neighbours:
            config += [
                f' neighbor {neighbour.address.ip} remote-as {neighbour.asn.asn}',
                f' neighbor {neighbour.address.ip} update-source {bgp_pe.update_source_interface.name}',
            ]
            if mesh.address_family.vpnv4_address_family == True:
                community = mesh.address_family.vpnv4_community
                if community is None:
                    community = ''
                vpnv4_config += [
                    f"  neighbor {neighbour.address.ip} activate",
                    f"  neighbor {neighbour.address.ip} send-community {community.lower()}",
                ]
            if mesh.address_family.vpnv6_address_family == True:
                community = mesh.address_family.vpnv4_community
                if community is None:
                    community = ''
                vpnv6_config += [
                    f"  neighbor {neighbour.address.ip} activate",
                    f"  neighbor {neighbour.address.ip} send-community {community.lower()}",
                ]

        if mesh.address_family.vpnv4_address_family == True:
            config += [" address-family vpnv4"]
            config += vpnv4_config
            config += [" exit-address-family"]
        if mesh.address_family.vpnv6_address_family == True:
            config += [" address-family vpnv6"]
            config += vpnv6_config
            config += [" exit-address-family"]

        return config

    @staticmethod
    def generate_vrf_subconfig(task: Task, bgp_pe: BGP_PE) -> List[str]:
        ret: List[str] = []

        @dataclass
        class Customer:
            address: str
            asn: int

        mapping: Dict[str, Dict[int, List[Customer]]] = {}
        """{<vrf_name>:{ip_v:[<customers>]}}"""

        # Generate map to avoid customers in same vrf overwriting eachother in the config.

        for advertised_customer in bgp_pe.advertised_customers:
            assert advertised_customer.asn is not None
            for address in advertised_customer.ip_addresses:
                if address.vrf is not None:
                    vrf_name: str = address.vrf.name
                    version: int = address.address.version
                    mapping.setdefault(vrf_name, {})
                    mapping[vrf_name].setdefault(version, [])
                    mapping[vrf_name][version].append(
                        Customer(address=address.address.ip, asn=advertised_customer.asn.asn)
                    )

        for vrf_name, x in mapping.items():
            for ip_v, customers in x.items():
                ret += [f" address-family ipv{ip_v} vrf {vrf_name}"]
                for c in customers:
                    ret += [
                        f"  neighbor {c.address} remote-as {c.asn}",
                        f"  neighbor {c.address} activate",
                    ]
                ret += [" exit-address-family"]
        return ret
