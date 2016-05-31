BEGIN {
  FS="\t"
  OFS="\t"
}

FNR == NR && NR > 1 {
  split($3,a,"@")
  name[a[1]] = $1
}

FNR < NR {
  if (FNR % 4 == 1) 
  {
    gsub("^#","", $0)
    print "#"name[$0]
  } else {
    print
  }
}
