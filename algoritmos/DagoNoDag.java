package algoritmos;
import java.util.*;

class Graph{

    int vertices;
    List<List<Integer>> adj;    

    public Graph(int nVer){
        this.vertices = nVer;
        this.adj = new ArrayList<>(nVer);
        for(int i=0; i<nVer; i++){
            adj.add(new ArrayList<>());
        }
    }

    public List<Integer> getNeighbords(int source){
        return this.adj.get(source);
    }

    public void addEdge(int u, int v){
        this.adj.get(u).add(v);
    }

    public void findSource(){
        
    }

    public void getTopological(){
        Queue<Integer> queue = new LinkedList<>();
        boolean[] visited = new boolean[this.vertices];
    }
}

public class DagoNoDag {
    public static void main(String[] args) {
        
    }
}