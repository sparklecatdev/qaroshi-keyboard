#!/usr/bin/env python3
"""Generate Windows MSKLC native keyboard layout sources.

MSKLC ligatures output the four Qaroshi digraphs with one physical keypress.
The .klc files must be compiled into a Windows DLL and setup package using
Microsoft Keyboard Layout Creator on Windows; no unsigned DLL is claimed here.
"""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
SPEC=json.loads((ROOT/"mapping.json").read_text(encoding="utf-8"))
OUT=ROOT/"desktop/native/windows"
OUT.mkdir(parents=True, exist_ok=True)

SCAN=[
    ["10","11","12","13","14","15","16","17","18","19"],
    ["1e","1f","20","21","22","23","24","25","26","27"],
    ["2c","2d","2e","2f","30","31","32","33","34","35"]
]
VK={"COLON":"OEM_1","COMMA":"OEM_COMMA","PERIOD":"OEM_PERIOD","SLASH":"OEM_2"}
EXTRA=[
    ("02","1","1","!"),("03","2","2","@"),("04","3","3","#"),("05","4","4","$"),
    ("06","5","5","%"),("07","6","6","^"),("08","7","7","&"),("09","8","8","*"),
    ("0a","9","9","("),("0b","0","0",")"),
    ("0c","OEM_MINUS","-","_"),("0d","OEM_PLUS","=","+"),
    ("1a","OEM_4","[","{"),("1b","OEM_6","]","}"),
    ("28","OEM_7","'",'"'),("29","OEM_3","\x60","~"),("2b","OEM_5","\\","|"),
    ("39","SPACE"," "," "),("53","DECIMAL",".","."),
]

def val(value):
    return "%%" if len(value)>1 else f"{ord(value):04X}"

def klc(layout,rows):
    tag={"qwerty":"qrqwer1","azerty":"qrazrt1","dvorak":"qrdvor1"}[layout]
    lines=[
        f'KBD\t{tag}\t"Qaroshi {layout.upper()}"',
        'COPYRIGHT\t"Copyright (c) 2026 Qaroshi contributors"',
        'COMPANY\t"Qaroshi"',
        'LOCALENAME\t"en-US"',
        'LOCALEID\t"00000409"',
        'VERSION\t1.0',
        'SHIFTSTATE', '0\t// Unshifted','1\t// Shifted','2\t// Ctrl',
        'LAYOUT','//SC\tVK_\tCap\t0\t1\t2'
    ]
    ligatures=[]
    # Emit physical keys in scancode order.
    result={}
    for i,row in enumerate(rows):
        for j,normal in enumerate(row):
            key=SPEC["physicalRows"][i][j]
            low=SPEC["specialLetterReplacements"].get(normal,normal)
            high=SPEC["shiftPunctuation"].get(layout,{}).get(key,low[:1].upper()+low[1:])
            sc=SCAN[i][j]
            vkey=VK.get(key,key)
            caps="1" if normal.isalpha() else "0"
            result[sc]=(vkey,caps,low,high)
            for shift,v in [(0,low),(1,high)]:
                if len(v)>1:
                    ligatures.append(f'{vkey}\t{shift}\t'+'\t'.join(f'{ord(c):04X}' for c in v))
    for sc,vkey,low,high in EXTRA:
        result.setdefault(sc,(vkey,"0",low,high))
    for sc,(vkey,caps,low,high) in sorted(result.items(),key=lambda kv:int(kv[0],16)):
        lines.append(f"{sc}\t{vkey}\t{caps}\t{val(low)}\t{val(high)}\t-1")
    if ligatures:
        lines+=["","LIGATURE","//VK_\tMod#\tChar0\tChar1","//----\t----\t----\t----"]+ligatures
    lines += ["","KEYNAME","01\tEsc","0e\tBackspace","0f\tTab","1c\tEnter","1d\tCtrl","2a\tShift","36\tRight Shift","38\tAlt","39\tSpace","3a\tCaps Lock","","KEYNAME_EXT","1c\tNum Enter","1d\tRight Ctrl","35\tNum /","38\tRight Alt","47\tHome","48\tUp","49\tPage Up","4b\tLeft","4d\tRight","4f\tEnd","50\tDown","51\tPage Down","52\tInsert","53\tDelete","","DESCRIPTIONS",f'0409\tQaroshi {layout.upper()}',"","LANGUAGENAMES","0409\tEnglish (United States)","","ENDKBD"]
    return "\r\n".join(lines)+"\r\n"

for layout,rows in SPEC["layoutRows"].items():
    name=f"Qaroshi-{layout}.klc"
    (OUT/name).write_bytes(klc(layout,rows).encode("utf-16-le"))
    # UTF-16 BOM required by MSKLC.
    content=(OUT/name).read_bytes()
    (OUT/name).write_bytes(b"\xff\xfe"+content)
    print("Generated", OUT/name)
