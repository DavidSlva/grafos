package algoritmos;

class Node {
    
    public Node before;
    public int data;

    public Node(int data){
        this.data = data;
    }


}

public abstract class Pila {

    public Node actual;

    public void push(int data){
        Node newNode = new Node(data);
        newNode.before = this.actual;
        this.actual = newNode;
    }

    public int pop(){
        if(this.actual == null){
            throw new IllegalStateException("La pila está vacia");
        }

        Node temp = this.actual;
        this.actual = temp.before;
        return temp.data;
    }

    public int peek(){
        if(this.actual == null){
            throw new IllegalStateException("La pila está vacia");
        }
        return this.actual.data;
    }
    
}
