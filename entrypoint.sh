!/bin/bash
test=1
while [ $test -eq 1 ]
do
    echo -n > /dev/tcp/172.22.0.2/4444
    test=$?
    echo test result: $test
done

exec 3>/dev/tcp/172.22.0.2/4444;echo -e "Hello from client" >&3

echo "Client done"
