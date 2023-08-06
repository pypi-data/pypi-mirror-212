from typing import Any, Dict, Generator, Iterable, List, Tuple

import networkx as nx
from matplotlib import pyplot as plt

from amora.config import settings
from amora.materialization import Task
from amora.models import Column, Model, list_models
from amora.utils import list_target_files

CytoscapeElements = List[Dict]


class DependencyDAG(nx.DiGraph):
    def __iter__(self):
        return nx.topological_sort(self)

    @classmethod
    def from_model(cls, model: Model) -> "DependencyDAG":
        """
        Builds the DependencyDAG for a given data model
        """
        dag = cls()
        dag.add_node(model.unique_name())

        def fetch_edges(node: Model):
            for dependency in getattr(node, "__depends_on__", []):
                dag.add_edge(dependency.unique_name(), node.unique_name())
                fetch_edges(dependency)

        fetch_edges(model)
        return dag

    @classmethod
    def from_project(cls) -> "DependencyDAG":
        """
        Builds the DependencyDAG for all models.
        """
        dag = cls()

        def fetch_edges(node: Model):
            for dependency in getattr(node, "__depends_on__", []):
                dag.add_edge(dependency.unique_name(), node.unique_name())
                fetch_edges(dependency)

        for model, _ in list_models():
            dag.add_node(model.unique_name())
            fetch_edges(model)

        return dag

    @classmethod
    def from_tasks(cls, tasks: Iterable[Task]) -> "DependencyDAG":
        dag = cls()

        for task in tasks:
            dag.add_node(task.model.unique_name())
            for dependency in task.model.dependencies():
                dag.add_edge(dependency.fullname, task.model.unique_name())

        return dag

    @classmethod
    def from_target(cls) -> "DependencyDAG":
        """
        Builds a DependencyDAG from the files compiled at `settings.AMORA_TARGET_PATH`
        """
        model_to_task = {}

        for target_file_path in list_target_files():
            task = Task.for_target(target_file_path)
            model_to_task[task.model.unique_name()] = task

        return cls.from_tasks(tasks=model_to_task.values())

    @classmethod
    def from_columns(cls, columns: List[Tuple[Model, Column]]) -> "DependencyDAG":
        dag = cls()

        for model, column in columns:
            dag.add_node(column)
            for dependency in getattr(model, "__depends_on__", []):
                dependency_columns = dependency.__table__.columns
                if column.key in dependency_columns:
                    dag.add_edge(dependency_columns[column.key], column)

        return dag

    def topological_generations(self) -> Generator[List[Any], None, None]:
        for generation in nx.topological_generations(self):
            yield sorted(generation)

    def get_all_dependencies(self, source: Any) -> Generator[Any, None, None]:
        for dep in nx.predecessor(self, source=source):
            if dep != source:
                yield dep

    def to_cytoscape_elements(self) -> CytoscapeElements:
        """

        Returns itself as a cytoscape schema compatible representation. E.g:

        For a `A --> B` graph:

        ```python
        [
            {"data": {"id": "A", "label": "A"}},
            {"data": {"id": "B", "label": "B"}},
            {"data": {"source": "A", "target": "B"}},
        ]
        ```
        """

        return [
            *(
                {"group": "nodes", "data": {"id": node, "label": node}}
                for node in self.nodes
            ),
            *(
                {"group": "edges", "data": {"source": source, "target": target}}
                for source, target in self.edges
            ),
        ]

    def draw(self) -> None:
        plt.figure(1, figsize=settings.CLI_MATERIALIZATION_DAG_FIGURE_SIZE)
        nx.draw(
            self,
            with_labels=True,
            font_weight="bold",
            font_size="12",
            linewidths=4,
            node_size=150,
            node_color="white",
            font_color="green",
        )
        plt.show()

    def root(self):
        sorted_elements = list(self)
        if not sorted_elements:
            return None
        return sorted_elements[0]
