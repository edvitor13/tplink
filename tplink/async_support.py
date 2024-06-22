from __future__ import annotations
from functools import partial
import threading
from typing import Callable, Self



class AsyncSupport():

    def __init__(self):
        self.__async_mode: bool = False
        self.__async_mode_running: bool = False
        self.__async_sequence: list[Callable] = []
        self.__async_last_error: Exception | None = None

    
    def is_async_mode(self) -> bool:
        return self.__async_mode
    

    def add_async_sequence(self, call: Callable) -> Self:
        self.__async_sequence.append(call)
        return self
    

    def begin_async_mode(self) -> Self:
        self.__async_mode = True
        return self
    

    def run_async_mode(self) -> Self:
        if self.__async_mode_running:
            return self
        
        def _execute_methods():
            self.__async_mode_running = True
            try:
                for seq in self.__async_sequence:
                    seq()
            except Exception as e:
                self.__async_last_error = e
                raise e
            finally:
                self.__async_mode = False
                self.__async_mode_running = False
                self.__async_sequence = []

        thread = threading.Thread(target=_execute_methods)
        thread.start()
        return self

    
    @staticmethod
    def _track_async_mode(func):
        def inner_wrapper(self, *args, **kwargs):
            if self.is_async_mode():
                self.add_async_sequence(partial(func, self, *args, **kwargs))
                return self
            return func(self, *args, **kwargs)
        return inner_wrapper
