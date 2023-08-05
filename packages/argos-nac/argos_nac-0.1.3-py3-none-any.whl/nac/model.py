from abc import abstractmethod
from typing import Any, Dict, List, ClassVar, Literal, Type
from logging import getLogger
from pydantic import (
    BaseModel,
    BaseConfig,
    IPvAnyInterface,
    root_validator,
)

LOGGER = getLogger(__name__)


class MyConfig(BaseConfig):
    underscore_attrs_are_private = True
    # extra = Extra.ignore
    # arbitrary_types_allowed = True


class IDInitializableModel(BaseModel):
    _mappings: ClassVar[Dict[Any, Dict[int, Any]]] = {}

    def __init__(self, *args, **kvargs):
        super().__init__(*args, **kvargs)
        self._post_init()

    @root_validator(pre=True)
    def initialize_from_id_if_known(cls, values):
        """Map ID to known vrfs, if already known. Allows for the graphql query to be simplified."""
        if "id" in values:
            id = int(values["id"])
            cls_dict = IDInitializableModel._mappings.get(cls, None)
            if cls_dict is not None:
                existing_instance = cls_dict.get(id, None)
                if existing_instance is not None:
                    return existing_instance.dict()
        return values

    def _register(self, id: int, cls: Type):
        """Register this instance to make it constructible via ID alone."""
        IDInitializableModel._mappings.setdefault(cls, {})

        cls_dict: Dict = IDInitializableModel._mappings.get(cls)  # type: ignore
        cls_dict.setdefault(id, self)

    @abstractmethod
    def _post_init(self):
        pass


class RouteTarget(BaseModel):
    id: int
    name: str

    Config = MyConfig


class VRF(IDInitializableModel):
    id: int
    name: str
    rd: str | None
    import_targets: List[RouteTarget] = []
    export_targets: List[RouteTarget] = []

    def __hash__(self):
        return (self.__class__, self.id).__hash__()

    def _post_init(self):
        self._register(self.id, VRF)

    class Config(MyConfig):
        frozen = True


class Manufacturer(BaseModel):
    id: int
    slug: str

    Config = MyConfig


class DeviceType(BaseModel):
    manufacturer: Manufacturer

    Config = MyConfig


class IPAddressWithMask(BaseModel):
    id: int
    address: IPvAnyInterface
    vrf: VRF | None

    Config = MyConfig


class Interface(IDInitializableModel):
    id: int
    mode: str | None
    name: str
    mgmt_only: bool
    ip_addresses: List[IPAddressWithMask]
    vrf: VRF | None

    def __hash__(self):
        return (self.__class__, self.id).__hash__()

    def _post_init(self):
        self._register(self.id, Interface)

    Config = MyConfig


class LDP(BaseModel):
    id: int
    auto_range: bool
    label_start: int | None
    label_end: int | None
    ldp_enabled_interfaces: List[Interface]


class ASN(BaseModel):
    id: int
    asn: int


class BGP_CE(BaseModel):
    id: int
    ip_addresses: List[IPAddressWithMask]
    asn: ASN


class BGP_Neighbour(BaseModel):
    id: int
    update_source_interface: Interface
    asn: ASN


class AddressFamily(BaseModel):
    id: int
    vpnv4_address_family: bool
    vpnv4_community: Literal['STANDARD', "EXTENDED", "BOTH"] | None
    vpnv6_address_family: bool
    vpnv6_community: Literal['STANDARD', "EXTENDED", "BOTH"] | None

    Config = MyConfig


class BGP_Mesh_Neighbourhood(IDInitializableModel):
    id: int
    bgp_mesh: List[BGP_Neighbour]
    address_family: AddressFamily

    def _post_init(self):
        self._register(self.id, BGP_Mesh_Neighbourhood)

    Config = MyConfig


class BGP_PE(BaseModel):
    id: int
    update_source_interface: Interface
    asn: ASN
    advertised_customers: List[BGP_CE]
    bgp_mesh: BGP_Mesh_Neighbourhood | None


class Device(IDInitializableModel):
    id: int
    name: str | None
    device_type: DeviceType | None
    interfaces: List[Interface]
    ldp: LDP | None
    bgp_pe: BGP_PE | None

    _chosen_management_interface: Interface | None = None

    def _post_init(self):
        self._register(self.id, Device)

    def get_management_interface(self) -> Interface | None:
        if self._chosen_management_interface is None:
            for interface in self.interfaces:
                if interface.mgmt_only:
                    if interface.ip_addresses is not None and len(interface.ip_addresses) > 0:
                        self._chosen_management_interface = interface
                        break
                    else:
                        LOGGER.warning(
                            f"Interface {interface.id} on device {self.id} is a designated management interface, but has no IP associated. Skipped."
                        )
        return self._chosen_management_interface

    Config = MyConfig


class Site(BaseModel):
    id: int
    devices: List[Device]

    Config = MyConfig


class QueryPrerequisites(BaseModel):
    """Data which needs to be loaded into the lookup table ahead of the model of interest"""

    vrf_list: List[VRF]
    interface_list: List[Interface]
    bgp_mesh_list: List[BGP_Mesh_Neighbourhood]
