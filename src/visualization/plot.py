import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rc('xtick', labelsize=1)
matplotlib.rc('ytick', labelsize=1)
matplotlib.rc('axes', titlesize=1)
matplotlib.rc('axes', labelsize=1)

class Plot:
    def __init__(self, analysis):
        self.user = analysis.author
        self.analysis = analysis

    def plot_problems(self):
        labels = ['Saudavel', 'Ardido&Mofado', 'Bandinha', 'Carunchado', 
                  'Contaminantes', 'Genetico', 'Imaturo', 'Manchado', 'Mordido']
        values = [self.analysis.saudavel, self.analysis.ardido, self.analysis.bandinha, self.analysis.caruncho, self.analysis.contaminantes,
                  self.analysis.genetico, self.analysis.imaturo, self.analysis.manchado, self.analysis.mordido]
        filtered_values, filtered_labels = self.remove_zeros(values, labels)
        sns.set(style="darkgrid")
        rs = np.random.RandomState(8)
        sns.barplot(x=filtered_labels, y=filtered_values, palette="rocket")
        plt.ylabel("Quantidade (%)")
        plt.title('Qualidade e Problemas nos Grãos')
        plt.tick_params(axis='x', labelsize=8, rotation=20)
        plt.savefig('data/client/{0}/{1}/plots/problem.png'.format(self.user.id, self.analysis.id), transparence=False)
        plt.clf()

    def plot_geometric(self):
        geometric_labels = ['Peneira-12', 'Peneira-11', 'Peneira-10', 'Peneira-9','Imaturo']
        geometric_values = [self.analysis.size_12, self.analysis.size_11, self.analysis.size_10, self.analysis.size_9, self.analysis.imaturo]
        filtered_values, filtered_labels = self.remove_zeros(geometric_values, geometric_labels)
        sns.set(style="darkgrid")
        rs = np.random.RandomState(8)
        sns.barplot(x=filtered_labels, y=filtered_values, palette="rocket")
        plt.ylabel("Quantidade (%)")
        plt.title('Qualidade Geometrica nos Grãos')
        plt.tick_params(axis='x', labelsize=8, rotation=20)
        plt.savefig('data/client/{0}/{1}/plots/geometric.png'.format(self.user.id, self.analysis.id), transparence=False)
        plt.clf()

    def remove_zeros(self, values, labels):
        filtered_values, filtered_labels = [], []
        for i in range(len(values)):
            if values[i] != 0:
                filtered_labels.append(labels[i])
                filtered_values.append(values[i])
        return filtered_values, filtered_labels            