import multiprocessing
import copy


class ResourceWorker():
    def __init__(self, exclusiveResource=None, sharedQueue=None, func=None):
        self.exclusiveResource = exclusiveResource
        self.sharedQueue = sharedQueue
        self.func = func
        self.results = multiprocessing.Manager().dict()
    
    def work(self):
        while self.sharedQueue.qsize() > 0:
            try:
                oneJob = self.sharedQueue.get_nowait()
                self.results[oneJob] = self.func(oneJob, self.exclusiveResource)
            except:
                continue
        
class ResourceManager():
    def __init__(self, nWorkers=None, jobsToBeDone=None, resourceToBeShared=None, func=None):
        self.nWorkers = nWorkers
        self.sharedQueue = multiprocessing.Queue()
        for j in jobsToBeDone:
            self.sharedQueue.put(j)
        self.resourceToBeShared = resourceToBeShared
        self.func = func
        self.workers = []        
        self.hireWorkers()
        self.processes = []
    
    def hireWorkers(self):
        for i in range(self.nWorkers):
            res_tmp = copy.deepcopy(self.resourceToBeShared)
            wor_tmp = ResourceWorker(res_tmp, self.sharedQueue, self.func)
            self.workers.append(wor_tmp)
        return
            
    def run(self):
        for w in self.workers:
            p = multiprocessing.Process(target=w.work)
            p.start()
            self.processes.append(p)
        for p in self.processes:
            p.join()
        return
resource1 = [1,1,2,3,5]
jobQueue = list(range(10000))
def myFunction(x, reso):
    return [x+y for y in reso]

m1 = ResourceManager(5, jobQueue, resource1, myFunction)

m1.run()
    
