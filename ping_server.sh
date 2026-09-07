#!/bin/bash

# Responsible for pinging a single server and determining its stats

NPINGS=4

ping -c $NPINGS $1
