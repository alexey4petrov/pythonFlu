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
#ifndef graph_cxx
#define graph_cxx


//---------------------------------------------------------------------------
%module "Foam.src.OpenFOAM.graph.graph";
%{
  #include "Foam/src/OpenFOAM/graph/graph.hh"
%}


//---------------------------------------------------------------------------
%import "Foam/src/OpenFOAM/primitives/strings/string.cxx"

%import "Foam/src/OpenFOAM/primitives/strings/fileName.cxx"

%import "Foam/src/OpenFOAM/meshes/primitiveShapes/point/point.cxx"

%import "Foam/src/OpenFOAM/fields/Fields/primitiveFields.cxx"

%import "Foam/src/OpenFOAM/db/IOstreams/IOstreams/Istream.cxx"

%import "Foam/src/OpenFOAM/containers/HashTables/HashPtrTable/HashPtrTable_curve_word_string_hash.cxx"

%include <graph.H>

#if FOAM_REF_VERSION( >=, 020000 )
%extend Foam::graph
{
  void ext_write( Foam::Ostream& os, const Foam::word& format) const
  {
    self->write( os, format );
  }

  void ext_write(const Foam::fileName& pName, const Foam::word& format) const
  {
    self->write( pName, format );
  }

  void ext_write( const Foam::fileName& path, const Foam::word& name, const Foam::word& format ) const
  {
    self->write( path, name, format );
  }
}
#endif

//---------------------------------------------------------------------------
#endif
