package algoritmos;
import java.util.*;

public class Flujos {
    static class Graph {
        private int[][] adjMatrix;
        private int size;

        public Graph(int size){
            this.size = size;
            this.adjMatrix = new int[size][size];
        }

        public void addEdge(int a, int b, int capacity){
            adjMatrix[a][b] = capacity;
        }
        private List<Integer> bfs(int s, int t, boolean[] visited){
            Queue<Integer> queue = new LinkedList<>();
            int[] parents = new int[size];
            Arrays.fill(parents, -1);
            Integer actual;
            queue.add(s);
            visited[s] = true;

            while((actual = queue.poll()) != null){
                for(int i=0; i<size; i++){
                    if(adjMatrix[actual][i] > 0 && !visited[i]){
                        parents[i] = actual;
                        visited[i] = true;
                        queue.add(i);
                        if(i == t){
                            List<Integer> path = new ArrayList<>();
                            int currentNode = t;
                            while(currentNode != -1){
                                path.add(0, currentNode);
                                currentNode = parents[currentNode];
                            }
                            return path;
                        }
                    }
                }
            }
            return null;
        }

        private List<Integer> dfs(int s, int t, boolean[] visited){
            if(s == t){
                List<Integer> path = new ArrayList<>();
                path.add(s);
                return path;
            }
            for(int i=0; i<size; i ++){
                if(!visited[i] && adjMatrix[s][i] > 0){
                    visited[i] = true;
                    List<Integer> subpath = dfs(i, t, visited);
                    if(subpath != null){
                        subpath.add(0,s);
                        return subpath;
                    }

                }
            }
            return null;
        }

        public int fordFulkersonDfs(int source, int sink){
            int maxFlow = 0;
            List<Integer>  path;
            while((path = dfs(source, sink, new boolean[size])) != null){
                int pathFlow = Integer.MAX_VALUE;
                int pathSize = path.size();
                // Buscamos el mínimo del path encontrado
                for(int i=0; i<pathSize-1; i++){
                    int s = path.get(i);
                    int t = path.get(i+1);
                    if(pathFlow > adjMatrix[s][t]){
                        pathFlow = adjMatrix[s][t];
                    }
                }
                // del flujo mínimo, quitamos la capacidad ocupada en nuestro grafo de flujos y añadimos el vértice inverso.
                for(int i=0; i<pathSize-1; i++){
                    int s = path.get(i);
                    int t = path.get(i+1);
                    adjMatrix[s][t] = adjMatrix[s][t] - pathFlow;
                    adjMatrix[t][s] = adjMatrix[t][s] + pathFlow;
                }
                maxFlow += pathFlow;
            }
            return maxFlow;
        }
        public int fordFulkersonBfs(int source, int sink){
            int maxFlow = 0;
            List<Integer>  path;
            while((path = bfs(source, sink, new boolean[size])) != null){
                int pathFlow = Integer.MAX_VALUE;
                int pathSize = path.size();
                // Buscamos el mínimo del path encontrado
                for(int i=0; i<pathSize-1; i++){
                    int s = path.get(i);
                    int t = path.get(i+1);
                    if(pathFlow > adjMatrix[s][t]){
                        pathFlow = adjMatrix[s][t];
                    }
                }
                // del flujo mínimo, quitamos la capacidad ocupada en nuestro grafo de flujos y añadimos el vértice inverso.
                for(int i=0; i<pathSize-1; i++){
                    int s = path.get(i);
                    int t = path.get(i+1);
                    adjMatrix[s][t] = adjMatrix[s][t] - pathFlow;
                    adjMatrix[t][s] = adjMatrix[t][s] + pathFlow;
                }
                maxFlow += pathFlow;
            }
            return maxFlow;
        }
    }


    

    public static void main(String[] args) {
        Graph g = new Graph(6);
        g.addEdge(0, 1, 3);
        g.addEdge(0, 2, 7);
        g.addEdge(1, 3, 3);
        g.addEdge(1, 4, 4);
        g.addEdge(2, 1, 5);
        g.addEdge(2, 4, 3);
        g.addEdge(3, 4, 3);
        g.addEdge(3, 5, 2);
        g.addEdge(4, 5, 6);
        int source = 0, sink = 5;
        int maxFlow = g.fordFulkersonDfs(source, sink);
        System.out.println("El flujo máximo posible es: " + maxFlow);

        
    }

}
