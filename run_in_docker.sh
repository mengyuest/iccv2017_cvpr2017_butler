HOSTPATH=$PWD/cvpr_lib@docker
BASEDIR=/docker_cvpr

echo HOSTPATH=${HOSTPATH}

sudo docker build -t cvpr2017_butler .

echo BASEDIR=${BASEDIR}
sudo docker run --rm -it --net=host -v /etc/localtime:/etc/localtime:ro -v ${HOSTPATH}:${BASEDIR}/cvpr_lib@local  cvpr2017_butler


