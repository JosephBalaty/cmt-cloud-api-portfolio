Param(
[boolean]$Delete = $true,
[boolean]$Create = $true
)

If ($Delete){
deactivate
rmdir ./src/Scripts -Recurse -Force
rmdir ./src/Include -Recurse -Force
rmdir ./src/Lib -Recurse -Force
rm ./src/pyvenv.cfg

} If ($Create) {

py -m venv ./src
./src/Scripts/activate
py -m pip install --upgrade pip
pip install -r ./src/requirements.txt

}
