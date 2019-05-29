package challenges.stairs

object Stairs extends App {

  /*
    Number of ways to climb 'n' stairs combining steps of different 'values'
    Number of ways to provide change for an amount 'n' by using coins of different 'values'
   */
  def countAllCombinations(n: Int, values: List[Int]): Int = n match {
    case 0 => 1
    case x => values.filter(_ <= x).map(step => countAllCombinations(x - step, values)).sum
  }

  def enumerateAllCombinations(n: Int, values: List[Int]): List[List[Int]] = n match {
    case 0 => List(Nil)
    case x => values.filter(_ <= x).flatMap(step => enumerateAllCombinations(x - step, values).map(comb => step :: comb))
  }

  def enumerateAllOptimalCombinations(n: Int, values: List[Int]): List[List[Int]] = enumerateAllCombinations(n, values).groupBy(l => l.length).toSeq.minBy(_._1)._2

  def enumerateAnyOptimalCombination(n: Int, steps: List[Int]): List[Int] = n match {
    case 0 => Nil
    case x => values.filter(_ <= x).map(step => step :: enumerateAnyOptimalCombination(x - step, steps)).minBy(_.length)
  }

  def lengthOfOptimalCombination(n: Int, values: List[Int]): Int = n match {
    case 0 => 0
    case x => values.filter(_ <= x).map(step => 1 + lengthOfOptimalCombination(x - step, values)).min
  }

  def enumerateAnyOptimalCombinationGreedy(n: Int, values: List[Int]): List[Int] = n match {
    case 0 => Nil
    case x =>
      val greatestCandidate = values.filter(_ <= x).max
      greatestCandidate :: enumerateAnyOptimalCombinationGreedy(x - greatestCandidate, values)
  }

  def lengthOfOptimalCombinationGreedy(n: Int, values: List[Int]): Int = n match {
    case 0 => 0
    case x =>
      val greatestCandidate = values.filter(_ <= n).max
      1 + lengthOfOptimalCombinationGreedy(x - greatestCandidate, values)
  }

  val n = 9
  val values = List(1, 4, 5)
  println(s"countAllCombinations: ${countAllCombinations(n, values)}")
  println(s"enumerateAllCombinations: ${enumerateAllCombinations(n, values)}")
  println(s"enumerateAllOptimalCombinations: ${enumerateAllOptimalCombinations(n, values)}")
  println(s"enumerateAnyOptimalCombination: ${enumerateAnyOptimalCombination(n, values)}")
  println(s"lengthOfOptimalCombination: ${lengthOfOptimalCombination(n, values)}")
  println(s"enumerateAnyOptimalCombinationGreedy: ${enumerateAnyOptimalCombinationGreedy(n, values)}")
  println(s"lengthOfOptimalCombinationGreedy: ${lengthOfOptimalCombinationGreedy(n, values)}")

}
