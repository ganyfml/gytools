#!/usr/bin/env bash

target_dir=include
rm -rf "$target_dir"
mkdir -p "$target_dir"
cd "$target_dir"

while read -r -d '' f
do
  export_dirs+=("$f")
done < <(find ../src/ -type f -name .export -printf '%h\0')

while read -r -d '' f
do
  d_base=$(echo "$f" | cut -d '/' -f 3)
  mkdir -p "$d_base"
  cd "$d_base"
  ln -fs "../$f"
  cd - > /dev/null
done < <(find "${export_dirs[@]}" -mindepth 1 -maxdepth 1 -type f -name '*.hpp' -print0)
