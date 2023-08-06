import io
from functools import wraps


def performance_profile(to_file=False):
    import cProfile, pstats

    def wrapper(function):
        @wraps(function)
        def inner(*args, **kwargs):
            pr = cProfile.Profile()
            pr.enable()

            result = function(*args, **kwargs)

            pr.disable()
            s = io.StringIO()
            sortby = "cumtime"  # 仅适用于 3.6, 3.7 把这里改成常量了
            ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
            ps.print_stats()
            print(s.getvalue())
            return result

        return inner

    return wrapper
