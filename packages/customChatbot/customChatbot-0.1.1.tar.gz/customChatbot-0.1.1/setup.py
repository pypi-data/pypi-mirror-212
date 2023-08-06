from setuptools import find_packages, setup
with open('requirements.txt') as f:
    required_packages = f.read().splitlines()
setup(
    name='customChatbot',
    packages=find_packages(include=['customGPT']),
    version='0.1.1',
    description='It is a custom GPT-3 bot that can be used to answer questions based on a custom dataset',
    author='Me',
    install_requires=required_packages,
)
