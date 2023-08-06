from setuptools import setup

setup(
    name='nexteraa-sedona',
    version='1.1.0',
    description='Nexteraa Glue jobs',
    author='Admin',
    packages=['nexteraa_glue_jobs'],
    install_requires=open('requirements.txt').readlines(),
)
