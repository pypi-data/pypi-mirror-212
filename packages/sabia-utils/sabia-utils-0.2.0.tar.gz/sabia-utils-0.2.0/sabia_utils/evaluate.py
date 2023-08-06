from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import (calinski_harabasz_score, davies_bouldin_score,
                             pairwise_distances, silhouette_score)


def convertion_to_array(emb):
    """Converte a matriz de embeddings para um array numpy

    :param emb: matriz de embeddings
    :type emb: numpy.array|scipy.sparse.csr.csr_matrix
    :return: matriz de embeddings convertida
    :rtype: numpy.array
    """
    if isinstance(emb, np.ndarray):
        return emb
    else:
        try:
            return emb.toarray()
        except Exception:
            raise Exception("O tipo da matriz de embeddings não é suportado.")


class Evaluate:
    def __init__(self, labels, emb):
        """
        Construtor Evaluate.

        :param labels: Os rótulos das amostras.
        :type labels: list ou numpy.array
        :param emb: As embeddings das amostras.
        :type emb: numpy.array
        """
        self.emb = emb
        self.labels = labels
        self.num_samples = len(self.labels)
        self.groups_indexes = np.unique(self.labels)
        self.n_clusters = len(self.groups_indexes)
        self.idx_dict = []
        self.centroides = []
        self.inertias = []
        self.cluster_samples = []
        self.inner_distances = None
        self.size_of_clusters = None
        for g in self.groups_indexes:
            d = {"grupo": g, "indexes": [id for id, v in enumerate(self.labels) if g == v]}
            self.idx_dict.append(d)

    def get_silhouette_score(self):
        """
        Calcula o índice de silhueta para as amostras.

        :return: O valor do índice de silhueta.
        :rtype: float
        """

        return silhouette_score(self.emb, self.labels)

    def get_sizes_of_clusters(self):
        """
        Calcula os tamanhos dos clusters.

        :return: Uma lista com os tamanhos dos clusters.
        :rtype: list
        """

        if not self.size_of_clusters:
            counter = Counter(self.labels)
            size_of_clusters = [counter[i] for i in self.groups_indexes]
            self.size_of_clusters = size_of_clusters

        return self.size_of_clusters

    def get_centroides(self):
        """
        Calcula os centroides dos clusters.

        :return: Os centroides dos clusters.
        :rtype: numpy.array
        """

        assert self.num_samples == self.emb.shape[0]
        if len(self.centroides) == 0:
            centroides = []
            for d in self.idx_dict:
                centroide = np.mean(self.emb[d["indexes"], :], axis=0)
                centroides.append(centroide)
            self.centroides = np.squeeze(np.asarray(centroides))

        return self.centroides

    def get_inertias(self):
        """
        Calcula as inércias dos clusters.

        :return: Uma lista com as inércias dos clusters.
        :rtype: list
        """

        if len(self.centroides) == 0:
            self.get_centroides()
        assert self.num_samples == self.emb.shape[0]
        assert self.n_clusters == self.centroides.shape[0]
        if not self.inertias:
            inertias = []

            for i, d in enumerate(self.idx_dict):
                ssd = []

                for j in range(self.emb[d["indexes"]].shape[0]):
                    diff = self.emb[d["indexes"]][j, :] - self.centroides[i]
                    ssd.append(np.inner(diff, diff))

                inertias.append(np.sum(ssd))

            self.inertias = inertias

        return self.inertias

    def get_inertia(self):
        """
        Calcula a inércia total dos clusters.

        :return: O valor da inércia total.
        :rtype: float
        """

        if not self.inertias:
            self.get_inertias()
        self.inertia = sum(self.inertias)
        return self.inertia

    # Distancia media dos elementos dos grupos
    def get_inner_distances(self):
        """
        Calcula as distâncias médias dentro dos clusters.

        :return: Uma lista com as distâncias médias dentro dos clusters.
        :rtype: list
        """

        if not self.inner_distances:
            inner_distances = []

            for i, d in enumerate(self.idx_dict):
                distances = pairwise_distances(self.emb[d["indexes"], :], metric="euclidean")
                inner_distances.append(np.mean(distances))

            self.inner_distances = inner_distances

        return inner_distances

    def get_cluster_distance_avg(self):
        """
        Calcula a distância média dos elementos
        até o centroide de cada cluster.

        :return: O valor da distância média dos elementos até o centroide.
        :rtype: float
        """

        if len(self.centroides) == 0:
            self.get_centroides()
        distancias_pontos_centroides = pairwise_distances(self.emb, self.centroides)

        distancia_media_grupo = []

        for i in range(self.n_clusters):
            group_indexes = np.where(self.labels == i)[0]

            if len(group_indexes) > 0:
                distancia_media_grupo.append(np.mean(distancias_pontos_centroides[group_indexes, i]))
            else:
                distancia_media_grupo.append(np.nan)

        self.cluster_distance_avg = np.nanmean(distancia_media_grupo)

        return self.cluster_distance_avg

    def get_outer_distance(self):
        """
        Calcula a distância média entre os centroides dos clusters.

        :return: A matriz de distâncias entre os centroides.
        :rtype: numpy.array
        """

        if len(self.centroides) == 0:
            self.get_centroides()
        assert self.n_clusters == len(self.centroides)

        outer_distance = pairwise_distances(self.centroides)

        self.outer_distance = np.mean(outer_distance)

        return outer_distance

    def get_calinski_harabasz(self):
        """
        Calcula o índice de Calinski-Harabasz para a avaliação dos clusters.

        :return: O valor do índice de Calinski-Harabasz.
        :rtype: float
        """

        self.calinski_harabasz = calinski_harabasz_score(convertion_to_array(self.emb), self.labels)
        return self.calinski_harabasz

    def get_davies_bouldin(self):
        """
        Calcula o índice de Davies-Bouldin para a avaliação dos clusters.

        :return: O valor do índice de Davies-Bouldin.
        :rtype: float
        """

        self.davies_bouldin = davies_bouldin_score(convertion_to_array(self.emb), self.labels)
        return self.davies_bouldin

    def get_metrics(
        self, metrics=["inertia", "silhouette_score", "calinski_harabasz", "davies_bouldin", "outer_distance"]
    ):
        """Retorna as métricas necessárias para avaliar o treinamento.

        :param metrics: Métricas que deseja coletar juntos, defaults to ["inertia", "silhouette_score", "calinski_harabasz","davies_bouldin", "outer_distance"]
        :type metrics: list, optional
        :return: dicionário contrento nome da métrica e o seu valor
        :rtype: dict
        :raises Exception: Exeção disparada quando recebe uma métrica que não existe na classe
        """  # noqa: E501
        dict_metrics = {}
        for metric in metrics:
            get_metric = f"get_{metric}"
            if hasattr(self, get_metric) and callable(getattr(self, get_metric)):
                dict_metrics.update({metric: getattr(self, get_metric)()})
            else:
                raise Exception(f"Metric {metric} invalid or not implemented")
        self.metrics = dict_metrics
        return self.metrics

    def get_inertias_chart(self):
        """
        Plota o gráfico da inercia de cada cluster.

        :return: O objeto matplotlib.pyplot com o gráfico do índice de silhueta.
        :rtype: matplotlib.pyplot.Figure
        """
        if not self.inertias:
            self.get_inertias()
        # Define o backend adequado para execução em ambiente concorrente
        plt.switch_backend("Agg")
        fig, ax = plt.subplots()
        ax.grid(True)

        num_clusters = np.arange(0, self.n_clusters)

        ax.bar(num_clusters, self.inertias)
        ax.set_title("Inercia dos Clusteres")
        ax.set_xlabel("Índice do Cluster")
        ax.set_ylabel("Inercia")
        ax.set_xticks(num_clusters)

        return fig

    def get_inner_distances_chart(self):
        """
        Plota o gráfico da distância média emtre elementos dos clusters.

        :return: O objeto matplotlib.pyplot com o gráfico do índice de silhueta.
        :rtype: matplotlib.pyplot.Figure
        """

        if not self.inner_distances:
            self.get_inner_distances()

        # Define o backend adequado para execução em ambiente concorrente
        plt.switch_backend("Agg")

        num_clusters = np.arange(0, self.n_clusters)

        fig, ax = plt.subplots()
        ax.grid(True)

        ax.bar(num_clusters, self.inner_distances)
        ax.set_title("Distância média entre elementos dos clusters.")
        ax.set_xlabel("Índice do Cluster")
        ax.set_ylabel("Distância média entre elementos do cluster")
        ax.set_xticks(num_clusters)

        return fig

    def get_charts(self, charts=["inertias", "inner_distances", "num_samples"]):
        """Retorna dicionario com os gráficos de avaliação individual do modelo

        :param charts: Gráficos que deseja coletar juntos, defaults to ["inertias", "inner_distances", "num_samples"]
        :return: Lista com gŕaficos para armazenar no mlflow
        :rtype: list[dict(str,fig|str)]
        """

        charts_return = list()

        for chart in charts:
            get_chart = f"get_{chart}_chart"
            if hasattr(self, get_chart) and callable(getattr(self, get_chart)):
                charts_return.append({"name": f"{chart}.png", "figure": getattr(self, get_chart)()})
            else:
                raise Exception(f"Chart {chart} invalid or not implemented")

        return charts_return

    def get_num_samples(self):
        """
        Obtém o número de amostras de cada cluster.

        :return: Lista com o número de amostras de cada cluster.
        :rtype: list
        """
        if not self.cluster_samples:
            self.cluster_samples = [len(g["indexes"]) for g in self.idx_dict]

        return self.cluster_samples

    def get_num_samples_chart(self):
        """
        Plota o boxplot do número de amostras de cada cluster.

        :return: O objeto matplotlib.pyplot do boxplot.
        :rtype: matplotlib.pyplot.Figure
        """
        if not self.cluster_samples:
            self.get_num_samples()

        plt.switch_backend("Agg")
        fig, ax = plt.subplots()

        # num_clusters = np.arange(0, self.n_clusters)
        ax.boxplot(self.cluster_samples)
        # ax.set_xticklabels(num_clusters)

        ax.set_title("Intervalo de número de amostras por cluster")
        ax.set_xlabel("Quantidade de clusters")
        ax.set_ylabel("Número de amostras por cluster")

        return fig
