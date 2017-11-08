from setuptools import setup

setup(name='official',
      version='1.0',
      description='flask App',
      author='Ben',
      author_email='ben@hopolite.com',
      url='http://www.python.org/sigs/distutils-sig/',
      install_requires=[
	    'Flask==0.10.1',
		'Flask-SQLAlchemy==2.1'
	  ]
     )
