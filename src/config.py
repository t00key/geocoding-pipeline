# This file is used to load the configuration file and store it in a class
import toml
from pathlib import Path

class Config:
    def __init__(self, filename):
        self.config = toml.load(filename)
        self.filename = filename
        # load header
        self.url = self.config["header"]["url"]
        self.name = self.config["header"]["name"]
        # load col mappings
        self.address = self.config["cols_mapping"]["address"]
        self.city = self.config["cols_mapping"]["city"]
        self.state = self.config["cols_mapping"]["state"]
        self.zip = self.config["cols_mapping"]["zip"]
        
    
    def __str__(self):
        return f"Config({self.filename})"

    def __repr__(self):
        return f"Config({self.config})"

    def data_path(self):
        # use pathlib to get absolute directory of project root and then down to ./data, if it doesn't exist create it
        p = Path(__file__).resolve().parents[1] / "data"
        if not p.exists():
            p.mkdir()
        return p