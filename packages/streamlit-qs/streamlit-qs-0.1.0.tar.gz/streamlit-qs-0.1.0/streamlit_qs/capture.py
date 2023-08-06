"""Capture utility extensions for the standard streamlit library"""
from __future__ import annotations

import logging
import sys
from contextlib import contextmanager
from io import StringIO
from threading import current_thread
from typing import Callable, TextIO

from streamlit.runtime.scriptrunner.script_run_context import SCRIPT_RUN_CONTEXT_ATTR_NAME


@contextmanager
def st_redirect(src: TextIO, dst: Callable, terminator: str = "\n"):
    """Redirect STDOUT and STDERR to streamlit functions."""
    with StringIO() as buffer:

        def new_write(b):
            buffer.write(b + terminator)
            dst(buffer.getvalue())

        # Test if we are actually running in the streamlit script thread before we redirect
        if getattr(current_thread(), SCRIPT_RUN_CONTEXT_ATTR_NAME, None):
            old_write = src.write
            try:
                src.write = new_write  # type: ignore
                yield
            finally:
                src.write = old_write  # type: ignore
        else:
            yield


@contextmanager
def st_stdout(dst: Callable, terminator="\n"):
    """Capture STDOUT and redirect it to a callable `dst`.

    Args:
        dst (callable[str]): A funciton callable with a single string argument. The entire captured contents will be
            passed to this function every time a new string is written. It is designed to be compatible with
            st.empty().* functions as callbacks.
        terminator (optional, str): If a `terminator` is specified, it is added onto each call to stdout.write/print.
            This defaults to a newline which causes them to display on separate lines within an st.empty.write `dst.
            If using this with st.empty.code as `dst` it is recommended to set `terminator` to empty string.

    Code Example:

        with st_stdout(st.empty().write):
            print("this will print as if st.write() was called")
    """
    with st_redirect(sys.stdout, dst, terminator):
        yield


@contextmanager
def st_stderr(dst: Callable, terminator="\n"):
    """Capture STDERR and redirect it to a callable `dst`.

    Args:
        dst (callable[str]): A funciton callable with a single string argument. The entire captured contents will be
            passed to this function every time a new string is written. It is designed to be compatible with
            st.empty().* functions as callbacks.
        terminator (optional, str): If a `terminator` is specified, it is added onto each call to stdout.write/print.
            This defaults to a newline which causes them to display on separate lines within an st.empty.write `dst.
            If using this with st.empty.code as `dst` it is recommended to set `terminator` to empty string.

    Code Example:

        with st_stderr(st.empty().code, terminator=""):
            print("this will print as if st.code() was called")
    """
    with st_redirect(sys.stderr, dst, terminator):
        yield


class StreamlitLoggingHandler(logging.StreamHandler):
    """Extension of Stream Handler that passes the value of the stream IO buffer to a callback function on every log."""

    def set_callback(self, func: Callable):
        """Set the callback to be used on this record."""
        # pylint: disable=attribute-defined-outside-init
        self.callback = func

    def emit(self, record: logging.LogRecord):
        """Emit a record but also call a function on the full buffer."""
        super().emit(record)
        self.callback(self.stream.getvalue())


@contextmanager
def st_logging(
    dst: Callable,
    terminator: str = "\n",
    from_logger: logging.Logger | None = None,
    formatter: logging.Formatter | None = None,
):
    """Redirect logging to a streamlit function call `dst`.

        Args:
            dst (callable[str]): A funciton callable with a single string argument. The entire log contents will be
                passed to this function every time a log is written. It is designed to be compatible with st.empty().*
                functions as callbacks.
            terminator (optional, str): If a `terminator` is specified, it is added onto the end of each log.
                This defaults to a newline which causes them to display on separate lines within an st.empty.write `dst.
                If using this with st.empty.code as `dst` it is recommended to set `terminator` to empty string.
            from_logger (optional, logging.Logger or loguru.logger): The logger from which logs will be captured.
                Defaults to `logging.root`.
            formatter (optional, logging.Formatter): If specified, the specified formatter will be added to the logging
                handler to control how logs are displayed.

        Code Examples:

            with st_logging(st.empty().write):
                logging.info("All logs will be output to an st.empty")

            with st_logging(st.empty().code, terminator="", to_logger=loguru.logger)
    #           loguru.logger.info("This will also log (if using loguru's logger)")
    """
    if not from_logger:
        from_logger = logging.getLogger()  # root logger

    # Special-case loguru
    using_loguru = "loguru" in sys.modules and sys.modules["loguru"].logger is from_logger

    with StringIO() as buffer:
        new_handler = StreamlitLoggingHandler(buffer)
        new_handler.set_callback(dst)
        new_handler.terminator = terminator
        if formatter:
            new_handler.setFormatter(formatter)
        elif using_loguru:
            pass
        else:
            new_handler.setFormatter(
                logging.Formatter("%(asctime)s - %(levelname)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p")
            )
        handler_id = None
        if using_loguru:
            handler_id = from_logger.add(new_handler)  # type: ignore
        else:
            from_logger.addHandler(new_handler)
        try:
            yield
        finally:
            if using_loguru:
                from_logger.remove(handler_id)  # type: ignore
            else:
                from_logger.removeHandler(new_handler)