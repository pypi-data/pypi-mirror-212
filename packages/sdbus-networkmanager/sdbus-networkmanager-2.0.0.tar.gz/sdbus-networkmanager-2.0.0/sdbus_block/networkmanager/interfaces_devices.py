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


class NetworkManagerDeviceBluetoothInterface(
        DbusInterfaceCommon,
        interface_name='org.freedesktop.NetworkManager.Device.Bluetooth'):
    """Bluetooth device interface"""

    @dbus_property('s')
    def name(self) -> str:
        """Name of Bluetooth device"""
        raise NotImplementedError

    @dbus_property('u')
    def bt_capabilities(self) -> int:
        """Bluetooth device capabilities

        See :py:class:`BluetoothCapabilities`
        """
        raise NotImplementedError


class NetworkManagerDeviceBondInterface(
        DbusInterfaceCommon,
        interface_name='org.freedesktop.NetworkManager.Device.Bond'):
    """Bond device interface"""

    @dbus_property('ao')
    def slaves(self) -> List[str]:
        """List of paths of enslaved devices"""
        raise NotImplementedError


class NetworkManagerDeviceBridgeInterface(
        DbusInterfaceCommon,
        interface_name='org.freedesktop.NetworkManager.Device.Bridge'):
    """Bridge device interface"""

    @dbus_property('ao')
    def slaves(self) -> List[str]:
        """List of paths of enslaved devices"""
        raise NotImplementedError


class NetworkManagerDeviceGenericInterface(
        DbusInterfaceCommon,
        interface_name='org.freedesktop.NetworkManager.Device.Generic'):
    """Generic device interface"""

    @dbus_property('s')
    def type_description(self) -> str:
        """Description of the interface type"""
        raise NotImplementedError


class NetworkManagerDeviceIPTunnelInterface(
        DbusInterfaceCommon,
        interface_name='org.freedesktop.NetworkManager.Device.IPTunnel'):
    """IP tunnel device interface"""

    @dbus_property('u')
    def mode(self) -> int:
        """Tunnel mode

        See :py:class:`IpTunnelMode`
        """
        raise NotImplementedError

    @dbus_property('o')
    def parent(self) -> str:
        """Object path of parent device"""
        raise NotImplementedError

    @dbus_property('s')
    def local(self) -> str:
        """Local endpoint"""
        raise NotImplementedError

    @dbus_property('s')
    def remote(self) -> str:
        """Remote endpoint"""
        raise NotImplementedError

    @dbus_property('y')
    def ttl(self) -> int:
        """Time to Live (TTL)

        0 is special value meaning the packets inherit TTL value.
        """
        raise NotImplementedError

    @dbus_property('y')
    def tos(self) -> int:
        """Type of service (IPv4) or traffic class (IPv6)"""
        raise NotImplementedError

    @dbus_property('b')
    def path_mtu_discovery(self) -> bool:
        """Whether path MTU discovery is enabled on this tunnel"""
        raise NotImplementedError

    @dbus_property('s')
    def input_key(self) -> str:
        """Key used for incoming packets"""
        raise NotImplementedError

    @dbus_property('s')
    def output_key(self) -> str:
        """Key used for outgoing packets"""
        raise NotImplementedError

    @dbus_property('y')
    def encapsulation_limit(self) -> int:
        """How many levels of enapsulation are permitted

        Only IPv6 tunnels
        """
        raise NotImplementedError

    @dbus_property('u')
    def flow_label(self) -> int:
        """Flow label assigned to tunnel packets

        Only IPv6 tunnels
        """
        raise NotImplementedError

    @dbus_property('u')
    def flags(self) -> int:
        """Tunnel flags

        Missing upstream documentation
        """
        raise NotImplementedError


class NetworkManagerDeviceLowpanInterface(
        DbusInterfaceCommon,
        interface_name='org.freedesktop.NetworkManager.Device.Lowpan'):
    """6LoWPAN device interface"""

    @dbus_property('o')
    def parent(self) -> str:
        """Path to parent device"""
        raise NotImplementedError


class NetworkManagerDeviceMacsecInterface(
        DbusInterfaceCommon,
        interface_name='org.freedesktop.NetworkManager.Device.Macsec'):
    """MacSec device interface"""

    @dbus_property('o')
    def parent(self) -> str:
        """Path to parent device"""
        raise NotImplementedError

    @dbus_property('t')
    def sci(self) -> int:
        """Secure Channel Identifier"""
        raise NotImplementedError

    @dbus_property('y')
    def icv_length(self) -> int:
        """Length of Integrity Check Value"""
        raise NotImplementedError

    @dbus_property('t')
    def cipher_suite(self) -> int:
        """Set of cryptographic algorithms in use

        Not documented upstream.
        """
        raise NotImplementedError

    @dbus_property('u')
    def window(self) -> int:
        """Size of replay window. (in number of packets)"""
        raise NotImplementedError

    @dbus_property('y')
    def encoding_sa(self) -> int:
        """Security Association in use"""
        raise NotImplementedError

    @dbus_property('s')
    def validation(self) -> str:
        """Validation mode for incoming packets

        * strict
        * check
        * disabled
        """
        raise NotImplementedError

    @dbus_property('b')
    def encrypt(self) -> bool:
        """Whether encryption of transmitted frames is enabled"""
        raise NotImplementedError

    @dbus_property('b')
    def protect(self) -> bool:
        """Whether protection of transmitted frames is enabled"""
        raise NotImplementedError

    @dbus_property('b')
    def include_sci(self) -> bool:
        """Whether SCI is always included in transmitted SecTAG"""
        raise NotImplementedError

    @dbus_property(
        property_signature='b',
        property_name='Es',
    )
    def end_station_enabled(self) -> bool:
        """Whether End Station bit is enabled in SecTAG"""
        raise NotImplementedError

    @dbus_property(
        property_signature='b',
        property_name='Scb',
    )
    def scb_enabled(self) -> bool:
        """Whether Single Copy Broadcast is enabled in SecTAG"""
        raise NotImplementedError

    @dbus_property('b')
    def replay_protect(self) -> bool:
        """Whether replay protection is enabled"""
        raise NotImplementedError


class NetworkManagerDeviceMacvlanInterface(
        DbusInterfaceCommon,
        interface_name='org.freedesktop.NetworkManager.Device.Macvlan'):
    """MACVLAN device interface"""

    @dbus_property('o')
    def parent(self) -> str:
        """Path to parent device"""
        raise NotImplementedError

    @dbus_property('s')
    def mode(self) -> str:
        """MacVlan mode

        One of:
        * private
        * vepa
        * bridge
        * passthru
        """
        raise NotImplementedError

    @dbus_property('b')
    def no_promisc(self) -> bool:
        """Whether this device is blocked from promiscuous mode"""
        raise NotImplementedError

    @dbus_property('b')
    def tap(self) -> bool:
        """Whether the device is macvtap"""
        raise NotImplementedError


class NetworkManagerDeviceModemInterface(
        DbusInterfaceCommon,
        interface_name='org.freedesktop.NetworkManager.Device.Modem'):
    """Modem device interface"""

    @dbus_property('u')
    def modem_capabilities(self) -> int:
        """Modem radio technology

        Switching the radio technology might require
        firmware reboot.

        See :py:class:`ModemCapabilities`
        """
        raise NotImplementedError

    @dbus_property('u')
    def current_capabilities(self) -> int:
        """Current supported radio technologies without firmware reload"""
        raise NotImplementedError

    @dbus_property('s')
    def device_id(self) -> str:
        """Unique modem identifier"""
        raise NotImplementedError

    @dbus_property('s')
    def operator_code(self) -> str:
        """Mobile country codes (MCC) + mobile network codes (MNC)

        Blank if disconnected or not a 3GPP modem.
        """
        raise NotImplementedError

    @dbus_property('s')
    def apn(self) -> str:
        """Access point name modem is connected to.

        Blank if disconnected.
        """
        raise NotImplementedError


class NetworkManagerDeviceOlpcMeshInterface(
        DbusInterfaceCommon,
        interface_name='org.freedesktop.NetworkManager.Device.OlpcMesh'):
    """OLPC Wireless Mesh device interface"""

    @dbus_property('o')
    def companion(self) -> str:
        """Path to companion device"""
        raise NotImplementedError

    @dbus_property('u')
    def active_channel(self) -> int:
        """Currently active channel"""
        raise NotImplementedError


class NetworkManagerDeviceOvsBridgeInterface(
        DbusInterfaceCommon,
        interface_name='org.freedesktop.NetworkManager.Device.OvsBridge'):
    """Open vSwitch device interface"""

    @dbus_property('ao')
    def slaves(self) -> List[str]:
        """List of paths to slave devices"""
        raise NotImplementedError


class NetworkManagerDeviceOvsPortInterface(
        DbusInterfaceCommon,
        interface_name='org.freedesktop.NetworkManager.Device.OvsPort'):
    """Open vSwitch port device interface"""

    @dbus_property('ao')
    def slaves(self) -> List[str]:
        """List of paths to slave devices"""
        raise NotImplementedError


class NetworkManagerDeviceStatisticsInterface(
        DbusInterfaceCommon,
        interface_name='org.freedesktop.NetworkManager.Device.Statistics'):
    """Device statistics interface"""

    @dbus_property('u')
    def refresh_rate_ms(self) -> int:
        """Refreshed rate of properties of this interface in milliseconds."""
        raise NotImplementedError

    @dbus_property('t')
    def tx_bytes(self) -> int:
        """Number of transmitted bytes"""
        raise NotImplementedError

    @dbus_property('t')
    def rx_bytes(self) -> int:
        """Number of received bytes"""
        raise NotImplementedError


class NetworkManagerDeviceTeamInterface(
        DbusInterfaceCommon,
        interface_name='org.freedesktop.NetworkManager.Device.Team'):
    """Teaming device

    Aggregates multiple devices to a single one.

    Seems to be Network Manager specific type bond device.
    """
    @dbus_property('ao')
    def slaves(self) -> List[str]:
        """List of paths to slave devices"""
        raise NotImplementedError

    @dbus_property('s')
    def config(self) -> str:
        """JSON config of the device"""
        raise NotImplementedError


class NetworkManagerDeviceTunInterface(
        DbusInterfaceCommon,
        interface_name='org.freedesktop.NetworkManager.Device.Tun'):
    """Userspace tunneling device interface"""

    @dbus_property('x')
    def owner(self) -> int:
        """User ID (UID) of the device owner"""
        raise NotImplementedError

    @dbus_property('x')
    def group(self) -> int:
        """Group ID (GID) of the device owner"""
        raise NotImplementedError

    @dbus_property('s')
    def mode(self) -> str:
        """Tunnel mode

        Either tun or tap
        """
        raise NotImplementedError

    @dbus_property('b')
    def no_pi(self) -> bool:
        """If true no protocol info is prepended to packets"""
        raise NotImplementedError

    @dbus_property('b')
    def vnet_hdr(self) -> bool:
        """If true tunnel packets include virtio network header"""
        raise NotImplementedError

    @dbus_property('b')
    def multi_queue(self) -> bool:
        """If true callers can connect multiple times"""
        raise NotImplementedError


class NetworkManagerDeviceVethInterface(
        DbusInterfaceCommon,
        interface_name='org.freedesktop.NetworkManager.Device.Veth'):
    """Virtual Ethernet device interface"""

    @dbus_property('o')
    def peer(self) -> str:
        """Path to peer device"""
        raise NotImplementedError


class NetworkManagerDeviceVlanInterface(
        DbusInterfaceCommon,
        interface_name='org.freedesktop.NetworkManager.Device.Vlan'):
    """Virtual LAN device interface"""

    @dbus_property('o')
    def parent(self) -> str:
        """Path to parent device"""
        raise NotImplementedError

    @dbus_property('u')
    def vlan_id(self) -> int:
        """VLAN ID of this interface"""
        raise NotImplementedError


class NetworkManagerDeviceVrfInterface(
        DbusInterfaceCommon,
        interface_name='org.freedesktop.NetworkManager.Device.Vrf'):
    """Virtual routing and forwarding device interface"""

    @dbus_property('u')
    def table(self) -> int:
        """Routing table ID of this device"""
        raise NotImplementedError


class NetworkManagerDeviceVxlanInterface(
        DbusInterfaceCommon,
        interface_name='org.freedesktop.NetworkManager.Device.Vxlan'):
    """Virtual Extensible LAN device interface"""

    @dbus_property('o')
    def parent(self) -> str:
        """Path to parent device"""
        raise NotImplementedError

    @dbus_property(
        property_signature='u',
        property_name='Id'
    )
    def vxlan_id(self) -> int:
        """VXLAN Network Identifier (VNI)"""
        raise NotImplementedError

    @dbus_property('s')
    def group(self) -> str:
        """Multicast IP group used to communicate (v4 or v6)"""
        raise NotImplementedError

    @dbus_property('s')
    def local(self) -> str:
        """Local IP address used to communicate"""
        raise NotImplementedError

    @dbus_property('y')
    def tos(self) -> int:
        """TOS field of IP packets"""
        raise NotImplementedError

    @dbus_property('y')
    def ttl(self) -> int:
        """TTL of IP packets"""
        raise NotImplementedError

    @dbus_property('b')
    def learning(self) -> bool:
        """If true VXLAN dynamically learns the remote IP address"""
        raise NotImplementedError

    @dbus_property('u')
    def ageing(self) -> int:
        """Interval in seconds at which kernel purges stale cached addresses"""
        raise NotImplementedError

    @dbus_property('u')
    def limit(self) -> int:
        """Maximum number of entries in forwarding table"""
        raise NotImplementedError

    @dbus_property('q')
    def dst_port(self) -> int:
        """Destination port for outgoing packets"""
        raise NotImplementedError

    @dbus_property('q')
    def src_port_min(self) -> int:
        """Lowest source port for outgoing packets"""
        raise NotImplementedError

    @dbus_property('q')
    def src_port_max(self) -> int:
        """Highest source port for outgoing packets"""
        raise NotImplementedError

    @dbus_property(
        property_signature='b',
        property_name='Proxy')
    def arp_proxy(self) -> bool:
        """If true ARP proxying is enabled"""
        raise NotImplementedError

    @dbus_property(
        property_signature='b',
        property_name='Rsc')
    def route_short_circuit(self) -> bool:
        """If true route short circuiting is enabled"""
        raise NotImplementedError

    @dbus_property('b')
    def l2miss(self) -> bool:
        """If true emit netlink notification on L2 switch misses"""
        raise NotImplementedError

    @dbus_property('b')
    def l3miss(self) -> bool:
        """If true emit netlink notification on L3 switch misses"""
        raise NotImplementedError


class NetworkManagerDeviceWifiP2PInterface(
        DbusInterfaceCommon,
        interface_name='org.freedesktop.NetworkManager.Device.WifiP2P'):
    """Wi-Fi Peet to Peer device interface"""

    @dbus_method('a{sv}')
    def start_find(
        self,
        options: Dict[str, Tuple[str, Any]],
    ) -> None:
        """Start find operation for Wi-Fi P2P peers

        Options supported:

        * ``timeout`` of type "i" which is a number of seconds \
                    for search timeout between 1-600. Default 300.
        """
        raise NotImplementedError

    @dbus_method()
    def stop_find(self) -> None:
        """Stop find operation"""
        raise NotImplementedError

    @dbus_property('ao')
    def peers(self) -> List[str]:
        """List of peer objects paths visible to this Wi-Fi device"""
        raise NotImplementedError


class NetworkManagerDeviceWiredInterface(
        DbusInterfaceCommon,
        interface_name='org.freedesktop.NetworkManager.Device.Wired'):
    """Wired Ethernet device interface"""

    @dbus_property('s')
    def perm_hw_address(self) -> str:
        """Permanent hardware address"""
        raise NotImplementedError

    @dbus_property('u')
    def speed(self) -> int:
        """Design speed of the device in megabits/second"""
        raise NotImplementedError

    @dbus_property('as')
    def s390_subchannels(self) -> List[str]:
        """Array of IBM Z Architecture S/390 subchannels"""
        raise NotImplementedError


class NetworkManagerDeviceWireGuardInterface(
        DbusInterfaceCommon,
        interface_name='org.freedesktop.NetworkManager.Device.WireGuard'):
    """WireGuard device interface"""

    @dbus_property('ay')
    def public_key(self) -> bytes:
        """Public key of the device"""
        raise NotImplementedError

    @dbus_property('q')
    def listen_port(self) -> int:
        """UDP listening port for incoming connections"""
        raise NotImplementedError

    @dbus_property('u')
    def fw_mark(self) -> int:
        """Optional packet marker to set routing policy"""
        raise NotImplementedError


class NetworkManagerDeviceWirelessInterface(
        DbusInterfaceCommon,
        interface_name='org.freedesktop.NetworkManager.Device.Wireless'):
    """Wi-Fi device interface"""

    @dbus_method(
        result_signature='ao',
    )
    def get_all_access_points(
        self,
    ) -> List[str]:
        """Return the list of paths to all access points visible

        Includes the hidden ones without SSID.
        """
        raise NotImplementedError

    @dbus_method('a{sv}',
                 )
    def request_scan(
        self,
        options: Dict[str, Tuple[str, Any]],
    ) -> None:
        """Request to scan for Wi-Fi access points

        Options:

        * ``ssids`` of type 'ayy' (List[bytes])
        """
        raise NotImplementedError

    @dbus_property('s')
    def perm_hw_address(self) -> str:
        """Permanent hardware address"""
        raise NotImplementedError

    @dbus_property('u')
    def mode(self) -> int:
        """Operating mode of the device

        See :py:class:`WiFiOperationMode`
        """
        raise NotImplementedError

    @dbus_property('u')
    def bitrate(self) -> int:
        """Bit rate currently used in kilobits/second"""
        raise NotImplementedError

    @dbus_property('ao')
    def access_points(self) -> List[str]:
        """List of paths of access point currently visible"""
        raise NotImplementedError

    @dbus_property('o')
    def active_access_point(self) -> str:
        """Path to currently used access point"""
        raise NotImplementedError

    @dbus_property('u')
    def wireless_capabilities(self) -> int:
        """List of wireless device capabilities

        See :py:class:`WirelessCapabilities`
        """
        raise NotImplementedError

    @dbus_property('x')
    def last_scan(self) -> int:
        """Time in CLOCK_BOOTTIME milliseconds since last scan

        Value -1 means never scanned.
        """
        raise NotImplementedError


class NetworkManagerDeviceInterface(
        DbusInterfaceCommon,
        interface_name='org.freedesktop.NetworkManager.Device'):
    """Device interface with common functionality"""

    @dbus_method(
        input_signature='a{sa{sv}}tu',
    )
    def reapply(
        self,
        connection: Dict[str, Dict[str, Tuple[str, Any]]],
        version_id: int,
        flags: int = 0,
    ) -> None:
        """Attempt to update the device configuration without deactivating

        :param connection: Optional connection settings to be reapplied
        :param version_id: Current version id of applied connection.
        :param flags: currently there are no flags so it should be zero
        """
        raise NotImplementedError

    @dbus_method(
        input_signature='u',
        result_signature='a{sa{sv}}t',
    )
    def get_applied_connection(
        self,
        flags: int = 0,
    ) -> Tuple[Dict[str, Dict[str, Tuple[str, Any]]], int]:
        """Get the currently applied connection on the device

        :param flags: Currently there are no flags so this should be zero
        :returns: Tuple of dictionary of connection settings \
                 and an int version id.
        """
        raise NotImplementedError

    @dbus_method()
    def disconnect(
        self,
    ) -> None:
        """Disconnect device and prevent from automatically activating"""
        raise NotImplementedError

    @dbus_method()
    def delete(
        self,
    ) -> None:
        """Deletes the software device.

        Raises an exception if the device is a hardware device.
        """
        raise NotImplementedError

    @dbus_property('s')
    def udi(self) -> str:
        """Not stable device identifier

        Should not be used for tracking connection.
        """
        raise NotImplementedError

    @dbus_property('s')
    def path(self) -> str:
        """Device path as exposed by Udev"""
        raise NotImplementedError

    @dbus_property('s')
    def interface(self) -> str:
        """Name of device control interface (???)"""
        raise NotImplementedError

    @dbus_property('s')
    def ip_interface(self) -> str:
        """Name of device data interface (???)"""
        raise NotImplementedError

    @dbus_property('s')
    def driver(self) -> str:
        """Driver handling device"""
        raise NotImplementedError

    @dbus_property('s')
    def driver_version(self) -> str:
        """Driver version"""
        raise NotImplementedError

    @dbus_property('s')
    def firmware_version(self) -> str:
        """Firmware version of the device"""
        raise NotImplementedError

    @dbus_property('u')
    def capabilities(self) -> int:
        """Capabilities of the device

        See :py:class:`DeviceCapabilities`
        """
        raise NotImplementedError

    @dbus_property('u')
    def state(self) -> int:
        """Device state.

        See :py:class:`DeviceState`
        """
        raise NotImplementedError

    @dbus_property('(uu)')
    def state_reason(self) -> Tuple[int, int]:
        """Current state and the reason.

        See :py:class:`DeviceState` and :py:class:`DeviceStateReason`
        """
        raise NotImplementedError

    @dbus_property('o')
    def active_connection(self) -> str:
        """Path of active connection object"""
        raise NotImplementedError

    @dbus_property('o')
    def ip4_config(self) -> str:
        """Path of Ip4Config object

        Only valid when device is in ACTIVATED state.
        """
        raise NotImplementedError

    @dbus_property('o')
    def dhcp4_config(self) -> str:
        """Path of Dhcp4 object

        Only valid when device is in ACTIVATED state.
        """
        raise NotImplementedError

    @dbus_property('o')
    def ip6_config(self) -> str:
        """Path to Ip6Config object

        Only valid when device is in ACTIVATED state.
        """
        raise NotImplementedError

    @dbus_property('o')
    def dhcp6_config(self) -> str:
        """Path to Dhcp6 object

        Only valid when device is in ACTIVATED state.
        """
        raise NotImplementedError

    @dbus_property('b')
    def managed(self) -> bool:
        """Whether or not this device is manager by NetworkManager

        This setting can be written.
        The value is not persistent on NetworkManager restarts.
        """
        raise NotImplementedError

    @dbus_property('b')
    def autoconnect(self) -> bool:
        """If true device is allowed to auto connect

        Can be written.
        """
        raise NotImplementedError

    @dbus_property('b')
    def firmware_missing(self) -> bool:
        """If true means the device is missing firmware"""
        raise NotImplementedError

    @dbus_property('b')
    def nm_plugin_missing(self) -> bool:
        """If true means the plugin for NetworkManager is missing"""
        raise NotImplementedError

    @dbus_property('u')
    def device_type(self) -> int:
        """Device type

        See :py:class:`DeviceType`
        """
        raise NotImplementedError

    @dbus_property('ao')
    def available_connections(self) -> List[str]:
        """List of object paths to connections available"""
        raise NotImplementedError

    @dbus_property('s')
    def physical_port_id(self) -> str:
        """Physical network port of the device"""
        raise NotImplementedError

    @dbus_property('u')
    def mtu(self) -> int:
        """Maximum Transmission Unit"""
        raise NotImplementedError

    @dbus_property('u')
    def metered(self) -> int:
        """Whether the traffic is subject to limitations

        See :py:class:`DeviceMetered`
        """
        raise NotImplementedError

    @dbus_property('aa{sv}')
    def lldp_neighbors(self) -> List[Dict[str, Tuple[str, Any]]]:
        """List of LLDP neighbors

        Each element is the dictionary of LLDP TLV names \
        to variants values.
        """
        raise NotImplementedError

    @dbus_property('b')
    def real(self) -> bool:
        """Whether this device is exists

        If it does not yet exist it can be automatically created \
        if one of the available connections becomes activated.
        """
        raise NotImplementedError

    @dbus_property('u')
    def ip4_connectivity(self) -> int:
        """IPv4 connectivity state

        See :py:class:`ConnectivityState`
        """
        raise NotImplementedError

    @dbus_property('u')
    def ip6_connectivity(self) -> int:
        """IPv6 connectivity state

        See :py:class:`ConnectivityState`
        """
        raise NotImplementedError

    @dbus_property('u')
    def interface_flags(self) -> int:
        """Interface flags

        See :py:class:`DeviceInterfaceFlags`
        """
        raise NotImplementedError

    @dbus_property('s')
    def hw_address(self) -> str:
        """Hardware address"""
        raise NotImplementedError

    def get_applied_connection_profile(
            self
    ) -> Tuple[ConnectionProfile, int]:
        """Get the currently applied connection on the device.

        .. note::

            This method cannot fetch secrets. Use
            :py:meth:`NetworkManagerSettingsConnectionInterfaceAsync.get_profile`
            to acquire profile with secrets.

        :returns: Tuple of profile and version id.
        :rtype: Tuple[ConnectionProfile, int]
        """

        connection_vardict, version_id = self.get_applied_connection(0)

        return ConnectionProfile.from_dbus(connection_vardict), version_id

    def reapply_profile(
            self,
            profile: ConnectionProfile,
            version_id: int = 0,
    ) -> None:
        """Attempts to update the configuration of a device
        without deactivating it.

        :param ConnectionProfile profile: Connection profile to update
            with.
        :param int version_id: If non-zero, the current version id of
            the applied-connection must match. The current version id can be
            retrieved via :py:meth:`get_applied_connection_profile`.
        """
        self.reapply(profile.to_dbus(), version_id, 0)


class NetworkManagerPPPInterface(
        DbusInterfaceCommon,
        interface_name='org.freedesktop.NetworkManager.PPP'):
    """Helper interface for PPP plugin"""

    @dbus_method(
        result_signature='ss',
    )
    def need_secrets(
        self,
    ) -> Tuple[str, str]:
        """Need secrets?

        Returns the tuple of username and password
        """
        raise NotImplementedError

    @dbus_method('a{sv}')
    def set_ip4_config(
        self,
        config: Dict[str, Tuple[str, Any]],
    ) -> None:
        """Set IPv4 configuration"""
        raise NotImplementedError

    @dbus_method('a{sv}')
    def set_ip6_config(
        self,
        config: Dict[str, Tuple[str, Any]],
    ) -> None:
        """Set IPv6 configuration"""
        raise NotImplementedError

    @dbus_method('u')
    def set_state(
        self,
        state: int,
    ) -> None:
        """Set connection state.

        Not documented upstream.
        """
        raise NotImplementedError

    @dbus_method('i')
    def set_ifindex(
        self,
        ifindex: int,
    ) -> None:
        """Set input device index

        Not documented upstream.
        """
        raise NotImplementedError


class NetworkManagerLoopbackInterface(
    DbusInterfaceCommon,
    interface_name='org.freedesktop.NetworkManager.Device.Loopback',
):
    ...
