import java.io.File
import java.nio.charset.StandardCharsets
import java.nio.file.{Files, Path, Paths}
import java.nio.file.StandardOpenOption.{APPEND, CREATE, TRUNCATE_EXISTING, WRITE}
import org.scalameter._

import scala.collection.immutable
import scala.io.Source

package object challenges {

  def resourcesPath(name: String): String = s"src/main/resources/$name"
  def writeToFile(filePath: String, content: String, overwrite: Boolean = false): Path = Files.write(Paths.get(filePath), content.toString.getBytes(StandardCharsets.UTF_8), CREATE, if(overwrite) TRUNCATE_EXISTING else APPEND, WRITE)
  def readFromFile(filePath: String): immutable.Seq[String] = Source.fromFile(new File(filePath)).getLines().toList

  val standardConfig = config(
    Key.exec.minWarmupRuns -> 10,
    Key.exec.maxWarmupRuns -> 20,
    Key.exec.benchRuns -> 10
  )

  def executionTime[U](f: U => Any, u: U): Quantity[Double] = standardConfig withWarmer new Warmer.Default measure {f(u)}
  def memoryFootprint[U](f: U => Any, u: U): Quantity[Double] = standardConfig withWarmer new Warmer.Default withMeasurer new Measurer.MemoryFootprint measure {f(u)}
  def gcCycles[U](f: U => Any, u: U): Quantity[Int] = standardConfig withWarmer new Warmer.Default withMeasurer(new Measurer.GarbageCollectionCycles, Aggregator.median[Int]) measure {f(u)}

  def executionTime[U,V](f: ((U, List[V])) => Any, u: U, l: List[V]): Quantity[Double] = standardConfig withWarmer new Warmer.Default measure {f(u,l)}
  def memoryFootprint[U,V](f: ((U, List[V])) => Any, u: U, l: List[V]): Quantity[Double] = standardConfig withWarmer new Warmer.Default withMeasurer new Measurer.MemoryFootprint measure {f(u,l)}
  def gcCycles[U,V](f: ((U, List[V])) => Any, u: U, l: List[V]): Quantity[Int] = standardConfig withWarmer new Warmer.Default withMeasurer(new Measurer.GarbageCollectionCycles, Aggregator.median[Int]) measure {f(u,l)}
}
