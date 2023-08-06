import logging

from stellar_sdk import Keypair

from lumensigner.controller import Controller
from lumensigner.gui.components import (
    FontAwesomeIconConstants,
    SeedSignerCustomIconConstants,
)
from lumensigner.gui.screens.request_address_screens import (
    RequestAddressShareAddressScreen,
)
from lumensigner.gui.screens.screen import (
    RET_CODE__BACK_BUTTON,
    ButtonListScreen,
    QRDisplayScreen,
)
from .view import BackStackView, View, Destination, MainMenuView
from ..models import EncodeQR, QRType, Seed

logger = logging.getLogger(__name__)


class RequestAddressSelectSeedView(View):
    def run(self, **kwargs):
        seeds = self.controller.storage.seeds
        SCAN_SEED = ("Scan a seed", FontAwesomeIconConstants.QRCODE)
        TYPE_12WORD = ("Enter 12-word seed", FontAwesomeIconConstants.KEYBOARD)
        TYPE_24WORD = ("Enter 24-word seed", FontAwesomeIconConstants.KEYBOARD)
        button_data = [
            (seed.get_fingerprint(), SeedSignerCustomIconConstants.FINGERPRINT, "blue")
            for seed in seeds
        ]
        button_data += [SCAN_SEED, TYPE_12WORD, TYPE_24WORD]

        selected_menu_num = ButtonListScreen(
            title="Select Signer",
            is_button_text_centered=False,
            button_data=button_data,
        ).display()

        if selected_menu_num == RET_CODE__BACK_BUTTON:
            return Destination(BackStackView)

        if len(seeds) > 0 and selected_menu_num < len(seeds):
            # User selected one of the n seeds
            seed = self.controller.get_seed(selected_menu_num)
            address_index = self.controller.request_address_data
            return Destination(
                RequestAddressShareAddressView,
                view_args=dict(seed=seed, address_index=address_index),
            )

        self.controller.resume_main_flow = Controller.FLOW__REQUEST_ADDRESS

        if button_data[selected_menu_num] == SCAN_SEED:
            from lumensigner.views.scan_views import ScanView

            return Destination(ScanView)

        elif button_data[selected_menu_num] in [TYPE_12WORD, TYPE_24WORD]:
            from lumensigner.views.seed_views import SeedMnemonicEntryView

            if button_data[selected_menu_num] == TYPE_12WORD:
                self.controller.storage.init_pending_mnemonic(num_words=12)
            else:
                self.controller.storage.init_pending_mnemonic(num_words=24)
            return Destination(SeedMnemonicEntryView)


class RequestAddressShareAddressView(View):
    def __init__(self, seed: Seed, address_index: int):
        super().__init__()
        self.address_index = address_index
        kp = Keypair.from_mnemonic_phrase(
            mnemonic_phrase=seed.mnemonic_str,
            passphrase=seed.passphrase,
            index=self.address_index,
        )
        self.public_key = kp.public_key

    def run(self, **kwargs):
        SHARE_ADDRESS = "Share Address"
        ABORT = "Abort"
        button_data = [SHARE_ADDRESS, ABORT]
        selected_menu_num = RequestAddressShareAddressScreen(
            address=self.public_key,
            derivation_index_id=self.address_index,
            button_data=button_data,
            show_back_button=False,
        ).display()

        print("selected_menu_num: ", selected_menu_num)

        if selected_menu_num == 0:
            qr_encoder = EncodeQR(
                qr_type=QRType.STELLAR_ADDRESS,
                stellar_address=self.public_key,
                derivation=f"m/44'/148'/{self.address_index}'",
            )
            QRDisplayScreen(
                qr_encoder=qr_encoder,
            ).display()

            return Destination(MainMenuView)

        elif selected_menu_num == 1:
            return Destination(MainMenuView)
