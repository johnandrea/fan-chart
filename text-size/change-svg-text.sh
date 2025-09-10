#!/bin/bash

lower="abcdefghijklmnopqrstuvwxyz"
upper="ABCDEFGHIJKLMNOPQRSTUVWXYZ"

for i in $(seq 1 26); do
    c=${upper:i-1:1}
    change=$(printf %26s | tr " " $c)
    sed "s/$upper/$change/" <original.svg >tmp.tmp
    c=${lower:i-1:1}
    change=$(printf %26s | tr " " $c)
    sed "s/$lower/$change/" <tmp.tmp >$c.svg
    rm tmp.tmp
done
