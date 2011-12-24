#!/usr/local/bin/python
#-*- coding = utf-8 -*-
''' The List Host Library Python Version'''

'''
Author      : Wei Lichun<lichun.william@gmail.com>
Create Date : Sat Sep 10 18:58:31 CST 2011
Version     : 0.1

This is free software; see the source for copying conditions. 
There is NO warranty; not even for MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.

Report bugs to lichun.william@gmail.com
'''
import threading
import subprocess
import os
import Queue

class Task(threading.Thread):
    def __init__(self,key,cmd,finish_pool,semaphore):
        threading.Thread.__init__(self)
        self.key=key
        self.cmd=cmd
        self.done_queue=finish_pool
        self.stdout=None
        self.semaphore=semaphore

    def run(self):
        p=subprocess.Popen(self.cmd,stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,stdin=None,shell=False)    
        self.stdout=p.communicate()[0]
        self.done_queue.put(self)
        self.semaphore.release()
        
class TaskGroup(threading.Thread):
    def __init__(self,parallel=10):     
        threading.Thread.__init__(self)
        self.done_queue=Queue.Queue()
        self.task_queue=Queue.Queue()
        self.semaphore=threading.Semaphore(parallel)
    
    def add_task(self,key,cmd):
        task=Task(key,cmd,self.done_queue,self.semaphore)
        self.task_queue.put(task)
    def run(self):
        while(not self.task_queue.empty()):
            t=self.task_queue.get()
            self.semaphore.acquire()
            t.start()    
