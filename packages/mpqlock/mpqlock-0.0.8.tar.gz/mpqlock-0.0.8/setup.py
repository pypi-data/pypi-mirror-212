from setuptools import find_packages, setup
setup(
    name='mpqlock',
    version='0.0.8',
    description='lock for MPQ_code',
    author='MPQ',#作者
    author_email='miaopeiqi@163.com',
    url='https://github.com/miaopeiqi',
    #packages=find_packages(),
    packages=['mpqlock'],  #这里是所有代码所在的文件夹名称
    package_data={
    '':['*.pyd'],
    },
    install_requires=[''],
)
