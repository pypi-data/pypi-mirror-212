import os
import re
from setuptools import setup, find_packages


def get_long_description():
    with open(os.path.join(RELATIVE_PWD, 'PYDOC.md'), encoding='utf-8') as f:
        return f.read()

def get_requirements(path):
    """Load requirements from a pip requirements file."""
    reqs = []
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in [l.strip() for l in f.read().splitlines() if l]:
                if line.startswith('#'):
                    continue
                else:
                    if '#' in line:
                        line = re.sub(r'[ \t]+#.*$', '', line, re.M)
                        
                    reqs.append(line)
    return reqs

def find_scripts(path):
    scripts = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if not file.endswith('.py'):
                continue
                
            file_path = os.path.join(root, file)
            
            with open(file_path, 'r') as f:
                lines = f.readlines()
                if len(lines) <= 0:
                    continue
                    
                # scripts that have shebang and a main func
                if re.match(r'^#!.*python', lines[0]) and any(re.search(r'^def +?main\(.*\):', line, re.M) for line in lines):
                    script_name = os.path.splitext(file)[0]
                    scripts.append((script_name, file_path))
                    
    return scripts

def build_entry_points(scripts):
    current_dir = os.path.dirname(__file__)
    entries = []
    for script_name, script_path in scripts:
        relative_path = os.path.relpath(script_path, current_dir)
        
        module_path = os.path.normpath(relative_path.replace('.py', '')).replace(os.sep, '.')
        
        # 'name=module:attrs [extras]'
        point = f"{script_name}={module_path}:main"
        entries.append(point)
        
    return entries

RELATIVE_PWD = os.path.dirname(os.path.realpath(__file__))

setup(
    name='abusentry',
    version='0.2.3',
    author='Kevin Haas',
    author_email="kevin.haas96@gmail.com",
    license='GPLv3+',
    description='A set of tools for security auditing websites and domains.',
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url='https://github.com/xransum/abusentry/',
    py_modules=[
        'abusentry',
    ],
    packages=find_packages(),
    install_requires=[
        # additional requirements can be added here
        *get_requirements(os.path.join(RELATIVE_PWD, 'deps', 'requirements.txt')),
    ],
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Operating System :: POSIX",
        "Operating System :: Unix",
    ],
    entry_points = {
        'console_scripts': [
            *build_entry_points(find_scripts(os.path.join(RELATIVE_PWD, 'abusentry'))),
        ],
    },
)
