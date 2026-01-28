"""Client for EveryAyah.com audio URLs."""

from typing import Dict, List

from quran_unified.exceptions import InvalidReferenceError


class EveryAyahClient:
    """Constructs audio URLs for EveryAyah.com. No HTTP requests needed."""

    BASE_URL = "https://everyayah.com/data"

    RECITERS: Dict[str, str] = {
        "alafasy": "Alafasy_128kbps",
        "husary": "Husary_128kbps",
        "husary_mujawwad": "Husary_Mujawwad_128kbps",
        "husary_muallim": "Husary_Muallim_128kbps",
        "minshawi": "Minshawy_Murattal_128kbps",
        "minshawi_mujawwad": "Minshawy_Mujawwad_192kbps",
        "sudais": "Abdurrahmaan_As-Sudais_192kbps",
        "abdulbasit": "Abdul_Basit_Murattal_192kbps",
        "abdulbasit_mujawwad": "Abdul_Basit_Mujawwad_128kbps",
        "ghamdi": "Ghamadi_40kbps",
        "ajamy": "Ahmed_ibn_Ali_al-Ajamy_128kbps_ketaballah.net",
        "muaiqly": "Maher_AlMuawordy_128kbps",
        "shuraym": "Saood_ash-Shuraym_128kbps",
        "basfar": "Abdullah_Basfar_192kbps",
        "shaatree": "Abu_Bakr_Ash-Shaatree_128kbps",
        "ayyoub": "Hani_Rifai_192kbps",
        "tablaway": "Mohammad_al_Tablaway_128kbps",
        "jibreel": "Muhsin_Al_Qasim_192kbps",
        "khalil": "Khalil_Al_Husary_128kbps",
        "hudhaify": "Hudhaify_128kbps",
        "saad_alghamdi": "Saad_Al_Ghamdi_128kbps",
        "ali_jaber": "Ali_Jaber_64kbps",
        "fares_abbad": "Fares_Abbad_64kbps",
        "abdulsamad": "AbdulSamad_64kbps_QuranExplorer.Com",
        "nasser_alqatami": "Nasser_Alqatami_128kbps",
        "yasser_aldosari": "Yasser_Ad-Dussary_128kbps",
        "maher_al_muaiqly": "MauroAudio_128kbps",
        "ahmed_alajmy": "Ahmed_Al-Ajmy_128kbps",
        "khalefa_taniji": "Khalefa_Al-Tunaiji_64kbps",
        "mahmoud_ali_albanna": "Mahmoud_Ali_Al_Banna_128kbps",
        "salah_budair": "Salah_Al_Budair_128kbps",
        "abdullah_matroud": "Abdullah_Matroud_128kbps",
        "ahmed_neana": "Ahmed_Neana_128kbps",
        "muhammad_ayyoub": "Muhammad_Ayyoub_128kbps",
        "muhammad_jibreel": "Muhammad_Jibreel_128kbps",
        "sahl_yasin": "Sahl_Yassin_128kbps",
        "yaser_salamah": "Yaser_Salamah_128kbps",
        "mishary_alafasy": "Alafasy_128kbps",
        "ibrahim_akhdar": "Ibrahim_Akhdar_32kbps",
        "mostafa_ismail": "Mostafa_Ismail_128kbps",
        "warsh_khalil": "Warsh/Khalil_Al_Husary_128kbps",
        "parhizgar": "Parhizgar_48kbps",
        "ayman_sowaid": "Ayman_Sowaid_64kbps",
        "ali_hajjaj_souasi": "Ali_Hajjaj_AlSouasi_128kbps",
    }

    def get_audio_url(self, surah: int, ayah: int, reciter: str = "alafasy") -> str:
        """Get the audio URL for a specific verse."""
        reciter_path = self._get_reciter_path(reciter)
        return f"{self.BASE_URL}/{reciter_path}/{surah:03d}{ayah:03d}.mp3"

    def get_surah_audio_urls(
        self, surah: int, total_ayahs: int, reciter: str = "alafasy"
    ) -> List[str]:
        """Get audio URLs for all verses in a surah."""
        return [
            self.get_audio_url(surah, ayah, reciter)
            for ayah in range(1, total_ayahs + 1)
        ]

    def get_available_reciters(self) -> List[str]:
        """Return list of available reciter identifiers."""
        return list(self.RECITERS.keys())

    def _get_reciter_path(self, reciter: str) -> str:
        """Resolve reciter identifier to the EveryAyah directory name."""
        if reciter not in self.RECITERS:
            raise InvalidReferenceError(
                f"Unknown reciter '{reciter}'. "
                f"Available: {', '.join(sorted(self.RECITERS.keys()))}"
            )
        return self.RECITERS[reciter]
