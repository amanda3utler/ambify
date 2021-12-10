from setuptools import setup, find_packages


setuptools.setup(
    name="ambify",
    version="0.1",
    author="Amanda Butler",
    author_email="amanda.butler@yale.edu",
    description='An all-in-one ambient music player',
    packages=["ambify"],
    package_data={'ambify': ['outputs/sounds/*.mp3']},
    install_requires=[
        'numpy>=1.17',
        'scipy',
        'spotipy',
        'pandas',
        'requests',
        'streamlit',
        'pygame',
        'Pillow',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Spotify Users",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
