library(ggplot2)
library(reshape)
library(ggstance)
library(dendextend)
library(scales)
library(dplyr)
library(tidyverse)
library(gridExtra)
library(leaflet)

# library(ape)
# library(devtools)
# library(plyr)
# library(raster)
# library(leaflet.extras)
# library(magrittr)
# library(ape)
# library(ggplot2)
# library(Rling)
# library(rgl)
# library(plotly)
# library(Hmisc)
# library(shiny)
# library(gg3d)
# library(stats)
# library(ggmap)
# library(stringr)
# library(reshape2)


# normalized data used in the analysis
timok_data_norm = read.csv("data/timok_features_norm.txt", sep = "\t", header = TRUE)

# adding metadata for the analysis of geographic and demographic factors (Section 5.1. and Appendix 1)
timok_locations = read.csv("data/timok_locations.csv", sep = "\t", header = TRUE, stringsAsFactors = TRUE)
timok_speakers = read.csv("data/timok_speakers.csv", sep = ",", header = TRUE, stringsAsFactors = TRUE)



# statistics and distribution for each feature (Section 5.1)

#accent
plot(density(timok_data_norm$accent_prop))
shapiro.test(timok_data_norm$accent_prop)
min(timok_data_norm$accent_prop)
max(timok_data_norm$accent_prop)
median(timok_data_norm$accent_prop)
mean(timok_data_norm$accent_prop)
sd(timok_data_norm$accent_prop)


# si
plot(density(timok_data_norm$si_norm))
shapiro.test(timok_data_norm$si_norm)
min(timok_data_norm$si_norm)
max(timok_data_norm$si_norm)
median(timok_data_norm$si_norm)
mean(timok_data_norm$si_norm)
sd(timok_data_norm$si_norm)


# perf
plot(density(timok_data_norm$perf_norm))
shapiro.test(timok_data_norm$perf_norm)
min(timok_data_norm$perf_norm)
max(timok_data_norm$perf_norm)
median(timok_data_norm$perf_norm)
mean(timok_data_norm$perf_norm)
sd(timok_data_norm$perf_norm)

# art
plot(density(timok_data_norm$art_norm))
shapiro.test(timok_data_norm$art_norm)
min(timok_data_norm$art_norm)
max(timok_data_norm$art_norm)
median(timok_data_norm$art_norm)
mean(timok_data_norm$art_norm)
sd(timok_data_norm$art_norm)


# case
plot(density(timok_data_norm$case_prop))
shapiro.test(timok_data_norm$case_prop)
min(timok_data_norm$case_prop)
max(timok_data_norm$case_prop)
median(timok_data_norm$case_prop)
mean(timok_data_norm$case_prop)
sd(timok_data_norm$case_prop)


# density and boxplot (Figure 3)
timok_norm_dens = timok_data_norm[c("transcript", "accent_prop", "perf_norm", "si_norm", "art_norm", "case_prop")]
timok_norm_dens = melt(timok_norm_dens)
timok_norm_dens$variable <- factor(timok_norm_dens$variable , levels = c("accent_prop", "perf_norm",   "si_norm",     "art_norm",    "case_prop"),
                  labels = c("Non-st. accent \nproportion", "AUX omission\n norm. freq", "Pronoun 'si'\n norm. freq", "PP Article \nnorm. freq", "Analytic case \nproportion"))

unique(timok_norm_dens$variable )
density_plot_all = ggplot(timok_norm_dens, aes(x=value))+ 
  geom_density()+ 
  geom_boxploth(aes(x = value, y=-0.01), width=0.01)+
  # geom_vline(aes(xintercept=grp.mean, color="black"), linetype="dashed")+
  labs( x="Frequency")+
  theme(axis.text = element_text(size = 20), axis.title = element_text(size = 20), strip.text.x = element_text(size = 20))+
  facet_grid(cols = vars(variable), scales = "free")
density_plot_all



# Linear regression / pearson correlation (Section 5.2)

# checking for linearity with pearson correlation

cor.test(timok_data_norm$accent_prop, timok_data_norm$si_norm, method = c("pearson")) 
cor.test(timok_data_norm$accent_prop, timok_data_norm$perf_norm, method = c("pearson"))
cor.test(timok_data_norm$accent_prop, timok_data_norm$art_norm, method = c("pearson"))
cor.test(timok_data_norm$accent_prop, timok_data_norm$case_prop, method = c("pearson"))

cor.test(timok_data_norm$si_norm, timok_data_norm$accent_prop, method = c("pearson"))
cor.test(timok_data_norm$si_norm, timok_data_norm$perf_norm, method = c("pearson"))
cor.test(timok_data_norm$si_norm, timok_data_norm$art_norm, method = c("pearson"))
cor.test(timok_data_norm$si_norm, timok_data_norm$case_prop, method = c("pearson"))

cor.test(timok_data_norm$perf_norm, timok_data_norm$accent_prop, method = c("pearson"))
cor.test(timok_data_norm$perf_norm, timok_data_norm$si_norm, method = c("pearson"))
cor.test(timok_data_norm$perf_norm, timok_data_norm$art_norm, method = c("pearson"))
cor.test(timok_data_norm$perf_norm, timok_data_norm$case_prop, method = c("pearson"))

cor.test(timok_data_norm$art_norm, timok_data_norm$accent_prop, method = c("pearson"))
cor.test(timok_data_norm$art_norm, timok_data_norm$si_norm, method = c("pearson"))
cor.test(timok_data_norm$art_norm, timok_data_norm$perf_norm, method = c("pearson"))
cor.test(timok_data_norm$art_norm, timok_data_norm$case_prop, method = c("pearson"))


cor.test(timok_data_norm$case_prop, timok_data_norm$accent_prop, method = c("pearson")) 
cor.test(timok_data_norm$case_prop, timok_data_norm$si_norm, method = c("pearson")) 
cor.test(timok_data_norm$case_prop, timok_data_norm$perf_norm, method = c("pearson")) 
cor.test(timok_data_norm$case_prop, timok_data_norm$art_norm, method = c("pearson")) 


# Hierarchical clustering (Section 5.2)

# preparing the data frame
timok_data_norm_clust = timok_data_norm
timok_data_norm_clust$tokens = NULL
timok_data_norm_clust$transcript = timok_data_norm_clust$transcript %>% str_replace(".*_", "")
row.names(timok_data_norm_clust) = timok_data_norm_clust$transcript
timok_data_norm_clust$transcript = NULL

# creating dist object
torlak_dist = dist(timok_data_norm_clust, method = "euclidean")

# clustering
torlak_hclust = hclust(torlak_dist, method = "ward.D2", members = NULL)
# torlak_htree = plot(torlak_hclust)

# plotting 3 clusters
torlak_dhc <- as.dendrogram(torlak_hclust)
torlak_dhc = torlak_dhc %>%
  set("labels_col", value = c("red", "blue", "green"), k=3)

# The dendrogram (Figure 5)
plot(torlak_dhc, main="Hierarchical clustering of the speakers")
legend("topright", 
       legend = c("1" , "2" , "3"), # , "4" , "5"
       col = c("red", "blue", "green"), #, "yellow", "pink"
       pch = c(20,20,20,20,20), bty = "n",  pt.cex = 1.5, cex = 0.8 , 
       text.col = "black", horiz = FALSE, inset = c(0, 0.1))

# adding the cluster variable to the main data frame
cluster = cutree(torlak_dhc, k = 3)
timok_data_norm$cluster = cluster

# rescaling values for cluster means preview
timok_data_norm$accent_scaled = rescale(timok_data_norm$accent_prop, to = c(0, 1))
timok_data_norm$perf_scaled = rescale(timok_data_norm$perf_norm, to = c(0, 1))
timok_data_norm$si_scaled = rescale(timok_data_norm$si_norm, to = c(0, 1))
timok_data_norm$art_scaled = rescale(timok_data_norm$art_norm, to = c(0, 1))
timok_data_norm$case_scaled = rescale(timok_data_norm$case_prop, to = c(0, 1))

# cluster means (Table 5)
timok_cluster_means = timok_data_norm %>% 
  group_by(cluster) %>% 
  summarise(n = n(),
            mean_perf = round(mean(perf_scaled), 2), 
            mean_art = round(mean(art_scaled), 2),
            mean_accent = round(mean(accent_scaled), 2),
            mean_case = round(mean(case_scaled), 2),
            mean_si = round(mean(si_scaled), 2))

timok_cluster_means

# plotting cluster means (Figure 6)
timok_cluster_means_visual = timok_cluster_means[, c(1, 3:7)]
timok_cluster_means_visual = timok_cluster_means_visual %>%
  gather(key, Value, -cluster)
timok_cluster_means_visual$cluster = as.factor(timok_cluster_means_visual$cluster)
timok_cluster_means_visual$key = factor(timok_cluster_means_visual$key, levels = c("mean_case", "mean_accent", "mean_perf", "mean_si", "mean_art"))

# Figure 6
ggplot(timok_cluster_means_visual, aes(x = key, y = Value, fill = cluster)) +
  geom_point(color = "black", size = 5, shape = 21, alpha = 0.6) +
  theme_light() +
  geom_line(aes(group = cluster, color = cluster))


# mapping clusters (Figure 7)
cluster_pal <- colorFactor(c("red", "blue", "green"), timok_data_norm$cluster)

timok_data_norm$speaker = timok_data_norm$transcript
timok_speakers$transcript = timok_speakers$speaker
timok_data_norm_clust_geo = left_join(
  x=timok_data_norm,
  y=timok_speakers,
  by="transcript")

timok_data_norm_clust_geo = left_join(
  x=timok_data_norm_clust_geo,
  y=timok_locations,
  by="location")

timok_data_norm_clust_geo = timok_data_norm_clust_geo[c("cluster", "location", "speaker.x", "latitude", "longitude")]

map_clusters <- leaflet(timok_data_norm_clust_geo) %>% 
  addProviderTiles(providers$Stamen.TonerLite) %>%
  addCircles(~longitude, ~latitude,
             radius = 1000, 
             label = ~speaker.x, 
             labelOptions = labelOptions(noHide = F, textOnly = TRUE, direction = 'bottom', textsize = "20px"), 
             popup = ~speaker.x,
             color = ~cluster_pal(cluster)
  ) %>%
  addLegend(title = "The map of Timok clusters",
            pal = cluster_pal, 
            values = ~cluster, 
            opacity = 1)
map_clusters



# correlation with the geo information (Section 5.1)

# preparing data for the geo analysis
timok_speakers_locations = left_join(
  timok_speakers,
    timok_locations,
    by = "location")
timok_speakers_locations$transcript.x = NULL
timok_speakers_locations$transcript.y = NULL
timok_data_norm$speaker = timok_data_norm$transcript

timok_data_norm_meta = left_join(
  timok_data_norm,
  timok_speakers_locations,
  by = "speaker")


# geo correlation
cor.test(timok_data_norm_meta$accent_prop, timok_data_norm_meta$longitude, method = c("pearson")) # yes
cor.test(timok_data_norm_meta$accent_prop, timok_data_norm_meta$latitude, method = c("pearson")) #no
cor.test(timok_data_norm_meta$si_norm, timok_data_norm_meta$longitude, method = c("pearson")) #no
cor.test(timok_data_norm_meta$si_norm, timok_data_norm_meta$latitude, method = c("pearson")) #no
cor.test(timok_data_norm_meta$perf_norm, timok_data_norm_meta$longitude, method = c("pearson")) #no
cor.test(timok_data_norm_meta$perf_norm, timok_data_norm_meta$latitude, method = c("pearson")) #no
cor.test(timok_data_norm_meta$art_norm, timok_data_norm_meta$longitude, method = c("pearson")) # yes
cor.test(timok_data_norm_meta$art_norm, timok_data_norm_meta$latitude, method = c("pearson")) #no
cor.test(timok_data_norm_meta$case_prop, timok_data_norm_meta$longitude, method = c("pearson")) #no
cor.test(timok_data_norm_meta$case_prop, timok_data_norm_meta$latitude, method = c("pearson")) #no


# maps of feature distribution
map_accent <- leaflet(timok_data_norm_meta) %>% 
  addProviderTiles(providers$Stamen.TonerLite) %>%
  addCircles(~longitude, ~latitude,
             radius = ~accent_prop*accent_prop/4, 
             label = ~location, 
             labelOptions = labelOptions(noHide = F, textOnly = TRUE, direction = 'bottom', textsize = "20px"), 
             popup = ~location,
             color = "black") %>%
  addLegend("topright",
            values = c("Non-standard accent"),
            labels = c("Non-standard accent"),
            colors = c("Black"))
map_accent

map_si <- leaflet(timok_data_norm_meta) %>% 
  addProviderTiles(providers$Stamen.TonerLite) %>%
  addCircles(~longitude, ~latitude,
             radius = ~si_norm*si_norm/3, 
             label = ~location, 
             labelOptions = labelOptions(noHide = F, textOnly = TRUE, direction = 'bottom', textsize = "20px"), 
             popup = ~location,
             color = "black") %>%
  addLegend("topright",
            values = c("Pronoun 'si'"),
            labels = c("Pronoun 'si'"),
            colors = c("Black"))
map_si

map_perf <- leaflet(timok_data_norm_meta) %>% 
  addProviderTiles(providers$Stamen.TonerLite) %>%
  addCircles(~longitude, ~latitude,
             radius = ~perf_norm*perf_norm/250, 
             label = ~location, 
             labelOptions = labelOptions(noHide = F, textOnly = TRUE, direction = 'bottom', textsize = "20px"), 
             popup = ~location,
             color = "black") %>%
  addLegend("topright",
            values = c("AUX ommission in the perfect tense"),
            labels = c("AUX ommission in the perfect tense"),
            colors = c("Black"))
map_perf

map_art <- leaflet(timok_data_norm_meta) %>% 
  addProviderTiles(providers$Stamen.TonerLite) %>%
  addCircles(~longitude, ~latitude,
             radius = ~art_norm*art_norm/2, 
             label = ~location, 
             labelOptions = labelOptions(noHide = F, textOnly = TRUE, direction = 'bottom', textsize = "20px"), 
             popup = ~location,
             color = "black") %>%
  addLegend("topright",
            values = c("Post-positive article"),
            labels = c("Post-positive article"),
            colors = c("Black"))
map_art

map_case <- leaflet(timok_data_norm_meta) %>% 
  addProviderTiles(providers$Stamen.TonerLite) %>%
  addCircles(~longitude, ~latitude,
             radius = ~case_prop*case_prop/7, 
             label = ~location, 
             labelOptions = labelOptions(noHide = F, textOnly = TRUE, direction = 'bottom', textsize = "20px"), 
             popup = ~location,
             color = "black") %>%
  addLegend("topright",
            values = c("Analytic case marking in IO and POSS"),
            labels = c("Analytic case marking in IO and POSS"),
            colors = c("Black"))
map_case



# compare old speakers data and young speakers (Appendix 1)
timok_data_norm_young_old = read.csv('data/timok_data_norm_young_old.csv', header = T, sep = "\t")

# box plots 
gg_boxplot_accent <- ggplot(data = timok_data_norm_young_old, aes(x = age, y = accent_prop)) +
  geom_boxplot(fill = 'white', width = 0.8) +
  scale_x_discrete(labels = c('Old', 'Young')) +
  stat_summary(geom = 'pointrange', 
               fun.data = mean_sdl, fun.args = list(mult = 1)) +
  coord_cartesian(ylim = c(0, 100)) +
  labs(x = NULL, y = 'Proportion') +
  ggtitle('Non-standard accent')+
  theme(axis.title.x = element_text(size = 24),axis.text.x = element_text(size = 24), 
        axis.title.y = element_text(size = 24),axis.text.y = element_text(size = 18), 
        title = element_text(size = 24))

gg_boxplot_accent

gg_boxplot_si <- ggplot(data = timok_data_norm_young_old, aes(x = age, y = si_norm)) +
  geom_boxplot(fill = 'white', width = 0.8) +
  scale_x_discrete(labels = c('Old', 'Young')) +
  stat_summary(geom = 'pointrange', 
               fun.data = mean_sdl, fun.args = list(mult = 1)) +
  labs(x = NULL, y = "Normalised frequency") +
  ggtitle("Pronoun 'si'")+
  theme(axis.title.x = element_text(size = 24),axis.text.x = element_text(size = 24), 
        axis.title.y = element_text(size = 24),axis.text.y = element_text(size = 18), 
        title = element_text(size = 24))
gg_boxplot_si

timok_data_norm_young_old$perf_norm

gg_boxplot_perf <- ggplot(data = timok_data_norm_young_old, aes(x = age, y = perf_norm)) +
  geom_boxplot(fill = 'white', width = 0.8) +
  scale_x_discrete(labels = c('Old', 'Young')) +
  stat_summary(geom = 'pointrange', fun.data = mean_sdl, fun.args = list(mult = 1)) +
  labs(x = NULL, y = 'Nomralized frequency') + 
  ggtitle('AUX omission')+
  theme(axis.title.x = element_text(size = 24),axis.text.x = element_text(size = 24), 
        axis.title.y = element_text(size = 24),axis.text.y = element_text(size = 18), 
        title = element_text(size = 24))
gg_boxplot_perf

gg_boxplot_art <- ggplot(data = timok_data_norm_young_old, aes(x = age, y = art_norm)) +
  geom_boxplot(fill = 'white', width = 0.8) +
  scale_x_discrete(labels = c('Old', 'Young')) +
  stat_summary(geom = 'pointrange', 
               fun.data = mean_sdl, fun.args = list(mult = 1)) +
  coord_cartesian(ylim = c(0, 100)) +
  labs(x = NULL, y = 'Nomralized frequency') + 
  ggtitle('Post-positive article')+
  theme(axis.title.x = element_text(size = 24),axis.text.x = element_text(size = 24), 
        axis.title.y = element_text(size = 24),axis.text.y = element_text(size = 18), 
        title = element_text(size = 24))
gg_boxplot_art

gg_boxplot_case <- ggplot(data = timok_data_norm_young_old, aes(x = age, y = case_prop)) +
  geom_boxplot(fill = 'white', width = 0.8) +
  scale_x_discrete(labels = c('Old', 'Young')) +
  stat_summary(geom = 'pointrange', 
               fun.data = mean_sdl, fun.args = list(mult = 1)) +
  coord_cartesian(ylim = c(0, 100)) +
  labs(x = NULL, y = 'Proportion') + 
  ggtitle('Analytic case marking')+
  theme(axis.title.x = element_text(size = 24),axis.text.x = element_text(size = 24), 
        axis.title.y = element_text(size = 24),axis.text.y = element_text(size = 18), 
        title = element_text(size = 24))
gg_boxplot_case

# Figure 8, Appendix 1
grid.arrange(gg_boxplot_accent, gg_boxplot_si, gg_boxplot_perf, gg_boxplot_art, gg_boxplot_case, nrow = 1)

# subsetting only the frequencies for the younger speakers
timok_data_norm_young = timok_data_norm_young_old[timok_data_norm_young_old$age=="YOUNG",]

# mean values for the younger speakers
mean(timok_data_norm_young$accent_prop)
mean(timok_data_norm_young$si_norm)
mean(timok_data_norm_young$perf_norm)
mean(timok_data_norm_young$art_norm)
mean(na.omit(timok_data_norm_young$case_prop))

