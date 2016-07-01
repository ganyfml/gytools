$2 > 6 {n = n + 1}
END    { if (n > 0)
            print n, $1, $2
         else
            print "none"
        }
