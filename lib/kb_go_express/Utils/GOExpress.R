
## 1. x= cond , Return a list where names are "conditions" and values are "sample names"
#
cond2Sample <- function(file_condition_sample) {
  
  cond2sample <- read.table(textConnection(gsub(":", ",", readLines(file_condition_sample))), sep = ",", fill = T, header = F, stringsAsFactors = F)## opt$cond = file_condition_sample is opt$cond
  
  cond = cond2sample[[1]]
  cond2sample_list = apply(cond2sample, 1, function(x) {list(x[2:length(x)])})
  names(cond2sample_list) = cond
  
  #a list where names are "conditions" and values are "sample names"
  cond2sample_list <- lapply(cond2sample_list, function(x) {
    snames = as.vector(x[[1]])
    snames = snames[snames != ""]})
  
  return(cond2sample_list)
  
}
  

## 2. x = expMatrix, Return a list whose elements are "eSet class" objects having names "conditinalPairs"...may need to call function 1
condPair_Eset <- function(file_expression_matrix, cond2sample_list = cond2sample_list) {

  fpkmCounts <- read.table(file_expression_matrix, header = T, sep = "\t", fill = T, check.names = F, row.names = 1)

  exprs <- as.matrix(fpkmCounts)
  
  ##converting the expression matrixinto minimal set matrix 
  minimalSet <- ExpressionSet(assayData = exprs)
  
  pData <- data.frame(condition = c(rep(names(cond2sample_list), 
                                        as.vector(vapply(cond2sample_list, function(x) { length(x) }, 
                                                         FUN.VALUE = numeric(1))))),
                      
                      stringsAsFactors = T)
  
  
  
  rownames(pData) <- as.vector(unlist(cond2sample_list))
  
  
  exprs <- exprs[,rownames(pData)] #reordering the columns of expression matrix based on pData rows!
  
  ##creating 'phenoData' object from the AnnotatedDataFrame Class
  phenoData <- new("AnnotatedDataFrame", data = pData)
  
  
  ##Building 'fpkm_eset' Eset object using 1) Expression matrix 2) phenoData 3) annotation
  fpkm_eset <- ExpressionSet(assayData = exprs, phenoData = phenoData)
  
  
  pairwise <- as.data.frame(combn(names(cond2sample_list), 2))
  pairwise[] <- lapply(pairwise, as.character)
  
  cond_pairs <- vapply(pairwise, function(x){paste(gsub(" ","_",x[1]), gsub(" ","_",x[2]), sep = "_VS_") }, FUN.VALUE = character(1))
  cond_pairs <- as.vector(cond_pairs)
  
  cond_pairs2sample <- lapply(pairwise, function(x){ c(cond2sample_list[[x[[1]]]], cond2sample_list[[x[[2]]]])})
  names(cond_pairs2sample) <- cond_pairs
  
  fpkm_cond_pairs <- lapply(cond_pairs2sample, function(x) { 
    fpkm_eset_cond <- fpkm_eset[,x]
    fpkm_eset_cond <- fpkm_eset_cond[rowSums(exprs(fpkm_eset_cond)) > 1, ]
    pData(fpkm_eset_cond)$condition <- droplevels(pData(fpkm_eset_cond)$condition)
    return(fpkm_eset_cond)
  })
  
  return(fpkm_cond_pairs)
}

##6. x= "List object from function 2", y = "allGO" ...Return - permuation Test Results

PermutationTest <- function (condPair_eset, all_GO, GO_genes, all_genes, N) {
  
  set.seed(4543) #set random seed for reproducibility
  results <- GO_analyse(eSet = condPair_eset, f = "condition", 
                               GO_genes = GO_genes, 
                               all_GO = all_GO, 
                               all_genes = all_genes)# pairs 
  
  ###Permutation-based P-value for ontologies
  #####Recommended N is 1000 ...could be performed on Newton
  
  results.pVal = pValue_GO(result = results, N = N) ###modify the N parameter     opt$N
  #####to scale it up to 1000
  
  return(results.pVal)
}


  ## 3. x= Permutation Test Result, Return 1) HMAPS 2) .csv files
#output is data object for the csv file  
  
BP_Ontology <- function(resultPval, condPair) {
  
  BP_5  <- subset_scores(result = resultPval,
                         namespace = "biological_process",
                         total = 5, # requires 5 or more associated genes
                         p.val = 0.05)
  
  write.csv(BP_5$GO, file = paste(result_path,
                                             paste(condPair, "BP_5.csv", sep = "."),
                                             sep = "/"))
  return(BP_5)
  
}

## 4.x =  Permutation Test Result 1) HMAps 2).csv files
MF_Ontology <- function(resultPval, condPair) {
  
  MF_10  <- subset_scores(result = resultPVal,
                         namespace = "molecular_function",
                         total = 10, # requires 5 or more associated genes
                         p.val = 0.05)
  
  write.csv(x = MF_10$GO, file = paste(result_path,
                                             paste(condPair, "MF_10.csv", sep = "."),
                                             sep = "/"))
  return(MF_10)
  
}



##5.x =  Permutation Test Result 1)HMAPS 2) .csv files 
CC_Ontology <- function(resultPval = resultPVal, condPair) {
  
  CC_15<- subset_scores(result = resultPVal, 
                        namespace = "cellular_component",
                        total = 15, # requires 5 or more associated genes
                        p.val = 0.05)

  write.csv(CC_15$GO, file = paste(result_path,
                                        paste(condPair, "CC_15.csv", sep = "."),
                                        sep = "/"))
  return(CC_15)
  
}


#Merge ontology objects

mergeGO<- function(BP, MF, CC) {
  rbind.data.frame(BP$GO, MF$GO, CC$GO)
}



.libPaths( c( .libPaths(), "/kb/deployment/lib") )
##Load the packages

library(GOexpress)
library(Biobase)
library(gplots)
library(optparse)

##Reading command-line arguments in R

option_list = list(
  make_option(c("--expMatrix"), type="character", default=NULL, 
              help="normalised expression matrix file name"),
  
  make_option(c("--gi2go"), type="character", default=NULL, 
              help= "tsv file with gene identifier to GO identifier map"),
  
  make_option(c("--goDes"), type="character", default=NULL, 
              help="csv file having the fields GO_ID, GO_Term, GO_ROOT_TERM respectively"),
  
  make_option(c("--geneDes"), type="character", default=NULL, 
              help="tsv file having the fields geneID, gene_name and gene_description respectively"),
  
  make_option(c("--Nper"), type = "integer", default=1000, dest = "N", 
              help="Number of permutations >= 1000"),
  
  make_option(c("--outDir"), type = "character", default=NULL,
              help="provide an ouput directory"),
  
  make_option(c("--cond"), type = "character", default=NULL,
              help= "provide the formatted file showing condtion:sample relatioship")
  
)

opt_parser = OptionParser(option_list=option_list)
opt = parse_args(opt_parser)

###########################################

result_path <- paste(opt$outDir, sep = "/")# provide full path to the OUT DIR opt$outDir opt$outDir
print(result_path)
ifelse(!dir.exists(result_path), dir.create(result_path), F)

##Reading the geneDescription file 

allgenes <- read.table(file = opt$geneDes, header = T, sep = "\t", stringsAsFactors = F, 
                       fill = T)# opt$geneDes-
#allgenes$external_gene_name <- sub(":$", "", paste(allgenes$gene_id, allgenes$description, sep = ":"))
#allgenes <- allgenes[,c(1,3,2)]


write.table(allgenes, "file=test.txt", sep="\t")


##Preparing the GO and genes related annotation Files #############

allGO <- read.table(opt$goDes, sep='\t', header = T, stringsAsFactors = F)#opt$goDes--Ptrichocarpa_210_v3.0.allGO.txt

GOgenes <- read.table(opt$gi2go, header = T, sep = "\t", stringsAsFactors = F) # opt$gi2go -- Ptrichocarpa_210_v3.0.gi_go.txt

## Arguments passed...

file_condition_sample = opt$cond#opt$cond #out.txt

cond2sample_list = cond2Sample(file_condition_sample = file_condition_sample)

##fpkm_counts_with_snames.tsv is the first file to be read 
file_name <- opt$expMatrix #opt$expMatrix 
  
fpkm_cond_pairs <- condPair_Eset(file_expression_matrix = file_name , cond2sample_list = cond2sample_list)



i <- 0


AllCombined = data.frame()
for (pairs in fpkm_cond_pairs) {
  
  print(pairs)

  i <- i+1
##Running Random Forrest Algorithm with Local Annotations##
  condPair <- names(fpkm_cond_pairs)[i]
  print(condPair)
  resultPVal <- PermutationTest(condPair_eset = pairs, 
                                all_GO = allGO, GO_genes = GOgenes, all_genes = allgenes, 
                                N = opt$N) #opt$N
  
  BP_5 <- BP_Ontology(resultPVal, condPair = condPair)
  MF_10 <- MF_Ontology(resultPVal, condPair = condPair)
  CC_15 <- CC_Ontology(resultPval, condPair = condPair)
  
  combinedGO <-mergeGO(BP_5, MF_10, CC_15)
  combinedGO[["condition1"]] <- rep(strsplit(condPair, split = "_VS_", perl = T)[[1]][1], nrow(combinedGO))
  combinedGO[["condition2"]] <- rep(strsplit(condPair, split = "_VS_", perl = T)[[1]][2], nrow(combinedGO))
  
  ##Log2+1 Fpkm count transformation of the expression matrix for visualisation of the data on heatmap
  temp_exp <- exprs(pairs)
  temp_log <- log2(temp_exp + 1)
  cond_pair_logTransformed <- ExpressionSet(assayData = temp_log,  phenoData = phenoData(pairs))
  
  #######Hierarchial clustering of samples based on gene expression associated with each GO term##
  fpHMAP_all = character()
  
  for (parents in c("BP_5", "MF_10", "CC_15")) {
    ##Try to assert if the go_ids exist and not an empty vector???
    
    go_ids <- get(parents)$GO$go_id # get a list of significantly enriched go_ids from the associated PARENT GO ID
    c <- 0
    for (id in go_ids) {
      
      c <- c+1 # the suffix c to preserve order to siginifcant GO_IDs
      
      full_path_HMAP <- paste(result_path,
                              paste(condPair, parents, c, "png", sep = "."), 
                              sep = "/")
      fpHMAP_all <- c(fpHMAP_all, full_path_HMAP)
      print(fpHMAP_all)
      png(full_path_HMAP, height = 5*300, width = 5*300, res=300, pointsize = 8)
     
      
    
      
      heatmap_GO(go_id = id, result = get(parents), eSet = cond_pair_logTransformed, gene_names = T,
                 cexCol = 1, cexRow = 1, cex.main = 1, main.Lsplit = 30, 
                 margins = c(13, 8), srtCol = 30, 
                 offsetRow = -0.6, offsetCol = -0.5)
      
      dev.off()
    }
     
  } 
  
  combinedGO$pathToHMAP <- fpHMAP_all
  
  #writing for BP,MF,CC for a SINGLE CONDITIONAL PAIR
  write.csv(combinedGO, paste(result_path,paste0(condPair,".csv"), sep = "/"))
  AllCombined <- rbind.data.frame(AllCombined,combinedGO)
}

#writing to a File -with BP, MF, CC across ALL POSSIBLE CONDITIONAL PAIRS
write.csv(AllCombined, file = paste(result_path,paste0("AllCombined",".csv"), sep = "/"))


