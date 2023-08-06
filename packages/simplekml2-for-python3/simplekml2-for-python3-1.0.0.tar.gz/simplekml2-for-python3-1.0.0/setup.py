from distutils.core import setup

setup(
    name = 'simplekml2-for-python3',
    packages = ['simplekml'],
    version = '1.0.0',
    description = 'A Simple KML creator',
    author='Daniel Fernandez',
    author_email='daf111@yahoo.com.ar',
    url='https://github.com/daf111/simplekml2',
    license='GNU General Public License',
    classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.0',
            'Programming Language :: Python :: 3.1',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.10',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Operating System :: OS Independent',
            'Topic :: Scientific/Engineering :: GIS',
            'Topic :: Software Development :: Libraries :: Python Modules'
          ],
    long_description="""
simplekml is a python package which enables you to generate KML with as little effort as possible.

Note: This project is a Fork from https://github.com/tjlang/simplekml but has support for Python 3.8 and superior.

At the time of making this package nothing was available (at least I could not find anything) that could create KML files easily. You needed a lot of bloated code to even create a simple point. This is understandable because the KML standard is quite extensive, but what if you just work with the simple elements of KML like Document, Folder, Point, LineString and Polygon? This package supports those elements and everything documented in the KML Reference. With simplekml creating a KML file containing a point as simple as::

    import simplekml
    kml = simplekml.Kml()
    kml.newpoint(name="Kirstenbosch", coords=[(18.432314,-33.988862)])
    kml.save("botanicalgarden.kml")

See the Documentation_ for usage and reference or visit the Homepage_ for more information.

.. _Documentation: http://simplekml.readthedocs.org
.. _Homepage: http://code.google.com/p/simplekml/

"""

)
