from setuptools import find_packages, setup

with open('README.md', 'r', encoding='utf-8') as fp:
    long_description = fp.read()

setup(name='minidevice',
      version='1.0.5',
      description='Android Auto Pypi',
      author='KateTseng',
      author_email='Kate.TsengK@outlook.com',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/NakanoSanku',
      license='MIT',
      keywords='game',
      project_urls={},
      packages=find_packages(),
      package_data={
          "minidevice": [
              "bin/*",
          ]
      },
      include_package_data=True,
      install_requires=['requests>=2.31.0',
                        'opencv-python>=4.7.0.72',
                        'uiautomator2>=2.16.23',
                        'pyminitouch>=0.3.3',
                        'urllib3'],
      python_requires='>=3'
      )
