from setuptools import setup

setup(
    name='gptscannotation',
    version='0.1',
    description='Simple package for asking OpenAI GPT to do the scRNA-seq annotation based on the gene signatures',
    author='Ran Ran',
    author_email='andran@umich.edu',
    packages=['gptscannotation'],
    install_requires=[i.strip() for i in open("requirements.txt").readlines()],
)