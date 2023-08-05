from setuptools import setup, find_packages

setup(
    name="firegs",
    version="0.4",
    packages=find_packages(),
    install_requires=[
        'requests',
        'google-auth',
        'google-auth-httplib2',
        'google-auth-oauthlib',
        'google-api-python-client',
    ],
    entry_points={
        'console_scripts': [
            'firegs = firegs.script:main',
        ],
    },
    author="Android Dev Notes",
    author_email="awesomedevnotes@gmail.com",
    description="A tool to add app to Firebase project from the command line",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/androiddevnotes/firegs",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
