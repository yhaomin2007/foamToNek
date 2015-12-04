#=========================================================================================
# module
import os
from geoElement import *
from arrayConstructor import *
from reaWriter import *
#=========================================================================================
# files
polymesh = os.getcwd()+'/foamBox/constant/polyMesh/'
pointsFile = polymesh + 'points'
facesFile = polymesh + 'faces'
ownerFile = polymesh + 'owner'
neighbourFile = polymesh + 'neighbour'
boundaryFile = polymesh + 'boundary'
nekCase = os.getcwd()+ '/3dbox/'
reaFile = nekCase + 'base.rea'
newReaFile = nekCase + 'new.rea'
#=========================================================================================
# 1. construct points array
# 2. construct faces array
# 3. construct cells array

points = pointsConstructor(pointsFile)

faces = facesConstructor(facesFile,boundaryFile,ownerFile,neighbourFile,points)

cells = cellsConstructor(ownerFile,neighbourFile,faces)

#=========================================================================================
# 4. write rea file

reaWriter(reaFile,newReaFile,points,faces,cells)