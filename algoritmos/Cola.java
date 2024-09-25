package algoritmos;

class Node {
    
    public Node next;
    public int data;

    public Node(int data){
        this.data = data;
        this.next = null;
    }
}


public class Cola {
    public Node front;
    public Node back;

    public Cola(){
        this.back = null;
        this.front = null;
    }

    public void enqueue(int data){
        Node newNode = new Node(data);
        if(this.back == null){
            this.front = this.back = newNode;
        } else {
            System.out.println("Anterior -> " + this.back.data);
            this.back.next = newNode;
            this.back = newNode;
        }
    }

    public int dequeue(){
        int data = this.front.data;
        this.front = this.front.next;
        if(this.front == null){
            this.back = null;
        }
        return data;
    }

}
