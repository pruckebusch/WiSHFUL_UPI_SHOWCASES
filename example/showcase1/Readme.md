# Wishful showcase 1

This showcase demonstrates the efficient airtime management in IEEE 802.11 enterprise networks using Wishful UPI. In
particular a central controller remotely sets-up and controls the hybrid TDMA/CSMA MAC layer on each wireless node
under control. The showcase consists of two parts: i) hidden node detection, ii) using hybrid MAC and assigning of
different time slots to interfering wireless links.

## 1. HowTo

### 1. Set PYTHONPATH to point main wishful_upis dir:
In wishful_upis dir execute:

```
export PYTHONPATH=$(pwd)
```

### 2. Bootstrapping & configuration
On each node to be controlled, i.e. the two APs (nuc2 and nuc3) and the client station (laptop), we have to set-up
and configure the wireless networking system. Moreover, we have to start hostapd on the AP nodes.

On nuc2 start:
```
./nuc2_start_ap.sh
```

On nuc3 start:
```
./nuc3_start_ap.sh
```

On the laptop start:
```
./laptop_start_client.sh
```

### 3. Starting slave agents
Start the slave agent on each node to be controlled, i.e. the two APs (nuc2 and nuc3) and the client station (laptop).

```
sudo python start_slave.py
```

### 4. Starting the global controller

The global controller has to be started on the testbed server. To run it from main project directory, user has to execute command:

```
python ./examples/showcase1/start_sc1.py
```
