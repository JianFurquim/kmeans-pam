import sys
import random
import math
import matplotlib.pyplot as plt
import datetime

#	Autor: Jian Furquim
#   furquimjian@gmail.com
#	
#	Algoritimo k-means dinamico
#
#	Roda
#		$ python3 kmeans.py data.dat 3 7
#		
# 		Sendo o parametro 2 o arquivo com os pontos "data.dat"
#		E o parametro 3 o numero de clusters que deseja usar (no exemplo está sendo usado 3)
#		E o parametro 7 é o numero de iteraçãos
#

# função pra gerar colors e maker baseado no numero de clusters
def colorsMakers(num):
	auxC = ['b', 'g', 'r', 'c', 'm', 'y']
	auxM = ['o', 'v', '^', '<', '>', '1', '2', '3', '4', 's', 'p', '*', 'h', 'H', '+', 'x', 'D', 'd']
	colors = []
	makers = []

	for i in range(num):
		numr = random.randint(0 , len(auxC)-1)
		colors.append(auxC[numr])
		numr = random.randint(0 , len(auxM)-1)
		makers.append(auxM[numr])

	return colors, makers

# Função para ler os dados do arquivo e gerar um K aleatório
def leitor(arquivo, num):
	file = open(arquivo, 'r')
	lista  = []

	for line in file:
		a, b = line.split()
		lista.append([float(a), float(b), random.randint(1 , num)])

	return lista

# Função para criar um arrey de tamanho num com todos elementos zeros 
def startArrayNum(num):
	centroids = []
	for i in range(num):
		centroids.append(0)

	return centroids

#Função pra calcular a distancia de um ponto para outro
def distancia(x1, y1, x2, y2):
	return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

# Função pra atualizar o centroid baseado nos seus pontos K
def calCentroids(lista, k):

	cont = 0
	auxY = 0
	auxX = 0

	for i in range(len(lista)):
		if(lista[i][2] == k):
			auxX += lista[i][0]
			auxY += lista[i][1]
			cont += 1

	if(cont != 0):
		return[auxX/cont, auxY/cont]
	else:
		return[lista[0][0], lista[0][1]]

# Função para retornar o indice onde está a menor distancia de de um centroid para um ponto
def indexMenorDist(dist):
	tempdist = dist[0]
	index = 1
	for i in range(len(dist)):
		if(dist[i] < tempdist):
			tempdist = dist[i]
			index = i+1
	return index

# Função para recalcular o K baseado no centroid
def recalK(lista, centroids):
	
	dist = startArrayNum(len(centroids))
	
	for i in range(len(lista)):
		for j in range(len(dist)):
			dist[j] = distancia(lista[i][0], lista[i][1], centroids[j][0], centroids[j][1])
		
		value = indexMenorDist(dist)
		lista[i][2] = value

	return lista

def printResult(data, medoids, num):
	
	colors, makers = colorsMakers(num)
	
	for i in range(len(data)):
		for j in range(len(medoids)):
			if(data[i][2] == j+1):
				plt.plot(data[i][0], data[i][1], colors[j]+makers[j])


	for i in range(len(medoids)):
	 	plt.plot(medoids[i][0], medoids[i][1], 'ko')

	plt.show()	

def main():
	flag = int(sys.argv[3])
	centroids = []

	num = int(sys.argv[2])
	data = leitor(sys.argv[1], num)
	centroids = startArrayNum(num)

	time_begin = datetime.datetime.now()
	# Roda dependendo do numero de iteraçẽos
	while(flag > 0):
		
		#For para recalcular o centroid baseado nos seus pontos K
		for i in range(len(centroids)):
			aux = calCentroids(data, i+1)

			if(aux != centroids[i]):
				centroids[i] = aux
				flag -= 1
		# Função para atualizar o K dos pontos baseado no seu centroid atualizado
		data = recalK(data, centroids)

	time_end = datetime.datetime.now()
	time_diff = (time_end - time_begin)
	time_diff_seconds = time_diff.seconds + (time_diff.microseconds/1000000.0)

	file = open('results/'+str(sys.argv[1])+'_saida.txt', 'a+')
	saida = 'k '+str(num)+' '+str(time_diff_seconds)
	file.write(saida+'\n') 

	printResult(data, centroids, num)

if __name__ == '__main__':
	main()