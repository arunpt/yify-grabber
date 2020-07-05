from setuptools import setup, find_packages

try:
    description = open("README.md").read()
except:
    description = ""

setup(
    name="yify-grabber",
    version="0.1",
    description="Command line tool for downloading subtitles from yify",
    python_requires='>=3.6',
    license="MIT",
    author="W4RR10R",
    author_email = 'arunptndpl@gmail.com',     
    url = 'https://github.com/CW4RR10R/yify-grabber',   
    keywords = ['yify', 'yts', 'subtitle', 'W4RR10R', 'yify grabber'],    
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4==4.9.1',
        'requests==2.23.0', 
      ],
    long_description=description,
    entry_points={
        'console_scripts': [
            'yify=yify:main'
        ]
    },
)