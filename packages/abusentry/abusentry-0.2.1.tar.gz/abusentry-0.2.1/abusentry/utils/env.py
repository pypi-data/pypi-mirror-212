import logging
import dotenv

# read env file as dict
def get_env(file_path):
    dotenv.load_dotenv(file_path)
    return os.environ

# write env file
def set_env(path, environ):
    try:
        with open(path, 'w') as f:
            for key, value in environ.items():
                f.write(f'{key}={value}\n')
    except:
        logging.error(f'Unable to write to {path}')

# api key object 
class ApiKey:
    def __init__(self, path, name):
        self.path = path
        self.name = name
        
    def _get(self):
        return get_env(self.path)
        
    def set(self, api_key):
        environ = self._get()
        environ[self.name] = api_key
        set_env(self.path, environ)

    def get(self):
        environ = self._get()
        return environ[self.name] if self.name in environ else None

    def remove(self):
        environ = self._get()
        if self.name in environ:
            del environ[self.name]
            set_env(self.path, environ)

    def exists(self):
        environ = self._get()
        return self.name in environ

    def __str__(self):
        return self.get()

    def __repr__(self):
        return self.get()
