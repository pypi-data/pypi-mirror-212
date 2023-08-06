import os
import re
import numpy as np
import pandas as pd
import xlrd
import openpyxl
from .e import e2int
from typing import Union

if xlrd.__version__ < "2.0.0":
    xlrd.xlsx.ensure_elementtree_imported(False, None)
    xlrd.xlsx.Element_has_iter = True


autoREG = """
e 8000lc29  > bb.txt
e 8900laa   > modem.txt
e 8a00la4   > rf.txt
e 8b00l1c   > codec.txt

e 8336l16   > lpm.txt

e 801c 0
e 83a1l4    > "LDO Control.txt"

e 801c 1
e 8380l4    > "CHARGER CTRL.txt"

e 801c 2
e 8380l4    > "XO32K CONTROL.txt"

e 801c 4
e 8380l4    > CHARGER_WAKE_CTRL.txt

e 81f2 1
e 8389l4    > TS_ANA_CTRL.txt
e 81f2 0
e 81f2 2
e 8389l4    > TS_FIR_CTRL.txt
e 81f2 0
e 81f2 4
e 8389l4    > TS_CAL_CTRL1.txt
e 81f2 0
e 81f2 8
e 8389l4    > TS_CAL_CTRL2.txt
e 81f2 0
e 81f2 10
e 8389l4    > TS_CAL_CTRL3.txt
e 81f2 0
e 81f2 20
e 8389l4    > TS_CAL_CTRL4.txt
e 81f2 0
e 81f2 40
e 8389l4    > TS_CMP_CTRL1.txt
e 81f2 0
e 81f2 80
e 8389l4    > TS_CMP_CTRL2.txt
e 81f2 0

e 81f3 1
e 8389l4    > TS_CAL_CFG.txt
e 81f3 0
e 81f3 2
e 8389l4    > TS_BL_CTRL1.txt
e 81f3 0
e 81f3 4
e 8389l4    > TS_BL_CTRL2.txt
e 81f3 0
e 81f3 8
e 8389l4    > TS_BL_CTRL3.txt
e 81f3 0
e 81f3 10
e 8389l4    > TS_BL_CTRL4.txt
e 81f3 0
"""
addr_name = "addr"
reg_name = "name"
width_name = "width"
domain_name = "domain"
access_name = "access"
init_name = "init"
description_name = "description"

__workbook_type = Union[xlrd.book.Book,openpyxl.workbook.workbook.Workbook]

def read_excel(wb:__workbook_type, sheet_name:str) -> pd.DataFrame:
    """read excel from workbook(xlrd/openpyxl), and fill merged cells"""
    if isinstance(wb, xlrd.book.Book):
        table = pd.read_excel(wb,sheet_name=sheet_name,dtype="string")
        for rl, rh, cl, ch in wb.sheet_by_name(sheet_name).merged_cells:
            table.iloc[rl-1:rh-1, cl:ch] = table.iloc[rl-1,cl]
    elif isinstance(wb, openpyxl.workbook.workbook.Workbook):
        table = pd.DataFrame(wb[sheet_name].values,dtype="string")
        col = table.iloc[0].copy()
        col[col.isna()] = "NAN" # otherwise table will use `pandas._libs.missing.NAType` as column name, which is undesirable
        table.columns = col
        table = table[1:]
        for r in wb[sheet_name].merged_cells.ranges:
            rl, rh, cl, ch = r.bounds
            table.iloc[rh-2:ch-1,rl-1:cl] = table.iloc[rh-2,rl-1]
    return table

def keep_rename_columns(table:pd.DataFrame) -> None:
    """only keep columns in `names`, and rename them to dict keys"""
    names = {
        "write addr":["Write Address"],
        "read addr":["Read Address"],
        addr_name:[addr_name,"地址","addr"],
        reg_name:[reg_name,"寄存器","reg_name","Type"],
        width_name:[width_name,"位置","width","Bit"],
        domain_name:[domain_name,"域名","field_name","Register Name"],
        access_name:[access_name,"RW","access","读写"],
        init_name:[init_name,"original","initVal\n（HEX）","初始值","Default Value"],
        description_name:[description_name,"Description","描述","Note"],
    }
    for col in table.columns:
        for k,v in names.items():
            if col in v:
                table.rename(columns={col:k}, inplace=True)
                break
        else:
            table.drop(col, axis=1, inplace=True, errors="ignore")     

def format_table(table:pd.DataFrame) -> None: # NOTE: not support LPM
    """format table for later use"""
    # item is invalid if either addr or width is nan
    invalid = table[addr_name].isna() | table[width_name].isna()
    invalid |= ~(table[addr_name].str.match(r'^[\da-fA-F]+$'))
    table.drop(labels=table.index[invalid], inplace=True)
    # format addr to int
    table[addr_name].replace(r"\.\d*","",regex=True,inplace=True)
    # if domain is nan, use reg+reseverd as domain name
    domain_na = table[domain_name].isna()
    table.loc[domain_na,(domain_name)] = table.loc[domain_na,(reg_name)] + "_reserved"
    # replace " " and "[]" with "_"
    table[reg_name].replace(r"[ \[\]:]","_",regex=True,inplace=True)
    table[domain_name].replace(r"[ \[\]:]","_",regex=True,inplace=True)
    # remove [] from width
    table[width_name].replace("[\[\]]","",regex=True,inplace=True)
    # "W"->"WO", "R"->"RO", else->"RW" # disable when use diff compare generated file with original reg_struct.h
    # table.loc[table[access_name]=="W",(access_name)] = "WO"
    # table.loc[table[access_name]=="R",(access_name)] = "RO"
    # table.loc[table[access_name].isna(),(access_name)] = "RW"
    # table.loc[~((table[access_name]=="WO") | (table[access_name]=="RO")),(access_name)] = "RW"
    # if description is nan, use "" as default
    table.loc[table[description_name].isna(),(description_name)] = ""
    table[description_name].replace("None","",regex=True,inplace=True)
    # reg is upper case, domain is lower case
    table[reg_name] = table[reg_name].str.upper()
    table[domain_name] = table[domain_name].str.lower()

def read_yc_reg(wb:__workbook_type, sheet_name:str) -> pd.DataFrame:
    """read table from workbook then format it"""
    table = read_excel(wb,sheet_name)
    keep_rename_columns(table)
    format_table(table)
    return table

def efile_to_hashmap(filename:str) -> dict:
    """convert an `e [addr]l[size]` output file to dict where key is addr and value is data"""
    return {f"{a:x}":d for d,a in zip(e2int(filename,"u1"))}

def parse_width(width:Union[str,int]) -> tuple[int,int]:
    """parse_width('[x]/x') = (x,x);  parse_width('[x:y]/x:y') = (x,y)"""
    if isinstance(width, (np.integer, int)):
        return width, width
    if (not width) or (width == "nan"):
        raise ValueError(f"parse_width() failed: {type(width)}:{width}")
    width = width.replace("[","").replace("]","").replace(" ","").split(":")
    return (int(width[1]), int(width[0])) if len(width)==2 else (int(width[0]), int(width[0]))

def parse_reg(addr:str, reg_map:dict, start:int, stop:int) -> str:
    """Get bits between `start` and `stop` from start address `addr` in `reg_map`.
    if total bits > 64, return `too large`, if cannot find `addr` in `reg_map` return `nan`, otherwise return string of data in hex"""
    bits = stop-start+1
    if bits > 64:
        return "too large"    
    if reg_map.get(addr,-1) >= 0:
        num = 0
        for i in range(stop//8+1):
            num |= reg_map[f"{int(addr,16)+i:x}"]<<(i*8)
        num = (num >> start) & ((1<<bits)-1)
        return f"{num:0{((bits-1)//8+1)*2}x}"
    else:
        return "nan"
    
def parse_table(table:pd.DataFrame, reg_map:dict, new_column:str) -> None:        
    """add new column named `new_column` to `table`, apply `parse_reg` to each row"""
    table[new_column] = np.zeros(len(table),str)
    for i in table.index:    
        try:
            start, stop = parse_width(table.loc[i,width_name])
            if start >= 0 and not pd.isna(table.loc[i,addr_name]):            
                addr = re.search(r"[\da-f]{4,}",table.loc[i,addr_name])
                if addr is not None:     
                    table.loc[i,new_column] = parse_reg(addr.group(), reg_map, start, stop)
        except:
            print(f"Unable to parse table line{i}: \n{table.loc[i]}")

def read_yc_reg_map(table:pd.DataFrame, reg_map_file:str, new_column=None) -> pd.DataFrame:
    """apply `parse_table` to a copy of `table` with reg_map read from `reg_map_file`"""
    table = table.copy()
    reg_map = efile_to_hashmap(reg_map_file)
    new_column = reg_map_file if new_column is None else new_column    
    parse_table(table, reg_map, new_column)
    return table

def read_yc_reg_map_in_folder(table:pd.DataFrame, top_folder:str, sheet_name:str, suffix:str=""):
    """apply `read_yc_reg_map` to every files start with `sheet_name` in a folder"""
    table = table[table[access_name]=="RW"]
    count = 0
    for dir,_,files in os.walk(top_folder):
        for f in files:
            if f.startswith(sheet_name):
                new_column = suffix + str(count) if suffix else f
                table = read_yc_reg_map(table, dir + "\\" + f, new_column=new_column)
                count += 1
    return table

def table2tree(table:pd.DataFrame, key:str) -> dict:
    """convert pandas Dataframe to tree like dict, use either `addr_name` or `reg_name` as `key`"""
    tree = {}
    old_key = ""
    for i in table.to_dict("records"):
        if tree.get(i[key],False):
            if i[key] != old_key:
                raise ValueError(f"multiple '{i[key]}'")
            tree[i[key]].append(i)
        else:
            tree[i[key]] = [i]
        old_key = i[key]
    return tree

