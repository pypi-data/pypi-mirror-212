import matplotlib.pyplot as plt
import numpy as np


class EvaluateExperiments:
    def __init__(self, metrics):
        """
        Construtor EvaluateExperiments.

        :param metrics: As métricas de avaliação dos clusters.
        :type metrics: list
        """
        self.metrics = metrics
        self.inertias = [metric["inertia"] for metric in self.metrics]
        self.silhouette_scores = [metric["silhouette_score"] for metric in self.metrics]
        self.num_clusters = [metric["num_clusters"] for metric in self.metrics]

    def get_elbow(self, line_coefficients=False):
        """
        Calcula os valores do método do cotovelopara determinar o número ideal de clusters.

        :param line_coefficients: Indica se os coeficientes da reta devem ser retornados, defaults para False.
        :type returnA: bool, optional
        :return: Os valores do método do cotovelo ou os coeficientes da reta, dependendo do parâmetro line_coefficients.
        :rtype: list ou tuple
        """  # noqa: E501

        slope = (self.inertias[-1] - self.inertias[0]) / (self.num_clusters[-1] - self.num_clusters[0])
        b = [y - slope * x for x, y in zip(self.num_clusters, self.inertias)]
        if line_coefficients:
            return slope, b
        else:
            return b

    def get_elbow_chart(self):
        """
        Plota o gráfico do método do cotovelo para determinar o número ideal de clusters.

        :return: O objeto matplotlib.pyplot com o gráfico do método do cotovelo.
        :rtype: matplotlib.pyplot.Figure
        """
        plt.switch_backend("Agg")
        fig, ax = plt.subplots()
        ax.grid(True)

        a, b = self.get_elbow(line_coefficients=True)
        min_i = np.argmin(b)
        min_b = self.inertias[min_i]

        ax.plot(self.num_clusters, self.inertias, marker="o")
        ax.plot([self.num_clusters[min_i]], [min_b], marker="*", ls="none", ms=20)

        ax.set_title("Método do cotovelo.")
        ax.set_xlabel("Quantidade de clusters")
        ax.set_ylabel("Inércia")
        ax.set_xticks(self.num_clusters)

        return fig

    def get_silhouette_chart(self):
        """
        Plota o gráfico do índice de silhueta

        para determinar o número ideal de clusters.
        :return: O objeto matplotlib.pyplot
        com o gráfico do índice de silhueta.
        :rtype: matplotlib.pyplot.Figure
        """
        plt.switch_backend("Agg")  # backend adequado para execução em ambiente concorrente
        fig, ax = plt.subplots()
        ax.grid(True)

        ax.plot(self.num_clusters, self.silhouette_scores, marker="o")

        ax.set_title("Índice de Silhueta.")
        ax.set_xlabel("Número de Clusters")
        ax.set_ylabel("Índice de Silhueta")
        ax.set_xticks(self.num_clusters)

        return fig

    def get_charts(self):
        """Retorna lista de dicionarios contendo o grafico e sua etiqueta

        :return: Lista com gŕaficos para armazenar no mlflow
        :rtype: list[dict(str,fig|str)]
        """
        return [
            {"figure": self.get_elbow_chart(), "name": "elbowChart.png"},
            {"figure": self.get_silhouette_chart(), "name": "silhouetteChart.png"},
        ]

    def get_best_k(self):
        """Retorna o k (numero de clusters) ótimo segundo o método do cotovelo

        :return: valor do k
        :rtype: int
        """
        a, b = self.get_elbow(line_coefficients=True)
        # line eq: #y=ax+b
        # quando x = 0, y=b
        # estamos interessados no b mínimo

        k = self.num_clusters[np.argmin(b)]
        return k

    def get_metrics(self, metrics=["best_k"]):
        """Retorna as métricas necessárias para avaliar um conjunto de modelos

        :param metrics: Métricas que deseja coletar juntos, defaults to ["best_k"]
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
