#!/usr/bin/env python

#---------------------------------------------------------------------------
## VulaSHAKA (Simultaneous Neutronic, Fuel Performance, Heat And Kinetics Analysis)
## Copyright (C) 2009-2010 Pebble Bed Modular Reactor (Pty) Limited (PBMR)
## 
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
## 
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.
## 
## See https://vulashaka.svn.sourceforge.net/svnroot/vulashaka
##
## Author : Alexey PETROV
##


#---------------------------------------------------------------------------
import sys, os
from Foam import FOAM_VERSION,  FOAM_BRANCH_VERSION, FOAM_REF_VERSION
if FOAM_VERSION( "<=", "010401" ):
   if __name__ == "__main__" :
      argv = sys.argv
      if len( argv ) > 1 and argv[ 1 ] == "-test":
         argv = None
         test_dir= os.path.join( os.environ[ "PYFOAM_TESTING_DIR" ],'cases', 'local', 'r1.4.1-dev', 'icoFoam' )
         argv = [ __file__, test_dir, 'cavity' ]
         pass
      from Foam.applications.solvers.incompressible.r1_4_1_dev.icoFoam import main_embedded
      os._exit( main_embedded( len( argv ), argv ) )
   else:
      from Foam.applications.solvers.incompressible.r1_4_1_dev.icoFoam import *
      pass
   pass
pass


#-------------------------------------------------------------------------------------------------
if FOAM_REF_VERSION( "==", "010500" ):
   if __name__ == "__main__" :
      argv = sys.argv
      if len( argv ) > 1 and argv[ 1 ] == "-test":
         argv = None
         test_dir= os.path.join( os.environ[ "PYFOAM_TESTING_DIR" ],'cases', 'local', 'r1.5', 'icoFoam', 'cavity' )
         argv = [ __file__, "-case", test_dir ]
         pass
      from Foam.applications.solvers.incompressible.r1_5.icoFoam import main_standalone
      os._exit( main_standalone( len( argv ), argv ) )
      pass
   else:
      from Foam.applications.solvers.incompressible.r1_5.icoFoam import *
      pass
   pass


#-------------------------------------------------------------------------------------------------
if FOAM_BRANCH_VERSION( "dev", "==", "010500" ):
   if __name__ == "__main__" :
      argv = sys.argv
      if len( argv ) > 1 and argv[ 1 ] == "-test":
         argv = None
         test_dir= os.path.join( os.environ[ "PYFOAM_TESTING_DIR" ],'cases', 'propogated', 'r1.5-dev', 'icoFoam', 'cavity' )
         argv = [ __file__, "-case", test_dir ]
         pass
      from Foam.applications.solvers.incompressible.r1_5_dev.icoFoam import main_standalone
      os._exit( main_standalone( len( argv ), argv ) )
      pass
   else:
      from Foam.applications.solvers.incompressible.r1_5_dev.icoFoam import *
      pass
   pass


#-------------------------------------------------------------------------------------------------
if FOAM_VERSION( ">=", "010600" ):
   if __name__ == "__main__" :
      argv = sys.argv
      if len( argv ) > 1 and argv[ 1 ] == "-test":
         argv = None
         test_dir= os.path.join( os.environ[ "PYFOAM_TESTING_DIR" ],'cases', 'propogated', 'r1.6', 'incompressible', 'icoFoam', 'cavity' )
         argv = [ __file__, "-case", test_dir ]
         pass
      from Foam.applications.solvers.incompressible.r1_6.icoFoam import main_standalone
      os._exit( main_standalone( len( argv ), argv ) )
      pass
   else:
      from Foam.applications.solvers.incompressible.r1_6.icoFoam import *
      pass
   pass

    
#--------------------------------------------------------------------------------------

