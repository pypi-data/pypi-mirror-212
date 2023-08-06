import os
import shutil
from setuptools import setup, find_packages
from setuptools.command.install import install


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        target_dir = os.path.expanduser('~/.local/bin')
        target_path = os.path.join(target_dir, "liveports")
        if(os.path.exists(target_path)):
            return  # already on path

        script_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'run.py')
        try:
            os.makedirs(target_dir)
        except FileExistsError:
            pass
        shutil.copy(script_path, target_path)
        os.chmod(target_path, 0o755)


with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='liveports',
    version='0.1.11',
    description='Give address to your localmachine',
    author='Abhinav',
    author_email='abhinavabcd@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "brotlipy>=0.7.0",
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'liveports = liveports.client:main',
        ],
    },
    cmdclass={
        'install': PostInstallCommand,
    }
)
