
import pandas as pd
from datetime import datetime,timedelta
import random
import sys
from flask import Flask,render_template,request


dias = 15
diasmin = 3
diasmax = 3

Nodos = ['ATL','BOS','IAD','PHL','MIA']
origen = 'ATL'
inicio = '2022-04-26'
Finicio = datetime.strptime(inicio, "%Y-%m-%d")

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

def CSV_Creation():
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

    print('======================================')
    print('CSV cargado')
    print('======================================')
    return(csv_reader)

def precioiteracion(a,r):

    rutatemp = a
    rutas = r
    arr=[]
    A = origen
    B = rutatemp[0]
    T = Finicio

    total = 0
    ruta2 = []

    total = total + int(PriceCheck(A,B,T,rutas))
    print ('viaje ',A,' -> ',B,' |Precio: ',PriceCheck(A,B,T,rutas),' |fecha salida: ',T) 
    arr.append('viaje %s -> %s |Precio: %s |fecha salida: %s'%(A,B,PriceCheck(A,B,T,rutas),T))
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
            print('ruta ',A,'->',B,'no posible dadas las fechas')
            return (0)
            
        else: 
            total = total + int(PriceCheck(A,B,T,rutas))            
            print ('viaje ',A,' -> ',B,' |Precio: ',PriceCheck(A,B,T,rutas),' |fecha salida: ',mejordia)
            arr.append('viaje %s -> %s |Precio: %s |fecha salida: %s'%(A,B,PriceCheck(A,B,T,rutas),mejordia))

            T = mejordia + timedelta(days=diasmin)
            A = rutatemp[0]
            ruta2.append(B)
            rutatemp.remove(B) 

    print ('precio total ruta : ',truncate(total,2))
    return(total,arr)

#=======================================================================================================
#=======================================================================================================


def mejorruta(dias,diasmin,diasmax,Nodos,origen,Finicio):
    print('======================================')
    print('Inicio Programa')
    print('======================================')
    arr=[]
    rutas = CSV_Creation()
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

    print('fecha inicio: ', Finicio)

    A = B1
    T = Finicio

    for B in mapaaux:
        paso = 9999
        B1 = ''
        if int(PriceCheck(A,B,T,rutas)) < paso:
            paso = int(PriceCheck(A,B,T,rutas))
            B1 = B

    total = total + PriceCheck(A,B1,T,rutas)        
    ruta.append(B1)
    mapaaux.remove(B1)        
    print ('viaje ',A,' -> ',B1,' |Precio: ',PriceCheck(A,B1,T,rutas),' |fecha salida: ',Finicio)

    T = T + timedelta(days=diasmin)

    while len(mapaaux) > 0:

        Tmax = T + timedelta(days=diasmax)
        paso = 9999
        A = B1

        for B in mapaaux:

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
                return
                sys.exit()
                
            else: 
                total = total + int(PriceCheck(A,B1,T,rutas))        
                ruta.append(B1)
                mapaaux.remove(B1)        
                print ('viaje ',A,' -> ',B1,' |Precio: ',PriceCheck(A,B1,T,rutas),' |fecha salida: ',mejordia)
                T = mejordia + timedelta(days=diasmin)

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

        propuesta,a = precioiteracion(rutaux,rutas)

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
    a,arr=precioiteracion(rutaux2,rutas)
    print('======================================')
    print(' mejor ruta: ', total)
    print('======================================')
    return total,arr


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')
@app.route('/calculate/',methods=["GET", "POST"])
def calculate():
    origen=request.form['origen']
    Nodos=str(request.form['visitar'])
    Nodos=Nodos.split(sep=',')
    nodosf=[origen]+Nodos
    diasmin=int(request.form['diasmin'])
    diasmax=int(request.form['diasmax'])
    inicio=request.form['inicio']
    Finicio = datetime.strptime(inicio, "%Y-%m-%d")
    mejor,arr=mejorruta(dias,diasmin,diasmax,nodosf,origen,Finicio)
    return arr,mejor


if __name__ == '__main__':
    app.run(debug=True,port=5000)