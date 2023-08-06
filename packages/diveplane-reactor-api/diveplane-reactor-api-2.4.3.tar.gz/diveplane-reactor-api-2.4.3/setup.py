import codecs
import os

from setuptools import find_namespace_packages, setup


def read(rel_path):
    """General file reader."""
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r', encoding='utf-8') as fp:
        return fp.read()


def get_version(rel_path):
    """Get and return the version."""
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


def parse_requirements(requirements):
    """Fix-up the requirements."""
    with open(requirements) as requirements_file:
        return [
            line.strip('\n') for line in requirements_file
            if line.strip(' \t\n') and not line.startswith('#')
        ]


setup(
    name='diveplane-reactor-api',
    version=get_version("diveplane/client/__init__.py"),
    description=('Diveplane Reactor and Scikit Estimator for the interpretable Machine Learning '
                 'and Artificial Intelligence API Diveplane.'),
    long_description="""# Diveplane Reactor\n\n""",
    long_description_content_type='text/markdown',
    author='Diveplane Corp',
    author_email='support@diveplane.com',
    license_files=('LICENSE.txt', ),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 3'
    ],
    keywords='machine learning artificial intelligence',
    install_requires=parse_requirements('requirements.in'),
    python_requires='>=3.8',
    url='https://www.diveplane.com',
    packages=find_namespace_packages(include=['diveplane.*']),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'verify_diveplane_install=diveplane.utilities.installation_verification:main',
            'diveplane_eula_helper=diveplane.utilities.eula_helper:main'
        ],
    },
)
