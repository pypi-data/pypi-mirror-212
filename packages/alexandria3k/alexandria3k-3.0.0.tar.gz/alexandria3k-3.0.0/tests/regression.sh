#!/bin/sh

OPERATION="$1"

case $OPERATION in
  -c)
    rm -rf tests/tmp/regression
    ;;
  -p)
    rm -rf tests/ref
    ;;
  *)
    echo "Usage: $0 -c|-p" 1>&2
    exit 2
    ;;
esac

mkdir -p tests/tmp/regression tests/ref

run()
{
  id=$(echo "$@" | md5sum | cut -d ' ' -f 1)
  case $OPERATION in
    -c)
      out=tests/tmp/regression/$id
      rm -f $out

      if ! "$@" >"$out" 2>&1 ; then
        echo "Command $@ failed" 1>&2
        exit 1
      fi

      if ! diff $out tests/ref/$id 1>&2 ; then
        echo "Output of $@ differs" 1>&2
        exit 1
      fi
      ;;
    -p)
      "$@" >tests/ref/$id
      ;;
  esac
}

run alexandria3k --help

run alexandria3k --data-source Crossref tests/data/sample \
   --query 'SELECT DOI, title FROM works ORDER BY doi'
