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
//  See https://csrcs.pbmr.co.za/svn/nea/prototypes/reaktor/pyfoam
//
//  Author : Alexey PETROV


//---------------------------------------------------------------------------
#ifndef TGeometricBoundaryField_hxx
#define TGeometricBoundaryField_hxx


%inline
{
namespace Foam
{
  //This struct redirect all call's to "nested class" GeometricBoundaryField
  template<class Type, template<class> class PatchField, class GeoMesh> 
  struct TGeometricBoundaryField 
  {
  
     public: 
              
       typedef typename GeometricField<Type, PatchField, GeoMesh>::GeometricBoundaryField GeomBounField;
     
     private:  
       GeomBounField& engine;
     
     public:   
       
       TGeometricBoundaryField(  GeomBounField& theArg ):engine( theArg )
       { }
       
       void updateCoeffs()
       {
        engine.updateCoeffs();
       }
       List< word > types()
       {
         return engine.types();
       }
       
       label size()
       {
         return engine.size();
       }
       
       Field< Type >& operator[]( label index )
       {
         return engine[ index ];
       }
  };  
}

}


//----------------------------------------------------------------------------
#endif
