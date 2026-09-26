import struct
import hashlib

def create_signable_arm64_macho(output_path, bundle_id="com.phuquy.testkey"):
    # Target page size on arm64: 0x4000 (16KB)
    PAGE_SIZE = 0x4000

    # Segments:
    # 0: __PAGEZERO: vmaddr=0, vmsize=0x100000000, fileoff=0, filesize=0
    # 1: __TEXT:     vmaddr=0x100000000, vmsize=0x4000, fileoff=0, filesize=0x4000 (r-x)
    # 2: __DATA:     vmaddr=0x100004000, vmsize=0x4000, fileoff=0x4000, filesize=0x4000 (rw-)
    # 3: __LINKEDIT: vmaddr=0x100008000, vmsize=0x4000, fileoff=0x8000, filesize=0x4000 (r--)

    magic = 0xfeedfacf       # MH_MAGIC_64
    cputype = 0x0100000c     # CPU_TYPE_ARM64
    cpusubtype = 0x00000000  # CPU_SUBTYPE_ARM64_ALL
    filetype = 0x2           # MH_EXECUTE
    flags = 0x00200085       # MH_NOUNDEFS | MH_DYLDLINK | MH_TWOLEVEL | MH_PIE

    # 1. LC_SEGMENT_64 (__PAGEZERO)
    lc_pagezero = struct.pack(
        "<II16sQQQQIIII",
        0x19, 72,
        b"__PAGEZERO\x00\x00\x00\x00\x00\x00",
        0x0000000000000000, 0x0000000100000000,
        0, 0,
        0, 0,
        0, 0
    )

    # 2. LC_SEGMENT_64 (__TEXT) with 2 sections: __text, __cstring
    lc_text = struct.pack(
        "<II16sQQQQIIII",
        0x19, 72 + 80 * 2,
        b"__TEXT\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
        0x0000000100000000, PAGE_SIZE,
        0, PAGE_SIZE,
        7, 5, # max rwx, init r-x
        2, 0  # 2 sections
    )
    sect_text = struct.pack(
        "<16s16sQQIIIIIIII",
        b"__text\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
        b"__TEXT\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
        0x0000000100000000 + 0x1000, 0x40,
        0x1000, 2,
        0, 0,
        0x80000400, 0, 0, 0
    )
    sect_cstring = struct.pack(
        "<16s16sQQIIIIIIII",
        b"__cstring\x00\x00\x00\x00\x00\x00\x00",
        b"__TEXT\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
        0x0000000100000000 + 0x1040, 0x40,
        0x1040, 0,
        0, 0,
        0x00000002, 0, 0, 0
    )

    # 3. LC_SEGMENT_64 (__DATA) with 1 section: __data
    lc_data = struct.pack(
        "<II16sQQQQIIII",
        0x19, 72 + 80,
        b"__DATA\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
        0x0000000100000000 + PAGE_SIZE, PAGE_SIZE,
        PAGE_SIZE, PAGE_SIZE,
        7, 3, # max rwx, init rw-
        1, 0  # 1 section
    )
    sect_data = struct.pack(
        "<16s16sQQIIIIIIII",
        b"__data\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
        b"__DATA\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
        0x0000000100000000 + PAGE_SIZE, 0x20,
        PAGE_SIZE, 3,
        0, 0,
        0x00000000, 0, 0, 0
    )

    # 4. LC_SEGMENT_64 (__LINKEDIT) - CRITICAL for ldid / Scarlet / ESign
    lc_linkedit = struct.pack(
        "<II16sQQQQIIII",
        0x19, 72,
        b"__LINKEDIT\x00\x00\x00\x00\x00\x00",
        0x0000000100000000 + PAGE_SIZE * 2, PAGE_SIZE,
        PAGE_SIZE * 2, PAGE_SIZE,
        7, 1, # max rwx, init r--
        0, 0
    )

    # 5. LC_DYLD_INFO_ONLY (cmd=0x80000022, cmdsize=48)
    lc_dyld_info = struct.pack(
        "<IIIIIIIIIIII",
        0x80000022, 48,
        0, 0, # rebase
        0, 0, # bind
        0, 0, # weak bind
        0, 0, # lazy bind
        0, 0  # export
    )

    # 6. LC_SYMTAB (cmd=0x2, cmdsize=24)
    # symoff at beginning of LINKEDIT: 0x8000
    lc_symtab = struct.pack(
        "<IIIIII",
        0x2, 24,
        PAGE_SIZE * 2, 0, # symoff, nsyms
        PAGE_SIZE * 2, 0  # stroff, strsize
    )

    # 7. LC_DYSYMTAB (cmd=0xb, cmdsize=80)
    lc_dysymtab = struct.pack(
        "<IIIIIIIIIIIIIIIIIIII",
        0xb, 80,
        0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    )

    # 8. LC_LOAD_DYLINKER (/usr/lib/dyld)
    dylinker_str = b"/usr/lib/dyld\x00"
    dylinker_cmdsize = (12 + len(dylinker_str) + 7) & ~7
    lc_dylinker = struct.pack("<III", 0xe, dylinker_cmdsize, 12) + dylinker_str
    lc_dylinker += b"\x00" * (dylinker_cmdsize - len(lc_dylinker))

    # 9. LC_MAIN (entry point)
    lc_main = struct.pack("<IIQQ", 0x80000028, 24, 0x1000, 0)

    # 10. LC_LOAD_DYLIBs
    def make_dylib(name):
        bname = name.encode("utf-8") + b"\x00"
        csize = (24 + len(bname) + 7) & ~7
        cmd = struct.pack("<IIIIII", 0xc, csize, 24, 0, 0x00010000, 0x00010000) + bname
        return cmd + b"\x00" * (csize - len(cmd))

    lc_dylib_sys = make_dylib("/usr/lib/libSystem.B.dylib")
    lc_dylib_uikit = make_dylib("/System/Library/Frameworks/UIKit.framework/UIKit")
    lc_dylib_fnd = make_dylib("/System/Library/Frameworks/Foundation.framework/Foundation")
    lc_dylib_objc = make_dylib("/usr/lib/libobjc.A.dylib")

    # 11. LC_BUILD_VERSION (iOS 13.0, SDK 17.0)
    lc_build = struct.pack("<IIIIII", 0x32, 24, 2, (13 << 16), (17 << 16), 0)

    # 12. LC_CODE_SIGNATURE (cmd=0x1d, cmdsize=16)
    sig_offset = PAGE_SIZE * 2
    sig_size = 0x800
    lc_code_sig = struct.pack("<IIII", 0x1d, 16, sig_offset, sig_size)

    commands = [
        lc_pagezero,
        lc_text, sect_text, sect_cstring,
        lc_data, sect_data,
        lc_linkedit,
        lc_dyld_info,
        lc_symtab,
        lc_dysymtab,
        lc_dylinker,
        lc_main,
        lc_dylib_sys,
        lc_dylib_uikit,
        lc_dylib_fnd,
        lc_dylib_objc,
        lc_build,
        lc_code_sig
    ]
    load_commands_data = b"".join(commands)
    ncmds = len(commands) - 3 # subtract section structs which are part of segment commands
    # Exactly:
    # 1. pagezero (1)
    # 2. text (1)
    # 3. data (1)
    # 4. linkedit (1)
    # 5. dyld_info (1)
    # 6. symtab (1)
    # 7. dysymtab (1)
    # 8. dylinker (1)
    # 9. main (1)
    # 10. dylib_sys (1)
    # 11. dylib_uikit (1)
    # 12. dylib_fnd (1)
    # 13. dylib_objc (1)
    # 14. build (1)
    # 15. code_sig (1)
    actual_ncmds = 15
    sizeofcmds = len(load_commands_data)

    header = struct.pack(
        "<IIIIIIII",
        magic, cputype, cpusubtype, filetype,
        actual_ncmds, sizeofcmds, flags, 0
    )

    # Build binary file:
    # 0x0000 - 0x3fff: Header + Load commands + padding + arm64 entrypoint code
    pre_text = header + load_commands_data
    if len(pre_text) > 0x1000:
        raise ValueError(f"Header too large: {len(pre_text)}")

    # ARM64 code at 0x1000:
    # UIApplicationMain(argc, argv, nil, @"AppDelegate")
    # or simple exit(0)
    # mov x0, #0; ret
    arm64_code = b"\x00\x00\x80\xd2\xc0\x03\x5f\xd6" + b"\x00" * (0x40 - 8)
    cstring_data = b"TEST PHUQUY iOS 26 Auth\x00" + b"\x00" * 39

    segment_text_content = pre_text + (b"\x00" * (0x1000 - len(pre_text))) + arm64_code + cstring_data
    segment_text_content += b"\x00" * (PAGE_SIZE - len(segment_text_content))

    # 0x4000 - 0x7fff: __DATA segment
    segment_data_content = b"\x00" * PAGE_SIZE

    # 0x8000 - 0xbfff: __LINKEDIT segment with CodeSignature SuperBlob
    # Code Signature SuperBlob (magic = 0xfade0cc0)
    # 1 blob: CodeDirectory (type = 0, magic = 0xfade0c02)
    ident = bundle_id.encode("utf-8") + b"\x00"
    n_code_slots = (PAGE_SIZE * 2) // 4096 # 8 slots
    hash_size = 32 # SHA-256
    cd_header_size = 88 # CS_CodeDirectory v0x20400
    ident_offset = cd_header_size
    hash_offset = ident_offset + len(ident)
    cd_length = hash_offset + n_code_slots * hash_size

    # Hashes of pages in __TEXT and __DATA:
    pre_sig_data = segment_text_content + segment_data_content
    hashes = b""
    for i in range(n_code_slots):
        page = pre_sig_data[i*4096 : (i+1)*4096]
        hashes += hashlib.sha256(page).digest()

    cd_blob = struct.pack(
        ">IIIIIIIIIIBBHIIII",
        0xfade0c02,       # magic (CSMAGIC_CODEDIRECTORY)
        cd_length,        # length
        0x00020400,       # version
        0,                # flags
        hash_offset,      # hashOffset
        ident_offset,     # identOffset
        0,                # nSpecialSlots
        n_code_slots,     # nCodeSlots
        PAGE_SIZE * 2,    # codeLimit
        hash_size,        # hashSize
        2,                # hashType (CS_HASHTYPE_SHA256)
        0,                # platform
        12,               # pageSize (2^12 = 4096)
        0,                # spare2
        0,                # scatterOffset
        0,                # teamOffset
        0                 # execSegBase
    ) + ident + hashes

    # SuperBlob:
    sb_header_size = 12 + 8 # magic(4), length(4), count(4), index[type(4), offset(4)]
    super_blob = struct.pack(
        ">III II",
        0xfade0cc0,
        sb_header_size + len(cd_blob),
        1,
        0, # CSSLOT_CODEDIRECTORY
        sb_header_size
    ) + cd_blob

    linkedit_content = super_blob + b"\x00" * (PAGE_SIZE - len(super_blob))

    full_binary = segment_text_content + segment_data_content + linkedit_content
    with open(output_path, "wb") as f:
        f.write(full_binary)
    print(f"Generated Signable Mach-O Binary: {output_path} ({len(full_binary)} bytes)")

if __name__ == "__main__":
    create_signable_arm64_macho("test_bin")
