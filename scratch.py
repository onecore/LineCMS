x = """
MONEY_CURRENCY_AED = "AED"
MONEY_CURRENCY_AFN = "AFN"
MONEY_CURRENCY_ALL = "ALL"
MONEY_CURRENCY_AMD = "AMD"
MONEY_CURRENCY_ANG = "ANG"
MONEY_CURRENCY_AOA = "AOA"
MONEY_CURRENCY_ARS = "ARS"
MONEY_CURRENCY_AUD = "AUD"
MONEY_CURRENCY_AWG = "AWG"
MONEY_CURRENCY_AZN = "AZN"
MONEY_CURRENCY_BAM = "BAM"
MONEY_CURRENCY_BBD = "BBD"
MONEY_CURRENCY_BDT = "BDT"
MONEY_CURRENCY_BGN = "BGN"
MONEY_CURRENCY_BHD = "BHD"
MONEY_CURRENCY_BND = "BND"
MONEY_CURRENCY_BOB = "BOB"
MONEY_CURRENCY_BRL = "BRL"
MONEY_CURRENCY_BSD = "BSD"
MONEY_CURRENCY_BTN = "BTN"
MONEY_CURRENCY_BWP = "BWP"
MONEY_CURRENCY_BYR = "BYR"
MONEY_CURRENCY_BZD = "BZD"
MONEY_CURRENCY_CAD = "CAD"
MONEY_CURRENCY_CHF = "CHF"
MONEY_CURRENCY_CLP = "CLP"
MONEY_CURRENCY_CNY = "CNY"
MONEY_CURRENCY_COP = "COP"
MONEY_CURRENCY_CRC = "CRC"
MONEY_CURRENCY_CZK = "CZK"
MONEY_CURRENCY_DKK = "DKK"
MONEY_CURRENCY_DOP = "DOP"
MONEY_CURRENCY_DZD = "DZD"
MONEY_CURRENCY_EGP = "EGP"
MONEY_CURRENCY_ETB = "ETB"
MONEY_CURRENCY_EUR = "EUR"
MONEY_CURRENCY_FJD = "FJD"
MONEY_CURRENCY_GBP = "GBP"
MONEY_CURRENCY_GEL = "GEL"
MONEY_CURRENCY_GHS = "GHS"
MONEY_CURRENCY_GMD = "GMD"
MONEY_CURRENCY_GTQ = "GTQ"
MONEY_CURRENCY_GYD = "GYD"
MONEY_CURRENCY_HKD = "HKD"
MONEY_CURRENCY_HNL = "HNL"
MONEY_CURRENCY_HRK = "HRK"
MONEY_CURRENCY_HUF = "HUF"
MONEY_CURRENCY_IDR = "IDR"
MONEY_CURRENCY_ILS = "ILS"
MONEY_CURRENCY_INR = "INR"
MONEY_CURRENCY_ISK = "ISK"
MONEY_CURRENCY_JEP = "JEP"
MONEY_CURRENCY_JMD = "JMD"
MONEY_CURRENCY_JOD = "JOD"
MONEY_CURRENCY_JPY = "JPY"
MONEY_CURRENCY_KES = "KES"
MONEY_CURRENCY_KGS = "KGS"
MONEY_CURRENCY_KHR = "KHR"
MONEY_CURRENCY_KRW = "KRW"
MONEY_CURRENCY_KWD = "KWD"
MONEY_CURRENCY_KYD = "KYD"
MONEY_CURRENCY_KZT = "KZT"
MONEY_CURRENCY_LBP = "LBP"
MONEY_CURRENCY_LKR = "LKR"
MONEY_CURRENCY_LTL = "LTL"
MONEY_CURRENCY_LVL = "LVL"
MONEY_CURRENCY_MAD = "MAD"
MONEY_CURRENCY_MDL = "MDL"
MONEY_CURRENCY_MGA = "MGA"
MONEY_CURRENCY_MKD = "MKD"
MONEY_CURRENCY_MMK = "MMK"
MONEY_CURRENCY_MNT = "MNT"
MONEY_CURRENCY_MOP = "MOP"
MONEY_CURRENCY_MUR = "MUR"
MONEY_CURRENCY_MVR = "MVR"
MONEY_CURRENCY_MXN = "MXN"
MONEY_CURRENCY_MYR = "MYR"
MONEY_CURRENCY_MZN = "MZN"
MONEY_CURRENCY_NAD = "NAD"
MONEY_CURRENCY_NGN = "NGN"
MONEY_CURRENCY_NIO = "NIO"
MONEY_CURRENCY_NOK = "NOK"
MONEY_CURRENCY_NPR = "NPR"
MONEY_CURRENCY_NZD = "NZD"
MONEY_CURRENCY_OMR = "OMR"
MONEY_CURRENCY_PEN = "PEN"
MONEY_CURRENCY_PGK = "PGK"
MONEY_CURRENCY_PHP = "PHP"
MONEY_CURRENCY_PKR = "PKR"
MONEY_CURRENCY_PLN = "PLN"
MONEY_CURRENCY_PYG = "PYG"
MONEY_CURRENCY_QAR = "QAR"
MONEY_CURRENCY_RON = "RON"
MONEY_CURRENCY_RSD = "RSD"
MONEY_CURRENCY_RUB = "RUB"
MONEY_CURRENCY_RWF = "RWF"
MONEY_CURRENCY_SAR = "SAR"
MONEY_CURRENCY_SCR = "SCR"
MONEY_CURRENCY_SEK = "SEK"
MONEY_CURRENCY_SGD = "SGD"
MONEY_CURRENCY_STD = "STD"
MONEY_CURRENCY_SYP = "SYP"
MONEY_CURRENCY_THB = "THB"
MONEY_CURRENCY_TND = "TND"
MONEY_CURRENCY_TRY = "TRY"
MONEY_CURRENCY_TTD = "TTD"
MONEY_CURRENCY_TWD = "TWD"
MONEY_CURRENCY_TZS = "TZS"
MONEY_CURRENCY_UAH = "UAH"
MONEY_CURRENCY_UGX = "UGX"
MONEY_CURRENCY_USD = "USD"
MONEY_CURRENCY_UYU = "UYU"
MONEY_CURRENCY_VEF = "VEF"
MONEY_CURRENCY_VND = "VND"
MONEY_CURRENCY_VUV = "VUV"
MONEY_CURRENCY_WST = "WST"
MONEY_CURRENCY_XAF = "XAF"
MONEY_CURRENCY_XBT = "XBT"
MONEY_CURRENCY_XCD = "XCD"
MONEY_CURRENCY_XOF = "XOF"
MONEY_CURRENCY_XPF = "XPF"
MONEY_CURRENCY_ZAR = "ZAR"
MONEY_CURRENCY_ZMW = "ZMW"

"""

y = x.split("\n")
o = []
ii = []
for i in y:
    if i:
        ii.append(i.split(" ")[2].replace("\"", ""))

print(ii)
