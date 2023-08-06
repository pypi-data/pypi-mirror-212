#from numero_letras import numero_a_letras, numero_a_moneda
from jgp_utils.numero_letras import numero_a_letras, numero_a_moneda
#import el time
import locale 
from datetime import datetime 
import locale 
locale.setlocale(locale.LC_TIME) 

class Utils:
        
    def literalDecimal(doubleX):
        literal=numero_a_letras(doubleX)
        sw='punto' in literal
        if(sw==False):
            literal=literal+ ' punto cero'
        print(literal.upper())
        return literal

    #convertimos de numero a letras
    def literalNumeral(int):
        literal=numero_a_letras(int)
        literal=literal.upper()
        return literal    

    def literalEnteroMontoPrestamo(doubleX):
        numero_entero = int(doubleX)
        numero_decimal = int(round((abs(doubleX) - abs(numero_entero)) * 100))
        literal_decimal =''
        if(numero_decimal == 0):   
            literal_decimal='00' 
            literal=numero_a_letras(numero_entero).upper() +' ' +literal_decimal
        if len(str(numero_decimal)) == 1: 
            literal_decimal= '0' + str(numero_decimal)
            literal=numero_a_letras(numero_entero).upper() + ' '+literal_decimal
        else:
            literal_decimal = str(numero_decimal)
            literal=numero_a_letras(numero_entero).upper() +' '+ literal_decimal
        
        literal= 'Bs. '+str(int(doubleX))+','+literal_decimal+'.- ('+literal+'/100 BOLIVIANOS)'
        print("======================================")
        print(literal)
        print("======================================")
        return literal
    def get_fecha(self, fecha):
        #diccionario (clave- valor)
        mesesDic = { 
            1:'enero', 
            2:'febrero', 
            3:'marzo', 
            4:'abril', 
            5:'mayo', 
            6:'junio', 
            7:'julio', 
            8:'agosto', 
            9:'septiembre', 
            10:'octubre', 
            11:'noviembre', 
            12:'diciembre' 
        } 
        
        datetime_obj = datetime.strptime(fecha, '%Y-%m-%d') 
        
        #
        return (datetime_obj.strftime("%d de "+mesesDic[datetime_obj.month]+" de %Y"))
