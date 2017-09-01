from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='raven',
      version='0.1',
      description='CLI tools to manage your Spotify music library.',
      keywords='music, cli, Spotify, api',
      url='http://github.com/bhavika/raven',
      author='Bhavika Tekwani',
      author_email='bhavicka@protonmail.com',
      license='MIT',
      packages=['raven'],
      install_requires=[
          'python-dotenv', 'spotipy', 'fire',
          'requests', 'flake8', 'tqdm'
      ],
      zip_safe=False)
