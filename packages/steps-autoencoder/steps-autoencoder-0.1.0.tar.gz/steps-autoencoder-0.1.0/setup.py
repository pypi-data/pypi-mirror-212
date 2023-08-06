from setuptools import setup, find_packages
import pkg_resources
import re
import os

setup(
    name='steps-autoencoder', 
    version='0.1.0',  
    url='https://github.com/Hekler-Designing-Health-Lab/steps-autoencoder',
    author='Junghwan Park',
    author_email='jup014@ucsd.edu',
    description='An Autoencoder for Steps Data',
    packages=find_packages(),
    install_requires=['numpy', 'pandas', 'tensorflow', 'mlflow', 'neptune']
)


from setuptools import setup, find_packages
import pkg_resources
import re
import os

# package name and initial version
PACKAGE_NAME = 'steps-autoencoder'
INITIAL_VERSION = '0.1.0'

# file path to manage version
version_file_path = os.path.join(os.path.dirname(__file__), 'VERSION')

# if there is no VERSION file, create one and write initial version
if not os.path.isfile(version_file_path):
    with open(version_file_path, 'w') as version_file:
        version_file.write(INITIAL_VERSION)

# read version from VERSION file
with open(version_file_path, 'r') as version_file:
    version = version_file.read().strip()

# e.g. 0.1.0 -> 0.1.1
version_parts = version.split('.')
version_parts[-1] = str(int(version_parts[-1]) + 1)
new_version = '.'.join(version_parts)

# write new version to VERSION file
with open(version_file_path, 'w') as version_file:
    version_file.write(new_version)

# find all imported packages from all .py files
imported_packages = []
for root, _, files in os.walk('.'):
    for file in files:
        if file.endswith('.py'):
            with open(os.path.join(root, file)) as f:
                imported_packages.extend(
                    re.findall(r'^import (\S+)|^from (\S+)', f.read(), re.MULTILINE)
                )
imported_packages = list(set([pkg[0] or pkg[1] for pkg in imported_packages]))

# list up all packages in working set
install_requires = [
    dist.project_name for dist in pkg_resources.working_set
    if dist.project_name in imported_packages and dist.project_name != PACKAGE_NAME
]

setup(
    name=PACKAGE_NAME,
    version=new_version,
    url='https://github.com/Hekler-Designing-Health-Lab/steps-autoencoder',
    author='Junghwan Park',
    author_email='jup014@ucsd.edu',
    description='An Autoencoder for Steps Data',
    packages=find_packages(),
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: Apache License 2.0',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)