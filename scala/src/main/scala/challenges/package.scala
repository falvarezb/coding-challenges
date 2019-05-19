import java.io.File
import java.nio.charset.StandardCharsets
import java.nio.file.{Files, Path, Paths}
import java.nio.file.StandardOpenOption.{APPEND, CREATE, TRUNCATE_EXISTING, WRITE}
import scala.collection.immutable
import scala.io.Source

package object challenges {

  def filePath(name: String): String = s"src/main/resources/$name"
  def writeToFile(filePath: String, content: String, overwrite: Boolean = false): Path = Files.write(Paths.get(filePath), content.toString.getBytes(StandardCharsets.UTF_8), CREATE, if(overwrite) TRUNCATE_EXISTING else APPEND, WRITE)
  def readFromFile(filePath: String): immutable.Seq[String] = Source.fromFile(new File(filePath)).getLines().toList
}
