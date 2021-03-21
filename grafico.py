import matplotlib.pyplot as plt
import seaborn as sns
import numpy
import os
import sys

def readfile(file):
	
	file = open('results/'+file+'_saida.txt', 'r')

	listaTipo = []
	listaCluster = []
	listaTempo = []
	

	for line in file:
		tipo, clust, tp = line.split(' ') 
		clust = int(clust)
		tp = float(tp)
		
		listaTipo.append(tipo)
		listaCluster.append(clust)
		listaTempo.append(tp)
			

	return listaTipo, listaCluster, listaTempo

def main():
	
	sns.set_theme(style="whitegrid")
	sns.set_palette('bright')

	listaTipo = []
	listaCluster = []
	listaTempo = []

	listaTipo, listaCluster, listaTempo = readfile(sys.argv[1])
	sns.pointplot(x=listaCluster, y=listaTempo, hue=listaTipo, palette='Paired', capsize=.1)	

	plt.title('Grafico dataset '+sys.argv[1])
	plt.xlabel('Numero de Clusters')
	plt.ylabel('Tempo execução (segundos)')
	plt.legend(title='Algoritimo')
	# plt.yticks(np.arange(0, 1.1, step=0.1))
	plt.show()

if __name__ == '__main__':
	main()