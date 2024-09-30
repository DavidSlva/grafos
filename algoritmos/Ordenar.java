package algoritmos;



public class Ordenar {


    public static int[] bubbleSort(int[] arr){
        for (int i=0; i<arr.length; i++){
            int now = arr[i];
            for(int j=0; j<i; j++){
                int back = arr[i-j-1];
                System.out.println("back: " + back + " fron: " + now);
                if(back > now){
                    arr[i-j] = back;
                    arr[i-j-1] = now;
                    System.out.println("Intercambio de: " + now + " Con " + back);
                }else{
                    break;
                }
            }
        }
        return arr;
    }



    public static int[] _selectionSort(int[] arr, int position){
        if(position == arr.length - 1){
            return arr;
        }else{
            int minor = position;
            for(int i=position; i<arr.length; i++){
                if(arr[minor] > arr[i]){
                    minor = i;
                }
            }
            int tmp = arr[position];
            arr[position] = arr[minor];
            arr[minor] = tmp;
            return _selectionSort(arr, position + 1);
        }
    }

    public static int[] mergeSort(int[] arr, int left, int right){
        if(left==right){
            return arr;
        }
        if(left > right){
            return arr;
        }
        int mid = (left + right)/2;

        mergeSort(arr, left, mid);
        mergeSort(arr, mid + 1, right);
        // Tomamos la izquierda primero y la vamos ordenando con la derecha.

        int nIzquierda = mid-left+1;
        int nDerecha = right-mid;
        int[] izquierda = new int[nIzquierda];
        int[] derecha = new int[nDerecha];

        // Copiamos la parte de la izquierda
        for(int i=0; i<nIzquierda; i++){
            izquierda[i] = arr[i+left];
        }
        for(int i=0; i<nDerecha; i++){
            derecha[i] = arr[i+mid+1];
        }
        // fusionamos
        int i=0, j=0;
        int k = left;

        while(i<nIzquierda && j<nDerecha){
            if(izquierda[i] > derecha[j]){
                arr[k] = derecha[j];
                j++;
            }else{
                arr[k] = izquierda[i];
                i++;
            }
            k++;
        }

        while(nIzquierda>i){
            arr[k] = izquierda[i];
            k++;
            i++;
        }
        while(nDerecha>j){
            arr[k] = derecha[j];
            k++;
            j++;
        }
        return arr;

    }

    public static void main(String[] args) {
        int[] arr = {6,8,4,3,2};
        int[] result = bubbleSort(arr);
        System.out.print("[");
        for (int i =0 ; i<result.length; i++){
            System.out.print(result[i] + " , ");
        }
        System.out.println("]");
        int[] resultSelectionSort = _selectionSort(arr, 0);

        for (int i =0 ; i<resultSelectionSort.length; i++){
            System.out.print(resultSelectionSort[i] + " , ");
        }
        System.out.println("]");
        System.out.println(resultSelectionSort);

        // System.out.println();
    }
    
}
