
from setuptools import find_packages, setup
from typing import List

def get_requirements(file_path: str = 'requirements.txt') -> List[str]:
    """
    Reads the requirements.txt file and returns a list of valid packages
    suitable for install_requires in setup().
    
    It ignores:
        - editable installs (-e .)
        - comments (# ...)
        - empty lines
    """
    requirements = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('-e') and not line.startswith('#'):
                    requirements.append(line)
    except FileNotFoundError:
        print(f"Warning: {file_path} not found. install_requires will be empty.")
    return requirements

setup(
    name="network_security",           # Change to your project name
    version="0.0.1",
    description="A network security project",
    author="amisha",
    author_email="khichariyaamisha@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements(),  # <-- safe list of packages
    include_package_data=True,            # include files like data, configs, etc.
)
