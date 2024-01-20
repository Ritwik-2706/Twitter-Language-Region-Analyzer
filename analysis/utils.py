import json
import operator
import time
class Utils:
    
    def processGridObject(sydGridJson):
        
        '''Process sydGrid.json and create a sydGrid object of the required format with location grids A1,A2 etc.'''
        
        sydGrid=json.load(open(sydGridJson))
        sydGrid=sorted(sydGrid['features'], key=lambda d: (-d['geometry']['coordinates'][0][2][1],d['geometry']['coordinates'][0][0][0]))
        gridObj=[]
        char='A'
        id=1
        for grid in sydGrid:
            st=char
            if(id%4==0): 
                grid['properties']['id']=st+str(4)
                char=chr(ord(char)+1)
            else:
                grid['properties']['id']=st+str(id%4)
            grid['properties']['xmin']=grid['geometry']['coordinates'][0][0][0]
            grid['properties']['xmax']=grid['geometry']['coordinates'][0][2][0]
            grid['properties']['ymin']=grid['geometry']['coordinates'][0][2][1]
            grid['properties']['ymax']=grid['geometry']['coordinates'][0][0][1]
            gridObj.append(grid['properties'])
            id+=1
        return gridObj

    def getTweetRegion(tweet,gridObj):

        '''Obtain location grid information for the tweet '''

        x = tweet['coordinates'][0]
        y = tweet['coordinates'][1]
        for region in gridObj:
            if (x >= region['xmin']) and (x <= region['xmax']):
                if (y > region['ymin']) and (y <= region['ymax']):
                    tweet['grid']=region['id']
                    break
        return tweet

    def updateRegionDict(tweet,regionDict):

        '''Update the count based on language'''

        if tweet['grid'] in regionDict.keys():
            if tweet['lang'] in regionDict[tweet['grid']]:
                regionDict[tweet['grid']][tweet['lang']]+=1
            else:
                regionDict[tweet['grid']][tweet['lang']]=1
        else:
            regionDict[tweet['grid']]={tweet['lang']:1}
        return regionDict

    def getLang(tweet,langObj):

        '''Obtain language information for the tweet'''

        if tweet["doc"]["lang"] in langObj.keys():
            return langObj[tweet["doc"]["lang"]]
        elif tweet["doc"]["lang"]=='und':
            return None
        else:
            return tweet["doc"]["lang"]
    
    def processTweets(comm,jsonFile,gridObj,langObj):

        '''Responsible to analyze tweets and find the associated region and language'''

        rank=comm.Get_rank()
        size=comm.Get_size()
        regionDict={}
        start=time.time()
        #To read selected lines line by line
        with open(jsonFile,encoding="utf-8") as tweetData:
            for lineNum,line in enumerate(tweetData):
                if (lineNum!=0):
                    try:
                        if line[-2:] == ",\n":
                            line = line[:-2]
                        if line[-3:]=="]}\n":
                            line = line[:-3]
                        if (line=="\n")|(line==""):
                            continue
                        tweet=json.loads(line)
                        if((tweet['doc']['coordinates'] is not None) & (tweet["doc"]["lang"]!='und')):
                            lang=Utils.getLang(tweet,langObj) #get language information from tweet
                            if(lang!=None):
                                tweet={"id":tweet['id'],"lang":lang,'coordinates':tweet['doc']['coordinates']['coordinates']}
                                tweet=Utils.getTweetRegion(tweet,gridObj) #get region information of the tweet
                                if("grid" in tweet.keys()):
                                    regionDict=Utils.updateRegionDict(tweet,regionDict)
                    except Exception as e:
                        print("Error in line:",lineNum,"\n Error:",str(e),"\n Line:",line)
                        continue

        print("Completed Job:",rank, "Time to process tweets:",time.time()-start)
        return regionDict

    def mergeResults(regionDictArray):

        '''Responsible to merge results from the child and master processor to create the final output json'''

        finalDict={}
        for regionDict in regionDictArray:
            for region in regionDict.keys():
                if region in finalDict.keys():
                    for lang in regionDict[region].keys():
                        if lang in finalDict[region].keys():
                            finalDict[region][lang]+=regionDict[region][lang]
                        else:
                            finalDict[region][lang]=regionDict[region][lang]
                else:
                    finalDict[region]=regionDict[region]
        resultDict={}

        ##Display Prettified Results
        for region in finalDict.keys():
            resultDict[region]={}
            # resultDict[region]['lang']=finalDict[region]
            resultDict[region]['totalCount']=sum(finalDict[region].values())
            resultDict[region]['langCount']=len(finalDict[region].values())
            resultDict[region]['top10Lang']=json.dumps(sorted(finalDict[region].items(),key=operator.itemgetter(1),reverse=True)[0:10])
        resultDict=sorted(resultDict.items(),key=operator.itemgetter(0))
        print ("{:<10} {:<25} {:<25} {:<25}".format('Cell', '#Total Tweets', '#Number of languages used', '#Top 10 Languages & #Tweets'))
        for key, value in resultDict:
            print ("{:<10} {:<25} {:<25} {:<25}".format(key, value['totalCount'], value['langCount'], value['top10Lang']))