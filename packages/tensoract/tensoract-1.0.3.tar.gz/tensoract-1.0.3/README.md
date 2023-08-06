# Tensoract API client

This is python package to call all API from (https://api.tensoract.com/docs)

## Import package and create a `client`
## "api_url" is and optional parameter for private installs
```python
from pprint import pprint
from tensoract.client import Tensoract

client = tensoract.Tensoract(api_url="YOUR_API_URL",api_key="YOUR_API_KEY")
```

## 1. Task
### 1.1. Add new task

```python

pprint(client.add_task(project_id="cd1a965e334a9a63e2f17932",
                  dataset_item_id="bd1a965e334a9a63e2f179er"))
```
### 1.2. Add bulk tasks
```python
dataset_items = [
   "15542b60229da3f94f82d1a2",
    "09f5dd6f24b057615f9c583c",
    "e8cbb47f599c99b28a5d3466"
]
  

pprint(client.add_bulk_tasks(project_id="a28aedc450e845523d4bfa10",
                                   note="test note",
                          dateset_items=dateset_items))
```
### 1.3. Add labels to task
```python
body = {
  "annotations": "s3://examples/pdfs/annotation.json"
}

pprint(client.add_labels_to_task(task_id=task_id,body=body))
```
### 1.4. Add task file (deprecated )

```python
data = client.add_task_file(
    project_id="449354de1168469a8229f605", 
    file_path="examples/pdfs/document.pdf",
    mime_type="application/pdf",
    annotations=None
)

pprint(data)
```
### 1.5. Get Task by task_id
- To Find all annotations for the task use optional trail = True 

```python
data = client.get_task(
    task_id="449354de1168469a8229f605", 
    trail = True 
)

pprint(data)
```
### 1.6. Delete Task by task_id
```python
data = client.delete_task(
    task_id="449354de1168469a8229f605"
)

pprint(data)
```
### 1.7. Get tasks by filters

- Find all the tasks by `task_id`, `file_name`, `file_type` 
- `trail` parameter is deprecated
- If all of `task_id`, `file_name`, `file_type` are `None`, it will return all possible tasks

```python
tasks = client.get_tasks(
    project_id="449354de1168469a8229f605", 
    task_id="449354de1168469a8229f605-0",
    file_name=None,
    file_type=None,
    //trail = False (deprecated)
)

pprint(tasks)
```
### 1.8. Export Tasks by project_id

```python
response = client.export_tasks(
    project_id="449354de1168469a8229f605", 
)

pprint(response)
```
### 1.9. Get Bounding box coordinates for Words for a task 
- Get Bounding Box coordinates of all pages in a document
- Optionally pass "page" number to restrict by the page
```python
response = client.get_word_boxes(
    task_id="449354de1168469a8229f605",
    page = 1 
)

pprint(response)
```
### 1.10. Get deep link for task
```python
response = client.get_task_deep_link(
    task_id="449354de1168469a8229f605" 
 )

pprint(response)
```
### 1.11. Set deep link for task
```python
response = client.create_task_deep_link(
    task_id="449354de1168469a8229f605", 
    user_name="johndoe",
    user_email="john.doe@acme.com",
    role="Annotator",
    expire_in=5,
    return_url=https://yourdomain.com
)

pprint(response)
```
### 1.12. Get url for task
```python
response = client.get_task_url(
    task_id="449354de1168469a8229f605",
    role="annotator"|"reviewer"
 )

pprint(response)
```

## 2. Project
### 2.1. Create a new project
```python
body = {
  "project_name": "TestProject",
  "project_type": "NER",
  "enable_text_mode_option": True,
  "disable_quality_audit": True,
  ...
}
# check API docs for the full body: https://api.tensoract.com/docs/#/projects/upload_project

pprint(client.create_project(body))
```
### 2.2. Get project by project_id
```python
response = client.get_project(
    project_id="449354de1168469a8229f605", 
)

```
### 2.3. Update project 
```python
body = {
  "project_name": "TestProject",
  "project_type": "NER",
  "enable_text_mode_option": True,
  "disable_quality_audit": True,
  ...
}
response = client.update_project(
    project_id="449354de1168469a8229f605",
    body=body 
)

```
### 2.4. Delete project 
```python
response = client.delete_project(
    project_id="449354de1168469a8229f605",
)
```
### 2.5. Get projects by Filters
- Find all the projects by `project_id`, `project_name` or `active`
- If all of `project_id`, `project_name`, `active` are `None`, it will return all possible projects 
```python
response = client.get_projects(
    project_id="449354de1168469a8229f605", 
    project_name=None, 
    active=None
)
```
### 2.6. Export project Tasks
```python
response = client.export_project_tasks(
    project_id="449354de1168469a8229f605", 
    export_note="This is test export via API"
)
```
### 2.7. List Project Exports
```python
response = client.list_project_exports(
    project_id="449354de1168469a8229f605", 
)
```
### 2.8. Download Project Exports
```python
response = client.download_project_export(
    export_id="449354de1168469a8229f605", 
)
```

## 3. Team Management
### 3.1. Add member to the team
```python
member = client.add_team_member(
    project_id="449354de1168469a8229f605", 
    email="someone@email.com", 
    role="annotator|reviewer|supervisor"
)
```
### 3.2. Get project team members
```python
team = client.get_project_team_members(
    project_id="449354de1168469a8229f605", 
)
```
### 3.3. Remove member from the project team
```python
team = client.remove_project_team_member(
    project_id="449354de1168469a8229f605",
    email="someone@email.com" 
)
```
## 4. Dataset Management
### 4.1. Create a new Dataset
```python
body = {
  "dataset_name": "Test Dataset",
  "dataset_description": "This is a test Dataset",
  "dataset_type": "Image",
  "item_format": "image/tiff",
  "meta_data": {
    "key": "value"
  },
  "s3IntermediateUrl": "s3://test-dataset/intermediate",
  "aws_credentials_enabled": true,
  "aws_credentials": {
    "awsKey": "...",
    "awsSecret": "...",
    "awsRegion": "us-east-1",
    "awsType": "key"
  }
}
# check API docs for the full body:http://54.83.23.220:8089/docs/#/datasets/upload_dataset

pprint(client.create_dataset(body))
```
### 4.2. Get dataset by dataset_id
```python
response = client.get_dataset(
    dataset_id="449354de1168469a8229f605", 
)
```
### 4.3. Update dataset 
```python
body = {
  "dataset_name": "Test Dataset",
  "dataset_description": "This is a test Dataset",
  "dataset_type": "Image",
  "item_format": "image/tiff",
  "meta_data": {
    "key": "value"
  },
  "s3IntermediateUrl": "s3://mybucket/test-dataset/intermediate",
  "aws_credentials_enabled": true,
  "aws_credentials": {
    "awsKey": "xxxxx",
    "awsSecret": "xxx",
    "awsRegion": "us-east-1",
    "awsType": "key"
  }
}
response = client.update_dataset(
    dataset_id="449354de1168469a8229f605",
    body=body 
)

```
### 4.4. List datasets by Filters
- Find all the datasets by `dataset_id`, `dataset_name` or `active`
- If all of `dataset_id`, `dataset_name`, `active` are `None`, it will return all possible datasets 
```python
response = client.list_datasets(
    dataset_id="449354de1168469a8229f605", 
    dataset_name=None, 
    active=None
)
```
### 4.5. Delete dataset by dataset_id
```python
response = client.delete_dataset(
    dataset_id="449354de1168469a8229f605", 
)
```
### 4.6. Export Dataset (by project_id optional)
```python
response = client.export_dataset(
    dataset_id="449354de1168469a8229f605", 
    export_note="This is test export via API",
    project_id="449354de1168469a8229f606"
)
```
### 4.7. List Dataset Exports
```python
response = client.list_dataset_exports(
    dataset_id="449354de1168469a8229f605", 
)
```

### 4.8. Download Dataset Export
```python
response = client.download_dataset_export(
    export_id="449354de1168469a8229f605", 
)
```

### 4.9. Create a new Dataset Item
```python
body = {
  "dataset_id": "208eb554d3fa1e161b2c6a44",
  "dataset_items": [
    {
      "meta_data": {
        "batch": "10",
        "test": "cell"
      },
      "source": "s3://mybucket/test-dataset/file1.tiff"
    },
    {
      "meta_data": {
        "batch": "1",
        "test": "cell"
      },
      "source": "s3://mybucket/test-dataset/file2.tiff"
    } 
    ....
    ....
  ]
}
# check API docs for the full body:https://adl.tensoract.com/docs/#/datasets/upload_dataset

pprint(client.create_dataset_item(body))
```
### 4.10. Get dataset_item by item_id
```python
response = client.get_dataset_item(
    item_id="449354de1168469a8229f605" 
)
```
### 4.11. Delete dataset_item by item_id
```python
response = client.delete_dataset_item(
    item_id="449354de1168469a8229f605" 
)

```
### 4.12. List dataset items by Filters
- Find all the dataset items by `dataset_id`, `dataset_version`
- If `dataset_version` is  `None`, it will return all possible dataset items for all versions 
```python
projects = client.list_dataset_items(
    dataset_id="449354de1168469a8229f605", 
    dataset_version=3 
)
```