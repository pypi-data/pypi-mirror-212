/*
 * Mount tool fuse functions
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

#if defined( HAVE_ERRNO_H ) || defined( WINAPI )
#include <errno.h>
#endif

#if defined( HAVE_STDLIB_H ) || defined( WINAPI )
#include <stdlib.h>
#endif

#if defined( HAVE_UNISTD_H )
#include <unistd.h>
#endif

#include "fsexttools_libcerror.h"
#include "fsexttools_libcnotify.h"
#include "fsexttools_libfsext.h"
#include "fsexttools_unused.h"
#include "mount_fuse.h"
#include "mount_handle.h"

extern mount_handle_t *fsextmount_mount_handle;

#if defined( HAVE_LIBFUSE ) || defined( HAVE_LIBOSXFUSE )

#if ( SIZEOF_OFF_T != 8 ) && ( SIZEOF_OFF_T != 4 )
#error Size of off_t not supported
#endif

/* Sets the values in a stat info structure
 * The time values are a signed 64-bit POSIX date and time value in number of nanoseconds
 * Returns 1 if successful or -1 on error
 */
int mount_fuse_set_stat_info(
     struct stat *stat_info,
     size64_t size,
     uint16_t file_mode,
     int64_t access_time,
     int64_t inode_change_time,
     int64_t modification_time,
     libcerror_error_t **error )
{
	static char *function = "mount_fuse_set_stat_info";

	if( stat_info == NULL )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_ARGUMENTS,
		 LIBCERROR_ARGUMENT_ERROR_INVALID_VALUE,
		 "%s: invalid stat info.",
		 function );

		return( -1 );
	}
#if SIZEOF_OFF_T <= 4
	if( size > (size64_t) UINT32_MAX )
#else
	if( size > (size64_t) INT64_MAX )
#endif
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_RUNTIME,
		 LIBCERROR_RUNTIME_ERROR_VALUE_OUT_OF_BOUNDS,
		 "%s: invalid size value out of bounds.",
		 function );

		return( -1 );
	}
	stat_info->st_size  = (off_t) size;
	stat_info->st_mode  = file_mode;

	if( ( file_mode & 0x4000 ) != 0 )
	{
		stat_info->st_nlink = 2;
	}
	else
	{
		stat_info->st_nlink = 1;
	}
#if defined( HAVE_GETEUID )
	stat_info->st_uid = geteuid();
#endif
#if defined( HAVE_GETEGID )
	stat_info->st_gid = getegid();
#endif

	stat_info->st_atime = access_time / 1000000000;
	stat_info->st_ctime = inode_change_time / 1000000000;
	stat_info->st_mtime = modification_time / 1000000000;

#if defined( STAT_HAVE_NSEC )
	stat_info->st_atime_nsec = access_time % 1000000000;
	stat_info->st_ctime_nsec = inode_change_time % 1000000000;
	stat_info->st_mtime_nsec = modification_time % 1000000000;
#endif
	return( 1 );
}

/* Fills a directory entry
 * Returns 1 if successful or -1 on error
 */
int mount_fuse_filldir(
     void *buffer,
     fuse_fill_dir_t filler,
     const char *name,
     struct stat *stat_info,
     mount_file_entry_t *file_entry,
     libcerror_error_t **error )
{
	static char *function      = "mount_fuse_filldir";
	size64_t file_size         = 0;
	uint64_t access_time       = 0;
	uint64_t inode_change_time = 0;
	uint64_t modification_time = 0;
	uint16_t file_mode         = 0;

	if( filler == NULL )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_ARGUMENTS,
		 LIBCERROR_ARGUMENT_ERROR_INVALID_VALUE,
		 "%s: invalid filler.",
		 function );

		return( -1 );
	}
	if( file_entry != NULL )
	{
		if( mount_file_entry_get_size(
		     file_entry,
		     &file_size,
		     error ) != 1 )
		{
			libcerror_error_set(
			 error,
			 LIBCERROR_ERROR_DOMAIN_RUNTIME,
			 LIBCERROR_RUNTIME_ERROR_GET_FAILED,
			 "%s: unable to retrieve file entry size.",
			 function );

			return( -1 );
		}
		if( mount_file_entry_get_file_mode(
		     file_entry,
		     &file_mode,
		     error ) != 1 )
		{
			libcerror_error_set(
			 error,
			 LIBCERROR_ERROR_DOMAIN_RUNTIME,
			 LIBCERROR_RUNTIME_ERROR_GET_FAILED,
			 "%s: unable to retrieve file mode.",
			 function );

			return( -1 );
		}
		if( mount_file_entry_get_access_time(
		     file_entry,
		     &access_time,
		     error ) != 1 )
		{
			libcerror_error_set(
			 error,
			 LIBCERROR_ERROR_DOMAIN_RUNTIME,
			 LIBCERROR_RUNTIME_ERROR_GET_FAILED,
			 "%s: unable to retrieve access time.",
			 function );

			return( -1 );
		}
		if( mount_file_entry_get_modification_time(
		     file_entry,
		     &modification_time,
		     error ) != 1 )
		{
			libcerror_error_set(
			 error,
			 LIBCERROR_ERROR_DOMAIN_RUNTIME,
			 LIBCERROR_RUNTIME_ERROR_GET_FAILED,
			 "%s: unable to retrieve modification time.",
			 function );

			return( -1 );
		}
		if( mount_file_entry_get_inode_change_time(
		     file_entry,
		     &inode_change_time,
		     error ) != 1 )
		{
			libcerror_error_set(
			 error,
			 LIBCERROR_ERROR_DOMAIN_RUNTIME,
			 LIBCERROR_RUNTIME_ERROR_GET_FAILED,
			 "%s: unable to retrieve inode change time.",
			 function );

			return( -1 );
		}
	}
	if( memory_set(
	     stat_info,
	     0,
	     sizeof( struct stat ) ) == NULL )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_MEMORY,
		 LIBCERROR_MEMORY_ERROR_SET_FAILED,
		 "%s: unable to clear stat info.",
		 function );

		return( -1 );
	}
	if( mount_fuse_set_stat_info(
	     stat_info,
	     file_size,
	     file_mode,
	     (int64_t) access_time,
	     (int64_t) inode_change_time,
	     (int64_t) modification_time,
	     error ) != 1 )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_RUNTIME,
		 LIBCERROR_RUNTIME_ERROR_SET_FAILED,
		 "%s: unable to set stat info.",
		 function );

		return( -1 );
	}
	if( filler(
	     buffer,
	     name,
	     stat_info,
	     0 ) == 1 )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_RUNTIME,
		 LIBCERROR_RUNTIME_ERROR_SET_FAILED,
		 "%s: unable to set directory entry.",
		 function );

		return( -1 );
	}
	return( 1 );
}

/* Opens a file or directory
 * Returns 0 if successful or a negative errno value otherwise
 */
int mount_fuse_open(
     const char *path,
     struct fuse_file_info *file_info )
{
	libcerror_error_t *error = NULL;
	static char *function    = "mount_fuse_open";
	int result               = 0;

#if defined( HAVE_DEBUG_OUTPUT )
	if( libcnotify_verbose != 0 )
	{
		libcnotify_printf(
		 "%s: %s\n",
		 function,
		 path );
	}
#endif
	if( path == NULL )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_ARGUMENTS,
		 LIBCERROR_ARGUMENT_ERROR_INVALID_VALUE,
		 "%s: invalid path.",
		 function );

		result = -EINVAL;

		goto on_error;
	}
	if( file_info == NULL )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_ARGUMENTS,
		 LIBCERROR_ARGUMENT_ERROR_INVALID_VALUE,
		 "%s: invalid file information.",
		 function );

		result = -EINVAL;

		goto on_error;
	}
	if( file_info->fh != (uint64_t) NULL )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_RUNTIME,
		 LIBCERROR_RUNTIME_ERROR_VALUE_ALREADY_SET,
		 "%s: invalid file information - file handle already set.",
		 function );

		result = -EINVAL;

		goto on_error;
	}
	if( ( file_info->flags & 0x03 ) != O_RDONLY )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_RUNTIME,
		 LIBCERROR_RUNTIME_ERROR_UNSUPPORTED_VALUE,
		 "%s: write access currently not supported.",
		 function );

		result = -EACCES;

		goto on_error;
	}
	if( mount_handle_get_file_entry_by_path(
	     fsextmount_mount_handle,
	     path,
	     (mount_file_entry_t **) &( file_info->fh ),
	     &error ) != 1 )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_RUNTIME,
		 LIBCERROR_RUNTIME_ERROR_GET_FAILED,
		 "%s: unable to retrieve file entry for path: %s.",
		 function,
		 path );

		result = -ENOENT;

		goto on_error;
	}
	return( 0 );

on_error:
	if( error != NULL )
	{
		libcnotify_print_error_backtrace(
		 error );
		libcerror_error_free(
		 &error );
	}
	return( result );
}

/* Reads a buffer of data at the specified offset
 * Returns number of bytes read if successful or a negative errno value otherwise
 */
int mount_fuse_read(
     const char *path,
     char *buffer,
     size_t size,
     off_t offset,
     struct fuse_file_info *file_info )
{
	libcerror_error_t *error = NULL;
	static char *function    = "mount_fuse_read";
	ssize_t read_count       = 0;
	int result               = 0;

#if defined( HAVE_DEBUG_OUTPUT )
	if( libcnotify_verbose != 0 )
	{
		libcnotify_printf(
		 "%s: %s\n",
		 function,
		 path );
	}
#endif
	if( path == NULL )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_ARGUMENTS,
		 LIBCERROR_ARGUMENT_ERROR_INVALID_VALUE,
		 "%s: invalid path.",
		 function );

		result = -EINVAL;

		goto on_error;
	}
	if( size > (size_t) INT_MAX )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_ARGUMENTS,
		 LIBCERROR_ARGUMENT_ERROR_VALUE_EXCEEDS_MAXIMUM,
		 "%s: invalid size value exceeds maximum.",
		 function );

		result = -EINVAL;

		goto on_error;
	}
	if( file_info == NULL )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_ARGUMENTS,
		 LIBCERROR_ARGUMENT_ERROR_INVALID_VALUE,
		 "%s: invalid file information.",
		 function );

		result = -EINVAL;

		goto on_error;
	}
	if( file_info->fh == (uint64_t) NULL )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_RUNTIME,
		 LIBCERROR_RUNTIME_ERROR_VALUE_MISSING,
		 "%s: invalid file information - missing file handle.",
		 function );

		result = -EINVAL;

		goto on_error;
	}
	read_count = mount_file_entry_read_buffer_at_offset(
	              (mount_file_entry_t *) file_info->fh,
	              (void *) buffer,
	              size,
	              (off64_t) offset,
	              &error );

	if( read_count < 0 )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_IO,
		 LIBCERROR_IO_ERROR_READ_FAILED,
		 "%s: unable to read from file entry.",
		 function );

		result = -EIO;

		goto on_error;
	}
	return( (int) read_count );

on_error:
	if( error != NULL )
	{
		libcnotify_print_error_backtrace(
		 error );
		libcerror_error_free(
		 &error );
	}
	return( result );
}

/* Releases a file entry
 * Returns 0 if successful or a negative errno value otherwise
 */
int mount_fuse_release(
     const char *path,
     struct fuse_file_info *file_info )
{
	libcerror_error_t *error = NULL;
	static char *function    = "mount_fuse_release";
	int result               = 0;

#if defined( HAVE_DEBUG_OUTPUT )
	if( libcnotify_verbose != 0 )
	{
		libcnotify_printf(
		 "%s: %s\n",
		 function,
		 path );
	}
#endif
	if( path == NULL )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_ARGUMENTS,
		 LIBCERROR_ARGUMENT_ERROR_INVALID_VALUE,
		 "%s: invalid path.",
		 function );

		result = -EINVAL;

		goto on_error;
	}
	if( file_info == NULL )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_ARGUMENTS,
		 LIBCERROR_ARGUMENT_ERROR_INVALID_VALUE,
		 "%s: invalid file information.",
		 function );

		result = -EINVAL;

		goto on_error;
	}
	if( file_info->fh != (uint64_t) NULL )
	{
		if( mount_file_entry_free(
		     (mount_file_entry_t **) &( file_info->fh ),
		     &error ) != 1 )
		{
			libcerror_error_set(
			 &error,
			 LIBCERROR_ERROR_DOMAIN_RUNTIME,
			 LIBCERROR_RUNTIME_ERROR_FINALIZE_FAILED,
			 "%s: unable to free file entry.",
			 function );

			result = -ENOENT;

			goto on_error;
		}
	}
	return( 0 );

on_error:
	if( error != NULL )
	{
		libcnotify_print_error_backtrace(
		 error );
		libcerror_error_free(
		 &error );
	}
	return( result );
}

/* Retrieves the value data of an extended attribute
 * Returns 0 if successful or a negative errno value otherwise
 */
int mount_fuse_getxattr(
     const char *path,
     const char *name,
     char *value,
     size_t size )
{
	libcerror_error_t *error                           = NULL;
	libfsext_extended_attribute_t *extended_attribute = NULL;
	mount_file_entry_t *file_entry                     = NULL;
	static char *function                              = "mount_fuse_getxattr";
	size64_t value_data_size                           = 0;
	size_t name_length                                 = 0;
	ssize_t read_count                                 = 0;
	int result                                         = 0;

#if defined( HAVE_DEBUG_OUTPUT )
	if( libcnotify_verbose != 0 )
	{
		libcnotify_printf(
		 "%s: %s\n",
		 function,
		 path );
	}
#endif
	if( path == NULL )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_ARGUMENTS,
		 LIBCERROR_ARGUMENT_ERROR_INVALID_VALUE,
		 "%s: invalid path.",
		 function );

		result = -EINVAL;

		goto on_error;
	}
	if( name == NULL )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_ARGUMENTS,
		 LIBCERROR_ARGUMENT_ERROR_INVALID_VALUE,
		 "%s: invalid name.",
		 function );

		result = -EINVAL;

		goto on_error;
	}
	if( size > (size_t) INT_MAX )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_ARGUMENTS,
		 LIBCERROR_ARGUMENT_ERROR_VALUE_EXCEEDS_MAXIMUM,
		 "%s: invalid size value exceeds maximum.",
		 function );

		result = -EINVAL;

		goto on_error;
	}
	result = mount_handle_get_file_entry_by_path(
	          fsextmount_mount_handle,
	          path,
	          &file_entry,
	          &error );

	if( result == -1 )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_RUNTIME,
		 LIBCERROR_RUNTIME_ERROR_GET_FAILED,
		 "%s: unable to retrieve value for: %s.",
		 function,
		 path );

		result = -ENOENT;

		goto on_error;
	}
	else if( result == 0 )
	{
		return( -ENOENT );
	}
	name_length = narrow_string_length(
	               name );

	result = libfsext_file_entry_get_extended_attribute_by_utf8_name(
	          file_entry->fsext_file_entry,
	          (uint8_t *) name,
	          name_length,
	          &extended_attribute,
	          &error );

	if( result == -1 )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_RUNTIME,
		 LIBCERROR_RUNTIME_ERROR_GET_FAILED,
		 "%s: unable to retrieve extended attribute.",
		 function );

		result = -EIO;

		goto on_error;
	}
	else if( result != 0 )
	{
		if( libfsext_extended_attribute_get_size(
		     extended_attribute,
		     &value_data_size,
		     &error ) != 1 )
		{
			libcerror_error_set(
			 &error,
			 LIBCERROR_ERROR_DOMAIN_RUNTIME,
			 LIBCERROR_RUNTIME_ERROR_GET_FAILED,
			 "%s: unable to retrieve extended attribute value data size.",
			 function );

			result = -EIO;

			goto on_error;
		}
		if( value_data_size > (size64_t) INT_MAX )
		{
			libcerror_error_set(
			 &error,
			 LIBCERROR_ERROR_DOMAIN_RUNTIME,
			 LIBCERROR_RUNTIME_ERROR_VALUE_OUT_OF_BOUNDS,
			 "%s: invalid value data size value out of bounds.",
			 function );

			result = -E2BIG;

			goto on_error;
		}
		/* When size is 0 determine and return the required value size
		 */
		if( size == 0 )
		{
			read_count = (ssize_t) value_data_size;
		}
		else
		{
			if( (size64_t) size < value_data_size )
			{
				libcerror_error_set(
				 &error,
				 LIBCERROR_ERROR_DOMAIN_ARGUMENTS,
				 LIBCERROR_ARGUMENT_ERROR_VALUE_TOO_SMALL,
				 "%s: invalid size value too small.",
				 function );

				result = -ERANGE;

				goto on_error;
			}
			read_count = libfsext_extended_attribute_read_buffer_at_offset(
			              extended_attribute,
			              (void *) value,
			              size,
			              0,
			              &error );

			if( read_count == -1 )
			{
				libcerror_error_set(
				 &error,
				 LIBCERROR_ERROR_DOMAIN_IO,
				 LIBCERROR_IO_ERROR_READ_FAILED,
				 "%s: unable to read from extended attribute.",
				 function );

				result = -EIO;

				goto on_error;
			}
		}
	}
	if( libfsext_extended_attribute_free(
	     &extended_attribute,
	     &error ) != 1 )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_RUNTIME,
		 LIBCERROR_RUNTIME_ERROR_FINALIZE_FAILED,
		 "%s: unable to free extended attribute.",
		 function );

		result = -EIO;

		goto on_error;
	}
	if( mount_file_entry_free(
	     &file_entry,
	     &error ) != 1 )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_RUNTIME,
		 LIBCERROR_RUNTIME_ERROR_FINALIZE_FAILED,
		 "%s: unable to free file entry.",
		 function );

		result = -EIO;

		goto on_error;
	}
	if( result == 0 )
	{
		return( -ENOENT );
	}
	return( (int) read_count );

on_error:
	if( error != NULL )
	{
		libcnotify_print_error_backtrace(
		 error );
		libcerror_error_free(
		 &error );
	}
	if( file_entry != NULL )
	{
		mount_file_entry_free(
		 &file_entry,
		 NULL );
	}
	return( result );
}

/* Lists the names of extended attributes
 * Returns 0 if successful or a negative errno value otherwise
 */
int mount_fuse_listxattr(
     const char *path,
     char *list,
     size_t size )
{
	libcerror_error_t *error                           = NULL;
	libfsext_extended_attribute_t *extended_attribute = NULL;
	mount_file_entry_t *file_entry                     = NULL;
	static char *function                              = "mount_fuse_listxattr";
	size_t extended_attribute_name_size                = 0;
	size_t list_offset                                 = 0;
	int extended_attribute_index                       = 0;
	int number_of_extended_attributes                  = 0;
	int result                                         = 0;

#if defined( HAVE_DEBUG_OUTPUT )
	if( libcnotify_verbose != 0 )
	{
		libcnotify_printf(
		 "%s: %s\n",
		 function,
		 path );
	}
#endif
	if( path == NULL )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_ARGUMENTS,
		 LIBCERROR_ARGUMENT_ERROR_INVALID_VALUE,
		 "%s: invalid path.",
		 function );

		result = -EINVAL;

		goto on_error;
	}
	/* When size is 0 determine and return the required list size
	 */
	if( size > 0 )
	{
		if( list == NULL )
		{
			libcerror_error_set(
			 &error,
			 LIBCERROR_ERROR_DOMAIN_ARGUMENTS,
			 LIBCERROR_ARGUMENT_ERROR_INVALID_VALUE,
			 "%s: invalid list.",
			 function );

			result = -EINVAL;

			goto on_error;
		}
	}
	if( size > (size_t) INT_MAX )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_ARGUMENTS,
		 LIBCERROR_ARGUMENT_ERROR_VALUE_EXCEEDS_MAXIMUM,
		 "%s: invalid size value exceeds maximum.",
		 function );

		result = -EINVAL;

		goto on_error;
	}
	result = mount_handle_get_file_entry_by_path(
	          fsextmount_mount_handle,
	          path,
	          &file_entry,
	          &error );

	if( result == -1 )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_RUNTIME,
		 LIBCERROR_RUNTIME_ERROR_GET_FAILED,
		 "%s: unable to retrieve value for: %s.",
		 function,
		 path );

		result = -ENOENT;

		goto on_error;
	}
	else if( result == 0 )
	{
		return( -ENOENT );
	}
	if( libfsext_file_entry_get_number_of_extended_attributes(
	     file_entry->fsext_file_entry,
	     &number_of_extended_attributes,
	     &error ) != 1 )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_RUNTIME,
		 LIBCERROR_RUNTIME_ERROR_GET_FAILED,
		 "%s: unable to retrieve number of extended attributes.",
		 function );

		result = -EIO;

		goto on_error;
	}
	for( extended_attribute_index = 0;
	     extended_attribute_index < number_of_extended_attributes;
	     extended_attribute_index++ )
	{
		if( libfsext_file_entry_get_extended_attribute_by_index(
		     file_entry->fsext_file_entry,
		     extended_attribute_index,
		     &extended_attribute,
		     &error ) != 1 )
		{
			libcerror_error_set(
			 &error,
			 LIBCERROR_ERROR_DOMAIN_RUNTIME,
			 LIBCERROR_RUNTIME_ERROR_GET_FAILED,
			 "%s: unable to retrieve extended attribute: %d.",
			 function,
			 extended_attribute_index );

			result = -EIO;

			goto on_error;
		}
		if( libfsext_extended_attribute_get_utf8_name_size(
		     extended_attribute,
		     &extended_attribute_name_size,
		     &error ) != 1 )
		{
			libcerror_error_set(
			 &error,
			 LIBCERROR_ERROR_DOMAIN_RUNTIME,
			 LIBCERROR_RUNTIME_ERROR_GET_FAILED,
			 "%s: unable to retrieve extended attribute: %d name string size.",
			 function,
			 extended_attribute_index );

			result = -EIO;

			goto on_error;
		}
		if( size > 0 )
		{
			if( extended_attribute_name_size > ( size - list_offset ) )
			{
				libcerror_error_set(
				 &error,
				 LIBCERROR_ERROR_DOMAIN_RUNTIME,
				 LIBCERROR_RUNTIME_ERROR_VALUE_OUT_OF_BOUNDS,
				 "%s: invalid extended attribute name size value out of bounds.",
				 function );

				result = -EIO;

				goto on_error;
			}
			if( libfsext_extended_attribute_get_utf8_name(
			     extended_attribute,
			     (uint8_t *) &( list[ list_offset ] ),
			     extended_attribute_name_size,
			     &error ) != 1 )
			{
				libcerror_error_set(
				 &error,
				 LIBCERROR_ERROR_DOMAIN_RUNTIME,
				 LIBCERROR_RUNTIME_ERROR_GET_FAILED,
				 "%s: unable to retrieve extended attribute name: %d string.",
				 function,
				 extended_attribute_index );

				result = -EIO;

				goto on_error;
			}
		}
		list_offset += extended_attribute_name_size;

		if( libfsext_extended_attribute_free(
		     &extended_attribute,
		     &error ) != 1 )
		{
			libcerror_error_set(
			 &error,
			 LIBCERROR_ERROR_DOMAIN_RUNTIME,
			 LIBCERROR_RUNTIME_ERROR_FINALIZE_FAILED,
			 "%s: unable to free extended attribute: %d.",
			 function,
			 extended_attribute_index );

			result = -EIO;

			goto on_error;
		}
	}
	if( mount_file_entry_free(
	     &file_entry,
	     &error ) != 1 )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_RUNTIME,
		 LIBCERROR_RUNTIME_ERROR_FINALIZE_FAILED,
		 "%s: unable to free file entry.",
		 function );

		result = -EIO;

		goto on_error;
	}
	return( (int) list_offset );

on_error:
	if( error != NULL )
	{
		libcnotify_print_error_backtrace(
		 error );
		libcerror_error_free(
		 &error );
	}
	if( extended_attribute != NULL )
	{
		libfsext_extended_attribute_free(
		 &extended_attribute,
		 NULL );
	}
	if( file_entry != NULL )
	{
		mount_file_entry_free(
		 &file_entry,
		 NULL );
	}
	return( result );
}

/* Opens a directory
 * Returns 0 if successful or a negative errno value otherwise
 */
int mount_fuse_opendir(
     const char *path,
     struct fuse_file_info *file_info )
{
	libcerror_error_t *error = NULL;
	static char *function    = "mount_fuse_opendir";
	int result               = 0;

#if defined( HAVE_DEBUG_OUTPUT )
	if( libcnotify_verbose != 0 )
	{
		libcnotify_printf(
		 "%s: %s\n",
		 function,
		 path );
	}
#endif
	if( path == NULL )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_ARGUMENTS,
		 LIBCERROR_ARGUMENT_ERROR_INVALID_VALUE,
		 "%s: invalid path.",
		 function );

		result = -EINVAL;

		goto on_error;
	}
	if( file_info == NULL )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_ARGUMENTS,
		 LIBCERROR_ARGUMENT_ERROR_INVALID_VALUE,
		 "%s: invalid file information.",
		 function );

		result = -EINVAL;

		goto on_error;
	}
	if( file_info->fh != (uint64_t) NULL )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_RUNTIME,
		 LIBCERROR_RUNTIME_ERROR_VALUE_ALREADY_SET,
		 "%s: invalid file information - file handle already set.",
		 function );

		result = -EINVAL;

		goto on_error;
	}
	if( mount_handle_get_file_entry_by_path(
	     fsextmount_mount_handle,
	     path,
	     (mount_file_entry_t **) &( file_info->fh ),
	     &error ) != 1 )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_RUNTIME,
		 LIBCERROR_RUNTIME_ERROR_GET_FAILED,
		 "%s: unable to retrieve file entry for path: %s.",
		 function,
		 path );

		result = -ENOENT;

		goto on_error;
	}
	return( 0 );

on_error:
	if( error != NULL )
	{
		libcnotify_print_error_backtrace(
		 error );
		libcerror_error_free(
		 &error );
	}
	return( result );
}

/* Reads a directory
 * Returns 0 if successful or a negative errno value otherwise
 */
int mount_fuse_readdir(
     const char *path,
     void *buffer,
     fuse_fill_dir_t filler,
     off_t offset FSEXTTOOLS_ATTRIBUTE_UNUSED,
     struct fuse_file_info *file_info FSEXTTOOLS_ATTRIBUTE_UNUSED )
{
	struct stat *stat_info             = NULL;
	libcerror_error_t *error           = NULL;
	mount_file_entry_t *sub_file_entry = NULL;
	static char *function              = "mount_fuse_readdir";
	char *name                         = NULL;
	size_t name_size                   = 0;
	int number_of_sub_file_entries     = 0;
	int result                         = 0;
	int sub_file_entry_index           = 0;

	FSEXTTOOLS_UNREFERENCED_PARAMETER( offset )

#if defined( HAVE_DEBUG_OUTPUT )
	if( libcnotify_verbose != 0 )
	{
		libcnotify_printf(
		 "%s: %s\n",
		 function,
		 path );
	}
#endif
	if( path == NULL )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_ARGUMENTS,
		 LIBCERROR_ARGUMENT_ERROR_INVALID_VALUE,
		 "%s: invalid path.",
		 function );

		result = -EINVAL;

		goto on_error;
	}
	if( file_info == NULL )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_ARGUMENTS,
		 LIBCERROR_ARGUMENT_ERROR_INVALID_VALUE,
		 "%s: invalid file information.",
		 function );

		result = -EINVAL;

		goto on_error;
	}
	if( file_info->fh == (uint64_t) NULL )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_RUNTIME,
		 LIBCERROR_RUNTIME_ERROR_VALUE_MISSING,
		 "%s: invalid file information - missing file handle.",
		 function );

		result = -EINVAL;

		goto on_error;
	}
	stat_info = memory_allocate_structure(
	             struct stat );

	if( stat_info == NULL )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_MEMORY,
		 LIBCERROR_MEMORY_ERROR_INSUFFICIENT,
		 "%s: unable to create stat info.",
		 function );

		result = errno;

		goto on_error;
	}
	if( mount_fuse_filldir(
	     buffer,
	     filler,
	     ".",
	     stat_info,
	     (mount_file_entry_t *) file_info->fh,
	     &error ) != 1 )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_RUNTIME,
		 LIBCERROR_RUNTIME_ERROR_SET_FAILED,
		 "%s: unable to set self directory entry.",
		 function );

		result = -EIO;

		goto on_error;
	}
	if( mount_fuse_filldir(
	     buffer,
	     filler,
	     "..",
	     stat_info,
	     NULL,
	     &error ) != 1 )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_RUNTIME,
		 LIBCERROR_RUNTIME_ERROR_SET_FAILED,
		 "%s: unable to set parent directory entry.",
		 function );

		result = -EIO;

		goto on_error;
	}
	if( mount_file_entry_get_number_of_sub_file_entries(
	     (mount_file_entry_t *) file_info->fh,
	     &number_of_sub_file_entries,
	     &error ) != 1 )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_RUNTIME,
		 LIBCERROR_RUNTIME_ERROR_GET_FAILED,
		 "%s: unable to retrieve number of sub file entries.",
		 function );

		result = -EIO;

		goto on_error;
	}
	for( sub_file_entry_index = 0;
	     sub_file_entry_index < number_of_sub_file_entries;
	     sub_file_entry_index++ )
	{
		if( mount_file_entry_get_sub_file_entry_by_index(
		     (mount_file_entry_t *) file_info->fh,
		     sub_file_entry_index,
		     &sub_file_entry,
		     &error ) != 1 )
		{
			libcerror_error_set(
			 &error,
			 LIBCERROR_ERROR_DOMAIN_RUNTIME,
			 LIBCERROR_RUNTIME_ERROR_GET_FAILED,
			 "%s: unable to retrieve sub file entry: %d.",
			 function,
			 sub_file_entry_index );

			result = -EIO;

			goto on_error;
		}
		if( mount_file_entry_get_name_size(
		     sub_file_entry,
		     &name_size,
		     &error ) != 1 )
		{
			libcerror_error_set(
			 &error,
			 LIBCERROR_ERROR_DOMAIN_RUNTIME,
			 LIBCERROR_RUNTIME_ERROR_GET_FAILED,
			 "%s: unable to retrieve sub file entry: %d name size.",
			 function,
			 sub_file_entry_index );

			result = -EIO;

			goto on_error;
		}
		name = narrow_string_allocate(
		        name_size );

		if( name == NULL )
		{
			libcerror_error_set(
			 &error,
			 LIBCERROR_ERROR_DOMAIN_MEMORY,
			 LIBCERROR_MEMORY_ERROR_INSUFFICIENT,
			 "%s: unable to create sub file entry: %d name.",
			 function );

			result = -EIO;

			goto on_error;
		}
		if( mount_file_entry_get_name(
		     sub_file_entry,
		     name,
		     name_size,
		     &error ) != 1 )
		{
			libcerror_error_set(
			 &error,
			 LIBCERROR_ERROR_DOMAIN_RUNTIME,
			 LIBCERROR_RUNTIME_ERROR_GET_FAILED,
			 "%s: unable to retrieve sub file entry: %d name.",
			 function,
			 sub_file_entry_index );

			result = -EIO;

			goto on_error;
		}
		if( mount_fuse_filldir(
		     buffer,
		     filler,
		     name,
		     stat_info,
		     sub_file_entry,
		     &error ) != 1 )
		{
			libcerror_error_set(
			 &error,
			 LIBCERROR_ERROR_DOMAIN_RUNTIME,
			 LIBCERROR_RUNTIME_ERROR_SET_FAILED,
			 "%s: unable to set directory entry.",
			 function );

			result = -EIO;

			goto on_error;
		}
		memory_free(
		 name );

		name = NULL;

		if( mount_file_entry_free(
		     &sub_file_entry,
		     &error ) != 1 )
		{
			libcerror_error_set(
			 &error,
			 LIBCERROR_ERROR_DOMAIN_RUNTIME,
			 LIBCERROR_RUNTIME_ERROR_FINALIZE_FAILED,
			 "%s: unable to free sub file entry: %d.",
			 function,
			 sub_file_entry_index );

			result = -EIO;

			goto on_error;
		}
	}
	memory_free(
	 stat_info );

	return( 0 );

on_error:
	if( error != NULL )
	{
		libcnotify_print_error_backtrace(
		 error );
		libcerror_error_free(
		 &error );
	}
	if( name != NULL )
	{
		memory_free(
		 name );
	}
	if( sub_file_entry != NULL )
	{
		mount_file_entry_free(
		 &sub_file_entry,
		 NULL );
	}
	if( stat_info != NULL )
	{
		memory_free(
		 stat_info );
	}
	return( result );
}

/* Releases a directory entry
 * Returns 0 if successful or a negative errno value otherwise
 */
int mount_fuse_releasedir(
     const char *path,
     struct fuse_file_info *file_info )
{
	libcerror_error_t *error = NULL;
	static char *function    = "mount_fuse_releasedir";
	int result               = 0;

#if defined( HAVE_DEBUG_OUTPUT )
	if( libcnotify_verbose != 0 )
	{
		libcnotify_printf(
		 "%s: %s\n",
		 function,
		 path );
	}
#endif
	if( path == NULL )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_ARGUMENTS,
		 LIBCERROR_ARGUMENT_ERROR_INVALID_VALUE,
		 "%s: invalid path.",
		 function );

		result = -EINVAL;

		goto on_error;
	}
	if( file_info == NULL )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_ARGUMENTS,
		 LIBCERROR_ARGUMENT_ERROR_INVALID_VALUE,
		 "%s: invalid file information.",
		 function );

		result = -EINVAL;

		goto on_error;
	}
	if( file_info->fh != (uint64_t) NULL )
	{
		file_info->fh = (uint64_t) NULL;
	}
	return( 0 );

on_error:
	if( error != NULL )
	{
		libcnotify_print_error_backtrace(
		 error );
		libcerror_error_free(
		 &error );
	}
	return( result );
}

/* Retrieves the file stat info
 * Returns 0 if successful or a negative errno value otherwise
 */
int mount_fuse_getattr(
     const char *path,
     struct stat *stat_info )
{
	libcerror_error_t *error       = NULL;
	mount_file_entry_t *file_entry = NULL;
	static char *function          = "mount_fuse_getattr";
	size64_t file_size             = 0;
	uint64_t access_time           = 0;
	uint64_t inode_change_time     = 0;
	uint64_t modification_time     = 0;
	uint16_t file_mode             = 0;
	int result                     = 0;

#if defined( HAVE_DEBUG_OUTPUT )
	if( libcnotify_verbose != 0 )
	{
		libcnotify_printf(
		 "%s: %s\n",
		 function,
		 path );
	}
#endif
	if( path == NULL )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_ARGUMENTS,
		 LIBCERROR_ARGUMENT_ERROR_INVALID_VALUE,
		 "%s: invalid path.",
		 function );

		result = -EINVAL;

		goto on_error;
	}
	if( stat_info == NULL )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_ARGUMENTS,
		 LIBCERROR_ARGUMENT_ERROR_INVALID_VALUE,
		 "%s: invalid stat info.",
		 function );

		result = -EINVAL;

		goto on_error;
	}
	if( memory_set(
	     stat_info,
	     0,
	     sizeof( struct stat ) ) == NULL )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_MEMORY,
		 LIBCERROR_MEMORY_ERROR_SET_FAILED,
		 "%s: unable to clear stat info.",
		 function );

		result = errno;

		goto on_error;
	}
	result = mount_handle_get_file_entry_by_path(
	          fsextmount_mount_handle,
	          path,
	          &file_entry,
	          &error );

	if( result == -1 )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_RUNTIME,
		 LIBCERROR_RUNTIME_ERROR_GET_FAILED,
		 "%s: unable to retrieve value for: %s.",
		 function,
		 path );

		result = -ENOENT;

		goto on_error;
	}
	else if( result == 0 )
	{
		return( -ENOENT );
	}
	if( mount_file_entry_get_size(
	     file_entry,
	     &file_size,
	     &error ) != 1 )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_RUNTIME,
		 LIBCERROR_RUNTIME_ERROR_GET_FAILED,
		 "%s: unable to retrieve file entry size.",
		 function );

		result = -EIO;

		goto on_error;
	}
	if( mount_file_entry_get_file_mode(
	     file_entry,
	     &file_mode,
	     &error ) != 1 )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_RUNTIME,
		 LIBCERROR_RUNTIME_ERROR_GET_FAILED,
		 "%s: unable to retrieve file mode.",
		 function );

		result = -EIO;

		goto on_error;
	}
	if( mount_file_entry_get_access_time(
	     file_entry,
	     &access_time,
	     &error ) != 1 )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_RUNTIME,
		 LIBCERROR_RUNTIME_ERROR_GET_FAILED,
		 "%s: unable to retrieve access time.",
		 function );

		result = -EIO;

		goto on_error;
	}
	if( mount_file_entry_get_modification_time(
	     file_entry,
	     &modification_time,
	     &error ) != 1 )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_RUNTIME,
		 LIBCERROR_RUNTIME_ERROR_GET_FAILED,
		 "%s: unable to retrieve modification time.",
		 function );

		result = -EIO;

		goto on_error;
	}
	if( mount_file_entry_get_inode_change_time(
	     file_entry,
	     &inode_change_time,
	     &error ) != 1 )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_RUNTIME,
		 LIBCERROR_RUNTIME_ERROR_GET_FAILED,
		 "%s: unable to retrieve inode change time.",
		 function );

		result = -EIO;

		goto on_error;
	}
	if( mount_fuse_set_stat_info(
	     stat_info,
	     file_size,
	     file_mode,
	     (int64_t) access_time,
	     (int64_t) inode_change_time,
	     (int64_t) modification_time,
	     &error ) != 1 )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_RUNTIME,
		 LIBCERROR_RUNTIME_ERROR_SET_FAILED,
		 "%s: unable to set stat info.",
		 function );

		result = -EIO;

		goto on_error;
	}
	if( mount_file_entry_free(
	     &file_entry,
	     &error ) != 1 )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_RUNTIME,
		 LIBCERROR_RUNTIME_ERROR_FINALIZE_FAILED,
		 "%s: unable to free file entry.",
		 function );

		result = -EIO;

		goto on_error;
	}
	return( 0 );

on_error:
	if( error != NULL )
	{
		libcnotify_print_error_backtrace(
		 error );
		libcerror_error_free(
		 &error );
	}
	if( file_entry != NULL )
	{
		mount_file_entry_free(
		 &file_entry,
		 NULL );
	}
	return( result );
}

/* Reads the target of a symbolic link
 * Returns 0 if successful or a negative errno value otherwise
 */
int mount_fuse_readlink(
     const char *path,
     char *buffer,
     size_t size )
{
	libcerror_error_t *error       = NULL;
	mount_file_entry_t *file_entry = NULL;
	static char *function          = "mount_fuse_readlink";
	int result                     = 0;

#if defined( HAVE_DEBUG_OUTPUT )
	if( libcnotify_verbose != 0 )
	{
		libcnotify_printf(
		 "%s: %s\n",
		 function,
		 path );
	}
#endif
	if( path == NULL )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_ARGUMENTS,
		 LIBCERROR_ARGUMENT_ERROR_INVALID_VALUE,
		 "%s: invalid path.",
		 function );

		result = -EINVAL;

		goto on_error;
	}
	result = mount_handle_get_file_entry_by_path(
	          fsextmount_mount_handle,
	          path,
	          &file_entry,
	          &error );

	if( result == -1 )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_RUNTIME,
		 LIBCERROR_RUNTIME_ERROR_GET_FAILED,
		 "%s: unable to retrieve value for: %s.",
		 function,
		 path );

		result = -ENOENT;

		goto on_error;
	}
	else if( result == 0 )
	{
		return( -ENOENT );
	}
	if( mount_file_entry_get_symbolic_link_target(
	     file_entry,
	     buffer,
	     size,
	     &error ) != 1 )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_RUNTIME,
		 LIBCERROR_RUNTIME_ERROR_GET_FAILED,
		 "%s: unable to retrieve symbolic link target string.",
		 function );

		result = -EIO;

		goto on_error;
	}
	if( mount_file_entry_free(
	     &file_entry,
	     &error ) != 1 )
	{
		libcerror_error_set(
		 &error,
		 LIBCERROR_ERROR_DOMAIN_RUNTIME,
		 LIBCERROR_RUNTIME_ERROR_FINALIZE_FAILED,
		 "%s: unable to free file entry.",
		 function );

		result = -EIO;

		goto on_error;
	}
	return( 0 );

on_error:
	if( error != NULL )
	{
		libcnotify_print_error_backtrace(
		 error );
		libcerror_error_free(
		 &error );
	}
	if( file_entry != NULL )
	{
		mount_file_entry_free(
		 &file_entry,
		 NULL );
	}
	return( result );
}

/* Cleans up when fuse is done
 */
void mount_fuse_destroy(
      void *private_data FSEXTTOOLS_ATTRIBUTE_UNUSED )
{
	libcerror_error_t *error = NULL;
	static char *function    = "mount_fuse_destroy";

	FSEXTTOOLS_UNREFERENCED_PARAMETER( private_data )

#if defined( HAVE_DEBUG_OUTPUT )
	if( libcnotify_verbose != 0 )
	{
		libcnotify_printf(
		 "%s\n",
		 function );
	}
#endif
	if( fsextmount_mount_handle != NULL )
	{
		if( mount_handle_free(
		     &fsextmount_mount_handle,
		     &error ) != 1 )
		{
			libcerror_error_set(
			 &error,
			 LIBCERROR_ERROR_DOMAIN_RUNTIME,
			 LIBCERROR_RUNTIME_ERROR_FINALIZE_FAILED,
			 "%s: unable to free mount handle.",
			 function );

			goto on_error;
		}
	}
	return;

on_error:
	if( error != NULL )
	{
		libcnotify_print_error_backtrace(
		 error );
		libcerror_error_free(
		 &error );
	}
	return;
}

#endif /* defined( HAVE_LIBFUSE ) || defined( HAVE_LIBOSXFUSE ) */

