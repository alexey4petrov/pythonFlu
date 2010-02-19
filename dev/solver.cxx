%module(directors="1") solver
%{
    #include "solver.hpp"
%}

/* Let's just grab the original header file here */
%feature("director") cSolver;

%include "solver.hpp"

%inline
{
    int main()
    {}
}


