/*
 * Implements a function to fetch the list of objective-C classes known
 * in the runtime.
 */
#include "pyobjc.h"

NS_ASSUME_NONNULL_BEGIN

PyObject*
PyObjC_GetClassList(void)
{
    PyObject* result    = NULL;
    Class*    buffer    = NULL;
    int       bufferLen = 0;
    int       neededLen = 0;
    int       i;

    /*
     * objc_getClassList returns the number of classes known in the runtime,
     * the documented way to fetch the list is:
     * 1. call ret = objc_getClassList(NULL, 0);
     * 2. allocate a buffer of 'ret' class-pointers
     * 3. call objc_getClassList again with this buffer.
     *
     * Step 3 might return more classes because another thread may have
     * loaded a new framework/bundle. This means we need a loop to be sure
     * we'll get all classes.
     */
    neededLen = objc_getClassList(NULL, 0);
    bufferLen = 0;
    buffer    = NULL;

    while (bufferLen < neededLen) {
        Class* newBuffer;
        bufferLen = neededLen;

        newBuffer = PyMem_Realloc(buffer, sizeof(Class) * bufferLen);
        if (newBuffer == NULL) { // LCOV_BR_EXCL_LINE
            // LCOV_EXCL_START
            PyErr_NoMemory();
            goto error;
            // LCOV_EXCL_STOP
        }

        buffer    = newBuffer;
        newBuffer = NULL;
        neededLen = objc_getClassList(buffer, bufferLen);
    }
    bufferLen = neededLen;

    result = PyTuple_New(bufferLen);
    if (result == NULL) { // LCOV_BR_EXCL_LINE
        goto error;       // LCOV_EXCL_LINE
    }

    for (i = 0; i < bufferLen; i++) {
        PyObject* pyclass;

        pyclass = PyObjCClass_New(buffer[i]);
        if (pyclass == NULL) { // LCOV_BR_EXCL_LINE
            goto error;        // LCOV_EXCL_LINE
        }
        PyTuple_SET_ITEM(result, i, pyclass);
    }

    PyMem_Free(buffer);
    buffer = NULL;

    return result;

error:
    // LCOV_EXCL_START
    if (buffer != NULL) {
        PyMem_Free(buffer);
    }
    Py_XDECREF(result);
    return NULL;
    // LCOV_EXCL_STOP
}

NS_ASSUME_NONNULL_END
