# CS272 Project AI Album Backend
This repository holds the backend part of the AI album project.

## 🌲 Project Structure

The project structure is as follows, and the content below is produced using `tree .` command.
```plain
.
├── README.md
├── resource
│   ├── album : where we save pics.
│   └── densenet : take densenet for example, this is where we store static file we need for this model. 
├── src
│   ├── api : where you expose the api of your model, one model one file.
│   ├── app.py : entry point for the project.
│   └── model : where you write methods to load model and inference.
└── test : where you test whether your api works.

```

## 💡 Development Guide

Take densenet for example, this is a model for image classification.

First, save model weights, you can refer to the code `src/model/densenet/save_model_example.py`, you should run this code to generate the file named `densenet121.pt` under `resource\densenet\`.

**Notice**: You'd better use _torchscript_ to save model, just as the example do. The reason is explained in [saving_loading_models](https://pytorch.org/tutorials/beginner/saving_loading_models.html). However, you can use any save method as long as you can load your model to work properly.

Secondly, you should load your model and write the method to predict the result. You should write these code in the package `src.model.<your_model>`, please look at the example code under `src/model/densenet`.

Next, you should set up your api to expose the predict method you write. You should write these code in the package `src.api.<your_model>.py`, please look at the example code under `src/api/densenet.py`.

Then, you should register your api in the main application. To do this, first import your api in `src/app.py`, then register it. Here is the example for densenet, you can check the code in `app.py` for details.
```python
from api.densenet import densenet_api

...

app.register_blueprint(densenet_api)
```

Last but not least, you should test your api. Please write this part of code under the `test` directory. Alternatively, you can use GUI tools such as postman to test your api.
