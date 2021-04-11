# mini_mips_a_hex
Mini traductor de instrucciones básicas de MIPS en 32 bits a hexadecimal

Entrada necesaria: fichero codigo.txt al mismo nivel que compilador.py, con instrucciones cuyos operandos están separados por una coma y un espacio (1 por línea)
  Ejemplos:
    add r1, r2, r3
    beq r1, r4, 8
    sw r3, 4(r0)

Salida: instrucciones correspondientes pasadas a hexadecimal, línea a línea, en salida.txt
