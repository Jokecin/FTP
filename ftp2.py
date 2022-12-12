
import pandas as pd
import random


dias = 10
fields = []
rows = []
mapabase = []
mapa = []
maparutas = []

class Nodo(object):
    origen = ""
    destino = ""
    tiempo = ""
    precio = 0
    def org(): return  self.origen
    def des(): return  self.destino
    def tmp(): return  self.tiempo
    def pre(): return  self.precio

def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier    

def newnodo(origen, destino, tiempo,precio):
    nodo = Nodo()
    nodo.org = origen
    nodo.des = destino
    nodo.tmp = tiempo
    nodo.pre = precio
    # Note: I didn't need to create a variable in the class definition before doing this.
    return nodo

#=======================================================================================================

def PriceCheck (a,b,r):

    start = a
    end = b
    csv_reader = r

    startcheck = csv_reader[csv_reader['startingAirport'] == start]
    endcheck = startcheck[startcheck['destinationAirport'] == end]

    if endcheck.size == 0:
        return ('0')

    price = 9999999
    for A in endcheck['totalFare']:
        if A < price:
            price = A    

    return(price)

def Timecheck(a,b,r):

    start = a
    end = b
    csv_reader = r

    startcheck = csv_reader[csv_reader['startingAirport'] == start]
    endcheck = startcheck[startcheck['destinationAirport'] == end]

    if endcheck.size == 0:
        return ('0')

    price = 9999999
    for A in endcheck['travelDuration']:
        if A < price:
            price = A    

    return(price)

def Datecheck(a,b,p,r):
    
    start = a
    end = b
    price = p
    csv_reader = r

    startcheck = csv_reader[csv_reader['startingAirport'] == start]
    endcheck = startcheck[startcheck['destinationAirport'] == end]
    PriceCheck = endcheck[endcheck['totalFare'] == price]

    for A in PriceCheck['flightDate']:
        Date = A

    return(Date)    

def BuscaRuta (a,b,c,r):

    start = a
    end = b
    precio = c
    csv_reader = r

    startcheck = csv_reader[csv_reader['startingAirport'] == start]
    endcheck = startcheck[startcheck['destinationAirport'] == end]
    price = endcheck[endcheck['totalFare'] == precio] 

    return(price)

def CSV_Creation():
  with open('itineraries.csv', 'r') as csv_file:
    csv_reader = pd.read_csv(csv_file, nrows= 100000)

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

    return(csv_reader)

def precioiteracion(a,r):

    rutatemp = a
    rutas = r

    A = origen
    total = 0
    ruta2 = []

    while len(rutatemp) > 0:
        B = rutatemp[0]
        paso = int(PriceCheck(A,B,rutas))
        total = total + PriceCheck(A,B,rutas)   
        print ('viaje ',A,' -> ',B,' |Precio: ',PriceCheck(A,B,rutas),' |fecha: ',Datecheck(A,B,PriceCheck(A,B,rutas),rutas))     
        A = rutatemp[0]
        ruta2.append(B)
        rutatemp.remove(B)        
    print ('viaje ',B1,' -> ',origen,' |Precio: ',PriceCheck(B1,origen,rutas))

    total = total + int(PriceCheck(B1,origen,rutas))
    print ('precio total ruta base: ',truncate(total,2))

    return(total)

#=======================================================================================================
#=======================================================================================================

rutas = CSV_Creation()

Nodos = ['ATL','BOS','IAD','PHL','MIA']
origen = 'ATL'
inicio = '2022-04-23'    

mapaaux = Nodos
mapaaux.remove(origen)

B1 = origen
total = 0
ruta = []

#===========================================================================
# Calculo ruta base
#===========================================================================

print('======================================')
print('ruta base')
print('======================================')

while len(mapaaux) > 0:
    A = B1
    for B in mapaaux:
        paso = 9999
        B1 = ''
        if int(PriceCheck(A,B,rutas)) < paso:
            paso = int(PriceCheck(A,B,rutas))
            B1 = B
    total = total + PriceCheck(A,B1,rutas)        
    ruta.append(B1)
    mapaaux.remove(B1)        
    print ('viaje ',A,' -> ',B1,' |Precio: ',PriceCheck(A,B1,rutas))
print ('viaje ',B1,' -> ',origen,' |Precio: ',PriceCheck(B1,origen,rutas))

total = total + PriceCheck(B1,origen,rutas)
print ('precio total ruta base: ',truncate(total,2))

print('======================================')
print(ruta)
print('======================================')

#===========================================================================
#===========================================================================

mejorruta = ruta
iteracion = 0
k = len(ruta)-1

while iteracion < 10:

    i = random.randint(0,k)
    rutab = mejorruta
    
    if i+1 >= k:
        j = i-1
    else:
        j = i+1
    temp = rutab[i]
    rutab[i] = rutab[j]
    rutab[j] = temp

    rutaux = []
    for A in rutab:
        rutaux.append(A)
    print ('rutaux: ',rutaux)        

    propuesta = precioiteracion(rutaux,rutas)

    if propuesta < total:
        total = propuesta
        mejorruta = rutab
        rutaux2 = []
        for A in mejorruta:
            rutaux2.append(A)
        print('======================================')
        print('nueva mejor ruta: ', rutab)
        print('======================================')
    else:
        print('======================================')
        print('ruta: ',rutab)
        print('======================================')    

    iteracion = iteracion+1    

print('======================================')  
print('======================================')  
precioiteracion(mejorruta,rutas)
print('======================================')
print(' mejor ruta: ', total)
print('======================================')