import json
from analysis.utils import Utils
import time
from math import ceil
import subprocess
from mpi4py import MPI

class TwitterRegionAnalysis:

    sydGridObj = {}
    inputFileName = ''
    languageFile = {}


    def __init__(self,sydGridFile,inputFileName,languageFile,tmpFilesPath):
        
        '''Gather information about input files from command line arguments'''

        self.sydGridObj = Utils.processGridObject(sydGridFile) #create a location grid object
        self.inputFileName = inputFileName #get bigTwitter.json filename information
        self.languageFile = json.load(open(languageFile)) #create a language object using twitter language code information
        self.tmpFilesPath=tmpFilesPath
        self.analysisController() #invoke the master child process


    def analysisController(self):
        
        '''Responsible to parallelize the flow between master and child process'''

        comm = MPI.COMM_WORLD #communicator object
        rank = comm.Get_rank() #rank of each core

        if rank == 0: #first rank is assigned to Master
           self.masterProcessor(comm)
        else:       
            self.childProcessor(comm)

    def masterProcessor(self,comm):

        '''Responsible to process the tweets and combine data from child nodes to form final output'''

        size = comm.Get_size() #total number of ranks in the comm object
        rank = comm.Get_rank()
        if size > 1:
            numberOfLines=int(subprocess.check_output("wc -l "+self.inputFileName,shell=True).split()[0])
            subprocess.call("rm -rf "+self.tmpFilesPath+"/*",shell=True)
            subprocess.call("split -d -a 1 -l "+str(ceil(numberOfLines/size))+" "+self.inputFileName+" "+self.tmpFilesPath+"/segment",shell=True)
            for i in range(size - 1):
                comm.send('Start_Process', dest = (i+1), tag=(i+1))
            finalOutput = Utils.processTweets(comm,self.tmpFilesPath+"/segment"+str(rank),self.sydGridObj,self.languageFile)
        else:
            finalOutput = Utils.processTweets(comm,self.inputFileName,self.sydGridObj,self.languageFile)

        
        combinedData = []
        combinedData.append(finalOutput) #add processed tweets results from the master processor

        if size > 1: #if the resource allocation is not 1 node 1 core
            combinedData.extend(self.combineChildData(comm)) #combine child data
                    
        #Printing Results
        print("Aggregated Results:")
        start=time.time()
        Utils.mergeResults(combinedData)
        print("Time to merge: ",time.time()-start) #time to merge the data from master and child processors

    def childProcessor(self,comm):

        '''Responsible to parallely execute the tweet analysis in different cores based on rank'''

        rank = comm.Get_rank()
        #wait to recieve start process message from master process
        while True:
            command = comm.recv(source = 0, tag = rank)
            if command == 'Start_Process':
                final_child_output = Utils.processTweets(comm,self.tmpFilesPath+"/segment"+str(rank),self.sydGridObj,self.languageFile)
                break

        #wait to receive message from combine function
        while True:

            command = comm.recv(source = 0, tag = rank)
           # Pass tweet analysis results from each processor
            if command == 'Send_Collected_Data':
                comm.send(final_child_output, dest=0, tag=0)
                exit(0)
            

    
    def combineChildData(self,comm):

        childData = []
        size = comm.Get_size()
        #Pass request to send analyzed data from each child processor
        for i in range(size - 1):
            comm.send('Send_Collected_Data', dest = (i+1), tag=(i+1))

        #Append the results from the child processors
        for i in range(size-1):
            childData.append(comm.recv(source=(i+1),tag=0))

        return childData