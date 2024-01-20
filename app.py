import sys
import time
from analysis.twitterRegionAnalysis import TwitterRegionAnalysis

def main(argv):

    '''Invocation function - Gathers information about the bigTwitter, sydGrid, language file and temp folder to invoke Twitter Region Analysis'''
    
    inputFileName = argv[1]
    sydGridFile = argv[2]
    langFile = argv[3]
    tmpFilesPath=argv[4]

    start=time.time() 

    TwitterRegionAnalysis(sydGridFile,inputFileName,langFile,tmpFilesPath) #to process and analyze the bigTwitter file and store the output 

    end=time.time()

    print("Time taken:",end-start, " secs") #to calculate the actual processing time (secs), excluding the queue time

    
if __name__ == '__main__':
    main(sys.argv[0:]) #read command line arguments
