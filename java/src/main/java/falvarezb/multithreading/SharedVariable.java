package falvarezb.multithreading;

import java.util.concurrent.atomic.AtomicInteger;

public class SharedVariable {
    static AtomicInteger value = new AtomicInteger(0);

    public static void main(String[] args) {
        Thread t1 = new Thread(() -> {
            for (int i = 0; i < 1000000; i++) {
                value.getAndIncrement();
            }
        });
        Thread t2 = new Thread(() -> {
            for (int i = 0; i < 1000000; i++) {
                value.getAndIncrement();
            }
        });

        t1.start();
        t2.start();

        try {
            t1.join();
            t2.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        System.out.println(value);
    }


}
