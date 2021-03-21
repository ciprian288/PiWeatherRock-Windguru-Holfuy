mkdir 700
for file in *.png; do convert $file -resize 180%x180% ~/700/resized-$file; done