class ProtocolConstants:
    CODES = {
        "login" : "LGN",
        "confirm register": "CRG",
        "register" : "RGS",
        "forgot" : "FRG",
        "send" : "SND",
        "recieve" : "RCV",
        "error" :  "ERR",
        "verify" : "VRF",
        "resend": "RSD",
        "reset": "RST",
        "verforgot": "VFR",
        "resendmail": "RSE"
    }

    ERRORS = [
        "username or password",
        "wrong email",
        "username taken",
        "email taken",
        "wrong code",
        "code expired",
        "user already valid"
    ]