from setuptools import setup

setup(
    name='insituTEM',
    version='0.1.1',
    author='Meng Li',
    description='A package of tools for processing in situ TEM data',
    packages=['insituTEM'],
    install_requires=[
        'tifffile',
        'moviepy',
        'tqdm',
        'numpy',
        'cv2',
        'scipy',
        'PIL',
        'matplotlib.pyplot'
    ],
)