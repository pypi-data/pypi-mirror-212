"""
Time-frequency analysis through Stockwell transform.

:copyright:
    2021-2023 Claudio Satriano <satriano@ipgp.fr>

:license:
    GNU General Public License v3.0 or later.
    (https://www.gnu.org/licenses/gpl-3.0.html)
"""


# start delvewheel patch
def _delvewheel_init_patch_1_3_7():
    import os
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'stockwell.libs'))
    if os.path.isdir(libs_dir):
        os.add_dll_directory(libs_dir)


_delvewheel_init_patch_1_3_7()
del _delvewheel_init_patch_1_3_7
# end delvewheel patch


from ._version import get_versions
__version__ = get_versions()['version']
del get_versions