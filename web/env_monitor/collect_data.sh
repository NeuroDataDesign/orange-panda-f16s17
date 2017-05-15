#!/bin/bash

./runonesub.sh /data/BNU_sub/session_1/rest_1/rest.nii.gz /data/BNU_sub/session_1/anat_1/anat.nii.gz /data/BNU_sub/BNU_single > /data/BNU_sub/BNU_single/out.txt

sleep 30

./runonesub.sh /data/DC_sub/session_1/rest_1/rest.nii.gz /data/DC_sub/session_1/anat_1/anat.nii.gz /data/DC_sub/DC_single > /data/DC_sub/DC_single/out.txt

sleep 30

./runonesub.sh /data/HNU_sub/session_1/rest_1/rest.nii.gz /data/HNU_sub/session_1/anat_1/anat.nii.gz /data/HNU_sub/HNU_single > /data/HNU_sub/HNU_single/out.txt

sleep 30

./runonesub.sh /data/NKI_sub/session_1/rest_1400_1/rest.nii.gz /data/NKI_sub/session_1/anat_1/anat.nii.gz /data/NKI_sub/NKI_single > /data/NKI_sub/NKI_single/out.txt

./runonesub.sh /data/sol/sub-15/anat/sub-15_anat.nii.gz /data/sol/sub-15/func/sub-15_run1.nii.gz /data/sol/sol_single > /data/sol/sol_single/out.txt

sleep 30

