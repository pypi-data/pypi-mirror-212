from setuptools import setup

readme = open("./README.md", "r")

setup(
    name='titulosuagrm',
    packages=['titulosuagrm'],  # this must be the same as the name above
    version='0.1',
    description='Caso de estudio sobre extraccion de datos generados por javascript.',
    long_description=readme.read(),
    long_description_content_type='text/markdown',
    author='Giovanni Vega',
    # use the URL to the github repo
    url='https://github.com/zxvega/consulta-uagrm-titulo',
    install_requires=['requests', 'webdriver-manager', 'selenium', 'pandas'],
    keywords=[],
    classifiers=[ ],
    license='MIT',
    include_package_data=True   
)