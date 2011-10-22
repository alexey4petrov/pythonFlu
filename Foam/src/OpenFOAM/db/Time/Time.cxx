//  pythonFlu - Python wrapping for OpenFOAM C++ API
//  Copyright (C) 2010- Alexey Petrov
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
//  See http://sourceforge.net/projects/pythonflu
//
//  Author : Alexey PETROV


//---------------------------------------------------------------------------
#ifndef Time_cxx
#define Time_cxx


//---------------------------------------------------------------------------
%module "Foam.src.OpenFOAM.db.Time.Time";
%{
  #include "Foam/src/OpenFOAM/db/Time/Time.hh"
%}


//---------------------------------------------------------------------------
%import "Foam/src/OpenFOAM/db/objectRegistry.cxx"

%import "Foam/src/OpenFOAM/db/Time/clock.cxx"

%import "Foam/src/OpenFOAM/db/Time/cpuTime.cxx"

%import "Foam/src/OpenFOAM/db/Time/TimePaths.cxx"

%import "Foam/src/OpenFOAM/db/Time/TimeState.cxx"

%import "Foam/src/OpenFOAM/primitives/scalar.cxx"

%import "Foam/src/OpenFOAM/dimensionedTypes/dimensionedScalar.cxx"

%import "Foam/src/OpenFOAM/primitives/strings/word.cxx"

%ignore Foam::Time::writeVersion;

%include <Time.H>

%extend Foam::Time
{
  void increment()
  {
    self->operator++();
  }
  // It will have been deleted on "merge with master" step and potentialFlux will have been changed
  void functionObjects_start()
  {
    self->functionObjects().start();
  }
  
  void functionObjects_end()
  {
    self->functionObjects().end();
  }
  //***********************************************

}


//---------------------------------------------------------------------------
%include "Foam/ext/common/OpenFOAM/managedFlu/TimeHolder.cpp"
NO_HOLDER_TYPEMAP( Foam::Time )


//---------------------------------------------------------------------------

#endif
