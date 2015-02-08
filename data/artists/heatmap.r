library(reshape2)
library(ggplot2)

# set up ggplot theme
theme_set(theme_bw())
theme_update(legend.background = element_rect(colour="transparent", fill="transparent"),
	panel.grid.major = element_blank(),
	panel.grid.minor = element_blank()
)
corr <- read.csv("corr.csv")
corr <- as.matrix(corr)
colnames(corr) <- gsub("\\.", " ", colnames(corr))
rownames(corr) <- colnames(corr)
hc <- hclust(as.dist(exp(-corr)), 'ave')
perm <- hc$order
sub <- 31:60
corr.30 <- corr[perm[sub], perm[sub]]

corr.30[upper.tri(corr.30,diag=F)]<-NA #We only want to plot 1/2 the matrix

pd<-melt(t(corr.30),value.name='Correlation')

pd$Var2 <- factor(as.character(pd$Var2), levels=rev(as.character(levels(pd$Var1))))

p<-ggplot(data=pd,aes(x=Var1,y=Var2,fill=Correlation,label=Correlation))+geom_raster()
p<-p+geom_raster()+theme_bw()+labs(title='The Raw Plot')

p<-p+scale_fill_gradient2(name='Correlation',na.value='white') #create a diverging color gradient
p+labs(title='Now we have a diverngent Color Scale')

p<-p+theme(panel.border=element_rect(colour=NULL,fill=NULL),panel.grid.major=element_line(colour=NULL),axis.text=element_text(size=8),axis.text.x=element_text(size=8,angle=45, hjust = 1))

p<-p+scale_x_discrete(expand=c(0,0))+scale_y_discrete(expand=c(0,0))

p<-p+labs(x='',y='',title='Cosine Similarity between Painters')
p+coord_equal()

print(p)
ggsave(filename = "~/Dropbox/Slides/Insight/figure/similarity.png", width=7, height = 6)


## comparing three schools of painters

impressionist = c("Claude Monet", "Pierre Auguste Renoir", "Edgar Degas", "Georges Seurat")

classical= c("Raphael", "Sandro Botticelli", "Leonardo da Vinci", "Michelangelo")

dutch = c("Rembrandt", "Johannes Vermeer", "Peter Paul Rubens", "Frans Hals")

abstract= c("Mark Rothko", "Jackson Pollock", "Willem de Kooning", "Georgia O Keeffe")

post = c("Paul Cezanne", "Vincent van Gogh", "Paul Gauguin", "Henri Matisse")

index = match(c(impressionist, dutch, classical, abstract, post), rownames(corr))

index.impressionist = match(impressionist, rownames(corr))
index.classical = match(classical, rownames(corr))
index.dutch = match(dutch, rownames(corr))
index.abstract = match(abstract, rownames(corr))
index.post = match(post, rownames(corr))

corr.impressionist <- corr[index.impressionist, index.impressionist]
corr.classical <- corr[index.classical, index.classical]
corr.dutch <- corr[index.dutch, index.dutch]
corr.post <- corr[index.post, index.post]
corr.abstract <- corr[index.abstract, index.abstract]

mds <- cmdscale(as.dist((1-corr)/2))
plot(mds, type="n")
text(mds, labels=rownames(mds))
pdata=as.data.frame(mds[index, ])
colnames(pdata) <- c("x", "y")
pdata['label'] <- rownames(pdata)
pdata['genre'] <- rep(c("impressionist", "classical", "dutch", "abstract", 'post-imp'), rep(4, 5))

p <- ggplot(data=pdata, aes(x=x, y=y, label=label, color=factor(genre)))
p <- p + geom_text() + labs(x="Component 1", y="Component 2", title="Separation of Genres using Cosine Similarity") + scale_color_tableau()
print(p)
ggsave(filename = "~/Dropbox/Slides/Insight/figure/separation.png", width=10, height = 8)
text(mds[index, ], labels=rownames(mds[index, ]), col=rep(1:5, rep(4,5)))
