#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

set -v
SECONDS=0
../phraseCount.py << EOF
The human homologue of murine double minute 2 (HDM2) and HDM4 negatively regulate p53.
HDM4 has not been assessed in acute myeloid leukemia (AML) or myelodysplastic syndrome (MDS).
We examined the expression of HDM4 and the short splicing variant, HDM4-S, in bone marrow samples obtained from 85 and 23 patients with AML and MDS, respectively, and 18 negative tumor staging bone marrow samples (used as the control).
Immunohistochemical staining showed that HDM4 was overexpressed in 78 AML cases (92%) and 12 MDS cases (52%) compared with 1 stressed bone marrow sample (6%).
Quantitative reverse transcriptase-polymerase chain reaction analysis of 8 AML and 11 low-grade (LG)-MDS cases confirmed that HDM4 and HDM4-S mRNA expression were also elevated in all AML cases.
HDM4 and HDM4-S mRNA expression was elevated in 3 (27%) and 10 (91%) LG-MDS cases, respectively.
HDM4 and HDM4-S mRNA levels were higher in those with AML than in those with LG-MDS.
In leukemia cell lines, HEL and U937 predominantly expressed HDM4-S.
In contrast, NALM6 expressed HDM4 and HDM4-S.
Downregulation of HDM4 expression by treatment with small interfering RNA in NALM6 and HEL cells induced p21 expression but not increased apoptotic activity.
Our results indicate that HDM4 is a potential therapeutic target in patients with AML or MDS.
The human homologue of murine double minute 2 (HDM2) and HDM4 negatively regulate p53.
HDM4 has not been assessed in acute myeloid leukemia (AML) or myelodysplastic syndrome (MDS).
We examined the expression of HDM4 and the short splicing variant, HDM4-S, in bone marrow samples obtained from 85 and 23 patients with AML and MDS, respectively, and 18 negative tumor staging bone marrow samples (used as the control).
Immunohistochemical staining showed that HDM4 was overexpressed in 78 AML cases (92%) and 12 MDS cases (52%) compared with 1 stressed bone marrow sample (6%).
Quantitative reverse transcriptase-polymerase chain reaction analysis of 8 AML and 11 low-grade (LG)-MDS cases confirmed that HDM4 and HDM4-S mRNA expression were also elevated in all AML cases.
HDM4 and HDM4-S mRNA expression was elevated in 3 (27%) and 10 (91%) LG-MDS cases, respectively.
HDM4 and HDM4-S mRNA levels were higher in those with AML than in those with LG-MDS.
In leukemia cell lines, HEL and U937 predominantly expressed HDM4-S.
In contrast, NALM6 expressed HDM4 and HDM4-S.
Downregulation of HDM4 expression by treatment with small interfering RNA in NALM6 and HEL cells induced p21 expression but not increased apoptotic activity.
Our results indicate that HDM4 is a potential therapeutic target in patients with AML or MDS.
EOF
duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed."

SECONDS=0
../phraseCount.py << EOF
The human homologue of murine double minute 2 (HDM2) and HDM4 negatively regulate p53.
HDM4 has not been assessed in acute myeloid leukemia (AML) or myelodysplastic syndrome (MDS).
EOF
duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed."
