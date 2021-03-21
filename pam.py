import sys
import random
import math
import matplotlib.pyplot as plt
import datetime

#	Autor: Jian Furquim
#   furquimjian@gmail.com
#	
#	Algoritimo PAM dinamico
#
#	Roda
#		$ python3 pam.py data.dat 3 7
#		
# 		Sendo o parametro 2 o arquivo com os pontos "data.dat"
#		E o parametro 3 o numero de clusters que deseja usar (no exemplo está sendo usado 3)
#		E o parametro 7 é o numero de iteraçãos
#
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

def distance(x1, y1, x2, y2):
	return float(math.sqrt((x1 - x2)**2 + (y1 - y2)**2))

# Função para ler os dados do arquivo e gerar um K aleatório
def leitor(arquivo, num):
	file = open(arquivo, 'r')
	data  = []

	for line in file:
		a, b = line.split()
		data.append([float(a), float(b), random.randint(1 , num)])

	return data

# Função para criar um arrey de tamanho num com todos elementos zeros 
def startArrayNum(num):
	dist = []
	for i in range(num):
		dist.append(0)

	return dist

def startMedoids(medoids, ponto):
	
	medoids.append([ponto[0], ponto[1], 0])

	return medoids

def calCost(data, ponto, k):
	cost = 0.0
	for i in range(len(data)):
		if(k == data[i][2]):
			cost += distance(data[i][0], data[i][1], ponto[0], ponto[1])
	return cost

def indexMenorDist(dist):
	tempdist = dist[0]
	index = 1
	for i in range(len(dist)):
		if(dist[i] < tempdist):
			tempdist = dist[i]
			index = i+1
	return index

def recalK(data, medoids):
	
	dist = startArrayNum(len(medoids))
	
	for i in range(len(data)):
		for j in range(len(medoids)):
			dist[j] = distance(data[i][0], data[i][1], medoids[j][0], medoids[j][1])
		
		index = indexMenorDist(dist)
		data[i][2] = index

	return data

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

	medoids = []
	num = int(sys.argv[2])
	data = leitor(sys.argv[1], num)

	flagReplace = startArrayNum(num)

	for i in range(num):
		medoids = startMedoids(medoids, data[random.randint(0 , len(data)-1)])

	time_begin = datetime.datetime.now()
	
	# Função para atualizar o K dos pontos baseado no seu medoids atualizado
	data = recalK(data, medoids)

	for i in range(len(medoids)):
		medoids[i][2] = calCost(data, medoids[i], i+1)
	

	itera = int(sys.argv[3])
	j = 0
	while(j < len(medoids)):
		flag = False
		i = 0

		#While para recalcular o medoid baseado na distancia euclidiana
		while(i < len(data) and flagReplace[j] < itera):
			aux = calCost(data, data[i], j+1)

			if(aux < medoids[j][2]):
				medoids[j][0] = data[i][0]
				medoids[j][1] = data[i][1]
				medoids[j][2] = aux
				flagReplace[j] += 1
				i = 0
				j = 0
				flag = True
				# Função para atualizar o K dos pontos baseado no seu medoids atualizado
				data = recalK(data, medoids)
			i += 1
		if(flag == False):
			j += 1

	time_end = datetime.datetime.now()
	time_diff = (time_end - time_begin)
	time_diff_seconds = time_diff.seconds + (time_diff.microseconds/1000000.0)

	file = open('results/'+str(sys.argv[1])+'_saida.txt', 'a+')
	saida = 'p '+str(num)+' '+str(time_diff_seconds)
	file.write(saida+'\n') 

	printResult(data, medoids, num)


if __name__ == '__main__':
	main()