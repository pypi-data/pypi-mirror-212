from setuptools import find_packages, setup
import platform

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

if platform.system() == 'Linux':
    with open('requirements_linux.txt') as f:
        install_requirement = f.readlines()
elif platform.system() == 'Windows':
    with open('requirements_windows.txt') as f:
        install_requirement = f.readlines()

setup(
    name="armspeech",
    version="0.1.4",
    author="Varuzhan Baghdasaryan",
    author_email="varuzh2014@gmail.com",
    description="ArmSpeech is an offline Armenian speech recognition library (speech-to-text) and CLI tool based on Coqui STT (🐸STT) and trained on the ArmSpeech dataset.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    keywords=['speech recognition', 'speech-to-text', 'Armenian language'],
    url="https://github.com/Varuzhan97/armspeech",
    project_urls = {
        "Funding": 'https://donate.pypi.org',
        "Bug Tracker": "https://github.com/Varuzhan97/armspeech/issues"
    },
    packages=['armspeech'],
    package_dir={'armspeech':'src'},
    package_data={
        'armspeech': ['model/*.tflite'],
    },
    install_requires=install_requirement,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Customer Service',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Home Automation',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Multimedia :: Sound/Audio :: Analysis',
        'Topic :: Multimedia :: Sound/Audio :: Speech',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Human Machine Interfaces',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ],
    python_requires=">=3.6,<3.11",
    entry_points={
        "console_scripts": [
            "armspeech_stt_cli = armspeech.armspeech_stt_cli:main",
        ]
    }
)
