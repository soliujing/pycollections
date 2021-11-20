#bin/sh
whome='/Users/xxxxxx/Desktop/04_Validated_DATA'
wyear='2020'
cd $whome || exit 1
# which uncompress rename sed recode mv awk || exit 2

# uncompress *.Z

# rename 's/^0151_//g' *.csv

for (( i = 1; i <= 12; i++ )); do
	#folder for each period
	# mkdir -p $(printf "%s/%04d%02d" $whome $wyear $i)
	#move appropriate files in
	# mv $(printf "%s/kj_pzjk_%s%02d-*.csv" $whome $wyear $i) $(printf "%s/%04d%02d" $whome $wyear $i)

	cd $(printf "%s/%04d%02d" $whome $wyear $i)
    echo "concatenating files under :$(printf "%s/%04d%02d" $whome $wyear $i)"
	#concatenate csv into a single file, keep header from 1st file
	wfile=$(printf "%s/kj_pzjk_%s%02d.csv" $whome $wyear $i)
	awk '(NR == 1) || (FNR > 1)' *.csv > $wfile

done

for (( i = 1; i <= 12; i++ )); do
	wfile=$(printf "%s/kj_pzjk_%s%02d.csv" $whome $wyear $i)

	echo "removing leading 0 at $wfile"
	#remove leading zero for item# & GL account#
	sed -i '' -E 's/,0{1,}([1-9][0-9]{0,7}),/,\1,/g' $wfile

	#remove BOM from original file
	sed -i '' -E '1s/^\xEF\xBB\xBF//' $wfile

	# echo "convert encoding for $wfile"
	#encoding to GBK
	# recode utf8..gbk $wfile
done


# parallel recode utf8..gbk/CR-LF {} ::: *.csv

#convert line break to DOS/windows style
#unix2dos $wfile
