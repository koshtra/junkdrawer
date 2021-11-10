import json
import datetime
import unittest

class Task:
    """ One item in a to-do list """
    def __init__(self, name, first_occurrence, how_often, how_many):
        """ Initialize task attributes """
        self.name = name                            # name of the task
        self.first_occurrence = first_occurrence    # date it will first happen
        self.how_often = how_often                  # how often it recurs, in days
        self.how_many = how_many                    # how many times will the task recur? 0 means forever
        self.postponed = 0                          # how many times has this task been left undone?
        self.times_done = 0                         # how many times has this task been completed?
        self.date_created = datetime.datetime.now() # when was this task created?
        self.date_last_done = None                  # when was this task last completed?

    def task_attributes(self):
        """ Report the state of a Task object """
        if self.how_many == 0:
            hm = "forever"
        else:
            hm = self.how_many
        task_attributes = f"\n{self.name}                               \
                          \nfirst occurrence: {self.first_occurrence}   \
                          \nhow often (in days): {self.how_often}       \
                          \nhow many intended recurrences: {hm}         \
                          \nhow many times postponed: {self.postponed}  \
                          \nhow many times done: {self.times_done}      \
                          \nfirst created: {self.date_created}          \
                          \nlast time done: {self.date_last_done}"
        return task_attributes
        
def get_user_task():
    """ input a task from the user """
    u_name = input("Task name? ")
    u_first = input("First occurrence? ")
    u_oft = input("How often will it repeat? ")
    u_many = input("How many times will it repeat? ")
    u_task = Task(u_name, u_first, u_oft, u_many)
    return u_task

def store_task_list(tl):
    """ save the task list as a JSON object """
    filename = "task_storage.json"
    with open(filename,'w') as f:
        serialized_tasks = []
        for t in tl:
            created = t.date_created.isoformat()
            if t.date_last_done == None:
                done = None
            else:
                done = t.date_last_done.isoformat()
            serialized_tasks.append([t.name, t.first_occurrence, t.how_often, t.how_many, \
                       t.postponed, t.times_done, created, done])
        json.dump(serialized_tasks, f)

def retrieve_task_list():
    """ read the saved task list """
    filename = "task_storage.json"
    with open(filename) as f:
        tl = json.load(f)
        resurrected_tasks = []
        for t in tl:
            task = Task(t[0],t[1],t[2],t[3])
            task.postponed = t[4]
            task.times_done = t[5]
            task.date_created = datetime.datetime.fromisoformat(t[6])
            if t[7] == None:
                task.date_last_done = None
            else:
                task.date_last_done = datetime.datetime.fromisoformat(t[7])
            resurrected_tasks.append(task)
    return(resurrected_tasks)

class TestStoreAndRetrieveTask(unittest.TestCase):                  
    def test_simple_store_and_retrieve_task(self):
        task_list = []                     
        task1 = Task("burp",1,2,3)
        task2 = Task("eruct",2,3,4)
        task3 = Task("obfuscate",0,0,0)
        task3.date_last_done = datetime.datetime.today()

        task_list.append(task1)
        task_list.append(task2)
        task_list.append(task3) 
    
        store_task_list(task_list)
        restored_task_list = retrieve_task_list()
        
        for i in [0,1,2]:
            s=task_list[i].task_attributes()
            t=restored_task_list[i].task_attributes()    
            self.assertEqual(s,t)

if __name__ == '__main__':
    unittest.main()

