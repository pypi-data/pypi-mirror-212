# Spark-LLM

Spark-LLM is a Python library that can assist in the development of Spark applications, including Spark Dataframe, Spark SQL, testings, and so on.

## Usage
To create an instance of SparkLLMAssistant:
```python
from langchain.chat_models import ChatOpenAI
from spark_llm import SparkLLMAssistant

llm = ChatOpenAI(model_name='gpt-4') # using gpt-4 can achieve better results
assistant=SparkLLMAssistant(llm=llm)
```

To create a Dataframe with web search and LLM:
```python
auto_df=assistant.create_df("2022 USA national auto sales by brand")
auto_df.show(n=5)
```
| rank | brand     | sales   | Percentage_Change |
|------|-----------|---------|-------------------|
| 1    | Toyota    | 1849751 | -9                |
| 2    | Ford      | 1767439 | -2                |
| 3    | Chevrolet | 1502389 | 6                 |
| 4    | Honda     | 881201  | -33               |
| 5    | Hyundai   | 724265  | -2                |

To explain a Spark Dataframe in simple words
```python
auto_top_growth_df = auto_df.orderBy(auto_df.percentage_change.desc()).limit(1)
assistant.explain_df(auto_top_growth_df)
```

> In summary, this dataframe is retrieving the single record with the highest percentage change in sales from the `auto_sales_2022` view, which contains information about the rank, brand, sales, and percentage change in sales for various car brands in the year 2022.

Refer to example.ipynb in the examples/ directory for more detailed usage examples.


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
Licensed under the Apache License 2.0.
