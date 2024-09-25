package algoritmos;

import java.io.*;
import java.util.*;


public class Recursivo {

    static int factorial(int number){
        if(number < 0){
            throw new IllegalArgumentException("El número no debe ser negativo");
        }
        return (number <= 1) ? 1 : number * factorial(number-1);
    }

    public static int fibonnaci_recursivo(int number){
        return _fibonnaci_recursivo(1, 0, 1, number);
    }

    private static int _fibonnaci_recursivo(int actual, int pasado, int cantidad, int finalizar){
        if(finalizar == cantidad){
            return actual;
        }
        return _fibonnaci_recursivo(actual + pasado, actual, cantidad + 1, finalizar);
    }

    public static int fibonacci_ingenuo(int destino){
        if(destino <= 1){
            return destino;
        }else{
            return fibonacci_ingenuo(destino-1)+fibonacci_ingenuo(destino-2);
        }
    }

    public static int fibonnaci_iterativo(int destino){
        int actual = 1;
        int pasado = 0;
        for(int i=1; i<destino; i++){
            int temp = actual;
            actual += pasado;
            pasado = temp;
        }
        return actual;
    }

    public static Map<Integer, Integer> memo = new HashMap<>();

    public static int fibonnaci_memoizado(int destino){
        if(destino <=1){
            return destino;
        }
        if(memo.containsKey(destino)){
            return memo.get(destino);
        }else{
            int result = fibonnaci_memoizado(destino-1) + fibonnaci_memoizado(destino - 2);
            memo.put(destino, result);
            return result;
        }
    }

    public static int binary_search(int[] lista, int low, int high,int x){
        if (low > high){
            return -1;
        }
        int mid = (low + high)/2;
        if(lista[mid] == x){
            if(mid != 0 && lista[mid - 1] != x){
                return mid;
            }else{
                return binary_search(lista, low, mid-1, x);
            }
        }else if(lista[mid] > x){
            return binary_search(lista, low, mid - 1, x);
        }else{
            return binary_search(lista, mid + 1, high, x);
        }
    }

    // int[] arr = {15, 18, 2, 3, 6, 12};
    public static int rotation_point(int[] arr, int low, int high){
        if(low == high){
            return low;
        }
        if(low > high){
            return -1;
        }
        int mid = (low + high)/2;

        if(mid < high && arr[mid] > arr[mid + 1]){
            return mid + 1;
        }
        if(mid > low && arr[mid] < arr[mid -1]){
            return mid;
        }

        if(arr[mid] > arr[high]){
            return rotation_point(arr, mid + 1, high);
        }else {
            return rotation_point(arr, low, mid - 1);
        }

    }

    // int[] arr = {1, 3, 20, 4, 1, 0};
    public static int findPeak(int[] arr, int low, int high){
        if(low == high){
            return low;
        }
        int mid = (low + high)/2;

        if((mid == 0 || arr[mid] > arr[mid-1]) && (mid == arr.length-1 || arr[mid] > arr[mid + 1])){
            return mid;
        }
        if(arr[mid+1] > arr[mid]){
            return findPeak(arr, mid + 1, high);
        }else{
            return findPeak(arr, low, mid - 1);
        }
    }

    public static int potencia(int number, int exponent){
        if(exponent == 0){
            return 1;
        }
        return number * potencia(number, exponent-1);
    }

    public static double potencia_divide_and_conquer(int number, int exponent){
        if(exponent == 0){
            return 1;
        }
        double middlePower = potencia_divide_and_conquer(number, exponent/2);
        if(exponent%2 == 0){
            return middlePower * middlePower;
        }else{
            if(exponent > 0){
                return middlePower * middlePower * number;
            }else{
                return (middlePower * middlePower) / number;
            }
        }
    }

    public static ArrayList<Stack<Integer>> torres;


    // n es el número de discos
    public static void torres_hanoi(int n, Stack<Integer> torre_origen, Stack<Integer> torre_destino, Stack<Integer> torre_auxiliar){
        

        if(n == 1){
            int disco = torre_origen.pop();
            torre_destino.push(disco);
            System.out.println("Mover disco " + disco + " de " + torre_origen + " a " + torre_destino);
        }else{
            torres_hanoi(n-1, torre_origen, torre_auxiliar, torre_destino);
            int disco = torre_origen.pop();
            torre_destino.push(disco);
            System.out.println("Mover disco " + disco + " de " + torre_origen + " a " + torre_destino);
            torres_hanoi(n-1, torre_auxiliar, torre_destino, torre_origen);
        }
    }
    
    
    
    public static void hanoi(int n, Stack<Integer> torre_origen, Stack<Integer> torre_destino, Stack<Integer> torre_auxiliar){
        if(n == 1){
            int disco = torre_origen.pop();
            torre_destino.push(disco);
        }else{
            hanoi(n-1, torre_origen, torre_auxiliar, torre_destino);
            int disco = torre_origen.pop();
            torre_destino.push(disco);
            hanoi(n-1, torre_auxiliar, torre_destino, torre_origen);

        }
    }




    public static void main(String[] args) {
        System.out.println("Hola, mundo!");
        int result = factorial(9);
        System.out.println("Factoria lde 9");
        System.out.println(result);
        System.out.println("Fibonnaci de 9");
        int fibonnaci_recursivo_result = fibonnaci_recursivo(9);
        System.out.println(fibonnaci_recursivo_result);
        int fibonnaci_pesado = fibonacci_ingenuo(9);
        System.out.println(fibonnaci_pesado);
        int fibonnaci_iterativo_result = fibonnaci_iterativo(9);
        System.out.println(fibonnaci_iterativo_result);
        int fibonnaci_memoizado_result = fibonnaci_memoizado(9);
        System.out.println(fibonnaci_memoizado_result);
        System.out.println("Encontrar por búsqeda binaria el numero 9");
        int[] arr = {1, 3, 5, 7, 9, 11, 13, 15, 17, 19};
        int x = 9;
        int search_binary_result = binary_search(arr, 0, arr.length -1 , x);
        System.out.println(search_binary_result);

        int discos_torre = 4;
        Stack<Integer> torre_origen = new Stack<>();
        Stack<Integer> torre_destino = new Stack<>();
        Stack<Integer> torre_auxiliar = new Stack<>();
        for(int i=discos_torre; i>0; i--){
            torre_origen.push(i);
        }
        torres_hanoi(discos_torre, torre_origen, torre_destino, torre_auxiliar);



    }
}
