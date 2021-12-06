echo -n "Please enter the folder: "
read folder
echo -n "Please enter the amount of inputs that one machine should do: "
read load
echo -n "Please enter the starting idx: "
read start_idx
echo -n "Please enter the ending idx: "
read end_idx


start_session=$(tmux ls | wc -l)
# find new session number to start tmux windows from

for ((i = $start_idx; i <= $end_idx; i=i+load)); do
    ((session_name = $((i + $start_session))))
    # assuming the session name hasn't been created yet
    tmux new-session -d -s "$session_name"
    tmux send-keys -t "$session_name" "source ~/.bashrc; conda activate 170; python solver.py $folder $i $(($i + $load - 1))" ENTER
    echo "$session_name $folder $i $(($i + $load - 1))"
done