<p align="center">
  <img width="500" height="220" src="https://github-production-user-asset-6210df.s3.amazonaws.com/87842051/293287492-574661fe-a0fb-489a-bc99-027cf6af3460.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAVCODYLSA53PQK4ZA%2F20231228%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231228T231513Z&X-Amz-Expires=300&X-Amz-Signature=a5e1d70ed9131d9b35919500b8ed4d5e8579b8ff41139011d41297cbc15e8423&X-Amz-SignedHeaders=host&actor_id=87842051&key_id=0&repo_id=474514659">
</p>


# Parallel Private Retrieval of Merkle/Verkle Proofs via Tree Colorings

---
## Experimental setup
The experiments in the report were run in an Ubuntu 22.04 LTS environment. The Verkle tree nodes are 32 bytes in size. Each experiment was repeated ten times for various trees (see Table 4), changing the number of leaves ($n$) from $2^{10}$ to $2^{24}$ and the number of children ($q$) in the set $\{2, 16, 128, 256\}$. The average values were then calculated.

<p align="center">
  <img width="600" height="700" src="https://github-production-user-asset-6210df.s3.amazonaws.com/87842051/293293909-fc0d53ea-be98-441c-b3f9-39abe2fd4209.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAVCODYLSA53PQK4ZA%2F20231229%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231229T004705Z&X-Amz-Expires=300&X-Amz-Signature=916eb9f847654a053f2089eae15ea8eb7a3b619a913259f499413240611b5360&X-Amz-SignedHeaders=host&actor_id=87842051&key_id=0&repo_id=474514659">
</p>

Our local machine (Intel® Core™ i5-1035G1 CPU @ 1.00GHz×8, 15GB System memory) was employed for the PIR Client and Orchestrator (see Figure \ref{fig:orchestrator}). For PIR Servers, we ran our experiments using up to 36 PIR servers on the Amazon m5.8xlarge instance (Intel® Xeon® Platinum 8175M CPU @ 2.50GHz, 32 vCPUs, 128GB System memory) that cost around $\$1.92$ per hour, using only one core. In Table 5 and Table 6, we used until $36$ instances because, with h = 24, PBC generates $1.5 \times h = 36$ databases, each of server processed a PIR database in parallel while our CTA employed only $24$ servers. We choose an arbitrary C-PIR such as SealPIR \cite{angel2018} for our baseline implementations.


---
## ACKNOWLEDGMENTS 
This work was supported by the Australian Research Council through the Discovery Project under Grant DP200100731. Additionally, it was supported through Academic Grants Round 2022 by Ethereum Foundation and received support from the RACE Merit Allocation Scheme (RMAS) in 2024 via the RMIT AWS Cloud Supercomputing Hub in Melbourne, Victoria, Australia, with the grant number RMAS00012.
