from ..cores.test_executor import TestExecutor
import unittest

def cmd_test(args, config):
    TestExecutor.args = args
    TestExecutor.config = config
    loader = unittest.TestLoader()
    tests = loader.discover('./tests', '*')
    testRunner = unittest.runner.TextTestRunner(verbosity=4)
    testRunner.run(tests)

