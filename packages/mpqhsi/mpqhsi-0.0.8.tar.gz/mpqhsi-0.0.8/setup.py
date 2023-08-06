from setuptools import find_packages, setup
setup(
    name='mpqhsi',
    version='0.0.8',
    description='hsi for MPQ_code',
    author='MPQ',#作者
    author_email='miaopeiqi@163.com',
    url='https://github.com/miaopeiqi',
    #packages=find_packages(),
    packages=['mpqhsi'],  #这里是所有代码所在的文件夹名称
    package_data={
    '':['*.pyd'],
    },
    install_requires=['mpqlock','mpqcv'],
)
