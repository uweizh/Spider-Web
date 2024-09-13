from textfsm import TextFSM
from netmiko import ConnectHandler
import pandas as pd

# 将 header 和 data 转换成字典列表
def convert_to_dict(header, data):
    result = []
    for row in data:
        row_dict = {}
        for i, value in enumerate(row):
            row_dict[header[i]] = value
        result.append(row_dict)
    return result

mac_address = """
<ASW1-D1-900C-TMH-UBRMB>display  mac-address
MAC Address      VLAN ID    State            Port/Nickname            Aging
3e51-88b9-801f   4015       Learned          GE1/0/11                 Y
64d6-9ad0-1c6d   4015       Learned          GE1/0/3                  Y
74d6-cb2b-67c0   4093       Learned          GE1/0/13                 Y
74d6-cb2b-6840   4093       Learned          GE1/0/21                 Y
74d6-cb2b-68e0   4093       Learned          GE1/0/6                  Y
74d6-cb2b-6900   4093       Learned          GE1/0/14                 Y
6ce5-f7d9-2601   4094       Learned          BAGG1                    Y
000f-e50b-5c07   3511       Learned          GE5/0/9                  Y
000f-e50b-5c0a   3511       Learned          GE5/0/10                 Y
000f-e50b-5c0b   3511       Learned          GE5/0/8                  Y
"""
arp = """
<DSW4-803/909-TP-UBRMB>display  arp
  Type: S-Static   D-Dynamic   O-Openflow   R-Rule   M-Multiport  I-Invalid
IP address      MAC address    VLAN/VSI name Interface                Aging Type
10.95.8.31      6893-20e1-51cf vxlan4094     BAGG55                   894   D
10.95.8.36      00be-d5a2-f6e0 vxlan4094     BAGG53                   973   D
10.95.8.38      6893-20e1-53af vxlan4094     BAGG51                   622   D
10.95.8.49      1451-7ece-a0a1 vxlan4094     BAGG47                   673   D
10.95.8.63      fc60-9bc2-5d1e vxlan4094     BAGG54                   989   D
10.95.8.192     743a-204a-eb24 vxlan4094     BAGG1                    225   D
10.95.8.193     703a-a65c-af66 vxlan4094     BAGG2                    1200  D
10.95.8.194     743a-204a-d3fc vxlan4094     BAGG3                    727   D
10.95.8.195     743a-204a-acfc vxlan4094     BAGG8                    301   D
10.95.8.196     6c87-20a6-070a vxlan4094     BAGG20                   104   D
10.95.8.197     743a-204b-3ac4 vxlan4094     BAGG6                    1115  D
"""

inter = """
<ASW1-D1-900C-TMH-UBRMB>display  interface Bridge-Aggregation
<ASW1-D1-900C-TMH-UBRMB>display  interface brief
Brief information on interfaces in route mode:
Link: ADM - administratively down; Stby - standby
Protocol: (s) - spoofing
Interface            Link Protocol Primary IP      Description
InLoop0              UP   UP(s)    --
MGE0/0/0             DOWN DOWN     --
NULL0                UP   UP(s)    --
REG0                 UP   --       --
Vlan99               UP   UP       192.168.100.5
Vlan4094             UP   UP       10.112.22.40

Brief information on interfaces in bridge mode:
Link: ADM - administratively down; Stby - standby
Speed: (a) - auto
Duplex: (a)/A - auto; H - half; F - full
Type: A - access; T - trunk; H - hybrid
Interface            Link Speed   Duplex Type PVID Description
BAGG1                UP   20G(a)  F(a)   T    1
GE1/0/1              UP   1G(a)   F(a)   T    4093
GE1/0/2              UP   1G(a)   F(a)   T    4093
GE1/0/3              UP   1G(a)   F(a)   T    4093
GE1/0/4              UP   1G(a)   F(a)   T    4093
GE1/0/5              UP   1G(a)   F(a)   T    4093
GE1/0/6              UP   1G(a)   F(a)   T    4093
GE1/0/7              UP   1G(a)   F(a)   T    4093
GE1/0/8              UP   1G(a)   F(a)   T    4093
GE1/0/9              UP   1G(a)   F(a)   T    4093
GE1/0/10             UP   1G(a)   F(a)   T    4093
GE1/0/11             UP   1G(a)   F(a)   T    4093
GE1/0/12             UP   1G(a)   F(a)   T    4093
GE1/0/13             UP   1G(a)   F(a)   T    4093
GE1/0/14             UP   1G(a)   F(a)   T    4093
GE1/0/15             UP   1G(a)   F(a)   T    4093
GE1/0/16             UP   1G(a)   F(a)   T    4093
GE1/0/17             UP   1G(a)   F(a)   T    4093
GE1/0/18             UP   1G(a)   F(a)   T    4093
GE1/0/19             UP   1G(a)   F(a)   T    4093
GE1/0/20             UP   1G(a)   F(a)   T    4093
GE1/0/21             UP   1G(a)   F(a)   T    4093
GE1/0/22             UP   1G(a)   F(a)   T    4093
GE1/0/23             DOWN auto    A      A    101
GE1/0/24             DOWN auto    A      A    102
GE1/0/25             DOWN auto    A      A    103
GE1/0/26             UP   100M(a) F(a)   A    104
GE1/0/27             DOWN auto    A      T    3511
GE1/0/28             UP   100M(a) F(a)   T    3511
GE1/0/29             DOWN auto    A      A    105
GE1/0/30             DOWN auto    A      A    106
GE1/0/31             DOWN auto    A      A    107
GE1/0/32             DOWN auto    A      A    108
GE1/0/33             DOWN auto    A      A    109
GE1/0/34             DOWN auto    A      A    110
GE1/0/35             DOWN auto    A      A    111
GE1/0/36             DOWN auto    A      A    112
GE1/0/37             DOWN auto    A      A    113
GE1/0/38             DOWN auto    A      A    114
GE1/0/39             DOWN auto    A      A    115
GE1/0/40             DOWN auto    A      A    116
GE1/0/41             DOWN auto    A      A    117
GE1/0/42             DOWN auto    A      A    118
GE1/0/43             DOWN auto    A      A    119
GE1/0/44             DOWN auto    A      A    120
GE1/0/45             DOWN auto    A      A    121
GE1/0/46             DOWN auto    A      A    122
GE1/0/47             DOWN auto    A      A    123
GE1/0/48             UP   1G(a)   F(a)   T    1
GE5/0/1              DOWN auto    A      A    125
GE5/0/2              DOWN auto    A      A    126
GE5/0/3              DOWN auto    A      A    127
GE5/0/4              DOWN auto    A      A    128
GE5/0/5              DOWN auto    A      A    129
GE5/0/6              DOWN auto    A      A    130
GE5/0/7              DOWN auto    A      A    131
GE5/0/8              UP   100M(a) F(a)   T    3511
GE5/0/9              UP   100M(a) F(a)   T    3511
GE5/0/10             UP   100M(a) F(a)   T    3511
GE5/0/11             DOWN auto    A      A    132
GE5/0/12             DOWN auto    A      A    133
GE5/0/13             DOWN auto    A      A    134
GE5/0/14             DOWN auto    A      A    135
GE5/0/15             DOWN auto    A      A    136
GE5/0/16             DOWN auto    A      A    137
GE5/0/17             DOWN auto    A      A    138
GE5/0/18             DOWN auto    A      A    139
GE5/0/19             DOWN auto    A      A    140
GE5/0/20             DOWN auto    A      A    141
GE5/0/21             DOWN auto    A      A    142
GE5/0/22             DOWN auto    A      A    143
GE5/0/23             DOWN auto    A      A    144
GE5/0/24             DOWN auto    A      A    145
GE5/0/25             DOWN auto    A      A    146
GE5/0/26             DOWN auto    A      A    147
GE5/0/27             DOWN auto    A      A    148
GE5/0/28             DOWN auto    A      A    149
GE5/0/29             DOWN auto    A      A    150
GE5/0/30             DOWN auto    A      A    151
GE5/0/31             DOWN auto    A      A    152
GE5/0/32             DOWN auto    A      A    153
GE5/0/33             DOWN auto    A      A    154
GE5/0/34             DOWN auto    A      A    155
GE5/0/35             DOWN auto    A      A    156
GE5/0/36             DOWN auto    A      A    157
GE5/0/37             DOWN auto    A      A    158
GE5/0/38             DOWN auto    A      A    159
GE5/0/39             DOWN auto    A      A    160
GE5/0/40             DOWN auto    A      A    161
GE5/0/41             DOWN auto    A      A    162
GE5/0/42             DOWN auto    A      A    163
GE5/0/43             DOWN auto    A      A    164
GE5/0/44             DOWN auto    A      A    165
GE5/0/45             DOWN auto    A      A    166
GE5/0/46             DOWN auto    A      A    167
GE5/0/47             DOWN auto    A      A    168
GE5/0/48             UP   1G(a)   F(a)   T    1
XGE1/0/49            DOWN auto    A      A    124
XGE1/0/50            UP   10G(a)  F(a)   T    1
XGE1/0/51            UP   10G(a)  F(a)   --   --
XGE1/0/52            UP   10G(a)  F(a)   --   --
XGE5/0/49            DOWN auto    A      A    169
XGE5/0/50            UP   10G(a)  F(a)   T    1
XGE5/0/51            UP   10G(a)  F(a)   --   --
XGE5/0/52            UP   10G(a)  F(a)   --   --
"""

# mac_template = open("hp_comware_display_mac-address.textfsm")
# fsm = TextFSM(mac_template)
# result = fsm.ParseText(mac_address)

# print(fsm.header)
# print(result[:2])

# arp_template = open("hp_comware_display_arp.textfsm")
# fsm = TextFSM(arp_template)
# result = fsm.ParseText(arp)

# print(fsm.header)
# print(result[:2])

int_template = open("hp_comware_display_interface_brief.textfsm")
fsm = TextFSM(int_template)
result = fsm.ParseText(inter)

formatted_data = convert_to_dict(fsm.header, result)

print(formatted_data[:2])


# 将字典列表转换为DataFrame
df = pd.DataFrame(formatted_data)

# 将DataFrame写入Excel文件
df.to_excel('output.xlsx', index=False)