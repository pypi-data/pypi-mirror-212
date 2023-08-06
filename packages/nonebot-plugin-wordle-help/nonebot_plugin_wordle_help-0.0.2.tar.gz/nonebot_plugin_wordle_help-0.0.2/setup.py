

from setuptools import find_packages, setup
name = 'nonebot_plugin_wordle_help'

setup(
    name=name,
    version='0.0.2',
    author="Special-Week",
    author_email='2385612749@qq.com',
    description="wordle小游戏工具",
    python_requires=">=3.8.0",
    packages=find_packages(),
    long_description="https://github.com/Special-Week/Hinata-Bot/tree/main/src/plugins/wordle_help",
    url="https://github.com/Special-Week/Hinata-Bot/tree/main/src/plugins/wordle_help",
    package_data={name: ['*']},
    # 设置依赖包
    install_requires=["nonebot2", "nonebot-adapter-onebot"],
)
