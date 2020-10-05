package util

import java.time.LocalDate
import java.time.format.{DateTimeFormatter, ResolverStyle}

object DateUtil {

  val `uuuu-MM-dd pattern` = "uuuu-MM-dd"
  val `uuuu-MM-dd formatter` = DateTimeFormatter.ofPattern(`uuuu-MM-dd pattern`).withResolverStyle(ResolverStyle.STRICT)
  def formatDate(formatter: DateTimeFormatter, date: LocalDate): String = formatter.format(date)


}