BEGIN {
  IFS="\t"
  OFS="\t"
}

NR % 4 == 1 {
  printf $0
}
NR % 4 == 2 {
  printf("\t%s",$0)
}
NR %4 == 3 {
  printf("\t%s\n",$0)
}



