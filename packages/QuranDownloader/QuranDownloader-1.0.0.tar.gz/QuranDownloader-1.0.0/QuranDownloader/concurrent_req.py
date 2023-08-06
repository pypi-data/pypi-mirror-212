import concurrent.futures
# make concurrent requests


def concurrent_req(fun, url):
    executor = concurrent.futures.ProcessPoolExecutor()
    future = executor.submit(fun, url)
    return future.result()
