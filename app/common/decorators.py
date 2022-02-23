import time


def timeit(method):
    async def timed(*args, **kw):
        ts = time.time()
        result = await method(*args, **kw)
        te = time.time()
        from app import app
        app.logger.info('%r  %2.2f ms' % (method.__name__, (te - ts) * 1000))
        return result

    return timed
