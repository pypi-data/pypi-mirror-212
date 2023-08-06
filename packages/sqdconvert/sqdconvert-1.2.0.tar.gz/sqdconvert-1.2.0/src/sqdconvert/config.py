import os
import json
from datetime import datetime

from . import color, errors
from .utils import fs

default_config_path = os.path.normpath(os.path.expandvars(os.path.expanduser("~/.sqdconfig/sqdconvert/")))
os.makedirs(default_config_path, exist_ok=True)

class Config:
    def __init__(self, config) -> None:
        try:
            if os.path.exists(config["ffmpeg_path"]):
                if os.path.isfile(config["ffmpeg_path"]):
                    ffmpeg_path = config["ffmpeg_path"]
                
                else:
                    _p = os.path.join(config["ffmpeg_path"], "ffmpeg.exe")
                
                    if os.path.exists(_p):
                        ffmpeg_path = _p
                
                    else:
                        raise errors.FFmpegNotFound(config["ffmpeg_path"])
            else:
                raise errors.FFmpegNotFound(config["ffmpeg_path"])
        
            _ffpath = ffmpeg_path.split(fs)
            self.ffmpeg_path = []
            for x in _ffpath:
                if " " in x:
                    x = '"'+x+'"'
                self.ffmpeg_path.append(x)
            
            self.ffmpeg_path = fs.join(self.ffmpeg_path)
            self.update_notification = config["update_notification"]
            
        except Exception as e:
            raise errors.ConfigLoadError(e)

def make_default_config():
    t = datetime.now()
    return """{
    "ffmpeg_path": "path to ffmpeg",
    "update_notification": true
}
""", f"""// Default Config -- Generated on {t.day}/{t.month}/{t.year}
""""""{
    "ffmpeg_path": "./ffmpeg", // path to ffmpeg
    "update_notification": true // whether to turn on notification for updates or not
}
"""

def get_config(path: str = default_config_path):
    os.makedirs(path, exist_ok=True)
    config_path = os.path.join(path, "config.json")

    if not os.path.exists(config_path):
        print(f"{color.bright_white}WARNING: {color.reset}{color.bright_yellow}Could not find the config file. Generating a new one.{color.reset}")
        
        default_config, example_default_config = make_default_config()
        
        with open(os.path.join(default_config_path, "config.json"), "w") as configfile:
            configfile.write(default_config)
        
        with open(os.path.join(default_config_path, "example_config.json"), "w") as exampleconfigfile:
            exampleconfigfile.write(example_default_config)

        print(f"{color.bright_white}INFO: {color.reset}{color.bright_green}Successfully generated config file at '{color.bright_yellow}{default_config_path}{color.bright_green}'.{color.reset}")
        print()

    with open(config_path) as cf:
        config = json.load(cf)
    
    return Config(config)