unpack_path="/home/timur/РЖД/unpack/"

find "${unpack_path}" -maxdepth 1 -type f \( -name "*.zip" \) ! -newermt '3 seconds ago' -print0 | while read -d $'\0' file
do
  unzip "${file}" -d "${unpack_path}"
done