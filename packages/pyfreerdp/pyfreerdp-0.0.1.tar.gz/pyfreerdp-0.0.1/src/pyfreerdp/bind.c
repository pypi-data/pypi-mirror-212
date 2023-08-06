#include "libpyfreerdp.h"

char pyfreerdpfunc_docs[] = "python Freerdp description.";

PyMethodDef pyfreerdp_funcs[] = {
	{	"check_connectivity",
		(PyCFunction)check_connectivity,
		METH_VARARGS,
		pyfreerdpfunc_docs},
	{	NULL}
};

char pyfreerdpmod_docs[] = "This is python Freerdp module.";

PyModuleDef pyfreerdp_mod = {
	PyModuleDef_HEAD_INIT,
	"pyfreerdp",
	pyfreerdpmod_docs,
	-1,
	pyfreerdp_funcs,
	NULL,
	NULL,
	NULL,
	NULL
};

PyMODINIT_FUNC PyInit_pyfreerdp(void) {
	return PyModule_Create(&pyfreerdp_mod);
}