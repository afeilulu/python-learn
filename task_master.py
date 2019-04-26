import random, time, queue
from multiprocessing.managers import BaseManager
from multiprocessing import freeze_support

# 发送任务的队列:
task_queue = queue.Queue()
# 接收结果的队列:
result_queue = queue.Queue()

# 从BaseManager继承的QueueManager:
class QueueManager(BaseManager):
    pass

def gettask():
    return task_queue

def getresult():
    return result_queue

def test():
    # 把两个Queue都注册到网络上, callable参数关联了Queue对象:
    QueueManager.register('get_task', callable=gettask)
    QueueManager.register('get_result', callable=getresult)
    # 绑定端口5000, 设置验证码'abc':
    manager = QueueManager(address=('127.0.0.1', 5000), authkey=b'abc')
    # 启动Queue:
    manager.start()

    try:
        # 获得通过网络访问的Queue对象:
        task = manager.get_task()
        result = manager.get_result()
        # 放几个任务进去:
        for i in range(20):
            n = random.randint(0, 10000)
            print('Put task %d...' % n)
            task.put(n)

        print('Try get results...')
        while not task.empty():
            time.sleep(1)

        # 从result队列读取结果:
        for i in range(20):
            r = result.get(timeout=10)
            print('Result: %s' % r)

    except:
        print('Manager master error')

    finally:
        # 关闭:
        manager.shutdown()
    print('master exit.')

if __name__=='__main__':
    freeze_support()
    test()