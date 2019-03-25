from setuptools import setup
from setuptools import find_packages

setup(
    name='hanging-merge-requests',
    version='1.0.0-rc3',
    packages=find_packages(include=('hmr*', )),
    include_package_data=True,
    install_requires=open('requirements.txt').read(),
    zip_safe=False,
    entry_points = {
        'console_scripts': ['send-notifications=hmr.scripts.send_notifications:main'],
    },
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
)
