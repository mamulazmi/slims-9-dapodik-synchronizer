from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, Undefined, config
from typing import Optional, TYPE_CHECKING
from uuid import UUID
import os
import hashlib

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class PesertaDidik:
    registrasi_id: UUID
    peserta_didik_id: UUID
    jenis_pendaftaran_id: int
    jenis_pendaftaran_id_str: str
    tanggal_masuk_sekolah: str
    nik: str
    nisn: str
    nama: str
    tingkat_pendidikan_id: int
    nama_rombel: str
    jenis_kelamin: str
    tempat_lahir: str
    tanggal_lahir: str
    agama_id: int
    agama_id_str: str
    alamat_jalan: str
    nipd: Optional[str] = field(
    default=None, metadata=config(exclude=lambda x: x is None)
    )
    email: Optional[str] = None
    nomor_telepon_rumah: Optional[str] = None
    nomor_telepon_seluler: Optional[str] = None
   
    def __str__(self):
        return self.nama
    
    def memberId(self):
        return self.nipd
    
    def toSlims(self):
        return {
            'member_id': self.nipd,
            'member_name': self.nama.title(),
            'gender': (0 if self.jenis_kelamin == "p" else 1),
            'member_type_id': os.getenv('SLIMS_MEMBERSHIP_STUDENT_ID'),
            'member_email': self.email,
            'member_address': self.alamat_jalan,
            'inst_name': self.nama_rombel,
            'pin': self.nipd,
            'member_phone': self.nomor_telepon_seluler,
            'member_fax': self.nomor_telepon_rumah,
            'member_since_date': self.tanggal_masuk_sekolah,
            'register_date': self.tanggal_masuk_sekolah,
            'expire_date': '2099-12-1', # Placeholder
            'birth_date': self.tanggal_lahir,
            'input_date': self.tanggal_masuk_sekolah,
            'last_update': self.tanggal_masuk_sekolah,
            'member_notes': '',
            'mpasswd': hashlib.md5(
                        str(self.nipd).encode('utf-8')
                ).hexdigest()
        }
    