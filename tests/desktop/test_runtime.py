import importlib.util,hashlib
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('runtime_pack',ROOT/'scripts/package.py');pack=importlib.util.module_from_spec(spec);spec.loader.exec_module(pack)
def test_runtime_checksum_mismatch_is_rejected(tmp_path):
    p=tmp_path/'runtime.zip';p.write_bytes(b'invalid archive')
    with pytest.raises(ValueError,match='checksum'):pack.verify_download(p,'0'*64)

def test_actual_windows_distribution():
    path=ROOT/'dist'/pack.archive_name('windows-x64')
    metadata=pack.verify_windows(path)
    assert metadata['platform']=='desktop'
