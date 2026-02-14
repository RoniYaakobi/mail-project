class ProtocolConstants:
    CODES = {
        "login" : "LGN",
        "register" : "RGS",
        "forgot" : "FRG",
        "send" : "SND",
        "receive" : "RCV",
        "error" :  "ERR"
    }

    ERRORS = {
        "general" : 0,
        "register" : 1,
        "login" : 2,
        "email" : 3,
        "send" : 4,
        "recv" : 5
    }