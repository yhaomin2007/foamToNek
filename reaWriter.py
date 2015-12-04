# reaWriter.py
from geoElement import *
import sys


def reaWriter(reaFile,newReaFile,points,faces,cells):
	# write mesh information into rea file.
	# 1. read .rea file
	# 2. extract part before and after mesh information.
	# 3. write element vertices information
	# 4. write element boundary information
	# 5. rewrite .rea file
	
	print 'writing new .rea file'
	
	reaFileHolder = open(reaFile,'rw')
	wholeReaFile = reaFileHolder.read()
	
	newReaFileHolder = open(newReaFile,'w')
	newReaFileHolder.seek(0)
#	newReaFileHolder.write(newRea)
#	newReaFileHolder.close()
	
	
	
	newRea = wholeReaFile[:wholeReaFile.find('**MESH')-1]
	
	newRea = newRea + ' **MESH DATA** 6 lines are X,Y,Z;X,Y,Z. Columns corners 1-4;5-8\n'

	newRea = newRea + '         '+str(len(cells))+'  3         '+str(len(cells))+'           NEL,NDIM,NELV\n'

	newReaFileHolder.write(newRea)
	newRea = ''
	
	for i in range(0,len(cells)):
		cell = cells[i]
		print 'write element ',i
		# write cells information into rea file. each cell is regarded as an element in nek
		
		newRea = newRea + '            ELEMENT     '+str(i+1).rjust(7)+' [    1a]  GROUP  0\n'
		# adding x
		newRea = (newRea + format(cell.points_nek[0].x,'f').rjust(10) + format(cell.points_nek[1].x,'f').rjust(14)
			+ format(cell.points_nek[2].x,'f').rjust(14) + format(cell.points_nek[3].x,'f').rjust(14) +'\n')
		# adding y
		newRea = (newRea + format(cell.points_nek[0].y,'f').rjust(10) + format(cell.points_nek[1].y,'f').rjust(14)
			+ format(cell.points_nek[2].y,'f').rjust(14) + format(cell.points_nek[3].y,'f').rjust(14) +'\n')
		# adding z
		newRea = (newRea + format(cell.points_nek[0].z,'f').rjust(10) + format(cell.points_nek[1].z,'f').rjust(14)
			+ format(cell.points_nek[2].z,'f').rjust(14) + format(cell.points_nek[3].z,'f').rjust(14) +'\n')
		# adding x
		newRea = (newRea + format(cell.points_nek[4].x,'f').rjust(10) + format(cell.points_nek[5].x,'f').rjust(14)
			+ format(cell.points_nek[6].x,'f').rjust(14) + format(cell.points_nek[7].x,'f').rjust(14) +'\n')
		# adding y
		newRea = (newRea + format(cell.points_nek[4].y,'f').rjust(10) + format(cell.points_nek[5].y,'f').rjust(14)
			+ format(cell.points_nek[6].y,'f').rjust(14) + format(cell.points_nek[7].y,'f').rjust(14) +'\n')
		# adding z
		newRea = (newRea + format(cell.points_nek[4].z,'f').rjust(10) + format(cell.points_nek[5].z,'f').rjust(14)
			+ format(cell.points_nek[6].z,'f').rjust(14) + format(cell.points_nek[7].z,'f').rjust(14) +'\n')
		newReaFileHolder.write(newRea)
		newRea = ''
	# all elements are written.
	
	newRea = newRea + '  ***** CURVED SIDE DATA *****\n'
	newRea = newRea + '  0 Curved sides follow IEDGE,IEL,CURVE(I),I=1,5, CCURVE\n'
	newRea = newRea + ' ***** BOUNDARY CONDITIONS *****\n  ***** FLUID   BOUNDARY CONDITIONS *****\n'
	newReaFileHolder.write(newRea)
	newRea = ''
	
	# write faces connection information
	for i in range(0,len(cells)):
		cell = cells[i]
		print 'write faces for element ',i
		for j in range(0,6):
			face = cell.faces_nek[j]
			newRea = newRea + ' ' + face.nekWord
			
			k = 5
			if ((i+1) > 999): k = 6
			if ((i+1) > 9999): k = 7
			#if (len(cells) > 100000):
			#	print 'WARNING: too many elements (more than 1E6)'
			#	sys.exit()
			
			newRea = newRea + str(i+1).rjust(k) + str(j+1).rjust(3)
			
			if(face.ifCyclic):
				# if cyclic face
				neighbourFace = faces[face.pFaceID]
				#newRea = newRea + str(neighbourFace.ownerCellID+1).rjust(10) + str(neighbourFace.ownerCellNekSequence+1).rjust(14)+'\n'
				newRea = newRea + format(neighbourFace.ownerCellID+1,'.5f').rjust(14) + format(neighbourFace.ownerCellNekSequence+1,'.5f').rjust(14)+'\n'
				
			else:
				# if not cyclic face
				
				if(face.ownerCellID == i):
					newRea = newRea + format(face.neighbourCellID+1,'.5f').rjust(14) + format(face.neighbourCellNekSequence+1,'.5f').rjust(14)+'\n'
				else:
					newRea = newRea + format(face.ownerCellID+1,'.5f').rjust(14) + format(face.ownerCellNekSequence+1,'.5f').rjust(14)+'\n'
		
		newReaFileHolder.write(newRea)
		newRea = ''
	'''
	for i in range(0,len(faces)):
		face = faces[i]
		
		if(face.ifCyclic):
			# if this face is cylic(periodic)
			neighbourFace = faces[face.pFaceID]
			newRea = newRea + ' ' + face.nekWord
			newRea = newRea + str(face.ownerCellID+1).rjust(6) + str(face.ownerCellNekSequence+1).rjust(6)
			newRea = newRea + str(neighbourFace.ownerCellID+1).rjust(6) + str(neighbourFace.ownerCellNekSequence+1).rjust(6)+'\n'
		else:
			newRea = newRea + ' ' + face.nekWord
			newRea = newRea + str(face.ownerCellID+1).rjust(6) + str(face.ownerCellNekSequence+1).rjust(6)
			newRea = newRea + str(face.neighbourCellID+1).rjust(6) + str(face.neighbourCellNekSequence+1).rjust(6)+'\n'
	'''
	
	newRea = newRea + '  ***** NO THERMAL BOUNDARY CONDITIONS *****\n'
	
	newRea = newRea + wholeReaFile[wholeReaFile.find('0 PRESOLVE/RESTART OPTIONS  *****')-10:]
	
	newReaFileHolder.write(newRea)
	newRea = ''
	
	reaFileHolder.close()
	 
#	newReaFileHolder = open(newReaFile,'w')
#	newReaFileHolder.seek(0)
#	newReaFileHolder.write(newRea)
	newReaFileHolder.close()
	print 'new .rea file done'