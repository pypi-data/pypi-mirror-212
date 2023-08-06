from setuptools import setup, find_packages

if __name__ == "__main__":
    setup(
        name='Audio Similarity',
        version='1.0',
        author='Mark Stent',
        author_email='mark@markstent.co.za',
        description='Audio similarity metrics for audio tasks',
        packages=find_packages(),
        install_requires=[
            'numpy',
            'librosa',
            'pystoi',
            'Pillow',
            'matplotlib',
            'soundfile',
            'tqdm'
        ],
    )
