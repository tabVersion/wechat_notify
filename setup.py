from setuptools import setup

setup(name="wechat-notify",
    description="notify you on Wechat when certain task is completed",
    version="1.0",
    author="Tab_version",
    author_email="tabvision@bupt.edu.cn",
    packages=['wechat_notify'],
    install_requires=[
          'requests',
      ],
    entry_points = {
        'console_scripts': ['notify=wechat_notify.notify:main'],
    },
    include_package_data=True,
)
