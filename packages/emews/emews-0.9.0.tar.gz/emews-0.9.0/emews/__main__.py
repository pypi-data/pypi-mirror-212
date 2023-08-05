import argparse

from emews import __version__
from emews.base.node import node_init

# TODO: test launching eMews with python -OO
# Note: log messages still use %-style, due to JIT processing of them (important to prevent overhead
# from messages which will be ignored, such as DEBUG messages when INFO is the lowest level.)

parser = argparse.ArgumentParser(description='eMews network node loader')
parser.add_argument("-c", "--node_config", help="path of the node-specific configuration file")
parser.add_argument("-n", "--node_name", help="name given to this node, for example a host name")
parser.add_argument('--version', action='version', version=f'eMews {__version__}')
subparsers = parser.add_subparsers(dest='node_type', title='node_type',
                                   help='network node type to start as', required=True)

parser_host = subparsers.add_parser('host', help='host node', description='host node')
parser_host.add_argument("--hub_address", help="IPv4 address of the hub node")
parser_host.add_argument("--hub_port", type=int, help="port of the hub node")

parser_hub = subparsers.add_parser('hub', help='hub node', description='hub node')
parser_hub.add_argument("--scn_autostart", action="store_true",
                        help="start experiment scenario automatically, using values from system configuration")

parser_servspawn = subparsers.add_parser('servspawn', help='service spawner host process node',
                                         description='service spawner host process node')
parser_servspawn.add_argument("service_name", help="name of service to load on host node")
parser_servspawn.add_argument("service_configuration",
                              help="name of the service's configuration file")

parser_hubmon = subparsers.add_parser('monitor', help='hub monitor node',
                                      description='hub monitor node')
parser_hubmon.add_argument("--hub_address", help="IPv4 address of the hub node")
parser_hubmon.add_argument("--hub_port", type=int, help="port of the hub node")
parser_hubmon.add_argument("--log_local", action="store_true",
                           help="enables logging output from the monitor node itself")

parser_hubconsole = subparsers.add_parser('console', help='hub console node',
                                          description='hub console node')
parser_hubconsole.add_argument("--hub_address", help="IPv4 address of the hub node")
parser_hubconsole.add_argument("--hub_port", type=int, help="port of the hub node")
parser_hubconsole.add_argument("--log_local", action="store_true",
                               help="enables logging output from the console node itself")
args = parser.parse_args()

node_init(args).run()
