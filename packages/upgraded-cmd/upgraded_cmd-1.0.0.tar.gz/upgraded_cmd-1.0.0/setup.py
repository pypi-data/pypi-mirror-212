from setuptools import setup

setup(
    name='upgraded_cmd',
    packages=[
        'upgraded_cmd', 'upgraded_cmd.classes'
    ],
    version='1.0.0',
    description='Similar to built-in.cmd but allows tab completion in windows',
    author='Loïc Chevalier',
    long_description="This is a package",
    long_description_content_type='text/markdown'
)
