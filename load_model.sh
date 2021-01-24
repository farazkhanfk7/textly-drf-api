#!/usr/bin/env bash
cd models/grammer_check

echo "Downloading Grammer BERT Models:"
fileid="1bfFRMEnWywP_1jW-5z66FO9iVUfGoh6t"
filename="pytorch_model.bin"
curl -c ./cookie -s -L "https://drive.google.com/uc?export=download&id=${fileid}" > /dev/null
curl -Lb ./cookie "https://drive.google.com/uc?export=download&confirm=`awk '/download/ {print $NF}' ./cookie`&id=${fileid}" -o ${filename}

cd ../../

cd models/sentiment
echo "Downloading Sentiment BERT Models:"
fileid="1LuGfTU18W99TA6XFb3g99kyIDRWw_kIr"
filename="pytorch_model.bin"
curl -c ./cookie -s -L "https://drive.google.com/uc?export=download&id=${fileid}" > /dev/null
curl -Lb ./cookie "https://drive.google.com/uc?export=download&confirm=`awk '/download/ {print $NF}' ./cookie`&id=${fileid}" -o ${filename}

cd ../../

cd models/text_gen
echo "Downloading TextGeneration GPT2 Models:"
fileid="1-RltGuP5NLez-lIyYhp-DlvvkyNpR_8m"
filename="pytorch_model.bin"
curl -c ./cookie -s -L "https://drive.google.com/uc?export=download&id=${fileid}" > /dev/null
curl -Lb ./cookie "https://drive.google.com/uc?export=download&confirm=`awk '/download/ {print $NF}' ./cookie`&id=${fileid}" -o ${filename}

cd ../../

cd models/translate
echo "Downloading Translation:"
fileid="1nEiRZnIRXaplftW1wSbuDq79qGwhpigZ"
filename="model.pt"
curl -c ./cookie -s -L "https://drive.google.com/uc?export=download&id=${fileid}" > /dev/null
curl -Lb ./cookie "https://drive.google.com/uc?export=download&confirm=`awk '/download/ {print $NF}' ./cookie`&id=${fileid}" -o ${filename}

cd ../../

pwd
ls
echo "Textly : Models downloaded"
echo "Please run Docker Container or start server"