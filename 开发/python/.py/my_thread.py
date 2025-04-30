import threading


# 自定义线程，重写join()方法，添加返回值

class MyThread(threading.Thread):

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)
        else:
            print(111)

    def join(self):
        """

        :rtype: object
        """
        super().join()
        return self._return
