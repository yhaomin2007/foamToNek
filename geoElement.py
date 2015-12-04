class point:
	# point object,
	# contains pointID and its xyz locations.
	def __init__(self,pointID,x,y,z):
		self.pointID = pointID
		self.x = x
		self.y = y
		self.z = z
		
class face(point):
	# face object
	# contains faceID, four points information.
	def __init__(self,faceID):
		self.faceID = faceID
		self.points = []
		self.ownerCellID = -1
		self.ownerCellNekSequence = -1
		self.neighbourCellID = -1
		self.neighbourCellNekSequence = -1
		self.ifBoundary = False
		self.patchType = None
		self.ifCyclic = False
		self.pFaceID = -1			# periodic faceID
		self.nekWord = 'E' 			# default boundary condition for a element is connecting to another element.
		
		
	def addPoint(self,newPoint):
		self.points.append(newPoint)	# point here is a point object
		if (len(self.points) > 4): print 'error, too much points for a face'
	
	def ownerCell(self,cellID):				# owner cell of this face
		self.ownerCellID = cellID
	
	def ownerCellNek(self,nekSequence):
		self.ownerCellNekSequence = nekSequence
	
	def neighbourCell(self,cellID):			# neighbour cell of this face
		self.neighbourCellID = cellID
		
	def neighbourCellNek(self,nekSequence):
		self.neighbourCellNekSequence = nekSequence

	def addPatchType(self,patchType):		# direct use work in boundary file to specify boundary condition
		self.patchType = patchType
		self.nekWord = self.patchType
		if(patchType == 'P'):
			self.ifCyclic = True
			
class patch():
	def __init__(self,patchID):
		self.patchID = patchID
		self.patchName = ''
		self.patchType = ''
		self.ifCyclic = False
		self.nFaces = -1
		self.startFace = -1
		self.neighbourPatch = None
		self.neighbourPatchName = ''
	
	def patchName(self,patchName):
		self.patchName = patchName
		
	def addPatchType(self,patchType):
		self.patchType = patchType
		if (patchType == 'P'):
			self.ifCyclic = True
			print 'Please specify neighbour patch name'
	
	def nFaces(self,nFaces):
		self.nFaces = nFaces
	
	def startFace(self,startFace):
		self.startFace = startFace
	
	def neighbourPatch(neighbourPatch):
		self.neighbourPatch = neighbourPatch
	
	def neighbourPatchName(neighbourPatchName):	
		self.neighbourPatchName = neighbourPatchName
	

			
class cell(face,point):
	# cell object stores information about cell.
	# including 6 faces, and 6 neighbour cells 
	# 8 vertices.
	# However, the numbering of vertices and faces must follow strict rules required by
	# nek. 
	
	# notes about hex8 format.
	# 1. number of vertices follow the rules in hex8.png
	# 2. normal vector from vertice 1->2->3->4 using right hand should point to the inside of hex.
	# 3. if not, exchange vertice 1,2,3,4 with 5,6,7,8, and exchange face 5 and face 6.
	
	def __init__(self,cellID):
		#print 'initial a cell object'
		self.cellID = cellID
		self.faces = [] 						# face array
		#self.faceNeighbourCellIDs = []			# neighbour cell array
		
		self.faces_nek = []  					# face array in nek sequence.
		self.points_nek = []					# point array in nek sequence.
		#self.faceNeighbourCellIDs_nek = []		# neighbour cell array in nek sequence.
		
			
	def nekorder_flag(flag):
		self.nekorder_flag_ = flag
	def nekorder_flag():
		return self.nekorder_flag_
	
	
	def addFace(self,newFace):
		# add new face object to face array.
		# and new face's corresponding neighbour cell ID.
		
		self.faces.append(newFace)				# newFace is a face object
		#self.faceNeighbourCellIDs.append(neighbourCellID) 
		if (len(self.faces) > 6): print 'error, too much face for a cell'
	
	def initFourPoints(self):
		# make initial four points in order.
		# 1,2,3,4 vertices must be  1 - 2
		#		    			    |	|
		#                           4 - 3
	
		# if 1 - 2
		#    |   |
		#    4 - 3
	    # just return
	        
	    # if 1 - 3   1 - 2
		#    |   |   |   | 
		#    4 - 2   3 - 4 
		# 2 < - > 3
	    	
		# make a line between 1 and 3, if 2,4 are on each side, just return.
		# if 2,4 are on same side, exchange 2 and 3. 
		
		# 1st point
		x1 = self.points_nek[0].x
		y1 = self.points_nek[0].y
		z1 = self.points_nek[0].z
		
		# 2nd point
		x2 = self.points_nek[1].x
		y2 = self.points_nek[1].y
		z2 = self.points_nek[1].z
		
		# 3rd point
		x3 = self.points_nek[2].x
		y3 = self.points_nek[2].y
		z3 = self.points_nek[2].z
		
		# 4th point
		x4 = self.points_nek[3].x
		y4 = self.points_nek[3].y
		z4 = self.points_nek[3].z
		
		vector213 = point(213,(x2-x1)+(x2-x3),(y2-y1)+(y2-y3),(z2-z1)+(z2-z3))
		vector413 = point(413,(x4-x1)+(x4-x3),(y4-y1)+(y4-y3),(z4-z1)+(z4-z3))
		
		dot24 = vector213.x*vector413.x + vector213.y*vector413.y + vector213.z*vector413.z

		if(dot24 < 0):
			return			# if 2,4 are on either side of line13
		else:
			# if not, exchange point 2 and 3
			point2 = self.points_nek[1]
			self.points_nek[1] = self.points_nek[2]
			self.points_nek[3] = self.point2
			return			
	
	
	def makeNekSequence(self):
	
		# convert the sequence of vertices and faces into nek sequence.
		# this must be done after all faces have been added.
		
		if (len(self.faces) != 6): print 'error, not enough faces for a cell, or too much faces for a cell'
		
		# add the first face.
		# this first face is actually the 5th face.
		self.faces_nek.append(self.faces[0])
		self.faces_nek.append(self.faces[0])
		self.faces_nek.append(self.faces[0])
		self.faces_nek.append(self.faces[0])
		self.faces_nek.append(self.faces[0])
		if (self.faces_nek[-1].ownerCellID == self.cellID): self.faces_nek[-1].ownerCellNek(4)
		if (self.faces_nek[-1].neighbourCellID == self.cellID): self.faces_nek[-1].neighbourCellNek(4)
		#print self.faces_nek[-1].faceID, self.faces_nek[-1].ownerCellID,self.faces_nek[-1].neighbourCellID
		
		#self.faceNeighbourself.cellIDs_nek.append(faceNeighbourself.cellIDs[0])
		# add the four points of the first face.
		# However this face is 5th face.
		# 5th face is surround by 1,2,3,4th vertices.
		for i in range(0,4):
			self.points_nek.append(self.faces[0].points[i])
		
		# however, 1,2,3,4 vertices must be  1 - 2
		#									 |	 |
		#                                    4 - 3
		self.initFourPoints() 	
		

		# nek elment vertices and face sequance:
		# 1 - 2    5 - 6
		# |	  | -  |   |
		# 4 - 3    7 - 8
		
		# vertices     face
		# 1,2,6,5       1
		# 2,3,7,6       2
		# 3,4,8,7       3
		# 1,4,8,5       4
		# 1,2,3,4       5
		# 5,6,7,8       6
			
		# adding subsequente faces. 
		# find the 1st face.
		# 1st face share 1,2, points
		for i in range(1,6): # loop over rest faces 
			flag1 = False
			flag2 = False
			for j in range(0,4):	
				# if share 1st point
				if(self.faces[i].points[j].pointID == self.points_nek[0].pointID):
					flag1 = True
					j1 = j
				# if share 2nd point	
				if(self.faces[i].points[j].pointID == self.points_nek[1].pointID):
					flag2 = True
					j2 = j

			if(flag1 and flag2):
				# if this face share 1 and 2 point,
				# then is this face is 1st face.
				i1 = i
				self.faces_nek[0] = self.faces[i]
				if (self.faces_nek[0].ownerCellID == self.cellID): self.faces_nek[0].ownerCellNek(0)
				if (self.faces_nek[0].neighbourCellID == self.cellID): self.faces_nek[0].neighbourCellNek(0)
				
				# 1st face has point 5 and point 6. adding them to points_nek
				for j in range(0,4):
					if ((j==j1) or (j==j2)):
						continue
					self.points_nek.append(self.faces[i].points[j])
				
				# now, we should make 5 and 6 point are in same order.
				# 1 point
				x1 = self.points_nek[0].x
				y1 = self.points_nek[0].y
				z1 = self.points_nek[0].z
		
				# 2 point
				x2 = self.points_nek[1].x
				y2 = self.points_nek[1].y
				z2 = self.points_nek[1].z
					
				# 5 point
				x5 = self.points_nek[4].x
				y5 = self.points_nek[4].y
				z5 = self.points_nek[4].z
		
				# 6 point
				x6 = self.points_nek[5].x
				y6 = self.points_nek[5].y
				z6 = self.points_nek[5].z	
				
				indicator = ((x2-x1)*(x6-x5)+(y2-y1)*(y6-y5)+(z2-z1)*(z6-z5))
				
				if (indicator) > 0 :
					# if in correct order
					# no need to change position
			
					break
				else:
					# if not in correct order
					# exchange point 5 and 6
					point6 = self.points_nek[4]
					self.points_nek[4] = self.points_nek[5]
					self.points_nek[5] = point6
					break
				
		
		
		
		# find the 2nd face.
		# 2nd face share point 2 and 3, and 6
		for i in range(1,6):
			if(i == i1):
				continue
			flag1 = False
			flag2 = False
			for j in range(0,4):
				
				# if share 2nd point
				if(self.faces[i].points[j].pointID == self.points_nek[1].pointID):
					flag1 = True
					j2 = j
				# if share 3rd point	
				if(self.faces[i].points[j].pointID == self.points_nek[2].pointID):
					flag2 = True
					j3 = j
				# if share 6th point
				if(self.faces[i].points[j].pointID == self.points_nek[5].pointID):
					j6 = j

			if(flag1 and flag2):
				# if this face share 2,3,6 point,
				# then is this face is 2nd face.
				i2 = i
				self.faces_nek[1] = self.faces[i]
				if (self.faces_nek[1].ownerCellID == self.cellID): self.faces_nek[1].ownerCellNek(1)
				if (self.faces_nek[1].neighbourCellID == self.cellID): self.faces_nek[1].neighbourCellNek(1)
		
				#self.faceNeighbourCellIDs_nek.append(faceNeighbourCellIDs[i])	
					
				# adding point 7
				for j in range(0,4):
					if ((j==j2) or (j==j3) or (j==j6)):
						continue
					self.points_nek.append(self.faces[i].points[j])
		
		# find the 3rd face.
		# 3rd face share point 3 and 4, and 7
		for i in range(1,6):
			if((i == i1) or (i==i2)):
				continue
			flag1 = False
			flag2 = False
			for j in range(0,4):
				
				# if share 3 point
				if(self.faces[i].points[j].pointID == self.points_nek[2].pointID):
					flag1 = True
					j3 = j
				# if share 4 point	
				if(self.faces[i].points[j].pointID == self.points_nek[3].pointID):
					flag2 = True
					j4 = j
				# if share 7 point
				if(self.faces[i].points[j].pointID == self.points_nek[6].pointID):
					j7 = j

			if(flag1 and flag2):
				# if this face share 2 and 3 point,
				# then is this face is 3rd face.
				i3 = i
				self.faces_nek[2] = self.faces[i]
				if (self.faces_nek[2].ownerCellID == self.cellID): self.faces_nek[2].ownerCellNek(2)
				if (self.faces_nek[2].neighbourCellID == self.cellID): self.faces_nek[2].neighbourCellNek(2)
		
				#self.faceNeighbourCellIDs_nek.append(faceNeighbourCellIDs[i])	
					
				# adding point 8
				for j in range(0,4):
					if ((j==j3) or (j==j4) or (j==j7)):
						continue
					self.points_nek.append(self.faces[i].points[j])
					# now, all points has been added to self.points_nek
					
		# find the 4th face.
		# 4th face share point 1 and 4
		for i in range(1,6):
			if((i == i1) or (i==i2) or (i==i3)):
				continue
			flag1 = False
			flag2 = False
			for j in range(0,4):
				
				# if share 1 point
				if(self.faces[i].points[j].pointID == self.points_nek[0].pointID):
					flag1 = True
				# if share 4 point	
				if(self.faces[i].points[j].pointID == self.points_nek[3].pointID):
					flag2 = True
			
			if(flag1 and flag2):
				# if this face share 1 and 2 point,
				# then is this face is 5th face.
				i4 = i
				self.faces_nek[3] = self.faces[i]
				if (self.faces_nek[3].ownerCellID == self.cellID): self.faces_nek[3].ownerCellNek(3)
				if (self.faces_nek[3].neighbourCellID == self.cellID): self.faces_nek[3].neighbourCellNek(3)
		
				# no need to add point, as all points are added	
		
		# find the 6th face.
		for i in range(1,6):
			if((i == i1) or (i == i2) or (i==i3) or (i==i4)):
				continue
			
			# must use append, since not declared
			self.faces_nek.append(self.faces[i])
			if (self.faces_nek[-1].ownerCellID == self.cellID): self.faces_nek[-1].ownerCellNek(5)
			if (self.faces_nek[-1].neighbourCellID == self.cellID): self.faces_nek[-1].neighbourCellNek(5)
	
	def checkTopoSequence(self):
		# in this function,  the topology of cell is checked. 
		# 
		
		#self.faces_nek
		#self.points_nek
		
		# 1. obtain normal vector of plane 1234. v1234 using right hand rule
		# 2. obtain vector 15. v15
		# 3. if v15*v1234 > 0, then ok.
		# if not, exchange points 1,2,3,4, and points 5,6,7,8 in points_nek, and exchange face 5 and 6 in faces_nek.
		point1 = self.points_nek[0]
		point2 = self.points_nek[1]
		point3 = self.points_nek[2]
		point4 = self.points_nek[3]
		point5 = self.points_nek[4]
		point6 = self.points_nek[5]
		point7 = self.points_nek[6]
		point8 = self.points_nek[7]
		
		# vector 12,14 are point1->point2, and point1->point4
		v12 = point(12,point2.x-point1.x,point2.y-point1.y,point2.z-point1.z)
		v14 = point(14,point4.x-point1.x,point4.y-point1.y,point4.z-point1.z)
		
		# normal vector from v12, and v14
		nv1234 = point(1234,v12.y*v14.z-v12.z*v14.y,v12.z*v14.x-v12.x*v14.z,v12.x*v14.y-v12.y*v14.x)
		
		v15 = point(15,point5.x-point1.x,point5.y-point1.y,point5.z-point1.z)
		
		flag = v15.x*nv1234.x + v15.y*nv1234.y + v15.z*nv1234.z
		
		if (flag > 0):
			return
		
		# exchange points
		self.points_nek[0] = point5 
		self.points_nek[1] = point6 
		self.points_nek[2] = point7
		self.points_nek[3] = point8

		self.points_nek[4] = point1 
		self.points_nek[5] = point2 
		self.points_nek[6] = point3
		self.points_nek[7] = point4 
		
		# exchange face 5 and 6
		face6 = self.faces_nek[4]
		self.faces_nek[4] = self.faces_nek[5]
		self.faces_nek[5] = face6
		
		if (self.faces_nek[4].ownerCellID == self.cellID): self.faces_nek[4].ownerCellNek(4)
		if (self.faces_nek[4].neighbourCellID == self.cellID): self.faces_nek[4].neighbourCellNek(4)
		
		if (self.faces_nek[5].ownerCellID == self.cellID): self.faces_nek[5].ownerCellNek(5)
		if (self.faces_nek[5].neighbourCellID == self.cellID): self.faces_nek[5].neighbourCellNek(5)