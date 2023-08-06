import unicodedata
from typing import List

from embit import bip39
from stellar_sdk import Keypair

from lumensigner.models.settings import SettingsConstants


class InvalidSeedException(Exception):
    pass


class Seed:
    def __init__(
        self,
        mnemonic: List[str] = None,
        passphrase: str = "",
        wordlist_language_code: str = SettingsConstants.WORDLIST_LANGUAGE__ENGLISH,
    ) -> None:
        self.wordlist_language_code = wordlist_language_code

        if not mnemonic:
            raise Exception("Must initialize a Seed with a mnemonic List[str]")
        self._mnemonic: List[str] = unicodedata.normalize(
            "NFKD", " ".join(mnemonic).strip()
        ).split()

        self._passphrase: str = ""
        self.set_passphrase(passphrase, regenerate_seed=False)

        self.seed_bytes: bytes = None
        self._generate_seed()

    @staticmethod
    def get_wordlist(
        wordlist_language_code: str = SettingsConstants.WORDLIST_LANGUAGE__ENGLISH,
    ) -> List[str]:
        # TODO: Support other BIP-39 wordlist languages!
        if wordlist_language_code == SettingsConstants.WORDLIST_LANGUAGE__ENGLISH:
            return bip39.WORDLIST
        else:
            raise Exception(
                f"Unrecognized wordlist_language_code {wordlist_language_code}"
            )

    def _generate_seed(self) -> bool:
        try:
            self.seed_bytes = bip39.mnemonic_to_seed(
                self.mnemonic_str, password=self._passphrase, wordlist=self.wordlist
            )
        except Exception as e:
            print(repr(e))
            raise InvalidSeedException(repr(e))

    @property
    def mnemonic_str(self) -> str:
        return " ".join(self._mnemonic)

    @property
    def mnemonic_list(self) -> List[str]:
        return self._mnemonic

    @property
    def mnemonic_display_str(self) -> str:
        return unicodedata.normalize("NFC", " ".join(self._mnemonic))

    @property
    def mnemonic_display_list(self) -> List[str]:
        return unicodedata.normalize("NFC", " ".join(self._mnemonic)).split()

    @property
    def passphrase(self):
        return self._passphrase

    @property
    def passphrase_display(self):
        return unicodedata.normalize("NFC", self._passphrase)

    def set_passphrase(self, passphrase: str, regenerate_seed: bool = True):
        if passphrase:
            self._passphrase = unicodedata.normalize("NFKD", passphrase)
        else:
            # Passphrase must always have a string value, even if it's just the empty
            # string.
            self._passphrase = ""

        if regenerate_seed:
            # Regenerate the internal seed since passphrase changes the result
            self._generate_seed()

    @property
    def wordlist(self) -> List[str]:
        return Seed.get_wordlist(self.wordlist_language_code)

    def set_wordlist_language_code(self, language_code: str):
        # TODO: Support other BIP-39 wordlist languages!
        raise Exception("Not yet implemented!")

    def get_fingerprint(self) -> str:
        kp = Keypair.from_mnemonic_phrase(
            self.mnemonic_str, passphrase=self.passphrase, index=0
        )
        return kp.raw_secret_key().hex()[-8:]

    ### override operators
    def __eq__(self, other):
        if isinstance(other, Seed):
            return self.seed_bytes == other.seed_bytes
        return False
