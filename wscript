#! /usr/bin/env python
# encoding: utf-8

import os

APPNAME = 'cpprestsdk'
VERSION = '0.0.0'


def configure(conf):
    if conf.is_mkspec_platform('linux'):

        # if not conf.env['LIB_PTHREAD']:
        conf.check_cxx(lib='ssl')
        conf.check_cxx(lib='crypto')

def build(bld):
    bld.env.append_unique(
        'DEFINES_STEINWURF_VERSION',
        'STEINWURF_CPPRESTSDK_VERSION="{}"'.format(
            VERSION))

    cpprestsdk_path = bld.dependency_path('cpprestsdk-source')
    cpprestsdk_path = os.path.realpath(cpprestsdk_path)
    cpprestsdk_path = os.path.relpath(cpprestsdk_path, bld.root.abspath())

    include_path = os.path.join(cpprestsdk_path, "Release", "include")
    src_path = os.path.join(cpprestsdk_path, "Release", "src")
    export_includes = [
        include_path
    ]

    includes = [
        os.path.join(cpprestsdk_path, "Release", "src", "pch"),
        os.path.join(cpprestsdk_path, "Release", "src", "http", "client")
    ] + export_includes

    sources = [
        "{}/http/client/http_client.cpp".format(src_path),
        "{}/http/client/http_client_msg.cpp".format(src_path),
        "{}/http/client/x509_cert_utilities.cpp".format(src_path),
        "{}/http/common/http_helpers.cpp".format(src_path),
        "{}/http/common/http_msg.cpp".format(src_path),
        "{}/http/listener/http_listener.cpp".format(src_path),
        "{}/http/listener/http_listener_msg.cpp".format(src_path),
        "{}/http/listener/http_server_api.cpp".format(src_path),
        "{}/http/oauth/oauth1.cpp".format(src_path),
        "{}/http/oauth/oauth2.cpp".format(src_path),
        "{}/json/json.cpp".format(src_path),
        "{}/json/json_parsing.cpp".format(src_path),
        "{}/json/json_serialization.cpp".format(src_path),
        "{}/pplx/pplx.cpp".format(src_path),
        "{}/uri/uri.cpp".format(src_path),
        "{}/uri/uri_builder.cpp".format(src_path),
        "{}/utilities/asyncrt_utils.cpp".format(src_path),
        "{}/utilities/base64.cpp".format(src_path),
        "{}/utilities/web_utilities.cpp".format(src_path)
    ]

    websocketpp_includes = [
        bld.root.find_dir(
            os.path.join(cpprestsdk_path, "Release", "libs", "websocketpp"))]
    bld(name='websocketpp_includes',
        includes=websocketpp_includes,
        export_includes=websocketpp_includes)

    use = []
    defines = ["CPPREST_EXCLUDE_COMPRESSION=1"]
    if bld.is_mkspec_platform('mac') or bld.is_mkspec_platform('ios'):
        # WEBSOCKETS
        use += ['websocketpp_includes']
        sources += [
            "{}/websockets/client/ws_msg.cpp".format(src_path),
            "{}/websockets/client/ws_client.cpp".format(src_path),
            "{}/websockets/client/ws_client_wspp.cpp".format(src_path)
        ]

        # PPLX
        sources += [
            "{}/pplx/pplxapple.cpp".format(src_path),
            "{}/pplx/threadpool.cpp".format(src_path)
        ]

        # FILEIO
        sources += ["{}/streams/fileio_posix.cpp".format(src_path)]

        # HTTP_CLIENT
        # cpprest_find_boost()
        # cpprest_find_openssl()
        use += ['boost_system']
        defines += ["CPPREST_FORCE_HTTP_CLIENT_ASIO"]
        sources += ["{}/http/client/http_client_asio.cpp".format(src_path)]

        # HTTP_LISTENER
        # cpprest_find_boost()
        # cpprest_find_openssl()
        defines += ["CPPREST_FORCE_HTTP_LISTENER_ASIO"]
        sources += ["{}/http/listener/http_server_asio.cpp".format(src_path)]
    elif bld.is_mkspec_platform('linux') or bld.is_mkspec_platform('android'):
        # WEBSOCKETS
        use += ['websocketpp_includes']
        sources += [
            "{}/websockets/client/ws_msg.cpp".format(src_path),
            "{}/websockets/client/ws_client.cpp".format(src_path),
            "{}/websockets/client/ws_client_wspp.cpp".format(src_path)
        ]

        # PPLX
        sources += [
            "{}/pplx/pplxlinux.cpp".format(src_path),
            "{}/pplx/threadpool.cpp".format(src_path)
        ]

        # FILEIO
        sources += ["{}/streams/fileio_posix.cpp".format(src_path)]

        # HTTP_CLIENT
        # cpprest_find_openssl()
        use += [
            'boost_system',
            'boost_thread',
            'boost_filesystem',
            'boost_chrono',
            'boost_timer',
            'boost_includes',
            'SSL',
            'CRYPTO']

        defines += ["CPPREST_FORCE_HTTP_CLIENT_ASIO"]
        sources += ["{}/http/client/http_client_asio.cpp".format(src_path)]

        # HTTP_LISTENER
        # cpprest_find_boost()
        # cpprest_find_openssl()
        defines += ["CPPREST_FORCE_HTTP_LISTENER_ASIO"]
        sources += ["{}/http/listener/http_server_asio.cpp".format(src_path)]

    elif bld.is_mkspec_platform('windows'):
        # WEBSOCKETS
        use += ['websocketpp_includes']
        sources += [
            "{}/websockets/client/ws_msg.cpp".format(src_path),
            "{}/websockets/client/ws_client.cpp".format(src_path),
            "{}/websockets/client/ws_client_wspp.cpp".format(src_path)
        ]

        # PPLX
        sources += [
            "{}/pplx/pplxwin.cpp".format(src_path),
            "{}/pplx/threadpool.cpp".format(src_path)
        ]

        # FILEIO
        sources += ["{}/streams/fileio_win32.cpp".format(src_path)]

        # HTTP_CLIENT
        # Link with
        # httpapi.lib
        # Winhttp.lib
        sources += ["{}/http/client/http_client_winhttp.cpp".format(src_path)]

        # HTTP_LISTENER
        sources += ["{}/http/listener/http_server_httpsys.cpp".format(src_path)]

    bld.stlib(
        features='cxx',
        source=map(bld.root.find_node, sources),
        includes=map(bld.root.find_dir, includes),
        target='cpprestsdk',
        use=use,
        defines=defines,
        export_defines=defines,
        export_includes=map(bld.root.find_dir, export_includes)
    )
    if bld.is_toplevel():
        # Only build tests when executed from the top-level wscript,
        # i.e. not when included as a dependency
        bld.recurse('examples')
