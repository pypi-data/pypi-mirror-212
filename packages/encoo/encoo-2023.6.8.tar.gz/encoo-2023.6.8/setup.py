from setuptools import find_packages, setup

setup(
    name='encoo',
    version='2023.6.8',
    packages=find_packages(),
    install_requires=['xlwt>=1.3.0', 'xlrd==1.2.0',
                      'configparser>=5.3.0', 'mail-parser>=3.15.0',
                      'extract-msg>=0.40.0'],
)


# 打包 python .\setup.py sdist bdist_wheel
# 上传 twine upload dist/*

# 安装 pip install encoo==2.0.0  -i https://www.pypi.org/simple/
