x = """
AT Austria
BE Belgium
BR Brazil
BG Bulgaria
CA Canada
HR Croatia
CY Cyprus
CZ CzechRepublic
DK Denmark
EE Estonia
FI Finland
FR France
DE Germany
GI Gibraltar
GR Greece
HK HongKong
HU Hungary
IN India
ID Indonesia
IE Ireland
IT Italy
JP Japan
LV Latvia
LI Liechtenstein
LT Lithuania
LU Luxembourg
MY Malaysia
MT Malta
MX Mexico
NL Netherlands
NZ NewZealand
NO Norway
PL Poland
PT Portugal
RO Romania
SG Singapore
SK Slovakia
SI Slovenia
ES Spain
SE Sweden
CH Switzerland
TH Thailand
AE UnitedArabEmirates
GB UnitedKingdom
US UnitedStates
"""

i = x.split("\n")

l = {}
for o in i:
    aa = o.split()
    try:
        l[aa[0]] = aa[1]
    except: pass

print(l)
