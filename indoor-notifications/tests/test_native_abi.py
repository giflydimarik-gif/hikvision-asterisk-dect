"""Call a compiled local C transport stub using the real ctypes path."""
import ctypes as C
from datetime import datetime, timezone
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from indoor_notice import Notice, sdk_send


class NativeABITests(unittest.TestCase):
    def test_native_signature_layout_and_existing_wrapper_unchanged(self):
        if not shutil.which("cc"):
            self.skipTest("C compiler unavailable")
        code = r'''
        #include <stdint.h>
        #include <stddef.h>
        typedef struct { uint16_t year; uint8_t rest[6]; } TimeEx;
        typedef struct { void *data; uint32_t length; uint8_t reserved[32]; } Pic;
        typedef struct { uint32_t size; TimeEx time; uint8_t id[32],title[64],body[1024];
                         uint8_t level,count,r1[2]; Pic pictures[6]; uint8_t r2[128]; } Notice;
        _Static_assert(sizeof(Notice)==1552, "notice size");
        _Static_assert(offsetof(Notice,pictures)==1136, "picture offset");
        int32_t NET_DVR_RemoteControl(int32_t user, uint32_t command, void *buffer, uint32_t size) {
            Notice *n=buffer;
            return user==2147483647 && command==16008 && size==1552 && n->size==1552 &&
                   n->level==3 && n->count==0 && n->id[0]=='t' && n->r2[127]==0;
        }
        uint32_t NET_DVR_GetLastError(void) { return 29; }
        '''
        with tempfile.TemporaryDirectory() as temp:
            source, output = Path(temp) / "stub.c", Path(temp) / "stub.so"
            source.write_text(code)
            subprocess.run(["cc", "-shared", "-fPIC", "-std=c11", str(source), "-o", str(output)], check=True, capture_output=True)
            sdk = C.CDLL(str(output))
            sdk.NET_DVR_RemoteControl.argtypes = None
            notice = Notice("test", "Тема", "Текст", datetime.now(timezone.utc), "alarm")
            self.assertEqual(sdk_send(sdk, 2147483647, notice)["status"], "accepted")
            self.assertIsNone(sdk.NET_DVR_RemoteControl.argtypes)
            self.assertEqual(sdk_send(sdk, 1, notice)["status"], "rejected")


if __name__ == "__main__":
    unittest.main()
