import collections
from random import randint
import math
import time
import copy


# Constants
NUM_OF_TYPES = 5

MAX_NUM_OF_JOBS = 1000
MIN_NUM_OF_JOBS = 1


debug_file = open("debugout.txt", "w")

file_times = (time.time()/10000)


# returns the total number of machines that will be in use , and a raw jobs data
def handleInput():
    if input("Would you like to generate a new input file? Y/N\n") == "Y":
        num_of_machines = int(input("Please enter the number of machines: \n"))
        min_processing_time = int(input("Please enter the minimum processing time for a single job: \n"))
        max_processing_time = int(input("Please enter the maximum processing time for a single job: \n"))
        num_of_jobs = int(input("Please enter the number of jobs: \n"))

        print("max process time is :", max_processing_time)

        """
         Generate the soon-to-be input file
         input file format will be :
        
         NUMBER_OF_MACHINES
         JOB_INDEX JOB_SIZE JOB_TYPE
        
         notice that the total number of jobs will be indicated in the [n-1,0] cell
        """
        inpt = open("input.txt", 'w')

        inpt.write(str(num_of_machines))
        inpt.write("\n")

        # Generate random number of jobs
        print("number of jobs generated: ", num_of_jobs)
        jobs = []
        for index in range(0, num_of_jobs):
            j = []
            j.append(index)
            job_size = randint(min_processing_time, int(max_processing_time))
            j.append(job_size)
            type = randint(1, NUM_OF_TYPES)
            j.append(type)
            inpt.write(str(index))
            inpt.write(" ")
            inpt.write(str(job_size))
            inpt.write(" ")
            inpt.write(str(type))
            inpt.write("\n")
            jobs.append(j)

        inpt.close()


    else:
        inpt = open("input.txt", 'r')
        jobs = []
        for index, line in enumerate(inpt):
            if index == 0:
                num_of_machines = int(line)
                print("The number of machines loaded : ", line, "\n")
            else:
                jobs.append(line.split())

        inpt.close()

    return num_of_machines, jobs


class Job(object):
    def __init__(self, ind, length, kind):
        self.number = ind
        self.length = length
        self.type = kind
        self.in_machine = -1

    def __iter__(self):
        return iter(self)


    def __str__(self):
        return "[%s, %s, %s]" % (self.number, self.length, self.type)


    def __repr__(self):
        return "[%s, %s, %s]" % (self.number, self.length, self.type)

    def __len__(self):
        return self.length

    def __eq__(self, other):
        if self.number != other.number:
            return False
        else:
            return True

    def getNumber(self):
        return self.number

    def getLength(self):
        return self.length

    def getType(self):
        return self.type


class Machine(object):
    def __init__(self, num):
        self.assigned_jobs = {}
        self.number = num  # Machine serial #
        self.span = 0  # Initial makespan
        self.types = [0] * NUM_OF_TYPES  # Histogram of size 5 - to count each type assigned to the machine
        self.types_sums = [0] * NUM_OF_TYPES

    def __str__(self):
        ret = ""
        for key, val in self.assigned_jobs.items():
            ret.join(val.getNumber()).join(", ")
        return "Jobs numbers : %s" % (ret)

    def __repr__(self):
        ret = ""
        for a in self.assigned_jobs:
            ret.join(a.getNumber()).join(", ")
        return "Jobs numbers : %s" % (ret)

    def __iter__(self):
        return iter(self)


    def retrieveJobsList(self):
        return self.assigned_jobs

    def addJob(self, job):
        job_type = job.getType() - 1
        self.assigned_jobs[job.getNumber()] = job
        self.span += job.getLength()
        self.types[job_type] = self.types[job_type] + 1
        self.types_sums[job_type] = self.types_sums[job_type] + job.length
        job.in_machine = self.number

    def retrieveJob(self, job_number):
        return self.assigned_jobs[job_number]

    # removing job from the machine by job number
    def removeJob(self, job_number):
        job = self.retrieveJob(job_number)
        job_type = job.getType() - 1
        del (self.assigned_jobs[job_number])
        self.span -= job.getLength()
        self.types[job_type] = self.types[job_type] - 1
        self.types_sums[job_type] = self.types_sums[job_type] - job.length
        job.in_machine = -1

    # Check if the machine has jobs of at most three types
    def isLegal(self):
        counter = 0
        for t in self.types:
            if t > 0:
                counter = counter + 1
        if counter < 4:
            return True
        else:
            return False

    # Check how many different types do I have
    def checkDiffTypes(self):
        count = 0
        for t in self.types:
            if t > 0:
                count = count + 1
        return count

    # returns a list of the types numbers assigned
    def getTypes(self):
        re_list = []
        for index, t in enumerate(self.types):
            if t > 0:
                re_list.append(index + 1)
        return re_list


# get input and handle it
num_of_machines, raw_jobs = handleInput()
num_of_jobs = len(raw_jobs)

# output file
out_file = open("output"+str(file_times)+"_"+str(NUM_OF_TYPES)+"types_"+str(num_of_machines)+"machines_"+str(num_of_jobs)+"jobs_"+".txt", "w")

print("Number of Machines:",num_of_machines,file=out_file)
print(num_of_jobs,"jobs:",file=out_file)
for job in raw_jobs:
    print(job,file=out_file)

print("---------------------------------",file=out_file)


# Creates and returns a machines list
def createMachines():
    machines = []
    for i in range(0, num_of_machines):
        cur_machine = Machine(i)
        machines.append(cur_machine)
    return machines


# Create and returns a list of jobs objects
def createJobs():
    jobs_list = []
    for job in raw_jobs:
        cur_job = Job(int(job[0]), int(job[1]), int(job[2]))
        print("Created job: index:", cur_job.number, "Length:", cur_job.length, "Type", cur_job.type, file=debug_file)
        jobs_list.append(cur_job)
    print("-----------------FINISHED CREATING JOB OBJECTS----------------------\n\n", file=debug_file)
    return jobs_list


# Creating objects
machines_list = createMachines()
jobs_list = createJobs()

# removes all jobs from a state ( a list of machines )
def removeAllJobs(m_list):
    for machine in m_list:
        cur_jobs = dict(machine.assigned_jobs)
        for key, job in cur_jobs.items():
            if key != job.number:
                print("SOMETHING WENT WRONG")
            num = job.number
            machine.removeJob(num)
            # print("REMOVED  -- machine#: ", machine.number, "assigned jobs: ", job)


# returns the minumum loaded machine in a given state
def findMinLoadMachine(m_list):
    prev_min_load = m_list[0].span
    min_load_index = 0
    for i in range(1,len(m_list)):
        if m_list[i].span < prev_min_load:
            prev_min_load = m_list[i].span
            min_load_index = i
    return min_load_index


# finds the minumum loaded machine in a state
def findMinLoadMachineLegaly(m_list):
    m_list_sorted = sorted(m_list, key=lambda x: x.span)
    return m_list_sorted

# this lpt is actually returning a new full state (after lpt algorithm) -  CAN BE ILLEGAL STATE - not in use !
def lpt(jobs, m_list):
    job_list_sorted_by_length = sorted(jobs, key=lambda x: x.length, reverse=True)
    new_machines_list = copy.deepcopy(m_list)
    for i in range(len(job_list_sorted_by_length)):
        new_machines_list[findMinLoadMachine(new_machines_list)].addJob(job_list_sorted_by_length[i])
    return new_machines_list


# the same LPT algorithm , but making sure the returned state is legal. If no legal state is possible - returns an empty list
def legalLpt(jobs,m_list):
    job_list_sorted_by_length = sorted(jobs, key=lambda x: x.length, reverse=True)
    new_machines_list = copy.deepcopy(m_list)
    for i in range(len(job_list_sorted_by_length)):
        legal = False
        # check assignment for next min loaded machine that is legal
        for j in range(len(new_machines_list)):
            assign_to_machines = findMinLoadMachineLegaly(new_machines_list)
            new_machines_list[assign_to_machines[j].number].addJob(job_list_sorted_by_length[i])
            if new_machines_list[assign_to_machines[j].number].isLegal():
                legal = True
                break
            else:   # revert
                new_machines_list[assign_to_machines[j].number].removeJob(job_list_sorted_by_length[i].number)
        if not legal:
            return []

    return new_machines_list


# return the makespan of a give state
def makeSpan(m_list: list):
    max_span = 0
    for machine in m_list:
        if machine.span > max_span:
            max_span = machine.span
    return max_span


# assigning a new job to a state , returning a copy of the originle so it can be reverted in case of illegal state
def simulateState(cur_job, cur_machine, cur_state):
    new_state = copy.deepcopy(cur_state)
    new_state[cur_machine].addJob(cur_job)
    return new_state


# printing the current state status
def printMachineStatOut(m_list):
    print("---------------MACHINES STATS--------------------------\n",file=out_file)
    for machine in m_list:
        cur_job_list = machine.retrieveJobsList()
        print("machine number ", machine.number, "assigned jobs [number,length,type]:",file=out_file)
        l = []
        for job_number, job in cur_job_list.items():
            l.append(job)
        print("".join(str(l)),file=out_file)

        print("Assigned types: ", machine.getTypes(),file=out_file)
        print("Types histogram: ", machine.types, "Sum of each type: ", machine.types_sums, "Makespan : ", machine.span,file=out_file)


# check if a state is legal so far
def checkLegalState(state:list):
    for machine in state:
        if machine.isLegal() is False:
            return False
    return True



# returns the sum of all jobs with this type
def sumOfTypeLeft(type,jobs):
    sum = 0
    for job in jobs:
        if job.type == type:
            sum += job.length
    return sum


# calculating the lowe bound
def lowerBound(state,jobs):
    args = []
    args.append(avg_job)
    args.append(max_job)
    for machine in state:
        args.append(machine.span)
    machine_possibilities = findLegalPossiblities(state,jobs[0].type)
    possibilities_sum = 0
    for i in machine_possibilities:
        possibilities_sum += state[i].span

    delta = sumOfTypeLeft(jobs[0].type,jobs[1:])
    args.append((possibilities_sum + delta)/len(machine_possibilities))
    return max(args)


# gets a job type with a current state (m_list) and returns a list of machines(numbers) that can accept this job type
def findLegalPossiblities(m_list,job_type):
    machines = []
    for machine in m_list:
        types = machine.getTypes()
        if job_type in types:
            machines.append(machine.number)
        elif len(types) < 3:
            machines.append(machine.number)
    if len(machines) == 0:
        print()
    return machines


# returns the minumum loaded LEGAL machine (by number of jobs), with the least types. If fails to find a legal machine, returns -1
def findMinJobLoadedMachine(m_list,job_type,job):
    legal_possibilities_numbers = findLegalPossiblities(m_list,job_type)
    if len(legal_possibilities_numbers) == 0:
        print()
    legal_machines = [m_list[i] for i in legal_possibilities_numbers]
    legal_machines_sorted_count_types = sorted(legal_machines, key=lambda x: (len(x.assigned_jobs),x.checkDiffTypes()), reverse=False)
    if len(legal_machines_sorted_count_types) == 0:
        return -1
    return legal_machines_sorted_count_types[0].number


def upperBoundAlg(jobs, m_list):
    # job_list_sorted_by_type_by_length = sorted(jobs, key=lambda x: (x.type,x.length), reverse=True)
    assigned_types = set()
    assigned_jobs_indices = []
    new_machines_list = copy.deepcopy(m_list)
    new_jobs = copy.deepcopy(jobs)

    # check which type already have a machine yet
    type_check = set()
    for i in range(len(new_machines_list)):
        for type in new_machines_list[i].getTypes():
            type_check.add(type)



    if len(type_check) < NUM_OF_TYPES:
        # need to add the missing types so each type will have at least one machine
        for i in range(len(new_jobs)):
            if len(assigned_types) == NUM_OF_TYPES - len(type_check):
                break
            assigned = False
            if new_jobs[i].type in assigned_types or new_jobs[i].type in type_check:
                continue
            else:   # first time seen this type
                for j in range(len(new_machines_list)):
                    new_machines_list[j].addJob(new_jobs[i])
                    if new_machines_list[j].isLegal():
                        assigned_types.add(new_jobs[i].type)
                        assigned_jobs_indices.append(i)
                        assigned = True
                    else:
                        # revert
                        new_machines_list[j].removeJob(new_jobs[i].number)
                    if assigned:
                        break

    # fix the job list that left after first assign
    for i in sorted(assigned_jobs_indices, reverse=True):
        del new_jobs[i]

    for i in range(len(new_jobs)):
        legal = False
        job_type = new_jobs[i].type
        # check assignment for next min loaded machine that is legal
        for j in range(len(new_machines_list)):
            assign_to_machine = findMinJobLoadedMachine(new_machines_list,job_type,new_jobs[i])
            if assign_to_machine == -1:    # meaning there's no legal machine to assign to
                return []
            new_machines_list[assign_to_machine].addJob(new_jobs[i])
            if new_machines_list[assign_to_machine].isLegal():
                legal = True
                break
            else:  # revert
                new_machines_list[assign_to_machine].removeJob(new_jobs[i].number)
        if not legal:
            return []

    return new_machines_list


# main branch and bound function
def bnb(state, jobs):
    global best_state,best_state_makespan,level_count
    if len(jobs) == 0:
        return

    # track levels
    level_count[jobs[0].number] += 1

    if best_state_makespan == math.ceil(avg_job):
        return

    for i in range(len(machines_list)):
        new_state = simulateState(jobs[0], i, state)
        is_legal_state = checkLegalState(new_state)
        lower_bound = lowerBound(new_state,jobs)

        if is_legal_state is True:
            # remember that doing lpt is just for upper bound calculation , so there might be no need in getting the after_lpt
            # print("now doing lpt for the rest", file=out_file)
            after_lpt = legalLpt(jobs[1:], new_state)
            # print("legal state,after lpt:", checkLegalState(after_lpt), file=out_file)
            if len(after_lpt) == 0:
                # meaning legalLPT has failed - need the other algorithm
                after_lpt = upperBoundAlg(jobs[1:],new_state)
                if len(after_lpt) == 0:   # upperBoundAlg can't find legal bound
                    upper_bound = 9999999999
                else:   # upperBoundAlg succeeded
                    upper_bound = makeSpan(after_lpt)

            else:   # lpt succeeded
                upper_bound = makeSpan(after_lpt)

            if lower_bound == upper_bound:
                if best_state_makespan > upper_bound:
                    best_state_makespan = upper_bound
                    # print only if there's new best solution
                    printMachineStatOut(after_lpt)
                    best_state = after_lpt
            else:
                if lower_bound < upper_bound and lower_bound < best_state_makespan:
                    bnb(new_state, jobs[1:])


# do a kind of sort/reordring of the jobs to make sure that the all the types has representatives - OPTIONAL
def intialSort():
    types = set()
    first_in_line = {}
    for index, job in enumerate(jobs_list):
        if job.type not in types:
            types.add(job.type)
            first_in_line[index] = job

    for i, job in collections.OrderedDict(sorted(first_in_line.items())).items():
        del jobs_list[i]
        jobs_list.insert(0, job)

    # update jobs numbers
    for i in range(len(jobs_list)):
        jobs_list[i].number = i


# If initial sort is wanted , uncomment the next line
# initailSort()


max_job = max(x.length for x in jobs_list)
avg_job = sum(x.length for x in jobs_list)/num_of_machines

best_state = legalLpt(jobs_list,machines_list)
if len(best_state) != 0:
    best_state_makespan = makeSpan(best_state)
else:
    best_state = upperBoundAlg(jobs_list,machines_list)
    best_state_makespan = makeSpan(best_state)

level_count = [0] * num_of_jobs
start_time = time.time()
bnb(machines_list , jobs_list)

print("***************************************************",file=out_file)
print("***************************************************",file=out_file)
print("BEST STATE IS",file=out_file)
printMachineStatOut(best_state)
print("***************************************************",file=out_file)
print("---Finished in %s seconds ---" % (time.time() - start_time),file=out_file)
print("***************************************************",file=out_file)
print("***************************************************",file=out_file)
for i in range(len(level_count)):
    print("Number of nodes in level",i,":",level_count[i],file=out_file)

out_file.close()
