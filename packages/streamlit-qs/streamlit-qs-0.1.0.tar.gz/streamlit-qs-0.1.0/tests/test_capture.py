
import logging
import sys
import unittest.mock as mock

from streamlit.runtime.scriptrunner.script_run_context import SCRIPT_RUN_CONTEXT_ATTR_NAME

import streamlit_qs.capture as stu


# This patch makes the test _think_ it's running in stremalit
@mock.patch("streamlit_qs.capture.current_thread", **{SCRIPT_RUN_CONTEXT_ATTR_NAME: True})
def test_st_stdout(_mock_cur_thread):
    fake_callback = mock.MagicMock()
    with stu.st_stdout(fake_callback, terminator=""):
        print("Hello")
        fake_callback.assert_called_with("Hello\n")
        print("World")
        fake_callback.assert_called_with("Hello\nWorld\n")


# This patch makes the test _think_ it's running in stremalit
@mock.patch("streamlit_qs.capture.current_thread", **{SCRIPT_RUN_CONTEXT_ATTR_NAME: True})
def test_st_stderr(_mock_cur_thread):
    fake_callback = mock.MagicMock()
    with stu.st_stderr(fake_callback):
        print("olleH")
        sys.stderr.write("Hello")
        fake_callback.assert_called_with("Hello\n")
        sys.stderr.write("World")
        fake_callback.assert_called_with("Hello\nWorld\n")


def test_non_streamlit_no_patch():
    # When we're not mocking the current thread, these functions shouldn't patch anything.
    fake_callback = mock.MagicMock()
    original_stdout_write = sys.stdout.write
    original_stderr_write = sys.stderr.write
    with stu.st_stderr(fake_callback):
        assert sys.stderr.write is original_stderr_write
    with stu.st_stdout(fake_callback):
        assert sys.stdout.write is original_stdout_write


def test_st_logging():
    fake_callback = mock.MagicMock()

    # Test basic config
    with stu.st_logging(fake_callback):
        logging.root.warning("test log")
        assert "WARNING test log\n" in fake_callback.call_args[0][0]

    # Test from_logger
    testlogger = logging.getLogger("test_logger")
    assert not testlogger.handlers
    fake_callback.reset_mock()
    with stu.st_logging(fake_callback, from_logger=testlogger):
        logging.root.warning("don't show this")
        fake_callback.assert_not_called()
        testlogger.warning("but show this")
        assert "WARNING but show this\n" in fake_callback.call_args[0][0]

    # Test terminator
    with stu.st_logging(fake_callback, terminator="foo"):
        logging.root.warning("test log")
        assert "WARNING test logfoo" in fake_callback.call_args[0][0]
        pass

    # Test formatter
    with stu.st_logging(fake_callback, formatter=logging.Formatter("%(message)s %(levelname)s")):
        logging.root.warning("test log")
        assert "test log WARNING" in fake_callback.call_args[0][0]

    # Test loguru
    sys.modules["loguru"] = mock_loguru = mock.MagicMock()
    mock_loguru.logger.add.return_value = 54
    with stu.st_logging(fake_callback, from_logger=mock_loguru.logger):
        assert isinstance(mock_loguru.logger.add.call_args[0][0], logging.Handler)
    assert mock_loguru.logger.remove.call_args[0][0] == 54