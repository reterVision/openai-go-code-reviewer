git diff HEAD~1..HEAD -- hello.go | awk '

  /^-/ {
    actual_line = actual_line - 1
    next
  }
  /^+/ {
    line_number = actual_line - 5
    print line_number $0
  }
'
