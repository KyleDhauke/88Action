import os
import json
import shutil
from enum import Enum

class Config:
    settingsPath = None
    configPath = None
    data = None
    
    def __init__(self) -> None:
        # Store the system path to the settings folder.
        currlocation = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        self.settingsPath = os.path.abspath(os.path.join(currlocation, '..', 'settings'))
        
        # Check if the config file exists.
        if self.config_exists():
            self.configPath = os.path.join(self.settingsPath, 'config.json')
            with open(self.configPath) as f:
                self.data = json.load(f)
        elif self.default_exists():
            self.clone_default()
            self.configPath = os.path.join(self.settingsPath, 'config.json')
            with open(self.configPath) as f:
                self.data = json.load(f)
        else:
            raise FileNotFoundError("Default configuration file was not found.")  
        return
    
    def restore_default(self):
        if self.config_exists():
             os.remove(os.path.join(self.settingsPath, 'config.json'))
        
        if self.default_exists():
            self.clone_default()
            self.configPath = os.path.join(self.settingsPath, 'config.json')
            with open(self.configPath) as f:
                self.data = json.load(f)
        else:
            raise FileNotFoundError("Default configuration file was not found.")  
        return
    
    
    def config_exists(self):
        return os.path.isfile(os.path.join(self.settingsPath, 'config.json'))
    
    
    def default_exists(self):
        return os.path.isfile(os.path.join(self.settingsPath, 'default.json'))
    
    
    def clone_default(self):
        shutil.copyfile(os.path.join(self.settingsPath, 'default.json'),
                os.path.join(self.settingsPath, "config.json"))
        return
    
    def get_auto_header(self):
        return AutoHeaders(self.data['configuration']['importCSV']['AutoHeaders'])
    
    
    
class AutoHeaders(Enum):
    CLEAN = 'CLEAN'
    AUTO = 'AUTO'
    NONE = None