# FakeCSVService Tutorial

This is a short tutorial that will help you familiarize yourself with all the functionality and capabilities of this project.



## Table of Contents
* [Authorization](#authorization)
* [Actions with the schemes](#actions-with-the-schemes)
* [Actions with the datasets](#actions-with-the-datasets)
* [Checking the status of the dataset](#checking-the-status-of-the-dataset)
* [Download Dataset](#download-dataset)


## Authorization
First of all, you need to log in. To do this, do the following in the terminal:

`curl -X POST -d "username=test_user&password=1357246test" localhost:8000/api/user/auth/`

_Note: The access token you received will be needed for further work with the project._

## Actions with the schemes

Here are the actions you can perform with a schema, namely create a new one, modify an existing one, delete an existing one, create a dataset based on the schema

* [Create Scheme](#create-scheme)
* [Update Scheme](#update-scheme)
* [Delete Scheme](#delete-scheme)
* [Get scheme](#get-scheme)

### Create scheme

To do this, you need to execute the following command:

`curl -X POST http://localhost:8000/api/schema/ -H "Content-Type:application/json" -H "Authorization: Bearer <access token>" -d '{"name":"schema_1","column_separator":",","string_character":"'\''","columns":[{"name":"Full_name","type":"full_name"},{"name":"Job","type":"job"},{"name":"Email","type":"email"},{"name":"Phone_number","type":"phone_number"},{"name":"Integer","type":"integer","value_from":18,"value_to":70}]}'`

All values in the data can be changed at your discretion. However, some fields have clearly defined values. Here are the available values:

#### column_separator: ',' '.'
#### string_character: ''\' '"'
#### type field in columns: 'job', 'full_name', 'phone_number', 'email', 'integer'(required two additional fields 'value_from' and 'value_to')

_Note: The number of columns can be any, and you can use all types several times or not at all._

### Update scheme

To do this, you need to execute the following command:

`curl -X PUT http://localhost:8000/api/schema/<schema_id>/ -H "Content-Type:application/json" -H "Authorization: Bearer <access token>" -d '{"name":"schema_1","column_separator":",","string_character":"'\''","columns":[{"name":"Full_name","type":"full_name"},{"name":"Job","type":"job"},{"name":"Email","type":"email"},{"name":"Phone_number","type":"phone_number"},{"name":"Integer","type":"integer","value_from":18,"value_to":70}]}'`

The list of available values is the same as when creating.

### Delete scheme

To do this, you need to execute the following command:

`curl -X DELETE http://localhost:8000/api/schema/<scheme_id>/ -H "Content-Type:application/json" -H "Authorization: Bearer <access token>"`

### Get scheme

If you want to view one or all existing schemes, then use the following command:

#### For one scheme
`curl http://localhost:8000/api/schema/<scheme_id>/ -H "Content-Type:application/json" -H "Authorization: Bearer <access token>"`
#### For all schemes
`curl http://localhost:8000/api/schema/ -H "Content-Type:application/json" -H "Authorization: Bearer <access token>"`


## Actions with the datasets

* [Create Dataset](#create-dataset)
* [Delete Dataset](#delete-dataset)
* [Get Dataset](#get-dataset)

### Create dataset

To do this, you need to execute the following command:

`curl -X POST http://localhost:8000/api/schema/<scheme_id/create_dataset/ -H "Content-Type:application/json" -H "Authorization: Bearer <access token>" -d '{"name":"Dataset_1","rows":100}'`

_Note: Also, response returns a key that can be used to find out the execution status of this dataset_
### Delete dataset

To do this, you need to execute the following command:

`curl -X DELETE http://localhost:8000/api/dataset/<dataset_id>/ -H "Content-Type:application/json" -H "Authorization: Bearer <access token>"`

### Get dataset

If you want to view one or all existing schemes, then use the following command:

#### For one dataset
`curl http://localhost:8000/api/dataset/<id_dataset/ -H "Content-Type:application/json" -H "Authorization: Bearer <access token>"`
#### For all datasets
`curl http://localhost:8000/api/dataset/ -H "Content-Type:application/json" -H "Authorization: Bearer <access token>"`


### Checking the status of the dataset

In order to check the execution status of our dataset, we need a key that can be obtained with the [dataset creation command](#create-dataset), as well as the following command:

`curl http://localhost:8000/api/status_task/?task_id=<cache_task_key> -H "Content-Type:application/json" -H "Authorization: Bearer <access token>"`


## Download dataset

To do this, you need to execute the following command:

`curl http://localhost:8000/api/dataset/<dataset_id>/download/ -H "Content-Type:application/json" -H "Authorization: Bearer <access token>"`

After executing the command, you will receive a link to download your dataset.