from setuptools import setup, find_packages
'''
setup(
   name="CDynamics",
   version="2.0.4",
   packages=find_packages(),
   install_requires=['numpy','matplotlib','sympy'],
)
'''

VERSION = '2.0.4'
DESCRIPTION = 'Plot Julia Sets Of Complex Valued Functions'
LONG_DESCRIPTION = 'A package that allows users to visualize julia sets of complex-valued holormorhphic self-maps defined on the Riemann sphere.'

setup(
    name="CDynamics",
    version=VERSION,
    author="Kanak Dhotre",
    author_email="dhotrekanak@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy','matplotlib','sympy'],
    keywords=['python', 'complex dynamics', 'julia set', 'filled julia sets'],
)
