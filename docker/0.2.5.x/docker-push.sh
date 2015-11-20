#!/bin/bash
docker push usharesoft/hammr:0.2.5.8
docker tag -f usharesoft/hammr:0.2.5.8 usharesoft/hammr:latest
docker push usharesoft/hammr:latest
