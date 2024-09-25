package algoritmos;

class Node {
    
    public Node next;
    public int data;

    public Node(int data){
        this.data = data;
        this.next = null;
    }
}


public class ListaEnlazada {
    public Node tail;
    public Node head;
    
    public ListaEnlazada(){
        this.tail = null;
        this.head = null;
        
    }

    public void insertAtEnd(int data){
        Node node = new Node(data);
        if(tail == null){
            this.tail = this.head = node;
        }else{
            this.tail.next = node;
            this.tail = node;
        }
    }

    public void insertAtStart(int data){
        Node node = new Node(data);
        if(tail == null){
            this.tail = this.head = node;
        }else{
            node.next = this.head;
            this.head = node;
        }
    }

    public void insertAtPosition(int pos, int data){
        if(pos == 0){
            this.insertAtStart(data);
        }else{
            Node newNode = new Node(data);
            Node temp = this.head;
            for (int i=0; i<pos-1; i++){
                if( temp == null ){
                    throw new IndexOutOfBoundsException();
                }
                temp = temp.next;
            }
            if(temp.next == null){
                temp.next = newNode;
                this.tail = newNode;
            }else{
                newNode.next = temp.next;
                temp.next = newNode;
            }
            
        }
    }
}
