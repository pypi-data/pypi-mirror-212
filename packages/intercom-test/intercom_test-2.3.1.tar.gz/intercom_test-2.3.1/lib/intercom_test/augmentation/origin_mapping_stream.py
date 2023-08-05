from bisect import bisect_right
import io
import os

def open(
    path: os.PathLike,
    *,
    buffer_size: int = io.DEFAULT_BUFFER_SIZE,
) -> io.TextIOBase:
    """Open a UTF-8 encoded file for reading with origin-byte tracking
    
    :param path: file path to open, like :func:`io.open`
    :keyword buffer_size: size of buffer to use for :class:`io.BufferedReader`
    :returns: text reader with an :attr:`origin_mapper`
    
    To correctly jump to the starting point of a test case, :mod:`intercom_test`
    needs the *byte offset* in the file, while the YAML parser reports position
    in terms of characters.  This requires taking the text encoding into
    account.  To do this efficiently, the object returned by this function
    provides an :attr:`origin_mapper`, which is an :class:`.OriginMapper`
    instance.
    
    As a consequence of needing to start in the middle of the file, the only
    Unicode encoding that can be supported is UTF-8.
    
    The stream does not currently support seeking forward.
    """
    return _PosmapTextWrapper(
        io.open(path, 'rb', buffering=0),
        buffer_size
    )

class _RawPosmapStream(io.RawIOBase):
    def __init__(self, base_stream):
        self._base_stream = base_stream
        self._lb_invlist = [] # Leading (or single) byte mode inversion list
        self._chr_pos = 0
        self._chr_dc = [0] # character discontinuities
        self._chr_cor = [0] # character corrections
        self._lb = True # Last byte seen was a leading byte
        self._crs = set()
        self._last_pos = base_stream.tell()
    
    def readable(self, ):
        return True
    
    def readinto(self, b):
        base = self._base_stream
        start_pos = base.tell()
        if start_pos > self._last_pos:
            raise IOError(f"Underlying stream skipped from {self._last_pos} to {start_pos}")
        if start_pos < self._last_pos:
            self._lb = not (bisect_right(self._lb_invlist, start_pos) & 0x1)
        result = base.readinto(b)
        for i in range(result):
            is_lb = (b[i] & 0xc0) != 0x80 \
                and (b[i] != 0xa or (start_pos + i - 1) not in self._crs)
            if is_lb != self._lb:
                self._lb_invlist.append(start_pos + i)
                if is_lb:
                    self._chr_cor.append(start_pos + i)
                else:
                    self._chr_dc.append(self._chr_pos)
                self._lb = is_lb
            if is_lb:
                self._chr_pos += 1
            if b[i] == 0xd:
                self._crs.add(start_pos + i)
        self._last_pos += result
        return result

class OriginMapper:
    __slots__ = ('discontinuities', 'corrections')
    def __init__(self, mapper):
        self.discontinuities = mapper._chr_dc
        self.corrections = mapper._chr_cor
    
    def tell_of_chr(self, n):
        """Given a *character* index, compute the *byte* index in the source file
        
        Due to character encodings and line-ending conventions, each *character*
        produced from a stream comes from one *or more* bytes in the input
        file.  Partial-reading a YAML file requires knowing the exact byte
        offset into the file at which to start.  This function allows "back
        mapping" from the :attr:`index` in a YAML event's :attr:`start_mark` to
        the byte offset within the file.
        """
        dc_i = bisect_right(self.discontinuities, n) - 1
        cp = self.discontinuities[dc_i]
        return self.corrections[dc_i] + (n - cp)

class _PosmapTextWrapper(io.TextIOWrapper):
    def __init__(self, raw_io, buffer_size):
        mapped = _RawPosmapStream(raw_io)
        buffered = io.BufferedReader(mapped, buffer_size=buffer_size)
        super().__init__(buffered, encoding='utf8')
        self.origin_mapper = OriginMapper(mapped)
        self.tell_of_chr = self.origin_mapper.tell_of_chr
        self._to_close = [buffered, mapped, raw_io]
    
    def close(self):
        super().close()
        for l in self._to_close:
            l.close()
