#include <cstdlib>
#include <iostream>
#include <gsl/gsl_specfunc.h>
#include <gsl/gsl_errno.h>
#include <cmath>


int main()
{

  gsl_sf_result res;
  int status = gsl_sf_airy_zero_Ai_e(1,&res);

  std::cout << "First zero of Airy function" << std::endl;
  std::cout << "---------------------------" << std::endl;
  std::cout << "status: " << gsl_strerror(status) << std::endl;
  std::cout <<"value: " << res.val << " +- " << res.err <<  std::endl;

  bool correct = std::floor(res.val * 100000) == -233811;
  std::cout << "correct? " << correct << std::endl;

							    
  if(status==0 and correct)
      return EXIT_SUCCESS;


  return EXIT_FAILURE;

							 
}
