# Analyza_transkriptomu_DP
Tento GitHub repozitář byl vytvořen k uložení skriptů a výsledných souborů diplomové práce "**Analýza transkriptomu tasemnice *Mesocestoides corti***"

### Skripty napsané v programovacím jazyku Python
- Vzorová testovací data jsou k dispozici ve složce `Testovaci_soubory`

`filtering_ncbi.py`
* Slouží k výběru jedné konkrétní anotace z 5 různých NCBI anotací u každého transkriptu primárně na základě funkční anotace genu a sekundárně podle nejvyšší hodnoty bit_score

`transcriptoms_annotation.py`
* Provádí anotaci všech transkriptů s hodnotou *expected counts* větší či rovné 10 všech replikátů konkrétního vzorku (**B**, **ICR**, **IV**)

`diffexpr_annotation.py`
* Slučuje tabulku s diferenciálně exprimovanými transkripty jednotlivých dvojic replikátů (**B&IV**, **ICR&IV**, **B&ICR**) s KEGG a NCBI anotacemi na základě unikátního identifikátoru každého transkriptu

`gene_enrichment.py`
* Provádí analýzu genového obohacení (gene enrichment analysis) pomocí Fisherova exaktiního testu


### Výsledné soubory
``Anotované transkriptomy``
* Obsahuje soubory s anotovanými transkriptomy pro každý vzorek (**B_transcriptome_annotaion.xlsx**, **ICR_transcriptome_annotation.xlsx**, **IV_transckriptome_annotation.xlsx**)

``Diferenciální exprese anotovaných transkriptů``
* Obsahuje soubory s diferenciálně exprimovanými transkripty anotovanými pomocí KEGG a NCBI databáze pro každou dvojici vzorků (**B&ICR_diffexprese_anotace.xlsx**, **B&IV_diffexprese_anotace.xlsx**, **ICR&IV_diffexprese_anotace.xlsx**)

``Gene enrichment``
* Obsahuje soubory s provedenou analýzou genového obohacení (gene enrichment analysis) biologických drah pomocí Fisherova exaktního testu pro každou dvojici vzorků (**B&ICR_diffexprese_anotace.xlsx**, **B&IV_diffexprese_anotace.xlsx**, **ICR&IV_diffexprese_anotace.xlsx**) 
