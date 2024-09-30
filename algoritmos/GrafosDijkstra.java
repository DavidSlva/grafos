package algoritmos;

import java.util.ArrayList;
import java.util.List;

public class GrafosDijkstra {
    
    // Clase para representar una arista con destino y peso
    static class Arista {
        int destino, peso;

        public Arista(int destino, int peso) {
            this.destino = destino;
            this.peso = peso;
        }
    }

    // Lista de adyacencia para representar el grafo
    static List<List<Arista>> adj;
    static int numVertices;

    // Método para inicializar el grafo con n vértices
    public static void inicializarGrafo(int vertices) {
        numVertices = vertices;
        adj = new ArrayList<>();
        for (int i = 0; i < vertices; i++) {
            adj.add(new ArrayList<>());  // Inicializamos la lista de adyacencia para cada nodo
        }
    }

    // Método para agregar aristas
    public static void agregarArista(int origen, int destino, int peso) {
        adj.get(origen).add(new Arista(destino, peso));
    }

    // Método para mostrar el grafo
    public static void mostrarGrafo() {
        for (int i = 0; i < adj.size(); i++) {
            System.out.print("Nodo " + i + ":");
            for (Arista arista : adj.get(i)) {
                System.out.print(" -> " + arista.destino + "(peso " + arista.peso + ")");
            }
            System.out.println();
        }
    }

   public static void dijkstra(int origen, int destino){
        boolean[] visited = new boolean[adj.size()]; 
        int[] pesos = new int[adj.size()];

        for(int i=0; i<pesos.length; i++){
            pesos[i] = Integer.MAX_VALUE;
        }
        pesos[origen] = 0;
        for(int i=0; i<visited.length; i++){
            int min = Integer.MAX_VALUE;
            int minIndex = -1;
            for(int j=0; j<pesos.length; j++){
                if(!visited[j] && min > pesos[j]){
                    min = pesos[j];
                    minIndex = j;
                }
            }
            if(minIndex == -1){
                break;
            }
            visited[minIndex] = true;
            if(minIndex == destino){
                System.out.println("Encontramos el destino");
                imprimirSolucion(pesos);
                return;
            }
            for(Arista ady : adj.get(minIndex)){
                if(!visited[ady.destino] && pesos[minIndex] + ady.peso < pesos[ady.destino]){
                    pesos[ady.destino] = pesos[minIndex] + ady.peso;
                }
            }

        }
        if(pesos[destino] == Integer.MAX_VALUE){
            System.out.println("No se encontró solución");
        }else{
            imprimirSolucion(pesos);
        }
   }

   public static void floydWarshall(){
        int aristas = adj.size();
        int[][] distancias = new int[aristas][aristas];
        for(int i=0; i<aristas; i++){
            for (int j=0; j<aristas; j++){
                distancias[i][j] = (i==j) ? 0 : Integer.MAX_VALUE;
            }
        }

        for(int i=0; i<adj.size(); i++){
            List<Arista> fila = adj.get(i);
            for(Arista nodo : fila){
                distancias[i][nodo.destino] = nodo.peso;
            }
        }

        for(int k=0; k<aristas; k++){
            for(int i=0; i<aristas; i++){
                for(int j=0; j<aristas; j++){
                    if(distancias[i][k] != Integer.MAX_VALUE && distancias[k][j] != Integer.MAX_VALUE){
                        if(distancias[i][j] > distancias[i][k] + distancias[k][j]){
                            distancias[i][j] = distancias[i][k] + distancias[k][j];
                        }
                    }
                    
                }
            }
        }
        for(int i=0; i<aristas; i++){
            if(distancias[i][i] < 0){
                System.out.println("El grafo contine eu nciclo negativo en el nodo: " + i + " De: " + distancias[i][i]);
            }
        }
   } 


    public static void imprimirSolucion(int[] distancias) {
        System.out.println("Distancias mínimas desde el nodo origen:");
        for (int i = 0; i < distancias.length; i++) {
            System.out.println("Nodo " + i + " -> " + distancias[i]);
        }
    }


    public static void main(String[] args) {
        // Inicializamos el grafo con 4 nodos (0, 1, 2, 3)
        inicializarGrafo(4);

        // Agregar aristas con pesos (incluyendo un ciclo negativo)
        agregarArista(0, 1, 1);   // Nodo 0 a Nodo 1 con peso 1
        agregarArista(1, 2, 2);   // Nodo 1 a Nodo 2 con peso 2
        agregarArista(2, 0, -5);  // Nodo 2 a Nodo 0 con peso -5 (esto forma el ciclo negativo)
        agregarArista(0, 3, 4);   // Nodo 0 a Nodo 3 con peso 4
        agregarArista(1, 3, 6);   // Nodo 1 a Nodo 3 con peso 6


        // Mostrar el grafo
        mostrarGrafo();
        dijkstra(0, 3);
        floydWarshall();

    }
}
