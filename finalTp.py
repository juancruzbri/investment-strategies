# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 21:39:20 2022

@author: Win10
"""

import csv
from datetime import datetime as dt
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd



def cargarDicc():
    """
    cargarDicc no recibe ningún parámetro inicial.

    Inicializa un diccionario, y la misma cantidad de listas vacías por columna del archivo
    dónde están las cotizaciones.

    abre el archivo en modo lectura y además usamos un módulo "csv" más arriba para
    que se pueda leer correctamente ese tipo.

    luego por cada línea del archivo, exceptuando la primera(contador i==0),va a
    appendear el elemento que le corresponda a la misma que le corresponda.

    para luego armar el diccionario con las claves como el nombre de cada columna
    y como valor cada lista cargada en el for
    

    Returns
    -------
    dicc : diccionario
    """
    dicc        =   {}
    FECHAs      =   []
    ADAs        =   []
    BTCs        =   []
    DOGEs       =   []
    ETHs        =   []
    LTCs        =   []
    
    i= 0
    
    with open('cryptos_1h_6_months.csv', 'r') as file:
        reader = csv.reader(file)
        for date, ADA, BTC, DOGE, ETH, LTC in reader:
           #cambiar por slicing 
            if i == 0:
                i=1
                continue
            
            FECHAs.append(dt.fromisoformat(date))
            ADAs.append(float(ADA))
            BTCs.append(float(BTC))
            DOGEs.append(float(DOGE))
            ETHs.append(float(ETH))
            LTCs.append(float(LTC))
            
        dicc["fechas"]  =   FECHAs
        dicc["ADA"]     =   ADAs
        dicc["BTC"]     =   BTCs
        dicc["DOGE"]    =   DOGEs
        dicc["ETH"]     =   ETHs
        dicc["LTC"]     =   LTCs
        
    return dicc


def graficarSeparados(dicc):
    """
    Esta función graficarSeparados recibe como parámetro inicial un diccionario

    el dicc tiene que tener una clave “fecha” y alguna más.

    Esta función recorre las claves del diccionario menos "fechas"

    y por cada clave restante gráfica con matplotlib.plot

    en la posición x ira la lista dicc["fechas"]
    en la posición y ira la lista dicc[key](ira variando por el for)

    la función gráfica cada gráfico con cada título y nombre correspondiente por cada vuelta
    

    Parameters
    ----------
    dicc : diccionario

    Returns
    -------
    None.

    """
    
    for key in list(dicc.keys())[1::]:        
        
        
        plt.plot(dicc["fechas"], dicc[key], label = key)  
        
        plt.legend()
        plt.xlabel("fechas")
        plt.ylabel("valor")
        plt.title(f"Valuación en el tiempo de {key} ")
        plt.xticks(rotation=70)
        plt.show()



def graficarDicc(dicc):
    """
   graficarDicc recive un diccionario como parámetro inicial

   el dicc tiene que tener una clave “fecha” y alguna más.

   Esta función recorre las claves del diccionario menos "fechas"

   y por cada clave restante normaliza la lista(el valor) de dicha clave y lo almacena en normalizado
   para luego ir concatenando matplotlib.plot de cada clave

   en la posición x ira la lista dicc["fechas"]
   en la posición y ira la lista dicc[key](ira variando por el for)
   y en label la clave

   para luego del for hacer un solo matplotlib.show()
   y que nos muestre un gráfico con toda la variación de cada moneda pero normalizados.
    

    Parameters
    ----------
    dicc : diccionario

    Returns
    -------
    None.

    """
    for key in list(dicc.keys())[1::]:
        
        normalizado = np.array(dicc[key])/dicc[key][0]
        
        plt.plot(dicc["fechas"], normalizado, label = key)  
             
    plt.legend()
    plt.xlabel("Fechas.")
    plt.ylabel("Puntos porcentuales.")
    plt.title("Valores normalizados de criptomonedas.")   
    plt.xticks(rotation=70)
    plt.show()





      
def rendimiento(dicc):
    """
  La función rendimiento recibe un diccionario(uno que contenga variación de moneda)

  hace un for por cada clave menos "fechas"
  donde calcula el rendimiento de cada moneda a través de la cuenta
  rendimiento = (valor final-valor inicial)/valor inicial

  grafica el rendimiento de cada criptoactivo en un grafico de barras
   

   Parameters
   ----------
   dicc : diccionario

   Returns
   -------
   None.

   """
    for key in list(dicc.keys())[1::]:
        rend = (dicc[key][-1]-dicc[key][0])/dicc[key][0]
        plt.bar(key, rend)
    plt.xlabel("Activos.")
    plt.ylabel("Rendimineto.")
    plt.title("Rendimientos del los criptoactivos")
        
    plt.show()    

        
def plata_plomo(portfolio,fecha , data):
    """
   plata_plomo recibe un diccionario(portfolio), una fecha en forma de string y el diccionario del formato cargarDicc()

   busca el índice en el que se encuentra la fecha en la lista dicc["fechas"]

   inicializa {usd} con los dólares del portafolio

   y por cada vuelta del for, que va a buclear por todas las claves menos la primera va a ir
   sumando a usd el valor en dólares de cada moneda que tiene en el portafolio

   lo que hace es devolver el valor en dólares del portafolio en la fecha del parámetro pasado a la función

  

   Parameters
   ----------
   portfolio : diccionario
   fecha : str
   data : diccionario

   Returns
   -------
   usd : float

   """
    
    
    indiceFecha = data["fechas"].index(dt.fromisoformat(fecha))
    
    usd = portfolio["USD"]
    for key in list(data.keys())[1::]:
        usd += float(data[key][indiceFecha])*portfolio[key]
    
    return (usd)

def compra (data, portfolio , activo , cantidad , momento ):
    
    portfolio[activo] += float(cantidad)
    indice_cot=data["fechas"].index(dt.fromisoformat(momento))
    valor=(data[activo][indice_cot])*float(cantidad)
    portfolio["USD"] -= valor
    
    return portfolio

def venta (data, portfolio , activo , cantidad , momento ):
    
    portfolio[activo] -= float(cantidad)
    indice_cot=data["fechas"].index(dt.fromisoformat(momento))
    valor=(data[activo][indice_cot])*float(cantidad)
    portfolio["USD"] += valor
    
    return portfolio
 
def tonycash(capital):
    """
   tonycash recibe los dólares que tiene inicialmente el portafolio

   inicializa un portafolio con solo el capital
   abre el archivo de compras ventas
   hasta tener una lista {c_v} con cada elemento como una línea del archivo pero en forma de string

   luego hace un for de esa lista pero por cada línea 
   y con un split y desempaquetado asigna cada columna del string a una variable correspondiente

   para finalmente, si es compra
                           sumará la cantidad de criptomoneda 
                           y restará la cantidad de dólares utilizados para comprar dicha cantidad de cripto
                   
                   si es venta
                           restará la cantidad de criptomoneda 
                           y sumará la cantidad de dólares de dicha venta de cripto
                           
   todo lo anterior en el portafolio

   devuelve el portafolio final, luego de todas las transacciones y
   el valor del portafolio en dólares en la última fecha(plata_plomo())
   

   Parameters
   ----------
   capital : float

   Returns
   -------
   devuelve el portafolio final, luego de todas las transacciones y
   el valor del portafolio en dólares en la última fecha(plata_plomo())
   
   

   """
   
    data=cargarDicc()
    portfolio={'ADA': 0, 'BTC': 0, 'DOGE': 0, 'ETH': 0, 'LTC': 0, 'USD': capital}
    
    c_v_file=open("compras_ventas.csv" , "r")
    c_v=c_v_file.read().split("\n")[1:]
    ultima_fecha=data["fechas"][-1]
    c_v_file.close()
    
    
    for i in c_v:
        
        momento, activo , cantidad , tipo=i.split(",")
        #se podria desempaquetar los valores de datos para que sea mas leible
        if tipo=="COMPRA":
           portfolio=compra (data, portfolio , activo , cantidad , momento )
        
            
            
        elif tipo=="VENTA":
            portfolio=venta (data, portfolio , activo , cantidad , momento )
        
        
    return portfolio , plata_plomo(portfolio,str(ultima_fecha) ,cripto_dict)


def graf_tony(capital):
   
    """
   graf_tony recibe los dolares que tiene inicialmente el portafolio

   crea una lista l_fechas donde estan las fechas de cada transacción
   crea una lista l_port donde esta el portafolio inicial y luego todas sus modificaciones

   NOTA: l_port va a contener un elemento más que l_fechas ya que tiene el portafolio inicial

   con un for de todas las fechas(por hora)
   en una lista v_port concatena la evolución por hora de el portfolio


   pregunta si las fechas son iguales para sumar 1 al contador y que coincida siempre 
   como esta el portafolio en ese momento

   No devuelve nada, solo grafica las el valor en dólares del portafolio con respecto al tiempo.

   Parameters
   ----------
   capital : float

   Returns
   -------
   None.

   """
    data=cargarDicc()
    portfolio={'ADA': 0, 'BTC': 0, 'DOGE': 0, 'ETH': 0, 'LTC': 0, 'USD': capital}
    l_port=[]

    l_port.append(portfolio.copy())
    l_fecha=[]
    c_v_file=open("compras_ventas.csv" , "r")
    c_v=c_v_file.read().split("\n")[1:]
    
    c_v_file.close()
    
   
    for i in c_v:
        momento, activo , cantidad , tipo=i.split(",")
        
        
        if tipo=="COMPRA":
            
           portfolio=compra (data, portfolio , activo , cantidad , momento )
        
            
            
        elif tipo=="VENTA":
            
            portfolio=venta (data, portfolio , activo , cantidad , momento )

        l_port.append(portfolio.copy())
        l_fecha.append(dt.fromisoformat(momento))
        count=1
 
     

    count=0
    v_port=[]
    
    for x in data["fechas"]:
        
        if count != len(l_fecha):
            if x==l_fecha[count]:       
                count+=1            
            valor_portfolio=plata_plomo(l_port[count], str(x) ,cripto_dict )
            v_port.append(valor_portfolio)
        else:
            valor_portfolio=plata_plomo(l_port[count], str(x) ,cripto_dict )
            v_port.append(valor_portfolio)
    # de la linea 261 a la 300 se puede hacer mas eficiente?
        
    plt.plot(data["fechas"], v_port, label = "Valor en dolares.")
    plt.xlabel("fechas.")
    plt.ylabel("USD.")
    plt.xticks(rotation=70)
    plt.legend()
    plt.title("Valores del portfolio de Tony.  ")
    plt.show()
    
                                           
    
        
    
    
def media_movil(l_precios , n):
    """
    media movil() calcula la media movil de una secuencia y una ventana n,
    en los primeros elementos de la secuencia cuando la ventana sea mayor a los nueros a analizar se usara el primer numero de la secuencia para completar.


    Parameters
    ----------
    l_precios : list
        lista de valores a analizar
    n : int
        ventana en la cual se caulcula la media movil

    Returns
    -------
    TYPE list
        lista de las medias moviles de cada valor

    """
    #ej 3a
    for x in range(n-1):
        l_precios.insert( 0 , l_precios[0])
    precios_frame=pd.DataFrame(l_precios)
    
    l_media_movil=precios_frame.rolling(n , min_periods=0).mean()
    
    return list(l_media_movil[n-1:][0])
    
def graf_media_movil(data ,moneda):
    """
    grafica la media movil de ETH en una ventana de 30 dias y de 7 junto con la cotisacion de esta
    

    Parameters
    ----------
    data : dicionario
        DESCRIPTION.
        dicionario con las cotisaciones y fechas de las criptomonedas

    Returns
    -------
    None.

    """
    plt.plot(data["fechas"] , data[moneda] , label=f"valor {moneda}")
        
    media_ETH=media_movil(cripto_dict[moneda].copy(), 30*24)
    plt.plot(cripto_dict["fechas"] , media_ETH , label="media movil 30 dias")
    
    media_ETH=media_movil(cripto_dict[moneda].copy(), 24*7)
    plt.plot(cripto_dict["fechas"] , media_ETH , label="media movil 7 dias")
    
    plt.xlabel("Fechas." )
    plt.ylabel("USD.")
    plt.xticks(rotation=70)
    plt.legend()
    plt.title(f"{moneda}.")
    plt.show()
    
def estrategia_de_invercion(data, media_movil , activo , capital):
    
    portfolio={'ADA': 0, 'BTC': 0, 'DOGE': 0, 'ETH': 0, 'LTC': 0, 'USD': capital}
    frame=(zip(data[activo][::-1],media_movil))
    
    indice=0
    for precio , media_movil in frame:
        
        momento=str(data["fechas"][indice])
        
        if precio== media_movil:
            continue
        
        elif precio>media_movil:
            cantidad=portfolio["USD"]/data[activo][indice]
            portfolio=compra(data, portfolio, activo, cantidad , momento)
            
        elif precio<media_movil:
            portfolio=venta(data, portfolio, activo, portfolio[activo], momento)
        indice+=1
            
    capital_final=plata_plomo(portfolio,str(data["fechas"][-1]) , data)
    
    return ((capital_final/capital)-1)

def DMAC(data, small_window, big_window , activo: str, capital):
    
    media_small = media_movil(cripto_dict[activo].copy(), small_window)
    media_big   = media_movil(cripto_dict[activo].copy(), big_window)  
    
    portfolio   = {'ADA': 0, 'BTC': 0, 'DOGE': 0, 'ETH': 0, 'LTC': 0, 'USD': capital}
    
    frame       = (zip(media_small,media_big))
    
    indice      = 0
    
    for small , big in frame:
        
        momento=str(data["fechas"][indice])
        
        if small==big:
            continue
        
        elif small>big:
            cantidad  = portfolio["USD"]/data[activo][indice]
            portfolio = compra(data, portfolio, activo, cantidad , momento)
            
        elif small<big:
            portfolio = venta(data, portfolio, activo, portfolio[activo], momento)
            
        indice+=1
            
    capital_final = plata_plomo(portfolio,str(data["fechas"][-1]) , data)
    
    return ((capital_final/capital)-1)

def superDMAC(data):   
    
    capital_final   = 0
    
    for activo in list(cripto_dict.keys())[1::]:
        portfolio   = {'ADA': 0, 'BTC': 0, 'DOGE': 0, 'ETH': 0, 'LTC': 0, 'USD': 0}
        media_small = media_movil(cripto_dict[activo].copy(), 168)
        media_big   = media_movil(cripto_dict[activo].copy(), 720) 
        frame       = (zip(media_small,media_big))
        indice      = 0
        primera_vez = 1
        
        for small , big in frame:
            
            momento=str(data["fechas"][indice])
            
            if small==big:
                continue
            
            elif small>big:
                if primera_vez == 1:
                    portfolio["USD"] = 200.0                    
                    primera_vez = 0
                
                cantidad  = portfolio["USD"]/data[activo][indice]                    
                portfolio = compra(data, portfolio, activo, cantidad , momento)
                
            elif small<big:                
                portfolio = venta(data, portfolio, activo, portfolio[activo], momento)
                
                
            indice+=1
        """vende todo y el portafolio vuelve al inicial pero le sumamos plata al capital final"""  
        portfolio = venta(data, portfolio, activo, portfolio[activo], momento)
        capital_final += portfolio["USD"]
    return ((capital_final/1000)-1)

def finalStrategy(archivo):
    """toda la mágia"""
    
    with open('transacciones.txt', 'w') as file:
        file.write("hola")

   
if __name__ ==   '__main__':
    cripto_dict = cargarDicc()
    
    graficarSeparados(cripto_dict)

    graficarDicc(cripto_dict)

    rendimiento(cripto_dict)

    dic_and_cash=tonycash(1000)
    print(f"El portfolio final de tony es {dic_and_cash[0]} y el valor es {dic_and_cash[1]}")
    
    graf_tony(1000)
    
    graf_media_movil(cripto_dict.copy() , "ETH")
    graf_media_movil(cripto_dict.copy() , "BTC")
    
    x=estrategia_de_invercion(cripto_dict, media_movil(cripto_dict["BTC"].copy(), 24) , "BTC" , 1000)
    
    DMAC(cripto_dict, 168, 720, "BTC", 1000)
    
    superDMAC(cripto_dict.copy())
    
    finalStrategy(cripto_dict)

    






"""
PROBLEMAS ENCONTRADOS

-Invalid isoformat string: 'datetime' (por la primera linea del archivo)
    -solución--->salteamos la primer línbea con un contador

-problemas en la funcion de grafiacr a tony, como crear una lista con todos los valores

-el problema de plataplomo era que cada vezque la llamaba abria y copiaba los valores , se lo puse como un parametro para ahorrar eso

-en tonygraf yo apendiaba un portfolio pero este se iba cambiando porque se autoreferenciaba por eso el copy

"""

