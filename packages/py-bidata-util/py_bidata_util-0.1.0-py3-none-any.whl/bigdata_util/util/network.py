#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import socks
import socket

default_socket = socket.socket
default_getaddrinfo = None


def set_proxy_global(proxy_url):
    """
    设置本python进程的全局代理
    :param proxy_url:
    :return:
    """
    from urllib.parse import urlparse
    proxy_info = urlparse(proxy_url)

    # https://github.com/albin3/book-notes/issues/1
    import socks
    import socket

    proxy_type = socks.PROXY_TYPE_HTTP
    if proxy_info.scheme.startswith('socks4'):
        proxy_type = socks.PROXY_TYPE_SOCKS4
    elif proxy_info.scheme.startswith('socks5'):
        proxy_type = socks.PROXY_TYPE_SOCKS5
    proxy_host = proxy_info.hostname
    proxy_port = proxy_info.port

    socks.setdefaultproxy(proxy_type, proxy_host, proxy_port)
    socket.socket = socks.socksocket

    global getaddrinfo

    # Magic!
    def new_getaddrinfo(*args):
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]
    getaddrinfo = new_getaddrinfo
    pass


def reset_proxy_global():
    import socket
    if default_socket is not None:
        socket.socket = default_socket

    global getaddrinfo
    if default_getaddrinfo is not None:
        getaddrinfo = default_getaddrinfo
    pass