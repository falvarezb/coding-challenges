package challenges.stairs

import challenges._
import scala.util.Try

/**
  * Number of ways to climb 'n' stairs combining 'steps' of different length OR
  * Number of ways to provide change for an amount 'n' by using coins of different 'values'
  */
object Stairs extends App {

  /**
    * Counts all combinations, including permutations.
    *
    * n=5
    * values=[2,3]
    * combinations: [2,3] and [3,2]
    */
  def countAllCombinations(n: Int, steps: List[Int]): Int = n match {
    case 0 => 1
    case `n` => steps.filter(_ <= n).map(step => countAllCombinations(n - step, steps)).sum
  }

  /**
    * Finds all combinations, including permutations.
    *
    * n=5
    * values=[2,3]
    * combinations: [2,3] and [3,2]
    *
    * If no combination exists, returns an empty list
    */
  def enumerateAllCombinations(n: Int, steps: List[Int]): List[List[Int]] = n match {
    case 0 => List(Nil)
    case `n` => steps.filter(_ <= n).flatMap(step => enumerateAllCombinations(n - step, steps).map(comb => step :: comb))
  }

  /**
    * Like 'enumerateAllCombinations' but excluding permutations.
    * 'canonical combination' is defined as the only representative of a list of steps and all its permutations
    *
    * n=5
    * values=[2,3]
    * canonical combination: [2,3]
    *
    * If no combination exists, returns an empty list
    */
  def enumerateAllCanonicalCombinations(n: Int, steps: List[Int]): List[List[Int]] = {
    enumerateAllCombinations(n, steps).map(_.sorted).distinct
  }

  /**
    * Like 'enumerateAllCombinations' but taking only the shortest combinations.
    * 'optimal combination' is defined as the shortest one.
    * There may be more than one optimal combination
    *
    * n=5
    * values=[2,3]
    * combinations: [2,3] and [3,2]
    *
    * If no combination exists, returns an empty list
    */
  def enumerateAllOptimalCombinations(n: Int, steps: List[Int]): List[List[Int]] = Try {
    enumerateAllCombinations(n, steps).groupBy(l => l.length).toSeq.minBy(_._1)._2
  }.getOrElse(List())

  /**
    * n=5
    * values=[2,3]
    * canonical combination: [2,3] and [3,2]
    *
    * If no combination exists, returns an empty list
    */
  def enumerateAllOptimalCanonicalCombinations(n: Int, steps: List[Int]): List[List[Int]] = Try {
    enumerateAllCanonicalCombinations(n, steps).groupBy(l => l.length).toSeq.minBy(_._1)._2
  }.getOrElse(List())

  /**
    * Finds any optimal combination, if there is more than one optimal combination, returns any one of them.
    * If no combination exists, returns an empty list
    */
  def enumerateAnyOptimalCombination(n: Int, steps: List[Int]): List[Int] = Try {
    n match {
      case 0 => Nil
      case `n` => steps.filter(_ <= n).map(step => step :: enumerateAnyOptimalCombination(n - step, steps)).filter(_.sum == n).minBy(_.length)
    }
  }.getOrElse(Nil)

  /**
    * Finds the greedy combination
    * If no greedy combination exists, returns an empty list
    */
  def greedyCombination(n: Int, steps: List[Int]): List[Int] = Try {
    n match {
      case 0 => Nil
      case `n` =>
        val greatestCandidate = steps.filter(_ <= n).max
        greatestCandidate :: greedyCombination(n - greatestCandidate, steps) match {
          case solution if solution.sum == n => solution
          case _ => Nil
        }
    }
  }.getOrElse(Nil)

}

object StairsBenchmark extends App {
  import challenges.stairs.Stairs._

  val n = 50
  val steps = List(2,5,8)


  println(s"countAllCombinations ${executionTime((countAllCombinations _).tupled, n, steps)}")
  println(s"enumerateAllCombinations.length ${executionTime((enumerateAllCombinations _).tupled andThen(_.length), n, steps)}")
  println(s"enumerateAnyOptimalCombination ${executionTime((enumerateAnyOptimalCombination _).tupled, n, steps)}")
  println(s"enumerateAllOptimalCombinations.head ${executionTime((enumerateAllOptimalCombinations _).tupled andThen(_.head), n, steps)}")
  println(s"greedyCombination ${executionTime((greedyCombination _).tupled, n, steps)}")

  println("\n==============\n")
  println(s"countAllCombinations ${memoryFootprint((countAllCombinations _).tupled, n, steps)}")
  println(s"enumerateAllCombinations.length ${memoryFootprint((enumerateAllCombinations _).tupled andThen(_.length), n, steps)}")
  println(s"enumerateAnyOptimalCombination ${memoryFootprint((enumerateAnyOptimalCombination _).tupled, n, steps)}")
  println(s"enumerateAllOptimalCombinations.head ${memoryFootprint((enumerateAllOptimalCombinations _).tupled andThen(_.head), n, steps)}")
  println(s"greedyCombination ${memoryFootprint((greedyCombination _).tupled, n, steps)}")

  println("\n==============\n")
  println(s"countAllCombinations ${gcCycles((countAllCombinations _).tupled, n, steps)}")
  println(s"enumerateAllCombinations.length ${gcCycles((enumerateAllCombinations _).tupled andThen(_.length), n, steps)}")
  println(s"enumerateAnyOptimalCombination ${gcCycles((enumerateAnyOptimalCombination _).tupled, n, steps)}")
  println(s"enumerateAllOptimalCombinations.head ${gcCycles((enumerateAllOptimalCombinations _).tupled andThen(_.head), n, steps)}")
  println(s"greedyCombination ${gcCycles((greedyCombination _).tupled, n, steps)}")
}
