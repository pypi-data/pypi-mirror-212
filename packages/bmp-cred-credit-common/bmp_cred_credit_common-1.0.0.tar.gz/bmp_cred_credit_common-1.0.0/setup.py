from setuptools import setup

default_requirements = [
    'boto3==1.26.146',
    'pandas==2.0.2',
    'parameterized==0.9.0',
    'pytz==2023.3',
    'setuptools==65.5.0',
    'validate_docbr==1.10.0'
]

requirements = default_requirements

setup(
    name='bmp_cred_credit_common',
    version='1.0.0',
    author='O estagiário',
    author_email='estagiario@bmp.com.br',
    description='Qualquer problema é culpa do estagiário.',
    packages=['bmp_cred_credit_common'],
    install_requires=requirements,
)
