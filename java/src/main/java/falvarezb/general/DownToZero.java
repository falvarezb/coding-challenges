package falvarezb.general;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class DownToZero {

    public static void main(String[] args) {
//        for (int i: arr) {
//            callCount = 0;
//            var start = System.currentTimeMillis();
//            System.out.println(downToZero(i));
//            System.out.println(String.format("elapsed: %d", System.currentTimeMillis() - start));
//            System.out.println(String.format("callCount: %d", callCount));
//
//        }
        System.out.println(downToZeroSequence(966514));
    }

    static int[] arr = {
            966514
//            812849,
//            808707,
//            360422,
//            691410,
//            691343,
//            551065,
//            432560,
//            192658,
//            554548,
//            27978 ,
//            951717,
//            663795,
//            315528,
//            522506,
//            300432,
//            412509,
//            109052,
//            614346,
//            589115,
//            301840,
//            7273  ,
//            193764,
//            702818,
//            639354,
//            584658,
//            208828,
//            255463,
//            506460,
//            471454,
//            554516,
//            739987,
//            303876,
//            813024,
//            118681,
//            708473,
//            616288,
//            962466,
//            55094 ,
//            599778,
//            385504,
//            428443,
//            646717,
//            572077,
//            463452,
//            750219,
//            725457,
//            672957,
//            750371,
//            542716,
//            87017 ,
//            743756,
//            293742,
//            301031,
//            939025,
//            503398,
//            334595,
//            209039,
//            191818,
//            158563,
//            617470,
//            118260,
//            176581,
//            966721,
//            48924 ,
//            235330,
//            200174,
//            992221,
//            411098,
//            559560,
//            117381,
//            814728,
//            795418,
//            309832,
//            943111,
//            775314,
//            875208,
//            168234,
//            933574,
//            444474,
//            995856,
//            687362,
//            543687,
//            761831,
//            952514,
//            970724,
//            611269,
//            237583,
//            88891 ,
//            708888,
//            387629,
//            407891,
//            393991,
//            577592
            };
    static int callCount = 0;
    static int max = 1000000;
    static int[] partialSolutions = new int[max+1];
    static {
        partialSolutions[0]=0;
        partialSolutions[1]=1;
        for(int j=2; j<=max; j++)
            partialSolutions[j] = -1;
    };

    static List<Integer>[] sequences = new List[max + 1];
    static {
        sequences[0] = new ArrayList<>(List.of(0));
        sequences[1] = new ArrayList<>(Arrays.asList(0, 1));
        for(int j=2; j<=max; j++)
            sequences[j] = null;
    }

    public static int downToZero(int n) {
        callCount++;
        if(partialSolutions[n] != -1) return partialSolutions[n];

        int solution = Integer.MAX_VALUE;
//         int sq = (int)Math.sqrt(n);
//         for(int j=2; j<=sq; j++) {
//             if(n%j == 0) {
//                 solution = Math.min(solution, downToZero(n/j) + 1);
//             }
//         }
//         solution = Math.min(solution, downToZero(n-1) + 1);

         List<Integer> candidates = next(n);
         for(int j: candidates) {
             solution = Math.min(solution, downToZero(j) + 1);
         }

//        int solution = next(n).stream().map(DownToZero::downToZero).min(Integer::compare).orElse(0) + 1;

        return (partialSolutions[n] = solution);
    }

    public static List<Integer> downToZeroSequence(int n) {
        if(sequences[n] != null) return sequences[n];
        List<Integer> sequence = new ArrayList<>();
        List<Integer> candidates = next(n);
        for(int j: candidates) {
            var temp = downToZeroSequence(j);
            if(sequence.isEmpty() || temp.size() < sequence.size()) {
                sequence.clear();
                sequence.addAll(temp);
            }
        }
        sequence.add(n);

        return sequences[n] = sequence;
    }

    static List<Integer> next(int n) {
        List<Integer> candidates = new ArrayList<>();
        int sq = (int)Math.sqrt(n);
        for(int j=2; j<=sq; j++) {
            if(n%j == 0) {
                candidates.add(n/j);
            }
        }
        candidates.add(n-1);
        return candidates;
    }
}
