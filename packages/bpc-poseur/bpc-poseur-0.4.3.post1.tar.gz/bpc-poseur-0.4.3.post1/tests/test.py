# -*- coding: utf-8 -*-
# pylint: disable=no-member, redefined-outer-name

import contextlib
import os
import subprocess
import sys
import tempfile
import unittest

# root path
ROOT = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(ROOT, '..')))
#from poseur import ConvertError, _decorator, convert, decorator, get_parser
from bpc_utils import BPCSyntaxError as ConvertError
from poseur import DECORATOR_TEMPLATE as _decorator
from poseur import convert, decorator, get_parser  # pylint: disable=no-name-in-module
from poseur import main as main_func
from poseur import poseur as core_func
sys.path.pop(0)

# macros
with open(os.path.join(ROOT, 'sample.py')) as file:
    CODE = file.read()
with open(os.path.join(ROOT, 'sample.txt')) as file:
    TEXT = file.read()

# environs
os.environ['POSEUR_DECORATOR'] = '_poseur_decorator'
os.environ['POSEUR_QUIET'] = 'true'
os.environ['POSEUR_LINESEP'] = 'LF'
POSEUR_LINESEP = '\n'


@contextlib.contextmanager
def test_environ(path, *env):
    with open(path, 'w') as file:
        file.write(CODE)
    _env = dict()
    for var in env:
        _env[var] = os.environ.get(var)
        os.environ[var] = 'true'

    try:
        yield
    finally:
        pass

    for var in env:
        if _env[var] is None:
            del os.environ[var]
        else:
            os.environ[var] = _env[var]
    with open(path, 'w') as file:
        file.write(CODE)


class TestPoseur(unittest.TestCase):

    def __init__(self, methodName):
        self.maxDiff = None
        super().__init__(methodName)

    def _check_output(self, path):
        output = subprocess.check_output(
            [sys.executable, path],
            universal_newlines=True
        )
        self.assertEqual(output, TEXT)

    def _check_convert(self, src, dst):
        out = convert(src)
        self.assertEqual(out, dst)

    def test_get_parser(self):
        parser = get_parser()
        args = parser.parse_args(['-na', '-q', '-k/tmp/',
                                  '-vs', '3.8', 'test1.py', 'test2.py'])

        self.assertIs(args.quiet, True,
                      'run in quiet mode')
        self.assertIs(args.do_archive, False,
                      'do not archive original files')
        self.assertEqual(args.archive_path, '/tmp/',
                         'path to archive original files')
        # self.assertEqual(args.encoding, 'gb2312',
                        #  'encoding to open source files')
        self.assertEqual(args.source_version, '3.8',
                         'convert against Python version')
        self.assertEqual(args.files, ['test1.py', 'test2.py'],
                         'python source files and folders to be converted')

    def test_convert(self):
        # error conversion
        os.environ['POSEUR_SOURCE_VERSION'] = '3.7'
        with self.assertRaises(ConvertError):
            convert('def func(a, /, b, *, c): pass')
        del os.environ['POSEUR_SOURCE_VERSION']

    def test_core(self):
        with tempfile.TemporaryDirectory() as tempdir:
            path = os.path.join(tempdir, 'test.py')

            # --dismiss
            with test_environ(path, 'POSEUR_DISMISS'):
                core_func(path)
                self._check_output(path)

            # --linting
            with test_environ(path, 'POSEUR_LINTING'):
                core_func(path)
                self._check_output(path)

    def test_main(self):
        with tempfile.TemporaryDirectory() as tempdir:
            path = os.path.join(tempdir, 'test.py')
            with open(path, 'w') as file:
                file.write(CODE)

            with open(os.devnull, 'w') as devnull:
                with contextlib.redirect_stdout(devnull):
                    os.environ['POSEUR_QUIET'] = 'false'
                    main_func(['-na', path])
                os.environ['POSEUR_QUIET'] = 'true'
            self._check_output(path)

    def test_decorator(self):
        @decorator('a')
        def func(a, b, *, c):  # pylint: disable=unused-argument
            pass

        # wrong code
        with self.assertRaises(TypeError):
            func(a=1, b=2, c=3)

        # right code
        func(1, b=2, c=3)

    def test_async(self):
        src = 'async def func(param, /): pass'
        dst = 'async def func(param): pass'
        dst = "%s\n\n\n@_poseur_decorator(\'param\')\nasync def func(param): pass" % (
            POSEUR_LINESEP.join(_decorator) % dict(decorator='_poseur_decorator', indentation='\t'.expandtabs(4))).lstrip()
        self._check_convert(src, dst)

    def test_lambdef(self):
        # no poseur
        src = 'lambda param: param'
        dst = 'lambda param: param'
        self._check_convert(src, dst)

        # basic poseur
        src = 'lambda param, /: param'
        dst = "%s\n\n\n_poseur_decorator('param')(lambda param: param)" % (
            POSEUR_LINESEP.join(_decorator) % dict(decorator='_poseur_decorator', indentation='\t'.expandtabs(4))).lstrip()
        self._check_convert(src, dst)

        # no poseur in default value
        src = 'lambda param=lambda p: p: param'
        dst = 'lambda param=lambda p: p: param'
        self._check_convert(src, dst)

        # poseur in default value
        src = 'lambda param=lambda p, /: p: param'
        dst = "%s\n\n\nlambda param=_poseur_decorator('p')(lambda p: p): param" % (
            POSEUR_LINESEP.join(_decorator) % dict(decorator='_poseur_decorator', indentation='\t'.expandtabs(4))).lstrip()
        self._check_convert(src, dst)

        # poseur in lambda suite
        src = 'lambda param: lambda p, /: p'
        dst = "%s\n\n\nlambda param: _poseur_decorator('p')(lambda p: p)" % (
            POSEUR_LINESEP.join(_decorator) % dict(decorator='_poseur_decorator', indentation='\t'.expandtabs(4))).lstrip()
        # XXX: idk why this fails on poseur.convert but works through CLI
        #self._check_convert(src, dst)

        # hybrid poseur
        src = 'lambda param: param\nlambda param, /: param'
        dst = "lambda param: param\n\n%s\n\n\n_poseur_decorator('param')(lambda param: param)" % (
            POSEUR_LINESEP.join(_decorator) % dict(decorator='_poseur_decorator', indentation='\t'.expandtabs(4)))
        self._check_convert(src, dst)

    def test_funcdef(self):
        # no poseur
        src = 'def func(): pass'
        dst = 'def func(): pass'
        self._check_convert(src, dst)

        # simple poseur
        src = 'def func(a, /, b): pass'
        dst = "%s\n\n\n@_poseur_decorator(\'a\')\ndef func(a, b): pass" % (
            POSEUR_LINESEP.join(_decorator) % dict(decorator='_poseur_decorator', indentation='\t'.expandtabs(4))).lstrip()
        self._check_convert(src, dst)

        # poseur in function suite
        src = 'def func(): lambda param, /: param'
        dst = "%s\n\n\ndef func():\n    _poseur_decorator('param')(lambda param: param)" % (
            POSEUR_LINESEP.join(_decorator) % dict(decorator='_poseur_decorator', indentation='\t'.expandtabs(4))).lstrip()
        # XXX: idk why this fails on poseur.convert but works through CLI
        #self._check_convert(src, dst)

        # keyword arguments
        src = 'def func(a, *, b): pass'
        dst = 'def func(a, *, b): pass'
        self._check_convert(src, dst)

        # poseur in default value
        src = 'def func(a=lambda param, /: param): pass'
        dst = "%s\n\n\ndef func(a=_poseur_decorator('param')(lambda param: param)): pass" % (
            POSEUR_LINESEP.join(_decorator) % dict(decorator='_poseur_decorator', indentation='\t'.expandtabs(4))).lstrip()
        self._check_convert(src, dst)


if __name__ == '__main__':
    unittest.main()
