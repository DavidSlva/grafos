/*
 * Referencia apoyo de la implementación DFS por Sedgewick y Wayne;
 */

package solemne;

import java.util.*;

public class Solution {
    private static int[] dRow = {-1, -1, -1, 0, 0, 1, 1, 1};
    private static int[] dCol = {-1, 0, 1, -1, 1, -1, 0, 1};
    
    public String encontrarGanador(int[][] tablero) {
        int n = tablero.length;
        boolean jug1Gana = false;
        boolean jug2Gana = false;
        boolean[][] vis1 = new boolean[n][n];
        for (int col = 0; col < n; col++) {
            if (tablero[0][col] == 1 && dfs(tablero, 0, col, 1, vis1)) {
                jug1Gana = true;
                break;
            }
        }
        boolean[][] vis2 = new boolean[n][n];
        for (int row = 0; row < n; row++) {
            if (tablero[row][0] == 2 && dfs(tablero, row, 0, 2, vis2)) {
                jug2Gana = true;
                break;
            }
        }

        if (jug1Gana && jug2Gana) {
            return "AMBIGUOUS";
        } else if (jug1Gana) {
            return "1";
        } else if (jug2Gana) {
            return "2";
        } else {
            return "0";
        }
    }

    private boolean dfs(int[][] tablero, int row, int col, int jugador, boolean[][] visited) {
        int n = tablero.length;

        if (jugador == 1 && row == n - 1) {
            return true;
        }
        if (jugador == 2 && col == n - 1) {
            return true;
        }
        visited[row][col] = true;
        for (int i = 0; i < 8; i++) {
            int newRow = row + dRow[i];
            int newCol = col + dCol[i];
            if (newRow >= 0 && newRow < n && newCol >= 0 && newCol < n && !visited[newRow][newCol] && tablero[newRow][newCol] == jugador) {
                if (dfs(tablero, newRow, newCol, jugador, visited)) {
                    return true;
                }
            }
        }

        return false;
    }

    public static void main(String[] args) {
        Solution sol = new Solution();
        Scanner sc = new Scanner(System.in);
        int size = sc.nextInt();
        int[][] tablero = new int[size][size];
        for(int i=0; i<size; i++){
            for(int j=0; j<size; j++){
                tablero[i][j] = sc.nextInt();
            }
        }
        System.out.println(sol.encontrarGanador(tablero));

    }
}