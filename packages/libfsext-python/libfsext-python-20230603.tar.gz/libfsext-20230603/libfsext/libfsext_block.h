/*
 * Block functions
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

#if !defined( _LIBFSEXT_BLOCK_H )
#define _LIBFSEXT_BLOCK_H

#include <common.h>
#include <types.h>

#include "libfsext_libbfio.h"
#include "libfsext_libcerror.h"

#if defined( __cplusplus )
extern "C" {
#endif

typedef struct libfsext_block libfsext_block_t;

struct libfsext_block
{
	/* The data
	 */
	uint8_t *data;

	/* The data size
	 */
	size_t data_size;
};

int libfsext_block_initialize(
     libfsext_block_t **block,
     size_t data_size,
     libcerror_error_t **error );

int libfsext_block_free(
     libfsext_block_t **block,
     libcerror_error_t **error );

int libfsext_block_read_file_io_handle(
     libfsext_block_t *block,
     libbfio_handle_t *file_io_handle,
     off64_t file_offset,
     libcerror_error_t **error );

#if defined( __cplusplus )
}
#endif

#endif /* !defined( _LIBFSEXT_BLOCK_H ) */

