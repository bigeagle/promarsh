#!/usr/bin/env python2
# -*- coding:utf-8 -*-
import sys
sys.path.insert(0, '..')
from promarsh import *


IPProtocolEnum = Enum[UInt8b](
    ICMP=1,
    TCP=6,
    UDP=17
)

IP4_Header = Struct(
    EmbeddedBitStruct(
        "version" << UBitIntb[4],
        "header_len" << UBitIntb[4],
        after_unpack=lambda ctx, v: ctx.set("header_len", v.header_len * 4)
    ),
    EmbeddedBitStruct(
        "DSCP" << UBitIntb[6],
        "ECN" << UBitIntb[2],
    ),
    "total_len" << UInt16b,
    "id" << UInt16b,
    EmbeddedBitStruct(
        "flags" << BitStruct(
            BitPadding[1],
            'DF' << BitFlag,
            'MF' << BitFlag,
        ),
        "frag_offset" << UBitIntb[13],
    ),
    "TTL" << UInt8b,
    "protocol" << UInt8b,
    "checksum" << UInt16b,
    "src" << Array[UInt8b:4],
    "dst" << Array[UInt8b:4],
)

TCP_Header = Struct(
    "src_port" << UInt16b,
    "dst_port" << UInt16b,
    "seq" << UInt32b,
    "ack_seq" << UInt32b,
    EmbeddedBitStruct(
        "data_offset" << UBitIntb[4],
        "Reserved" << UBitIntb[3],
        "Flags" << BitStruct(
            "NS" << BitFlag,
            "CWR" << BitFlag,
            "ECE" << BitFlag,
            "URG" << BitFlag,
            "ACK" << BitFlag,
            "PSH" << BitFlag,
            "RST" << BitFlag,
            "SYN" << BitFlag,
            "FIN" << BitFlag
        ),
    ),
    "win_size" << UInt16b,
    "checksum" << UInt16b,

)

if __name__ == "__main__":
    ipv4_pack = list_to_bytestring([
        0x45, 0x00, 0x00, 0x34, 0x81, 0x53, 0x40, 0x00, 0x30, 0x06, 0xeb, 0x64, 0x17, 0x15, 0xb7, 0xca,
        0x0a, 0x2a, 0x05, 0x03, 0x01, 0xbb, 0xe9, 0xff, 0x57, 0x11, 0x0e, 0x49, 0xf3, 0xac, 0xb2, 0x62,
        0x80, 0x10, 0x00, 0x46, 0x41, 0x49, 0x00, 0x00, 0x01, 0x01, 0x08, 0x0a, 0x50, 0xe1, 0xb8, 0x47,
        0x15, 0x70, 0x41, 0x64,
    ])
    with context():
        ip4_header, buf = IP4_Header.deserialize_from(ipv4_pack)
        print ip4_header
        tcp_header, buf = TCP_Header.deserialize_from(buf)
        print tcp_header

# vim: ts=4 sw=4 sts=4 expandtab
