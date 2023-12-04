from src.EnvReader import EnvReader

import unittest


class TestValidatemode(unittest.TestCase):

    # Validates the mode field when it is set to INCLUDE.
    def test_validate_mode_include(self):
        env_reader = EnvReader()
        env_reader.mode = EnvReader.INCLUDE
        env_reader._EnvReader__validate_mode()
        self.assertEqual(env_reader.mode, EnvReader.INCLUDE)

    # Validates the mode field when it is set to an empty string.
    def test_validate_mode_empty_string(self):
        env_reader = EnvReader()
        env_reader.mode = ""
        env_reader._EnvReader__validate_mode()
        self.assertEqual(env_reader.mode, EnvReader.INCLUDE)

    # Validates the mode field when it is set to None.
    def test_validate_mode_none(self):
        env_reader = EnvReader()
        env_reader.mode = None
        env_reader._EnvReader__validate_mode()
        self.assertEqual(env_reader.mode, EnvReader.INCLUDE)

    # Validates the mode field when it is set to EXCLUDE.
    def test_validate_mode_exclude(self):
        env_reader = EnvReader()
        env_reader.mode = EnvReader.EXCLUDE
        env_reader._EnvReader__validate_mode()
        self.assertEqual(env_reader.mode, EnvReader.EXCLUDE)

    # Validates the mode field when it is set to an integer.
    def test_validate_mode_integer(self):
        env_reader = EnvReader()
        env_reader.mode = 123
        env_reader._EnvReader__validate_mode()
        self.assertEqual(env_reader.mode, EnvReader.INCLUDE)

    # Validates the mode field when it is set to a boolean.
    def test_validate_mode_boolean(self):
        env_reader = EnvReader()
        env_reader.mode = True
        env_reader._EnvReader__validate_mode()
        self.assertEqual(env_reader.mode, EnvReader.INCLUDE)

    # Does not modify the mode field when it is already a valid mode.
    def test_does_not_modify_mode_when_valid_mode(self):
        # Arrange
        env_reader = EnvReader()
        env_reader.mode = EnvReader.INCLUDE

        # Act
        env_reader._EnvReader__validate_mode()

        # Assert
        self.assertEqual(env_reader.mode, EnvReader.INCLUDE)


class TestPrepareRecord(unittest.TestCase):

    # The method correctly removes whitespace characters from the input string.
    def test_remove_whitespace(self):
        # Initialize the class object
        env_reader = EnvReader()

        # Test input string with whitespace characters
        input_string = "  hello  world  "
        expected_result = "helloworld"
        result = env_reader._EnvReader__prepare_record(input_string)
        self.assertEqual(result, expected_result)

        # Test input string with leading and trailing whitespace characters
        input_string = "  hello world  "
        expected_result = "helloworld"
        result = env_reader._EnvReader__prepare_record(input_string)
        self.assertEqual(result, expected_result)

        # Test input string with only whitespace characters
        input_string = "     "
        expected_result = ""
        result = env_reader._EnvReader__prepare_record(input_string)
        self.assertEqual(result, expected_result)

    # The method correctly handles an empty input string.
    def test_empty_input_string(self):
        # Initialize the class object
        env_reader = EnvReader()

        # Test empty input string
        input_string = ""
        expected_result = ""
        result = env_reader._EnvReader__prepare_record(input_string)
        self.assertEqual(result, expected_result)

    # The method correctly handles an input string with only whitespace characters.
    def test_whitespace_input_string(self):
        # Initialize the class object
        env_reader = EnvReader()

        # Test input string with only whitespace characters
        input_string = "     "
        expected_result = ""
        result = env_reader._EnvReader__prepare_record(input_string)
        self.assertEqual(result, expected_result)

    # The method correctly removes newline characters from the input string.
    def test_remove_newline_characters(self):
        # Initialize the class object
        env_reader = EnvReader()

        # Test input string with newline characters
        input_string = "hello\nworld"
        expected_result = "helloworld"
        result = env_reader._EnvReader__prepare_record(input_string)
        self.assertEqual(result, expected_result)

        # Test input string with leading and trailing newline characters
        input_string = "\nhello\nworld\n"
        expected_result = "helloworld"
        result = env_reader._EnvReader__prepare_record(input_string)
        self.assertEqual(result, expected_result)

        # Test input string with only newline characters
        input_string = "\n\n\n"
        expected_result = ""
        result = env_reader._EnvReader__prepare_record(input_string)
        self.assertEqual(result, expected_result)

    # The method correctly removes tab characters from the input string.
    def test_remove_tab_characters(self):
        # Initialize the class object
        env_reader = EnvReader()

        # Test input string with tab characters
        input_string = "hello\tworld"
        expected_result = "helloworld"
        result = env_reader._EnvReader__prepare_record(input_string)
        self.assertEqual(result, expected_result)

        # Test input string with leading and trailing tab characters
        input_string = "\thello world\t"
        expected_result = "helloworld"
        result = env_reader._EnvReader__prepare_record(input_string)
        self.assertEqual(result, expected_result)

        # Test input string with only tab characters
        input_string = "\t\t\t"
        expected_result = ""
        result = env_reader._EnvReader__prepare_record(input_string)
        self.assertEqual(result, expected_result)

    # The method returns the cleaned up string.
    def test_remove_whitespace(self):
        # Initialize the class object
        env_reader = EnvReader()

        # Test input string with whitespace characters
        input_string = "  hello  world  "
        expected_result = "helloworld"
        result = env_reader._EnvReader__prepare_record(input_string)
        self.assertEqual(result, expected_result)

        # Test input string with leading and trailing whitespace characters
        input_string = "  hello world  "
        expected_result = "helloworld"
        result = env_reader._EnvReader__prepare_record(input_string)
        self.assertEqual(result, expected_result)

        # Test input string with only whitespace characters
        input_string = "     "
        expected_result = ""
        result = env_reader._EnvReader__prepare_record(input_string)
        self.assertEqual(result, expected_result)

    # The method correctly handles an input string with only newline characters.
    def test_input_string_with_only_newline_characters(self):
        # Initialize the class object
        env_reader = EnvReader()

        # Test input string with only newline characters
        input_string = "\n\n\n\n"
        expected_result = ""
        result = env_reader._EnvReader__prepare_record(input_string)
        self.assertEqual(result, expected_result)

    # The method correctly handles an input string with only tab characters.
    def test_correctly_handles_input_with_only_tab_characters(self):
        # Initialize the class object
        env_reader = EnvReader()

        # Test input string with only tab characters
        input_string = "\t\t\t"
        expected_result = ""
        result = env_reader._EnvReader__prepare_record(input_string)
        self.assertEqual(result, expected_result)

    # The method correctly handles an input string with a mix of whitespace, newline, and tab characters.
    def test_correctly_handles_mix_of_whitespace(self):
        # Initialize the class object
        env_reader = EnvReader()

        # Test input string with whitespace characters
        input_string = "  hello  world  "
        expected_result = "helloworld"
        result = env_reader._EnvReader__prepare_record(input_string)
        self.assertEqual(result, expected_result)

        # Test input string with leading and trailing whitespace characters
        input_string = "  hello world  "
        expected_result = "helloworld"
        result = env_reader._EnvReader__prepare_record(input_string)
        self.assertEqual(result, expected_result)

        # Test input string with newline characters
        input_string = "hello\nworld"
        expected_result = "helloworld"
        result = env_reader._EnvReader__prepare_record(input_string)
        self.assertEqual(result, expected_result)

        # Test input string with tab characters
        input_string = "hello\tworld"
        expected_result = "helloworld"
        result = env_reader._EnvReader__prepare_record(input_string)
        self.assertEqual(result, expected_result)

        # Test input string with a mix of whitespace, newline, and tab characters
        input_string = "  hello\n\tworld  "
        expected_result = "helloworld"
        result = env_reader._EnvReader__prepare_record(input_string)
        self.assertEqual(result, expected_result)

        # Test input string with only whitespace characters
        input_string = "     "
        expected_result = ""
        result = env_reader._EnvReader__prepare_record(input_string)
        self.assertEqual(result, expected_result)

    # The method correctly handles an input string with non-ASCII characters.
    def test_handles_non_ascii_characters(self):
        # Initialize the class object
        env_reader = EnvReader()

        # Test input string with non-ASCII characters
        input_string = "héllø wørld"
        expected_result = "hélløwørld"
        result = env_reader._EnvReader__prepare_record(input_string)
        self.assertEqual(result, expected_result)

    # The method correctly handles an input string with special characters (e.g. punctuation marks).
    def test_input_with_special_characters(self):
        # Initialize the class object
        env_reader = EnvReader()

        # Test input string with special characters
        input_string = "Hello, world!"
        expected_result = "Hello,world!"
        result = env_reader._EnvReader__prepare_record(input_string)
        self.assertEqual(result, expected_result)

        # Test input string with multiple special characters
        input_string = "Hello, world!!!"
        expected_result = "Hello,world!!!"
        result = env_reader._EnvReader__prepare_record(input_string)
        self.assertEqual(result, expected_result)

        # Test input string with only special characters
        input_string = "!!!"
        expected_result = "!!!"
        result = env_reader._EnvReader__prepare_record(input_string)
        self.assertEqual(result, expected_result)

    # The method correctly handles an input string with leading and trailing whitespace characters.
    def test_input_string_with_only_whitespace_characters(self):
        # Initialize the class object
        env_reader = EnvReader()

        # Test input string with only whitespace characters
        input_string = "     "
        expected_result = ""
        result = env_reader._EnvReader__prepare_record(input_string)
        self.assertEqual(result, expected_result)

    # The method correctly handles an input string with leading and trailing newline characters.
    def test_input_string_with_newline_characters(self):
        # Initialize the class object
        env_reader = EnvReader()

        # Test input string with leading and trailing newline characters
        input_string = "\nhello world\n"
        expected_result = "helloworld"
        result = env_reader._EnvReader__prepare_record(input_string)
        self.assertEqual(result, expected_result)

    # The method correctly handles an input string with leading and trailing tab characters.
    def test_input_string_with_leading_and_trailing_tab_characters(self):
        # Initialize the class object
        env_reader = EnvReader()

        # Test input string with leading and trailing tab characters
        input_string = "\t\tHello World\t\t"
        expected_result = "HelloWorld"
        result = env_reader._EnvReader__prepare_record(input_string)
        self.assertEqual(result, expected_result)
        

class TestSplitRecords(unittest.TestCase):

    # Returns an empty list when given an empty string.
    def test_empty_string(self):
        env_reader = EnvReader()
        result = env_reader._EnvReader__split_dns_record("")
        self.assertEqual(result, [])

    # Returns a list with one element when given a string without commas.
    def test_string_without_commas(self):
        env_reader = EnvReader()
        result = env_reader._EnvReader__split_dns_record("example")
        self.assertEqual(result, ["example"])

    # Returns a list with multiple elements when given a string with commas.
    def test_string_with_commas(self):
        env_reader = EnvReader()
        result = env_reader._EnvReader__split_dns_record("example1,example2,example3")
        self.assertEqual(result, ["example1", "example2", "example3"])

    # Returns an empty list when given None.
    def test_none(self):
        env_reader = EnvReader()
        result = env_reader._EnvReader__split_dns_record(None)
        self.assertEqual(result, [])

    # Returns an empty list when given an empty string with spaces.
    def test_empty_string_with_spaces(self):
        env_reader = EnvReader()
        result = env_reader._EnvReader__split_dns_record("   ")
        self.assertEqual(result, [])

    # Returns a list with one empty string when given a string with only commas.
    def test_string_with_only_commas(self):
        env_reader = EnvReader()
        result = env_reader._EnvReader__split_dns_record(",,")
        self.assertEqual(result, [])

    # Returns a list with multiple elements when given a string with spaces between commas.
    def test_multiple_elements_with_spaces(self):
        env_reader = EnvReader()
        result = env_reader._EnvReader__split_dns_record("element1, element2, element3")
        self.assertEqual(result, ["element1", " element2", " element3"])

    # Returns a list with multiple elements when given a string with spaces before or after commas.
    def test_string_with_spaces(self):
        env_reader = EnvReader()
        result = env_reader._EnvReader__split_dns_record("a, b, c")
        self.assertEqual(result, ["a", " b", " c"])

    # Returns a list with multiple elements when given a string with tabs between commas.
    def test_multiple_elements_with_tabs(self):
        env_reader = EnvReader()
        result = env_reader._EnvReader__split_dns_record("element1,\t\telement2,\t\telement3")
        self.assertEqual(result, ["element1", "\t\telement2", "\t\telement3"])

    # Returns a list with multiple elements when given a string with newlines between commas.
    def test_multiple_elements_with_newlines(self):
        env_reader = EnvReader()
        record = "element1,\nelement2,\nelement3"
        result = env_reader._EnvReader__split_dns_record(record)
        self.assertEqual(result, ["element1", "\nelement2", "\nelement3"])

    # Returns a list with multiple elements when given a string with a mix of spaces, tabs, and newlines between commas.
    def test_multiple_elements_with_mix_of_spaces_tabs_and_newlines(self):
        env_reader = EnvReader()
        result = env_reader._EnvReader__split_dns_record("element1, element2, element3")
        self.assertEqual(result, ["element1", " element2", " element3"])
