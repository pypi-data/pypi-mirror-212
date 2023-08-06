

from setuptools import find_packages, setup
name = 'nonebot_plugin_impact'

setup(
    name=name,
    version='0.0.09',
    author="Special-Week",
    author_email='2385612749@qq.com',
    description="encapsulate logger",
    python_requires=">=3.8.0",
    packages=find_packages(),
    long_description="淫趴插件",
    url="https://github.com/Special-Week/nonebot_plugin_impact",

    # 设置依赖包
    install_requires=["pillow", "nonebot2", "nonebot-adapter-onebot"],
)
