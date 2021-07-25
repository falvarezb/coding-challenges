package challenges.order

import java.util
import scala.util.control.Breaks.{break, breakable}

object LexicographicalOrder {

  def main(args: Array[String]): Unit = {
    println(nextElement("dkhc"))
  }

  def nextElement(s: String): String = {
    val arr = s.toCharArray
    var finalJ = 0
    breakable {
      for (i <- arr.length - 1 to(0, -1)) {
        for (j <- i to(0, -1)) {
          if (arr(j) < arr(i)) {
            val temp = arr(j)
            arr(j) = arr(i)
            arr(i) = temp
            finalJ = j
            break()
          }
        }
      }
    }
    val left = arr.take(finalJ+1)
    val right = arr.takeRight(s.length-finalJ-1)
    util.Arrays.sort(right)
    (left ++ right).toList.toString()
  }

}
