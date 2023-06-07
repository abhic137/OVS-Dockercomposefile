sudo docker-compose up -d

sudo docker ps


sudo docker exec -it ovs-vswitchd bash

sudo docker exec -it ryu bash

sudo docker exec -it ubuntu1 bash

sudo docker exec -it ubuntu2 bash

#inside the vswitchd
ovs-vsctl add-br ovsbr0
ovs-vsctl add-port ovsbr0 
#to set the ryu controller
ovs-vsctl set-controller ovsbr0 tcp:<ryu_controller_ip>:6653

#to check the connection between ovs vswitchd and ryu we have to run ovs-vsctl show inside the vswitchd  and we have to look for the is_connected: true part and in ryu service we have to use the 
#command : netstat -anp | grep 6653 
