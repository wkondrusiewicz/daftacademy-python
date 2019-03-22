#task I


def to_list(func):
    def wrapper(*args):
      result = func(*args)
      return list(result)
    return wrapper



#task II

def is_correct(*args):
  def wraper_1(func):
    def real_func():
      k_list = tuple(func().keys())
      if set(args).issubset(k_list):
        return func()
      else:
        return None
    return real_func
  return wraper_1


#task III

import datetime  # do not change this import, use datetime.datetime.now() to get date

def add_date(format):
    def wraper_1(func):
        def real_func():
            result = func()
            result['date'] = datetime.datetime.now().strftime(format)
            return result
        return real_func
    return wraper_1
