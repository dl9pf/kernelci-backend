# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest

import utils
import utils.errors


class TestBaseUtils(unittest.TestCase):

    def test_is_hidden(self):
        self.assertTrue(utils.is_hidden(".hidden"))
        self.assertFalse(utils.is_hidden("hidden"))

    def test_is_lab_dir(self):
        self.assertTrue(utils.is_lab_dir("lab-foo"))
        self.assertFalse(utils.is_lab_dir("foo"))

    def test_extrapolate_defconfig_full_non_valid(self):
        kconfig_fragments = "foo-CONFIG.bar"
        defconfig = "defconfig"

        self.assertEqual(
            defconfig,
            utils._extrapolate_defconfig_full_from_kconfig(
                kconfig_fragments, defconfig)
        )

    def test_extrapolate_defconfig_full_valid(self):
        kconfig_fragments = "frag-CONFIG=y.config"
        defconfig = "defconfig"

        expected = "defconfig+CONFIG=y"
        self.assertEqual(
            expected,
            utils._extrapolate_defconfig_full_from_kconfig(
                kconfig_fragments, defconfig)
        )

    def test_extrapolate_defconfig_full_from_dir_non_valid(self):
        dirname = "foo-defconfig+FRAGMENTS"
        self.assertIsNone(
            utils._extrapolate_defconfig_full_from_dirname(dirname))

    def test_extrapolate_defconfig_full_from_dir_valid(self):
        dirname = "arm-defconfig+FRAGMENTS"
        self.assertEqual(
            "defconfig+FRAGMENTS",
            utils._extrapolate_defconfig_full_from_dirname(dirname))

        dirname = "arm64-defconfig+FRAGMENTS"
        self.assertEqual(
            "defconfig+FRAGMENTS",
            utils._extrapolate_defconfig_full_from_dirname(dirname))

        dirname = "x86-defconfig+FRAGMENTS"
        self.assertEqual(
            "defconfig+FRAGMENTS",
            utils._extrapolate_defconfig_full_from_dirname(dirname))

    def test_error_add_no_error(self):
        errors = {}
        expected = {}

        utils.errors.add_error(errors, None, None)
        self.assertDictEqual(expected, errors)

    def test_error_add_new_error(self):
        errors = {}
        expected = {500: ["Error message"]}

        utils.errors.add_error(errors, 500, "Error message")
        self.assertDictEqual(expected, errors)

    def test_error_add_another_error(self):
        errors = {
            500: ["First message"]
        }
        expected = {
            500: ["First message", "Second message"]
        }
        utils.errors.add_error(errors, 500, "Second message")
        self.assertDictEqual(expected, errors)

    def test_error_update_none(self):
        errors = {
            500: ["A message"]
        }
        expected = {
            500: ["A message"]
        }

        utils.errors.update_errors(errors, {})
        self.assertDictEqual(expected, errors)
        utils.errors.update_errors(errors, None)
        self.assertDictEqual(expected, errors)

    def test_error_update_new(self):
        errors = {}
        expected = {
            500: ["Updated message"]
        }

        utils.errors.update_errors(errors, {500: ["Updated message"]})
        self.assertDictEqual(expected, errors)

    def test_error_update_another(self):
        errors = {
            500: ["Old message"]
        }
        expected = {
            500: ["Old message", "New message"]
        }

        utils.errors.update_errors(errors, {500: ["New message"]})
        self.assertDictEqual(expected, errors)
