<p align="center">
  <img width="500" height="220" src="https://github.com/cnquang/cnquang/assets/87842051/03c984eb-31c0-4f63-a07b-6edacc8daa47">
</p>


# Parallel Private Retrieval of Merkle/Verkle Proofs via Tree Colorings

---
## Experimental setup
The experiments in the report were run in an Ubuntu 22.04 LTS environment. The Verkle tree nodes are 32 bytes in size. Each experiment was repeated ten times for various trees (see Table 4), changing the number of leaves ($n$) from $2^{10}$ to $2^{24}$ and the number of children ($q$) in the set $\{2, 16, 128, 256\}$. The average values were then calculated.

<p align="center">
  <img width="600" height="700" src="https://github-production-user-asset-6210df.s3.amazonaws.com/87842051/293293909-fc0d53ea-be98-441c-b3f9-39abe2fd4209.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAVCODYLSA53PQK4ZA%2F20231229%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231229T004705Z&X-Amz-Expires=300&X-Amz-Signature=916eb9f847654a053f2089eae15ea8eb7a3b619a913259f499413240611b5360&X-Amz-SignedHeaders=host&actor_id=87842051&key_id=0&repo_id=474514659">
</p>

Our local machine (Intel® Core™ i5-1035G1 CPU @ 1.00GHz×8, 15GB System memory) was employed for the PIR Client and Orchestrator (see Figure 14). For PIR Servers, we ran our experiments using up to 36 PIR servers on the Amazon m5.8xlarge instance (Intel® Xeon® Platinum 8175M CPU @ 2.50GHz, 32 vCPUs, 128GB System memory) that cost around $\$1.92$ per hour, using only one core. In Table 5 and Table 6, we used until $36$ instances because, with h = 24, PBC generates $1.5 \times h = 36$ databases, each of server processed a PIR database in parallel while our CTA employed only $24$ servers. We choose an arbitrary C-PIR such as SealPIR for our baseline implementations.

<p align="center">
  <img width="500" height="250" src="https://github-production-user-asset-6210df.s3.amazonaws.com/87842051/293294359-1b853360-f044-4b20-bc8b-b54426a19996.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAVCODYLSA53PQK4ZA%2F20231229%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231229T005503Z&X-Amz-Expires=300&X-Amz-Signature=c17cd7364c5c6785834e0764c65c6d303bbe4b5ff6695ef42c184783a4edaad0&X-Amz-SignedHeaders=host&actor_id=87842051&key_id=0&repo_id=474514659">
</p>

---
## Installing Libraries

- ##### Javac
      $ sudo apt update
      $ sudo apt upgrade
      $ sudo apt install default-jdk

- ##### SEAL 4.0.0
      $ sudo apt install build-essential cmake clang git g++ libssl-dev libgmp3-dev
      $ sudo apt update
      $ sudo apt upgrade
      $ git clone https://github.com/cnquang/SEAL-4.0.0.git
      $ cd SEAL-4.0.0
      $ cmake -S . -B build
      $ cmake --build build
      $ sudo cmake --install build

- ##### JSON
      $ git clone https://github.com/microsoft/vcpkg
      $ ./vcpkg/bootstrap-vcpkg.sh
      $ ./vcpkg install rapidjson

- ##### Google gRPC
      $ sudo apt install -y build-essential autoconf libtool pkg-config
      $ git clone --recurse-submodules -b v1.58.0 --depth 1 --shallow-submodules https://github.com/grpc/grpc
      $ cd grpc
      $ mkdir -p cmake/build
      $ pushd cmake/build
      $ cmake -DgRPC_INSTALL=ON \
        -DgRPC_BUILD_TESTS=OFF \
        ../..
      $ make -j 4
      $ sudo make install
      $ popd

---
## Network Settings
      
- ### On AWS
  Create EC2 instances on AWS, the number of instances based on the tree's height (See Table 5 and Table 6).
  Ensure all the instances have TCP allow ports in the 0 to 65535 range. Connect all instances via SSH (See Figure below - Edit inbound rules).

<p align="center">
  <img width="600" height="300" src="https://github-production-user-asset-6210df.s3.amazonaws.com/87842051/293305599-4987b5cc-c7dc-47f6-9413-49b6021f9930.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAVCODYLSA53PQK4ZA%2F20231229%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231229T033445Z&X-Amz-Expires=300&X-Amz-Signature=508fd19b27a657e01beb5fe38fcc54ab00c36850d52c5a6e58bbff2de89e4f38&X-Amz-SignedHeaders=host&actor_id=87842051&key_id=0&repo_id=474514659">
</p>

- ### On the local machine
  Open the **Orchestrator folder** and add the list of Public IPv4 addresses of each instance in each line of the *list_servers_IPs.txt*.
  
  #### Open the terminal
      $ cd Orchestrator
      $ python3 orchestrator.py <parameter1: (h)> <parameter2: (q)>
      $ Example: python3 main.py 4 4
  All the local machine and instances' logs will be stored in the Logs folder.

  #### Plotting
      $ cd Logs/figures
      $ python3 figures.py
  All the figures will be created the same as in the report.
  
---
## ACKNOWLEDGMENTS 
This work was supported by the Australian Research Council through the Discovery Project under Grant DP200100731. Additionally, it was supported through Academic Grants Round 2022 by the Ethereum Foundation and received support from the RACE Merit Allocation Scheme (RMAS) in 2024 via the RMIT AWS Cloud Supercomputing Hub in Melbourne, Victoria, Australia, with the grant number RMAS00012.
