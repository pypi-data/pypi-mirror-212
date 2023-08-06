import mock
import unittest
import os
from zappa_packer.zappa import Zappa

class TestZappa(unittest.TestCase):
    def setUp(self):
        self.sleep_patch = mock.patch("time.sleep", return_value=None)
        # Tests expect us-east-1.
        # If the user has set a different region in env variables, we set it aside for now and use us-east-1
        self.users_current_region_name = os.environ.get("AWS_DEFAULT_REGION", None)
        os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
        if not os.environ.get("PLACEBO_MODE") == "record":
            self.sleep_patch.start()

    def tearDown(self):
        if not os.environ.get("PLACEBO_MODE") == "record":
            self.sleep_patch.stop()
        del os.environ["AWS_DEFAULT_REGION"]
        if self.users_current_region_name is not None:
            # Give the user their AWS region back, we're done testing with us-east-1.
            os.environ["AWS_DEFAULT_REGION"] = self.users_current_region_name

    ##
    # Sanity Tests
    ##

    def test_test(self):
        self.assertTrue(True)

    def test_create_lambda_package(self):
        # mock the pkg_resources.WorkingSet() to include a known package in lambda_packages so that the code
        # for zipping pre-compiled packages gets called
        mock_installed_packages = {"psycopg2": "2.6.1"}
        with mock.patch(
            "zappa.zappa.Zappa.get_installed_packages",
            return_value=mock_installed_packages,
        ):
            z = Zappa(runtime="python3.7")
            path = z.create_lambda_zip(handler_file=os.path.realpath(__file__))
            self.assertTrue(os.path.isfile(path))
            os.remove(path)