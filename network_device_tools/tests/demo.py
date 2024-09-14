from textfsm import TextFSM
from netmiko import ConnectHandler
import pandas as pd
import os

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
000f-e207-f2e0   1          Learned          BAGG1                    Y
0000-0000-0001   104        Learned          BAGG1                    Y
c81f-ea81-12ff   104        Learned          GE1/0/26                 Y
0000-0000-0001   3506       Learned          BAGG1                    Y
0000-0000-0001   3511       Learned          BAGG1                    Y
000f-e50b-67c4   3511       Learned          GE1/0/28                 Y
0000-0000-0001   3512       Learned          BAGG1                    Y
0000-0000-0001   3517       Learned          BAGG1                    Y
0000-0000-0001   3519       Learned          BAGG1                    Y
0000-0000-0001   3521       Learned          BAGG1                    Y
22fa-974c-b781   4001       Learned          BAGG1                    Y
6ab8-6164-8127   4001       Learned          BAGG1                    Y
6ce5-f7d9-2601   4001       Learned          BAGG1                    Y
72e4-9ea0-c115   4001       Learned          BAGG1                    Y
7a42-0b67-6da5   4001       Learned          BAGG1                    Y
9e62-00e3-dee4   4001       Learned          BAGG1                    Y
a6b9-f097-5c33   4001       Learned          BAGG1                    Y
aa23-76b7-8caf   4001       Learned          BAGG1                    Y
aa4a-de39-26d6   4001       Learned          BAGG1                    Y
b2ed-f757-3520   4001       Learned          BAGG1                    Y
bea3-91b7-a0e2   4001       Learned          BAGG1                    Y
da81-22cb-f061   4001       Learned          BAGG1                    Y
e2d5-445c-0768   4001       Learned          BAGG1                    Y
f28b-1931-bf7c   4001       Learned          BAGG1                    Y
f639-2dc2-75fe   4001       Learned          BAGG1                    Y
0c60-766f-7f9b   4011       Learned          GE1/0/19                 Y
328e-d1f5-446c   4011       Learned          GE1/0/16                 Y
4c49-e31f-f37f   4011       Learned          GE1/0/20                 Y
66c3-b785-ffbf   4011       Learned          GE1/0/15                 Y
6ce5-f7d9-2601   4011       Learned          BAGG1                    Y
a611-5976-a2ae   4011       Learned          GE1/0/11                 Y
c215-031a-3a9a   4011       Learned          GE1/0/17                 Y
dc72-9bcd-61d3   4011       Learned          GE1/0/18                 Y
1ae0-bb84-fe34   4012       Learned          GE1/0/22                 Y
6ce5-f7d9-2601   4012       Learned          BAGG1                    Y
a46b-b63c-e22c   4012       Learned          GE1/0/14                 Y
0217-5990-7731   4013       Learned          GE1/0/18                 Y
6ce5-f7d9-2601   4013       Learned          BAGG1                    Y
387a-0ea6-ccaf   4014       Learned          GE1/0/22                 Y
6ce5-f7d9-2601   4014       Learned          BAGG1                    Y
821d-985e-2293   4014       Learned          GE1/0/13                 Y
a4b1-c1da-20be   4014       Learned          GE1/0/15                 Y
caeb-c3c0-ad5a   4014       Learned          GE1/0/17                 Y
f260-d66f-d966   4014       Learned          GE1/0/16                 Y
0aa1-70aa-a8b8   4015       Learned          GE1/0/11                 Y
1656-ac9f-ee32   4015       Learned          GE1/0/12                 Y
3e51-88b9-801f   4015       Learned          GE1/0/11                 Y
64d6-9ad0-1c6d   4015       Learned          GE1/0/3                  Y
6ce5-f7d9-2601   4015       Learned          BAGG1                    Y
7c6b-9c83-643d   4015       Learned          GE1/0/19                 Y
923b-a4bb-8bc3   4015       Learned          GE1/0/21                 Y
b24d-e170-44bf   4015       Learned          GE1/0/16                 Y
56d3-14b1-a1a6   4016       Learned          GE1/0/21                 Y
6ce5-f7d9-2601   4016       Learned          BAGG1                    Y
88d8-2e9e-5679   4016       Learned          GE1/0/19                 Y
0e3b-9e40-9ec5   4017       Learned          GE1/0/4                  Y
6ce5-f7d9-2601   4017       Learned          BAGG1                    Y
ac12-03fb-f455   4017       Learned          GE1/0/4                  Y
4613-b85e-c3eb   4018       Learned          GE1/0/12                 Y
6ce5-f7d9-2601   4018       Learned          BAGG1                    Y
c608-6a70-f3ff   4018       Learned          GE1/0/10                 Y
2a28-a01e-d5f6   4019       Learned          GE1/0/20                 Y
50de-061e-8fe8   4019       Learned          GE1/0/11                 Y
6ce5-f7d9-2601   4019       Learned          BAGG1                    Y
a051-0b90-4769   4019       Learned          GE1/0/3                  Y
ac92-3261-4119   4019       Learned          GE1/0/13                 Y
0000-0000-0001   4093       Learned          BAGG1                    Y
74d6-cb24-64e0   4093       Learned          GE1/0/16                 Y
74d6-cb24-65c0   4093       Learned          GE1/0/5                  Y
74d6-cb24-65e0   4093       Learned          GE1/0/8                  Y
74d6-cb24-6640   4093       Learned          GE1/0/15                 Y
74d6-cb24-6660   4093       Learned          GE1/0/18                 Y
74d6-cb24-6680   4093       Learned          GE1/0/19                 Y
74d6-cb24-66a0   4093       Learned          GE1/0/11                 Y
74d6-cb24-66c0   4093       Learned          GE1/0/7                  Y
74d6-cb24-6700   4093       Learned          GE1/0/3                  Y
74d6-cb24-6720   4093       Learned          GE1/0/17                 Y
74d6-cb2b-6280   4093       Learned          GE1/0/20                 Y
74d6-cb2b-6380   4093       Learned          GE1/0/1                  Y
74d6-cb2b-63a0   4093       Learned          GE1/0/2                  Y
74d6-cb2b-64c0   4093       Learned          GE1/0/22                 Y
74d6-cb2b-6620   4093       Learned          GE1/0/10                 Y
74d6-cb2b-6640   4093       Learned          GE1/0/12                 Y
74d6-cb2b-6760   4093       Learned          GE1/0/9                  Y
74d6-cb2b-6780   4093       Learned          GE1/0/4                  Y
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

current_script_dir = os.path.dirname(os.path.abspath(__file__))

mac_template = open(current_script_dir + r"\textfsm_templates\hp_comware_display_mac-address.textfsm")
fsm = TextFSM(mac_template)
result = fsm.ParseText(mac_address)

mac_data = convert_to_dict(fsm.header, result)

print(mac_data[:2])

# arp_template = open("hp_comware_display_arp.textfsm")
# fsm = TextFSM(arp_template)
# result = fsm.ParseText(arp)

# print(fsm.header)
# print(result[:2])
# 获取当前脚本文件的绝对路径
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', None)

int_template = open(current_script_dir + r"\textfsm_templates\hp_comware_display_interface_brief.textfsm")
fsm = TextFSM(int_template)
result = fsm.ParseText(inter)

finterface_data = convert_to_dict(fsm.header, result)

print(finterface_data[:2])

# 将数据转换为DataFrame
df1 = pd.DataFrame(mac_data)
df2 = pd.DataFrame(finterface_data)

# 合并数据，以INTERFACE为键，以df2为准
# merged_df = pd.merge(df1, df2, on='INTERFACE', how='left')

# 合并数据，以INTERFACE为键，保留所有接口
merged_df = pd.merge(df1, df2, on='INTERFACE', how='outer')

# 将 MAC_ADDRESS 列转换为列表
merged_df['MAC_ADDRESS'] = merged_df['MAC_ADDRESS'].apply(lambda x: [x])

# 按 INTERFACE 分组，并将 MAC_ADDRESS 列合并为列表
grouped_df = merged_df.groupby('INTERFACE').agg({
    'MAC_ADDRESS': 'sum',
    'VLAN_ID': 'first',
    'STATE': 'first',
    'AGING': 'first',
    'LINK': 'first',
    'SPEED': 'first',
    'DUPLEX': 'first',
    'Type': 'first',
    'PVID': 'first'
}).reset_index()

# # 打印分组后的数据
# print(grouped_df)

# 保存为 Excel 文件
output_file = 'output_table.xlsx'
grouped_df.to_excel(output_file, index=True)

print(f"表格已保存为 {output_file}")


# 将字典列表转换为DataFrame
# df = pd.DataFrame(formatted_data)

# 将DataFrame写入Excel文件
# df.to_excel('output.xlsx', index=False)