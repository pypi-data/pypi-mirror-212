"""
This module contains the HiSockClient, used to power the client
of HiSock, but also contains a `connect` function, to pass in
things automatically. It is strongly advised to use `connect`
over `HiSockClient`, as `connect` passes in some key arguments
that `HiSockClient` does not provide

====================================
Copyright SSS_Says_Snek, 2021-present
====================================
"""

# Imports
from __future__ import annotations  # Remove when 3.10 is used by majority

import socket
import json  # Handle sending dictionaries
import errno  # Handle fatal errors with the server
import sys  # Utilize stderr
import threading  # Threaded client and decorators
import traceback  # Error handling
from typing import Callable, Union  # Type hints
from ipaddress import IPv4Address  # Comparisons
from time import time  # Unix timestamp support

try:
    # Pip builds require relative import
    from .utils import (
        ClientException,
        ClientNotFound,
        ServerException,
        ServerNotRunning,
        MessageCacheMember,
        ClientInfo,
        Sendable,
        Client,
        _removeprefix,
        _type_cast,
        make_header,
        iptup_to_str,
        validate_ipv4,
    )
    from ._shared import _HiSockBase
except ImportError:
    # Relative import doesn't work for non-pip builds
    from utils import (
        ClientException,
        ClientNotFound,
        ServerException,
        ServerNotRunning,
        MessageCacheMember,
        ClientInfo,
        Sendable,
        Client,
        _removeprefix,
        _type_cast,
        make_header,
        iptup_to_str,
        validate_ipv4,
    )
    from _shared import _HiSockBase


# ░█████╗░░█████╗░██╗░░░██╗████████╗██╗░█████╗░███╗░░██╗██╗
# ██╔══██╗██╔══██╗██║░░░██║╚══██╔══╝██║██╔══██╗████╗░██║██║
# ██║░░╚═╝███████║██║░░░██║░░░██║░░░██║██║░░██║██╔██╗██║██║
# ██║░░██╗██╔══██║██║░░░██║░░░██║░░░██║██║░░██║██║╚████║╚═╝
# ╚█████╔╝██║░░██║╚██████╔╝░░░██║░░░██║╚█████╔╝██║░╚███║██╗
# ░╚════╝░╚═╝░░╚═╝░╚═════╝░░░░╚═╝░░░╚═╝░╚════╝░╚═╝░░╚══╝╚═╝
#   Change this code only if you know what you are doing!
# If this code is changed, the client may not work properly


class HiSockClient(_HiSockBase):
    """
    The client class for :mod:`HiSock`.

    :param addr: A two-element tuple, containing the IP address and the
        port number of where the server is hosted.
        **Only IPv4 is currently supported.**
    :type addr: tuple
    :param name: Either a string or NoneType, representing the name the client
        goes by. Having a name provides an easy interface of sending.
        data to a specific client and identifying clients. It is therefore
        highly recommended to pass in a name.

        Pass in NoneType for no name (:meth:`connect` should handle that)
    :type name: str, optional
    :param group: Either a string or NoneType representing the group the client
        is in. Being in a group provides an easy interface of sending
        data to multiple specific clients, and identifying multiple clients.
        It is highly recommended to provide a group for complex servers.
        Pass in NoneType for no group (:meth:`connect` should handle that).
    :type group: str, optional
    :param header_len: An integer defining the header length of every message.
        A larger header length would mean a larger maximum message length
        (about 10**header_len).
        **MUST** be the same header length as the server, or else it will crash
        (hard to debug too!).
        Default sets to 16 (maximum length of content: 10 quadrillion bytes).
    :type header_len: int, optional
    :param cache_size: The size of the message cache.
        -1 or below for no message cache, 0 for an unlimited cache size,
        and any other number for the cache size.
    :type cache_size: int, optional

    :ivar tuple addr: A two-element tuple containing the IP address and the
        port number of the server.
    :ivar int header_len: An integer storing the header length of each "message".
    :ivar str name: A string representing the name of the client to identify by.
        Default is None.
    :ivar str group: A string representing the group of the client to identify by.
        Default is None.
    :ivar dict funcs: A list of functions registered with decorator :meth:`on`.
        **This is mainly used for under-the-hood-code.**
    :ivar int connect_time: An integer sotring the Unix timestamp of when the
        client connected to the server.
    """

    def __init__(
        self,
        addr: tuple[str, int],
        name: Union[str, None] = None,
        group: Union[str, None] = None,
        header_len: int = 16,
        cache_size: int = -1,
    ):
        super().__init__(addr=addr, header_len=header_len, cache_size=cache_size)

        self.name = name
        self.group = group

        self.original_name = name
        self.original_group = group

        # Socket initialization
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect(self.addr)
        except ConnectionRefusedError:
            raise ServerNotRunning("Server is not running! Aborting...") from None
        self.sock.setblocking(True)

        # Stores the names of the reserved functions and information about them
        self._reserved_funcs = {
            "client_connect": {
                "number_arguments": 1,
                "type_cast_arguments": ("client_data",),
            },
            "client_disconnect": {
                "number_arguments": 1,
                "type_cast_arguments": ("client_data",),
            },
            "force_disconnect": {
                "number_arguments": 0,
                "type_cast_arguments": (),
            },
            "*": {"number_arguments": 2, "type_cast_arguments": ("command", "message")},
        }
        self._unreserved_func_arguments = ("message",)

        # Flags
        self.connected = False
        self.connect_time = 0  # Unix timestamp

        # Send client hello
        self._send_client_hello()

    # Dunders

    def __str__(self) -> str:
        """Example: <HiSockClient connected to 192.168.1.133:5000>"""

        return f"<HiSockClient connected to {iptup_to_str(self.addr)}>"

    def __repr__(self):
        return self.__str__()

    # Comparisons

    def __gt__(self, other: Union[HiSockClient, str]) -> bool:
        """Example: HiSockClient(...) > "192.168.1.133:5000" """

        if type(other) not in (HiSockClient, str):
            raise TypeError("Type not supported for > comparison")
        if isinstance(other, HiSockClient):
            return IPv4Address(self.addr[0]) > IPv4Address(other.addr[0])
        ip = other.split(":")
        return IPv4Address(self.addr[0]) > IPv4Address(ip[0])

    def __ge__(self, other: Union[HiSockClient, str]) -> bool:
        """Example: HiSockClient(...) >= "192.168.1.133:5000" """

        if type(other) not in (HiSockClient, str):
            raise TypeError("Type not supported for >= comparison")
        if isinstance(other, HiSockClient):
            return IPv4Address(self.addr[0]) >= IPv4Address(other.addr[0])
        ip = other.split(":")
        return IPv4Address(self.addr[0]) >= IPv4Address(ip[0])

    def __lt__(self, other: Union[HiSockClient, str]) -> bool:
        """Example: HiSockClient(...) < "192.168.1.133:5000" """

        if type(other) not in (HiSockClient, str):
            raise TypeError("Type not supported for < comparison")
        if isinstance(other, HiSockClient):
            return IPv4Address(self.addr[0]) < IPv4Address(other.addr[0])
        ip = other.split(":")
        return IPv4Address(self.addr[0]) < IPv4Address(ip[0])

    def __le__(self, other: Union[HiSockClient, str]) -> bool:
        """Example: HiSockClient(...) <= "192.168.1.133:5000" """

        if type(other) not in (HiSockClient, str):
            raise TypeError("Type not supported for <= comparison")
        if isinstance(other, HiSockClient):
            return IPv4Address(self.addr[0]) <= IPv4Address(other.addr[0])
        ip = other.split(":")
        return IPv4Address(self.addr[0]) <= IPv4Address(ip[0])

    def __eq__(self, other: Union[HiSockClient, str]) -> bool:
        """Example: HiSockClient(...) == "192.168.1.133:5000" """

        if type(other) not in (HiSockClient, str):
            raise TypeError("Type not supported for == comparison")
        if isinstance(other, HiSockClient):
            return IPv4Address(self.addr[0]) == IPv4Address(other.addr[0])
        ip = other.split(":")
        return IPv4Address(self.addr[0]) == IPv4Address(ip[0])

    # Internal methods

    def _send_client_hello(self):
        """
        Sends a hello to the server for the first connection.

        :raises ClientException: If the client is already connected.
        """

        if self.connected:
            raise ClientException(
                f"Client is already connected! (connected {time() - self.connect_time} seconds ago)"
            )

        hello_dict = {"name": self.name, "group": self.group}
        self._send_raw(f"$CLTHELLO${json.dumps(hello_dict)}")

        self.connected = True
        self.connect_time = time()

    def _handle_keepalive(self):
        """Handle a keepalive sent from the server."""

        self._send_raw("$KEEPACK$")

    # On decorator

    def on(
        self, command: str, threaded: bool = False, override: bool = False
    ) -> Callable:
        """
        A decorator that adds a function that gets called when the client
        receives a matching command.

        Reserved functions are functions that get activated on
        specific events, and they are:

        1. ``client_connect`` - Activated when a client connects to the server
        2. ``client_disconnect`` - Activated when a client disconnects from the server

        The parameters of the function depend on the command to listen.
        For example, reserved functions ``client_connect`` and
        ``client_disconnect`` gets the client's data passed in as an argument.
        All other unreserved functions get the message passed in.

        In addition, certain type casting is available to unreserved functions.
        That means, that, using type hints, you can automatically convert
        between needed instances. The type casting currently supports:

        - ``bytes``
        - ``str``
        - ``int``
        - ``float``
        - ``bool``
        - ``None``
        - ``list`` (with the types listed here)
        - ``dict`` (with the types listed here)

        For more information, read the documentation for type casting.

        :param command: A string, representing the command the function should activate
            when receiving it.
        :type command: str
        :param threaded: A boolean, representing if the function should be run in a thread
            in order to not block the update loop.
            Default is False.
        :type threaded: bool, optional
        :param override: A boolean representing if the function should override the
            reserved function with the same name and to treat it as an unreserved function.
            Default is False.
        :type override: bool, optional

        :return: The same function (the decorator just appended the function to a stack).
        :rtype: function

        :raises TypeError: If the number of function arguments is invalid.
        """

        return self._on(self, command, threaded, override)

    # Getters
    def get_cache(
        self,
        idx: Union[int, slice, None] = None,
    ) -> list[MessageCacheMember]:
        """
        Gets the message cache.

        :param idx: An integer or ``slice``, specifying what specific message caches to return.
            Default is None (retrieves the entire cache).
        :type idx: Union[int, slice], optional

        :return: A list of dictionaries, representing the cache
        :rtype: list[dict]
        """

        if idx is None:
            return self.cache

        return self.cache[idx]

    def get_client(
        self, client: Client, get_as_dict: bool = False
    ) -> Union[ClientInfo, dict]:
        """
        Gets the client data for a client.

        :param client: The client name or IP+port to get.
        :type client: Client
        :param get_as_dict: A boolean representing if the client data should be
            returned as a dictionary. Otherwise, it'll be returned as an
            instance of :class:`ClientInfo`.
            Default is False.
        :type get_as_dict: bool, optional

        :return: The client data.
        :rtype: Union[ClientInfo, dict]

        :raises ValueError: If the client IP is invalid.
        :raises ClientNotFound: If the client couldn't be found.
        :raises ServerException: If another error occurred.
        """

        try:
            validate_ipv4(iptup_to_str(client))
        except ValueError as e:
            # Names are allowed, too.
            if not isinstance(client, str):
                raise e

        self._send_raw(f"$GETCLT${client}")
        response = self.recv()
        response = _type_cast(
            type_cast=dict,
            content_to_type_cast=response,
            func_name="<get_client response>",
        )

        # Validate response
        if "traceback" in response:
            if response["traceback"] == "$NOEXIST$":
                raise ClientNotFound(f"Client {client} not connected to the server.")
            raise ServerException(
                f"Failed to get client from server: {response['traceback']}"
            )

        # Type cast
        if get_as_dict:
            return response
        return ClientInfo(**response)

    def get_server_addr(self) -> tuple[str, int]:
        """
        Gets the address of where the client is connected to.

        :return: A tuple, with the format (str IP, int port)
        :rtype: tuple[str, int]
        """

        return self.addr

    def get_client_addr(self) -> tuple[str, int]:
        """
        Gets the address of the client.

        :return: A tuple, with the format (IP, port).
        :rtype: tuple[str, int]
        """

        return self.sock.getsockname()

    # Transmit data

    def send(self, command: str, content: Sendable = None):
        """
        Sends a command & content to the server.

        :param command: A string, containing the command to send
        :type command: str
        :param content: The message / content to send
        :type content: Sendable, optional
        """

        data_to_send = (
            b"$CMD$" + command.encode() + b"$MSG$" + self._send_type_cast(content)
        )
        content_header = make_header(data_to_send, self.header_len)
        self.sock.send(content_header + data_to_send)

    def _send_raw(self, content: Sendable = None):
        """
        Sends a message to the server: NO COMMAND REQUIRED.
        This is preferable in some situations, where clients need to send
        multiple data over the server, without overcomplicating it with commands

        :param content: The message / content to send
        :type content: Sendable, optional
        """

        data_to_send = self._send_type_cast(content)
        header = make_header(data_to_send, self.header_len)
        self.sock.send(header + data_to_send)

    # Changers

    def change_name(self, new_name: Union[str, None]):
        """
        Changes the name of the client

        :param new_name: The new name for the client to be called.
            If left blank, then the name will be reset.
        :type new_name: Union[str, None]
        """

        if new_name is None:
            new_name = self.original_name

        data_to_send = "$CHNAME$" + new_name
        self._send_raw(data_to_send)

    def change_group(self, new_group: Union[str, None]):
        """
        Changes the client's group.

        :param new_group: The new group name for the client to be called.
            if left blank, then the group will be reset
        :type new_group: Union[str, None]
        """

        if new_group is None:
            new_group = self.original_group

        data_to_send = "$CHGROUP$" + new_group
        self._send_raw(data_to_send)

    # Update

    def _update(self):
        """
        Handles new messages and sends them to the appropriate functions. This method
        should be called in a while loop in a thread. If this function isn't in its
        own thread, then :meth:`recv` won't work.

        .. warning::
           Don't call this method on its own; instead use :meth:`start`.
        """
        if self.closed:
            # This shouldn't happen due to `start` handling it, but just in case...
            return

        try:
            ### Receiving data ###

            self._receiving_data = True
            content_header = None

            try:
                content_header = self.sock.recv(self.header_len)
            except ConnectionResetError:
                raise ServerNotRunning(
                    "Server has stopped running, aborting..."
                ) from None
            except ConnectionAbortedError:
                # Keepalive timeout reached
                self.closed = True
                self._receiving_data = False
                self.close(emit_leave=False)
                return

            if content_header == b"":
                # Happens when the client is closing the connection while receiving
                # data. The content header will be empty.
                return

            data = self.sock.recv(int(content_header.decode()))
            self._receiving_data = False
            if not data:
                # Happens when the client is closing the connection while receiving
                # data. The data will be empty.
                return

            ### Reserved commands ###

            # Handle keepalive
            if data == b"$KEEPALIVE$":
                self._handle_keepalive()
                return

            # Handle force disconnection
            elif data == b"$DISCONN$":
                self.close(emit_leave=False)  # The server already knows we're gone

                self._call_function_reserved("force_disconnect")
                return

            # Handle new client connection
            elif data.startswith(b"$CLTCONN$"):
                if "client_connect" not in self.funcs:
                    return

                client_data = self._type_cast_client_data(
                    "client_connect",
                    _type_cast(
                        type_cast=dict,
                        content_to_type_cast=_removeprefix(data, b"$CLTCONN$"),
                        func_name="<client connect in update>",
                    ),
                )
                self._call_function_reserved("client_connect", client_data)
                return

            # Handle client disconnection
            elif data.startswith(b"$CLTDISCONN$"):
                if "client_disconnect" not in self.funcs:
                    return

                client_data = self._type_cast_client_data(
                    "client_disconnect",
                    _type_cast(
                        type_cast=dict,
                        content_to_type_cast=_removeprefix(data, b"$CLTDISCONN$"),
                        func_name="<client disconnect in update>",
                    ),
                )

                self._call_function_reserved("client_disconnect", client_data)
                return

            ### Unreserved commands ###

            # Handle random data
            elif not data.startswith(b"$CMD$"):
                if "*" not in self.funcs:
                    return
                self._call_wildcard_function(
                    client_data=None, command=None, content=data
                )
                return

            has_listener = False  # For cache

            # Get the command and the message
            command = _removeprefix(data, b"$CMD$").split(b"$MSG$")[0].decode()
            content = _removeprefix(data, f"$CMD${command}$MSG$".encode())

            # No content? (`_removeprefix` didn't do anything)
            if not content or content == data:
                content = None

            # Call functions that are listening for this command from the `on`
            # decorator
            for matching_command, func in self.funcs.items():
                if command != matching_command:
                    continue

                has_listener = True

                # Call function with dynamic args
                arguments = ()
                if len(func["type_hint"]) == 1:
                    arguments = (
                        _type_cast(
                            type_cast=func["type_hint"]["message"],
                            content_to_type_cast=content,
                            func_name=func["name"],
                        ),
                    )
                self._call_function(matching_command, *arguments)
                break
            else:
                has_listener = self._handle_recv_commands(command, content)

            # No listener found
            if not has_listener and "*" in self.funcs:
                # No recv and no catchall. A command and some data.
                self._call_wildcard_function(
                    client_data=None, command=command, content=content
                )

            # Caching
            self._cache(has_listener, command, content, data, content_header)

        except IOError as e:
            # Normal, means message has ended
            if not (
                e.errno != errno.EAGAIN
                and e.errno != errno.EWOULDBLOCK
                and not self.closed
            ):
                return

            # Fatal error, abort client
            traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)
            print(
                "\nServer error encountered, aborting client...",
                file=sys.stderr,
            )
            self.close()

            raise SystemExit from e

    # Stop

    def close(self, emit_leave: bool = True):
        """
        Closes the client; running ``client.update()`` won't do anything now

        :param emit_leave: Decides if the client will emit `leave` to the server or not
        :type emit_leave: bool
        """

        self.closed = True
        if emit_leave:
            try:
                self._send_raw("$USRCLOSE$")
            except OSError:  # Server already closed socket
                return
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
        except OSError:
            # Bad file descriptor
            ...
        self.sock.close()

    # Main loop

    def start(self, callback: Callable = None, error_handler: Callable = None):
        """
        Start the main loop for the client.

        :param callback: A function that will be called every time the
            client receives and handles a message.
        :type callback: Callable, optional
        :param error_handler: A function that will be called every time the
            client encounters an error.
        :type error_handler: Callable, optional
        """

        try:
            while not self.closed:
                self._update()
                if isinstance(callback, Callable):
                    callback()
        except Exception as e:
            if isinstance(error_handler, Callable):
                error_handler(e)
            else:
                raise e


class ThreadedHiSockClient(HiSockClient):
    """
    :class:`HiSockClient`, but running in its own thread as to not block the
    main loop. Please note that while this is running in its own thread, the
    event handlers will still be running in the main thread. To avoid this,
    use the ``threaded=True`` argument for the ``on`` decorator.

    For documentation purposes, see :class:`HiSockClient`.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._thread: threading.Thread
        self._stop_event = threading.Event()

    def close(self, *args, **kwargs):
        """
        Closes the client. Blocks the thread until the client is closed.
        For documentation, see :meth:`HiSockClient.close`.
        """

        super().close(*args, **kwargs)
        self._stop_event.set()
        try:
            self._thread.join()
        except RuntimeError:
            # Cannot join current thread
            return

    def _start(self, callback: Callable = None, error_handler: Callable = None):
        """Start the main loop for the threaded client."""

        def updated_callback():
            if self._stop_event.is_set() and not self.closed:
                self.close()

            # Original callback
            if isinstance(callback, Callable):
                callback()

        super().start(callback=updated_callback, error_handler=error_handler)

    def start(self, callback: Callable = None, error_handler: Callable = None):
        """
        Starts the main client loop.
        For documentation, see :meth:`HiSockClient.start`.
        """

        self._thread = threading.Thread(
            target=self._start, args=(callback, error_handler)
        )
        self._thread.start()


def connect(addr, name=None, group=None, header_len=16, cache_size=-1):
    """
    Creates a `HiSockClient` instance. See HiSockClient for more details

    :param addr: A two-element tuple containing the IP address and
        the port number of the server.
    :type addr: tuple
    :param name: A string containing the name of what the client should go by.
        This argument is optional.
    :type name: str, optional
    :param group: A string, containing the "group" the client is in.
        Groups can be utilized to send specific messages to them only.
        This argument is optional.
    :type group: str, optional
    :param header_len: An integer defining the header length of every message.
        Default is True.
    :type header_len: int, optional
    :param cache_size: The size of the message cache.
        -1 or below for no message cache, 0 for an unlimited cache size,
        and any other number for the cache size.
    :type cache_size: int, optional

    :return: A :class:`HiSockClient` instance.
    :rtype: instance

    .. note::
        A simple way to use this function is to use :func:`utils.input_client_config`
        which will ask you for the server IP, port, name, and group. Then, you can
        call this function by simply doing ``connect(*input_client_config())``
    """

    return HiSockClient(addr, name, group, header_len, cache_size)


def threaded_connect(*args, **kwargs):
    """
    Creates a :class:`ThreadedHiSockClient` instance. See :class:`ThreadedHiSockClient`
    for more details
    :return: A :class:`ThreadedHiSockClient` instance
    """
    return ThreadedHiSockClient(*args, **kwargs)


if __name__ == "__main__":
    print("Testing client!")
    client = connect(
        ("127.0.0.1", int(input("Port: "))),
        name=input("Name: "),
        group=input("Group: "),
    )

    # print(
    # "The HiSock police are on to you. "
    # "You must change your name and group before they catch you."
    # )
    # client.change_name(input("New name: "))
    # client.change_group(input("New group: "))

    @client.on("client_connect")
    def on_connect(client_data):
        print(
            f"{client_data.name} has joined! "
            f"Their IP is {iptup_to_str(client_data.ip)}. "
            f'Their group is {client_data["group"]}.'
        )

    @client.on("client_disconnect", override=True)
    def on_disconnect(leave_data: dict):
        print(
            f'{leave_data["name"]} disconnected from the server because {leave_data["reason"]} :('
        )

    @client.on("force_disconnect")
    def on_force_disconnect():
        print("You have been disconnected from the server.")
        client.close()
        __import__("os")._exit(0)

    @client.on("message", threaded=True)
    def on_message(message: str):
        print(f"Message received:\n{message}")

    @client.on("genocide")
    def on_genocide():
        print("It's time to die!")
        client.close()
        __import__("os")._exit(0)

    @client.on("*")
    def on_wildcard(command: str, data: str):
        print(f"There was some unhandled data from the server. {command=}, {data=}")

    def choices():
        print(
            "Your choices are:"
            "\n\tsend\n\tsend_to_group\n\tchange_name\n\tchange_group\n\tset_timer\n\tstop"
            "\n\tgenocide\n\tsend_random_data"
        )
        while True:
            choice = input("What would you like to do? ")
            if choice == "send":
                client.send("broadcast_message", input("Message: "))
            elif choice == "send_to_group":
                client.send("broadcast_message_to_group", input("Message: "))
            elif choice == "ping":
                client.send("ping")
                ping_time = time()
                client.recv("pong")
                print(f"Pong! Took {time() - ping_time} seconds.")
            elif choice == "change_name":
                client.change_name(input("New name: "))
            elif choice == "change_group":
                client.change_group(input("New group: "))
            elif choice == "set_timer":
                client.send("set_timer", input("Seconds: "))
                client.recv("timer_done")
                print("Timer done!")
            elif choice == "get_all_clients":
                client.send("get_all_clients")
                print(client.recv("all_clients", recv_as=dict))
            elif choice == "stop":
                client.close()
                return
            elif choice == "genocide":
                input("You will kill many people. Do you wish to proceed? ")
                print("Just kidding, your input had no effect. Time for genocide!")
                client.send(
                    "set_timer", input("How many seconds for the genocide to last?")
                )
                client.recv("timer_done")
                print("Genociding...")
                client.send("commit_genocide")
            elif choice == "send_random_data":
                print("Sending some random data...")
                choice, randint = (
                    __import__("random").choice,
                    __import__("random").randint,
                )
                client.send(
                    "uncaught_command",
                    "Random data: "
                    + "".join(
                        [
                            chr(choice((randint(65, 90), randint(97, 122))))
                            for _ in range(100)
                        ]
                    ),
                )
            else:
                print("Invalid choice.")

    choices_thread = threading.Thread(target=choices, daemon=False)
    choices_thread.start()

    client.start()
