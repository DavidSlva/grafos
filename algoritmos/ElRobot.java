package algoritmos;
import java.util.*;

class Graph {
    int nodes;
    List<List<Integer>> adjacencyList;

    public Graph(int nodes) {
        this.nodes = nodes;
        adjacencyList = new ArrayList<>(nodes);
        for (int i = 0; i < nodes; i++) {
            adjacencyList.add(new ArrayList<>());
        }
    }

    public void addEdge(int u, int v) {
        adjacencyList.get(u).add(v);
        adjacencyList.get(v).add(u);  // Since it's an undirected graph
    }

    public List<Integer> getNeighbors(int node) {
        return adjacencyList.get(node);
    }

    public boolean isInterferenceFreePath(int start1, int start2, int end1, int end2, int r) {
        // Build the graph H' as described
        Queue<int[]> queue = new LinkedList<>();
        Set<String> visited = new HashSet<>();
        queue.add(new int[]{start1, start2});
        visited.add(start1 + "-" + start2);
        while (!queue.isEmpty()) {
            int[] config = queue.poll();
            int node1 = config[0], node2 = config[1];
            if (node1 == end1 && node2 == end2) {
                return true;
            }

            // Movemos el nodo 1 hacia sus caminos posibles si su distancia entre ellos es mayor a r
            for (int neig : getNeighbors(node1)) {
                if (!visited.contains(neig + "-" + node2) && distance(neig, node2) > r) {
                    visited.add(neig + "-" + node2);
                    queue.add(new int[]{neig, node2});
                }
            }
            // Movemos el nodo 2 hacia sus caminos posibles si su distancia entre ellos es mayor a r
            for (int neig : getNeighbors(node2)) {
                if (!visited.contains(node1 + "-" + neig) && distance(node1, neig) > r) {
                    visited.add(node1 + "-" + neig);
                    queue.add(new int[]{node1, neig});
                }
            }
        }
        return false;
    }

    // Method to compute the shortest path (BFS) distance between two nodes
    private int distance(int u, int v) {
        Queue<int[]> queue = new LinkedList<>();
        Set<Integer> visited = new HashSet<>();
        queue.add(new int[]{u, 0});
        visited.add(u);
        if (u == v) {
            return 0;
        }
        while (!queue.isEmpty()) {
            int[] config = queue.poll();
            int node = config[0], dist = config[1];
            for (int neig : getNeighbors(node)) {
                if (neig == v) {
                    return dist + 1;
                }
                if (!visited.contains(neig)) {
                    queue.add(new int[]{neig, dist + 1});
                    visited.add(neig);  // Asegúrate de agregar el nodo visitado
                }
            }
        }
        return Integer.MAX_VALUE;
    }
}

public class ElRobot {
    public static void main(String[] args) {
        // Create the graph for the building (example with 6 nodes)
        Graph graph = new Graph(6);

        // Adding edges
        graph.addEdge(0, 1);  // Node 0 is connected to node 1
        graph.addEdge(1, 2);  // Node 1 is connected to node 2
        graph.addEdge(1, 3);  // Node 1 is connected to node 3
        graph.addEdge(2, 4);  // Node 2 is connected to node 4
        graph.addEdge(3, 5);  // Node 3 is connected to node 5

        // Define start and end positions for two robots
        int startRobot1 = 0;
        int startRobot2 = 3;
        int endRobot1 = 4;
        int endRobot2 = 5;

        // Distance threshold for interference
        int interferenceDistance = 1;

        // Check if there is an interference-free path
        boolean result = graph.isInterferenceFreePath(startRobot1, startRobot2, endRobot1, endRobot2, interferenceDistance);
        if (result) {
            System.out.println("There is an interference-free path.");
        } else {
            System.out.println("No interference-free path exists.");
        }
    }
}
