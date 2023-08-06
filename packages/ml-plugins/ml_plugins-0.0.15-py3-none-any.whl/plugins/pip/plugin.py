import functools
import subprocess
import sys

from typing import Callable, Dict
from metaflow.includefile import IncludeFile 
from metaflow.exception import MetaflowException

def write_to_disk(data: str, filename: str) -> None:
    with open(filename, mode='w+') as f:
        f.write(data)

def pip() -> Callable:
    def decorator(function: Callable) -> Callable:
        @functools.wraps(function)
        def wrapper(self, *args) -> Callable:
            write_to_disk(self.requirements, "requirements.txt")
            subprocess.run([sys.executable, '-m' 'pip', 'install', 'requirements.txt'])
            return function(self, *args)
        return wrapper
    return decorator

def packages(packages: Dict[str, str]) -> Callable:
    def decorator(function: Callable) -> Callable:
        @functools.wraps(function)
        def wrapper(self, *args) -> Callable:
            dependencies = list(map(lambda x: f"{x[0]}=={x[1]}", packages.items()))           
            requirements = "\n".join(dependencies)
            write_to_disk(requirements, "requirements.txt")
            subprocess.run([sys.executable, '-m' 'pip', 'install', 'requirements.txt'])
            return function(self, *args)
        return wrapper
    return decorator
 