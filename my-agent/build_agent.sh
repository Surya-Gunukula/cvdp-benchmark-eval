#!/bin/sh 

# SPDX-FileCopyrightText: Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

docker build -f Dockerfile-base --platform linux/amd64 -t cvdp-example-agent-base .
docker build -f Dockerfile-agent --platform linux/amd64 -t cvdp-example-agent --no-cache .
