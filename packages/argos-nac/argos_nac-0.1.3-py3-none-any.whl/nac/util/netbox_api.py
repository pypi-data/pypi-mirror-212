from pynetbox import api
from pynetbox.core.api import Api

import logging

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


class NetBoxAPI:
    def __init__(
        self,
        url: str,
        *,
        username: str | None = None,
        password: str | None = None,
        token: str | None = None,
    ):
        self.interface = api(url, token=token)
        if token is None and password is not None:
            self.interface.create_token(username=username, password=password)

    def assert_plugin_installed(self, plugin_name: str, version: str | None = None) -> None:
        """Uses NetBox API to verify if a plugin is installed.

        Provided `version` can use semantic versioning - Eg. `"1"`, `"1.2"` or `"1.2.5"`. Omitted details are ignored.
        """
        plugins = self.interface.plugins.installed_plugins()
        if plugins:
            for pl in plugins:
                if pl.get("package", "") == plugin_name:
                    installed_version = pl.get("version", "")
                    LOGGER.info(
                        f'Plugin "{plugin_name}" version "{installed_version}" detected on remote Netbox instance.'
                    )

                    if version is None:
                        return

                    from semver.version import Version

                    installed = Version.parse(installed_version, optional_minor_and_patch=True)
                    desired = Version.parse(version, optional_minor_and_patch=True)

                    if (
                        desired.major == installed.major
                        and (desired.minor == 0 or desired.minor == installed.minor)
                        and (desired.patch == 0 or desired.patch == installed.patch)
                    ):
                        return

                    raise Exception(
                        f'Plugin "{plugin_name}" expected to have version {desired}, but was {installed}. Exiting.'
                    )
        raise Exception("Plugin is not among installed plugins in Netbox instance. Exiting.")
