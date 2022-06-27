from setuptools import setup
import re


version = ''
with open('aioEasyPillow/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

readme = ''
with open('README.md') as f:
    readme = f.read()

requirements = []
with open("requirements.txt") as f:
    requirements = f.read().splitlines()


setup(
    name='aioEasyPillow',
    version=version,
    description='Async working easy to use Pillow Library.',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Guddi',
    url='https://github.com/Guddi8/aioEasyPillow',
    packages=['aioEasyPill'],
    license='MIT',
    keywords=[
        'PIL', 'Pillow', 'async PIL', 'async Pillow', 'Easy PIL', 'Easy Pillow',
        'discord images', 'discord card', 'discord rank card'
    ],
    install_requires=requirements,
    python_requires=">=3.8, <4",
    include_package_data=True,
)