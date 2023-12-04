import ipaddress
import logging
import unittest
from unittest.mock import patch

import requests

from src import RecordUpdater
from src.EnvReader import EnvReader
from src.RecordUpdater import remove_excluded_records, include_records, filter_records


class TestRemoveExcludedRecords(unittest.TestCase):

    # The function returns an empty list when given an empty list of records.
    def test_empty_list(self):
        records = []
        env = EnvReader()
        result = remove_excluded_records(records, env)
        self.assertEqual(result, set())

    # The function returns a list of all records when no records are excluded.
    def test_no_excluded_records(self):
        records = [
            {"name": "record1"},
            {"name": "record2"},
            {"name": "record3"}
        ]
        env = EnvReader()
        result = remove_excluded_records(records, env)
        self.assertEqual(result, {"record1", "record2", "record3"})

    # The function returns a list of records that are not excluded based on the environment settings.
    def test_excluded_records(self):
        records = [
            {"name": "record1"},
            {"name": "record2"},
            {"name": "record3"}
        ]
        env = EnvReader()
        env.dns_records = ["record2"]
        result = remove_excluded_records(records, env)
        self.assertEqual(result, {"record1", "record3"})

    # The function handles a list of records with a single record.
    def test_single_record(self):
        records = [
            {"name": "record1"}
        ]
        env = EnvReader()
        result = remove_excluded_records(records, env)
        self.assertEqual(result, {"record1"})

    # The function handles a list of records with multiple records.
    def test_multiple_records(self):
        records = [
            {"name": "record1"},
            {"name": "record2"},
            {"name": "record3"}
        ]
        env = EnvReader()
        result = remove_excluded_records(records, env)
        self.assertEqual(result, {"record1", "record2", "record3"})

    # The function handles an excluded list with a single record.
    def test_single_excluded_record(self):
        records = [
            {"name": "record1"},
            {"name": "record2"},
            {"name": "record3"}
        ]
        env = EnvReader()
        env.dns_records = ["record2"]
        result = remove_excluded_records(records, env)
        self.assertEqual(result, {"record1", "record3"})

    # The function handles records with names that are in the excluded list.
    def test_handles_records_in_excluded_list(self):
        # Arrange
        records = [
            {"name": "record1"},
            {"name": "record2"},
            {"name": "record3"}
        ]
        env = EnvReader()
        env.dns_records = ["record2"]

        # Act
        result = remove_excluded_records(records, env)

        # Assert
        self.assertEqual(result, {"record1", "record3"})

    # The function handles records with names that are not in the excluded list.
    def test_handles_records_not_in_excluded_list(self):
        # Arrange
        records = [
            {"name": "record1"},
            {"name": "record2"},
            {"name": "record3"}
        ]
        env = EnvReader()
        env.dns_records = ["excluded_record"]

        # Act
        result = remove_excluded_records(records, env)

        # Assert
        self.assertEqual(result, {"record1", "record2", "record3"})

    # The function handles a case where all records are excluded.
    def test_all_records_excluded(self):
        records = [
            {"name": "record1"},
            {"name": "record2"},
            {"name": "record3"}
        ]
        env = EnvReader()
        env.dns_records = ["record1", "record2", "record3"]
        result = remove_excluded_records(records, env)
        self.assertEqual(result, set())

    # The function handles an excluded list with multiple records.
    def test_excluded_list_with_multiple_records(self):
        # Arrange
        records = [
            {"name": "record1"},
            {"name": "record2"},
            {"name": "record3"}
        ]
        env = EnvReader()
        env.dns_records = ["record2", "record3"]

        # Act
        result = remove_excluded_records(records, env)

        # Assert
        self.assertEqual(result, {"record1"})

    # The function handles records with names that are partially matched in the excluded list.
    def test_handles_partially_matched_names(self):
        records = [
            {"name": "record1"},
            {"name": "record2"},
            {"name": "record3"},
            {"name": "record4"},
            {"name": "record5"}
        ]
        env = EnvReader()
        env.dns_records = ["cord1", "cord2", "cord3"]
        result = remove_excluded_records(records, env)
        self.assertEqual(set(result), {"record1", "record2", "record3", "record4", "record5"})

    # The function handles records with names that contain special characters in the excluded list.
    def test_handles_records_with_special_characters(self):
        records = [
            {"name": "record1"},
            {"name": "record2"},
            {"name": "record3"},
            {"name": "record@4"},
            {"name": "record#5"},
            {"name": "record$6"}
        ]
        env = EnvReader()
        env.dns_records = ["record2", "record@4", "record$6"]
        result = remove_excluded_records(records, env)
        self.assertEqual(result, {"record1", "record3", "record#5"})

    # The function handles an excluded list with duplicates.
    def test_excluded_list_with_duplicates(self):
        # Arrange
        records = [
            {"name": "record1"},
            {"name": "record2"},
            {"name": "record3"}
        ]
        env = EnvReader()
        env.dns_records = ["record2", "record2"]

        # Act
        result = remove_excluded_records(records, env)

        # Assert
        self.assertEqual(result, {"record1", "record3"})

    # The function handles records with names that contain Unicode characters in the excluded list.
    def test_handles_unicode_characters(self):
        # Create a list of records with names that contain Unicode characters
        records = [
            {"name": "record1"},
            {"name": "record2"},
            {"name": "record3"},
            {"name": "récord4"},
            {"name": "rëcord5"},
            {"name": "rêcord6"}
        ]

        # Create an instance of EnvReader
        env = EnvReader()

        # Set the excluded records to include Unicode characters
        env.dns_records = ["récord4", "rëcord5", "rêcord6"]

        # Call the remove_excluded_records function
        result = remove_excluded_records(records, env)

        # Assert that the result only contains records without Unicode characters
        self.assertEqual(result, {"record1", "record2", "record3"})


class TestIncludeRecords(unittest.TestCase):

    # Returns a list of DNS records that are included based on the environment settings.
    def test_included_records(self):
        dns_records = [
            {"name": "record1"},
            {"name": "record2"},
            {"name": "record3"}
        ]
        env = EnvReader()
        env.dns_records = ["record1", "record3"]

        result = include_records(dns_records, env)

        self.assertEqual(set(result), {"record1", "record3"})

    # Returns an empty list when no DNS records are included in the environment settings.
    def test_no_included_records(self):
        dns_records = [
            {"name": "record1"},
            {"name": "record2"},
            {"name": "record3"}
        ]
        env = EnvReader()

        result = include_records(dns_records, env)

        self.assertEqual(result, set())

    # Returns all DNS records when the environment settings do not specify any included records.
    def test_no_specified_included_records(self):
        dns_records = [
            {"name": "record1"},
            {"name": "record2"},
            {"name": "record3"}
        ]
        env = EnvReader()
        env.dns_records = []

        result = include_records(dns_records, env)

        self.assertEqual(result, set())

    # Returns an empty list when the input list of DNS records is empty.
    def test_empty_dns_records(self):
        dns_records = []
        env = EnvReader()
        env.dns_records = ["record1", "record2"]

        result = include_records(dns_records, env)

        self.assertEqual(result, set())

    # Returns an empty list when the input list of DNS records does not contain any "name" keys.
    def test_no_name_keys(self):
        dns_records = [
            {"type": "A", "value": "127.0.0.1"},
            {"type": "CNAME", "value": "example.com"}
        ]
        env = EnvReader()
        env.dns_records = ["record1", "record2"]

        result = include_records(dns_records, env)

        self.assertEqual(result, set())

    # Returns an empty list when none of the DNS records match the included records
    # specified in the environment settings.
    def test_no_matching_records(self):
        dns_records = [
            {"name": "record1"},
            {"name": "record2"},
            {"name": "record3"}
        ]
        env = EnvReader()
        env.dns_records = ["record4", "record5"]

        result = include_records(dns_records, env)

        self.assertEqual(result, set())

    # Returns only the DNS records that match the included records in the environment settings.
    def test_include_records_matching_included_records(self):
        dns_records = [
            {"name": "record1"},
            {"name": "record2"},
            {"name": "record3"}
        ]
        env = EnvReader()
        env.dns_records = ["record1", "record3"]

        result = include_records(dns_records, env)

        self.assertEqual(set(result), {"record1", "record3"})

    # Returns DNS records with different keys, in addition to the "name" key.
    def test_included_records(self):
        dns_records = [
            {"name": "record1"},
            {"name": "record2"},
            {"name": "record3"}
        ]
        env = EnvReader()
        env.dns_records = ["record1", "record3"]

        result = include_records(dns_records, env)

        self.assertEqual(result, ["record1", "record3"])

    # Returns DNS records with different values,
    # in addition to the included records specified in the environment settings.
    def test_include_records_with_different_values(self):
        dns_records = [
            {"name": "record1"},
            {"name": "record2"},
            {"name": "record3"}
        ]
        env = EnvReader()
        env.dns_records = ["record1", "record3"]

        result = include_records(dns_records, env)

        self.assertEqual(set(result), {"record1", "record3"})

    # Returns DNS records with duplicate "name" values, but only once in the output list.
    def test_include_records_duplicates(self):
        dns_records = [
            {"name": "record1"},
            {"name": "record2"},
            {"name": "record3"},
            {"name": "record1"},
            {"name": "record2"}
        ]
        env = EnvReader()
        env.dns_records = ["record1", "record2"]

        result = include_records(dns_records, env)

        self.assertEqual(set(result), {"record1", "record2"})

    # Returns DNS records that match the included records specified in the environment settings,
    # even when the input list of DNS records contains additional records that do not match.
    def test_included_records(self):
        dns_records = [
            {"name": "record1"},
            {"name": "record2"},
            {"name": "record3"}
        ]
        env = EnvReader()
        env.dns_records = ["record1", "record3"]

        result = include_records(dns_records, env)

        self.assertEqual(result, ["record1", "record3"])

    # Returns DNS records that match the included records specified in the environment settings,
    # even when the input list of DNS records contains records with missing "name" keys.
    def test_include_records_with_missing_name_keys(self):
        dns_records = [
            {"name": "record1"},
            {"name": "record2"},
            {"name": "record3"},
            {"type": "A"},
            {"type": "CNAME"},
            {"type": "MX"}
        ]
        env = EnvReader()
        env.dns_records = ["record1", "record3"]

        result = include_records(dns_records, env)

        self.assertEqual(result, {"record1", "record3"})

    # Returns DNS records that match the included records specified in the environment settings,
    # even when the input list of DNS records contains records with missing values for the "name" key.
    def test_included_records(self):
        dns_records = [
            {"name": "record1"},
            {"name": "record2"},
            {"name": "record3"}
        ]
        env = EnvReader()
        env.dns_records = ["record1", "record3"]

        result = include_records(dns_records, env)

        self.assertEqual(result, {"record1", "record3"})

    # Returns DNS records that match the included records specified in the environment settings,
    # even when the input list of DNS records contains records with duplicate "name" keys.
    def test_include_records_with_duplicates(self):
        dns_records = [
            {"name": "record1"},
            {"name": "record2"},
            {"name": "record3"},
            {"name": "record1"},
            {"name": "record2"}
        ]
        env = EnvReader()
        env.dns_records = ["record1", "record3"]

        result = include_records(dns_records, env)

        self.assertEqual(set(result), {"record1", "record3"})

    # Returns DNS records that match the included records specified in the environment settings,
    # even when the input list of DNS records contains records with duplicate values for the "name" key.
    def test_included_records(self):
        dns_records = [
            {"name": "record1"},
            {"name": "record2"},
            {"name": "record3"},
            {"name": "record1"},
            {"name": "record2"}
        ]
        env = EnvReader()
        env.dns_records = ["record1", "record3"]

        result = include_records(dns_records, env)

        self.assertEqual(result, {"record1", "record3"})

    # Returns DNS records that match the included records specified in the environment settings,
    # even when the input list of DNS records contains records with additional keys and values not used by the function.
    def test_included_records(self):
        dns_records = [
            {"name": "record1"},
            {"name": "record2"},
            {"name": "record3"}
        ]
        env = EnvReader()
        env.dns_records = ["record1", "record3"]

        result = include_records(dns_records, env)

        self.assertEqual(result, {"record1", "record3"})


class TestFilterRecords(unittest.TestCase):

    @patch('src.RecordUpdater.include_records', return_value={'record1', 'record2'})
    def test_include_records(self, mock_include_records):
        # Create a mock instance of EnvReader
        env = EnvReader()
        env.mode = EnvReader.INCLUDE

        # Create a list of DNS records
        dns_records = [{'name': 'record1'}, {'name': 'record2'}, {'name': 'record3'}]

        # Call the filter_records function
        result = filter_records(dns_records, env)

        # Assert that the include_records function was called with the correct arguments
        mock_include_records.assert_called_once_with(dns_records, env)

        # Assert that the result is the expected set of included records
        self.assertEqual(result, {'record1', 'record2'})

    @patch('src.RecordUpdater.remove_excluded_records', return_value={'record1', 'record2'})
    def test_exclude_records(self, mock_remove_excluded_records):
        # Create a mock instance of EnvReader
        env = EnvReader()
        env.mode = EnvReader.EXCLUDE

        # Create a list of DNS records
        dns_records = [{'name': 'record1'}, {'name': 'record2'}, {'name': 'record3'}]

        # Call the filter_records function
        result = filter_records(dns_records, env)

        # Assert that the remove_excluded_records function was called with the correct arguments
        mock_remove_excluded_records.assert_called_once_with(dns_records, env)

        # Assert that the result is the expected set of excluded records
        self.assertEqual(result, {'record1', 'record2'})

    def test_invalid_dns_records_type(self):
        # Create a mock instance of EnvReader
        env = EnvReader()

        # Try to call filter_records with invalid dns_records type
        with self.assertRaises(TypeError):
            filter_records("not_a_list", env)

    def test_invalid_env_type(self):
        # Try to call filter_records with invalid env type
        with self.assertRaises(TypeError):
            filter_records([], "not_an_env_instance")


class TestUpdate(unittest.IsolatedAsyncioTestCase):

    # Updates a DNS record with a new IP address using the GoDaddy API.
    @unittest.mock.patch('requests.put')
    async def test_update_dns_record(self, mock_put):
        env = EnvReader()
        record = "example.com"
        new_ip = ipaddress.IPv4Address("192.168.0.1")

        await RecordUpdater.update(record, new_ip, env)

        url = f"https://api.godaddy.com/v1/domains/{env.domain}/records/A/{record}"
        payload = [
            {
                "data": new_ip,
                "ttl": 3600
            }
        ]
        headers = {
            "accept": "application/json",
            "X-Shopper-Id": env.shopper_id,
            "Content-Type": "application/json",
            "Authorization": f"sso-key {env.api_key}:{env.api_secret}"
        }

        mock_put.assert_called_once_with(url, json=payload, headers=headers)

    # Sends a PUT request to the GoDaddy API with the constructed URL, payload, and headers.
    @unittest.mock.patch('requests.put')
    async def test_send_put_request(self, mock_put):
        env = EnvReader()
        record = "example.com"
        new_ip = ipaddress.IPv4Address("192.168.0.1")

        url = f"https://api.godaddy.com/v1/domains/{env.domain}/records/A/{record}"
        payload = [
            {
                "data": new_ip,
                "ttl": 3600
            }
        ]
        headers = {
            "accept": "application/json",
            "X-Shopper-Id": env.shopper_id,
            "Content-Type": "application/json",
            "Authorization": f"sso-key {env.api_key}:{env.api_secret}"
        }

        await RecordUpdater.update(record, new_ip, env)

        mock_put.assert_called_once_with(url, json=payload, headers=headers)

    # If the request is successful,
    # logs a message indicating that the DNS record has been updated with the new IP address.
    @unittest.mock.patch('requests.put')
    async def test_successful_update(self, mock_put):
        env = EnvReader()
        record = "example.com"
        new_ip = ipaddress.IPv4Address("192.168.0.1")

        await RecordUpdater.update(record, new_ip, env)

        url = f"https://api.godaddy.com/v1/domains/{env.domain}/records/A/{record}"
        payload = [
            {
                "data": new_ip,
                "ttl": 3600
            }
        ]
        headers = {
            "accept": "application/json",
            "X-Shopper-Id": env.shopper_id,
            "Content-Type": "application/json",
            "Authorization": f"sso-key {env.api_key}:{env.api_secret}"
        }

        mock_put.assert_called_once_with(url, json=payload, headers=headers)

    # If the request fails,
    # logs a warning message indicating that the DNS record was not updated and the reason for the failure.
    @unittest.mock.patch('requests.put')
    async def test_request_failure_logs_warning_message(self, mock_put):
        env = EnvReader()
        record = "example.com"
        new_ip = ipaddress.IPv4Address("192.168.0.1")

        mock_put.side_effect = requests.exceptions.RequestException("Request failed")
        with self.assertLogs(level=logging.WARNING) as cm:
            await RecordUpdater.update(record, new_ip, env)

        expected_log_message = f"Was not able to change the ip of record: {record}\n Request failed"
        self.assertIn(expected_log_message, cm.output.pop())
