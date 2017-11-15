# Math-in-the-Middle Docker Proof of Concept
## Building
To build the demo, do:

$ docker build .

## Obtaining the ID of the image
After the build, run:

$ docker images

which will show, among others, the ID of the latest image.

## Running
To run the demo:

$ docker run -ti --name mitm --memory="500MB" -p 8888:8888 imageID

Where imageID is the ID of the image. The link to the jupyter notebook will be printed to output.

## Cleaning up
After running the demo, run:

$ docker rm mitm

To prevent naming conflicts in later runs.
