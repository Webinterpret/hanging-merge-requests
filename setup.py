import os
from setuptools import setup
from setuptools import find_packages


def read_file(filename):
    """Open and a file, read it and return its contents."""
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path) as f:
        return f.read()


setup(
    name='hanging-merge-requests',
    version='1.0.2',
    packages=find_packages(include=('hmr*', )),
    include_package_data=True,
    description='Emojiful daily summaries of open merge requests directly in your Slack',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/Webinterpret/hanging-merge-requests',
    install_requires=open('requirements.txt').read(),
    zip_safe=False,
    entry_points={
        'console_scripts': ['send-notifications=hmr.scripts.send_notifications:main'],
    },
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python',
        'Topic :: Communications :: Chat',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development',
    ],
)
