from setuptools import setup, find_packages
import os

version = '0.2'

setup(name='upfront.pagetracker',
      version=version,
      description="Package to log requests from various views",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='',
      author_email='',
      url='https://github.com/upfrontsystems/upfront.pagetracker',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['upfront'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.app.dexterity',
          'plone.behavior',
          'plone.app.registry',          
          'plone.namedfile [blobs]',
          'collective.topictree',
          'upfront.classlist',
          'upfront.assessmentitem',
          'upfront.assessment',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      extras_require = {
          'test': [
                  'plone.app.testing',
              ]
      },
      # The next two lines may be deleted after you no longer need
      # addcontent support from paster and before you distribute
      # your package.
      setup_requires=["PasteScript"],
      paster_plugins = ["ZopeSkel"],

      )
