corr <- read.csv("corr.csv")
corr <- as.matrix(corr)
rownames(corr) <- colnames(corr)
hc <- hclust(as.dist(exp(-corr)), 'ave')
perm <- hc$order
sub <- 31:60
corr <- corr[perm[sub], perm[sub]]

corr[upper.tri(corr,diag=F)]<-NA #We only want to plot 1/2 the matrix

pd<-melt(t(corr),value.name='Correlation')

pd$Var2 <- factor(as.character(pd$Var2), levels=rev(as.character(levels(pd$Var1))))

p<-ggplot(data=pd,aes(x=Var1,y=Var2,fill=Correlation,label=Correlation))+geom_raster()
p<-p+geom_raster()+theme_bw()+labs(title='The Raw Plot')


p<-p+scale_fill_gradient2(name='Correlation',na.value='white') #create a diverging color gradient
p+labs(title='Now we have a diverngent Color Scale')

p<-p+theme(panel.border=element_rect(colour=NULL,fill=NULL),panel.grid.major=element_line(colour=NULL),axis.text=element_text(size=8),axis.text.x=element_text(size=8,angle=25, hjust = 1))

p<-p+scale_x_discrete(expand=c(0,0))+scale_y_discrete(expand=c(0,0))

p<-p+labs(x='',y='',title='Cosine Similarity between Painters')
p+coord_equal()

print(p)
ggsave(filename = "~/Dropbox/Slides/Insight/figure/similarity.png", width=22, height = 20)
