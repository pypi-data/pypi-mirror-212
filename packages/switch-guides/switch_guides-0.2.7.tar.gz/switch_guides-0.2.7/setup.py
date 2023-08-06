# -------------------------------------------------------------------------
# Copyright (c) Switch Automation Pty Ltd. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

# Import required functions
from setuptools import setup, find_packages

# Call setup function
setup(
    author="Switch Automation Pty Ltd.",
    description="A package for building Platform Guides in Switch Automation Platform.",
    long_description=open('README.md', 'r').read() + '\n\n' + open('HISTORY.md', 'r').read(),
    long_description_content_type='text/markdown',
    license='MIT License',
    name="switch_guides",
    version="0.2.7",
    packages=find_packages(
        include=["switch_guides", "switch_guides.*"],
        exclude=["switch_guides.tests", "switch_guides.tests.*"]
    ),
    install_requires=['switch-api','pydantic>=1.0.0,<2.0.0'],
    python_requires=">=3.8.0",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        "License :: OSI Approved :: MIT License",
        'Intended Audience :: Other Audience',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Natural Language :: English',
    ]
)
