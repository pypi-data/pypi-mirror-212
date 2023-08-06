import luddite
import argparse
import traceback

from . import (
    __name__ as name,
    __description__ as description,
    __copyright__ as copyright,
    __version__ as version
)
from . import color, utils 
from .start import main as start
from .config import get_config

def main():
    parser = argparse.ArgumentParser(
        prog = name,
        description = description,
        epilog = "Example: sqdconvert -in input_file.mp4 -out output_file.mp3"
    )

    parser.add_argument("-in", "--input",
                        help="input file for conversion")
    parser.add_argument("-out", "--output",
                        help="output file")
    parser.add_argument("-i", "--interactive",
                        action="store_true", help="start an interactive conversion")
    parser.add_argument("-v", "--verbose",
                        action="store_true", help="print more output")
    parser.add_argument("-c", "--config",
                        help="use a different config file")
    parser.add_argument("-V", "--version",
                        action="version", version=name+" "+version)
    parser.add_argument("-l", "--license",
                        action="version", version=copyright+" - MIT License. For more information see: https://opensource.org/license/mit/",
                        help="show program's license and exit")

    try:
        try:
            config = get_config()
        except Exception as e:
            args = parser.parse_args()
            raise e

        args = parser.parse_args()
        if args.config is not None:
            config = get_config(args.config)
    
        start(args, config)
    
    except Exception as e:
        if args.verbose:
            traceback.print_exc()
        print(f"{color.bright_red}💥 An error occured! {color.bright_yellow}{utils.get_full_class_name(e)}{color.bright_red}: {str(e)}{color.reset}")
    
    try:
        new_version = luddite.get_version_pypi(name)
    except:
        new_version = None
    
    try:
        config
    except:
        try_config = False
    else:
        try_config = True
    
    if new_version and version != new_version and try_config and config.update_notification:
        print()
        print(f"{color.bright_green}New version for {color.bright_yellow}{name}{color.bright_green} is available.{color.reset}")
        print(f"{color.bright_blue}{version} {color.bright_green}>> {color.bright_blue}{new_version}{color.reset}")
        print(f"{color.bright_white}Use {color.bright_red}pip install -U {name}{color.bright_white} to update!{color.reset}")

if __name__ == "__main__":
    main()