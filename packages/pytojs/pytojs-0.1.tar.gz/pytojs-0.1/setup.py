try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

long_desc = '''Translates JavaScript to Python code. pytojs is able to translate and execute virtually any JavaScript code.

pytojs is written in pure python and does not have any dependencies. Basically an implementation of JavaScript core in pure python.


    import pytojs

    f = pytojs.eval_js( "function $(name) {return name.length}" )

    f("Hello world")

    # returns 11

Now also supports ECMA 6 through pytojs.eval_js6(js6_code)!

More examples at: https://github.com/PiotrDabkowski/pytojs
'''



# rm -rf dist build && python3 setup.py sdist bdist_wheel
# twine upload dist/*
setup(
    name='pytojs',
    version='0.1',

    packages=['pytojs', 'pytojs.utils', 'pytojs.prototypes', 'pytojs.translators',
              'pytojs.constructors', 'pytojs.host', 'pytojs.es6', 'pytojs.internals',
              'pytojs.internals.prototypes', 'pytojs.internals.constructors', 'pytojs.py_node_modules'],
    url='https://github.com/jo-project/pytojs',
    install_requires = ['tzlocal>=1.2', 'six>=1.10', 'pyjsparser>=2.5.1'],
    license='MIT',
    author='jo-project',
    author_email='jo.project.0911@gmail.com',
    description='JavaScript to Python Translator & JavaScript interpreter written in 100% pure Python. (Fork from js2py)',
    long_description=long_desc
)
