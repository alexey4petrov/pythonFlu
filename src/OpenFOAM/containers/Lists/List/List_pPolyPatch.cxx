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
#ifndef List_pPolyPatch_cxx
#define List_pPolyPatch_cxx


//---------------------------------------------------------------------------
%include "src/OpenFOAM/containers/Lists/UList/UList_pPolyPatch.cxx"

%include "src/OpenFOAM/containers/Lists/List/List.cxx"

%ignore Foam::List< Foam::polyPatch* >::List( Istream& );

%template( List_pPolyPatch ) Foam::List< Foam::polyPatch* >;

%extend Foam::List< Foam::polyPatch* > COMMON_EXTENDS;


//---------------------------------------------------------------------------
%extend Foam::List< Foam::polyPatch* >
{
    Foam::autoPtr< Foam::polyPatch > set( Foam::label i, Foam::autoPtr< Foam::polyPatch > p)
    {
        Foam::polyPatch *pRet = self->operator[](i);
        self->operator[](i) = p.ptr();
        return Foam::autoPtr<Foam::polyPatch>(pRet);
    }

    void __del__()
    {
        if (self->size() > 0)
        {
            for(register int i = 0; i < self->size(); i++)
            {
                if (self->operator[](i) != NULL)
                {
                    delete self->operator[](i);
                    self->operator[](i) = NULL;
                }
            }
        }
    }
}


//---------------------------------------------------------------------------
#endif
