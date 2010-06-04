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
#ifndef TGeometricBoundaryField_hxx
#define TGeometricBoundaryField_hxx

%include "src/nestedClass_extend.hxx"

%inline
{
namespace Foam
{
  //This struct redirect all call's to "nested class" GeometricBoundaryField
  template<class Type, template<class> class PatchField, class GeoMesh> 
  struct TGeometricBoundaryField 
  {
  
     public: 
              
       typedef typename GeometricField<Type, PatchField, GeoMesh>::GeometricBoundaryField TSelf;
       
     private:  
       TSelf& engine;
     
     public:   
       
       TGeometricBoundaryField(  TSelf& theArg ):engine( theArg )
       { }
       
       TSelf& get_self()
       {
          return engine;
       }
       
       const TSelf& get_self() const
       {
          return engine;
       }
       
       List< word > types()
       {
         return engine.types();
       }
       
        //this function( with the "NESTEDCLASS_PYAPPEND_GETATTR" macro)
       // allow to use  full functional from the base classes, except __getitem__, __and__ and other's
       FieldField< PatchField, Type >& base()
       {
          return engine;
       }
       
       void ext_assign( const FieldField< PatchField, Type >& theArg )
       {
         engine = theArg; 
       }
  };  
}

}

//-------------------------------------------------------------------------
//the __getitem__, as  __and__,__sub__ and other's don't work with the __getattr__
%include "src/OpenFOAM/primitives/label.cxx"

%define TGEOM_BOUND_FIELD_GETITEM_EXTEND( Type )
    Type& __getitem__( const Foam::label theIndex )
    {
            return self->base()[ theIndex ];
    }
%enddef


//--------------------------------------------------------------------------
%define TGEOM_BOUND_FIELD_FVPATCHFIELD_EXTENDS()
    void updateCoeffs()
    {
      self->get_self().updateCoeffs();
    }

%enddef


//---------------------------------------------------------------------------
%define TGEOM_BOUND_FIELD_SCALAR_OPERATORS( TPatchField, TMesh )
    Foam::tmp< Foam::FieldField< TPatchField, Foam::vector > > __mul__
    ( const Foam::TGeometricBoundaryField< Foam::vector, TPatchField, TMesh >& theArg )
    {
      return self->get_self() * theArg.get_self();
    }
    
    Foam::tmp< Foam::FieldField< TPatchField, Foam::scalar > > __mul__( const Foam::FieldField< TPatchField, Foam::scalar >& theArg )
    {
      return self->get_self() * theArg; 
    }
       
    Foam::tmp< Foam::FieldField< TPatchField, Foam::scalar > > __mul__( const Foam::TGeometricBoundaryField< Foam::scalar, TPatchField, TMesh >& theArg )
    {
      return self->get_self() * theArg.get_self();
    }    
    
    Foam::tmp< Foam::FieldField< TPatchField, Foam::scalar > > __add__
    ( const Foam::FieldField< TPatchField, Foam::scalar >& theArg )
    {
      return self->get_self() + theArg;
    }
    
%enddef

//----------------------------------------------------------------------------
#endif
