import linecache
from geoElement import *

def pointsConstructor(pointsFile):
	# construct an array of object point that contains all points in points file.
	points = []
	
	# read how many points
	n = int(linecache.getline(pointsFile,19))
	print 'there is ' + str(n) + ' points'
	
	for i in range(0,n):
		line = linecache.getline(pointsFile,21+i)
		x = float(line[1:-2].split()[0])
		y = float(line[1:-2].split()[1])
		z = float(line[1:-2].split()[2])
	 	#print x,y,z
	 	
	 	newPoint = point(i,x,y,z)
	 	points.append(newPoint)
	
	linecache.clearcache()	
	return points
	
def facesConstructor(facesFile,boundaryFile,ownerFile,neighbourFile,points):
	# construct an array of object faces
	faces = []
	
	# read how many faces
	n = int(linecache.getline(facesFile,19))
	print 'there is ' + str(n) + ' faces'

	for i in range(0,n):
		line = linecache.getline(facesFile,21+i)
		newFace = face(i) # construct new face object.
		for j in range(0,4):
			pointNumber = int(line[2:-2].split()[j])
			#print pointNumber
			newPoint = points[pointNumber]
			#print newPoint.x,newPoint.y,newPoint.z,newFace.faceID
			newFace.addPoint(newPoint)
		faces.append(newFace)
	
	linecache.clearcache()
	
	# read owner file
	for i in range(0,n):
		line = linecache.getline(ownerFile,22+i)
		cellID = int(line)				
		faces[i].ownerCell(cellID)
	
	# read neighbour file
	n = int(linecache.getline(neighbourFile,20))
	print 'there is ' + str(n) + ' faces in neighbour file'
	for i in range(0,n):
		line = linecache.getline(neighbourFile,22+i)
		cellID = int(line)				
		faces[i].neighbourCell(cellID)
		
	# now, add boundary information into face in faces.
	n = int(linecache.getline(boundaryFile,18))
	print 'there is ' + str(n) + ' boundaries'

	# patches contains all patches as a patch object
	patches = []
	lineIndicator = 20
	# 
	for i in range(0,n):
		newPatch = patch(i)
		line = linecache.getline(boundaryFile,lineIndicator)
		# adding patch name
		newPatch.patchName = line.strip()
		
		lineIndicator = lineIndicator +2
		line = linecache.getline(boundaryFile,lineIndicator)
		# adding patch type
		newPatch.addPatchType(line[:-2].split()[1])
		
		lineIndicator = lineIndicator +1
		line = linecache.getline(boundaryFile,lineIndicator)
		newPatch.nFaces = int(line[:-2].split()[1])
		
		
		lineIndicator = lineIndicator +1
		line = linecache.getline(boundaryFile,lineIndicator)
		newPatch.startFace = int(line[:-2].split()[1])
	
		if(newPatch.ifCyclic):
			lineIndicator = lineIndicator +2
			line = linecache.getline(boundaryFile,lineIndicator)
			# adding neighbour patch name
			newPatch.neighbourPatchName = line[:-2].split()[1]
			print 'neighbourPatchName is ',newPatch.neighbourPatchName
		
		lineIndicator = lineIndicator +2
		patches.append(newPatch)
	
	# now, all patches has been added to paches.
	# find cyclic neighbour patch.
	for i in range(0,n):
		for j in range(0,n):
			if (patches[i].neighbourPatchName == patches[j].patchName):
				patches[i].neighbourPatch = patches[j]
	
	
	for i in range(0,n):
		nFaces = patches[i].nFaces
		startFace = patches[i].startFace
		
		for j in range(startFace,startFace+nFaces):
			faces[j].ifBoundary = True
			faces[j].addPatchType(patches[i].patchType) # forward patchType from patch to face
			
			if(faces[j].ifCyclic):	# if this face is cyclic, find its cyclic face ID
				faces[j].pFaceID = (j - startFace)+ patches[i].neighbourPatch.startFace
				
	linecache.clearcache()
	return faces	
	
	
def cellsConstructor(ownerFile,neighbourFile,faces):
	
	n = 0 
	for face in faces:
		if(face.ownerCellID > n): n = face.ownerCellID
	print 'there are ' + str(n+1)+ ' cells in total'
	
	# construct an array of object cell
	print 'constructing cell list'
	cells = []
	
	for i in range(n+1):
		cellID = i
		print 'create cell ',i
		newCell = cell(cellID)
		# find faces that attach to this cell.
		for face in faces:		
			if (face.ownerCellID == cellID):
				newCell.addFace(face)
				#print 'add a new face to cell, owner cell faceID is ', face.faceID, face.ownerCellID
			if (face.neighbourCellID == cellID):
				newCell.addFace(face)
				#print 'add a new face to cell, neighbour cell faceID is ', face.faceID, face.neighbourCellID

		# make faces in nek sequence		
		newCell.makeNekSequence()
		newCell.checkTopoSequence()
		cells.append(newCell)

	# after cell list is contructed, call function to make numbering of faces and points consistent. 
	
	return cells


