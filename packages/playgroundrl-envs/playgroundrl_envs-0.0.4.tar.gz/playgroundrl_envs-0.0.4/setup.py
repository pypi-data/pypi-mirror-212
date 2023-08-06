from setuptools import setup, find_packages

setup(
   name='playgroundrl_envs',
   version='0.0.4',
   author='Rayan Krishnan',
   # packages=['playgroundrl_envs', 'playgroundrl_envs.games', 'playgroundrl_envs.games.go', 'playgroundrl_envs.games.codenames', 'playgroundrl_envs.games.catan'],
   packages=find_packages(),
   package_dir={'':'src'},
   scripts=[],
   url='http://pypi.python.org/pypi/playgroundrl_envs/',
   description='The environments hosted on Playground RL',
   # long_description=open('README.txt').read(),
   install_requires=[
        'attrs==22.2.0',
        'cattrs==22.2.0',
   ],
)
