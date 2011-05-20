## pythonFlu - Python wrapping for OpenFOAM C++ API
## Copyright (C) 2010- Alexey Petrov
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
## See http://sourceforge.net/projects/pythonflu
##
## Author : Alexey PETROV
##


#--------------------------------------------------------------------------------------
def PtrList( Type ):
    def PtrList_init_Istream_iNew( is_, inewt ):
        #This function is constructor for PtrList(from Istream and Inew). But we not use OpenFOAM's PtrList,
        #we use Python's list. The reference code you can see in OpenFOAM "PtrListIO.C"
        from Foam.OpenFOAM import token
        firstToken = token(is_);
   
        is_.fatalCheck("PtrList<T>::read(Istream& is, const INew& inewt) : reading first token" )
    
        result = []
        if firstToken.isLabel():
           #  Read size of list
           s = firstToken.labelToken()
       
           # Read beginning of contents
           listDelimiter = is_.readBeginList("PtrList")
           
           if s:
              if listDelimiter == token.BEGIN_LIST:
                 for index in range(s):
                     result.append( inewt( is_ ) )
                     is_.fatalCheck( "PtrList<T>::read(Istream& is, const INew& inewt) : reading entry" )
              else:
                 result.append( inewt( is_ ) )
                 is_.fatalCheck( "PtrList<T>::read(Istream& is, const INew& inewt) : reading the single entry" ) 

                 for index in range(s):
                     result.append( inewt( is_ ).clone() )
                    
           is_.readEndList("PtrList")
    
        elif firstToken.isPunctuation():
           if firstToken.pToken() != token.BEGIN_LIST:
              raise IOError("incorrect first token, '(', found %s" %firstToken.info() )
       
           lastToken = token (is_)
       
           sllPtrs = []
       
           while not ( lastToken.isPunctuation() and lastToken.pToken() == token.END_LIST ):
              is_.putBack( lastToken )
              sllPtrs.append( inewt(is_) )
              is_ >> lastToken
       
           for index in range( len( sllPtrs ) ):
               result.append( sllPtrs[ index ] )
           
        else:
           raise IOError("incorrect first token, expected <int> or '(', found %s" %firstToken.info() )

        return result

    return PtrList_init_Istream_iNew
    
    
#--------------------------------------------------------------------------------------

