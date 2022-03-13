from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, Undefined, config
from typing import Optional, TYPE_CHECKING
from uuid import UUID
import os
import hashlib

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Gtk:
    tahun_ajaran_id: str
    ptk_terdaftar_id: UUID
    ptk_id: UUID
    ptk_induk: str
    tanggal_surat_tugas: str
    nama: str
    jenis_kelamin: str
    tempat_lahir: str
    tanggal_lahir: str
    agama_id: int
    agama_id_str: str
    nuptk: Optional[str]
    nik: str

    def __str__(self):
        return self.nama

    def memberId(self):
        return self.nik
        
    def toSlims(self):
        return {
            'member_id': self.nik,
            'member_name': self.nama.title(),
            'gender': (0 if self.jenis_kelamin == "P" else 1),
            'member_type_id': os.getenv('SLIMS_MEMBERSHIP_TEACHER_ID'),
            'member_email': '',
            'member_address': '',
            'postal_code': '',
            'inst_name': 'GURU',
            'pin': self.nik,
            'member_phone': '',
            'member_fax': '',
            'member_since_date': self.tanggal_surat_tugas,
            'member_image': '',
            'register_date': self.tanggal_surat_tugas,
            'expire_date': '2099-12-1',  # Placeholder
            'birth_date': self.tanggal_lahir,
            'input_date': self.tanggal_surat_tugas,
            'last_update': self.tanggal_surat_tugas,
            'member_notes': '',
            'mpasswd': hashlib.md5(
                        str(self.nik).encode('utf-8')
                ).hexdigest()
       }
   