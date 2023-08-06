# functions for setting and getting the abusentry global config
import os

GLOBAL_CONFIG_PATH = os.path.join(os.path.expanduser('~'), '.abusentryrc')

class configs:
    """Global variables."""
    def __init__(self):
        """Initialize global variables."""
        self.interactive = False
        self.verbose = False
        self.json = False
        self.quiet = False
        self.urlscan_api_key = None
        self.virustotal_api_key = None
        self.load()
    
    def load(self):
        """Load global config."""
        if not os.path.exists(GLOBAL_CONFIG_PATH):
            return
        
        with open(GLOBAL_CONFIG_PATH, 'r') as f:
            for line in f.readlines():
                if line.startswith('#'):
                    continue
                
                key, value = line.strip().split('=')
                key = key.strip().lower()
                value = value.strip()
                
                if key in self.__dict__:
                    if value == "True":
                        value = True
                    elif value == "False":
                        value = False
                    elif value == "None":
                        value = None
                    elif value.isdigit():
                        value = int(value)
                    elif value.replace('.', '', 1).isdigit():
                        value = float(value)
                    elif value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    else:
                        pass
                    
                    self.__dict__[key] = value
        return
    
    def save(self):
        """Save global config."""
        with open(GLOBAL_CONFIG_PATH, 'w') as f:
            for key, value in self.__dict__.items():
                key = key.upper()
                f.write(f"{key}={value}\n")
        return
    
    def set(self, key, value):
        """Set global config."""
        if key in self.__dict__:
            self.__dict__[key] = value
            self.save()
        return
    
    def get(self, key):
        """Get global config."""
        if key in self.__dict__:
            return self.__dict__[key]
        return None
    
    def __str__(self):
        """String representation of global config."""
        return str(self.__dict__)
    
    def __repr__(self):
        """Representation of global config."""
        return str(self.__dict__)
    
    def __getitem__(self, key):
        """Get item from global config."""
        return self.get(key)
    
    def __setitem__(self, key, value):
        """Set item in global config."""
        self.set(key, value)
        
    def __contains__(self, key):
        """Check if global config contains key."""
        return key in self.__dict__
    
    def __iter__(self):
        """Iterate over global config."""
        return iter(self.__dict__)
    
    def __len__(self):
        """Length of global config."""
        return len(self.__dict__)
# end configs
