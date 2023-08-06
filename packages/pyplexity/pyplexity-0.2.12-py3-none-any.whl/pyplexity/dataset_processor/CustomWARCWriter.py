# PyPlexity
# Copyright (C) 2022 Manuel Prada Corral
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# -*- coding: utf-8 -*-

import zlib

from socket import gethostname

from warcio.recordbuilder import RecordBuilder

from warcio.statusandheaders import StatusAndHeadersParser


# ============================================================================
class BaseWARCWriter(RecordBuilder):

    def __init__(self, gzip=True, *args, **kwargs):
        super(BaseWARCWriter, self).__init__(warc_version=kwargs.get('warc_version'),
                                             header_filter=kwargs.get('header_filter'))
        self.gzip = gzip
        self.hostname = gethostname()

        self.parser = StatusAndHeadersParser([], verify=False)

    def write_request_response_pair(self, req, resp, params=None):
        url = resp.rec_headers.get_header('WARC-Target-URI')
        dt = resp.rec_headers.get_header('WARC-Date')

        req.rec_headers.replace_header('WARC-Target-URI', url)
        req.rec_headers.replace_header('WARC-Date', dt)

        resp_id = resp.rec_headers.get_header('WARC-Record-ID')
        if resp_id:
            req.rec_headers.add_header('WARC-Concurrent-To', resp_id)

        self._do_write_req_resp(req, resp, params)

    def write_record(self, record, params=None):  # pragma: no cover
        raise NotImplemented()

    def _do_write_req_resp(self, req, resp, params):  # pragma: no cover
        raise NotImplemented()

    def _write_warc_record(self, out, record):
        if self.gzip:
            out = GzippingWrapper(out)

        if record.http_headers:
            record.http_headers.headers_buff = \
                record.http_headers.to_str(self.header_filter).encode('ascii', errors='replace') + b'\r\n'

        # Content-Length is None/unknown
        # Fix record by: buffering and recomputing all digests and length
        # (since no length, can't trust existing digests)
        # Also remove content-type for consistent header ordering
        if record.length is None:
            record.rec_headers.remove_header('WARC-Block-Digest')
            if record.rec_type != 'revisit':
                record.rec_headers.remove_header('WARC-Payload-Digest')
            record.rec_headers.remove_header('Content-Type')

            self.ensure_digest(record, block=True, payload=True)

            record.length = record.payload_length

        # ensure digests are set
        else:
            self.ensure_digest(record, block=True, payload=True)

        if record.content_type != None:
            # ensure proper content type
            record.rec_headers.replace_header('Content-Type', record.content_type)

        if record.rec_type == 'revisit':
            http_headers_only = True
        else:
            http_headers_only = False

        # compute Content-Length
        if record.http_headers and record.payload_length >= 0:
            actual_len = 0

            if record.http_headers:
                actual_len = len(record.http_headers.headers_buff)

            if not http_headers_only:
                actual_len += record.payload_length

            record.length = actual_len

        record.rec_headers.replace_header('Content-Length', str(record.length))

        # write record headers -- encoded as utf-8
        # WARC headers can be utf-8 per spec
        out.write(record.rec_headers.to_bytes(encoding='utf-8'))

        # write headers buffer, if any
        if record.http_headers:
            out.write(record.http_headers.headers_buff)

        if not http_headers_only:
            try:
                for buf in self._iter_stream(record.raw_stream):
                    out.write(buf)
            finally:
                if hasattr(record, '_orig_stream'):
                    record.raw_stream.close()
                    record.raw_stream = record._orig_stream

        # add two lines
        out.write(b'\r\n\r\n')

        out.flush()

# ============================================================================
class GzippingWrapper(object):
    def __init__(self, out):
        self.compressor = zlib.compressobj(9, zlib.DEFLATED, zlib.MAX_WBITS + 16)
        self.out = out

    def write(self, buff):
        if isinstance(buff, str):
            buff = buff.encode('utf-8')
        buff = self.compressor.compress(buff)
        self.out.write(buff)

    def flush(self):
        buff = self.compressor.flush()
        self.out.write(buff)
        self.out.flush()


# ============================================================================
class CustomWARCWriter(BaseWARCWriter):
    def __init__(self, filebuf, *args, **kwargs):
        super(CustomWARCWriter, self).__init__(*args, **kwargs)
        self.out = filebuf

    def write_record(self, record, params=None):
        self._write_warc_record(self.out, record)

    def _do_write_req_resp(self, req, resp, params):
        self._write_warc_record(self.out, resp)
        self._write_warc_record(self.out, req)


# ============================================================================
class BufferWARCWriter(CustomWARCWriter):
    def __init__(self, *args, **kwargs):
        out = self._create_temp_file()
        super(BufferWARCWriter, self).__init__(out, *args, **kwargs)

    def get_contents(self):
        pos = self.out.tell()
        self.out.seek(0)
        buff = self.out.read()
        self.out.seek(pos)
        return buff

    def get_stream(self):
        self.out.seek(0)
        return self.out
