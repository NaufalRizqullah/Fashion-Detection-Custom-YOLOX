# Fashion Object Detection using YOLOX


To run this server, using this line
```python
uvicorn services.main:app --reload
```

To run this server, using gunicorn this line
```shell
gunicorn services.main:app -w 4 -k uvicorn.workers.UvicornWorker
```
- -w, --workers = number of workers process
- -k, --worker-class =  the type worker process to run


clone YOLOX, and after that install the dependencies

```shell
git clone https://github.com/Megvii-BaseDetection/YOLOX
```