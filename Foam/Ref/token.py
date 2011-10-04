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
## Author : Alexey PETROV, Andrey SIMURZIN
##


#--------------------------------------------------------------------------------------
from Foam.src.OpenFOAM.db.IOstreams.token import *


#--------------------------------------------------------------------------------------
token.NULL_TOKEN = ext_make_punctuationToken( token.NULL_TOKEN )
token.SPACE = ext_make_punctuationToken( token.SPACE )
token.TAB = ext_make_punctuationToken( token.TAB )
token.NL = ext_make_punctuationToken( token.NL )

token.END_STATEMENT = ext_make_punctuationToken( token.END_STATEMENT )
token.BEGIN_LIST = ext_make_punctuationToken( token.BEGIN_LIST )
token.END_LIST = ext_make_punctuationToken( token.END_LIST )
token.BEGIN_SQR = ext_make_punctuationToken( token.BEGIN_SQR )
token.END_SQR = ext_make_punctuationToken( token.END_SQR )
token.BEGIN_BLOCK = ext_make_punctuationToken( token.BEGIN_BLOCK )
token.END_BLOCK = ext_make_punctuationToken( token.END_BLOCK )

token.COLON = ext_make_punctuationToken( token.COLON )
token.COMMA = ext_make_punctuationToken( token.COMMA )

token.BEGIN_STRING = ext_make_punctuationToken( token.BEGIN_STRING )
token.END_STRING = ext_make_punctuationToken( token.END_STRING )

token.ASSIGN = ext_make_punctuationToken( token.ASSIGN )
token.ADD = ext_make_punctuationToken( token.ADD )
token.SUBTRACT = ext_make_punctuationToken( token.SUBTRACT )
token.MULTIPLY = ext_make_punctuationToken( token.MULTIPLY )
token.DIVIDE = ext_make_punctuationToken( token.DIVIDE )
                                 

