package falvarezb.multithreading;

import java.util.ArrayDeque;
import java.util.Queue;
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingDeque;
import java.util.concurrent.BlockingQueue;

public class ProducerConsumer2 {


    public static void main(String[] args) {
        BlockingQueue<Integer> queue = new ArrayBlockingQueue<>(10);
        Runnable consumerAction = () -> {
            while(true) {
                try {
                    System.out.printf("Thread: %s, consumed: %d%n", Thread.currentThread().getName(), queue.take());
                } catch (InterruptedException e) {
                    throw new RuntimeException(e);
                }
            }

        };
        Thread consumer1 = new Thread(consumerAction);
        Thread consumer2 = new Thread(consumerAction);
        Thread producer = new Thread(() -> {
            for (int i = 0; i < 1000000; i++) {
                try {
                    queue.put(i);
                } catch (InterruptedException e) {
                    throw new RuntimeException(e);
                }
            }
        });


        consumer1.start();
        consumer2.start();
        producer.start();

        try {
            producer.join();
            consumer1.join();
            consumer2.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}
