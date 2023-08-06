#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <freerdp/freerdp.h>
#include "libpyfreerdp.h"

static DWORD rdp_freerdp_verify_certificate(freerdp* instance,
        const char* hostname, UINT16 port, const char* common_name,
        const char* subject, const char* issuer, const char* fingerprint,
        DWORD flags) {
    printf("ignore rdp_freerdp_verify_certificate\n");
    return 2;
}

char* g_strdup(const char* str) {

    /* Return NULL if no string provided */
    if (str == NULL)
        return NULL;

    /* Otherwise just invoke strdup() */
    return strdup(str);

}

PyObject * check_connectivity(PyObject * self, PyObject * args) {
    char *host;
	int port;
	char *username;
	char *password;
	char *domain;
    int security;

	if(!PyArg_ParseTuple(args, "sisssi", &host, &port, &username, &password, &domain, &security))
	{
	    return NULL;
	}

	freerdp* instance;
    instance = freerdp_new();
    instance->VerifyCertificateEx = rdp_freerdp_verify_certificate;


    if (!freerdp_context_new(instance)) {
         PyErr_Format(PyExc_Exception, "Unable to allocate context");
         return NULL;
    }

    instance->settings->ServerHostname = g_strdup(host);
    instance->settings->ServerPort = port;
    instance->settings->Username = g_strdup(username);
    instance->settings->Password = g_strdup(password);
    instance->settings->Domain = g_strdup(domain);
    instance->settings->IgnoreCertificate = TRUE;
    if (freerdp_connect(instance) == TRUE)
    {
       // 连接成功，可以进行操作
        freerdp_disconnect(instance);
        freerdp_context_free(instance);
        freerdp_free(instance);
        return PyBool_FromLong(1);
    }
    return PyBool_FromLong(0);
}

