import sys
import functools
import subprocess

from typing import Dict

def write_to_disk(data: str, filename: str) -> None:
    with open(filename, mode='w+') as f:
        f.write(data)

def pip():
    def decorator(function):
        @functools.wraps(function)
        def wrapper(self, *args):
            write_to_disk(self.requirements, "requirements.txt")
            subprocess.run([sys.executable, '-m' 'pip', 'install', "-r" 'requirements.txt'])
            return function(self, *args)
        return wrapper
    return decorator
 
def extra(libraries: Dict[str, str]):
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            for library, version in libraries.items():
                print('Pip Install:', library, version)
                subprocess.run([sys.executable, '-m', 'pip', 'install', '--quiet', library + '==' + version])
            return function(*args, **kwargs)

        return wrapper

    return decorator