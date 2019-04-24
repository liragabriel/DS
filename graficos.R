library(dplyr)
library(plyr)
library(sqldf)
library(ggplot2)

access <- read.csv('/home/desktop/dev/jupyter/DS/websvc_access.csv')
access <- select(access,-c(fora))
head(access)


acessos_por_usuario <- function(){
    usuarios <- select(access, c(usuario))
    usuarios <- data.frame(usuarios)
    
    acessos <- table(usuarios)
    data_acessos <- data.frame(acessos)
    
    jpeg('user.jpg')
    barplot(acessos, main='Acessos por Usuário')
    dev.off()
}

acessos_por_url <- function(){
    urls <- select(access, c(url))
    urls <- table(urls)
    urls <- data.frame(urls)
    urls <- sqldf('SELECT urls,Freq FROM urls Order BY Freq')
    urls <- sqldf('SELECT urls, Freq FROM urls Where Freq > 1000')
    
    print(urls)
}

status_code <- function(){
    status <- select(access, c(status_code))
    status <- data.frame(status)
    status <- table(status)
    
    jpeg('status.jpg')
    barplot(status, main='Status Code')
    dev.off()
}

acessos_por_usuario()
acessos_por_url()
status_code()
