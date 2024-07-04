#!/bin/bash

cd /Users/keru/Desktop/uni/internship/proj/back

uvicorn main:app --reload &

cd /Users/keru/Desktop/uni/internship/proj/front

npm run dev