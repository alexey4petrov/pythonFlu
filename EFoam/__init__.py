# These lines will allow to share the type information between different dynamic librararies
import sys, DLFCN
sys.setdlopenflags( DLFCN.RTLD_NOW | DLFCN.RTLD_GLOBAL )

