
import pandas as pd
from datetime import datetime,timedelta
import random
import sys


dias = 15
diasmin = 3
diasmax = 3

Nodos = ['BOS','IAD','PHL','MIA']
origen = 'ATL'
Final = 'EWR'
inicio = '2022-04-26'
Finicio = datetime.strptime(inicio, "%Y-%m-%d")

fields = []
rows = []
mapabase = []
mapa = []
maparutas = []

def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier    

#=======================================================================================================

def routefinder (a,b,T):

    ini = a
    fin = b
    today = T
    bestb = ''
    bestprice = 9999

    for B in mapalt:

        fir = int(PriceCheck(a,B,today,rutas))
        today2 = today + timedelta(days=3)
        sec = int(PriceCheck(B,b,today2,rutas))
        total = fir + sec

        if fir != 0:
            if sec != 0:
                if total < bestprice:
                    bestprice = total
                    bestb = B
                
    print ('ruta alternativa: ',ini,'->',bestb,'->',fin,' | precio: ', bestprice)   
    
    print('--------------------------------------')
    resp = input('0.- ruta original || 1.- ruta alterna  ||  ')
    print('--------------------------------------')

    if resp != '1':
        bestb = ''
        
    return(bestb) 

def PriceCheck (a,b,d,r):

    start = a
    end = b
    today = str(d)[:10]
    csv_reader = r

    startcheck = csv_reader[csv_reader['startingAirport'] == start]
    endcheck = startcheck[startcheck['destinationAirport'] == end]
    datecheck = endcheck[endcheck['flightDate'] == today]

    if datecheck.size == 0:
        return ('0')

    price = 9999999
    for A in datecheck['totalFare']:
        if A < price:
            price = A    

    return(price)

def BuscaRuta (a,b,c,r):

    start = a
    end = b
    precio = c
    csv_reader = r

    startcheck = csv_reader[csv_reader['startingAirport'] == start]
    endcheck = startcheck[startcheck['destinationAirport'] == end]
    price = endcheck[endcheck['totalFare'] == precio] 

    return(price)

def precioiteracion(a,r,t,i):

    rutatemp = a
    rutas = r

    A = i
    B = rutatemp[0]
    T = t

    total = 0
    ruta2 = []

    total = total + int(PriceCheck(A,B,T,rutas))
    # print ('viaje ',A,' -> ',B,' |Precio: ',PriceCheck(A,B,T,rutas),' |fecha salida: ',T) 

    A = rutatemp[0]
    ruta2.append(B)
    rutatemp.remove(B)  

    T = T + timedelta(days=diasmin)

    while len(rutatemp) > 0:

        Tmax = T + timedelta(days=diasmax)
        paso = 9999

        B = rutatemp[0]
        B1 = ''

        while T <= Tmax:

            price = int(PriceCheck(A,B,T,rutas))
            
            if price < paso and price > 0 :
                mejordia = T
                paso = price
                B1 = B

            T = T + timedelta(days=1)

        if B1 == '':
            # print('ruta ',A,'->',B,'no posible dadas las fechas')
            return (0)
            
        else: 
            total = total + int(PriceCheck(A,B,T,rutas))            
            # print ('viaje ',A,' -> ',B,' |Precio: ',PriceCheck(A,B,T,rutas),' |fecha salida: ',mejordia)
            T = mejordia + timedelta(days=diasmin)
            A = rutatemp[0]
            ruta2.append(B)
            rutatemp.remove(B) 

    # print ('precio total ruta : ',truncate(total,2))
    return(total)

def precioiteracion2(a,r):

    rutatemp = a
    rutas = r
    rutafinal = []
    rutatemp.remove(Final)

    A = origen
    B = rutatemp[0]
    T = Finicio
    total = 0

    rutafinal.append(origen)
    total = total + int(PriceCheck(A,B,T,rutas))
    print ('viaje ',A,' -> ',B,' |Precio: ',PriceCheck(A,B,T,rutas),' |fecha salida: ',T)
    rt = routefinder(A,B,T)

    if rt != '':

        mapalt.remove(rt)
        rutafinal.append(rt)
        T = T + timedelta(days=2)

        rutatemp.remove(B)
        temp = iteracion(rutatemp,T,B)
        rutatemp = []
        rutatemp.append(B)
        for I in temp:
            rutatemp.append(I)
    
    rutafinal.append(B)

    A = rutatemp[0]
    rutatemp.remove(B)  

    T = T + timedelta(days=diasmin)

    while len(rutatemp) > 0:

        Tmax = T + timedelta(days=diasmax)
        paso = 9999

        B = rutatemp[0]
        B1 = ''
        rt = ''

        while T <= Tmax:

            price = int(PriceCheck(A,B,T,rutas))
            
            if price < paso and price > 0 :
                mejordia = T
                paso = price
                B1 = B

            T = T + timedelta(days=1)

        if B1 == '':
            print('ruta ',A,'->',B,'no posible dadas las fechas')
            return (0)
            
        else: 
            total = total + int(PriceCheck(A,B,T,rutas))            
            print ('viaje ',A,' -> ',B,' |Precio: ',PriceCheck(A,B,T,rutas),' |fecha salida: ',mejordia)
            rt = routefinder(A,B,mejordia)

            if rt != '':
                
                mapalt.remove(rt)
                rutafinal.append(rt)
                T = T + timedelta(days=2)

                rutatemp.remove(B)
                if rutatemp != []:
                    temp = iteracion(rutatemp,T,B)
                    rutatemp = []
                    rutatemp.append(B)
                    for I in temp:
                        rutatemp.append(I)
                else:
                    rutatemp.append(B)
                

            T = mejordia + timedelta(days=diasmin)
            A = rutatemp[0]
            rutafinal.append(B)
            rutatemp.remove(B) 
    rutafinal.append(Final)

    # print ('precio total ruta : ',total,' USD')
    return(rutafinal)

def precioiteracionprint(a,r,t,i):

    rutatemp = a
    rutas = r
    T = t
    total = 0

    while len(rutatemp) > 1:

        Tmax = T + timedelta(days=diasmax)
        paso = 9999

        A = rutatemp[0]
        B = rutatemp[1]
        B1 = ''

        while T <= Tmax:

            price = int(PriceCheck(A,B,T,rutas))
            
            if price < paso and price > 0 :
                mejordia = T
                paso = price
                B1 = B

            T = T + timedelta(days=1)

        if B1 == '':
            # print('ruta ',A,'->',B,'no posible dadas las fechas')
            return (0)
            
        else: 
            total = total + int(PriceCheck(A,B,T,rutas))            
            print ('viaje ',A,' -> ',B,' |Precio: ',PriceCheck(A,B,T,rutas),' |fecha salida: ',mejordia)
            T = mejordia + timedelta(days=diasmin)
            rutatemp.remove(A) 

    print('======================================')
    print ('precio total ruta : ',truncate(total,2),' USD')
    return(total)

def iteracion (ruta,T,I):

    inicio = I
    today = T
    mejorruta = ruta
    ite = 0
    k = len(ruta)-1
    rutaux = []
    rutait = []
    total = 99999

    while ite < 20:

        i = random.randint(0,k)
        rutab = mejorruta
        
        if i+1 >= k:
            j = i-1
        else:
            j = i+1
        temp = rutab[i]
        rutab[i] = rutab[j]
        rutab[j] = temp
        

        for A in rutab:
            rutaux.append(A)    
        rutaux.append(Final)    

        propuesta = precioiteracion(rutaux,rutas,today,inicio)

        if propuesta < total:
            total = propuesta
            mejorruta = rutab
            rutait = []
            for A in mejorruta:
                rutait.append(A)
            # print('======================================')
            # print('nueva mejor ruta: ', rutab)
            # print('======================================')
        # else:
        #     print('======================================')
        #     print('ruta: ',rutab)
        #     print('======================================')    

        ite = ite+1    
    
    if rutait == []:
        rutait = ruta   

    return (rutait)

#=======================================================================================================
#=======================================================================================================
print('======================================')
print('Inicio Programa')
print('======================================')

with open('itineraries.csv', 'r') as csv_file:
    csv_reader = pd.read_csv(csv_file, nrows= 1000000)

    csv_reader.pop('legId')
    csv_reader.pop('searchDate')
    csv_reader.pop('fareBasisCode')
    csv_reader.pop('segmentsAirlineName')
    csv_reader.pop('segmentsAirlineCode')
    csv_reader.pop('segmentsEquipmentDescription')
    csv_reader.pop('segmentsDurationInSeconds')
    csv_reader.pop('segmentsDistance')
    csv_reader.pop('segmentsCabinCode')
    csv_reader.pop('elapsedDays')
    csv_reader.pop('segmentsDepartureTimeRaw')
    csv_reader.pop('segmentsArrivalTimeEpochSeconds')
    csv_reader.pop('segmentsArrivalTimeRaw')
    csv_reader.pop('segmentsArrivalAirportCode')
    csv_reader.pop('segmentsDepartureAirportCode')
    csv_reader.pop('isBasicEconomy')
    csv_reader.pop('isRefundable')
    csv_reader.pop('isNonStop')
    csv_reader.pop('baseFare')
    csv_reader.pop('seatsRemaining')
    csv_reader.pop('totalTravelDistance')
    csv_reader.pop('segmentsDepartureTimeEpochSeconds')


    for data in csv_reader.destinationAirport:
        if data not in mapa:
            mapa.append(data)

mapalt = mapa
mapalt.remove(origen)    
mapalt.remove(Final)

for i in Nodos:
    mapalt.remove(i)

print (mapalt)
print('======================================')
print('CSV cargado')
print('======================================')
    

rutas = csv_reader
       
mapaaux = Nodos

B1 = origen
total = 0
ruta = []

#===========================================================================
# Calculo ruta base
#===========================================================================

print('======================================')
print('ruta base')
print('======================================')

print('fecha inicio: ', Finicio)

A = B1
T = Finicio

for B in mapaaux:
    paso = 9999
    B1 = ''
    if int(PriceCheck(A,B,T,rutas)) < paso:
        paso = int(PriceCheck(A,B,T,rutas))
        B1 = B
    
ruta.append(B1)
mapaaux.remove(B1)        
print ('viaje ',A,' -> ',B1,' |Precio: ',PriceCheck(A,B1,T,rutas),' |fecha salida: ',Finicio)
total = total + PriceCheck(A,B1,T,rutas)    

T = T + timedelta(days=diasmin)

while len(mapaaux) > 0:

    Tmax = T + timedelta(days=diasmax)
    paso = 9999

    for B in mapaaux:

        A = B1
        B1 = ''

        while T <= Tmax:

            price = int(PriceCheck(A,B,T,rutas))
            
            if price < paso and price > 0 :
                mejordia = T
                paso = price
                B1 = B
            T = T + timedelta(days=1)

        if B1 == '':
            print('ruta no posible')
            sys.exit()
            
        else: 
            total = total + int(PriceCheck(A,B1,T,rutas))        
            ruta.append(B1)
            mapaaux.remove(B1)        
            print ('viaje ',A,' -> ',B1,' |Precio: ',PriceCheck(A,B1,T,rutas),' |fecha salida: ',mejordia)
            T = mejordia + timedelta(days=diasmin)

T = T + timedelta(days=diasmin)

while T <= Tmax:

    price = int(PriceCheck(B1,Final,T,rutas))
    
    if price < paso and price > 0 :
        mejordia = T
        paso = price
        B1 = B
        print(B1)   
    T = T + timedelta(days=1)      

print ('viaje ',B1,' -> ',Final,' |Precio: ',PriceCheck(B1,Final,T,rutas),' |fecha salida: ',T)     
total = total + PriceCheck(B1,Final,T,rutas)       

print ('precio total ruta base: ',truncate(total,2))

# print('======================================')
# print(ruta) 
# print('======================================')

#===========================================================================
# Calculo iteraciones
#===========================================================================

mejorruta = ruta
iter = 0
k = len(ruta)-1
rutaux = []
rutaux2 = []

while iter < 20:

    i = random.randint(0,k)
    rutab = mejorruta
    
    if i+1 >= k:
        j = i-1
    else:
        j = i+1
    temp = rutab[i]
    rutab[i] = rutab[j]
    rutab[j] = temp
    

    for A in rutab:
        rutaux.append(A)    
    rutaux.append(origen)    

    propuesta = precioiteracion(rutaux,rutas,Finicio,origen)

    if propuesta < total:
        total = propuesta
        mejorruta = rutab
        rutaux2 = []
        for A in mejorruta:
            rutaux2.append(A)
    #     print('======================================')
    #     print('nueva mejor ruta: ', rutab)
    #     print('======================================')
    # else:
    #     print('======================================')
    #     print('ruta: ',rutab)
    #     print('======================================')    

    
    iter = iter+1    

if rutaux2 == []:
    rutaux2 = ruta    
rutaux2.append(Final)

print('======================================')  
print('mejor ruta: ',rutaux2)
print('======================================')  
fin = precioiteracion2(rutaux2,rutas)
print('======================================')
print('ruta final: ',fin)
print('======================================')
precioiteracionprint(fin,rutas,Finicio,origen)
print('======================================')


