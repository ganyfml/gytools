#!/usr/bin/env bash
for i in {A..Z}
do
  wget https://rarediseases.info.nih.gov/gard/browse-by-first-letter/"$i"
  vim -c "source vim_script" "$i" 
done
wget https://rarediseases.info.nih.gov/gard/browse-by-first-letter/0-9
vim -c "source vim_script" "0-9"
cat {A..Z} 0-9 > rare_disease_list.mkd
rm -f {A..Z} 0-9
zip rare_disease_list.zip rare_disease_list.mkd
rm rare_disease_list.mkd
