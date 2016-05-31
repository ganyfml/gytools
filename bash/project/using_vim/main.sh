#!/usr/bin/env bash
#The purpose for this program is getting the rare disease list from nih

for i in {A..Z} 0-9
do
  wget https://rarediseases.info.nih.gov/gard/browse-by-first-letter/"$i"
  vim -c "source vim_script" "$i" 
done
cat {A..Z} 0-9 > rare_disease_list.mkd
rm -f {A..Z} 0-9
zip rare_disease_list.zip rare_disease_list.mkd
rm rare_disease_list.mkd
