#!/bin/bash -x

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

START_DIR="${1}"
if [ -z "${START_DIR}" ]; then
    echo "Please provide a start directory of .txt files."
    exit 1
fi

OUT_DIR="${2}"
if [ -z "${OUT_DIR}" ]; then
    echo "Please provide an output directory of .txt files."
    exit 1
fi

FOOTER="${3}"
GIT_HASH="${4}"

txtOutDir="${START_DIR}"
yamlOutDir="/tmp/yamlOutDir"
#mkdir -p ${txtOutDir}
rm -rf ${yamlOutDir}
mkdir -p ${yamlOutDir}
#python3 ${SCRIPT_DIR}/pullPagesFromDatabase.py ${START_FILE} ${txtOutDir}
for FILE in ${txtOutDir}/*; do
    f="$(basename -- $FILE)"
    mwtoast -i ${FILE} > ${yamlOutDir}/${f}.yaml
done

htmlOutDir="${OUT_DIR}"
rm -rf ${htmlOutDir}/*
mkdir -p ${htmlOutDir}
python3 ${SCRIPT_DIR}/wikiReconstructorTool.py -i ${yamlOutDir} -o ${htmlOutDir} ${FOOTER:+-f "$FOOTER"} ${GIT_HASH:+-g "$GIT_HASH"}
rm -rf ${yamlOutDir}
#rm -rf ${txtOutDir}
