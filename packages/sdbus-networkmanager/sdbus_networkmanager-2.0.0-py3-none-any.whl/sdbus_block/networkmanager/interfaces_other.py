# SPDX-License-Identifier: LGPL-2.1-or-later

# Copyright (C) 2020, 2021 igo95862

# This file is part of python-sdbus

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA
from __future__ import annotations

from typing import Any, Dict, List, Tuple

from sdbus import DbusInterfaceCommon, dbus_method, dbus_property

from .settings import ConnectionProfile
from .types import NetworkManagerConnectionProperties


class NetworkManagerAccessPointInterface(
        DbusInterfaceCommon,
        interface_name='org.freedesktop.NetworkManager.AccessPoint'):
    """Interface representing Wi-Fi access point"""

    @dbus_property('u')
    def flags(self) -> int:
        """Flags describing capabilities of the point

        See :py:class:`AccessPointCapabilities`
        """
        raise NotImplementedError

    @dbus_property('u')
    def wpa_flags(self) -> int:
        """Flags WPA authentication and encryption

        See :py:class:`WpaSecurityFlags`
        """
        raise NotImplementedError

    @dbus_property('u')
    def rsn_flags(self) -> int:
        """Flags describing RSN (Robust Secure Network) capabilities

        See :py:class:`WpaSecurityFlags`
        """
        raise NotImplementedError

    @dbus_property('ay')
    def ssid(self) -> bytes:
        """SSID of the access point. (name)"""
        raise NotImplementedError

    @dbus_property('u')
    def frequency(self) -> int:
        """Frequency in MHz"""
        raise NotImplementedError

    @dbus_property('s')
    def hw_address(self) -> str:
        """Hardware address (BSSID)"""
        raise NotImplementedError

    @dbus_property('u')
    def mode(self) -> int:
        """Mode of operation of access point

        See :py:class:`WiFiOperationMode`
        """
        raise NotImplementedError

    @dbus_property('u')
    def max_bitrate(self) -> int:
        """Maximum bit rate of this access point. (in kilobits/second)"""
        raise NotImplementedError

    @dbus_property('y')
    def strength(self) -> int:
        """Current signal quality in % percent"""
        raise NotImplementedError

    @dbus_property('i')
    def last_seen(self) -> int:
        """Timestamp in CLOCK_BOOTTIME seconds since last seen in scan

        Value of -1 means that the point was never found in scans.
        """
        raise NotImplementedError


class NetworkManagerSecretAgentManagerInterface(
        DbusInterfaceCommon,
        interface_name='org.freedesktop.NetworkManager.AgentManager'):
    """Secret Agent Manager"""

    @dbus_method('s')
    def register(
        self,
        identifier: str,
    ) -> None:
        """Identifies an agent.

        Only one agent in each user session may use same identifier.
        """
        raise NotImplementedError

    @dbus_method('su')
    def register_with_capabilities(
        self,
        identifier: str,
        capabilities: int,
    ) -> None:
        """Same as register() but with agent capabilities

        See :py:class:`SecretAgentCapabilities`
        """
        raise NotImplementedError

    @dbus_method()
    def unregister(
        self,
    ) -> None:
        """Notify NetworkManager that secret agent is no longer active"""
        raise NotImplementedError


class NetworkManagerCheckpointInterface(
        DbusInterfaceCommon,
        interface_name='org.freedesktop.NetworkManager.Checkpoint'):
    """Network Manager configuration snapshot interface"""

    @dbus_property('ao')
    def devices(self) -> List[str]:
        """List of devices which are part of this checkpoint"""
        raise NotImplementedError

    @dbus_property('x')
    def created(self) -> int:
        """Snapohot creation time in CLOCK_BOOTTIME milliseconds"""
        raise NotImplementedError

    @dbus_property('u')
    def rollback_timeout(self) -> int:
        """Automatic tollback timeout in seconds or zero"""
        raise NotImplementedError


class NetworkManagerConnectionActiveInterface(
        DbusInterfaceCommon,
        interface_name='org.freedesktop.NetworkManager.Connection.Active'):
    """Represents an attempt to connect to network"""

    @dbus_property('o')
    def connection(self) -> str:
        """Path of connection object"""
        raise NotImplementedError

    @dbus_property('o')
    def specific_object(self) -> str:
        """Specific object associated with active connection"""
        raise NotImplementedError

    @dbus_property('s')
    def id(self) -> str:
        """Connection id"""
        raise NotImplementedError

    @dbus_property('s')
    def uuid(self) -> str:
        """Connection UUID"""
        raise NotImplementedError

    @dbus_property(
        property_signature='s',
        property_name="Type"
    )
    def connection_type(self) -> str:
        """Connection type"""
        raise NotImplementedError

    @dbus_property('ao')
    def devices(self) -> List[str]:
        """Array of devices object paths which are part of connection"""
        raise NotImplementedError

    @dbus_property('u')
    def state(self) -> int:
        """Connection state

        See :py:class:`ConnectionState`
        """
        raise NotImplementedError

    @dbus_property('u')
    def state_flags(self) -> int:
        """Connection state flags

        See :py:class:`ConnectionStateFlags`
        """
        raise NotImplementedError

    @dbus_property('b')
    def default(self) -> bool:
        """Whether or not this connection owns default IPv4 route"""
        raise NotImplementedError

    @dbus_property('o')
    def ip4_config(self) -> str:
        """Object path to Ip4Config object

        Only valid if connection state is ACTIVATED
        """
        raise NotImplementedError

    @dbus_property('o')
    def dhcp4_config(self) -> str:
        """Object path to Dhcp4Config object

        Only valid if connection state is ACTIVATED
        """
        raise NotImplementedError

    @dbus_property('b')
    def default6(self) -> bool:
        """Whether or not this connection owns default IPv6 route"""
        raise NotImplementedError

    @dbus_property('o')
    def ip6_config(self) -> str:
        """Object path to Ip4Config object

        Only valid if connection state is ACTIVATED
        """
        raise NotImplementedError

    @dbus_property('o')
    def dhcp6_config(self) -> str:
        """Object path to Dhcp6Config object

        Only valid if connection state is ACTIVATED
        """
        raise NotImplementedError

    @dbus_property('b')
    def vpn(self) -> bool:
        """Whether this connection is a VPN"""
        raise NotImplementedError

    @dbus_property('o')
    def master(self) -> str:
        """Path to master device if this connection is a slave"""
        raise NotImplementedError


class NetworkManagerVPNConnectionInterface(
        DbusInterfaceCommon,
        interface_name='org.freedesktop.NetworkManager.VPN.Connection'):
    """VPN connection interface"""

    @dbus_property('u')
    def vpn_state(self) -> int:
        """VPN connection state

        See :py:class:`ConnectionState`
        """
        raise NotImplementedError

    @dbus_property('s')
    def banner(self) -> str:
        """Banner string of VPN connection"""
        raise NotImplementedError


class NetworkManagerDHCP4ConfigInterface(
        DbusInterfaceCommon,
        interface_name='org.freedesktop.NetworkManager.DHCP4Config'):
    """DHCPv4 configuration"""

    @dbus_property('a{sv}')
    def options(self) -> Dict[str, Tuple[str, Any]]:
        """Options and configurations returned by DHCPv4 server"""
        raise NotImplementedError


class NetworkManagerDHCP6ConfigInterface(
        DbusInterfaceCommon,
        interface_name='org.freedesktop.NetworkManager.DHCP6Config'):
    """DHCPv6 configuration"""

    @dbus_property('a{sv}')
    def options(self) -> Dict[str, Tuple[str, Any]]:
        """Options and configurations returned by DHCPv6 server"""
        raise NotImplementedError


class NetworkManagerDnsManagerInterface(
        DbusInterfaceCommon,
        interface_name='org.freedesktop.NetworkManager.DnsManager'):
    """DNS configuration state"""

    @dbus_property('s')
    def mode(self) -> str:
        """Current DNS processing mode"""
        raise NotImplementedError

    @dbus_property('s')
    def rc_manager(self) -> str:
        """Current resolv.conf management mode"""
        raise NotImplementedError


class NetworkManagerIP4ConfigInterface(
        DbusInterfaceCommon,
        interface_name='org.freedesktop.NetworkManager.IP4Config'):
    """IPv4 configuration state"""

    @dbus_property('aa{sv}')
    def address_data(self) -> List[Dict[str, Tuple[str, Any]]]:
        """Array of IP address data objects

        Each dictionary includes ``'address'`` item with IP address string \
        and ``'prefix'`` with an int of prefix. Some addresses may include \
        additional attributes.
        """
        raise NotImplementedError

    @dbus_property('s')
    def gateway(self) -> str:
        """Gateway in use"""
        raise NotImplementedError

    @dbus_property('aa{sv}')
    def route_data(self) -> List[Dict[str, Tuple[str, Any]]]:
        """Array of route data objects

        Each dictionary includes 'dest' (IP address string), 'prefix' (int).
        Some routes may include 'next-hop', 'metric' and additional attributes.
        """
        raise NotImplementedError

    @dbus_property('aa{sv}')
    def nameserver_data(self) -> List[Dict[str, Tuple[str, Any]]]:
        """List of nameserver objects

        Currently, each dictionary only has the 'address' value. \
        (string of IP address)
        """
        raise NotImplementedError

    @dbus_property('as')
    def domains(self) -> List[str]:
        """List of domains this address belongs to."""
        raise NotImplementedError

    @dbus_property('as')
    def searches(self) -> List[str]:
        """List of DNS searches"""
        raise NotImplementedError

    @dbus_property('as')
    def dns_options(self) -> List[str]:
        """List of dns options"""
        raise NotImplementedError

    @dbus_property('i')
    def dns_priority(self) -> int:
        """Relative priority of DNS servers"""
        raise NotImplementedError

    @dbus_property('as')
    def wins_server_data(self) -> List[str]:
        """Windows Internet Name Service servers"""
        raise NotImplementedError


class NetworkManagerIP6ConfigInterface(
        DbusInterfaceCommon,
        interface_name='org.freedesktop.NetworkManager.IP6Config'):
    """IPv6 configuration"""

    @dbus_property('aa{sv}')
    def address_data(self) -> List[Dict[str, Tuple[str, Any]]]:
        """Array of IP address data objects

        Each dictionary includes ``'address'`` item with IP address string \
        and ``'prefix'`` with an int of prefix. Some addresses may include \
        additional attributes.
        """
        raise NotImplementedError

    @dbus_property('s')
    def gateway(self) -> str:
        """Gateway in use"""
        raise NotImplementedError

    @dbus_property('aa{sv}')
    def route_data(self) -> List[Dict[str, Tuple[str, Any]]]:
        """Array of route data objects

        Each dictionary includes 'dest' (IP address string), 'prefix' (int).
        Some routes may include 'next-hop', 'metric' and additional attributes.
        """
        raise NotImplementedError

    @dbus_property('aay')
    def nameservers(self) -> List[bytes]:
        """Nameservers in use"""
        raise NotImplementedError

    @dbus_property('as')
    def domains(self) -> List[str]:
        """List of domains this address belongs to."""
        raise NotImplementedError

    @dbus_property('as')
    def searches(self) -> List[str]:
        """List of DNS searches"""
        raise NotImplementedError

    @dbus_property('as')
    def dns_options(self) -> List[str]:
        """List of dns options"""
        raise NotImplementedError

    @dbus_property('i')
    def dns_priority(self) -> int:
        """Relative priority of DNS servers"""
        raise NotImplementedError


class NetworkManagerSecretAgentInterface(
        DbusInterfaceCommon,
        interface_name='org.freedesktop.NetworkManager.SecretAgent'):
    """D-Bus interface that stores secrets such as Wi-Fi passwords"""

    @dbus_method(
        input_signature='a{sa{sv}}osasu',
        result_signature='a{sa{sv}}',
    )
    def get_secrets(
        self,
        connection: NetworkManagerConnectionProperties,
        connection_path: str,
        setting_name: str,
        hints: List[str],
        flags: int,
    ) -> Dict[str, Dict[str, Tuple[str, Any]]]:
        """Retrieve stored secrets"""
        raise NotImplementedError

    @dbus_method('os')
    def cancel_get_secrets(
        self,
        connection_path: str,
        setting_name: str,
    ) -> None:
        """Cancel pending get_secrets request"""
        raise NotImplementedError

    @dbus_method('a{sa{sv}}o')
    def save_secrets(
        self,
        connection: NetworkManagerConnectionProperties,
        connection_path: str,
    ) -> None:
        """Save given secrets"""
        raise NotImplementedError

    @dbus_method('a{sa{sv}}o')
    def delete_secrets(
        self,
        connection: NetworkManagerConnectionProperties,
        connection_path: str,
    ) -> None:
        """Delete secrets"""
        raise NotImplementedError


class NetworkManagerSettingsConnectionInterface(
        DbusInterfaceCommon,
        interface_name='org.freedesktop.NetworkManager.Settings.Connection'):
    """Represents a single network connection"""

    @dbus_method('a{sa{sv}}')
    def update(
        self,
        properties: NetworkManagerConnectionProperties,
    ) -> None:
        """Update connection settings.

        Replaces all previous settings and properties.
        """
        raise NotImplementedError

    @dbus_method('a{sa{sv}}')
    def update_unsaved(
        self,
        properties: NetworkManagerConnectionProperties,
    ) -> None:
        """Update connection settings but do not save to disk"""
        raise NotImplementedError

    @dbus_method()
    def delete(
        self,
    ) -> None:
        """Delete connection"""
        raise NotImplementedError

    @dbus_method(
        result_signature='a{sa{sv}}',
    )
    def get_settings(
        self,
    ) -> NetworkManagerConnectionProperties:
        """Get connection settings"""
        raise NotImplementedError

    @dbus_method(
        input_signature='s',
        result_signature='a{sa{sv}}',
    )
    def get_secrets(
        self,
        setting_name: str,
    ) -> Dict[str, Dict[str, Tuple[str, Any]]]:
        """Get connection secrets"""
        raise NotImplementedError

    @dbus_method()
    def clear_secrets(
        self,
    ) -> None:
        """Clear connection secrets"""
        raise NotImplementedError

    @dbus_method()
    def save(
        self,
    ) -> None:
        """Save connection settings to storage"""
        raise NotImplementedError

    @dbus_method(
        input_signature='a{sa{sv}}ua{sv}',
        result_signature='a{sv}',
    )
    def update2(
        self,
        settings: NetworkManagerConnectionProperties,
        flags: int,
        args: Dict[str, Tuple[str, Any]],
    ) -> Dict[str, Tuple[str, Any]]:
        """Update connection settings"""
        raise NotImplementedError

    @dbus_property('b')
    def unsaved(self) -> bool:
        """If true some settings are not saved to disk"""
        raise NotImplementedError

    @dbus_property('u')
    def flags(self) -> int:
        """Connection flags

        See :py:class:`ConnectionFlags`
        """
        raise NotImplementedError

    @dbus_property('s')
    def filename(self) -> str:
        """File that stores connection settings"""
        raise NotImplementedError

    def update_profile(
            self,
            profile: ConnectionProfile,
            save_to_disk: bool = False,
    ) -> None:
        """Update connection using the profile dataclass.

        :param ConnectionProfile profile: Connection profile to update
            with.

        :param bool save_to_disk: Make changes permanent by saving
            updated values to disk.

            By default changes are temporary. (saved only to RAM)
        """
        flags = 0

        if save_to_disk:
            flags |= 0x1
        else:
            flags |= 0x2

        self.update2(profile.to_dbus(), flags, {})

    def get_profile(self, fetch_secrets: bool = True) -> ConnectionProfile:
        """Get the connection settings as the profile object.

        :param bool fetch_secrets: Retrieve secret values. (like VPN passwords)
            Makes additional calls to NetworkManager.
        """
        profile = ConnectionProfile.from_dbus(self.get_settings())

        if fetch_secrets:
            secrets_name_generator = profile.update_secrets_generator()
            try:
                secrets_name = next(secrets_name_generator)
                while True:
                    secret_profile = ConnectionProfile.from_dbus(
                        self.get_secrets(secrets_name))

                    secrets_name = secrets_name_generator.send(secret_profile)
            except StopIteration:
                ...

        return profile


class NetworkManagerSettingsInterface(
        DbusInterfaceCommon,
        interface_name='org.freedesktop.NetworkManager.Settings'):
    """Global NetworkManager settings"""

    @dbus_method(
        result_signature='ao',
    )
    def list_connections(
        self,
    ) -> List[str]:
        """List of connection object paths"""
        raise NotImplementedError

    @dbus_method(
        input_signature='s',
        result_signature='o',
    )
    def get_connection_by_uuid(
        self,
        uuid: str,
    ) -> str:
        """Get connection path by UUID"""
        raise NotImplementedError

    @dbus_method(
        input_signature='a{sa{sv}}',
        result_signature='o',
    )
    def add_connection(
        self,
        connection: NetworkManagerConnectionProperties,
    ) -> str:
        """Add connection and save to disk"""
        raise NotImplementedError

    @dbus_method(
        input_signature='a{sa{sv}}',
        result_signature='o',
    )
    def add_connection_unsaved(
        self,
        connection: NetworkManagerConnectionProperties,
    ) -> str:
        """Add connection and do not save"""
        raise NotImplementedError

    @dbus_method(
        input_signature='a{sa{sv}}ua{sv}',
        result_signature='oa{sv}',
    )
    def add_connection2(
        self,
        settings: NetworkManagerConnectionProperties,
        flags: int,
        args: Dict[str, Tuple[str, Any]],
    ) -> Tuple[str, Dict[str, Tuple[str, Any]]]:
        """Add connection. Flags indicate whether to save or not"""
        raise NotImplementedError

    @dbus_method(
        input_signature='as',
        result_signature='bas',
    )
    def load_connections(
        self,
        filenames: List[str],
    ) -> Tuple[bool, List[str]]:
        """Load connections from filenames

        :returns: Tuple of success and list of failed connection filenames.
        """
        raise NotImplementedError

    @dbus_method(
        result_signature='b',
    )
    def reload_connections(
        self,
    ) -> bool:
        """Reload all connection from disk"""
        raise NotImplementedError

    @dbus_method('s')
    def save_hostname(
        self,
        hostname: str,
    ) -> None:
        """Save hostname to persistent configuration

        If blank hostname is cleared.
        """
        raise NotImplementedError

    @dbus_property('ao')
    def connections(self) -> List[str]:
        """List of paths to connection objects"""
        raise NotImplementedError

    @dbus_property('s')
    def hostname(self) -> str:
        """Current hostname"""
        raise NotImplementedError

    @dbus_property('b')
    def can_modify(self) -> bool:
        """If true adding and modifying connections is supported"""
        raise NotImplementedError

    def add_connection_profile(
            self,
            profile: ConnectionProfile,
            save_to_disk: bool = False,
    ) -> Tuple[str, None]:
        """Add new connection using the profile object.

         :param ConnectionProfile profile: Connection profile to update
            with.

        :param bool save_to_disk: Make changes permanent by saving
            updated values to disk.

            By default changes are temporary. (saved only to RAM)

        :return: Object path of new connection and None
        :rtype: Tuple[str, None]
        """
        flags = 0

        if save_to_disk:
            flags |= 0x1
        else:
            flags |= 0x2

        return (
            (self.add_connection2(profile.to_dbus(), flags, {}))[0],
            None,
        )


class NetworkManagerVPNPluginInterface(
        DbusInterfaceCommon,
        interface_name='org.freedesktop.NetworkManager.VPN.Plugin'):
    """Interface provided by VPN plugins"""

    @dbus_method('a{sa{sv}}')
    def connect(
        self,
        connection: NetworkManagerConnectionProperties,
    ) -> None:
        """Connect to described connection

        Interactive secrets requests not allowed.
        """
        raise NotImplementedError

    @dbus_method('a{sa{sv}}a{sv}')
    def connect_interactive(
        self,
        connection: NetworkManagerConnectionProperties,
        details: Dict[str, Tuple[str, Any]],
    ) -> None:
        """Connect to described connection

        Interactive secrets requests allowed.
        (emits secrets_required signal)
        """
        raise NotImplementedError

    @dbus_method(
        input_signature='a{sa{sv}}',
        result_signature='s',
    )
    def need_secrets(
        self,
        settings: NetworkManagerConnectionProperties,
    ) -> str:
        """Asks plugin if connection will require secrets

        :return: Setting name that requires secrets
        """
        raise NotImplementedError

    @dbus_method()
    def disconnect(
        self,
    ) -> None:
        """Disconnect from VPN"""
        raise NotImplementedError

    @dbus_method('a{sv}')
    def set_config(
        self,
        config: Dict[str, Tuple[str, Any]],
    ) -> None:
        """Set generic connection details"""
        raise NotImplementedError

    @dbus_method('a{sv}')
    def set_ip4_config(
        self,
        config: Dict[str, Tuple[str, Any]],
    ) -> None:
        """Set IPv4 settings"""
        raise NotImplementedError

    @dbus_method('a{sv}')
    def set_ip6_config(
        self,
        config: Dict[str, Tuple[str, Any]],
    ) -> None:
        """Set IPv6 settings"""
        raise NotImplementedError

    @dbus_method('s')
    def set_failure(
        self,
        reason: str,
    ) -> None:
        """Set the plugin failure reason"""
        raise NotImplementedError

    @dbus_method('a{sa{sv}}')
    def new_secrets(
        self,
        connection: NetworkManagerConnectionProperties,
    ) -> None:
        """Called in response to secrets_required signal

        param: Describes the connection including the new secrets
        """
        raise NotImplementedError

    @dbus_property('u')
    def state(self) -> int:
        """VPN state

        See :py:class:`VpnState`
        """
        raise NotImplementedError


class NetworkManagerWifiP2PPeerInterface(
        DbusInterfaceCommon,
        interface_name='org.freedesktop.NetworkManager.WifiP2PPeer'):
    """Interface of a peer in Wi-Fi P2P connection"""

    @dbus_property('s')
    def name(self) -> str:
        """Device name"""
        raise NotImplementedError

    @dbus_property('u')
    def flags(self) -> int:
        """Flags describing capabilities of the point

        See :py:class:`AccessPointCapabilities`
        """
        raise NotImplementedError

    @dbus_property('s')
    def manufacturer(self) -> str:
        """Manufacturer of the Wi-Fi P2P peer."""
        raise NotImplementedError

    @dbus_property('s')
    def model(self) -> str:
        """Peer model"""
        raise NotImplementedError

    @dbus_property('s')
    def model_number(self) -> str:
        """Peer model number"""
        raise NotImplementedError

    @dbus_property('s')
    def serial(self) -> str:
        """Peer serial"""
        raise NotImplementedError

    @dbus_property('ay')
    def wfd_i_es(self) -> bytes:
        """Wi-Fi Display Information Elements of the peer"""
        raise NotImplementedError

    @dbus_property('y')
    def strength(self) -> int:
        """Current signal quality of the peer, in percent."""
        raise NotImplementedError

    @dbus_property('i')
    def last_seen(self) -> int:
        """Timestamp in CLOCK_BOOTTIME seconds since last seen in scan

        Value of -1 means that the point was never found in scans.
        """
        raise NotImplementedError


class NetworkManagerInterface(
        DbusInterfaceCommon,
        interface_name='org.freedesktop.NetworkManager'):
    """Main network manager interface"""

    @dbus_method('u')
    def reload(
        self,
        flags: int = 0x0,
    ) -> None:
        """Reload NetworkManager configuration

        Flags control what to reload:

        * 0x0 everything
        * 0x1 NetworkManager.conf
        * 0x2 DNS configuration
        * 0x4 Restart DNS plugin

        :param flags: Reload what?
        """
        raise NotImplementedError

    @dbus_method(
        result_signature='ao',
    )
    def get_devices(
        self,
    ) -> List[str]:
        """Get list of device object paths known"""
        raise NotImplementedError

    @dbus_method(
        result_signature='ao',
    )
    def get_all_devices(
        self,
    ) -> List[str]:
        """Get list of device object paths with placeholders"""
        raise NotImplementedError

    @dbus_method(
        input_signature='s',
        result_signature='o',
    )
    def get_device_by_ip_iface(
        self,
        iface: str,
    ) -> str:
        """Get device object path by interface name"""
        raise NotImplementedError

    @dbus_method(
        input_signature='ooo',
        result_signature='o',
    )
    def activate_connection(
        self,
        connection: str = '/',
        device: str = '/',
        specific_object: str = '/',
    ) -> str:
        """Activate the connection.

        :return: Activated connection object path.
        """
        raise NotImplementedError

    @dbus_method(
        input_signature='a{sa{sv}}oo',
        result_signature='oo',
    )
    def add_and_activate_connection(
        self,
        connection: NetworkManagerConnectionProperties,
        device: str,
        specific_object: str,
    ) -> Tuple[str, str]:
        """Add a new connection and activate"""
        raise NotImplementedError

    @dbus_method(
        input_signature='a{sa{sv}}ooa{sv}',
        result_signature='ooa{sv}',
    )
    def add_and_activate_connection2(
        self,
        connection: NetworkManagerConnectionProperties,
        device: str,
        specific_object: str,
        options: Dict[str, Tuple[str, Any]],
    ) -> Tuple[str, str, Dict[str, Tuple[str, Any]]]:
        """Add a new connection and activate"""
        raise NotImplementedError

    @dbus_method('o')
    def deactivate_connection(
        self,
        active_connection: str,
    ) -> None:
        """Deactivate connection by given path"""
        raise NotImplementedError

    @dbus_method('b')
    def sleep(
        self,
        sleep: bool,
    ) -> None:
        """Intended for system suspend/resume tracking not user"""
        raise NotImplementedError

    @dbus_method('b')
    def enable(
        self,
        enable: bool,
    ) -> None:
        """Disables all networking when set to false"""
        raise NotImplementedError

    @dbus_method(
        result_signature='a{ss}',
    )
    def get_permissions(
        self,
    ) -> Dict[str, str]:
        """Returns the permissions of caller"""
        raise NotImplementedError

    @dbus_method('ss')
    def set_logging(
        self,
        level: str,
        domains: str,
    ) -> None:
        """Set logging verbosity and which operations are logged"""
        raise NotImplementedError

    @dbus_method(
        result_signature='ss',
    )
    def get_logging(
        self,
    ) -> Tuple[str, str]:
        """Get current logging settings"""
        raise NotImplementedError

    @dbus_method(
        result_signature='u',
    )
    def check_connectivity(
        self,
    ) -> int:
        """Get current connectivity state

        See  :py:class:`NetworkManagerConnectivityState`
        """
        raise NotImplementedError

    @dbus_method(
        result_signature='u',
        method_name='State',
    )
    def get_state(
        self,
    ) -> int:
        """Get current NetworkManager state

        See :py:class:`NetworkManagerState`
        """
        raise NotImplementedError

    @dbus_method(
        input_signature='aouu',
        result_signature='o',
    )
    def checkpoint_create(
        self,
        devices: List[str],
        rollback_timeout: int,
        flags: int,
    ) -> str:
        """Create configuration checkpoint for given devices

        :return: New checkpoint object path
        """
        raise NotImplementedError

    @dbus_method('o')
    def checkpoint_destroy(
        self,
        checkpoint: str,
    ) -> None:
        """Destroy given checkpoint"""
        raise NotImplementedError

    @dbus_method(
        input_signature='o',
        result_signature='a{su}',
    )
    def checkpoint_rollback(
        self,
        checkpoint: str,
    ) -> Dict[str, int]:
        """Use given checkpoint to rollback configuration"""
        raise NotImplementedError

    @dbus_method('ou')
    def checkpoint_adjust_rollback_timeout(
        self,
        checkpoint: str,
        add_timeout: int,
    ) -> None:
        """Adjust checkpoint rollback timeout"""
        raise NotImplementedError

    @dbus_property('ao')
    def devices(self) -> List[str]:
        """List of all current devices"""
        raise NotImplementedError

    @dbus_property('ao')
    def all_devices(self) -> List[str]:
        """List of all current and un-realized devices"""
        raise NotImplementedError

    @dbus_property('ao')
    def checkpoints(self) -> List[str]:
        """List of all checkpoint objects"""
        raise NotImplementedError

    @dbus_property('b')
    def networking_enabled(self) -> bool:
        """Whether networking enabled or not"""
        raise NotImplementedError

    @dbus_property('b')
    def wireless_enabled(self) -> bool:
        """Whether wireless enabled or not"""
        raise NotImplementedError

    @dbus_property('b')
    def wireless_hardware_enabled(self) -> bool:
        """Whether wireless hardware enabled with RF kill switch"""
        raise NotImplementedError

    @dbus_property('b')
    def wwan_enabled(self) -> bool:
        """Whether mobile broadband devices enabled"""
        raise NotImplementedError

    @dbus_property('b')
    def wwan_hardware_enabled(self) -> bool:
        """Whether mobile hardware devices enabled with RF kill switch"""
        raise NotImplementedError

    @dbus_property('b')
    def wimax_enabled(self) -> bool:
        raise NotImplementedError

    @dbus_property('ao')
    def active_connections(self) -> List[str]:
        """List of active connection paths"""
        raise NotImplementedError

    @dbus_property('o')
    def primary_connection(self) -> str:
        """Object path for primary connection"""
        raise NotImplementedError

    @dbus_property('s')
    def primary_connection_type(self) -> str:
        """Primary connection type"""
        raise NotImplementedError

    @dbus_property('u')
    def metered(self) -> int:
        """Primary connection metered status

        See :py:class:`DeviceMetered`
        """
        raise NotImplementedError

    @dbus_property('o')
    def activating_connection(self) -> str:
        """Primary connection activating connection"""
        raise NotImplementedError

    @dbus_property('b')
    def startup(self) -> bool:
        """Whether NetworkManager is still activating"""
        raise NotImplementedError

    @dbus_property('s')
    def version(self) -> str:
        """NetworkManager version"""
        raise NotImplementedError

    @dbus_property('au')
    def capabilities(self) -> List[int]:
        """NetworkManager capabilities

        * 1 Team devices
        * 2 OpenVSwitch
        """
        raise NotImplementedError

    @dbus_property('u')
    def state(self) -> int:
        """Overall state of NetworkManager

        See :py:class:`NetworkManagerState`
        """
        raise NotImplementedError

    @dbus_property('u')
    def connectivity(self) -> int:
        """Overall state of connectivity

        See :py:class:`NetworkManagerConnectivityState`
        """
        raise NotImplementedError

    @dbus_property('b')
    def connectivity_check_available(self) -> bool:
        raise NotImplementedError

    @dbus_property('b')
    def connectivity_check_enabled(self) -> bool:
        """Whether the connectivity checking is enabled

        Can be written.
        """
        raise NotImplementedError

    @dbus_property('s')
    def connectivity_check_uri(self) -> str:
        """URI that network manager will hit to check internet connection"""
        raise NotImplementedError

    @dbus_property('a{sv}')
    def global_dns_configuration(self) -> Dict[str, Tuple[str, Any]]:
        """Global DNS connection settings"""
        raise NotImplementedError

    def add_and_activate_connection_profile(
            self,
            profile: ConnectionProfile,
            device_path: str = '/',
            specific_object: str = '/',
    ) -> Tuple[str, str]:
        """Adds new connection using the profile object as template.

         :param ConnectionProfile profile: Connection profile to update
            with.

        :param str device_path: Object path of device to be activated
            using the given connection

        :param str specific_object: The path of a connection-type-specific
            object this activation should use.

            This parameter is currently ignored for wired and mobile broadband
            connections, and the value of "/" should be used.

        :return: Object path of new connection and path of active connection.
        :rtype: Tuple[str, str]
        """

        return self.add_and_activate_connection(
            profile.to_dbus(),
            device_path,
            specific_object,
        )
