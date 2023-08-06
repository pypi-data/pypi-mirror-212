from . import utils

__all__ = (
    "ConfigLoadError",
    "FFmpegNotFound",
)

class ConfigLoadError(Exception):
    def __init__(self, e: Exception = None) -> None:
        super().__init__()
        self.e = e
    
    def __str__(self) -> str:
        if self.e:
            classname = utils.get_full_class_name(self.e)
            errormessage = str(self.e)
            return f"An error occurred while loading the configuration file: {classname}: {errormessage}"
        else:
            return "An error occurred while loading the configuration file."

class FFmpegNotFound(Exception):
    def __init__(self, path) -> None:
        super().__init__()
        self.path = path
    
    def __str__(self) -> str:
        return f"FFmpeg not found at location: '{self.path}'"