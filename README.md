<p align="center">
  <img width="500" height="220" src="https://github-production-user-asset-6210df.s3.amazonaws.com/87842051/293287492-574661fe-a0fb-489a-bc99-027cf6af3460.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAVCODYLSA53PQK4ZA%2F20231228%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231228T231513Z&X-Amz-Expires=300&X-Amz-Signature=a5e1d70ed9131d9b35919500b8ed4d5e8579b8ff41139011d41297cbc15e8423&X-Amz-SignedHeaders=host&actor_id=87842051&key_id=0&repo_id=474514659">
</p>


# Parallel Private Retrieval of Merkle/Verkle Proofs via Tree Colorings

---
## Experimental setup
The experiments in the report were run in an Ubuntu 22.04 LTS environment. The Verkle tree nodes are 32 bytes in size. Each experiment was repeated ten times for various trees (see Table below), changing the number of leaves ($n$) from $2^{10}$ to $2^{24}$ and the number of children ($q$) in the set $\{2, 16, 128, 256\}$. The average values were then calculated.

<!-- Table 1 -->
\begin{table}[ht]
    \centering
    \begin{tabular}{|c|c|p{0.3cm}|p{0.3cm}|p{0.3cm}|p{0.3cm}|p{0.3cm}|p{0.3cm}|p{0.3cm}|p{0.3cm}|p{0.3cm}|p{0.3cm}|p{0.3cm}|p{0.3cm}|p{0.3cm}|p{0.3cm}|p{0.3cm}|p{0.3cm}|p{0.3cm}|}
        \hline
        \multicolumn{2}{|c|}{$h$} & \multicolumn{15}{c|}{$n$} \\
        \cline{3-17}
        \multicolumn{2}{|c|}{} & $2^{10}$ & $2^{11}$ & $2^{12}$ & $2^{13}$ & $2^{14}$ & $2^{15}$ & $2^{16}$ & $2^{17}$ & $2^{18}$ & $2^{19}$ & $2^{20}$ & $2^{21}$ & $2^{22}$ & $2^{23}$ & $2^{24}$\\
        \hline
         & $2$ & $10$ & $11$ & $12$ & $13$ & $14$ & $15$ & $16$ & $17$ & $18$ & $19$ & $20$ & $21$ & $22$ & $23$ & $24$ \\
        \cline{2-17}
        \multirow{$q$} & $16$ & $-$ & $-$ & $3$ & $-$ & $-$ & $-$ & $4$ & $-$ & $-$ & $-$ & $5$ & $-$ & $-$ & $-$ & $6$ \\
        \cline{2-17}
         & $128$ & $-$ & $-$ & $-$ & $-$ & $2$ & $-$ & $-$ & $-$ & $-$ & $-$ & $-$ & $3$ & $-$ & $-$ & $-$ \\
        \cline{2-17}
        & $256$ & $-$ & $-$ & $-$ & $-$ & $-$ & $-$ & $2$ & $-$ & $-$ & $-$ & $-$ & $-$ & $-$ & $-$ & $3$ \\
        \hline
    \end{tabular}
    \caption{A comprehensive experimental evaluation across varying $q$-ary tree sizes ($2^{10}$ to $2^{24}$ leaves ($n$)), children numbers ($2$ to $256$ ($q$)), and tree heights ($h$).}
    \label{table:expTrees}
\end{table}

<!-- Table 2 -->
\begin{table}[ht]
    \centering
    \begin{tabular}{|c|c|p{0.3cm}|p{0.3cm}|p{0.3cm}|p{0.3cm}|p{0.3cm}|p{0.3cm}|p{0.3cm}|p{0.3cm}|p{0.3cm}|p{0.3cm}|p{0.3cm}|p{0.3cm}|p{0.3cm}|p{0.3cm}|p{0.3cm}|p{0.3cm}|p{0.3cm}|}
        \hline
        \multicolumn{2}{|c|}{\# servers (CTA)} & \multicolumn{15}{c|}{$n$} \\
        \cline{3-17}
        \multicolumn{2}{|c|}{} & $2^{10}$ & $2^{11}$ & $2^{12}$ & $2^{13}$ & $2^{14}$ & $2^{15}$ & $2^{16}$ & $2^{17}$ & $2^{18}$ & $2^{19}$ & $2^{20}$ & $2^{21}$ & $2^{22}$ & $2^{23}$ & $2^{24}$\\
        \hline
         & $2$ & $10$ & $11$ & $12$ & $13$ & $14$ & $15$ & $16$ & $17$ & $18$ & $19$ & $20$ & $21$ & $22$ & $23$ & $24$ \\
        \cline{2-17}
        \multirow{$q$} & $16$ & $-$ & $-$ & $3$ & $-$ & $-$ & $-$ & $4$ & $-$ & $-$ & $-$ & $5$ & $-$ & $-$ & $-$ & $6$ \\
        \cline{2-17}
         & $128$ & $-$ & $-$ & $-$ & $-$ & $2$ & $-$ & $-$ & $-$ & $-$ & $-$ & $-$ & $3$ & $-$ & $-$ & $-$ \\
        \cline{2-17}
        & $256$ & $-$ & $-$ & $-$ & $-$ & $-$ & $-$ & $2$ & $-$ & $-$ & $-$ & $-$ & $-$ & $-$ & $-$ & $3$ \\
        \hline
    \end{tabular}
    \caption{Active PIR servers required to handle $h$ concurrent client queries, across varied $q$-ary tree configurations ($2^{10}$ to $2^{24}$ leaves ($n$), and $2$ to $256$ children ($q$)) when each server stores one color database.}
    \label{table:CTAservers}
\end{table}

<!-- Table 3 -->
\begin{table}[ht]
    \centering
    \begin{tabular}{|c|c|p{0.3cm}|p{0.3cm}|p{0.3cm}|p{0.3cm}|p{0.3cm}|p{0.3cm}|p{0.3cm}|p{0.3cm}|p{0.3cm}|p{0.3cm}|p{0.3cm}|p{0.3cm}|p{0.3cm}|p{0.3cm}|p{0.3cm}|p{0.3cm}|p{0.3cm}|}
        \hline
        \multicolumn{2}{|c|}{\# servers (PBC)} & \multicolumn{15}{c|}{$n$} \\
        \cline{3-17}
        \multicolumn




---
## ACKNOWLEDGMENTS 
This work was supported by the Australian Research Council through the Discovery Project under Grant DP200100731. Additionally, it was supported through Academic Grants Round 2022 by Ethereum Foundation and received support from the RACE Merit Allocation Scheme (RMAS) in 2024 via the RMIT AWS Cloud Supercomputing Hub in Melbourne, Victoria, Australia, with the grant number RMAS00012.
