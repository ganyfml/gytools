```
cat aa.txt|cut -f 6 -d $'\t' | awk '{n=split($0,a," / ");for(i=1;i<=n;i++)print a[i]}'| sort | uniq -c | sort -k 1,1n
```
