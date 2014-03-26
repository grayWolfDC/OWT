import numpy as np
#from sklearn.cluster import KMeans 

#def randrange(n,vmin,vmax):
 #   return(vmax - vmin) * np.random.rand(n) + vmin
 
#def plotter(myDat,figNum,feat,**kwargs ):
#    from mpl_toolkits.mplot3d import Axes3D
#    import matplotlib.pyplot as plt
    #fig = plt.figure(figNum)
    #ax = fig.add_suplot(111,projection='3d')
    ## needs some means of converting flag to point color in hex
    ## or maybe require the user to set/enter it manually
    #availColors= ['#000000','#ff0000','#00ff00','#0000ff']
    #if "centroids" in kwargs:
    #    centroids = kwargs["centroids"]
    #    cshape=centroids.shape
    #    #get from cshape number of centroids
    #if "cFlag" in kwargs:
    #    cFlag = kwargs["cFlag"]
    #    c = availColors(cFlag)
    #    pass
    #else:
    #    c='#000000'
    #m = 'o'
    #ax.scatter(myDat[:,0],myDat[:,1],myDat[:,2],c=c,marker=m)
    #ax.set_xlabel(feat[0])
    #ax.set_ylabel(feat[1])
    #ax.set_zlabel(feat[2])
    #plt.draw()
    #pass
    
def findDist(array1,array2):
    # Given array1, an array of size m1xn
    # and array2, an array of size m2xn
    # where the magnitudes of m1 and m2 represent the number of 
    # points in their respective arrays and the magnitude of n 
    # is equal to the number of dimensions in which these points are 
    # represented.
    # The function returns a distance array of size m1xm2, containing 
    # the distance of each point in array 1 to each points in array 2
    from scipy.spatial.distance import cdist
    dist = cdist(array1,array2)
    return dist
    
def updateFlag(distArray):
    newFlag = np.argmin(distArray,axis=1)
    return newFlag
    
#def main():
def owt_kmeans():
    ts = np.loadtxt('training.txt')
    #for c,m,zl,zh in [('r','o', -50, -25),('b','^',-30,-5)]:
    #    xs = randrange(n,23,32)
    #    ys = randrange(n,0,100)
    #    zs = randrange(n,zl,zh)
    #    ax.scatter(xs,ys,zs,c=c,marker=m)
    myDat = ts[:,2:5]#features = ['443nm','510nm','555nm']
    dataShape = myDat.shape
    # begin clustering
    # -> will need something to determine the right numbers of clusters to fit
    
    #intialize some useful variables
    numClusters = 3 # number of clusters to shoot for
    tol = 0.001 # change limit below which the program stops
    centChng = 1 # difference between the greatest of the distances between the previous
            #      centroid positions and the corresponding updated positions.
    # get data range in all dimensions:
    [minX,minY,minZ] = myDat.min(axis=0)
    [maxX,maxY,maxZ] = myDat.min(axis=0)

    # initialize cluster centroids previous positions
    cXold = np.random.uniform(low=minX,high=maxX,size=(numClusters,1))
    cYold = np.random.uniform(minY,maxY,(numClusters,1))
    cZold = np.random.uniform(minZ,maxZ,(numClusters,1))
    # empty-initialize cluster centroids next position
    cXnew = np.empty_like(cXold)
    cYnew = np.empty_like(cYold)
    cZnew = np.empty_like(cZold)

    # organize centroid coordinates into a single array
    #  column 1: X, column 2: Y, column 3: Z
    oldCentXYZ = np.hstack((cXold,cYold,cZold))                       
    newCentXYZ = np.hstack((cXnew,cYnew,cZnew))
    # initialize clusterFlag
    clusterFlag = np.zeros(dataShape[0])
    
    # plotinitial conditions here
    # plot all points (they will be plotted in black
    # plot 
    while centChng > tol:
        # Two steps
        # A - based on initial cluster centroid positions, initialize cluster membership
        #     for all points, and color them accordingly.
        #     To do that: 
        #       1 - Calculate distance of each point to all old centroids
        distArray = findDist(myDat,oldCentXYZ)
	#       2 - Select the shortest distance
        #       3 - Flag the point for the corresponding cluster
        clusterFlag = updateFlag(distArray)    
        # B - calculate new centroid position based on cluster membership
        # To do that:
        #    1 - cycle through all flags
        flag = min(clusterFlag)
        
        while flag < numClusters:
       
            #    2 - for each flag:
            #        identify member points
            pts = myDat[np.nonzero(clusterFlag==flag),:]
            #   3 - update the centroid position 
            # column-wise mean of pts yields the new position of that centroid 
            newCentXYZ[flag,:] = np.mean(pts,axis=1)
            flag += 1            
            # end of while (flag) loop
        # update centChng
        centChng = max(np.diag(findDist(oldCentXYZ,newCentXYZ)))
        oldCentXYZ = newCentXYZ
        # update plot
    # end of while (tol) loop
    return oldCentXYZ   
#if __name__ == "__main__":
#    cenXYZ = main()
