# xroute_env
RL environment for detailed routing.

## Quickstart

### Installation

To interact with the xroute environment, you need to download the simulator first:

| Operating System | Download Link |
| --- | --- |
| Ubuntu 22.04 | [Download](https://drive.google.com/file/d/1-Zxd0HiOHclNtwCON5wOM78eCzsPrOBB/view?usp=sharing) |

Then, put the simulator in the `third_party/openroad` folder.

### Launch Algorithm Backend

[DQN](./baseline/DQN/README.md)

[PPO](./baseline/DQN/PPO.md)

### Launch Simulator

Run the following command to get launch script:

```bash
cd examples
python3 init.py [start_port][worker_num]
```

start_port: the listen port number of the first worker instance.

worker_num: the number of worker instances.

