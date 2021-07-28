# Description

This small system is a backend API with just one endpoint that is supposed to serve a dynamic dataset that corresponds to any combination of filters, breakdowns and sorting.

So, baically, this API takes in a request with some parameters that are filters, breakdowns, and sortings, and returns a response with the new dataset, which is a subset of the original dataset, that satisfies these filters and breakdowns, to be then used for analytics.

## Building, Testing, Running, and Connecting to the Service

This system is implemented in Python's Flask. It uses Python version 3.9.4 and Flask version 2.0.1. To build, just clone the repo
by running the following command in Git Bash in the appropriate directory:

``git clone https://github.com/eyadnawar/Adjust-task.git``

Open the terminal and activate the virtual environment via the command `.\venv\Scripts\activate.bat` then install the necessary packages in the [requirements.txt](https://github.com/eyadnawar/Adjust-task/requirements.txt) run `pip install -r requirements.txt`, then run the "importing_data" file to create the relational database that is going to store our csv file, and finally run `flask run <file_location>` or just open the `app.py` file, right click and choose build and run. It will run on the localhost.

To conect to the service, there is only 1 endpoint that does all of the aforementioned operations. This endpoint is:

* `/analyze_data` which is a `GET` method sent to the backend API by the user-facing application. The endpoint receives the following parameters in the body of the request:

    1. `filter`: dictionary / json object     ### The filtering values of the specified column names
    2. `break_down`: List / Array             ### The grouping-by variables
    3. `sort`: String                         ### The sorting variable, followed by the method of sorting (Asc / desc)
    4. `show`: List / Array                   ### The columns you want to select from the database for preview
       
       ```
       API request : {
                        "filter" : {
                                    "os" : "ios",
                                    "country" : "US",
                                    "channel" : "adcolony",
                                    "date": "< 2017-06-01"
                                    },
                        "break_down" : ["channel", "country"],
                        "sort"       : "clicks desc",
                        "show"       : ["impressions sum", "clicks sum"]
                    }
       ```
       
        and returns a response with the sql query corresponding to the specified filters and breakdowns along with the new dataset (which is a subset of the original dataset, that corresponds to those filtering, break down, and sorting commands)
    
### Rules for creating a request (Formats)

For the "date" key in the filter:
    if you want to specify a range (ie: date_from to date_to), you simply use the format "date_from date_to"
    But, if you want to specify a wide range of dates, then you must use the format "{</>/=} {date}" 

For the "sort" key of the request:
    you must use the format "{column name} {asc/desc}"

For the "show" key of the request:
    you must use the format "{column name} {aggregate function}" for each string in the list

### Working Examples (Common API use-cases)

1. Show the number of impressions and clicks that occurred before the 1st of June 2017, broken down by channel and country, sorted by clicks in descending order.

```
url: http://127.0.0.1:5000/analyze_data

request body: {
    "filter" : {
                "date": "< 2017-06-01"
                },
    "break_down" : ["channel", "country"],
    "sort"       : "clicks desc",
    "show"       : ["impressions sum", "clicks sum"]
}

reponse: {
    "message": "The operation was successful.",
    "result": [["adcolony", "US", 498861, 12277],
               ["apple_search_ads","US", 347554, 10738],
               ["vungle", "GB", 249197, 8831 ],
               ["vungle", "US", 249618, 7440],
               ...
             ]
    "satus": 200,
    "sql query": "select channel, country, sum(impressions) as impressions, sum(clicks) as clicks from AdjustData where date < '2017-06-01' group by channel, country order by clicks desc "
}
```
2. Show the number of installs that occurred in May of 2017 on iOS, broken down by date, sorted by date in ascending order.

```
url: http://127.0.0.1:5000/analyze_data

request body: {
    "filter" : {
                "os" : "ios",
                "date": "2017-05-01 2017-06-01"
                },
    "break_down" : ["date"],
    "sort"       : "date asc",
    "show"       : ["installs sum"]
}

response: {
    "message": "The operation was successful.",
    "result": [["2017-05-17", 755],
               ["2017-05-18", 765],
               ["2017-05-19", 745],
               ["2017-05-20", 816],
               ...
              ],
    "satus": 200,
    "sql query": "select date, sum(installs) as installs from AdjustData where (os = 'ios' AND date >= '2017-05-01' and date < '2017-06-01') group by date order by date asc"
    }
```

3. Show revenue, earned on June 1, 2017 in US, broken down by operating system and sorted by revenue in descending order.

```
url: http://127.0.0.1:5000/analyze_data

request body: {
    "filter" : {
                "os" : "ios",
                "date": "2017-05-01 2017-06-01"
                },
    "break_down" : ["date"],
    "sort"       : "date desc",
    "show"       : ["installs sum"]
}

response : {
    "message": "The operation was successful.",
    "result": [["android", 1205.21],
               ["ios", 398.87]
             ],
    "satus": 200,
    "sql query": "select os, sum(revenue) as revenue from AdjustData where (country = 'US' AND date = '2017-06-01') group by os order by revenue desc"
}
```

4. Show CPI and spend for Canada (CA) broken down by channel ordered by CPI in descending order.

```
url: http://127.0.0.1:5000/analyze_data

request body: {
    "filter" : {
                "country" : "CA",
                },
    "break_down" : ["channel"],
    "sort"       : "CPI desc",
    "show"       : ["CPI sum", "spend sum"]
}

response : {
    "message": "The operation was successful.",
    "result": [["unityads", 90.0, 2642.0],
               ["facebook", 64.93456177330992, 1164.0],
               ["chartboost", 60.0, 1274.0],
               ["google", 56.10034081126929, 999.9000000000004]
             ],
    "satus": 200,
    "sql query": "select channel, sum(spend/installs) as CPI, sum(spend) as spend from AdjustData where country = 'CA' group by channel order by CPI desc "
}
```

Note that for the last use case, the "sum" aggregate function should be employed after computing the values of the new derived column CPI since we can't sum the spends and sum the installs and divide both numbbers or we will then mess up the values because we will not have preserved the ratios.

## Technical *(Implementation)* Details

This system is built in Python's `Flask`, and uses `Sqlite` as its relational database storage system.

### Final Remarks

This endpoint is capable of working with any combination of filters, break-downs, and sortings. As the four use cases mentioned above have shown, this 1 single endpoint is compilant with all of the use cases with their different requests and filters.
