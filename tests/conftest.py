import sys
from os.path import abspath, dirname, join

package_path = abspath(join(dirname(dirname(__file__)), "src"))
sys.path.insert(0, package_path)
