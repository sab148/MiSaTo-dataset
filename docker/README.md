
## Pull the existing image 
We recommend to pull our misato image from Dockerhub. 

## Create your own image
You can create a docker image using the given Dockerfile. Before you build the image please download ambertools from https://ambermd.org/GetAmber.php#ambertools and place the tar.gz file into this folder.


```
sudo docker build -t misato .
```

To build a singularity container from the docker image run the following:

```
sudo docker build -t local/misato:latest .
sudo singularity build pyg.sif docker-daemon://local/misato:latest
```