package algoritmos;
import java.util.*;

public class Grafos{

    static List<List<Integer>> adj;
    static int numVertices;

    public static void addArista(int origen, int destino){
        List<Integer> aristas = adj.get(origen);
        aristas.add(destino);
        adj.set(origen, aristas);
    }

    public static void mostrarGrafo(){
        for(int i=0; i<adj.size(); i++){
            System.out.print("Vertice: " + i + ":");
            for(Integer adyacente: adj.get((i))){
                System.out.print(" -> " + adyacente);
            }
            System.out.println();
        }
    }

    public static void bfs(int start){
        int[] visited = new int[adj.size()];
        for(int i=0; i<visited.length; i++){
            visited[i] = 0;
        }

        Queue<Integer> queue = new LinkedList<>();
        queue.add(start);
        visited[start] = 1;

        while(!queue.isEmpty()){
            int now = queue.poll();
            System.out.println("Visited: " + now);
            for(int adyacente: adj.get(now)){
                if(visited[adyacente] == 0){
                    queue.add(adyacente);
                    visited[adyacente] = 1;
                }
            }
        }
    }

    public static void dfs(int start){
        System.out.println("DFS: ");
        int[] visited = new int[adj.size()];
        visited[start] = 1;
        _dfs(start, visited);
    }

    public static void _dfs(int start, int[] visited){
        visited[start] = 1;
        for(int i=0; i<adj.get(start).size(); i++ ){
            int ady = adj.get(start).get(i);
            System.out.println("Visitando: " + ady);
            if(visited[ady] != 1){
                System.out.println("No estaba visitado, ahora me estoy moviendo");
                _dfs(ady, visited);
            }
        }
    }

    public static boolean cyclic(int node, int[] visited){
        visited[node] = 1;

        for(int i=0; i<adj.get(node).size(); i++ ){
            int ady = adj.get(node).get(i);

            if(visited[ady] == 1){
                return true; 
            }
            
            if(visited[ady] == 0){
                System.out.println("No estaba visitado, ahora me estoy moviendo");
                if(cyclic(ady, visited)){
                    return true; 
                }
            }
        }
        visited[node] = 2;
        return false;
    }
    public static void main(String[] args) {
        System.out.println("Hola mundo");
        int numVertices = 5;
        adj = new ArrayList<>(numVertices);
        for (int i=0; i<numVertices; i++){
            adj.add(new ArrayList<>());
        }

        addArista(0, 1);
        addArista(0, 4);
        addArista(1, 2);
        addArista(1, 3);
        addArista(1, 4);
        addArista(2, 3);
        addArista(2, 0);
        addArista(3, 4);

        // Mostrar el grafo
        mostrarGrafo();
        bfs(0);
        dfs(0);
        System.out.println("Viendo si es cíclico");
        int[] visited = new int[adj.size()];
        boolean isCyclic = false;
        for(int i=0; i<adj.size(); i++){
            if(visited[i] != 2){
                if(cyclic(i, visited)){
                    isCyclic = true;
                    break;
                }
            }

        }
        System.out.println(isCyclic + " Es ciclico ");
    }
}