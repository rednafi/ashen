from functools import partial, wraps
import time
import logging

logging.getLogger(__name__)


def retry(check_exception, try_count=5, delay=5, backoff=1, logger=None):
    """Retry calling the decorated function using an exponential backoff.

    http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
    original from: http://wiki.python.org/moin/PythonDecoratorLibrary#Retry

    :param check_exception: the exception to check. may be a tuple of
        exceptions to check
    :type check_exception: Exception or tuple
    :param try_count: number of times to try (not retry) before giving up
    :type try_count: int
    :param delay: initial delay between retries in seconds
    :type delay: int
    :param backoff: backoff multiplier e.g. value of 2 will double the delay
        each retry
    :type backoff: int
    :param logger: logger to use. If None, print
    :type logger: logging.Logger instance
    """

    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = try_count, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except check_exception as e:
                    msg = "%s, Retrying in %d seconds..." % (str(e), mdelay)

                    if logger:
                        logging.warning(msg)
                    else:
                        print(msg)

                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry  # true decorator

    return deco_retry

