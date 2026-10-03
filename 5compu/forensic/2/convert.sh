convert $1 -quality $2 recompressed.jpg
compare -compose src $1 recompressed.jpg difference.png
convert difference.png -auto-level ela.png
