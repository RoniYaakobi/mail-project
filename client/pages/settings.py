from client.pages.page import Page, PageType

from protocol.protocol_constants import ProtocolConstants

class LoginPage(Page):
    PAGE_ID = PageType.assign_id("settings")
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.set_title("Settings")

        self.cipher_type = self.add_radio_choice(text="RSA",
                                                  value=ProtocolConstants.EncryptionType.RSA.value)
        
        self.cipher_type = self.add_radio_choice(text="Diffie Hellman",
                                                  value=ProtocolConstants.EncryptionType.DH.value,
                                                  variable=self.cipher_type)

        self.create_action_button("Connect", self.login_action, pack_pady=5)

    def connect_action(self):
        cipher_type = ProtocolConstants.EncryptionType(self.cipher_type)
        
        
        
