import functools
from metaflow.includefile import IncludeFile 
from metaflow.exception import MetaflowException



def write_to_disk(data: str):
    with open('pyproject.toml', mode='w+') as f:
        f.write(data)

def poetry():
    def decorator(function):
        @functools.wraps(function)
        def wrapper(self, *args):
            import subprocess
            import sys
            write_to_disk(self.data)
            subprocess.run([sys.executable, '-m', 'poetry', 'install', '-C', 'pyproject.toml'])
            return function(self, *args)
        return wrapper
    return decorator

