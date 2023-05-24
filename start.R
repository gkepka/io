install.packages("irace", repos = "http://cran.us.r-project.org")
library("irace")
setwd("./tuning")
scenario <- readScenario(filename = "scenario.txt", scenario = defaultScenario())
irace.main(scenario = scenario)

