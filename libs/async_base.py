from concurrent.futures import ThreadPoolExecutor


def async(fn):
    def wrapper(*args, **kwargs):
        if 'async' in kwargs:
            if kwargs['async'] == True:
                del kwargs['async']
                if not args[0].future:
                    executor = ThreadPoolExecutor(max_workers=1)
                    args[0].future = executor.submit(fn, *args, **kwargs)
                    executor.shutdown(wait=False)
                else:
                    raise Exception("Another async function is ongoing. Call wait() to end it.")
            else:
                del kwargs['async']
                return fn(*args, **kwargs)
        else:
            return fn(*args, **kwargs)
    return wrapper

class AsyncCall():
    def __init__(self):
        self.future = None

    def __del__(self):
        self.destroy_async_call()

    def destroy_async_call(self):
        if self.future:
            self.future.cancel()

    def wait(self):
        if self.future:
            result = self.future.result()
            self.future = None
            return result
        else:
            raise Exception("There is no ongoing async function calls.")
