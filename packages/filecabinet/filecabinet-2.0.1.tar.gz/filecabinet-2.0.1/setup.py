import setuptools

from filecabinet import version


with open('README.md', encoding='utf-8') as fd:
    long_description = fd.read()

with open('LICENSE', encoding='utf-8') as fd:
    licensetext = fd.read()


setuptools.setup(name='filecabinet',
      version=version.VERSION,
      description="A local, offline document archive",
      long_description=long_description,
      long_description_content_type='text/markdown',
      url="https://vonshednob.cc/filecabinet",
      author="R",
      author_email="dev+filecabinet-this-is-spam@vonshednob.cc",
      license=licensetext,
      entry_points={'console_scripts': ['filecabinet=filecabinet.main:run']},
      packages=['filecabinet',
                ],
      package_data={},
      data_files=[],
      install_requires=['pyyaml', 'pypdf', 'Pillow', 'metaindex >= 2.2.2'],
      python_requires='>=3.7',
      classifiers=['Development Status :: 3 - Alpha',
                   'License :: OSI Approved :: BSD License',
                   'Programming Language :: Python :: 3',
                   ])
