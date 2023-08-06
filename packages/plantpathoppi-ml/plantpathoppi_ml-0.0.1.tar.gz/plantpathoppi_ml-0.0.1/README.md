
plantpathoppi_ml predicts protein-protein interaction between plant and pathogen, 
based on an ensemble-based machine learning architecture.

***Input file:***
The user need to provide pairs of plant and pathogen protein as input. The first and second column should contain plant and pathogen 
protein, respecticely.
An example input file can be obtained from the given link https://github.com/snehaiasri/plantpathoppi/blob/main/example.csv.

***Usage:***
After installation, perform the following steps to use the package

*import the package*
>import plantpathoppi_ml as ppp

*save the input file as dataframe. Provide the full path of the input file.*
> df = pd.read_csv("example.csv")

*convert the df into numpy array*
> var = df.to_numpy()

*call the predict function*
> x = ppp.predict(var)

*to call the predict_proba function*
> y = ppp.predict_proba(var)

*call gen_file function to generate the output file (output.txt) in your current working directory*
> ppp.gen_file(var)

***Help***
To see the documentation of each function, use help command. For example, help(plantpathoppi_ml) or help(predict).

***Requirments***
Python >3.9,
numpy,
pickle-mixin,
sklearn.




