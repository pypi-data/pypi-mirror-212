#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import mayan

PACKAGE_NAME = 'mayan-edms'
PACKAGE_DIR = 'mayan'

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)


def find_packages(directory):
    # Compile the list of packages available, because distutils doesn't have
    # an easy way to do this.
    packages, data_files = [], []
    root_dir = os.path.dirname(__file__)
    if root_dir != '':
        os.chdir(root_dir)

    for dirpath, dirnames, filenames in os.walk(directory):
        if not dirpath.startswith('mayan/media'):
            # Ignore dirnames that start with '.'
            if os.path.basename(dirpath).startswith('.'):
                continue
            if '__init__.py' in filenames:
                packages.append('.'.join(fullsplit(dirpath)))
            elif filenames:
                data_files.append(
                    [
                        dirpath, [
                            os.path.join(dirpath, filename) for filename in filenames
                        ]
                    ]
                )

    return packages


install_requires = """
django==3.2.19
CairoSVG==2.5.2
Pillow==9.4.0
PyPDF2==1.28.4
PyYAML==6.0
Whoosh==2.7.4
bleach==4.1.0
boto3==1.24.70
celery==5.2.7
dateparser==1.1.1
django-activity-stream==1.4.0
django-auth-ldap==4.0.0
django-celery-beat==2.2.1
django-cors-headers==3.10.0
django-formtools==2.3
django-mathfilters==1.0.0
django-model-utils==4.2.0
django-mptt==0.13.4
django-qsstats-magic==1.1.0
django-solo==2.0.0
django-storages==1.13.1
django-stronghold==0.4.0
django-widget-tweaks==1.4.12
djangorestframework==3.14.0
djangorestframework-recursive==0.1.2
drf-yasg==1.21.4
elasticsearch==7.17.1
elasticsearch-dsl==7.4.0
extract-msg==0.36.4
flanker==0.9.11
flex==6.14.1
furl==2.1.3
fusepy==3.0.1
gevent==22.10.2
graphviz==0.17
greenlet==2.0.2
gunicorn==20.1.0
importlib-metadata==5.0.0
jsonschema==4.4.0
mozilla-django-oidc==2.0.0
node-semver==0.8.1
pycountry==22.3.5
pycryptodome==3.10.4
pyotp==2.6.0
python-dateutil==2.8.2
python-magic==0.4.26
python_gnupg==0.4.8
pytz==2022.1
qrcode==7.3.1
requests==2.27.1
sentry-sdk==1.12.1
sh==1.14.2
swagger-spec-validator==2.7.4
whitenoise==6.0.0
""".split()

with open(file='README.rst') as file_object:
    readme = file_object.read()

with open(file='HISTORY.rst') as file_object:
    history = file_object.read()

setup(
    author='Roberto Rosario',
    author_email='roberto.rosario@mayan-edms.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Education',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Communications :: File Sharing',
    ],
    description=mayan.__description__,
    include_package_data=True,
    install_requires=install_requires,
    license='Apache 2.0',
    long_description=readme + '\n\n' + history,
    name=PACKAGE_NAME,
    packages=find_packages(PACKAGE_DIR),
    platforms=['any'],
    project_urls={
        'Documentation': 'https://docs.mayan-edms.com/',
        'Changelog': 'https://gitlab.com/mayan-edms/mayan-edms/-/blob/master/HISTORY.rst',
        'Bug Tracker': 'https://gitlab.com/mayan-edms/mayan-edms/-/issues',
        'Source Code': 'https://gitlab.com/mayan-edms/mayan-edms',
        'Support': 'https://www.mayan-edms.com/support/'
    },
    python_requires='>=3.9',
    scripts=['mayan/bin/mayan-edms.py'],
    url=mayan.__website__,
    version=mayan.__version__,
    zip_safe=False,
)
