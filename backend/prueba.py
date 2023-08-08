sec = "TRANSICIÓNS VILA DE ABRENTE"

seclist = sec.split(".")

if len(seclist) > 2:
    cap = seclist[0]
    num = seclist[1]

    ub = ""
    ub_flag = True

    loc = ""

    amb = ""
    for item in seclist:
        if 'EXT' in item or 'INT' in item or 'NAT' in item:
            ub += item
            ub_flag = False
        elif ub_flag and seclist.index(item) > 1:
            loc += item + "."
        elif item != "INTERCUT" and seclist.index(item) > 2:
            amb += item
            
    print(cap, num, loc.strip(), ub.strip(), amb.strip())

