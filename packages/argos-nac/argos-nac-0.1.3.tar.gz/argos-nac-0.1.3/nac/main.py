from dataclasses import dataclass
from logging import getLogger
from os import environ, makedirs
from pathlib import Path

from nornir.core.inventory import Defaults
from nornir.core.task import AggregatedResult

from nac.cisco import CiscoNAC
from nac.util.common import HostMapping
from nac.util.netbox_api import NetBoxAPI

from .model import *
from .util.graphql_util import GraphQLUtil
from .__version__ import __version__

LOGGER = getLogger(__name__)


@dataclass
class Settings:
    interactive: bool
    output_dir: Path | None
    backup_dir: Path | None
    dry_run: bool

    netbox_url: str
    netbox_token: str
    site_id: int
    ignore_ssl_cert: bool

    ssh_password: str
    ssh_username: str

    def __repr__(self) -> str:
        pass

    def __str__(self) -> str:
        return f"""Settings:
        - netbox-url:             {self.netbox_url}
        - backup:                 {self.backup_dir is not None}
        - dry-run:                {self.dry_run}
        - interactive:            {self.interactive}
        - ignore-ssl-certificate: {self.ignore_ssl_cert}
        - site-id:                {self.site_id}"""


def get_confirmation(prompt: str) -> bool:
    truthy, falsy = False, False
    while not (truthy or falsy):
        proceed = input(f"{prompt} [y/n]: ")
        proceed = proceed.lower().strip()
        truthy = proceed in ('y', 'yes')
        falsy = proceed in ('n', 'no')
    return truthy


def run():
    settings: Settings = parse_cli_arguments()

    NetBoxAPI(settings.netbox_url, token=settings.netbox_token).assert_plugin_installed("argos_netbox", version="0.1")

    LOGGER.info(f"Querying site data for site: {settings.site_id}.")
    site: Site = GraphQLUtil.get_site_data(
        graphql_url=f"{settings.netbox_url}/graphql",
        token=settings.netbox_token,
        site_id=settings.site_id,
        ignore_ssl=settings.ignore_ssl_cert,
    )

    LOGGER.info(f"Data received. Creating host mappings.")

    defaults = Defaults(
        password=settings.ssh_password,
        username=settings.ssh_username,
        platform="ios",
    )

    # Create host mapping
    host_mapping: HostMapping = HostMapping.from_site(site, defaults)
    LOGGER.info(f"Found {len(host_mapping)} devices to configure: {', '.join((str(x) for x in host_mapping.keys()))}")
    LOGGER.info(settings)
    if settings.interactive:
        ok = get_confirmation("Please double-check the above information. Does it appear correct to you?")
        if not ok:
            LOGGER.info("Exiting.")
            exit()

    # Configure devices
    nac = CiscoNAC(
        host_mapping=host_mapping,
        defaults=defaults,
        dry_run=settings.dry_run,
    )
    result: AggregatedResult = nac.configure_devices(
        backup_dir=settings.backup_dir,
        output_dir=settings.output_dir,
    )
    result.raise_on_error()
    LOGGER.info("Operation completed successfully.")


def get_value(env_name: str, interactive: bool, prompt: str = '', critical: bool = False) -> str:
    value = environ.get(env_name, None)
    if value is None:
        if interactive:
            prompt = f'"{env_name}" unset. {prompt} '
            if not critical:
                value = input(prompt)
            else:
                import getpass

                value = getpass.getpass(prompt)
        else:
            raise Exception(f'Environment variable "{env_name}" unset and command is not running as interactive.')
    return value


def parse_cli_arguments() -> Settings:
    '''Parses and handles incoming CLI arguments.'''

    # Import locally to not clutter scope of caller
    import logging
    from argparse import ArgumentParser, SUPPRESS

    # Setup parser
    parser = ArgumentParser(
        prog="argos-deploy",
        description=f"Query NetBox via GraphQL and deploy the documented services. v{__version__}",
        add_help=False,
    )
    parser.add_argument(
        '-h',
        '--help',
        help='Show this help message and exit.',  # Default implementation is not capitalized
        action='help',
        default=SUPPRESS,
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        dest='verbose',
        help='Enable debug output.',
        default=False,
    )
    parser.add_argument(
        '-d',
        '--dry-run',
        action='store_true',
        dest='dry_run',
        help='Prevent making lasting changes to the network devices.',
        default=False,
    )
    parser.add_argument(
        '-f',
        '--file-output',
        dest='output_dir',
        help='Save commands to be applied in specified directory. Can be used with or without "--dry-run". Directory defaults to "./output" if unspecified.',
        nargs='?',
        default=None,
        const='./output',
    )
    parser.add_argument(
        '-b',
        '--backup',
        dest='backup_dir',
        help='Backup current network device configurations to specified directory. Directory defaults to "./backups" if unspecified.',
        nargs='?',
        default=None,
        const='./backups',
    )
    parser.add_argument(
        '-y',
        '--no-interact',
        action='store_false',
        dest='interactive',
        help='Proceed without further interactions, even through warnings.',
        default=True,
    )
    parser.add_argument(
        '--ignore-ssl',
        action='store_true',
        dest='ignore_ssl',
        help='Ignore NetBox SSL certificate check. Only use in safe environment.',
        default=False,
    )

    # Parse
    args, _ = parser.parse_known_args()

    # Apply known settings accordingly
    LOGGER.setLevel(logging.DEBUG if args.verbose else logging.INFO)

    interactive = args.interactive

    site = int(get_value('SITE', interactive, 'Enter NetBox ID of site:'))
    ssh_username = get_value('SSH_USERNAME', interactive, 'Enter SSH username of network devices:')
    ssh_password = get_value('SSH_PASSWORD', interactive, 'Enter SSH password of network devices:', critical=True)

    netbox_url = get_value('NETBOX_URL', interactive, 'Enter NetBox url:')
    netbox_token = get_value('NETBOX_TOKEN', interactive, 'Enter NetBox token:', critical=True)

    ignore_ssl = args.ignore_ssl or (
        environ.get('IGNORE_SSL_CERTIFICATE', 'false').lower() in ('false', '0', 'f', 'n', 'no')
    )

    output_dir = args.output_dir
    if output_dir is not None:
        output_dir = Path(output_dir).absolute()
        makedirs(output_dir, exist_ok=True)  # Create output directory if not exists

    backup_dir = args.backup_dir
    if backup_dir is not None:
        backup_dir = Path(backup_dir).absolute()
        makedirs(backup_dir, exist_ok=True)  # Create output directory if not exists

    # Order of arguments matters.
    return Settings(
        interactive=interactive,
        backup_dir=backup_dir,
        output_dir=output_dir,
        ignore_ssl_cert=ignore_ssl,
        ssh_username=ssh_username,
        ssh_password=ssh_password,
        netbox_url=netbox_url,
        netbox_token=netbox_token,
        site_id=site,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    run()
