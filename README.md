# Wind-turbine-US
In this project, we explore classification analysis of the Wind Turbines dataset from CORGIS Dataset Project published on https://corgis-edu.github.io/corgis/csv/wind_turbines/.

The dataset comprises of documented parameters describing the wind turbines installed across US, including the State and County of the turbines site, the year and location of installation and geometrical parameters of the turbines. The details of the parameters are as follows:

Key | List of... | Comment | Example Value
--- | --- | --- | ---
Site.State | String | Two letter abbreviation of state where turbine is located (e.g., CA for California) | "IA"
Site.County | String | County where the turbine is located. | "Story County"
Year | Integer  | Year when the turbine's project became operational | 2017
Turbine.Capacity | Integer | Electrical generation capacity of the turbine measured in KW (kilo-watts) |  3000
Turbine.Hub_Height | Float | Height in meters of the turbine's hub | 87.5
Turbine.Rotor_Diameter | Float | Diameter in meters of the turbine's rotor | 125.0
Turbine.Swept_Area | Float | The area swept on each rotation of the turbine | 12271.85
Turbine.Total_Height | Float | Total height of the turbine, in meters | 150.0
Project.Capacity | Float | Electrical generation capacity of the turbine measured in MW (mega-watts) | 30.0
Project.Number_Turbines | Integer | Number of turbines in this project | 10
Site.Latitude | Float | Latitude (decimal degrees - NAD 83 datum) of where turbine is located | -93.518082
Site.Longitude | Float | Longitude (decimal degrees - NAD 83 datum) | 42.01363

The scripts for data preparation, classification model building and model evaluation are locations ./src/ and the complete analysis can be run via running the bash script ./run.sh

The image directory contains some of the results and there seem to be 2 or 3 classes of Wind turbines that is defined by the size of the turbines which generally became bigger with year of installation.
