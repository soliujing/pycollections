# - remove empty rows
KJ_FN=kj_pzjk_202004.csv

#make a copy with UTF8 so sed can work
iconv -f GBK -t UTF8 $KJ_FN >$KJ_FN.UTF8

#delete empty rows with sed
sed -i '' -E '/^\,{3,}$/d' $KJ_FN.UTF8

#compare rows between two files
wc -l $KJ_FN $KJ_FN.UTF8

#check if still any empty rows
grep -E '^\,{3,}' $KJ_FN.UTF8

#convert UTF8 back to GBK for SAT
iconv -f UTF8 -t GBK $KJ_FN.UTF8 >$KJ_FN




# # add U for reversal Y0 document (with negative amount)
KJ_FN=kj_pzjk_202012.csv

#make a copy with UTF8 so sed can work
iconv -f GBK -t UTF8 $KJ_FN >$KJ_FN.UTF8

#display all Y0 document with negative amount
# grep -E '^2020,12,Y0,(\d{1,}),.*,-\d{1,}.*,,,' kj_pzjk_202012.csv.UTF8
grep -E '^(\d{4},\d{1,2},Y0,)(\d{1,})(,.*,-\d{1,}.*,,,)' $KJ_FN.UTF8

#update document# with U indicator empty rows with sed
sed -i '' -E 's/^([0-9]{4},[0-9]{1,2},Y0,)([0-9]{1,})(,.*,-[0-9]{1,}.*,,,)/\1\2U\3/g' $KJ_FN.UTF8

#check if updated with U
grep -E '^(\d{4},\d{1,2},Y0,)(\d{1,}U{0,1})(,.*,-\d{1,}.*,,,)' $KJ_FN.UTF8

#convert UTF8 back to GBK for SAT
iconv -f UTF8 -t GBK $KJ_FN.UTF8 >$KJ_FN




#find doc which not balanced
KJ_FN=kj_pzjk_202012.csv
# awk -F ',' 'FNR>1 {d[$4]+=$9*100;c[$4]+=$10*100} END {for (i in d) {printf("%s \tDr:%d \tCr:%d \tbal:%d\n",i,d[i],c[i],d[i]-c[i])}}' kj_pzjk*.csv | grep -v "bal:0.00|bal:-0.00" 

#awk to subtotal by doc# and print unbalanced 
awk -F ',' 'function abs(v) {return v < 0 ? -v : v} \
	FNR>1 {d[$4]+=$9;c[$4]+=$10} END {for (i in d) {\
	if ( abs(d[i]-c[i]) >= 0.01 ) \
		printf("%s \tDr:%.2f \tCr:%.2f \tbal:%.2f\n",i,d[i],c[i],d[i]-c[i])}}' \
$KJ_FN

# awk -F ',' 'FNR>1 {d[$4]+=$9;c[$4]+=$10} END {for (i in d) {\
# 	printf("%s \tDr:%.2f \tCr:%.2f \tbal:%.2f\n",i,d[i],c[i],d[i]-c[i])}}' \
# kj_pzjk*.csv

### delete above document from specified doc#
sed -i '' '/,1700004924,|,1700004924,/d' $KJ_FN