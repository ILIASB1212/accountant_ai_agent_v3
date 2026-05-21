from setuptools import setup, find_packages

def get_requirements( ) :
    with open("requirements.txt", "r") as f:
        return f.read().splitlines()
    

setup(
    name="accountant_ai_agents",
    version="3.0",
    author="ILIAS",
    packages=find_packages(),
    install_requires=get_requirements(),
)