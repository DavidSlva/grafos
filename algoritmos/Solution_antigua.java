package algoritmos;

import java.io.*;
import java.util.*;
import java.util.stream.*;
import static java.util.stream.Collectors.toList;

class Result {

    static char DESTINO = 'V';
    static char ORIGEN = 'H';
    static char OBSTACULO = '*';
    static char VACIO = '.';

    // derecha, abajo, izquierda, arriba
    static int[] dirX = {0, 1, 0, -1}; 
    static int[] dirY = {1, 0, -1, 0};

    static class Node implements Comparable<Node> {
        int x, y, giros, direccion;

        Node(int x, int y, int giros, int direccion) {
            this.x = x;
            this.y = y;
            this.giros = giros;
            this.direccion = direccion;
        }

        @Override
        public int compareTo(Node other) {
            return Integer.compare(this.giros, other.giros);
        }
    }

    public static int calcularMinimo(int pN, int pM, List<String> pMapa) {
        int xOr = -1, yOr = -1, xDes = -1, yDes = -1;
        
        for (int i = 0; i < pN; i++) {
            for (int j = 0; j < pM; j++) {
                if (pMapa.get(i).charAt(j) == ORIGEN) {
                    yOr = i;
                    xOr = j;
                }
                if (pMapa.get(i).charAt(j) == DESTINO) {
                    yDes = i;
                    xDes = j;
                }
            }
        }
        if (xOr == -1 || yOr == -1 || xDes == -1 || yDes == -1) {
            return -1;
        }
        
        PriorityQueue<Node> queue = new PriorityQueue<>();
        int[][][] visitado = new int[pN][pM][4];
        for (int i = 0; i < pN; i++) {
            for (int j = 0; j < pM; j++) {
                Arrays.fill(visitado[i][j], Integer.MAX_VALUE);
            }
        }

        queue.add(new Node(xOr, yOr, 0, -1));

        while (!queue.isEmpty()) {
            Node nodo = queue.poll();

            if (nodo.x == xDes && nodo.y == yDes) {
                return nodo.giros;
            }

            for (int i = 0; i < 4; i++) {
                int xAux = nodo.x + dirX[i];
                int yAux = nodo.y + dirY[i];
                if (xAux >= 0 && xAux < pM && yAux >= 0 && yAux < pN && pMapa.get(yAux).charAt(xAux) != OBSTACULO) {
                    int nuevosGiros = nodo.giros + (nodo.direccion != -1 && nodo.direccion != i ? 1 : 0);
                    
                    if (nuevosGiros < visitado[yAux][xAux][i]) {
                        visitado[yAux][xAux][i] = nuevosGiros;
                        queue.add(new Node(xAux, yAux, nuevosGiros, i));
                    }
                }
            }
        }
        
        return -1; 
    }

}

public class Solution {
    public static void main(String[] args) throws IOException {
        BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(System.in));
        BufferedWriter bufferedWriter = new BufferedWriter(new OutputStreamWriter(System.out));

        String[] firstMultipleInput = bufferedReader.readLine().replaceAll("\\s+$", "").split(" ");

        int n = Integer.parseInt(firstMultipleInput[0]);

        int m = Integer.parseInt(firstMultipleInput[1]);

        List<String> mapa = IntStream.range(0, n).mapToObj(i -> {
            try {
                return bufferedReader.readLine();
            } catch (IOException ex) {
                throw new RuntimeException(ex);
            }
        })
            .collect(toList());

        int resMinimo = Result.calcularMinimo(n, m, mapa);

        bufferedWriter.write(String.valueOf(resMinimo));
        bufferedWriter.newLine();

        bufferedReader.close();
        bufferedWriter.close();
    }
}
