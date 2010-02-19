// pseudo solver
#include <iostream>
// using namespace std;

class cSolver;

class visualizator
{
public:
  void call( cSolver* )
	{
	 std::cout << " - visu";
	 }
};

class cSolver
{
public:

   virtual void init();    // init() -prepare input data
   virtual void step();    //step() - let's count
   void  solve( visualizator* visu ) // solve- it's solver 
     {
	this->init();

       for(int i=0;i<10;i++)
         {
            this->step();
	    visu->call( this );
	    std::cout <<"\n";
         }
      }
};

   void cSolver::init()
     {
     std::cout << "init\n";
     }
   void cSolver::step() 
     {
       std::cout <<"step";
     }

