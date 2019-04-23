library(dplyr)

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
    urls <- data.frame(urls)
    urls <- table(urls)
    
    jpeg('url.jpg')
    barplot(urls, main='Acessos por URL')
    dev.off()
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
