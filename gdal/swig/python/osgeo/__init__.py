# __init__ for osgeo package.

# making the osgeo package version the same as the gdal version:
import sys
if sys.version_info >= (3, 8, 0) and sys.platform == 'win32':
    import os
    if 'USE_PATH_FOR_GDAL_PYTHON' in os.environ and 'PATH' in os.environ:
        for p in os.environ['PATH'].split(';'):
            if p:
                os.add_dll_directory(p)

if sys.version_info >= (2, 7, 0):
    def swig_import_helper():
        import importlib
        from os.path import dirname, basename
        import sys
        mname = basename(dirname(__file__)) + '._gdal'
        is_compiled = hasattr(sys, 'frozen')
        try:
            return importlib.import_module(mname)
        except ImportError as e:
            if is_compiled is False and sys.version_info >= (3, 8, 0) and sys.platform == 'win32':
                import os
                if not 'USE_PATH_FOR_GDAL_PYTHON' in os.environ:
                    msg = 'On Windows, with Python >= 3.8, DLLs are no longer imported from the PATH.\n'
                    msg += 'If gdalXXX.dll is in the PATH, then set the USE_PATH_FOR_GDAL_PYTHON=YES environment variable\n'
                    msg += 'to feed the PATH into os.add_dll_directory().'

                    import sys
                    import traceback
                    traceback_string = ''.join(traceback.format_exception(*sys.exc_info()))
                    raise ImportError(traceback_string + '\n' + msg)
            return importlib.import_module('_gdal')
    _gdal = swig_import_helper()
    del swig_import_helper
elif sys.version_info >= (2, 6, 0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        import sys
        fp = None
        is_compiled = hasattr(sys, 'frozen')
        try:
            fp, pathname, description = imp.find_module('_gdal', [dirname(__file__)])
        except ImportError:
            import _gdal
            return _gdal
        if fp is not None:
            try:
                _mod = imp.load_module('_gdal', fp, pathname, description)
            except ImportError as e:
                if is_compiled is False and sys.version_info >= (3, 8, 0) and sys.platform == 'win32':
                    import os
                    if not 'USE_PATH_FOR_GDAL_PYTHON' in os.environ:
                        msg = 'On Windows, with Python >= 3.8, DLLs are no longer imported from the PATH.\n'
                        msg += 'If gdalXXX.dll is in the PATH, then set the USE_PATH_FOR_GDAL_PYTHON=YES environment variable\n'
                        msg += 'to feed the PATH into os.add_dll_directory().'

                        import sys
                        import traceback
                        traceback_string = ''.join(traceback.format_exception(*sys.exc_info()))
                        raise ImportError(traceback_string + '\n' + msg)
                raise
            finally:
                fp.close()
            return _mod
    _gdal = swig_import_helper()
    del swig_import_helper
else:
    import _gdal

__version__ = _gdal.__version__ = _gdal.VersionInfo("RELEASE_NAME")
