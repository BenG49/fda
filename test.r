library(fpp2)
library(ggplot2)

beer2 <- window(ausbeer, start = 1992, end = c(2007, 4))

png("out.jpg")

autoplot(beer2) +
	autolayer(meanf(beer2, h = 11), series = "Mean") +
	ggtitle("Forecasts for quarterly beer production") +
	xlab("Year") + ylab("Megalitres") +
	guides(color = guide_legend(title = "Forecast"))

dev.off()
