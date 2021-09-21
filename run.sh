logname=$(date +'%d-%m-%y--%H-%M-%S')
nohup python3 -u active_players.py > ${logname}.log 2>&1 &
