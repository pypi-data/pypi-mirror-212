import dill
from multiprocessing import Process, Value
#TODO ADD DILL TO REQUIREMENTS IF REMAINS IN USE


class ValuedProcess(Process):
    """
    A subclass of Process that allows for the thread's target function return value to be captured
    with thread.join()
    Warning: Current implementation is that arguments passed to target will NOT get unpacked. Errors
    may arise if  more than one argument is provided to the thread target.
    """
    def __init__(self, value=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._target = dill.dumps(self._target)  # Save the target function as bytes, using dill
        if value is not None:
            self._return = None
            self._value = value

    def run(self):
        if self._target:
            self._target = dill.loads(self._target)    # Unpickle the target function before executing
            self._target(*self._args, **self._kwargs)
            if self._value:
                self._return = self._target(self._args, **self._kwargs)

    def join(self, *args):
        """
        Will wait for the thread's completion, and return the target's return value.

        @rtype: object
        """
        Process.join(self, *args)
        if self._target and self._value:
            self._value = self._return
        # return self._return


