package challenges.closest_points

import math._

case class Point(x: Int, y: Int)
case class PointDistance(p1: Point, p2: Point, d: Double)
case class PyElement(p: Point, xPosition: Int)

object ClosestPoints {

  /**
    * Euclidean distance
    */
  def distance(point1: Point, point2: Point): Double = {
    sqrt(pow(point1.x - point2.x, 2) + pow(point1.y - point2.y, 2))
  }

  /**
    * Brute force solution
    */
  def quadratic_solution(P: List[Point]): PointDistance = {
    if(P.length == 2) {
      PointDistance(P(0), P(1), distance(P(0), P(1)))
    }
    else {
      val tailSolution = quadratic_solution(P.tail)
      val (p, d) = P.tail.foldLeft((P.tail.head, Double.MaxValue)) { case (selectedPointDistance, nextPoint) =>
        val d = distance(P.head, nextPoint)
        if(d < selectedPointDistance._2) (nextPoint, d) else selectedPointDistance
      }
      if(d < tailSolution.d) {
        PointDistance(P.head, p, d)
      } else
        tailSolution
    }
  }

  /**
    * P -> Px, Py
    */
  def sortPoints(P: List[Point]): (List[Point], List[PyElement]) = {
    val Px = P.sortBy(_.x)
    val Py = Px.zipWithIndex.map{case (p,idx) => PyElement(p,idx)}.sortBy(_.p.y)
    (Px, Py)
  }

  def leftHalfPoints(Px: List[Point], Py: List[PyElement]): (List[Point], List[PyElement]) = {
    val leftHalfUpperBound = ceil(Px.length/2d).toInt
    val newPx = Px.slice(0, leftHalfUpperBound)
    val newPy = Py.filter(_.xPosition < leftHalfUpperBound)
    (newPx, newPy)
  }

  def rightHalfPoints(Px: List[Point], Py: List[PyElement]): (List[Point], List[PyElement]) = {
    val n = Px.length
    val rightHalfLowerBound = n/2
    val newPx = Px.slice(rightHalfLowerBound, n)
    val newPy = Py.filter(_.xPosition >= rightHalfLowerBound).map(p => PyElement(p.p, p.xPosition-rightHalfLowerBound))
    (newPx, newPy)
  }

  def getCandidatesFromDifferentHalves(rightmostLeftPoint: Point, Py: List[PyElement], minDistanceUpperBound: Double): List[PyElement] = {
    Py.filter(py => abs(rightmostLeftPoint.x - py.p.x) < minDistanceUpperBound)
  }

  def closestPointsFromDifferentHalves(candidates: List[PyElement]): Option[PointDistance] = {
    var minDistance = Double.MaxValue
    var closestPoints: Option[(Point, Point)] = None
    for(i <- candidates.indices) {
      for(j <- i+1 until min(candidates.length,16)) {
        val d = distance(candidates(i).p, candidates(j).p)
        if(d < minDistance) {
          minDistance = d
          closestPoints = Some((candidates(i).p, candidates(j).p))
        }
      }
    }
    closestPoints.map(x => PointDistance(x._1, x._2, minDistance))
  }

  def closestPoints(Px: List[Point], Py: List[PyElement]): PointDistance = {
    if(Px.length == 2) {
      PointDistance(Px(0), Px(1), distance(Px(0), Px(1)))
    }
    else {
      //https://stackoverflow.com/questions/44713728/why-cant-we-have-capital-letters-in-tuple-variable-declaration-in-scala
      val (lx, ly) = leftHalfPoints(Px, Py)
      val (rx,ry) = rightHalfPoints(Px, Py)

      val leftClosestPoints = closestPoints(lx, ly)
      val rightClosestPoints = closestPoints(rx, ry)

      val minDistanceUpperBound = min(leftClosestPoints.d, rightClosestPoints.d)
      val candidates = getCandidatesFromDifferentHalves(lx.last, Py, minDistanceUpperBound)
      val closestCandidates = closestPointsFromDifferentHalves(candidates)

      if(closestCandidates.exists(_.d < minDistanceUpperBound)) {
        closestCandidates.get
      }
      else if(leftClosestPoints.d < rightClosestPoints.d) {
        leftClosestPoints
      }
      else {
        rightClosestPoints
      }
    }
  }

  def nlognSolution(P: List[Point]): PointDistance = {
    (closestPoints _).tupled(sortPoints(P))
  }

}
