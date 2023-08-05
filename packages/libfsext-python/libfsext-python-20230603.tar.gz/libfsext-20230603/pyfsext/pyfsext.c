/*
 * Python bindings module for libfsext (pyfsext)
 *
 * Copyright (C) 2010-2023, Joachim Metz <joachim.metz@gmail.com>
 *
 * Refer to AUTHORS for acknowledgements.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

#include <common.h>
#include <narrow_string.h>
#include <types.h>

#if defined( HAVE_STDLIB_H ) || defined( HAVE_WINAPI )
#include <stdlib.h>
#endif

#include "pyfsext.h"
#include "pyfsext_error.h"
#include "pyfsext_extended_attribute.h"
#include "pyfsext_extended_attributes.h"
#include "pyfsext_file_entries.h"
#include "pyfsext_file_entry.h"
#include "pyfsext_file_object_io_handle.h"
#include "pyfsext_libbfio.h"
#include "pyfsext_libcerror.h"
#include "pyfsext_libfsext.h"
#include "pyfsext_python.h"
#include "pyfsext_unused.h"
#include "pyfsext_volume.h"

#if !defined( LIBFSEXT_HAVE_BFIO )

LIBFSEXT_EXTERN \
int libfsext_check_volume_signature_file_io_handle(
     libbfio_handle_t *file_io_handle,
     libfsext_error_t **error );

#endif /* !defined( LIBFSEXT_HAVE_BFIO ) */

/* The pyfsext module methods
 */
PyMethodDef pyfsext_module_methods[] = {
	{ "get_version",
	  (PyCFunction) pyfsext_get_version,
	  METH_NOARGS,
	  "get_version() -> String\n"
	  "\n"
	  "Retrieves the version." },

	{ "check_volume_signature",
	  (PyCFunction) pyfsext_check_volume_signature,
	  METH_VARARGS | METH_KEYWORDS,
	  "check_volume_signature(filename) -> Boolean\n"
	  "\n"
	  "Checks if a volume has an Extended File System (ext) volume signature." },

	{ "check_volume_signature_file_object",
	  (PyCFunction) pyfsext_check_volume_signature_file_object,
	  METH_VARARGS | METH_KEYWORDS,
	  "check_volume_signature_file_object(file_object) -> Boolean\n"
	  "\n"
	  "Checks if a volume has an Extended File System (ext) volume signature using a file-like object." },

	{ "open",
	  (PyCFunction) pyfsext_open_new_volume,
	  METH_VARARGS | METH_KEYWORDS,
	  "open(filename, mode='r') -> Object\n"
	  "\n"
	  "Opens a volume." },

	{ "open_file_object",
	  (PyCFunction) pyfsext_open_new_volume_with_file_object,
	  METH_VARARGS | METH_KEYWORDS,
	  "open_file_object(file_object, mode='r') -> Object\n"
	  "\n"
	  "Opens a volume using a file-like object." },

	/* Sentinel */
	{ NULL, NULL, 0, NULL }
};

/* Retrieves the pyfsext/libfsext version
 * Returns a Python object if successful or NULL on error
 */
PyObject *pyfsext_get_version(
           PyObject *self PYFSEXT_ATTRIBUTE_UNUSED,
           PyObject *arguments PYFSEXT_ATTRIBUTE_UNUSED )
{
	const char *errors           = NULL;
	const char *version_string   = NULL;
	size_t version_string_length = 0;

	PYFSEXT_UNREFERENCED_PARAMETER( self )
	PYFSEXT_UNREFERENCED_PARAMETER( arguments )

	Py_BEGIN_ALLOW_THREADS

	version_string = libfsext_get_version();

	Py_END_ALLOW_THREADS

	version_string_length = narrow_string_length(
	                         version_string );

	/* Pass the string length to PyUnicode_DecodeUTF8
	 * otherwise it makes the end of string character is part
	 * of the string
	 */
	return( PyUnicode_DecodeUTF8(
	         version_string,
	         (Py_ssize_t) version_string_length,
	         errors ) );
}

/* Checks if a volume has an Extended File System (ext) volume signature
 * Returns a Python object if successful or NULL on error
 */
PyObject *pyfsext_check_volume_signature(
           PyObject *self PYFSEXT_ATTRIBUTE_UNUSED,
           PyObject *arguments,
           PyObject *keywords )
{
	PyObject *string_object     = NULL;
	libcerror_error_t *error    = NULL;
	const char *filename_narrow = NULL;
	static char *function       = "pyfsext_check_volume_signature";
	static char *keyword_list[] = { "filename", NULL };
	int result                  = 0;

#if defined( HAVE_WIDE_SYSTEM_CHARACTER )
	const wchar_t *filename_wide = NULL;
#else
	PyObject *utf8_string_object = NULL;
#endif

	PYFSEXT_UNREFERENCED_PARAMETER( self )

	/* Note that PyArg_ParseTupleAndKeywords with "s" will force Unicode strings to be converted to narrow character string.
	 * On Windows the narrow character strings contains an extended ASCII string with a codepage. Hence we get a conversion
	 * exception. This will also fail if the default encoding is not set correctly. We cannot use "u" here either since that
	 * does not allow us to pass non Unicode string objects and Python (at least 2.7) does not seems to automatically upcast them.
	 */
	if( PyArg_ParseTupleAndKeywords(
	     arguments,
	     keywords,
	     "O|",
	     keyword_list,
	     &string_object ) == 0 )
	{
		return( NULL );
	}
	PyErr_Clear();

	result = PyObject_IsInstance(
	          string_object,
	          (PyObject *) &PyUnicode_Type );

	if( result == -1 )
	{
		pyfsext_error_fetch_and_raise(
		 PyExc_RuntimeError,
		 "%s: unable to determine if string object is of type Unicode.",
		 function );

		return( NULL );
	}
	else if( result != 0 )
	{
		PyErr_Clear();

#if defined( HAVE_WIDE_SYSTEM_CHARACTER )
		filename_wide = (wchar_t *) PyUnicode_AsUnicode(
		                             string_object );
		Py_BEGIN_ALLOW_THREADS

		result = libfsext_check_volume_signature_wide(
		          filename_wide,
		          &error );

		Py_END_ALLOW_THREADS
#else
		utf8_string_object = PyUnicode_AsUTF8String(
		                      string_object );

		if( utf8_string_object == NULL )
		{
			pyfsext_error_fetch_and_raise(
			 PyExc_RuntimeError,
			 "%s: unable to convert Unicode string to UTF-8.",
			 function );

			return( NULL );
		}
#if PY_MAJOR_VERSION >= 3
		filename_narrow = PyBytes_AsString(
		                   utf8_string_object );
#else
		filename_narrow = PyString_AsString(
		                   utf8_string_object );
#endif
		Py_BEGIN_ALLOW_THREADS

		result = libfsext_check_volume_signature(
		          filename_narrow,
		          &error );

		Py_END_ALLOW_THREADS

		Py_DecRef(
		 utf8_string_object );

#endif /* defined( HAVE_WIDE_SYSTEM_CHARACTER ) */

		if( result == -1 )
		{
			pyfsext_error_raise(
			 error,
			 PyExc_IOError,
			 "%s: unable to check volume signature.",
			 function );

			libcerror_error_free(
			 &error );

			return( NULL );
		}
		if( result != 0 )
		{
			Py_IncRef(
			 (PyObject *) Py_True );

			return( Py_True );
		}
		Py_IncRef(
		 (PyObject *) Py_False );

		return( Py_False );
	}
	PyErr_Clear();

#if PY_MAJOR_VERSION >= 3
	result = PyObject_IsInstance(
	          string_object,
	          (PyObject *) &PyBytes_Type );
#else
	result = PyObject_IsInstance(
	          string_object,
	          (PyObject *) &PyString_Type );
#endif
	if( result == -1 )
	{
		pyfsext_error_fetch_and_raise(
		 PyExc_RuntimeError,
		 "%s: unable to determine if string object is of type string.",
		 function );

		return( NULL );
	}
	else if( result != 0 )
	{
		PyErr_Clear();

#if PY_MAJOR_VERSION >= 3
		filename_narrow = PyBytes_AsString(
		                   string_object );
#else
		filename_narrow = PyString_AsString(
		                   string_object );
#endif
		Py_BEGIN_ALLOW_THREADS

		result = libfsext_check_volume_signature(
		          filename_narrow,
		          &error );

		Py_END_ALLOW_THREADS

		if( result == -1 )
		{
			pyfsext_error_raise(
			 error,
			 PyExc_IOError,
			 "%s: unable to check volume signature.",
			 function );

			libcerror_error_free(
			 &error );

			return( NULL );
		}
		if( result != 0 )
		{
			Py_IncRef(
			 (PyObject *) Py_True );

			return( Py_True );
		}
		Py_IncRef(
		 (PyObject *) Py_False );

		return( Py_False );
	}
	PyErr_Format(
	 PyExc_TypeError,
	 "%s: unsupported string object type.",
	 function );

	return( NULL );
}

/* Checks if a volume has an Extended File System (ext) volume signature using a file-like object
 * Returns a Python object if successful or NULL on error
 */
PyObject *pyfsext_check_volume_signature_file_object(
           PyObject *self PYFSEXT_ATTRIBUTE_UNUSED,
           PyObject *arguments,
           PyObject *keywords )
{
	PyObject *file_object            = NULL;
	libbfio_handle_t *file_io_handle = NULL;
	libcerror_error_t *error         = NULL;
	static char *function            = "pyfsext_check_volume_signature_file_object";
	static char *keyword_list[]      = { "file_object", NULL };
	int result                       = 0;

	PYFSEXT_UNREFERENCED_PARAMETER( self )

	if( PyArg_ParseTupleAndKeywords(
	     arguments,
	     keywords,
	     "O|",
	     keyword_list,
	     &file_object ) == 0 )
	{
		return( NULL );
	}
	if( pyfsext_file_object_initialize(
	     &file_io_handle,
	     file_object,
	     &error ) != 1 )
	{
		pyfsext_error_raise(
		 error,
		 PyExc_MemoryError,
		 "%s: unable to initialize file IO handle.",
		 function );

		libcerror_error_free(
		 &error );

		goto on_error;
	}
	Py_BEGIN_ALLOW_THREADS

	result = libfsext_check_volume_signature_file_io_handle(
	          file_io_handle,
	          &error );

	Py_END_ALLOW_THREADS

	if( result == -1 )
	{
		pyfsext_error_raise(
		 error,
		 PyExc_IOError,
		 "%s: unable to check volume signature.",
		 function );

		libcerror_error_free(
		 &error );

		goto on_error;
	}
	if( libbfio_handle_free(
	     &file_io_handle,
	     &error ) != 1 )
	{
		pyfsext_error_raise(
		 error,
		 PyExc_MemoryError,
		 "%s: unable to free file IO handle.",
		 function );

		libcerror_error_free(
		 &error );

		goto on_error;
	}
	if( result != 0 )
	{
		Py_IncRef(
		 (PyObject *) Py_True );

		return( Py_True );
	}
	Py_IncRef(
	 (PyObject *) Py_False );

	return( Py_False );

on_error:
	if( file_io_handle != NULL )
	{
		libbfio_handle_free(
		 &file_io_handle,
		 NULL );
	}
	return( NULL );
}

/* Creates a new volume object and opens it
 * Returns a Python object if successful or NULL on error
 */
PyObject *pyfsext_open_new_volume(
           PyObject *self PYFSEXT_ATTRIBUTE_UNUSED,
           PyObject *arguments,
           PyObject *keywords )
{
	pyfsext_volume_t *pyfsext_volume = NULL;
	static char *function            = "pyfsext_open_new_volume";

	PYFSEXT_UNREFERENCED_PARAMETER( self )

	/* PyObject_New does not invoke tp_init
	 */
	pyfsext_volume = PyObject_New(
	                  struct pyfsext_volume,
	                  &pyfsext_volume_type_object );

	if( pyfsext_volume == NULL )
	{
		PyErr_Format(
		 PyExc_MemoryError,
		 "%s: unable to create volume.",
		 function );

		goto on_error;
	}
	if( pyfsext_volume_init(
	     pyfsext_volume ) != 0 )
	{
		goto on_error;
	}
	if( pyfsext_volume_open(
	     pyfsext_volume,
	     arguments,
	     keywords ) == NULL )
	{
		goto on_error;
	}
	return( (PyObject *) pyfsext_volume );

on_error:
	if( pyfsext_volume != NULL )
	{
		Py_DecRef(
		 (PyObject *) pyfsext_volume );
	}
	return( NULL );
}

/* Creates a new volume object and opens it using a file-like object
 * Returns a Python object if successful or NULL on error
 */
PyObject *pyfsext_open_new_volume_with_file_object(
           PyObject *self PYFSEXT_ATTRIBUTE_UNUSED,
           PyObject *arguments,
           PyObject *keywords )
{
	pyfsext_volume_t *pyfsext_volume = NULL;
	static char *function            = "pyfsext_open_new_volume_with_file_object";

	PYFSEXT_UNREFERENCED_PARAMETER( self )

	/* PyObject_New does not invoke tp_init
	 */
	pyfsext_volume = PyObject_New(
	                  struct pyfsext_volume,
	                  &pyfsext_volume_type_object );

	if( pyfsext_volume == NULL )
	{
		PyErr_Format(
		 PyExc_MemoryError,
		 "%s: unable to create volume.",
		 function );

		goto on_error;
	}
	if( pyfsext_volume_init(
	     pyfsext_volume ) != 0 )
	{
		goto on_error;
	}
	if( pyfsext_volume_open_file_object(
	     pyfsext_volume,
	     arguments,
	     keywords ) == NULL )
	{
		goto on_error;
	}
	return( (PyObject *) pyfsext_volume );

on_error:
	if( pyfsext_volume != NULL )
	{
		Py_DecRef(
		 (PyObject *) pyfsext_volume );
	}
	return( NULL );
}

#if PY_MAJOR_VERSION >= 3

/* The pyfsext module definition
 */
PyModuleDef pyfsext_module_definition = {
	PyModuleDef_HEAD_INIT,

	/* m_name */
	"pyfsext",
	/* m_doc */
	"Python libfsext module (pyfsext).",
	/* m_size */
	-1,
	/* m_methods */
	pyfsext_module_methods,
	/* m_reload */
	NULL,
	/* m_traverse */
	NULL,
	/* m_clear */
	NULL,
	/* m_free */
	NULL,
};

#endif /* PY_MAJOR_VERSION >= 3 */

/* Initializes the pyfsext module
 */
#if PY_MAJOR_VERSION >= 3
PyMODINIT_FUNC PyInit_pyfsext(
                void )
#else
PyMODINIT_FUNC initpyfsext(
                void )
#endif
{
	PyObject *module           = NULL;
	PyGILState_STATE gil_state = 0;

#if defined( HAVE_DEBUG_OUTPUT )
	libfsext_notify_set_stream(
	 stderr,
	 NULL );
	libfsext_notify_set_verbose(
	 1 );
#endif

	/* Create the module
	 * This function must be called before grabbing the GIL
	 * otherwise the module will segfault on a version mismatch
	 */
#if PY_MAJOR_VERSION >= 3
	module = PyModule_Create(
	          &pyfsext_module_definition );
#else
	module = Py_InitModule3(
	          "pyfsext",
	          pyfsext_module_methods,
	          "Python libfsext module (pyfsext)." );
#endif
	if( module == NULL )
	{
#if PY_MAJOR_VERSION >= 3
		return( NULL );
#else
		return;
#endif
	}
#if PY_VERSION_HEX < 0x03070000
	PyEval_InitThreads();
#endif
	gil_state = PyGILState_Ensure();

	/* Setup the extended_attribute type object
	 */
	pyfsext_extended_attribute_type_object.tp_new = PyType_GenericNew;

	if( PyType_Ready(
	     &pyfsext_extended_attribute_type_object ) < 0 )
	{
		goto on_error;
	}
	Py_IncRef(
	 (PyObject *) &pyfsext_extended_attribute_type_object );

	PyModule_AddObject(
	 module,
	 "extended_attribute",
	 (PyObject *) &pyfsext_extended_attribute_type_object );

	/* Setup the extended_attributes type object
	 */
	pyfsext_extended_attributes_type_object.tp_new = PyType_GenericNew;

	if( PyType_Ready(
	     &pyfsext_extended_attributes_type_object ) < 0 )
	{
		goto on_error;
	}
	Py_IncRef(
	 (PyObject *) &pyfsext_extended_attributes_type_object );

	PyModule_AddObject(
	 module,
	 "extended_attributes",
	 (PyObject *) &pyfsext_extended_attributes_type_object );

	/* Setup the file_entries type object
	 */
	pyfsext_file_entries_type_object.tp_new = PyType_GenericNew;

	if( PyType_Ready(
	     &pyfsext_file_entries_type_object ) < 0 )
	{
		goto on_error;
	}
	Py_IncRef(
	 (PyObject *) &pyfsext_file_entries_type_object );

	PyModule_AddObject(
	 module,
	 "file_entries",
	 (PyObject *) &pyfsext_file_entries_type_object );

	/* Setup the file_entry type object
	 */
	pyfsext_file_entry_type_object.tp_new = PyType_GenericNew;

	if( PyType_Ready(
	     &pyfsext_file_entry_type_object ) < 0 )
	{
		goto on_error;
	}
	Py_IncRef(
	 (PyObject *) &pyfsext_file_entry_type_object );

	PyModule_AddObject(
	 module,
	 "file_entry",
	 (PyObject *) &pyfsext_file_entry_type_object );

	/* Setup the volume type object
	 */
	pyfsext_volume_type_object.tp_new = PyType_GenericNew;

	if( PyType_Ready(
	     &pyfsext_volume_type_object ) < 0 )
	{
		goto on_error;
	}
	Py_IncRef(
	 (PyObject *) &pyfsext_volume_type_object );

	PyModule_AddObject(
	 module,
	 "volume",
	 (PyObject *) &pyfsext_volume_type_object );

	PyGILState_Release(
	 gil_state );

#if PY_MAJOR_VERSION >= 3
	return( module );
#else
	return;
#endif

on_error:
	PyGILState_Release(
	 gil_state );

#if PY_MAJOR_VERSION >= 3
	return( NULL );
#else
	return;
#endif
}

