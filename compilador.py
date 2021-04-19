# entrada: fichero codigo.txt con instrucciones con operandos separados por una coma y un espacio, 1 por línea
#   add r1, r2, r3
#   beq r1, r4, 8
#   sw r3, 4(r0)
#   ...

# salida: instrucciones correspondientes pasadas a hexadecimal, línea a línea, en salida.txt

from enum import Enum
    
class instruccion_bin(Enum):
    ADD     = "000001"
    SUB     = "000001"
    OR      = "000001" 
    AND     = "000001" 
    LW      = "000010"
    SW      = "000011"
    BEQ     = "000100"
    SLTI    = "000111"
    NOP     = "000000"

##########################################################################################
# devuelve el codigo de operacion del string pasado a binario
def identificar_operacion(codigo):
    if (codigo == "add"):
        return instruccion_bin.ADD
    elif (codigo == "sub"):
        print("es sub(en identificar_operacion)")
        return instruccion_bin.SUB
    elif (codigo == "or"):
        return instruccion_bin.OR
    elif (codigo == "and"):
        return instruccion_bin.AND
    elif (codigo == "lw"):
        return instruccion_bin.LW
    elif (codigo == "sw"):
        return instruccion_bin.SW
    elif (codigo == "beq"):
        return instruccion_bin.BEQ
    elif (codigo == "slti"):
        return instruccion_bin.SLTI
    elif (codigo == "nop\n"):
        return instruccion_bin.NOP
    else:
        raise Exception("código no válido: ", codigo) 


##########################################################################################
# traduce rs/rt/rd a binario con 5 dígitos
def traducir_operando(op):
    op_bin = format(int(op), '#07b') #b: en binario, 07: 2 caracteres para 0b, resto para el digito(5)
    op_bin = op_bin[2:] # sin 0b
    return op_bin


##########################################################################################
# traduce funct a binario con 6 dígitos
def traducir_funct(codigo):
    # Se pasarán los 3 LSB de funct a la ALU como ctrl
    if (codigo == "add"):
        return "000000"
    elif (codigo == "sub"):
        print("es sub")
        return "000001"
    elif (codigo == "and"):
        return "000010"
    elif (codigo == "or"):
        return "000011"


##########################################################################################
# traduce add/sub/and/or
# formato aritméticas: 
#   op	    rs	    rt	    rd	    shamt	funct
#   000001	00001	00010  	00011  	00000	000000  ADD R3, R1, R2

# add  rd, rs, rt
# ...
def traducir_tipo_r(operacion_bin, operandos, codigo):
    rd_bin = traducir_operando(operandos[0].lstrip('r')) # quitando r
    rs_bin = traducir_operando(operandos[1].lstrip('r')) # quitando r
    rt_bin = traducir_operando(operandos[2].rstrip().lstrip('r')) # quitando r y '\n'
    
    shamt_bin = "00000" # no se hacen shifts
    
    funct_bin = traducir_funct(codigo) # hay que pasar el codigo de string, porque los enum al tener el mismo valor para add/sub/and/or, se confunden
    
    print("op: ", operacion_bin.value, "rs:", rs_bin, "rt:", rt_bin, "rd:", rd_bin, "shamt:", shamt_bin, "funct:", funct_bin)
    instr_bin = operacion_bin.value+rs_bin+rt_bin+rd_bin+shamt_bin+funct_bin
    print(instr_bin, "length:", len(instr_bin))
    
    instr_hex = hex(int(instr_bin, 2))
    instr_hex = instr_hex[2:] # quita 0x, como con 0b
    print(instr_hex)
    
    if (len(instr_hex) == 7): # añade padding en el caso de que salgan sólo 7 dígitos
        instr_hex = "0"+instr_hex
    
    return instr_hex


##########################################################################################
# traduce lw/sw/beq/slti
#formato lw, sw, beq:
#   op	    rs	    rt		inm
#   000010 	00000	00001 	0000000000000000 		LW  R1, 0(R0)  dir 0 

# lw  rt, inmed(rs)
# sw  rt, inmed(rs)
# stli rt, rs, inmed
# beq rs, rt, inmed
# ...
def traducir_tipo_i(operacion_bin, operandos, PC):
    if (operacion_bin == instruccion_bin.LW or operacion_bin == instruccion_bin.SW):
        # rt->inmed
        rt_bin = traducir_operando(operandos[0].lstrip('r')) # quitando r
        
        op2 = operandos[1].split("(") # [inm], [rs)\'n']
        inmediato = op2[0]
        
        rs = op2[1].rstrip(")'\n'")
        
        rs_bin = traducir_operando(rs.lstrip('r'))
        
        inmed_bin = format(int(op2[0]), '#018b') #b: en binario, 07: 2 caracteres para 0b, resto para el digito(16)
        inmed_bin = inmed_bin[2:] # quita 0b

    elif (operacion_bin == instruccion_bin.SLTI):
        # rt->rs->inmed
        rt_bin = traducir_operando(operandos[0].lstrip('r')) # quitando r
        
        rs_bin = traducir_operando(operandos[1].lstrip('r')) # quitando r
        
        inmed_bin = format(int(operandos[2]), '#018b') #b: en binario, 07: 2 caracteres para 0b, resto para el digito(16)
        inmed_bin = inmed_bin[2:] # quita 0b
        
    else: # BEQ
        # rs->rt->inmed
        # beq tiene los operandos de al revés que lw/sw/slti
        
        rs_bin = traducir_operando(operandos[0].lstrip('r')) # quitando r
        
        rt_bin = traducir_operando(operandos[1].lstrip('r')) # quitando r
        
        
        #la @ calculada es PC+4+4*Ext(inm)
        #PC = 20: queremos saltar a la posición 0, y el procesador calcula la dirección haciendo PC+4+ 4*Ëxt(inm) por eso ponemos FFFB: 4*FFFB+0014 = 0000
        
        inmed = (int(operandos[2]) - PC - 4)/4

           
        print("inmed calculado:", inmed)    
        
        inmed_bin = bin(int(inmed) % (1<<16)) # https://stackoverflow.com/questions/16255496/format-negative-integers-in-twos-complement-representation
        
        inmed_bin = inmed_bin[2:] # quita 0b
        
        print("inmed_bin: ", inmed_bin)

    
    print("op: ", operacion_bin.value, "rs:", rs_bin, "rt:", rt_bin, "inmed:", inmed_bin)
    instr_bin = operacion_bin.value+rs_bin+rt_bin+inmed_bin
    print(instr_bin)
    
    instr_hex = hex(int(instr_bin, 2))
    instr_hex = instr_hex[2:] # quita 0x, como con 0b
    print(instr_hex)
    
    if (len(instr_hex) == 7): # añade padding en el caso de que salgan sólo 7 dígitos HEX
        instr_hex = "0"+instr_hex
    
    return instr_hex



##########################################################################################
# Abre el fichero codigo.txt, crea el de salida y escribe las instrucciones en HEX
fich = open('codigo.txt') # read-only

fsalida = open("salida.txt", "w") # w: write, sobreescribe si existía, crea si no

fsalida.write("********************************\n")
fsalida.write("***** SUPERCOMPILADOR 5000 *****\n")
fsalida.write("********************************\n")
lines = fich.readlines()

PC = 0 # contador de PC para las BEQ

for line in lines:
    line = line.lower() # pasa todo a lowercase
    
    operandos_operacion = line.split(" ", 1) # [operacion] , [operandos]
    
    operacion_bin = identificar_operacion(operandos_operacion[0])

    if operacion_bin in {instruccion_bin.ADD, instruccion_bin.SUB, instruccion_bin.OR, instruccion_bin.AND}:
        operandos = operandos_operacion[1].split(", ") 
        # ([rd], [rs], [rt]) en aritmeticas, ([rt], [inmed(rs)]) en lw/sw, ([rs], [rt], [inm]) en beq, ([rt], [rs], [inmed]) en slti
        instr_hex = traducir_tipo_r(operacion_bin, operandos, operandos_operacion[0])
    
    elif operacion_bin in {instruccion_bin.LW, instruccion_bin.SW, instruccion_bin.BEQ, instruccion_bin.SLTI}:
        operandos = operandos_operacion[1].split(", ") 
        # ([rd], [rs], [rt]) en aritmeticas, ([rt], [inmed(rs)]) en lw/sw, ([rs], [rt], [inm]) en beq, ([rt], [rs], [inmed]) en slti
        instr_hex = traducir_tipo_i(operacion_bin, operandos, PC)
    
    elif operacion_bin == instruccion_bin.NOP:
        instr_hex = "00000000"
    
    fsalida.write(instr_hex.upper()+'\n')
    
    PC += 4

fich.close()
