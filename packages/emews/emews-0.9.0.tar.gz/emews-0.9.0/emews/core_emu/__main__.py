"""eMews CORE network emulator tools."""
import argparse
import pathlib

from ruamel.yaml import YAML

from emews.base.config import get_root_path

HELP_TXT_SERVICE_GEN = "CORE service generator - generates a CORE service class for each eMews " \
                       "service configuration corresponding to the given eMews service name"

parser = argparse.ArgumentParser(description='eMews CORE network emulator tools')
subparsers = parser.add_subparsers(dest='tool_type', title='tool_type',
                                   help='specific tool to execute', required=True)

parser_service_gen = subparsers.add_parser('service_gen', help=HELP_TXT_SERVICE_GEN,
                                           description='CORE service generator')
parser_service_gen.add_argument("emews_service_name",
                                help="Name of eMews service to be used to generate CORE service(s) "
                                     "- one CORE service for each eMews service configuration")
parser_service_gen.add_argument("-o", "--overwrite", action="store_true",
                                help="Overwrite any existing CORE services of the same name(s)")

args = parser.parse_args()


def tools_main() -> None:
    """Main function for tools."""

    if args.tool_type == 'service_gen':
        print(f"{HELP_TXT_SERVICE_GEN}\n")
        tools_service_gen()


def tools_service_gen() -> None:
    """CORE service generator tool."""
    emews_root = pathlib.Path(get_root_path())
    core_service_path = emews_root.joinpath('core_emu', 'config_services').resolve()

    if not core_service_path.exists():
        print("Could not find directory to write CORE service.  Expected location: {core_service_path}")
        return

    service_name: str = args.emews_service_name

    emews_service_path = emews_root.joinpath('services', service_name).resolve()

    if not emews_service_path.exists():
        print(f"Could not find eMews service: {service_name}.  Expected location: {emews_service_path}")
        return

    default_config_fullpath = emews_service_path.joinpath(f"default.yml").resolve()

    if not default_config_fullpath.exists():
        print(f"Could not find default service configuration.  Expected location: {default_config_fullpath}")
        return

    with open(default_config_fullpath) as f_config:
        config_dct = YAML().load(f_config)

    service_display_name = config_dct.get('display_name')

    if service_display_name is None:
        service_display_name = service_name

    core_service_template = emews_root.joinpath('core_emu', "service_template.py").read_text()

    core_service_fullpath = core_service_path.joinpath(f"{service_name}.py")

    print(f"- Using eMews service: {service_display_name}")
    print(f"- Writing CORE service to: {core_service_fullpath.resolve()}")

    is_overwrite = args.overwrite
    if is_overwrite:
        print("-- Will overwrite if CORE service already exists")
    print("\n[Generating CORE service] ...")

    service_exists = core_service_fullpath.exists()

    if service_exists and not is_overwrite:
        print(f"! {core_service_fullpath.name} not written - CORE service already exists")
        return

    additional_configs = ''
    additional_configs_txt = ''
    for s_file in emews_service_path.iterdir():
        if s_file.is_dir() or s_file.suffix != '.yml' or s_file.name == 'default.yml':
            continue

        additional_configs = f'{additional_configs}", "{s_file.stem}'
        additional_configs_txt = f"{additional_configs_txt}\n   |- {s_file.name}"

    gen_service = core_service_template\
        .replace("EMEWS_SERVICE_NAME", service_name, 1)\
        .replace("EMEWS_SERVICE_DISPLAY_NAME", service_display_name, 1)\
        .replace("EMEWS_CLASS_NAME", service_name.capitalize(), 1)\
        .replace("EMEWS_SERVICE_CONFIGS", additional_configs, 1)

    with open(core_service_fullpath, "w") as f_service:
        f_service.write(gen_service)

    if service_exists:
        print(f"+ {core_service_fullpath.name} (existing service overwritten){additional_configs_txt}")
    else:
        print(f"+ {core_service_fullpath.name}{additional_configs_txt}")


tools_main()
