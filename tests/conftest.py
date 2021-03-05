import sys
from os.path import abspath, dirname, join

package_path = abspath(join(dirname(dirname(__file__)), "problem_function_signature"))
sys.path.insert(0, package_path)
