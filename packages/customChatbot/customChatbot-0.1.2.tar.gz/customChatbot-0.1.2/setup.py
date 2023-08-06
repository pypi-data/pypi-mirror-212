from setuptools import find_packages, setup

setup(
    name='customChatbot',
    packages=find_packages(include=['customGPT']),
    version='0.1.2',
    description='It is a custom GPT-3 bot that can be used to answer questions based on a custom dataset',
    author='Me',
    install_requires=["openai==0.27.2",
                      "pandas==1.5.3", "scikit-learn==1.2.2", "plotly==5.13.1", "matplotlib==3.7.1",
                      "scipy==1.10.1"
                      ],
)
