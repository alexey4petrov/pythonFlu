//  VulaSHAKA (Simultaneous Neutronic, Fuel Performance, Heat And Kinetics Analysis)
//  Copyright (C) 2009-2010 Pebble Bed Modular Reactor (Pty) Limited (PBMR)
//  
//  This program is free software: you can redistribute it and/or modify
//  it under the terms of the GNU General Public License as published by
//  the Free Software Foundation, either version 3 of the License, or
//  (at your option) any later version.
//  
//  This program is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU General Public License for more details.
//  
//  You should have received a copy of the GNU General Public License
//  along with this program.  If not, see <http://www.gnu.org/licenses/>.
//
//  See https://vulashaka.svn.sourceforge.net/svnroot/vulashaka
//
//  Author : Alexey PETROV


//---------------------------------------------------------------------------
#ifndef common_hxx
#define common_hxx


//---------------------------------------------------------------------------
%{
  namespace Foam
  {}
  
  using namespace Foam;
  
  int main() 
  {
    return 0;
  }  
  
  // To process error within "director" classes
  #include "error.H"
  
  // To simulate Info functionality with Python "__str__" method
  #include "OStringStream.H"
  #include <stdio.h>


#define FOAM_VERSION( CMP, VERSION ) \
__FOAM_VERSION__ CMP VERSION 

#define FOAM_BRANCH_VERSION( NAME, CMP, VERSION ) \
( __FOAM_VERSION__ CMP VERSION  && defined( __FOAM_BRANCH__ ) && __FOAM_BRANCH__ == NAME )

#define FOAM_REF_VERSION( CMP, VERSION )\
( __FOAM_VERSION__ CMP VERSION && !defined( __FOAM_BRANCH__ ) )
%}


//---------------------------------------------------------------------------
%define FOAM_VERSION( CMP, VERSION ) __FOAM_VERSION__ CMP VERSION %enddef

//--------------
%define FOAM_BRANCH_VERSION( NAME, CMP, VERSION ) ( __FOAM_VERSION__ CMP VERSION  && defined( __FOAM_BRANCH__ ) && __FOAM_BRANCH__ == NAME ) %enddef

//--------------
%define FOAM_REF_VERSION( CMP, VERSION ) ( __FOAM_VERSION__ CMP VERSION && !defined( __FOAM_BRANCH__ ) ) %enddef


//---------------------------------------------------------------------------
%include "src/bareptr_typemap.hxx"

//---------------------------------------------------------------------------
%define COMMON_EXTENDS
{
  char* __str__()
  {
    Foam::OStringStream aStream;
    aStream << "\n" << *self;
    return strdup( aStream.str().c_str() );
  }
}
%enddef


//---------------------------------------------------------------------------
%include "src/iterators.hxx"

%include "src/isinstance.hxx"

%include "src/compound_operator.hxx"


//---------------------------------------------------------------------------
%ignore operator <<;
%ignore operator >>;

%ignore operator ==;
%ignore operator !=;

%ignore operator -;
%ignore operator +;
%ignore operator *;
%ignore operator /;

%ignore operator &;
%ignore operator ^;

%ignore operator &&;

%ignore *::operator =;
%ignore *::operator [];

%ignore *::operator ++;
%ignore *::operator --;

%ignore *::operator !;


//---------------------------------------------------------------------------
#endif

