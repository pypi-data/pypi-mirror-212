from time import sleep

from zoo_framework.workers.event_worker import EventWorker
from zoo_framework.workers import StateMachineWorker
from zoo_framework.utils import LogUtils

from .aop import worker_list, config_funcs
from .params_factory import ParamsFactory


class Master(object):
    def __init__(self, loop_interval=1):
        from zoo_framework.core.waiter import WaiterFactory
        # load params
        ParamsFactory("./config.json")
        self.config()
        
        from zoo_framework.params import WorkerParams
        self.workers = worker_list
        self.workers.append(StateMachineWorker())
        self.workers.append(EventWorker())
        self.loop_interval = loop_interval
        
        # 根据策略生成waiter
        waiter = WaiterFactory.get_waiter(WorkerParams.WORKER_RUN_POLICY)
        if waiter is not None:
            self.waiter = waiter
            self.waiter.call_workers(self.workers)
        else:
            raise Exception("Master hasn't available waiter,the application can't start.")
    
    def change_waiter(self, waiter):
        if self.waiter is not None:
            raise Exception("")
        self.waiter = waiter
    
    def config(self):
        for key, value in config_funcs.items():
            value()
    
    def run(self):
        while True:
            self.waiter.execute_service()
            if self.loop_interval > 0:
                LogUtils.debug("Master Sleep")
                sleep(self.loop_interval)
