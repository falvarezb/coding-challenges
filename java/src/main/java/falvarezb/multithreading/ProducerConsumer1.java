package falvarezb.multithreading;

import java.util.ArrayDeque;
import java.util.Queue;

public class ProducerConsumer1 {


    public static void main(String[] args) {
        Queue<Integer> queue = new ArrayDeque<>();
        Object lock = new Object();

        Runnable consumerAction = () -> {
            while(true) {
                try {
                    synchronized (lock) {
                        while(queue.isEmpty()) {
                            lock.wait(50);
                        }
                        System.out.printf("Thread: %s, consumed: %d%n", Thread.currentThread().getName(), queue.remove());
                    }
                } catch (InterruptedException e) {
                    throw new RuntimeException(e);
                }
            }

        };
        Thread consumer1 = new Thread(consumerAction);
        Thread consumer2 = new Thread(consumerAction);
        Thread producer = new Thread(() -> {
            for (int i = 0; i < 1000000; i++) {
//                try {
//                    Thread.sleep(1000);
//                } catch (InterruptedException e) {
//                    throw new RuntimeException(e);
//                }

                synchronized (lock) {
                    queue.add(i);
                    lock.notify();
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
